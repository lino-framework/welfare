# -*- coding: utf-8 -*-
# Copyright 2012-2020 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

"""
This module contains "quick" tests that are run on a demo database
without any fixture. You can run only these tests by issuing::

  $ python manage.py test cbss.QuickTest
  $ django-admin.py test --settings=lino_welfare.projects.eupen.settings.demo cbss.QuickTest


"""
import datetime

from django.conf import settings
from django.core.exceptions import ValidationError

from lino.utils.djangotest import TestCase
from lino.utils import IncompleteDate
from lino.utils.instantiator import create_and_get
from lino.api import rt
from lino_welfare.modlib.cbss import models as cbss

NOW = datetime.datetime(2015, 5, 11, 18, 31, 1)


class QuickTest(TestCase):
    never_build_site_cache = False
    fixtures = 'sectors purposes democfg'.split()

    def test01(self):

        # print("20180502 test_cbss.test01()")
        settings.SITE.startup()  # create cache/wsdl files

        root = create_and_get(settings.SITE.user_model, username='root')

        luc = create_and_get(
            rt.models.pcsw.Client, first_name='Luc', last_name='Saffre')

        # First IdentifyPersonRequest
        # Create an IPR with NISS just to have the XML validated.

        req = cbss.IdentifyPersonRequest(
            national_id="70100853190", user=root, person=luc)
        try:
            req.full_clean()
            self.fail('Expected ValidationError "birth_date cannot be blank."')
        except ValidationError:
            pass

        req.birth_date = IncompleteDate(1938, 6, 1)
        try:
            req.validate_request()
        except Warning as e:
            self.assertEqual(str(e), "")
            pass

        req.birth_date = IncompleteDate(1938, 0, 0)
        req.validate_request()
        req.execute_request(simulate_response='Foo', now=NOW)

        expected = """\
<ssdn:SSDNRequest xmlns:ssdn="http://www.ksz-bcss.fgov.be/XSD/SSDN/Service">
<ssdn:RequestContext>
<ssdn:AuthorizedUser>
<ssdn:UserID>00901234567</ssdn:UserID>
<ssdn:Email>info@example.com</ssdn:Email>
<ssdn:OrgUnit>0123456789</ssdn:OrgUnit>
<ssdn:MatrixID>17</ssdn:MatrixID>
<ssdn:MatrixSubID>1</ssdn:MatrixSubID>
</ssdn:AuthorizedUser>
<ssdn:Message>
<ssdn:Reference>IdentifyPersonRequest # 1</ssdn:Reference>
<ssdn:TimeRequest>20150511T183101</ssdn:TimeRequest>
</ssdn:Message>
</ssdn:RequestContext>
<ssdn:ServiceRequest>
<ssdn:ServiceId>OCMWCPASIdentifyPerson</ssdn:ServiceId>
<ssdn:Version>20050930</ssdn:Version>
<ipr:IdentifyPersonRequest xmlns:ipr="http://www.ksz-bcss.fgov.be/XSD/SSDN/OCMW_CPAS/IdentifyPerson">
<ipr:SearchCriteria>
<ipr:SSIN>70100853190</ipr:SSIN>
<ipr:PhoneticCriteria>
<ipr:LastName></ipr:LastName>
<ipr:FirstName></ipr:FirstName>
<ipr:MiddleName></ipr:MiddleName>
<ipr:BirthDate>1938-00-00</ipr:BirthDate>
</ipr:PhoneticCriteria>
</ipr:SearchCriteria>
<ipr:VerificationData>
<ipr:PersonData>
<ipr:LastName></ipr:LastName>
<ipr:FirstName></ipr:FirstName>
<ipr:MiddleName></ipr:MiddleName>
<ipr:BirthDate>1938-00-00</ipr:BirthDate>
</ipr:PersonData>
</ipr:VerificationData>
</ipr:IdentifyPersonRequest>
</ssdn:ServiceRequest>
</ssdn:SSDNRequest>"""
        self.assertEquivalent(expected, req.request_xml)

        ##

        req = cbss.IdentifyPersonRequest(
            last_name="MUSTERMANN",
            birth_date=IncompleteDate(1938, 0, 0))
        req.validate_request()

        # Create another one, this time a name search.
        # This time we also inspect the generated XML.

        req = cbss.IdentifyPersonRequest(
            user=root, person=luc,
            last_name="MUSTERMANN",
            first_name="Max",
            birth_date=IncompleteDate(1938, 6, 1))
        req.validate_request()
        req.execute_request(simulate_response='Foo', now=NOW)

        expected = """\
<ssdn:SSDNRequest xmlns:ssdn="http://www.ksz-bcss.fgov.be/XSD/SSDN/Service">
<ssdn:RequestContext>
<ssdn:AuthorizedUser>
<ssdn:UserID>00901234567</ssdn:UserID>
<ssdn:Email>info@example.com</ssdn:Email>
<ssdn:OrgUnit>0123456789</ssdn:OrgUnit>
<ssdn:MatrixID>17</ssdn:MatrixID>
<ssdn:MatrixSubID>1</ssdn:MatrixSubID>
</ssdn:AuthorizedUser>
<ssdn:Message>
<ssdn:Reference>IdentifyPersonRequest # 2</ssdn:Reference>
<ssdn:TimeRequest>20150511T183101</ssdn:TimeRequest>
</ssdn:Message>
</ssdn:RequestContext>
<ssdn:ServiceRequest>
<ssdn:ServiceId>OCMWCPASIdentifyPerson</ssdn:ServiceId>
<ssdn:Version>20050930</ssdn:Version>
<ipr:IdentifyPersonRequest xmlns:ipr="http://www.ksz-bcss.fgov.be/XSD/SSDN/OCMW_CPAS/IdentifyPerson">
<ipr:SearchCriteria>
<ipr:PhoneticCriteria>
<ipr:LastName>MUSTERMANN</ipr:LastName>
<ipr:FirstName>Max</ipr:FirstName>
<ipr:MiddleName></ipr:MiddleName>
<ipr:BirthDate>1938-06-01</ipr:BirthDate>
</ipr:PhoneticCriteria>
</ipr:SearchCriteria>
</ipr:IdentifyPersonRequest>
</ssdn:ServiceRequest>
</ssdn:SSDNRequest>"""

        self.assertEquivalent(expected, req.request_xml)

        if settings.SITE.plugins.cbss.cbss_environment != 'test':
            # Skip live tests unless we are in test environment.
            # Otherwise we would have to build /media/chache/wsdl files
            return

        # Execute a RetrieveTIGroupsRequest.

        req = cbss.RetrieveTIGroupsRequest(
            user=root, person=luc,
            national_id='12345678901', language='fr')

        # Try it without environment and see the XML.
        # Note that NewStyleRequests have no validate_request method.

        req.execute_request(simulate_response='Foo', now=NOW)
        expected = ""
        self.assertEquivalent(expected, req.request_xml)

        # Now a ManageAccessRequest

        today = datetime.date(2012, 5, 24)
        kw = dict()
        # dossier in onderzoek voor een maximale periode van twee maanden
        kw.update(purpose_id=1)
        kw.update(national_id='68060105329')
        kw.update(user=root)
        kw.update(person=luc)
        kw.update(start_date=today)
        kw.update(end_date=today)
        kw.update(action=cbss.ManageActions.REGISTER)
        kw.update(query_register=cbss.QueryRegisters.SECONDARY)
        #~ kw.update(id_card_no=)

        kw.update(last_name='SAFFRE')
        kw.update(first_name='LUC JOHANNES')
        kw.update(birth_date=IncompleteDate(1968, 6, 1))
        req = cbss.ManageAccessRequest(**kw)

        req.execute_request(simulate_response='Foo', now=NOW)
        expected = """<ssdn:SSDNRequest xmlns:ssdn="http://www.ksz-bcss.fgov.be/XSD/SSDN/Service">
<ssdn:RequestContext>
<ssdn:AuthorizedUser>
<ssdn:UserID>00901234567</ssdn:UserID>
<ssdn:Email>info@example.com</ssdn:Email>
<ssdn:OrgUnit>0123456789</ssdn:OrgUnit>
<ssdn:MatrixID>17</ssdn:MatrixID>
<ssdn:MatrixSubID>1</ssdn:MatrixSubID>
</ssdn:AuthorizedUser>
<ssdn:Message>
<ssdn:Reference>ManageAccessRequest # 1</ssdn:Reference>
<ssdn:TimeRequest>20150511T183101</ssdn:TimeRequest>
</ssdn:Message>
</ssdn:RequestContext>
<ssdn:ServiceRequest>
<ssdn:ServiceId>OCMWCPASManageAccess</ssdn:ServiceId>
<ssdn:Version>20050930</ssdn:Version>
<mar:ManageAccessRequest xmlns:mar="http://www.ksz-bcss.fgov.be/XSD/SSDN/OCMW_CPAS/ManageAccess">
<mar:SSIN>68060105329</mar:SSIN>
<mar:Purpose>10</mar:Purpose>
<mar:Period>
<common:StartDate xmlns:common="http://www.ksz-bcss.fgov.be/XSD/SSDN/Common">2012-05-24</common:StartDate>
<common:EndDate xmlns:common="http://www.ksz-bcss.fgov.be/XSD/SSDN/Common">2012-05-24</common:EndDate>
</mar:Period>
<mar:Action>REGISTER</mar:Action>
<mar:Sector>17</mar:Sector>
<mar:QueryRegister>SECONDARY</mar:QueryRegister>
<mar:ProofOfAuthentication>
<mar:PersonData>
<mar:LastName>SAFFRE</mar:LastName>
<mar:FirstName>LUC JOHANNES</mar:FirstName>
<mar:BirthDate>1968-06-01</mar:BirthDate>
</mar:PersonData>
</mar:ProofOfAuthentication>
</mar:ManageAccessRequest>
</ssdn:ServiceRequest>
</ssdn:SSDNRequest>
"""
        self.assertEquivalent(expected, req.request_xml)
