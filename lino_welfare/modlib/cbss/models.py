# -*- coding: UTF-8 -*-
# Copyright 2011-2015 Luc Saffre
# This file is part of Lino Welfare.
#
# Lino Welfare is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# Lino Welfare is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License along with Lino Welfare.  If not, see
# <http://www.gnu.org/licenses/>.

u"""Database models foe `lino_welfare.modlib.cbss`.

Lino currently knows the following requests (it is technically easy to
add more of them):

(French chunks of text collected from various documents issued by
http://www.bcss.fgov.be):

- :class:`IdentifyPersonRequest` : Identifier la personne par son NISS
  ou ses données phonétiques et vérifier son identité par le numéro de
  carte SIS, de carte d'identité ou par ses données phonétiques.

- :class:`ManageAccessRequest`: Enregistrer, désenregistrer ou
  consulter un dossier dans le registre du réseau de la sécurité
  sociale (registre BCSS) et dans le répertoire sectoriel des CPAS
  géré par la SmalS-MvM.
  
- :class:`RetrieveTIGroupsRequest
  <lino_welfare.modlib.cbss.tx25.RetrieveTIGroupsRequest>`: Obtenir
  des informations à propos d’une personne dans le cadre de l’enquête
  sociale.
  

"""

import os
import shutil
import logging
logger = logging.getLogger(__name__)


from suds import WebFault

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

# from appy.shared.xml_parser import XmlUnmarshaller

from lino import mixins
from lino.api import dd, rt
from lino.utils import assert_pure
from lino.utils import join_words
from lino.utils import AttrDict

from lino.modlib.users.mixins import ByUser
from lino_welfare.modlib.pcsw import models as pcsw

from .mixins import *
from .choicelists import *

from .roles import CBSSUser


CBSS_ERROR_MESSAGE = "CBSS error %s:\n"


def gender2cbss(gender):
    if gender == dd.Genders.male:
        return '1'
    elif gender == dd.Genders.female:
        return '2'
    else:
        return '0'


def cbss2gender(v):
    if v == '1':
        return dd.Genders.male
    elif v == '2':
        return dd.Genders.female
    return None


def cbss2date(s):
    a = s.split('-')
    assert len(a) == 3
    a = [int(i) for i in a]
    return dd.IncompleteDate(*a)


def cbss2civilstate(node):
    value = nodetext(node)
    if not value:
        return value
    v = pcsw.CivilState.get_by_value(value)
    #~ if v is None:
        #~ print "20120601 cbss2civilstate None for ", repr(value)
    return unicode(v)


def cbss2country(code):
    try:
        return rt.modules.countries.Country.objects.get(inscode=code)
    except Country.DoesNotExist:
        logger.warning("Unknown country code %s", code)


def cbss2address(obj, **data):
    n = obj.childAtPath('/Basic/DiplomaticPost')
    if n is not None:
        data.update(
            country=cbss2country(nodetext(n.childAtPath('/CountryCode'))))
        #~ n.childAtPath('/Post')
        data.update(address=nodetext(n.childAtPath('/AddressPlainText')))
        return data
    n = obj.childAtPath('/Basic/Address')
    if n is not None:
        data.update(
            country=cbss2country(nodetext(n.childAtPath('/CountryCode'))))
        #~ country = countries.Country.objects.get(
            #~ inscode=n.childAtPath('/CountryCode').text)
        addr = ''
        #~ addr += n.childAtPath('/MunicipalityCode').text
        addr += join_words(
            nodetext(n.childAtPath('/Street')),
            nodetext(n.childAtPath('/HouseNumber')),
            nodetext(n.childAtPath('/Box'))
        )
        addr += ', ' + join_words(
            nodetext(n.childAtPath('/PostalCode')),
            nodetext(n.childAtPath('/Municipality'))
        )
        data.update(address=addr)
    return data


class Sector(mixins.BabelNamed):

    """
    Default values filled from :mod:`lino_welfare.modlib.cbss.fixtures.sectors`.
    """
    class Meta:
        verbose_name = _("Sector")
        verbose_name_plural = _("Sectors")
        unique_together = ['code', 'subcode']

    #~ code = models.CharField(max_length=2,verbose_name=_("Code"),primary_key=True)
    code = models.IntegerField(max_length=2, verbose_name=_("Code"))
    subcode = models.IntegerField(
        max_length=2, verbose_name=_("Subcode"), default=0)
    abbr = dd.BabelCharField(_("Abbreviation"), max_length=50, blank=True)

    def __unicode__(self):
        #~ return '(' + str(self.code) + ') ' + mixins.BabelNamed.__unicode__(self)
        if self.subcode != 0:
            return str(self.code) + '.' + str(self.subcode) + ' - ' + mixins.BabelNamed.__unicode__(self)
        return str(self.code) + ' - ' + mixins.BabelNamed.__unicode__(self)


class Sectors(dd.Table):
    model = 'cbss.Sector'
    required_roles = dd.required(CBSSUser, dd.SiteStaff)
    column_names = 'code subcode abbr name *'
    order_by = ['code', 'subcode']


class Purpose(mixins.BabelNamed):

    u"""
    Codes qualité (Hoedanigheidscodes). 
    This table is usually filled with the official codes
    by :mod:`lino_welfare.modlib.cbss.fixtures.purposes`.
    """
    class Meta:
        verbose_name = _("Purpose")
        verbose_name_plural = _('Purposes')
        unique_together = ['sector_code', 'code']
    sector_code = models.IntegerField(
        max_length=2, verbose_name=_("Sector"), blank=True, null=True)
    #~ sector_subcode = models.IntegerField(max_length=2,verbose_name=_("Subsector"),blank=True,null=True)
    #~ sector = models.ForeignKey(Sector,blank=True,null=True)
    #~ code = models.CharField(max_length=3,verbose_name=_("Code"))
    code = models.IntegerField(max_length=3, verbose_name=_("Code"))

    def __unicode__(self):
        #~ return '(' + str(self.code) + ') ' + mixins.BabelNamed.__unicode__(self)
        return str(self.code) + ' - ' + mixins.BabelNamed.__unicode__(self)


class Purposes(dd.Table):
    model = 'cbss.Purpose'
    required_roles = dd.required(CBSSUser, dd.SiteStaff)
    column_names = 'sector_code code name *'
    order_by = ['sector_code', 'code']


NSCOMMON = ('common', 'http://www.ksz-bcss.fgov.be/XSD/SSDN/Common')
NSIPR = ('ipr',
         "http://www.ksz-bcss.fgov.be/XSD/SSDN/OCMW_CPAS/IdentifyPerson")
NSMAR = ('mar', "http://www.ksz-bcss.fgov.be/XSD/SSDN/OCMW_CPAS/ManageAccess")
NSWSC = ('wsc', "http://ksz-bcss.fgov.be/connectors/WebServiceConnector")


class CBSSRequestDetail(dd.FormLayout):
    #~ main = 'request response'
    main = 'request technical'

    request = dd.Panel("""
    info
    parameters
    result
    """, label=_("Request"))

    technical = dd.Panel("""
    environment ticket
    response_xml
    info_messages
    debug_messages
    """, label=_("Technical"),
        required_roles=dd.required(CBSSUser, dd.SiteStaff))

    info = dd.Panel("""
    id person user sent status printed
    """, label=_("Request information"))


class IdentifyPersonRequest(SSDNRequest, WithPerson):

    """
    A request to the IdentifyPerson service.
    
    """

    ssdn_service_id = 'OCMWCPASIdentifyPerson'
    ssdn_service_version = '20050930'
    xsd_filename = xsdpath('SSDN', 'OCMW_CPAS',
                           'IdentifyPerson', 'IdentifyPersonRequest.xsd')

    class Meta:
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
      #~ <p>Zum Beispiel
      #~ <table border=1 class="htmlText">
      #~ <tr>
        #~ <td>Geburtsdatum</td>
        #~ <td colspan="3">Toleranz</td>
      #~ </tr><tr>
        #~ <td></td>
        #~ <td>0</td>
        #~ <td>1</td>
        #~ <td>10</td>
      #~ </tr><tr>
        #~ <td> 1968-00-00  </td>
        #~ <td> im Jahr 1968 </td>
        #~ <td> von 1967 bis 1969 </td>
        #~ <td> 1958 bis 1978 </td>
      #~ </tr><tr>
        #~ <td> 1968-06-00  </td>
        #~ <td> im Juni 1968 </td>
        #~ <td> von Mai  bis Juli 1968 </td>
        #~ <td>von Oktober 1967 bis April 1969</td>
      #~ </tr>
      #~ </table>
      #~ </p>

    #~ def on_create(self,ar):
        #~ UserAuthored.on_create(self,ar)
        #~ SSIN.on_create(self,ar)
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
        #~ if not self.birth_date:
            #~ raise Warning("Empty birth date (a full_clean() would have told that, too!)")
            #~ raise Warning(_("Birth date may not be empty."))

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
            #~ if not self.last_name or not self.first_name:
                #~ raise Warning("Fields last_name and first_name are mandatory.")
            pd.append(E('ipr:LastName').setText(self.last_name))
            pd.append(E('ipr:FirstName').setText(self.first_name))
            pd.append(E('ipr:MiddleName').setText(self.middle_name))
            pd.append(E('ipr:BirthDate').setText(str(self.birth_date)))
            #~ if not self.birth_date.is_complete():
                #~ pd.append(E('ipr:Tolerance').setText(self.tolerance))
            #~ if gender is not None: pd.append(E('ipr:Gender').setText(gender))
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
        #~ return reply

        #~ if False:

            #~ try:
                #~ res = self.cbss_namespace.execute(srvreq,str(self.id),now)
            #~ except cbss.Warning,e:
                #~ self.status = RequestStates.exception
                #~ self.response_xml = unicode(e)
                #~ self.save()
                #~ return
            #~ except Exception,e:
                #~ self.status = RequestStates.exception
                #~ self.response_xml = traceback.format_exc(e)
                #~ self.save()
                #~ return
            #~ self.sent = now
            #~ self.response_xml = res.data.xmlString
            #~ reply = cbss.xml2reply(res.data.xmlString)
            #~ rc = reply.ServiceReply.ResultSummary.ReturnCode
            #~ if rc == '0':
                #~ self.status = RequestStates.ok
            #~ elif rc == '1':
                #~ self.status = RequestStates.warnings
            #~ elif rc == '10000':
                #~ self.status = RequestStates.errors
            #~ self.save()

            #~ if self.status != RequestStates.ok:
                #~ msg = '\n'.join(list(cbss.reply2lines(reply)))
                #~ raise Exception(msg)

            #~ self.on_cbss_ok(reply)


dd.update_field(IdentifyPersonRequest, 'birth_date', blank=False)
"""
DocumentInvalid
Element '{http://www.ksz-bcss.fgov.be/XSD/SSDN/OCMW_CPAS/IdentifyPerson}BirthDate': [facet 'length'] The value has a length of '0'; this differs from the allowed length of '10'., line 7

"""
#~ dd.update_field(IdentifyPersonRequest,'first_name',blank=True)
#~ dd.update_field(IdentifyPersonRequest,'last_name',blank=True)


class IdentifyPersonRequestDetail(CBSSRequestDetail):
    p1 = dd.Panel("""
    national_id
    spacer
    """, label=_("Using the national ID"))

    p2 = dd.Panel("""
    first_name middle_name last_name
    birth_date tolerance  gender
    """, label=_("Using phonetic search"))

    parameters = dd.Panel("p1 p2", label=_("Parameters"))

    # result = dd.Panel("IdentifyPersonResult", label=_("Result"))
    result = "IdentifyPersonResult"


class IdentifyPersonRequestInsert(IdentifyPersonRequestDetail):
    window_size = (60, 'auto')

    main = """
    person national_id
    p2
    """

    p2 = dd.Panel("""
    first_name middle_name last_name
    birth_date tolerance gender
    """, label=_("Phonetic search"))

    #~ def setup_handle(self,lh):
        #~ lh.p2.label = _("Phonetic search")


class CBSSRequests(dd.Table):
    pass


class IdentifyPersonRequests(CBSSRequests):
    required_roles = dd.required(CBSSUser)
    model = 'cbss.IdentifyPersonRequest'
    active_fields = 'person'
    detail_layout = IdentifyPersonRequestDetail()
    insert_layout = IdentifyPersonRequestInsert()

    @dd.constant()
    def spacer(self):
        return '<br/>'


class AllIdentifyPersonRequests(IdentifyPersonRequests):
    required_roles = dd.required(dd.SiteStaff, CBSSUser)


class MyIdentifyPersonRequests(ByUser, IdentifyPersonRequests):
    pass


class IdentifyRequestsByPerson(IdentifyPersonRequests):
    required_roles = dd.required(CBSSUser)
    master_key = 'person'
    column_names = 'user sent status *'


class IdentifyPersonResult(dd.VirtualTable):
    """
    Displays the response of an :class:`IdentifyPersonRequest`
    as a table.
    """
    master = 'cbss.IdentifyPersonRequest'
    master_key = None
    label = _("Results")
    column_names = 'national_id:10 last_name:20 first_name:10 address birth_date:10 birth_location civil_state *'

    class Row(AttrDict):
        @classmethod
        def get_chooser_for_field(cls, fieldname):
            return None

    @classmethod
    def get_data_rows(self, ar):
        ipr = ar.master_instance
        if ipr is None:
            #~ print "20120606 ipr is None"
            return
        #~ if not ipr.status in (RequestStates.ok,RequestStates.fictive):
        if not ipr.status in (RequestStates.ok, RequestStates.warnings):
            #~ print "20120606 wrong status", ipr.status
            return
        service_reply = ipr.get_service_reply()
        results = service_reply.childAtPath('/SearchResults').children
        #~ print "20120606 got", service_reply
        if results is None:
            #~ print "20120606 no /SearchResults"
            #~ return []
            return
        for obj in results:
            data = dict()
            data.update(
                national_id=nodetext(
                    obj.childAtPath('/Basic/SocialSecurityUser')))
            data.update(
                last_name=nodetext(obj.childAtPath('/Basic/LastName')))
            data.update(
                first_name=nodetext(obj.childAtPath('/Basic/FirstName')))
            data.update(
                gender=cbss2gender(nodetext(obj.childAtPath('/Basic/Gender'))))
            data.update(
                birth_date=cbss2date(nodetext(
                    obj.childAtPath('/Basic/BirthDate'))))
            data.update(civil_state=cbss2civilstate(
                obj.childAtPath('/Extended/CivilState')))
            data.update(
                birth_location=nodetext(
                    obj.childAtPath('/Extended/BirthLocation')))
            data.update(cbss2address(obj))
            yield self.Row(**data)

    @dd.displayfield(_("National ID"))
    def national_id(self, obj, ar):
        return obj.national_id

    @dd.displayfield(_("Last name"))
    def last_name(self, obj, ar):
        return obj.last_name

    @dd.displayfield(_("First name"))
    def first_name(self, obj, ar):
        return obj.first_name

    @dd.virtualfield(dd.Genders.field())
    def gender(self, obj, ar):
        return obj.gender

    @dd.displayfield(_("Birth date"))
    def birth_date(self, obj, ar):
        return obj.birth_date

    @dd.displayfield(_("Birth location"))
    def birth_location(self, obj, ar):
        return obj.birth_location

    @dd.displayfield(_("Civil state"))
    def civil_state(self, obj, ar):
        return obj.civil_state

    @dd.displayfield(_("Address"))
    def address(self, obj, ar):
        return obj.address


class ManageAccessRequest(SSDNRequest, WithPerson):

    """A request to the ManageAccess service.
    
    Registering a person means that this PCSW is going to maintain a
    dossier about this person.  Users commonly say "to integrate" a
    person.
    
    Fields include:

    
    .. attribute:: sector

        Pointer to :class:`Sector`.

    .. attribute:: purpose

        Pointer to :class:`Purpose`.

    .. attribute:: action
    
        The action to perform.  This must be one of the values in
        :class:`lino_welfare.modlib.cbss.choicelists.ManageActions`
    
    .. attribute:: query_register

        The register to be query.
        This must be one of the values in
        :class:`lino_welfare.modlib.cbss.choicelists.QueryRegisters`

    """

    ssdn_service_id = 'OCMWCPASManageAccess'
    ssdn_service_version = '20050930'

    xsd_filename = xsdpath('SSDN', 'OCMW_CPAS',
                           'ManageAccess', 'ManageAccessRequest.xsd')

    class Meta:
        verbose_name = _("ManageAccess Request")
        verbose_name_plural = _("ManageAccess Requests")

    #~ purpose = models.IntegerField(verbose_name=_('Purpose'),
      #~ default=0,help_text="""\
#~ The purpose for which the inscription needs to be
#~ registered/unregistered or listed.
#~ For listing this field is optional,
#~ for register/unregister it is obligated.""")

    #~ sector = models.IntegerField(verbose_name=_('Sector'),
      #~ blank=False,default=0,help_text="""\
#~ For register and unregister this element is ignored.
#~ It can be used for list,
#~ when information about sectors is required.""")

    sector = models.ForeignKey(
        'cbss.Sector', # on_delete=models.PROTECT,
        editable=False, help_text="""\
For register and unregister this element is ignored. 
It can be used for list, 
when information about sectors is required.""")

    purpose = models.ForeignKey(
        'cbss.Purpose',
        #~ blank=True,null=True,
        help_text="""\
The purpose for which the inscription needs to be
registered/unregistered or listed.
For listing this field is optional,
for register/unregister it is mandatory.""")

    start_date = models.DateField(
        #~ blank=True,null=True,
        verbose_name=_("Period from"))
    end_date = models.DateField(
        #~ blank=True,null=True,
        verbose_name=_("Period until"))

    # 20120527 : Django converts default value to unicode. didnt yet
    # understand why.
    action = ManageActions.field(blank=False, default=ManageActions.LIST)
    query_register = QueryRegisters.field(
        blank=False, default=QueryRegisters.ALL)
    #~ action = ManageActions.field(blank=False)
    # ~ query_register = QueryRegisters.field(blank=False) # ,default=QueryRegisters.ALL)

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
        #~ main.append(E('mar:Purpose').setText(str(self.purpose)))
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


class ManageAccessRequestDetail(CBSSRequestDetail):

    p1 = dd.Panel("""
    action start_date end_date
    purpose query_register
    """, label=_("Requested action"))

    proof = dd.Panel("""
    national_id sis_card_no id_card_no
    first_name last_name birth_date
    """, label=_("Proof of authentication"))
    parameters = dd.Panel("p1 proof", label=_("Parameters"))

    #~ def setup_handle(self,lh):
        #~ lh.p1.label = _("Requested action")
        #~ lh.proof.label = _("Proof of authentication")
        #~ CBSSRequestDetail.setup_handle(self,lh)


class ManageAccessRequestInsert(dd.FormLayout):
    window_size = (60, 'auto')

    p1 = dd.Panel("""
    action start_date end_date
    purpose query_register
    """, label=_("Requested action"))

    proof = dd.Panel("""
    national_id sis_card_no id_card_no
    first_name last_name birth_date
    """, label=_("Proof of authentication"))

    main = """
    person
    p1
    proof
    """

    #~ def setup_handle(self,lh):
        #~ lh.p1.label = _("Requested action")
        #~ lh.proof.label = _("Proof of authentication")
        #~ super(ManageAccessRequestInsert,self).setup_handle(lh)


class ManageAccessRequests(CBSSRequests):
    required_roles = dd.required(CBSSUser)
    #~ window_size = (500,400)
    model = 'cbss.ManageAccessRequest'
    detail_layout = ManageAccessRequestDetail()
    insert_layout = ManageAccessRequestInsert()
    active_fields = 'person'


class AllManageAccessRequests(ManageAccessRequests):
    required_roles = dd.required(dd.SiteStaff, CBSSUser)


class ManageAccessRequestsByPerson(ManageAccessRequests):
    master_key = 'person'


class MyManageAccessRequests(ManageAccessRequests, ByUser):
    required_roles = dd.required(CBSSUser)


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
        for i in reply.status.information:
            msg += "\n- %s = %s" % (i.fieldName, i.fieldValue)
        raise Warning(msg)


class RetrieveTIGroupsRequest(NewStyleRequest, SSIN):

    """
    A request to the RetrieveTIGroups service (aka Tx25)
    """

    class Meta:
        verbose_name = _("Tx25 Request")
        verbose_name_plural = _('Tx25 Requests')

    wsdl_parts = ('cache', 'wsdl', 'RetrieveTIGroupsV3.wsdl')

    language = RequestLanguages.field(blank=True, default=RequestLanguages.fr)
    history = models.BooleanField(
        verbose_name=_("History"), default=True,
        help_text="Whatever this means.")

    def get_print_language(self):
        if settings.SITE.get_language_info(self.language.value):
        #~ if self.language.value in babel.AVAILABLE_LANGUAGES:
            return self.language.value
        return settings.SITE.DEFAULT_LANGUAGE.django_code

    def fill_from_person(self, person):
        self.national_id = person.national_id
        if RequestLanguages.get_by_value(person.language, None):
            self.language = person.language  # .value # babel.DEFAULT_LANGUAGE

    def get_service_reply(self, **kwargs):
        assert_pure(self.response_xml)
        client = get_client(self)
        meth = client.service.retrieveTI
        clientclass = meth.clientclass(kwargs)
        client = clientclass(meth.client, meth.method)
        #~ print 20120613, portSelector[0]
        #~ print '20120613b', dir(client)
        s = self.response_xml.encode('utf-8')
        return client.succeeded(client.method.binding.input, s)

    def execute_newstyle(self, client, infoCustomer, simulate_response):
        si = client.factory.create('ns0:SearchInformationType')
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
                reply = client.service.retrieveTI(infoCustomer, None, si)
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
                msg += unicode(e.document)
                self.status = RequestStates.failed
                raise Warning(msg)
            self.response_xml = reply.decode('utf-8')  # 20130201

        #~ self.response_xml = unicode(reply)
        reply = self.get_service_reply()
        self.ticket = reply.informationCBSS.ticketCBSS
        self.status = RequestStates.warnings

        reply_has_result(reply)

        self.status = RequestStates.ok
        #~ self.response_xml = str(res)
        #~ self.response_xml = "20120522 %s %s" % (res.__class__,res)
        #~ print 20120523, res.informationCustomer
        #~ print self.response_xml
        return reply

    def Result(self, ar):
        return ar.spawn(RetrieveTIGroupsResult, master_instance=self)


class RetrieveTIGroupsRequestDetail(CBSSRequestDetail):

    parameters = dd.Panel("national_id language history",
                          label=_("Parameters"))

    result = "cbss.RetrieveTIGroupsResult"

    #~ def setup_handle(self,lh):
        #~ CBSSRequestDetail.setup_handle(self,lh)

#~ class RetrieveTIGroupsRequestInsert(dd.FormLayout):
    #~ window_size = (40,'auto')
    #~ main = """
    #~ person
    #~ national_id language
    #~ history
    #~ """


class RetrieveTIGroupsRequests(CBSSRequests):
    #~ debug_permissions = True
    required_roles = dd.login_required(CBSSUser)
    model = RetrieveTIGroupsRequest
    detail_layout = RetrieveTIGroupsRequestDetail()
    column_names = 'id user person national_id language history status ticket sent environment'
    #~ insert_layout = RetrieveTIGroupsRequestInsert()
    insert_layout = dd.FormLayout("""
    person
    national_id language
    history
    """, window_size=(40, 'auto'))
    #~ insert_layout = RetrieveTIGroupsRequestInsert(window_size=(400,'auto'))


class AllRetrieveTIGroupsRequests(RetrieveTIGroupsRequests):
    required_roles = dd.login_required(dd.SiteStaff, CBSSUser)


class RetrieveTIGroupsRequestsByPerson(RetrieveTIGroupsRequests):
    master_key = 'person'


class MyRetrieveTIGroupsRequests(RetrieveTIGroupsRequests, ByUser):
    required_roles = dd.login_required(CBSSUser)


from .tx25 import RetrieveTIGroupsResult


@dd.receiver(dd.pre_analyze)
def customize_system(sender, **kw):

    dd.inject_field('system.SiteConfig',
                    'sector',
                    models.ForeignKey(Sector,
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
    dd.inject_field('system.SiteConfig',
                    'ssdn_user_id',
                    models.CharField(_("SSDN User Id"),
                                     max_length=50,
                                     blank=True,
          help_text="""\
    Used in SSDN requests as text of the `AuthorizedUser\UserID` element.
    """))
    dd.inject_field('system.SiteConfig',
                    'ssdn_email',
                    models.EmailField(_("SSDN email address"),
                                      blank=True,
          help_text="""\
    Used in SSDN requests as text of the `AuthorizedUser\Email` element.
    """))
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
            help_text="""\
            Used in the http header of new-style requests.
            """))


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
    #~ qs = IdentifyPersonRequest.objects.filter(person=self,status=RequestStates.ok)
    html = '<p><ul>'
    #~ for m in (IdentifyPersonRequest,ManageAccessRequest,RetrieveTIGroupsRequest):
        #~ n = m.objects.filter(person=self).count()
        #~ if n > 0:
            #~ html += "<li>%d %s</li>" % (n,unicode(m._meta.verbose_name_plural))
    #~ html += '</ul></p>'
    #~ html += '<p>Using XyzByPerson:<ul>'
    for t in (IdentifyRequestsByPerson, ManageAccessRequestsByPerson, RetrieveTIGroupsRequestsByPerson):
        n = ar.spawn(t, master_instance=self).get_total_count()
        if n > 0:
            html += "<li>%d %s</li>" % (n,
                                        unicode(t.model._meta.verbose_name_plural))
    html += '</ul></p>'
    html = '<div class="htmlText">%s</div>' % html
    return html

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

    if not environment in CBSS_ENVS:
        raise Exception("Invalid `cbss_environment` %r: must be empty or one of %s." % (
            environment, CBSS_ENVS))

    context = dict(cbss_environment=environment)

    def make_wsdl(template, parts):
        fn = os.path.join(settings.MEDIA_ROOT, *parts)
        if not force and os.path.exists(fn):
            if os.stat(fn).st_mtime > self.kernel.code_mtime:
                logger.info(
                    "NOT generating %s because it is newer than the code.", fn)
                return
        s = file(os.path.join(os.path.dirname(__file__), 'WSDL', template)
                 ).read()
        s = s % context
        settings.SITE.makedirs_if_missing(os.path.dirname(fn))
        open(fn, 'wt').write(s)
        logger.info("Generated %s for environment %r.", fn, environment)

    make_wsdl('RetrieveTIGroupsV3.wsdl', RetrieveTIGroupsRequest.wsdl_parts)
    make_wsdl('WebServiceConnector.wsdl', SSDNRequest.wsdl_parts)
    #~ make_wsdl('TestConnectionService.wsdl',TestConnectionRequest.wsdl_parts)

    # The following xsd files are needed, unmodified but in the same directory
    #~ for fn in 'RetrieveTIGroupsV3.xsd', 'rn25_Release201104.xsd', 'TestConnectionServiceV1.xsd':
    for fn in 'RetrieveTIGroupsV3.xsd', 'rn25_Release201104.xsd':
        src = os.path.join(os.path.dirname(__file__), 'XSD', fn)
        target = os.path.join(settings.MEDIA_ROOT, 'cache', 'wsdl', fn)
        if not os.path.exists(target):
            shutil.copy(src, target)


