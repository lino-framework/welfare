# -*- coding: UTF-8 -*-
## Copyright 2013 Luc Saffre
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
This module contains "watch_tim" tests. 
You can run only these tests by issuing::

  python manage.py test pcsw.WatchTimTest
  
"""

from __future__ import unicode_literals

CHANGELOG_LINES = """
{"method":"POST","alias":"PAR","id":"0000023633","time":"20130220 08:55:30","user":"MELANIE","data":{"IDPAR":"0000023633","FIRME":"Schneider Georges","NAME2":"","RUE":"","CP":"","IDPRT":"S","PAYS":"B","TEL":"","FAX":"","COMPTE1":"","NOTVA":"","COMPTE3":"","IDPGP":"","DEBIT":"","CREDIT":"","ATTRIB":"N","IDMFC":"30","LANGUE":"D","IDBUD":"","PROF":"80","CODE1":"","CODE2":"","CODE3":"","DATCREA":{"__date__":{"year":2013,"month":2,"day":20}},"ALLO":"","NB1":"","NB2":"","IDDEV":"","MEMO":"","COMPTE2":"","RUENUM":"","RUEBTE":"","DEBIT2":"","CREDIT2":"","IMPDATE": {"__date__":{"year":0,"month":0,"day":0}},"ATTRIB2":"","CPTSYSI":"","EMAIL":"","MVIDATE":{"__date__":{"year":0,"month":0,"day":0}},"IDUSR":"","DOMI1":""}}
"""



import logging
logger = logging.getLogger(__name__)

#~ from django.utils import unittest
#~ from django.test.client import Client
from django.conf import settings

#from lino.igen import models
#from lino.modlib.contacts.models import Contact, Companies
#from lino.modlib.countries.models import Country
#~ from lino.modlib.contacts.models import Companies


from lino import dd
from lino.utils import i2d
from lino.utils import babel
#~ from lino.core.modeltools import resolve_model
#Companies = resolve_model('contacts.Companies')
from lino.utils.test import TestCase

#~ Person = dd.resolve_model('contacts.Person')
Client = dd.resolve_model('pcsw.Client')
#~ Property = dd.resolve_model('properties.Property')
#~ PersonProperty = dd.resolve_model('properties.PersonProperty')

#~ from lino.apps.pcsw.models import Person
#~ from lino.modlib.cv.models import PersonProperty
#~ from lino.modlib.properties.models import Property

from lino_welfare.modlib.pcsw.management.commands.watch_tim import process_line


class WatchTimTest(TestCase):
    pass
    #~ def setUp(self):
        #~ settings.LINO.never_build_site_cache = True
        #~ super(DemoTest,self).setUp()
            
  
def test01(self):
    """
    """
    for ln in CHANGELOG_LINES.splitlines():
        ln = ln.strip()
        if ln:
            process_line(ln)

    georges = Client.objects.get(id=23633)
    self.assertEqual(georges.first_name,"Georges")
    
    