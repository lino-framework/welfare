# -*- coding: UTF-8 -*-
# Copyright 2011-2019 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

"""Model mixins for `lino_welfare.modlib.cbss`. """

from builtins import str
import os
import traceback
import datetime
import logging

import six

logger = logging.getLogger(__name__)


from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

# from appy.shared.xml_parser import XmlUnmarshaller

from lino import mixins
from lino.api import dd

from lino.utils.ssin import ssin_validator

from lino.modlib.users.mixins import UserAuthored

from .utils import nodetext, xsdpath, CBSS_ENVS
from .choicelists import *


#~ try:

# import suds
from suds.client import Client
from suds.transport.http import HttpAuthenticated
from suds.transport.http import HttpTransport
from suds.sax.element import Element as E
from suds.sax.parser import Parser
PARSER = Parser()

from lino_xl.lib.excerpts.mixins import Certifiable

#~ except ImportError, e:
    #~ pass

_clients_dict = dict()


def get_client(obj):
    c = _clients_dict.get(obj.__class__, None)
    if c is not None:
        return c
    c = obj.create_client()
    _clients_dict[obj.__class__] = c
    return c





# class CBSSRequest(UserAuthored, mixins.Printable, mixins.Duplicable):
class CBSSRequest(UserAuthored, mixins.Duplicable, Certifiable):

    """
    Common Abstract Base Class for :class:`SSDNRequest`
    and :class:`NewStyleRequest`
    """

    workflow_state_field = 'status'

    wsdl_parts = NotImplementedError

    class Meta:
        abstract = True

    person = dd.ForeignKey(
        'pcsw.Client',
        verbose_name=_("Client"))

    sent = models.DateTimeField(
        verbose_name=_("Sent"),
        blank=True, null=True,
        editable=False,
        help_text="""\
The date and time when this request has been executed.
This is empty for requests than haven't been sent.
Read-only.""")

    status = RequestStates.field(editable=False, blank=True)
    environment = models.CharField(
        max_length=4, editable=False, verbose_name=_("T/A/B"))
    ticket = models.CharField(
        max_length=36, editable=False, verbose_name=_("Ticket"))
    #~ environment = Environment.field(blank=True,null=True)

    # will probably go away soon
    request_xml = models.TextField(verbose_name=_("Request"),
                                   editable=False, blank=True,
        help_text="""The raw XML string that has (or would have) been sent.""")

    response_xml = models.TextField(
        verbose_name=_("Response"),
        editable=False, blank=True,
        help_text="""\
The raw XML response received.
""")

    #~ logged_messages = models.TextField(
        #~ verbose_name=_("Logged messages"),
        #~ editable=False,blank=True,
        #~ help_text="""Logged messages about this request.""")

    debug_messages = models.TextField(
        verbose_name=_("Debug messages"),
        editable=False, blank=True)
    info_messages = models.TextField(
        verbose_name=_("Info messages"),
        editable=False, blank=True)

    #~ send_action = ExecuteRequest()
    #~ print_action = mixins.DirectPrintAction(required=dict(states=['ok','warnings']))
    if False:  # removed 20151021
        do_print = mixins.DirectPrintAction()

    def on_duplicate(self, ar, master):
        """When duplicating a CBSS request, we want re-execute it.  So please
        duplicate only the parameters, not the execution data like
        `ticket`, `sent` and `status`.  Note that also the `user` will
        be set to the user who asked to duplicate (because this is a
        subclass of `UserAuthored`.

        """
        self.user = ar.get_user()
        self.debug_messages = ''
        self.info_messages = ''
        self.ticket = ''
        self.response_xml = ''
        self.request_xml = ''
        self.sent = None
        #~ self.status = RequestStates.new
        self.status = ''  # RequestStates.blank_item
        self.environment = ''
        super(CBSSRequest, self).on_duplicate(ar, master)

    def get_row_permission(self, user, state, ba):
        """
        CBSS requests that have a `ticket` may never be modified.
        """
        #~ logger.info("20120622 CBSSRequest.get_row_permission %s %s", self.ticket, action.readonly)
        if self.ticket and not ba.action.readonly:
            return False
        return super(CBSSRequest, self).get_row_permission(user, state, ba)

    def on_cbss_ok(self, reply):
        """
        Called when a successful reply has been received.
        """
        pass

    #~ @classmethod
    #~ def setup_report(cls,rpt):
        # ~ # call_optional_super(CBSSRequest,cls,'setup_report',rpt)
        #~ rpt.add_action(ExecuteRequest())

    #~ def logmsg(self,s,*args):
        #~ if args:
            #~ s = s % args
        #~ self.logged_messages += ("[%s] " % datetime.datetime.now()) + s + '\n'

    def logmsg_debug(self, s, *args):
        if args:
            s = s % args
        self.debug_messages += ("[%s] " % datetime.datetime.now()) + s + '\n'

    def logmsg_info(self, s, *args):
        if args:
            s = s % args
        self.info_messages += s + '\n'

    def logmsg_warning(self, s, *args):
        if args:
            s = s % args
        self.info_messages += s + '\n'

    def __str__(self):
        return u"%s #%s" % (self._meta.verbose_name, self.pk)

    def after_ui_save(self, ar, cw):
        self.execute_request(ar)
        if self.status == RequestStates.failed:
            ar.set_response(message=self.debug_messages)
            ar.set_response(alert=True)
        elif self.status == RequestStates.warnings:
            ar.set_response(message=self.info_messages)
            #~ kw.update(message=_("Got valid response, but it contains warnings."))
            ar.set_response(alert=True)
        #~ kw.update(refresh=True)
        #~ return ar.success(**kw)
        #~ return kw

    def execute_request(self, ar=None, now=None,
                        simulate_response=None,
                        environment=None):
        """This is the common part of a request for both classic and
        new-style.

        """
        if self.ticket:
            raise Warning("Cannot re-execute %s with non-empty ticket." % self)
        if ar is not None:
            logger.info("%s executes CBSS request %s", ar.get_user(), self)
        if now is None:
            now = datetime.datetime.now()
        if environment is None:
            environment = settings.SITE.plugins.cbss.cbss_environment or ''

        self.environment = environment
        self.sent = now
        #~ self.logged_messages = ''
        self.debug_messages = ''
        self.info_messages = ''

        if not settings.SITE.plugins.cbss.cbss_live_requests:
            if simulate_response is None:  # and environment:
                self.validate_request()
                self.status = RequestStates.validated
                self.save()
                return

        self.status = RequestStates.sent
        self.save()

        retval = None
        try:
            retval = self.execute_request_(now, simulate_response)
        # except (IOError, Warning) as e:
        #     if self.ticket:
        #         self.status = RequestStates.errors
        #     else:
        #         self.status = RequestStates.failed
        #     # self.logmsg_debug(unicode(e))
        #     if six.PY2:
        #         self.logmsg_debug(traceback.format_exc(e))
        #     else:
        #         self.logmsg_debug(traceback.format_exc())
        except Exception as e:
            if self.ticket:
                self.status = RequestStates.errors
            else:
                self.status = RequestStates.failed
            #~ self.response_xml = traceback.format_exc(e)
            # self.logmsg_debug(traceback.format_exc(e))
            if six.PY2:
                self.logmsg_debug(traceback.format_exc(e))
            else:
                self.logmsg_debug(traceback.format_exc())

        self.save()
        return retval

    def validate_request(self):
        pass

    def get_wsdl_uri(self):
        url = os.path.join(settings.MEDIA_ROOT, *self.wsdl_parts)
        if not url.startswith('/'):
            # on a windows machine we need to prepend an additional "/"
            url = '/' + url
        if os.path.sep != '/':
            url = url.replace(os.path.sep, '/')
        url = 'file://' + url
        return url

    def check_environment(self, req):
#         if not self.environment:
#             raise Warning("""\
# Not actually sending because environment is empty. Request would be:
# """ + unicode(req))

        assert self.environment in CBSS_ENVS

    @dd.virtualfield(dd.HtmlBox(_("Result")))
    def result(self, ar):
        return self.response_xml

    def get_excerpt_options(self, ar, **kw):
        """When we print a request, the resulting excerpt should go to the
        client's history.

        """
        kw.update(project=self.person)
        return super(CBSSRequest, self).get_excerpt_options(ar, **kw)


#~ dd.update_field(CBSSRequest,'project',blank=False,null=False)
dd.update_field(CBSSRequest, 'user', blank=False, null=False)


class SSDNRequest(CBSSRequest):
    """Abstract Base Class for Models that represent SSDN ("classic")
    requests.

    """

    wsdl_parts = ('cache', 'wsdl', 'WebServiceConnector.wsdl')

    xsd_filename = None

    class Meta:
        abstract = True

    def validate_against_xsd(self, srvreq, xsd_filename):
        #~ logger.info("20120524 Validate against %s", xsd_filename)
        from lxml import etree
        xml = str(srvreq)
        #~ print xml
        doc = etree.fromstring(xml)
        schema_doc = etree.parse(xsd_filename)
        schema = etree.XMLSchema(schema_doc)
        #~ if not schema.validate(doc):
            #~ print xml
        schema.assertValid(doc)
        #~ self.logmsg("Validated %s against %s", xml,xsd_filename)
        self.logmsg_debug("Validated %s against %s", self, xsd_filename)

    def validate_wrapped(self, srvreq):
        self.validate_against_xsd(
            srvreq, xsdpath('SSDN', 'Service', 'SSDNRequest.xsd'))

    def validate_inner(self, srvreq):
        if not self.xsd_filename:
            return
        self.validate_against_xsd(srvreq, self.xsd_filename)

    def validate_request(self):
        """
        Validates the generated XML against the XSD files.
        Used by test suite.
        It is not necessary to validate each real request before actually sending it.
        """
        srvreq = self.build_request()
        self.validate_inner(srvreq)
        wrapped_srvreq = self.wrap_ssdn_request(
            srvreq, datetime.datetime.now())
        self.validate_wrapped(wrapped_srvreq)
        self.logmsg_info(_("Request has been validated against XSD files"))

    def create_client(self):
        url = self.get_wsdl_uri()
        #~ logger.info("Instantiate Client at %s", url)
        t = HttpTransport()
        client = Client(url, transport=t, timeout=10)
        #~ print 20120507, client
        return client

    def execute_request_(self, now, simulate_response):
        """
        SSDN specific part of a request.
        """
        srvreq = self.build_request()

        wrapped_srvreq = self.wrap_ssdn_request(srvreq, now)
        xmlString = str(wrapped_srvreq)
        self.request_xml = xmlString

        if simulate_response is not None:
            self.environment = 'demo'
            self.response_xml = str(simulate_response)
            return self.fill_from_string(simulate_response)

        # the normal case
        self.check_environment(srvreq)

        client = get_client(self)

        #~ logger.info("20120521 Gonna sendXML(<xmlString>):\n%s",xmlString)
        if not settings.SITE.plugins.cbss.cbss_live_requests:
            raise Warning(
                "NOT sending because `cbss_live_requests` is False:\n"
                + xmlString)
        #~ xmlString.append(wrapped_srvreq)
        self.logmsg_debug("client.service.sendXML(\n%s\n)", xmlString)
        res = client.service.sendXML(xmlString)
        #~ print 20120522, res
        self.response_xml = str(res)
        return self.fill_from_string(res.encode('utf-8'))

    def fill_from_string(self, s, sent_xmlString=None):
        #~ self.response_xml = unicode(res)
        reply = PARSER.parse(string=s).root()
        self.ticket = nodetext(
            reply.childAtPath('/ReplyContext/Message/Ticket'))
        rs = reply.childAtPath('/ServiceReply/ResultSummary')
        if rs is None:
            raise Warning("Missing ResultSummary in :\n%s" % reply)

        for dtl in rs.getChildren('Detail'):
        #~ for detail in rs.getChildren():
            # WARNING, INFO, ERROR...
            msg = nodetext(dtl.childAtPath('/Severity'))
            msg += " " + nodetext(dtl.childAtPath('/ReasonCode'))
            msg += " (%s) : " % nodetext(dtl.childAtPath('/AuthorCodeList'))
            msg += nodetext(dtl.childAtPath('/Diagnostic'))
            #~ print '========'
            #~ print msg
            #~ raise Warning(msg)
            self.logmsg_info(msg)

        rc = nodetext(rs.childAtPath('/ReturnCode'))
        #~ print reply.__class__, dir(reply)
        #~ print reply
        #~ rc = reply.root().SSDNReply.ServiceReply.ResultSummary.ReturnCode

        if rc == '0':
            self.status = RequestStates.ok
        elif rc == '1':
            self.status = RequestStates.warnings
            #~ self.logmsg_debug("Warnings:==============\n%s\n===============" % s)
        #~ elif rc == '10000':
            #~ self.status = RequestStates.errors
        else:
            self.status = RequestStates.errors
            #~ self.response_xml = unicode(reply)
            #~ dtl = rs.childAtPath('/Detail')
            #~ msg = CBSS_ERROR_MESSAGE % rc
            #~ keys = ('Severity', 'ReasonCode', 'Diagnostic', 'AuthorCodeList')
            #~ msg += '\n'.join([
                #~ k+' : '+nodetext(dtl.childAtPath('/'+k))
                    #~ for k in keys])
            #~ raise Warning(msg)
            #~ return None
            #~ raise Exception("Got invalid response status")

        #~ self.on_cbss_ok(reply)
        service_reply = self.get_service_reply(reply)
        if service_reply is None:
            raise Warning("Got response without service reply.")
            #~ raise Exception(
              #~ "Return code is %r, but there's no service reply." % rc)
              #~ "Return code is %r but there's no service reply in:\n%s\n" % (rc,reply))
        #~ reply.childAtPath('/ServiceReply/IdentifyPersonReply')
        self.response_xml = str(service_reply)
        return service_reply

    def get_service_reply(self, full_reply=None):
        raise NotImplementedError()

    def wrap_ssdn_request(self, srvreq, dt):
        """
        Wrap the given service request into the SSDN envelope
        by adding AuthorizedUser and other information common
        the all SSDN requests).
        """
        #~ up  = settings.SITE.ssdn_user_params
        #~ user_params = settings.SITE.cbss_user_params
        sc = settings.SITE.site_config
        #~ au = E('common:AuthorizedUser',ns=NSCOMMON)
        #~ au.append(E('common:UserID').setText(up['UserID']))
        #~ au.append(E('common:Email').setText(up['Email']))
        #~ au.append(E('common:OrgUnit').setText(up['OrgUnit']))
        #~ au.append(E('common:MatrixID').setText(up['MatrixID']))
        #~ au.append(E('common:MatrixSubID').setText(up['MatrixSubID']))
        au = E('ssdn:AuthorizedUser')
        #~ au.append(E('ssdn:UserID').setText(user_params['UserID']))
        au.append(E('ssdn:UserID').setText(sc.ssdn_user_id))
        #~ au.append(E('ssdn:Email').setText(user_params['Email']))
        #~ if not sc.site_company:
            #~ raise Exception("")
        #~ au.append(E('ssdn:Email').setText(sc.site_company.email))
        au.append(E('ssdn:Email').setText(sc.ssdn_email))
        #~ au.append(E('ssdn:OrgUnit').setText(user_params['OrgUnit']))
        #~ au.append(E('ssdn:OrgUnit').setText(sc.site_company.vat_id))
        au.append(E('ssdn:OrgUnit').setText(sc.cbss_org_unit))
        #~ au.append(E('ssdn:MatrixID').setText(user_params['MatrixID']))
        au.append(E('ssdn:MatrixID').setText(sc.sector.code))
        #~ au.append(E('ssdn:MatrixSubID').setText(user_params['MatrixSubID']))
        au.append(E('ssdn:MatrixSubID').setText(sc.sector.subcode))

        ref = "%s # %s" % (self.__class__.__name__, self.id)
        msg = E('ssdn:Message')
        msg.append(E('ssdn:Reference').setText(ref))
        msg.append(E('ssdn:TimeRequest').setText(dt.strftime("%Y%m%dT%H%M%S")))

        context = E('ssdn:RequestContext')
        context.append(au)
        context.append(msg)

        sr = E('ssdn:ServiceRequest')
        sr.append(E('ssdn:ServiceId').setText(self.ssdn_service_id))
        sr.append(E('ssdn:Version').setText(self.ssdn_service_version))
        sr.append(srvreq)

        #~ xg.set_default_namespace(SSDN)
        e = E('ssdn:SSDNRequest',
              ns=('ssdn', 'http://www.ksz-bcss.fgov.be/XSD/SSDN/Service'))
        e.append(context)
        e.append(sr)
        #~ if srvreq.prefix != e.prefix:
            #~ e.addPrefix(srvreq.prefix,srvreq.nsprefixes[srvreq.prefix])

        return e


class NewStyleRequest(CBSSRequest):

    """
    Abstract Base Class for Models that represent
    "new style" requests to the :term:`CBSS` (and responses).
    """

    class Meta:
        abstract = True

    def create_client(self):
        url = self.get_wsdl_uri()

        logger.debug("Instantiate CBSS client at %s", url)
        sc = settings.SITE.site_config
        #~ t = HttpAuthenticated(
            #~ username=settings.SITE.cbss_username,
            #~ password=settings.SITE.cbss_password)
        t = HttpAuthenticated(
            username=sc.cbss_http_username,
            password=sc.cbss_http_password)
        client = Client(url, transport=t, retxml=True)
        #~ print 20120613, client
        return client

    def execute_request_(self, now, simulate_response):
        """
        NewStyle specific part of a request.
        """
        client = get_client(self)
        client.add_prefix("common", "http://kszbcss.fgov.be/types/common/v3")

        # info = client.factory.create('ns0:InformationCustomerType')
        info = client.factory.create('common:InformationCustomerType')
        info.ticket = str(self.id)
        info.timestampSent = now

        # ci = client.factory.create('ns0:CustomerIdentificationType')
        ci = client.factory.create('common:OrganizationIdentificationType')
        #~ cbeNumber = client.factory.create('ns0:CbeNumberType')
        #~ ci.cbeNumber = settings.SITE.cbss_cbe_number
        #~ ci.cbeNumber = settings.SITE.site_config.site_company.vat_id
        ci.cbeNumber = settings.SITE.site_config.cbss_org_unit

        info.customerIdentification = ci

        return self.execute_newstyle(client, info, simulate_response)

    def on_cbss_ok(self, reply):
        """
        Called when a successful reply has been received.
        """
        pass

    #~ def __unicode__(self):
        # ~ return u"%s#%s" % (self.__class__.__name__,self.pk)

    def get_service_reply(self):
        #~ """
    #~ Example of a reply::

    #~ (reply){
       #~ informationCustomer =
          #~ (InformationCustomerType){
             #~ ticket = "1"
             #~ timestampSent = 2012-05-23 09:24:55.316312
             #~ customerIdentification =
                #~ (CustomerIdentificationType){
                   #~ cbeNumber = "0123456789"
                #~ }
          #~ }
       #~ informationCBSS =
          #~ (InformationCBSSType){
             #~ ticketCBSS = "f11736b3-97bc-452a-a75c-16fcc2a2f6ae"
             #~ timestampReceive = 2012-05-23 08:24:37.000385
             #~ timestampReply = 2012-05-23 08:24:37.000516
          #~ }
       #~ status =
          #~ (StatusType){
             #~ value = "NO_RESULT"
             #~ code = "MSG00008"
             #~ description = "A validation error occurred."
             #~ information[] =
                #~ (InformationType){
                   #~ fieldName = "ssin"
                   #~ fieldValue = "12345678901"
                #~ },
          #~ }
       #~ searchInformation =
          #~ (SearchInformationType){
             #~ ssin = "12345678901"
             #~ language = "de"
             #~ history = False
          #~ }
     #~ }
        #~ """
        if not self.response_xml:
            return None
        client = get_client(self).service
        #~ print '20120613b', dir(client)
        return client.succeeded(client.method.binding.input, self.response_xml)

    def execute_newstyle(self, client, infoCustomer, simulate_response):
        raise NotImplementedError()


class SSIN(dd.Model):

    """
    Abstract base for Requests that have a field `national_id` and a method
    :meth:`get_ssin`.
    """
    class Meta:
        abstract = True

    national_id = models.CharField(
        max_length=200,
        blank=True, verbose_name=_("National ID"),
        validators=[ssin_validator])

    def get_ssin(self):
        national_id = self.national_id.replace('=', '')
        national_id = national_id.replace(' ', '')
        national_id = national_id.replace('-', '')
        return national_id

    #~ def save(self,*args,**kw):
        #~ if self.person_id and not self.last_name:
            #~ self.fill_from_person(self.person)
        #~ super(SSIN,self).save(*args,**kw)

    def on_create(self, ar):
        #~ print '20120629 SSIN.on_create', dd.obj2str(self), ar
        #~ super(ContractBase,self).on_create(request)
        self.person_changed(ar)
        super(SSIN, self).on_create(ar)

    def person_changed(self, ar):
        #~ raise Exception("20120704")
        #~ print '20120704 person_changed'
        if self.person_id:
            self.fill_from_person(self.person)

    def fill_from_person(self, person):
        self.national_id = person.national_id


class WithPerson(SSIN):

    """
    Mixin for models that have certain fields
    """
    class Meta:
        abstract = True

    birth_date = dd.IncompleteDateField(
        blank=True,
        verbose_name=_("Birth date"))

    sis_card_no = models.CharField(verbose_name=_('SIS card number'),
                                   max_length=10,
        blank=True, help_text="""\
The number of the SIS card used to authenticate the person.""")

    id_card_no = models.CharField(verbose_name=_('ID card number'),
                                  max_length=20,
        blank=True, help_text="""\
The number of the ID card used to authenticate the person.""")

    first_name = models.CharField(max_length=200,
                                  blank=True,
                                  verbose_name=_('First name'))
    "Space-separated list of all first names."

    last_name = models.CharField(max_length=200,
                                 blank=True,
                                 verbose_name=_('Last name'))
    """Last name (family name)."""

    def fill_from_person(self, person):
        self.national_id = person.national_id
        self.id_card_no = person.card_number
        self.last_name = person.last_name
        self.first_name = person.first_name
        self.birth_date = person.birth_date
        #~ print '20120603 fill_from_person', self.national_id
