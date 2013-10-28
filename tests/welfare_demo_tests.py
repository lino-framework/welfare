# -*- coding: UTF-8 -*-
## Copyright 2013 Luc Saffre
## This file is part of the Lino-Welfare project.
## Lino-Welfare is free software; you can redistribute it and/or modify 
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 3 of the License, or
## (at your option) any later version.
## Lino-Welfare is distributed in the hope that it will be useful, 
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
## GNU General Public License for more details.
## You should have received a copy of the GNU General Public License
## along with Lino-Welfare; if not, see <http://www.gnu.org/licenses/>.

"""
To run only this test::
 
  $ go welfare
  $ python setup.py test -s tests.welfare_demo_tests

"""
from lino.utils.test import DemoTestCase
from django.contrib.contenttypes.models import ContentType
from lino.runtime import *

class MyTestCase(DemoTestCase):
    
    
    def test_001(self):
        
        
        #~ ut = self.make_url_tester()
        
        json_fields = 'count rows title success no_data_text'
        kw = dict(fmt='json',limit=10,start=0)
        self.demo_get('rolf','api/contacts/Companies',json_fields,39,**kw)
        #~ ut.add_case('rolf','api/households/Households',json_fields,4,**kw)
        self.demo_get('rolf','api/households/Households',json_fields,4,**kw)
        self.demo_get('rolf','api/contacts/Partners',json_fields,118,**kw)
        self.demo_get('rolf','api/courses/CourseProviders',json_fields,3,**kw)
        self.demo_get('rolf','api/courses/CourseOffers',json_fields,4,**kw)
        self.demo_get('rolf','api/countries/Countries',json_fields,9,**kw)
        self.demo_get('rolf','api/jobs/JobProviders',json_fields,4,**kw)
        self.demo_get('rolf','api/jobs/Jobs',json_fields,9,**kw)
        
        mt = ContentType.objects.get_for_model(cbss.RetrieveTIGroupsRequest).pk
        self.demo_get('rolf','api/cbss/RetrieveTIGroupsResult',json_fields,18,mt=mt,mk=1,**kw)
        
        json_fields = 'count rows title success no_data_text param_values'
        self.demo_get('rolf','api/courses/PendingCourseRequests',json_fields,18,**kw)
        self.demo_get('rolf','api/contacts/Persons',json_fields,70,**kw)
        self.demo_get('rolf','api/pcsw/Clients',json_fields,29,**kw)
        self.demo_get('rolf','api/pcsw/DebtsClients',json_fields,0,**kw)
        self.demo_get('rolf','api/cal/MyEvents',json_fields,13,**kw)
        self.demo_get('rolf','api/newcomers/NewClients',json_fields,28,**kw)
        self.demo_get('rolf','api/newcomers/AvailableCoachesByClient',json_fields,2,mt=50,mk=119,**kw)
        self.demo_get('alicia','api/integ/Clients',json_fields,5,**kw)
        self.demo_get('hubert','api/integ/Clients',json_fields,23,**kw)
        
        alicia = settings.SITE.user_model.objects.get(username='alicia')
        kw = dict(fmt='json',limit=20,start=0,su=alicia.pk) # rolf working as alicia
        self.demo_get('rolf','api/integ/Clients',json_fields,5,**kw)
        
        
        kw = dict() 
        json_fields = 'count rows'
        self.demo_get('rolf','choices/cv/SkillsByPerson/property',json_fields,6,**kw)
        self.demo_get('rolf','choices/cv/ObstaclesByPerson/property',json_fields,15,**kw)
        self.demo_get('rolf','choices/pcsw/ContactsByClient/company?type=1',json_fields,5,**kw)
        
        if False: # TODO
            self.demo_get('rolf','choices/pcsw/ContactsByClient/company?type=1&query=mutu',json_fields,2,**kw)
            
        #~ ut.run_tests()
        
        

        #~ 
#~ 
        #~ json_fields = 'count rows title success no_data_text param_values'
        #~ kw = dict(fmt='json',limit=10,start=0)
        #~ mt = ContentType.objects.get_for_model(courses.Line).pk
#~ 
        #~ ut.add_case('rolf','api/courses/CoursesByLine',json_fields,4,mt=mt,mk=1,**kw)
        #~ ut.run_tests()
#~ 

