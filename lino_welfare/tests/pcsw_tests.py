# -*- coding: utf-8 -*-
## Copyright 2011-2013 Luc Saffre
## This file is part of the Lino project.
## Lino is free software; you can redistribute it and/or modify 
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 3 of the License, or
## (at your option) any later version.
## Lino is distributed in the hope that it will be useful, 
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
## GNU General Public License for more details.
## You should have received a copy of the GNU General Public License
## along with Lino; if not, see <http://www.gnu.org/licenses/>.

"""
This module contains "quick" tests that are run on a demo database 
without any fixture. You can run only these tests by issuing::

  python manage.py test lino_welfare.QuickTest

"""

from __future__ import unicode_literals

import logging
logger = logging.getLogger(__name__)

import decimal

#~ from django.utils import unittest
#~ from django.test.client import Client
from django.conf import settings

#from lino.igen import models
#from lino.modlib.contacts.models import Contact, Companies
#from lino.modlib.countries.models import Country
#~ from lino.modlib.contacts.models import Companies

from django.utils import translation
from django.utils.encoding import force_unicode
from django.core.exceptions import ValidationError

from lino import dd
from lino.utils import i2d
#~ from north import babel
#~ from lino.core.dbutils import resolve_model
#Companies = resolve_model('contacts.Companies')
#~ from djangosite.utils.test import TestCase
from djangosite.utils.test import RemoteAuthTestCase

contacts_RoleType = dd.resolve_model('contacts.RoleType')
contacts_Role = dd.resolve_model('contacts.Role')
Person = dd.resolve_model('contacts.Person')
Property = dd.resolve_model('properties.Property')
PersonProperty = dd.resolve_model('properties.PersonProperty')
cv = dd.resolve_app('cv')
pcsw = dd.resolve_app('pcsw')
contacts = dd.resolve_app('contacts')
households = dd.resolve_app('households')
debts = dd.resolve_app('debts')

#~ from lino.projects.pcsw.models import Person
#~ from lino.modlib.cv.models import PersonProperty
#~ from lino.modlib.properties.models import Property

isip_Contract = dd.resolve_model("isip.Contract")
isip_ContractType = dd.resolve_model("isip.ContractType")
jobs_Contract = dd.resolve_model("jobs.Contract")
from lino_welfare.modlib.jobs.models import Contracts, ContractType, JobProvider, Job
from lino.mixins.printable import PrintAction
from lino.modlib.users.models import User
#~ from lino_welfare.modlib.pcsw.models import Person
from lino_welfare.modlib.pcsw.models import Client

class QuickTest(RemoteAuthTestCase):
    maxDiff = None


    def test00(self):
        """
        Initialization.
        """
        #~ print "20130321 test00 started"
        self.user_root = User(username='root',language='en',profile='900') # ,last_name="Superuser")
        self.user_root.save()
        signer1 = Person(first_name="Ernst",last_name="Keutgen") ; signer1.save()
        signer2 = Person(first_name="Joseph",last_name="Ossemann") ; signer2.save()
        sc = settings.SITE.site_config
        sc.signer1 = signer1
        sc.signer2 = signer2
        sc.full_clean() ; sc.save()
        #~ print "20130321 test00 done"
        
        #~ def test01(self):
        """
        Tests error handling when printing a contract whose type's 
        name contains non-ASCII char.
        Created :blogref:`20110615`.
        See the source code at :srcref:`/lino/apps/pcsw/tests/pcsw_tests.py`.
        """
        
        #~ print "20130321 test01 started"
        self.job_provider = JobProvider(name="Test")
        self.job_provider.save()
        self.max_mustermann = Client(first_name="Max",last_name="Mustermann")
        self.max_mustermann.full_clean()
        self.max_mustermann.save()
        t = ContractType(id=1,build_method='pisa',template="",name=u'Art.60\xa77')
        t.save()
        job = Job(provider=self.job_provider,contract_type=t)
        job.save()
        kw = dict()
        kw['job'] = job
        kw['user'] = self.user_root
        kw['client'] = self.max_mustermann
        self.jobs_contract_1 = jobs_Contract(id=1,**kw)
        self.jobs_contract_1.full_clean()
        self.jobs_contract_1.save()
        self.assertEqual(self.jobs_contract_1.company,self.job_provider)
        
        
        if settings.SITE.get_language_info('en'):
        #~ if 'en' in settings.SITE.AVAILABLE_LANGUAGES:
            url = '/api/jobs/Contract/1?an=do_print'
            response = self.client.get(url,REMOTE_USER='root',HTTP_ACCEPT_LANGUAGE='en')
            result = self.check_json_result(response,'success message alert')
            self.assertEqual(result['success'],False)
            self.assertEqual(result['alert'],True)
            self.assertEqual(
              result['message'],
              """\
Invalid template '' configured for ContractType u'Art.60\\xa77' (expected filename ending with '.pisa.html').""")

        
        #~ def test02(self):
        """
        20130225 Melanie wrote: 
        
          ich kann keine 60/7 Konvention erstellen. 
          Cercle vicieux: ich müsste den VSE beenden aber VSE kann nicht beendet
          werden weil Datumüberschniedung mit 60/7 Konvention und genauso
          andersrum.
        
        A dateless contract is a contract that has no begin date and no end date.
        Lino allows multiple dateless contracts per client.
        OverlappingContractsTest gave false alert when trying to save a date contract while 
        another dateless contract existed.
        
        This test is based on the previous test (:func:`test01`) which created a dateless contract.
        Now we try to create another contract.
        The dateless contract should not cause problem here.
        """
        t = isip_ContractType(id=1,name='Test')
        t.save()
        self.isip_contract_1 = isip_Contract(id=1,
            client=self.max_mustermann,
            type=t,
            user=self.user_root,
            )
        self.isip_contract_1.full_clean()
        self.isip_contract_1.save()
        self.isip_contract_1.applies_from=i2d(20130201)
        self.isip_contract_1.applies_until=i2d(20130228)
        self.isip_contract_1.full_clean()
        self.isip_contract_1.save()
        
        """
        if now somebody edits the first contract and inserts a start date,
        then this should raise a ValidationError
        """    
        self.jobs_contract_1.applies_from=i2d(20130201)
        #~ self.jobs_contract_1.applies_until=i2d(20130228)
        #~ babel.set_language(None)
        translation.deactivate_all()
        try:
            self.jobs_contract_1.full_clean()
            self.fail("Expected a ValidationError")
        except ValidationError as e:
            self.assertEqual(force_unicode(e),"[u'Date range overlaps with ISIP #1']")
        self.jobs_contract_1.applies_from = None
        
        #~ self.jobs_contract_1.save()


        #~ def test02b(self):
        """
        If the job provider has a single contact person
        that person will automatically get filled as default signer 
        for a contract with this provider.
        """
        settings.SITE.uppercase_last_name = True
        gf = contacts_RoleType(name="Geschäftsführer",use_in_contracts=True)
        gf.full_clean() ; gf.save()
        self.hans = Person(first_name="Hans",last_name="Dampf")
        self.hans.full_clean() ; self.hans.save()
        r = contacts_Role(person=self.hans,company=self.job_provider,type=gf)
        r.full_clean() ; r.save()
        qs = self.jobs_contract_1.contact_person_choices_queryset(self.job_provider)
        self.assertEqual(qs.count(),1)
        #~ self.assertEqual(unicode(qs[0]).upper(),"HANS DAMPF") # some configurations uppercase last_name
        self.assertEqual(unicode(qs[0]),"Hans DAMPF") 
        self.assertEqual(self.jobs_contract_1.contact_person,None)
        self.jobs_contract_1.full_clean()
        self.assertEqual(self.jobs_contract_1.contact_person,self.hans)
        self.jobs_contract_1.save()
        

        #~ def test02c(self):
        """
        Test whether examination calendar events are being generated,
        """
        dd.set_language('en')
        msg = u'Date range overlaps with ISIP #1'
        self.jobs_contract_1.applies_from = i2d(20120325)
        self.jobs_contract_1.applies_until = i2d(20130325)
        try:
            self.jobs_contract_1.full_clean()
            self.fail("Expected ValidationError %r" % msg)
        except ValidationError as e:
            self.assertEqual(e.messages[0],msg)
            
        msg = 'Contract ends before it started.'
        self.jobs_contract_1.applies_from = i2d(20130325)
        self.jobs_contract_1.applies_until = i2d(20130131)
        try:
            self.jobs_contract_1.full_clean()
            self.fail("Expected ValidationError %s" % msg)
        except ValidationError as e:
            self.assertEqual(e.messages[0],msg)
        
        self.jobs_contract_1.save()
      
        
        #~ def test03(self):
        """
        Testing whether `/api/notes/NoteTypes/1?fmt=json` 
        has no item `templateHidden`.
        Created :blogref:`20110509`.
        See the source code at :srcref:`/lino/apps/pcsw/tests/pcsw_tests.py`.
        """
        from lino.modlib.notes.models import NoteType
        i = NoteType(build_method='appyodt',template="Default.odt",id=1)
        i.save()
        response = self.client.get('/api/notes/NoteTypes/1?fmt=json',REMOTE_USER='root')
        result = self.check_json_result(response,'data title navinfo disable_delete id')
        self.assertEqual(result['data']['template'],'Default.odt')
        self.assertEqual(result['data'].has_key('templateHidden'),False)
        
        response = self.client.get('/api/notes/NoteTypes/1?fmt=detail',REMOTE_USER='root')
        #~ print '\n'.join(response.content.splitlines()[:1])
        
        c = response.content
        
        #~ print c
        
        self.assertTrue(c.endswith('''\
<div id="body"></div>
</body></html>'''))

        if False:
            """
            TODO:
            expat has a problem to parse the HTML generated by Lino.
            Problem occurs near <div class="htmlText">...
            Note that even if the parseString gets through, we won't 
            have any INPUT elements since they will be added dynamically 
            by the JS code...
            """
            fd = file('tmp.html','w')
            fd.write(c)
            fd.close()
            
            from xml.dom import minidom 
            dom = minidom.parseString(c)
            print dom.getElementsByTagName('input')
            response = self.client.get('/api/lino/SiteConfigs/1?fmt=json')
            
            
        #~ def test04(self):
        """
        Test some features used in document templates.
        Created :blogref:`20110615`.
        See the source code at :srcref:`/lino/apps/pcsw/tests/pcsw_tests.py`.
        """
        #~ Company = dd.resolve_model('contacts.Company')
        #~ Person = dd.resolve_model('contacts.Person')
        Country = dd.resolve_model('countries.Country')
        City = dd.resolve_model('countries.City')
        be = Country(isocode="BE",name="Belgique")
        be.save()
        bxl = City(name="Bruxelles",country=be)
        bxl.save()
        p = Person(
          first_name="Jean Louis",last_name="Dupont",
          street_prefix="Avenue de la", street="gare", street_no="3", street_box="b",
          city=bxl, gender=dd.Genders.male
          )
        p.full_clean()
        p.save()
        
        #~ if 'fr' in settings.SITE.AVAILABLE_LANGUAGES:
        if settings.SITE.get_language_info('fr'):
            dd.set_language('fr')
            #~ self.assertEqual(p.get_titled_name,"Mr Jean Louis DUPONT")
            self.assertEqual(p.full_name,"M. Jean Louis DUPONT")
            self.assertEqual('\n'.join(p.address_lines()),u"""\
M. Jean Louis DUPONT
Avenue de la gare 3 b
Bruxelles
Belgique""")
        
        
        dd.set_language(None)
            
            
        #~ def test05(self):
        """
        obj2str() caused a UnicodeDecodeError when called on an object that had 
        a ForeignKey field pointing to another instance whose __unicode__() 
        contained non-ascii characters.
        See :blogref:`20110728`.
        """
        a = pcsw.Activity(name=u"Sozialhilfeempfänger")
        p = pcsw.Client(last_name="Test",activity=a)
        self.assertEqual(unicode(a),"Sozialhilfeempfänger")
        
        # Django pitfall: repr() of a model instance may return basestring containing non-ascii characters.
        self.assertEqual(type(repr(a)),str)

        # 
        self.assertEqual(dd.obj2str(a,True),"Activity(name='Sozialhilfeempf\\xe4nger')")
        a.save()
        self.assertEqual(dd.obj2str(a,True),"Activity(id=1,name='Sozialhilfeempf\\xe4nger')")
        
        expected = "Client(language='%s'," % settings.SITE.DEFAULT_LANGUAGE.django_code
        expected += "last_name='Test'"
        expected += ",client_state=ClientStates.newcomer:10"
        #~ expected += ",is_active=True"
        #~ expected += r",activity=Activity(name=u'Sozialhilfeempf\xe4nger'))"
        #~ expected += ",activity=1"
        expected += ")"
        self.assertEqual(dd.obj2str(p,True),expected)
        p.pk = 5
        self.assertEqual(dd.obj2str(p),"Client #5 (u'TEST  (5)')")
        
        
        #~ def test06(self):
        """
        :blogref:`20111003`.
        The `id` field of a Company or Person was never disabled 
        because Lino didn't recognize it as the primary key.
        
        """
        from django.db import models
        from lino.core.fields import get_data_elem
        de = get_data_elem(pcsw.Client,'id')
        #~ print de.__class__
        self.assertEqual(de.__class__,models.AutoField)
        self.assertEqual(de.primary_key,True)
        pk = Person._meta.pk
        self.assertEqual(pk.__class__,models.OneToOneField)
        self.assertEqual(pk.primary_key,True)
        self.assertEqual(pk.rel.field_name,'id')
        
        #~ self.assertEqual(de,pk)
        

        #~ def test07(self):
        """
        Bug 20120127 : VirtualFields had sneaked into wildcard columns.
        """
        wcde = [de.name for de in contacts.Companies.wildcard_data_elems()]
        #~ expected = '''\
    #~ id country city name addr1 street_prefix street street_no street_box 
    #~ addr2 zip_code region language email url phone gsm fax remarks 
    #~ partner_ptr prefix vat_id type is_active newcomer is_deprecated activity 
    #~ bank_account1 bank_account2 hourly_rate'''.split()
        expected = '''\
        id created modified country city region zip_code name addr1 street_prefix 
        street street_no street_box addr2 language email url phone gsm fax
        remarks is_obsolete activity bank_account1 bank_account2 partner_ptr 
        prefix vat_id type client_contact_type'''.split()
        s = ' '.join(wcde)
        #~ print s
        #~ print [de for de in Companies.wildcard_data_elems()]
        self.assertEqual(wcde,expected)
            

        #~ def test08(self):
        """
        Test disabled fields on imported partners
        """
        save_iip = settings.SITE.is_imported_partner
        def f(obj): return True
        settings.SITE.is_imported_partner = f
        
        
        def check_disabled(obj,df,names):
            for n in names.split():
                if not n in df:
                    self.fail(
                      "Field %r expected to be disabled on imported %s" % (n,obj))
        def check_enabled(obj,df,names):
            for n in names.split():
                if n in df:
                    self.fail(
                      "Field %r expected to be enabled on imported %s" % (n,obj))
        
        
        #~ Person = dd.resolve_model('contacts.Person')
        p = Person(last_name="Test Person")
        p.save()
        url = '/api/contacts/Person/%d?an=detail&fmt=json' % p.pk
        response = self.client.get(url,REMOTE_USER='root') # ,HTTP_ACCEPT_LANGUAGE='en')
        result = self.check_json_result(response,'navinfo disable_delete data id title')
        df = result['data']['disabled_fields']
        check_disabled(p,df,'id first_name last_name bank_account1')
        check_enabled(p,df,'gsm')
                    
        h = pcsw.Household(name="Test Household")
        h.save()
        df = households.Households.disabled_fields(h,None)
        #~ print df
        check_disabled(h,df,'name bank_account1')
        check_enabled(h,df,'gsm type')
        
                    
        # restore is_imported_partner method
        settings.SITE.is_imported_partner = save_iip

        #~ def unused_test09(self):
        #~ obj = pcsw.Client(pk=128,first_name="Erwin",last_name="Evertz")
        #~ obj.full_clean()
        #~ obj.save()
        #~ ar = cv.SoftSkillsByPerson.request(master_instance=obj)
        #~ self.assertEqual(ar.get_request_url(),"")


        #~ def test10(self):
        """
        Creates a Budget, fills it with some data, duplicates it, 
        modifies the duplicate,
        """
        from lino_welfare.modlib.debts.fixtures.std import objects
        from north.dbutils import set_language
        for obj in objects():
            obj.save()
        self.assertEqual(debts.Budget.objects.count(),0)
        b1 = debts.Budget(partner=self.max_mustermann,user=self.user_root)
        b1.fill_defaults()
        amount = decimal.Decimal(0)
        for e in b1.entry_set.all():
            e.amount = amount 
            amount += 2
            e.full_clean()
            e.save()
        ses = settings.SITE.login("root")
        set_language('de')
        for e in b1.entry_set.filter(account__ref="3010"):
            new = ses.run(e.duplicate)
            #~ e.duplicate()
        b1.full_clean()
        b1.save()
        self.assertEqual(b1.entry_set.count(),45)
        self.assertEqual(debts.Budget.objects.count(),1)
        s1 = debts.ResultByBudget.request(b1).to_rst()
        #~ print s1
        self.assertEqual(s1,"""\
========================================================= ===============
 Beschreibung                                              Betrag
--------------------------------------------------------- ---------------
 Monatliche Einkünfte                                      42,00
 Jährliche Einkünfte (48,00 / 12)                          4,00
 Monatliche Ausgaben                                       -986,00
 Monatliche Reserve für jährliche Ausgaben (836,00 / 12)   -69,67
 **Restbetrag für Kredite und Zahlungsrückstände**         **-1 009,67**
========================================================= ===============
""")
        
        #~ b2 = b1.duplicate()
        b2 = ses.run(b1.duplicate)
        self.assertEqual(debts.Budget.objects.count(),2)
        #~ b2 = debts.Budget.objects.get(pk=res.get('goto_record_id'))
        #~ s2 = b2.BudgetSummary().to_rst()
        s2 = debts.ResultByBudget.request(b2).to_rst()
        self.assertEqual(s1,s2)
        for e in b2.entry_set.all():
            if e.amount:
                e.amount = e.amount + 2
                e.full_clean()
                e.save()
            
        s1 = debts.ResultByBudget.request(b1).to_rst()
        s2 = debts.ResultByBudget.request(b2).to_rst()
        #~ s1 = b1.BudgetSummary().to_rst()
        #~ s2 = b2.BudgetSummary().to_rst()
        self.assertNotEqual(s1,s2)
            
        
        
