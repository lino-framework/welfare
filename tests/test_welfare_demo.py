# -*- coding: UTF-8 -*-
## Copyright 2013-2014 Luc Saffre
# License: BSD (see file COPYING for details)

"""
This runs a suite of JSON queries on the test database.

To run only this test::
 
  $ go welfare
  $ python setup.py test -s tests.test_welfare_demo

"""

import os
os.environ['DJANGO_SETTINGS_MODULE'] = \
    'lino_welfare.projects.docs.settings.doctests'

from lino.utils.test import DemoTestCase
from django.contrib.contenttypes.models import ContentType

from lino.runtime import *


class MyTestCase(DemoTestCase):
    
    def test_001(self):
        
        json_fields = 'count rows title success no_data_text'
        kw = dict(fmt='json', limit=10, start=0)
        self.demo_get(
            'rolf', 'api/contacts/Companies', json_fields, 50, **kw)
        self.demo_get(
            'rolf', 'api/households/Households', json_fields, 15, **kw)
        self.demo_get(
            'rolf', 'api/contacts/Partners', json_fields, 173, **kw)
        self.demo_get(
            'rolf', 'api/courses/CourseProviders', json_fields, 3, **kw)
        self.demo_get(
            'rolf', 'api/courses/CourseOffers', json_fields, 4, **kw)
        self.demo_get(
            'rolf', 'api/countries/Countries', json_fields, 9, **kw)
        self.demo_get('rolf', 'api/jobs/JobProviders', json_fields, 4, **kw)
        self.demo_get('rolf', 'api/jobs/Jobs', json_fields, 9, **kw)
        
        mt = ContentType.objects.get_for_model(cbss.RetrieveTIGroupsRequest).pk
        self.demo_get('rolf', 'api/cbss/RetrieveTIGroupsResult',
                      json_fields, 18, mt=mt, mk=1, **kw)
        
        json_fields = 'count rows title success no_data_text param_values'
        self.demo_get(
            'rolf', 'api/courses/PendingCourseRequests', json_fields, 19, **kw)
        self.demo_get(
            'rolf', 'api/contacts/Persons', json_fields, 101, **kw)
        self.demo_get('rolf', 'api/pcsw/Clients', json_fields, 30, **kw)
        self.demo_get('rolf', 'api/debts/Clients', json_fields, 0, **kw)
        self.demo_get('rolf', 'api/cal/MyEvents', json_fields, 13, **kw)
        self.demo_get(
            'rolf', 'api/newcomers/NewClients', json_fields, 29, **kw)
        self.demo_get(
            'rolf', 'api/newcomers/AvailableCoachesByClient', json_fields,
            2, mt=50, mk=120, **kw)
        self.demo_get('alicia', 'api/integ/Clients', json_fields, 7, **kw)
        self.demo_get('hubert', 'api/integ/Clients', json_fields, 19, **kw)
        
        alicia = settings.SITE.user_model.objects.get(username='alicia')
        # rolf working as alicia:
        kw = dict(fmt='json', limit=20, start=0, su=alicia.pk)
        self.demo_get('rolf', 'api/integ/Clients', json_fields, 7, **kw)
        
        kw = dict()
        json_fields = 'count rows'
        self.demo_get(
            'rolf', 'choices/cv/SkillsByPerson/property', json_fields, 6, **kw)
        self.demo_get(
            'rolf', 'choices/cv/ObstaclesByPerson/property', json_fields,
            15, **kw)
        self.demo_get(
            'rolf', 'choices/pcsw/ContactsByClient/company?type=1',
            json_fields, 4, **kw)

        self.demo_get(
            'rolf', 'choices/aids/IncomeConfirmations/aid_type',
            json_fields, 11, **kw)
        
        self.demo_get(
            'rolf', 'choices/aids/RefundConfirmations/aid_type',
            json_fields, 11, **kw)
        
        if False: # TODO
            self.demo_get('rolf','choices/pcsw/ContactsByClient/company?type=1&query=mutu',json_fields,2,**kw)
            
        
