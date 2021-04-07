# -*- coding: UTF-8 -*-
# Copyright 2011-2019 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)


from builtins import str
import os
import shutil
import logging ; logger = logging.getLogger(__name__)

from suds import WebFault

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


from lino import mixins
from lino.api import dd
from lino.utils import assert_pure


from lino_welfare.modlib.pcsw import models as pcsw

from .mixins import E, PARSER, get_client
from .mixins import SSDNRequest, WithPerson, NewStyleRequest, SSIN
from .utils import xsdpath, CBSS_ENVS, gender2cbss

from .choicelists import (RequestStates, ManageActions,
                          QueryRegisters, RequestLanguages)

CBSS_ERROR_MESSAGE = "CBSS error %s:\n"



class Sector(mixins.BabelNamed):

    class Meta:
        app_label = 'cbss'
        verbose_name = _("Sector")
        verbose_name_plural = _("Sectors")
        unique_together = ['code', 'subcode']

    # code = models.CharField(max_length=2,verbose_name=_("Code"),primary_key=True)
    code = models.IntegerField(_("Code"))
    subcode = models.IntegerField(_("Subcode"), default=0)
    abbr = dd.BabelCharField(_("Abbreviation"), max_length=50, blank=True)

    def __str__(self):
        if self.subcode != 0:
            return str(self.code) + '.' + str(self.subcode) + \
                ' - ' + dd.babelattr(self, 'name')
        return str(self.code) + ' - ' + dd.babelattr(self, 'name')



class Purpose(mixins.BabelNamed):

    class Meta:
        app_label = 'cbss'
        verbose_name = _("Purpose")
        verbose_name_plural = _('Purposes')
        unique_together = ['sector_code', 'code']
    sector_code = models.IntegerField(_("Sector"), blank=True, null=True)
    # sector_subcode = models.IntegerField(max_length=2,verbose_name=_("Subsector"),blank=True,null=True)
    # sector = dd.ForeignKey(Sector,blank=True,null=True)
    # code = models.CharField(max_length=3,verbose_name=_("Code"))
    code = models.IntegerField(_("Code"))

    def __str__(self):
        # return '(' + str(self.code) + ') ' + mixins.BabelNamed.__str__(self)
        return str(self.code) + ' - ' + dd.babelattr(self, 'name')


NSCOMMON = ('common', 'http://www.ksz-bcss.fgov.be/XSD/SSDN/Common')
NSIPR = ('ipr',
         "http://www.ksz-bcss.fgov.be/XSD/SSDN/OCMW_CPAS/IdentifyPerson")
NSMAR = ('mar', "http://www.ksz-bcss.fgov.be/XSD/SSDN/OCMW_CPAS/ManageAccess")
NSWSC = ('wsc', "http://ksz-bcss.fgov.be/connectors/WebServiceConnector")


class IdentifyPersonRequest(SSDNRequest, WithPerson):

    ssdn_service_id = 'OCMWCPASIdentifyPerson'
    ssdn_service_version = '20050930'
    xsd_filename = xsdpath('SSDN', 'OCMW_CPAS',
                           'IdentifyPerson', 'IdentifyPersonRequest.xsd')

    class Meta:
        app_label = 'cbss'
        verbose_name = _("IdentifyPerson Request")
        verbose_name_plural = _("IdentifyPerson Requests")

    middle_name = models.CharField(max_length=200,
                                   blank=True,
                                   verbose_name=_('Middle name'),
                                   help_text="Whatever this means...")

    gender = dd.Genders.field(blank=True)

    tolerance = models.IntegerField(verbose_name=_('Tolerance'),
                                    default=0,
      help_text=u"""
      Falls Monat oder Tag des Geburtsdatums unbekannt sind,
      um wieviel Monate bzw. Tage die Suche nach unten/oben ausgeweitet wird.
      Gültige Werte: 0 bis 10.
      """)
      # 20120606 gridcolumn doesn't like tooltips containing HTML
      # <p>Zum Beispiel
      # <table border=1 class="htmlText">
      # <tr>
        # <td>Geburtsdatum</td>
        # <td colspan="3">Toleranz</td>
      # </tr><tr>
        # <td></td>
        # <td>0</td>
        # <td>1</td>
        # <td>10</td>
      # </tr><tr>
        # <td> 1968-00-00  </td>
        # <td> im Jahr 1968 </td>
        # <td> von 1967 bis 1969 </td>
        # <td> 1958 bis 1978 </td>
      # </tr><tr>
        # <td> 1968-06-00  </td>
        # <td> im Juni 1968 </td>
        # <td> von Mai  bis Juli 1968 </td>
        # <td>von Oktober 1967 bis April 1969</td>
      # </tr>
      # </table>
      # </p>

    # def on_create(self,ar):
        # UserAuthored.on_create(self,ar)
        # SSIN.on_create(self,ar)
    def get_result_table(self, ar):
        return ar.spawn(IdentifyPersonResult, master_instance=self)

    def fill_from_person(self, person):
        self.national_id = person.national_id
        self.id_card_no = person.card_number
        self.birth_date = person.birth_date
        if not self.national_id:
            self.gender = person.gender
            self.last_name = person.last_name
            self.first_name = person.first_name

    def build_request(self):
        """Construct and return the root element of the (inner) service request."""
        # if not self.birth_date:
            # raise Warning("Empty birth date (a full_clean() would have told that, too!)")
            # raise Warning(_("Birth date may not be empty."))

        national_id = self.get_ssin()
        gender = gender2cbss(self.gender)
        # ~ https://fedorahosted.org/suds/wiki/TipsAndTricks#IncludingLiteralXML
        main = E('ipr:IdentifyPersonRequest', ns=NSIPR)
        sc = E('ipr:SearchCriteria')
        main.append(sc)
        if national_id:
            # VerificatioinData is ignored if there's no SSIN in the
            # SearchCriteria
            sc.append(E('ipr:SSIN').setText(national_id))

            vd = E('ipr:VerificationData')
            main.append(vd)
            if self.sis_card_no:
                vd.append(E('ipr:SISCardNumber').setText(self.sis_card_no))
            if self.id_card_no:
                vd.append(E('ipr:IdentityCardNumber').setText(self.id_card_no))

            pd = E('ipr:PersonData')
            vd.append(pd)
            # if not self.last_name or not self.first_name:
                # raise Warning("Fields last_name and first_name are mandatory.")
            pd.append(E('ipr:LastName').setText(self.last_name))
            pd.append(E('ipr:FirstName').setText(self.first_name))
            pd.append(E('ipr:MiddleName').setText(self.middle_name))
            pd.append(E('ipr:BirthDate').setText(str(self.birth_date)))
            # if not self.birth_date.is_complete():
                # pd.append(E('ipr:Tolerance').setText(self.tolerance))
            # if gender is not None: pd.append(E('ipr:Gender').setText(gender))
        pc = E('ipr:PhoneticCriteria')
        sc.append(pc)
        pc.append(E('ipr:LastName').setText(self.last_name))
        pc.append(E('ipr:FirstName').setText(self.first_name))
        pc.append(E('ipr:MiddleName').setText(self.middle_name))
        pc.append(E('ipr:BirthDate').setText(str(self.birth_date)))
        return main

    def get_service_reply(self, full_reply=None):
        if full_reply is not None:
            return full_reply.childAtPath('/ServiceReply/IdentifyPersonReply')
        return PARSER.parse(string=self.response_xml.encode('utf-8')).root()
        # return reply

        # if False:

            # try:
                # res = self.cbss_namespace.execute(srvreq,str(self.id),now)
            # except cbss.Warning,e:
                # self.status = RequestStates.exception
                # self.response_xml = unicode(e)
                # self.save()
                # return
            # except Exception,e:
                # self.status = RequestStates.exception
                # self.response_xml = traceback.format_exc(e)
                # self.save()
                # return
            # self.sent = now
            # self.response_xml = res.data.xmlString
            # reply = cbss.xml2reply(res.data.xmlString)
            # rc = reply.ServiceReply.ResultSummary.ReturnCode
            # if rc == '0':
                # self.status = RequestStates.ok
            # elif rc == '1':
                # self.status = RequestStates.warnings
            # elif rc == '10000':
                # self.status = RequestStates.errors
            # self.save()

            # if self.status != RequestStates.ok:
                # msg = '\n'.join(list(cbss.reply2lines(reply)))
                # raise Exception(msg)

            # self.on_cbss_ok(reply)


dd.update_field(IdentifyPersonRequest, 'birth_date', blank=False)
"""
DocumentInvalid
Element '{http://www.ksz-bcss.fgov.be/XSD/SSDN/OCMW_CPAS/IdentifyPerson}BirthDate': [facet 'length'] The value has a length of '0'; this differs from the allowed length of '10'., line 7

"""
# dd.update_field(IdentifyPersonRequest,'first_name',blank=True)
# dd.update_field(IdentifyPersonRequest,'last_name',blank=True)


class ManageAccessRequest(SSDNRequest, WithPerson):

    ssdn_service_id = 'OCMWCPASManageAccess'
    ssdn_service_version = '20050930'

    xsd_filename = xsdpath('SSDN', 'OCMW_CPAS',
                           'ManageAccess', 'ManageAccessRequest.xsd')

    class Meta:
        app_label = 'cbss'
        verbose_name = _("ManageAccess Request")
        verbose_name_plural = _("ManageAccess Requests")

    # purpose = models.IntegerField(verbose_name=_('Purpose'),
      # default=0,help_text="""\
# The purpose for which the inscription needs to be
# registered/unregistered or listed.
# For listing this field is optional,
# for register/unregister it is obligated.""")

    # sector = models.IntegerField(verbose_name=_('Sector'),
      # blank=False,default=0,help_text="""\
# For register and unregister this element is ignored.
# It can be used for list,
# when information about sectors is required.""")

    sector = dd.ForeignKey(
        'cbss.Sector', # on_delete=models.PROTECT,
        editable=False, help_text="""\
For register and unregister this element is ignored.
It can be used for list,
when information about sectors is required.""")

    purpose = dd.ForeignKey(
        'cbss.Purpose',
        # blank=True,null=True,
        help_text="""\
The purpose for which the inscription needs to be
registered/unregistered or listed.
For listing this field is optional,
for register/unregister it is mandatory.""")

    start_date = models.DateField(
        # blank=True,null=True,
        verbose_name=_("Period from"))
    end_date = models.DateField(
        # blank=True,null=True,
        verbose_name=_("Period until"))

    # 20120527 : Django converts default value to unicode. didnt yet
    # understand why.
    action = ManageActions.field(
        blank=False, default=ManageActions.as_callable('LIST'))
    query_register = QueryRegisters.field(
        blank=False, default=QueryRegisters.as_callable('ALL'))
    # action = ManageActions.field(blank=False)
    # ~ query_register = QueryRegisters.field(blank=False) # ,default=QueryRegisters.ALL.as_callable)

    def save(self, *args, **kw):
        if not self.sector_id:
            self.sector = settings.SITE.site_config.sector
        super(ManageAccessRequest, self).save(*args, **kw)

    @dd.chooser()
    def purpose_choices(cls, sector):
        if not sector:
            sector = settings.SITE.site_config.sector
        if not sector:
            raise Exception("SiteConfig.sector is not set!")
        Q = models.Q
        return Purpose.objects.filter(
            Q(sector_code=sector.code) | Q(sector_code__isnull=True)).order_by('code')

    def build_request(self):
        """Construct and return the root element of the (inner) service request."""
        national_id = self.get_ssin()
        main = E('mar:ManageAccessRequest', ns=NSMAR)
        main.append(E('mar:SSIN').setText(national_id))
        # main.append(E('mar:Purpose').setText(str(self.purpose)))
        if self.purpose_id:
            main.append(E('mar:Purpose').setText(str(self.purpose.code)))
        period = E('mar:Period')
        main.append(period)
        period.append(E('common:StartDate', ns=NSCOMMON)
                      .setText(str(self.start_date)))
        if self.end_date:
            period.append(E('common:EndDate', ns=NSCOMMON)
                          .setText(str(self.end_date)))
        main.append(E('mar:Action').setText(self.action.name))
        main.append(E('mar:Sector').setText(str(self.sector.code)))
        if self.query_register:
            main.append(E('mar:QueryRegister')
                        .setText(self.query_register.name))
        proof = E('mar:ProofOfAuthentication')
        main.append(proof)
        if self.sis_card_no:
            proof.append(E('mar:SISCardNumber').setText(self.sis_card_no))
        if self.id_card_no:
            proof.append(E('mar:IdentityCardNumber').setText(self.id_card_no))
        if self.last_name or self.first_name or self.birth_date:
            pd = E('mar:PersonData')
            proof.append(pd)
            pd.append(E('mar:LastName').setText(self.last_name))
            pd.append(E('mar:FirstName').setText(self.first_name))
            pd.append(E('mar:BirthDate').setText(self.birth_date))
        return main

    def get_service_reply(self, full_reply=None):
        """
        Extract the "service reply" part from a full reply.
        Example of a full reply::

         <ServiceReply>
            <ns2:ResultSummary xmlns:ns2="http://www.ksz-bcss.fgov.be/XSD/SSDN/Common" ok="YES">
               <ns2:ReturnCode>0</ns2:ReturnCode>
            </ns2:ResultSummary>
            <ServiceId>OCMWCPASManageAccess</ServiceId>
            <Version>20050930</Version>
            <ns3:ManageAccessReply xmlns:ns3="http://www.ksz-bcss.fgov.be/XSD/SSDN/OCMW_CPAS/ManageAccess">
               <ns3:OriginalRequest>
                  <ns3:SSIN>68060105329</ns3:SSIN>
                  <ns3:Purpose>1</ns3:Purpose>
                  <ns3:Period>
                     <ns4:StartDate xmlns:ns4="http://www.ksz-bcss.fgov.be/XSD/SSDN/Common">2012-05-24+02:00</ns4:StartDate>
                     <ns5:EndDate xmlns:ns5="http://www.ksz-bcss.fgov.be/XSD/SSDN/Common">2012-05-24+02:00</ns5:EndDate>
                  </ns3:Period>
                  <ns3:Action>REGISTER</ns3:Action>
               </ns3:OriginalRequest>
               <ns3:Registrations>
                  <ns3:Purpose>1</ns3:Purpose>
                  <ns3:Period>
                     <ns6:StartDate xmlns:ns6="http://www.ksz-bcss.fgov.be/XSD/SSDN/Common">2012-05-24+02:00</ns6:StartDate>
                     <ns7:EndDate xmlns:ns7="http://www.ksz-bcss.fgov.be/XSD/SSDN/Common">2012-05-24+02:00</ns7:EndDate>
                  </ns3:Period>
                  <ns3:OrgUnit>63023</ns3:OrgUnit>
                  <ns3:Register>SECONDARY</ns3:Register>
               </ns3:Registrations>
            </ns3:ManageAccessReply>
         </ServiceReply>
        """
        if full_reply is not None:
            return full_reply.childAtPath('/ServiceReply/ManageAccessReply')
        return PARSER.parse(string=self.response_xml.encode('utf-8')).root()


dd.update_field(ManageAccessRequest, 'national_id', blank=False, help_text="""\
The SSIN of the person to register/unregister/list.
""")


##
## RetrieveTIGroupsRequest ("Transaction 25")
##

def reply_has_result(reply):
    if reply.status.value == "NO_RESULT":
        msg = CBSS_ERROR_MESSAGE % reply.status.code
        keys = ('value', 'code', 'description')
        msg += '\n'.join([
            k + ' : ' + getattr(reply.status, k)
            for k in keys])
        if hasattr(reply.status, 'information'):
            for i in reply.status.information:
                msg += "\n- %s = %s" % (i.fieldName, i.fieldValue)
        raise Warning(msg)


class RetrieveTIGroupsRequest(NewStyleRequest, SSIN):

    class Meta:
        app_label = 'cbss'
        verbose_name = _("Tx25 Request")
        verbose_name_plural = _('Tx25 Requests')

    wsdl_parts = ('cache', 'wsdl', 'RetrieveTIGroups.wsdl')

    language = RequestLanguages.field(
        blank=True,
        default=RequestLanguages.as_callable('fr'))
    history = models.BooleanField(
        verbose_name=_("History"), default=True,
        help_text="Whatever this means.")

    def get_print_language(self):
        if settings.SITE.get_language_info(self.language.value):
            return self.language.value
        return settings.SITE.DEFAULT_LANGUAGE.django_code

    def fill_from_person(self, person):
        """Fill default values for some fields of this request from the person
        (pcsw.Client).

        - The `national_id` is always taken

        - The person's `language` is taken if it is one of the
          possible `RequestLanguages`

        """
        self.national_id = person.national_id
        # The request's language as a Choice instance:
        rlc = RequestLanguages.get_by_value(person.language, None)
        if rlc:
            self.language = rlc

    def get_service_reply(self, **kwargs):
        assert_pure(self.response_xml)
        client = get_client(self)
        meth = client.service.retrieveTI
        clientclass = meth.clientclass(kwargs)
        client = clientclass(meth.client, meth.method)
        # print 20120613, portSelector[0]
        # print '20120613b', dir(client)
        s = self.response_xml.encode('utf-8')
        return client.succeeded(client.method.binding.input, s)

    def execute_newstyle(self, client, infoCustomer, simulate_response):
        client.add_prefix("rtg", "http://kszbcss.fgov.be/types/RetrieveTIGroups/v2")
        si = client.factory.create('rtg:SearchInformationType')
        si.ssin = self.get_ssin()
        if self.language:
            si.language = self.language.value
        si.history = self.history
        if simulate_response is not None:
            self.environment = 'demo'
            self.response_xml = simulate_response
        else:
            self.check_environment(si)
            try:
                # The arguments to be used here are defined for the
                # RetrieveTIGroupsRequestType sequence which in
                # RetrieveTIGroupsV5.xsd has the following children:
                # (1) informationCustomer
                # (2) informationCBSS (minOccurs=0)
                # (3) legalContext (minOccurs=0)
                # (4) searchInformation

                # This sequence is important because suds uses it when
                # adding positional arguments as children to the XML
                # request.

                # The optional "legalContext" argument had been added
                # by CBSS in V5.
                # 20190615 legalContext is mandatory since v2
                legalContext = "PCSA:SOCIAL_INQUIRY"  # LegalContextType is str
                # reply = client.service.retrieveTI(infoCustomer, None, si)
                reply = client.service.retrieveTI(infoCustomer, None, legalContext, si)
                # reply = client.service.retrieveTI(
                #     informationCustomer=infoCustomer,
                #     searchInfdormation=si)
            except WebFault as e:
                """
                Example of a SOAP fault:
          <soapenv:Fault>
             <faultcode>soapenv:Server</faultcode>
             <faultstring>An error occurred while servicing your request.</faultstring>
             <detail>
                <v1:retrieveTIGroupsFault>
                   <informationCustomer xmlns:ns0="http://kszbcss.fgov.be/intf/RetrieveTIGroupsService/v1" xmlns:ns1="http://schemas.xmlsoap.org/soap/envelope/">
                      <ticket>2</ticket>
                      <timestampSent>2012-05-23T10:19:27.636628+01:00</timestampSent>
                      <customerIdentification>
                         <cbeNumber>0212344876</cbeNumber>
                      </customerIdentification>
                   </informationCustomer>
                   <informationCBSS>
                      <ticketCBSS>f4b9cabe-e457-4f6b-bfcc-00fe258a9b7f</ticketCBSS>
                      <timestampReceive>2012-05-23T08:19:09.029Z</timestampReceive>
                      <timestampReply>2012-05-23T08:19:09.325Z</timestampReply>
                   </informationCBSS>
                   <error>
                      <severity>FATAL</severity>
                      <reasonCode>MSG00003</reasonCode>
                      <diagnostic>Unexpected internal error occurred</diagnostic>
                      <authorCode>http://www.bcss.fgov.be/en/international/home/index.html</authorCode>
                   </error>
                </v1:retrieveTIGroupsFault>
             </detail>
          </soapenv:Fault>
                """

                msg = CBSS_ERROR_MESSAGE % e.fault.faultstring
                msg += str(e.document)
                self.status = RequestStates.failed
                raise Warning(msg)
            self.response_xml = reply.decode('utf-8')  # 20130201

        # self.response_xml = unicode(reply)
        reply = self.get_service_reply()
        self.ticket = reply.informationCBSS.ticketCBSS
        self.status = RequestStates.warnings

        reply_has_result(reply)

        self.status = RequestStates.ok
        # self.response_xml = str(res)
        # self.response_xml = "20120522 %s %s" % (res.__class__,res)
        # print 20120523, res.informationCustomer
        # print self.response_xml
        return reply

    def Result(self, ar):
        return ar.spawn(RetrieveTIGroupsResult, master_instance=self)


@dd.receiver(dd.pre_analyze)
def customize_system(sender, **kw):

    dd.inject_field('system.SiteConfig',
                    'sector',
                    dd.ForeignKey(Sector,
                                      blank=True, null=True,
            help_text="""\
    The CBSS sector/subsector of the requesting organization.
    For PCSWs this is always 17.1.
    Used in SSDN requests as text of the `MatrixID` and `MatrixSubID`
    elements of `AuthorizedUser`.
    Used in ManageAccess requests as default value
    for the non-editable field `sector`
    (which defines the choices of the `purpose` field).
    """))

    dd.inject_field('system.SiteConfig',
                    'cbss_org_unit',
                    models.CharField(_("Requesting organisation"),
                                     max_length=50,
                                     blank=True,
          help_text="""\
    In CBSS requests, identifies the requesting organization.
    For PCSWs this is the enterprise number
    (CBE, KBO) and should have 10 digits and no formatting characters.

    Used in SSDN requests as text of the `AuthorizedUser\OrgUnit` element .
    Used in new style requests as text of the `CustomerIdentification\cbeNumber` element .
    """))
    dd.inject_field(
        'system.SiteConfig', 'ssdn_user_id', models.CharField(
            _("SSDN User Id"), max_length=50,
            blank=True,
            help_text="Used in SSDN requests as text of "\
            "the `AuthorizedUser\\UserID` element."))
    dd.inject_field(
        'system.SiteConfig', 'ssdn_email', models.EmailField(
            _("SSDN email address"),
            blank=True,
            help_text="Used in SSDN requests as text of "\
            "the `AuthorizedUser\\Email` element."))
    dd.inject_field(
        'system.SiteConfig', 'cbss_http_username',
        models.CharField(
            _("HTTP username"), max_length=50, blank=True,
            help_text="""\
            Used in the http header of new-style requests.
            """))
    dd.inject_field(
        'system.SiteConfig', 'cbss_http_password',
        models.CharField(
            _("HTTP password"), max_length=50, blank=True,
            help_text="Used in the http header of new-style requests."))


@dd.receiver(dd.pre_analyze)
def customize_pcsw(sender, **kw):

    dd.inject_quick_add_buttons(
        pcsw.Client, 'cbss_identify_person', IdentifyRequestsByPerson)
    dd.inject_quick_add_buttons(
        pcsw.Client, 'cbss_manage_access', ManageAccessRequestsByPerson)
    dd.inject_quick_add_buttons(
        pcsw.Client, 'cbss_retrieve_ti_groups',
        RetrieveTIGroupsRequestsByPerson)


def cbss_summary(self, ar):
    """
    returns a summary overview of the CBSS requests for this person.
    """
    if ar is None:
        return ''
    html = u'<p><ul>'
    for t in (IdentifyRequestsByPerson, ManageAccessRequestsByPerson,
              RetrieveTIGroupsRequestsByPerson):
        n = ar.spawn(t, master_instance=self).get_total_count()
        if n > 0:
            html += "<li>%d %s</li>" % (
                n, str(t.model._meta.verbose_name_plural))
    html += '</ul></p>'
    return ar.html_text(html)
    # return html

dd.inject_field(pcsw.Client,
                'cbss_summary',
                dd.VirtualField(dd.HtmlBox(_("CBSS summary")), cbss_summary))


def setup_site_cache(self, force):
    """Called from
    :meth:`lino.modlib.extjs.ext_renderer.Renderer.build_site_cache`.
    First argument is the `Site` instance.

    """

    import logging
    logger = logging.getLogger(__name__)

    environment = settings.SITE.plugins.cbss.cbss_environment
    if not environment:
        return  # silently return

    if environment not in CBSS_ENVS:
        raise Exception(
            "Invalid `cbss_environment` %r: must be empty or one of %s." % (
                environment, CBSS_ENVS))

    context = dict(cbss_environment=environment)

    def make_wsdl(template, parts):
        fn = os.path.join(settings.MEDIA_ROOT, *parts)
        if not force and os.path.exists(fn):
            if os.stat(fn).st_mtime > self.kernel.code_mtime:
                logger.debug(
                    "NOT generating %s because it is newer than the code.", fn)
                return
        s = open(os.path.join(os.path.dirname(__file__), 'WSDL', template)
                 ).read()
        s = s % context
        settings.SITE.makedirs_if_missing(os.path.dirname(fn))
        open(fn, 'wt').write(s)
        logger.debug("Generated %s for environment %r.", fn, environment)

    # v1 was stopped in March 2019
    # make_wsdl('RetrieveTIGroups-v1.wsdl', RetrieveTIGroupsRequest.wsdl_parts)
    make_wsdl('RetrieveTIGroups-v2.wsdl', RetrieveTIGroupsRequest.wsdl_parts)
    make_wsdl('WebServiceConnector.wsdl', SSDNRequest.wsdl_parts)
    # make_wsdl('TestConnectionService.wsdl',TestConnectionRequest.wsdl_parts)

    # The following xsd files are needed, unmodified but in the same directory
    # for fn in 'RetrieveTIGroupsV3.xsd', 'rn25_Release201104.xsd', 'TestConnectionServiceV1.xsd':
    # for fn in 'RetrieveTIGroupsV5.xsd', 'rn25_Release201411.xsd':
    for fn in ['be']:
        src = os.path.join(os.path.dirname(__file__), 'XSD', fn)
        target = os.path.join(settings.MEDIA_ROOT, 'cache', 'wsdl', fn)
        if not os.path.exists(target):
            # shutil.copy(src, target)
            shutil.copytree(src, target)


from .ui import *
