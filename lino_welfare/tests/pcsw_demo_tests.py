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
This module contains tests that are run on a demo database.
  
To run only this test suite::

  $ cd ~/hgwork/welfare
  $ python manage.py test lino_welfare.DemoTest
  
Methods named `test0*` do not modify any data.

"""

from __future__ import unicode_literals


import logging
logger = logging.getLogger(__name__)

from pprint import pprint
import collections

from django.conf import settings
from django.utils.encoding import force_unicode
from django.utils import translation
from django.core.exceptions import ValidationError
from django.contrib.contenttypes.models import ContentType


#~ from django.utils import unittest
#~ from django.test.client import Client
#from lino.igen import models
#from lino.modlib.contacts.models import Contact, Companies
#from lino.modlib.countries.models import Country

from lino import dd
#~ from lino.utils import i2d
#~ from lino.utils.jsgen import py2js
#~ from north import babel
#~ from lino.core.dbutils import resolve_model
#~ from djangosite.utils.test import TestCase
from djangosite.utils.djangotest import RemoteAuthTestCase


#~ pcsw = dd.resolve_app('pcsw')
cbss = dd.resolve_app('cbss')
Event = dd.resolve_model('cal.Event')

#~ Person = resolve_model('contacts.Person')
#~ Property = resolve_model('properties.Property')
#~ PersonProperty = resolve_model('properties.PersonProperty')

DEMO_OVERVIEW = """\
30 applications: sessions, about, system, contenttypes, humanize, users, changes, countries, properties, contacts, uploads, outbox, cal, households, reception, languages, accounts, lino_welfare, statbel, pcsw, cv, isip, jobs, integ, courses, newcomers, debts, cbss, notes, djangosite.
100 models:
======================================= ========= =======
 Name                                    #fields   #rows
--------------------------------------- --------- -------
 accounts.Account                        15        49
 accounts.Chart                          5         1
 accounts.Group                          9         7
 cal.Calendar                            25        9
 cal.Event                               24        %s
 cal.Guest                               10        23
 cal.GuestRole                           9         4
 cal.Priority                            6         9
 cal.Room                                5         0
 cal.Subscription                        4         72
 cal.Task                                20        15
 cbss.IdentifyPersonRequest              20        5
 cbss.ManageAccessRequest                23        1
 cbss.Purpose                            7         106
 cbss.RetrieveTIGroupsRequest            14        2
 cbss.Sector                             11        209
 changes.Change                          9         0
 contacts.Company                        30        38
 contacts.CompanyType                    9         16
 contacts.Partner                        25        117
 contacts.Person                         31        76
 contacts.Role                           4         10
 contacts.RoleType                       6         5
 contenttypes.ConcreteModel              2         0
 contenttypes.ContentType                4         100
 contenttypes.FooWithBrokenAbsoluteUrl   3         0
 contenttypes.FooWithUrl                 3         0
 contenttypes.FooWithoutUrl              2         0
 contenttypes.ProxyModel                 2         0
 countries.City                          10        73
 countries.Country                       8         8
 courses.Course                          5         3
 courses.CourseContent                   2         2
 courses.CourseOffer                     5         3
 courses.CourseProvider                  31        2
 courses.CourseRequest                   10        20
 cv.LanguageKnowledge                    7         119
 debts.Actor                             6         6
 debts.Budget                            11        3
 debts.Entry                             16        147
 households.Household                    28        3
 households.Member                       6         6
 households.Role                         6         6
 households.Type                         5         4
 isip.Contract                           26        13
 isip.ContractEnding                     6         4
 isip.ContractType                       10        5
 isip.ExamPolicy                         20        5
 isip.StudyType                          5         8
 jobs.Candidature                        8         74
 jobs.Contract                           28        13
 jobs.ContractType                       9         5
 jobs.Experience                         10        30
 jobs.Function                           7         4
 jobs.Job                                10        8
 jobs.JobProvider                        31        3
 jobs.JobType                            4         5
 jobs.Offer                              9         1
 jobs.Regime                             5         3
 jobs.Schedule                           5         3
 jobs.Sector                             6         14
 jobs.Study                              12        2
 languages.Language                      6         5
 newcomers.Broker                        2         2
 newcomers.Competence                    5         7
 newcomers.Faculty                       6         5
 notes.EventType                         10        10
 notes.Note                              15        110
 notes.NoteType                          13        16
 outbox.Attachment                       4         0
 outbox.Mail                             9         0
 outbox.Recipient                        6         0
 pcsw.Activity                           3         0
 pcsw.AidType                            5         7
 pcsw.Client                             73        61
 pcsw.ClientContact                      7         0
 pcsw.ClientContactType                  5         5
 pcsw.Coaching                           8         77
 pcsw.CoachingEnding                     7         4
 pcsw.CoachingType                       5         3
 pcsw.Dispense                           6         0
 pcsw.DispenseReason                     6         4
 pcsw.Exclusion                          6         0
 pcsw.ExclusionType                      2         2
 pcsw.PersonGroup                        4         5
 properties.PersonProperty               6         310
 properties.PropChoice                   7         2
 properties.PropGroup                    5         3
 properties.PropType                     9         3
 properties.Property                     7         23
 sessions.Session                        3         4
 system.HelpText                         4         5
 system.SiteConfig                       29        1
 system.TextFieldTemplate                6         2
 uploads.Upload                          11        0
 uploads.UploadType                      2         5
 users.Authority                         3         3
 users.Membership                        3         0
 users.Team                              5         3
 users.User                              18        10
======================================= ========= =======
""" 



# Note: the number of cal.Event records may vary depending on the creation date of the database
# because of the automatic weekly evaluations of isip and jobs contracts .

class PseudoRequest:
    def __init__(self,name):
        self.user = settings.SITE.user_model.objects.get(username=name)
        self.subst_user = None


class DemoTest(RemoteAuthTestCase):
    maxDiff = None
    #~ fixtures = [ 'std','demo' ]
    fixtures = settings.SITE.demo_fixtures
    #~ fixtures = 'std few_countries few_cities few_languages props cbss democfg demo demo2'.split()
    #~ fixtures = 'std all_countries few_cities all_languages props demo'.split()
    #~ never_build_site_cache = True
    
    #~ avoid do_print failure due to build_absolute_uri() when use_davlink is True
    override_djangosite_settings = dict(use_davlink=False)
    
    #~ def setUp(self):
        #~ settings.SITE.never_build_site_cache = True
        #~ super(DemoTest,self).setUp()

        
    def test001(self):
        
        global DEMO_OVERVIEW
        DEMO_OVERVIEW = DEMO_OVERVIEW % Event.objects.all().count()
        s = settings.SITE.get_db_overview_rst()
        #~ print s
        self.assertEqual(DEMO_OVERVIEW,s)
        
        """
        Test the number of rows returned for certain queries
        """
        cases = []
        Query = collections.namedtuple('Query',
          ['username','url_base','json_fields','expected_rows','kwargs'])
        def add_case(username,url_base,json_fields,expected_rows,**kwargs):
            cases.append(Query(username,url_base,json_fields,expected_rows,kwargs))
            
        json_fields = 'count rows title success no_data_text'
        kw = dict(fmt='json',limit=10,start=0)
        add_case('rolf','api/contacts/Companies',json_fields,39,**kw)
        add_case('rolf','api/households/Households',json_fields,4,**kw)
        add_case('rolf','api/contacts/Partners',json_fields,118,**kw)
        add_case('rolf','api/courses/CourseProviders',json_fields,3,**kw)
        add_case('rolf','api/courses/CourseOffers',json_fields,4,**kw)
        add_case('rolf','api/countries/Countries',json_fields,9,**kw)
        add_case('rolf','api/jobs/JobProviders',json_fields,4,**kw)
        add_case('rolf','api/jobs/Jobs',json_fields,9,**kw)
        mt = ContentType.objects.get_for_model(cbss.RetrieveTIGroupsRequest).pk
        add_case('rolf','api/cbss/RetrieveTIGroupsResult',json_fields,18,mt=mt,mk=1,**kw)
        
        json_fields = 'count rows title success no_data_text param_values'
        add_case('rolf','api/courses/PendingCourseRequests',json_fields,18,**kw)
        add_case('rolf','api/contacts/Persons',json_fields,70,**kw)
        add_case('rolf','api/pcsw/Clients',json_fields,29,**kw)
        add_case('rolf','api/pcsw/DebtsClients',json_fields,0,**kw)
        add_case('rolf','api/cal/MyEvents',json_fields,13,**kw)
        add_case('rolf','api/newcomers/NewClients',json_fields,28,**kw)
        add_case('rolf','api/newcomers/AvailableCoachesByClient',json_fields,2,mt=50,mk=119,**kw)
        add_case('alicia','api/integ/Clients',json_fields,5,**kw)
        add_case('hubert','api/integ/Clients',json_fields,23,**kw)
        
        alicia = settings.SITE.user_model.objects.get(username='alicia')
        kw = dict(fmt='json',limit=20,start=0,su=alicia.pk) # rolf working as alicia
        add_case('rolf','api/integ/Clients',json_fields,5,**kw)
        
        
        kw = dict() 
        json_fields = 'count rows'
        add_case('rolf','choices/cv/SkillsByPerson/property',json_fields,6,**kw)
        add_case('rolf','choices/cv/ObstaclesByPerson/property',json_fields,15,**kw)
        add_case('rolf','choices/pcsw/ContactsByClient/company?type=1',json_fields,5,**kw)
        
        if False: # TODO
            add_case('rolf','choices/pcsw/ContactsByClient/company?type=1&query=mutu',json_fields,2,**kw)
            
        #~ kw = dict(fmt='json',an='detail') 
        #~ json_fields = 'count rows'
        #~ http://127.0.0.1:8000/?_dc=1369640821168&an=detail&rp=ext-comp-1340&fmt=json
        #~ add_case('rolf','api/debts/Budgets/3',json_fields,1,**kw)
            
        
        failures = 0
        for i,case in enumerate(cases):
            url = settings.SITE.build_admin_url(case.url_base,**case.kwargs)
            msg = 'Using remote authentication, but no user credentials found.'
            try:
                response = self.client.get(url) 
                self.fail("Expected '%s'" % msg)
            except Exception as e:
                self.assertEqual(str(e),msg)
                
            response = self.client.get(url,REMOTE_USER='foo') 
            self.assertEqual(response.status_code,403,"Status code for anonymous on GET %s" % url)
            
            response = self.client.get(url,REMOTE_USER=case.username)
            #~ if response.status_code != 200:
                #~ msg = "%s returned status_code %s" % (url,response.status_code)
                #~ print "[%d] %s" % (i, msg)
                #~ failures += 1
                #~ continue
            try:
                result = self.check_json_result(response,case.json_fields,url)
                
                num = case.expected_rows
                if not isinstance(num,tuple):
                    num = [num]
                if result['count'] not in num:
                    msg = "%s got %s rows instead of %s" % (url,result['count'],num)
                    print "[%d] %s" % (i, msg)
                    failures += 1
                
            #~ except self.failureException as e:
            except Exception as e:
                print "[%d] %s:\n%s" % (i, url,e)
                failures += 1
                
        if failures:
            msg = "%d URL failures" % failures
            self.fail(msg)


        #~ def test002(self):
        """
        Printing a Budget
        The same as in tests/debts.rst, but a different implementation
        """
        
        #~ settings.SITE.override_defaults(use_davlink=False)
            
        from lino.runtime import debts
        ses = settings.SITE.login('rolf')
        obj = debts.Budget.objects.get(pk=3)
        
        res = ses.run(obj.do_clear_cache)
        #~ print __file__, 20130414, repr(res)
        #~ msg = res['message'].decode('utf-8')
        msg = res['message']
        self.assertEqual(msg,'Budget 3 for Ausdemwald-Charlier printable cache has been cleared.')
        
        res = ses.run(obj.do_print)
        #~ print __file__, 20130414, repr(res)
        msg = res['message']
        #~ msg = res['message'].decode('utf-8')
        #~ self.assertEqual(msg,'Dokument Budget Nr. 3 für Altenberg-Charlier wurde generiert.')
        self.assertEqual(msg,'Budget 3 for Ausdemwald-Charlier printable has been built.')
        self.assertEqual(res['open_url'],'/media/userdocs/appyodt/debts.Budget-3.odt')



        """
        20130418 server traceback 
        TypeError at /plain/pcsw/UsersWithClients
        cannot serialize 90 (type int)
        """
        #~ from lino_welfare.modlib.pcsw.fixtures.std import objects
        #~ for obj in objects():
            #~ obj.save()
      
        url = settings.SITE.build_admin_url('plain/integ/UsersWithClients?cw=90&cw=45&cw=45&cw=45&cw=45&cw=45&cw=45&cw=45&cw=45&ch=&ch=&ch=&ch=&ch=&ch=&ch=&ch=&ch=&ci=user&ci=G1&ci=G2&ci=G4&ci=G4bis&ci=G9&ci=primary_clients&ci=active_clients&ci=row_total&name=0')
        response = self.client.get(url,REMOTE_USER='rolf')
        self.assertEqual(response.status_code,200)
        if not response.content.startswith('<!DOCTYPE html>\n<html language="en"><head>'):
            self.fail("Failed: UsersWithClients responded %r",response.content)
        #~ result = self.check_json_result(response,'',url)


        """
        All demo requests should have at least one row of result.
        This test
        """
        ses = settings.SITE.login('rolf')
        for obj in cbss.RetrieveTIGroupsRequest.objects.all():
            msg = "%s has no result" % obj
            self.assertNotEqual(obj.Result(ses).get_total_count(),0,msg)




    def unused_test001(self):
        """
        Some simple tests:
        - total number of Person records
        - name of some person
        """
        Person = dd.resolve_model('contacts.Person')
        #~ from lino.projects.pcsw.models import Person
        self.assertEquals(Person.objects.count(), 78)
        
        p = Person.objects.get(pk=118)
        #~ self.assertEquals(unicode(p), "ARENS Annette (118)")
        #~ self.assertEquals(unicode(p), "AUSDEMWALD Alfons (118)")
        #~ self.assertEquals(unicode(p), "COLLARD Charlotte (118)")
        self.assertEquals(unicode(p), "Herrn Laurent BASTIAENSEN")
        #~ self.assertEquals(unicode(p), "BASTIAENSEN Laurent (118)")
        
            
    def unused_test002(self):
        """
        Tests whether SoftSkillsByPerson works and whether it returns language-specific labels.
        Bug discovered :blogref:`20110228`.
        See also :blogref:`20110531`.
        See the source code at :srcref:`/lino/apps/pcsw/tests/pcsw_demo_tests.py`.
        """
        #~ from lino.modlib.users.models import User
        #~ u = User.objects.get(username='rolf')
        #~ lang = u.language
        #~ u.language = '' # HTTP_ACCEPT_LANGUAGE works only when User.language empty
        #~ u.save()
        
        settings.SITE.ui # trigger ui instance
        
        obj = pcsw.Client.objects.get(pk=128)
        ar = cv.SoftSkillsByPerson.request(master_instance=obj)
        
        pk = 128
        mt = 44 
        url = '/api/cv/SoftSkillsByPerson?mt=%d&mk=%d&fmt=json' % (mt,pk)
        
        #~ if 'en' in babel.AVAILABLE_LANGUAGES:
        if settings.SITE.get_language_info('en'):
            response = self.client.get(url,REMOTE_USER='robin',HTTP_ACCEPT_LANGUAGE='en')
            #~ result = self.check_json_result(response,'count rows gc_choices disabled_actions title')
            result = self.check_json_result(response,'count rows title success no_data_text')
            self.assertEqual(result['title'],"Soft skills of EVERS Eberhart (%d)" % pk)
            self.assertEqual(len(result['rows']),2)
            row = result['rows'][0]
            self.assertEqual(row[0],"Obedient")
            #~ self.assertEqual(row[1],7)
            self.assertEqual(row[2],"moderate")
            self.assertEqual(row[3],"2")
            
        #~ if 'de' in babel.AVAILABLE_LANGUAGES:
        if settings.SITE.get_language_info('de'):
            response = self.client.get(url,REMOTE_USER='rolf',HTTP_ACCEPT_LANGUAGE='de')
            result = self.check_json_result(response,'count rows title success no_data_text')
            self.assertEqual(result['title'],"Eigenschaften von EVERS Eberhart (%d)" % pk)
            self.assertEqual(len(result['rows']),2)
            row = result['rows'][0]
            self.assertEqual(row[0],"Gehorsam")
            #~ self.assertEqual(row[1],7)
            self.assertEqual(row[2],"mittelmäßig")
            self.assertEqual(row[3],"2")
            
        #~ 20111111 babel.set_language(None) # switch back to default language for subsequent tests
        
        u.language = lang
        u.save()
        
        
        #~ tf('http://127.0.0.1:8000/api/properties/SoftSkillsByPerson?_dc=1298881440121&fmt=json&mt=22&mk=15',
            #~ """
            #~ { 
            #~ count: 3, 
            #~ rows: [ 
              #~ [ "Gehorsam", 7, "mittelm\u00e4\u00dfig", "2", null, 53, "Sozialkompetenzen", 2 ], 
              #~ [ "F\u00fchrungsf\u00e4higkeit", 8, "mittelm\u00e4\u00dfig", "2", null, 54, "Sozialkompetenzen", 2 ], 
              #~ [ null, null, null, null, null, null, "Sozialkompetenzen", 2 ] 
            #~ ], 
            #~ gc_choices: [  ], 
            #~ title: "~Eigenschaften pro Person Arens Annette (15)" 
            #~ }
            #~ """)
        


    def unused_test003(self):
        """
        Test whether the AJAX call issued for Detail of Annette Arens is correct.
        """
        cases = [
        #  [ id,         name, recno, first, prev, next, last ]
           [ 119, "Charlier",     8,   199,  201,  118, 166  ],
           [ 167, "Ärgerlich",   56,   199,  164,  166, 166  ],
           [ 166, "Östges",      57,   199,  167, None, 166  ],
        ]
        # 
        for case in cases:
            url = '/api/contacts/Persons/%s?fmt=json' % case[0]
            response = self.client.get(url,REMOTE_USER='root')
            result = self.check_json_result(response,'navinfo disable_delete data id title')
            # disabled because they depend on local database sorting configuration
            # re-enabled because demo fixtures no longer contain cyrillic chars
            self.assertEqual(result['data']['last_name'],case[1])
            self.assertEqual(result['navinfo']['recno'],case[2])
            self.assertEqual(result['navinfo']['first'],case[3]) 
            self.assertEqual(result['navinfo']['prev'],case[4]) 
            self.assertEqual(result['navinfo']['next'],case[5])
            self.assertEqual(result['navinfo']['last'],case[6])
                
                
    def unused_test004(self):
        """
        Test whether date fields are correctly parsed.
        """
        for value in ('01.03.2011','15.03.2011'):
            url = '/api/jobs/Contracts/1'
            #~ data =  'applies_from='+value+'&applies_until=17.05.2009&company=R-Cycle%20'
            #~ 'Sperrgutsortierzentrum&companyHidden=83&contact=Arens%20Andreas%20(1'
            #~ '4)%20(Gesch%C3%A4ftsf%C3%BChrer)&contactHidden=2&date_decided=&date_e'
            #~ 'nded=&date_issued=&delay_type=Tage&delay_typeHidden=D&delay_value=0&du'
            #~ 'ration=&ending=Vertragsbeendigung%20ausw%C3%A4hlen...&endingHidden=&lan'
            #~ 'guage=Deutsch&languageHidden=de&person=Altenberg%20Hans%20(16)&personHi'
            #~ 'dden=16&reminder_date=11.11.2010&reminder_text=demo%20reminder&type=Kon'
            #~ 'vention%20Art.60%C2%A77%20Sozial%C3%B6konomie&typeHidden=1&user=root&us'
            #~ 'erHidden=4&user_asd=Benutzer%20ausw%C3%A4hlen...&user_asdHidden='
            data =  'applies_from='+value
            
            response = self.request_PUT(url,data,REMOTE_USER='root')
            result = self.check_json_result(response,'message success data_record')
            self.assertEqual(result['success'],True)
            self.assertEqual(result['data_record']['data']['applies_from'],value)
            
            url = "/api/jobs/Contracts/1?fmt=json"
            response = self.client.get(url,REMOTE_USER='root')
            #~ print 20110723, response
            result = self.check_json_result(response,'navinfo disable_delete data id title')
            self.assertEqual(result['data']['applies_from'],value)

    def unused_test005(self):
        """
        Simplification of test04, used to write Lino ticket #27.
        """
        url ='/api/countries/Countries/BE'
        value = 'Belgienx'
        data = 'name=%s&nameHidden=Belgienx&fmt=json' % value
        response = self.request_PUT(url,data,REMOTE_USER='root')
        #~ response = self.client.put(url,data,content_type='application/x-www-form-urlencoded')
        result = self.check_json_result(response,'message success data_record')
        self.assertEqual(result['success'],True)
        self.assertEqual(result['data_record']['data']['name'],value)
        
        url ='/api/countries/Countries/BE?fmt=json'
        response = self.client.get(url,REMOTE_USER='root')
        result = self.check_json_result(response,'navinfo disable_delete data id title')
        self.assertEqual(result['data']['name'],value)


    def unused_test006(self):
        """
        Testing BabelValues.
        """
        from lino.utils import babel
        from lino_welfare.modlib.pcsw.models import Person
        #~ from lino.apps.pcsw.models import Property, PersonProperty
        Property = settings.SITE.modules.properties.Property
        PersonProperty = settings.SITE.modules.properties.PersonProperty
        annette = Person.objects.get(pk=118)
        self.assertEquals(unicode(annette), "ARENS Annette (118)")
        
        p = Property.objects.get(id=2) # "Obedient"
        pp = PersonProperty.objects.filter(property=p)[0]
        
        #~ if 'en' in babel.AVAILABLE_LANGUAGES:
        with translation.override('en'):
        #~ if settings.SITE.get_language_info('en'):
            #~ dd.set_language('en')
            self.assertEquals(unicode(p), u"Obedient")
            self.assertEquals(unicode(pp), u"not at all")

        #~ if 'de' in babel.AVAILABLE_LANGUAGES:
        with translation.override('de'):
        #~ if settings.SITE.get_language_info('de'):
            #~ dd.set_language('de')
            self.assertEquals(unicode(p), u"Gehorsam")
            self.assertEquals(unicode(pp), u"gar nicht")
        
        #~ if 'fr' in babel.AVAILABLE_LANGUAGES:
        with translation.override('fr'):
        #~ if settings.SITE.get_language_info('fr'):
            #~ dd.set_language('fr')
            self.assertEquals(unicode(p), u"Obéissant")
            self.assertEquals(unicode(pp), u"pas du tout")
        
        #~ dd.set_language(None) # switch back to default language for subsequent tests
        

    def unused_test009(self):
        """
        This tests for the bug discovered :blogref:`20110610`.
        See the source code at :srcref:`/lino/apps/pcsw/tests/pcsw_demo_tests.py`.
        """
        #~ dd.set_language('en')
        url = '/choices/jobs/StudiesByPerson/city?start=0&limit=30&country=&query='
        response = self.client.get(url,REMOTE_USER='root')
        result = self.check_json_result(response,'count rows')
        #~ self.assertEqual(result['title'],u"Choices for city")
        self.assertEqual(len(result['rows']),30)
        #~ dd.set_language(None) # switch back to default language for subsequent tests

    def unused_test010(self):
        """
        Test the unique_together validation of City
        See :blogref:`20110610` and :blogref:`20110611`.
        See the source code at :srcref:`/lino/apps/pcsw/tests/pcsw_demo_tests.py`.
        """
        from lino.modlib.countries.models import City, Country
        from django.db.utils import IntegrityError
        be = Country.objects.get(pk='BE')
        try:
            City(name="Eupen",country=be,zip_code='4700').save()
        except IntegrityError:
            if settings.SITE.allow_duplicate_cities:
                self.fail("Got IntegrityError though allow_duplicate_cities should be allowed.")
        else:
            if not settings.SITE.allow_duplicate_cities:
                self.fail("Expected IntegrityError")
            
        
        try:
            be.city_set.create(name="Eupen",zip_code='4700')
        except IntegrityError:
            if settings.SITE.allow_duplicate_cities:
                self.fail("Got IntegrityError though allow_duplicate_cities should be allowed.")
        else:
            if not settings.SITE.allow_duplicate_cities:
                self.fail("Expected IntegrityError")
            
        
    def unused_test011(self):
        """
        Tests whether the user problem 
        described in :blogref:`20111206` 
        is solved.
        """
        from lino_welfare.modlib.jobs.models import Contract
        obj = Contract.objects.get(pk=5)
        with translation.override('de'):
            self.assertEqual(obj.contact.person.get_full_name(),"Herrn Hans ALTENBERG")
        #~ dd.set_language(None)
        #~ translation.deactivate()
        
        
    def unused_test012(self):
        """
        Test whether the contact person of a jobs contract is correctly filled in
        when the provider has exactly one contact person.
        """
        from lino_welfare.modlib.jobs.models import Contract, JobProvider, Job
        from lino_welfare.modlib.pcsw.models import Person
        from lino.modlib.users.models import User
        u = User.objects.get(username='root')
        #~ qs = Person.objects.order_by('last_name','first_name')
        p = Person.objects.get(pk=177) # Emil Eierschal
        #~ e = Employer.objects.get(pk=185)
        j = Job.objects.get(pk=1) # bisa
        c = Contract(person=p,user=u,job=j,applies_from=p.coached_from,duration=312)
        c.full_clean()
        c.save()
        self.assertEqual(c.contact.person.pk,118)
        #~ self.assertEqual(c.applies_until,p.coached_from+datetime.timedelta(days=))
        

    def unused_test014(self):
        """
        Tests for the bug discovered :blogref:`20111222`.
        """
        for url in """\
        /choices/isip/Contract/person?start=0&limit=10&query=
        /choices/contacts/Person/city?start=0&limit=10&country=BE&query=
        /choices/jobs/Contract/duration
        """.splitlines():
          url = url.strip()
          if url and not url.startswith("#"):
              response = self.client.get(url,REMOTE_USER='root')
              result = self.check_json_result(response,'count rows')
              #~ self.assertEqual(result['title'],u"Choices for city")
              self.assertEqual(len(result['rows']),min(result['count'],10))

    def unused_test015(self):
        """
        Temporary bug on :blogref:`20111223`.
        """
        url = '/api/contacts/Persons/-99999?fmt=json&an=insert'
        response = self.client.get(url,REMOTE_USER='root')
        result = self.check_json_result(response,'data phantom title')
        self.assertEqual(result['phantom'],True)

    def unused_test015b(self):
        """
        Test whether PropsByGroup has a detail.
        20120218 : "properties.PropsByGroup has no action u'detail'"
        """
        cases = [
          ('/api/properties/PropsByGroup/%s?mt=11&mk=1&an=detail&fmt=json',8),
          ('/api/contacts/AllPartners/%s?an=detail&fmt=json',117),
        ]
        for case in cases:
            url = case[0] % case[1]
            response = self.client.get(url,REMOTE_USER='root')
            result = self.check_json_result(response,
              'navinfo disable_delete data title disabled_actions id')
            self.assertEqual(result['id'],case[1])


    def unused_test016(self):
        """
        All rows of persons_by_user now clickable.
        See :blogref:`20111223`.
        """
        cases = [
          ['root', 19],
          ['alicia', 17],
        ]
        for case in cases:
            url = '/api/pcsw/MyPersons?fmt=json&limit=30&start=0&su=%s' % case[0]
            response = self.client.get(url,REMOTE_USER='root')
            result = self.check_json_result(response,'count rows gc_choices disabled_actions title')
            self.assertEqual(result['count'],case[1])
            
            
    def unused_test017(self):
        # moved to docs/tested
        Budget = resolve_model('debts.Budget')
        bud = Budget.objects.get(pk=3)
        s = bud.BudgetSummary().to_rst()
        #~ print s
        self.assertEquivalent(s,"""
        ========================================================= ==============
         Beschreibung                                              Betrag
        --------------------------------------------------------- --------------
         Monatliche Einkünfte                                      5 000,00
         Jährliche Einkünfte (2 400,00 / 12)                       200,00
         Monatliche Ausgaben                                       -550,00
         Monatliche Reserve für jährliche Ausgaben (236,00 / 12)   -19,67
         Raten der laufenden Kredite                               -45,00
         **Finanzielle Situation**                                 **4 585,33**
        ========================================================= ==============
        """)
        
            
    def unused_test101(self):
        """
        First we try to uncheck the is_jobprovider checkbox on 
        the Company view of a JobProvider. 
        This should fail since the JP has Jobs and Contracts.
        """
        Company = resolve_model('contacts.Company')
        JobProvider = resolve_model('jobs.JobProvider')
        Job = resolve_model('jobs.Job')
        Contract = resolve_model('jobs.Contract')
        bisaProvider = JobProvider.objects.get(name='BISA')
        bisaCompany = Company.objects.get(name='BISA')
        
        # it should work even on an imported partner
        save_iip = settings.SITE.is_imported_partner
        def f(obj): return True
        settings.SITE.is_imported_partner = f
        
        JOBS = Job.objects.filter(provider=bisaProvider)
        self.assertEqual(JOBS.count(),3)
        rr = PseudoRequest('rolf')
        try:
            Company.is_jobprovider.set_value_in_object(rr,bisaCompany,False)
            self.fail("Expected ValidationError")
        except ValidationError, e:
            # cannot delete because there are 3 Jobs referring to BISA
            pass
        for job in JOBS:
            for cont in Contract.objects.filter(job=job):
                cont.delete()
            job.delete()
        Company.is_jobprovider.set_value_in_object(rr,bisaCompany,False)
        
        bisaCompany = Company.objects.get(name='BISA') # still exists
        
        try:
            bisaProvider = JobProvider.objects.get(name='BISA')
            self.fail("Expected JobProvider.DoesNotExist")
        except JobProvider.DoesNotExist,e:
            pass
        
        # restore is_imported_partner method
        settings.SITE.is_imported_partner = save_iip
        

