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
This module contains tests for the 
:mod:`watch_tim <lino_welfare.management.commands.watch_tim>`
command.
You can run only these tests by issuing::

  $ python manage.py test lino_welfare.WatchTimTests
  
The module contains a single huge test case because we don't want 
Django to recreate a virgin test database for each of them.
  
"""

from __future__ import unicode_literals


import logging
logger = logging.getLogger(__name__)

#~ from django.utils import unittest
#~ from django.test.client import Client
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import translation

#from lino.igen import models
#from lino.modlib.contacts.models import Contact, Companies
#from lino.modlib.countries.models import Country
#~ from lino.modlib.contacts.models import Companies


from lino import dd
from lino.utils import i2d
#~ from lino.core.dbutils import resolve_model
#Companies = resolve_model('contacts.Companies')
from djangosite.utils.djangotest import TestCase

#~ Person = dd.resolve_model('contacts.Person')
#~ Property = dd.resolve_model('properties.Property')
#~ PersonProperty = dd.resolve_model('properties.PersonProperty')

#~ from lino.apps.pcsw.models import Person
#~ from lino.modlib.cv.models import PersonProperty
#~ from lino.modlib.properties.models import Property

from lino_welfare.management.commands.watch_tim import process_line


POST_GEORGES = """{"method":"POST","alias":"PAR","id":"0000023633","time":"20130220 08:55:30",\
"user":"MELANIE","data":{"IDPAR":"0000023633","FIRME":"Schneider Georges","NAME2":"",\
"RUE":"","CP":"","IDPRT":"S","PAYS":"B","TEL":"","FAX":"","COMPTE1":"","NOTVA":"",\
"COMPTE3":"","IDPGP":"","DEBIT":"","CREDIT":"","ATTRIB":"N","IDMFC":"30","LANGUE":"D",\
"IDBUD":"","PROF":"80","CODE1":"","CODE2":"","CODE3":"",\
"DATCREA":{"__date__":{"year":2013,"month":2,"day":20}},"ALLO":"","NB1":"","NB2":"",\
"IDDEV":"","MEMO":"","COMPTE2":"","RUENUM":"","RUEBTE":"","DEBIT2":"","CREDIT2":"",\
"IMPDATE": {"__date__":{"year":0,"month":0,"day":0}},"ATTRIB2":"","CPTSYSI":"",\
"EMAIL":"","MVIDATE":{"__date__":{"year":0,"month":0,"day":0}},"IDUSR":"","DOMI1":""}}"""

PUT_MAX_MORITZ = """{"method":"PUT","alias":"PAR","id":"0000005088","time":"20130222 12:06:01",
"user":"MELANIE","data":{"IDPAR":"0000005088","FIRME":"Müller Max Moritz","NAME2":"",
"RUE":"Werthplatz 12","CP":"4700","IDPRT":"I","PAYS":"B","TEL":"","FAX":"",
"COMPTE1":"001-1234567-89","NOTVA":"BE-0999.999.999","COMPTE3":"","IDPGP":"",
"DEBIT":"","CREDIT":"","ATTRIB":"N","IDMFC":"","LANGUE":"D","IDBUD":"",
"PROF":"80","CODE1":"RH","CODE2":"","CODE3":"",
"DATCREA":{"__date__":{"year":1991,"month":8,"day":12}},
"ALLO":"Herr","NB1":"","NB2":"","IDDEV":"","MEMO":"","COMPTE2":"",
"RUENUM":"","RUEBTE":"","DEBIT2":"","CREDIT2":"",
"IMPDATE":{"__date__":{"year":1999,"month":5,"day":3}},"ATTRIB2":"",
"CPTSYSI":"","EMAIL":"","MVIDATE":{"__date__":{"year":0,"month":0,"day":0}},
"IDUSR":"ALICIA","DOMI1":""}}
"""

POST_PXS = """{"method":"POST","alias":"PXS","id":"0000023635","time":"20130222 11:07:42",
"user":"MELANIEL","data":{"IDPAR":"0000023635","NAME":"Heinz Hinz",
"GEBDAT":{"__date__":{"year":0,"month":0,"day":0}},"APOTHEKE":"","HILFE":"",
"ANTEIL":"","IDMUT":"","VOLLMACHT":{"__date__":{"year":0,"month":0,"day":0}},
"LAUFZEIT":{"__date__":{"year":0,"month":0,"day":0}},"DRINGEND":"","MONATLICH":"",
"SOZIAL":"","MIETE":"","MAF":"","REFERENZ":"","MEMO":"","SEXE":"","GENERIKA":"",
"IDPRT":"S","CARDNUMBER":"","VALID1":{"__date__":{"year":0,"month":0,"day":0}},
"VALID2":{"__date__":{"year":0,"month":0,"day":0}},"CARDTYPE":0,"NATIONALIT":"",
"BIRTHPLACE":"","NOBLECOND":"","CARDISSUER":""}}
"""

# // 2013-02-25 11:46:31 Exception("Cannot handle conversion from <class 'lino_welfare.modlib.pcsw.models.Household'> to <class 'lino_welfare.modlib.pcsw.models.Client'>",)
PUT_PAR_POTTER = """{"method":"PUT","alias":"PAR","id":"0000004260","time":"20130225 11:44:16",
"user":"WIL011","data":{"IDPAR":"0000004260","FIRME":"Voldemort-Potter Harald",
"NAME2":"","RUE":"Schilsweg 26","CP":"4700","IDPRT":"I","PAYS":"B","TEL":"","FAX":"","COMPTE1":"",
"NOTVA":"BE-0999.999.999","COMPTE3":"","IDPGP":"","DEBIT":"","CREDIT":"","ATTRIB":"N","IDMFC":"",
"LANGUE":"D","IDBUD":"","PROF":"80","CODE1":"ER","CODE2":"","CODE3":"",
"DATCREA":{"__date__":{"year":1985,"month":7,"day":23}},"ALLO":"Eheleute","NB1":"","NB2":"",
"IDDEV":"","MEMO":"","COMPTE2":"","RUENUM":"","RUEBTE":"","DEBIT2":"","CREDIT2":"",
"IMPDATE":{"__date__":{"year":2000,"month":6,"day":26}},"ATTRIB2":"","CPTSYSI":"","EMAIL":"",
"MVIDATE":{"__date__":{"year":0,"month":0,"day":0}},"IDUSR":"ALICIA","DOMI1":""}}
"""

#// 2013-02-25 12:00:37 Exception("Cannot handle conversion from <class 'lino_welfare.modlib.pcsw.models.Person'> to <class 'lino_welfare.modlib.pcsw.models.Household'>",)

PUT_PAR_6283 = """
{"method":"PUT","alias":"PAR","id":"0000006283","time":"20130225 11:52:56","user":"WIL011","data":
{"IDPAR":"0000006283","FIRME":"Willekens-Delanuit Paul","NAME2":"","RUE":"Rotenbergplatz","CP":"4700",
"IDPRT":"I","PAYS":"B","TEL":"","FAX":"","COMPTE1":"","NOTVA":"","COMPTE3":"","IDPGP":"",
"DEBIT":"","CREDIT":"","ATTRIB":"A","IDMFC":"","LANGUE":"D","IDBUD":"","PROF":"80","CODE1":"",
"CODE2":"","CODE3":"","DATCREA":{"__date__":{"year":1998,"month":11,"day":17}},
"ALLO":"Eheleute","NB1":"","NB2":"","IDDEV":"","MEMO":"","COMPTE2":"","RUENUM":"  24","RUEBTE":"",
"DEBIT2":"","CREDIT2":"","IMPDATE":{"__date__":{"year":1999,"month":8,"day":9}},
"ATTRIB2":"","CPTSYSI":"","EMAIL":"",
"MVIDATE":{"__date__":{"year":0,"month":0,"day":0}},"IDUSR":"","DOMI1":""}}
"""


User = dd.resolve_model('users.User')
Partner = dd.resolve_model('contacts.Partner')
Company = dd.resolve_model('contacts.Company')
Person = dd.resolve_model('contacts.Person')
Client = dd.resolve_model('pcsw.Client')
Coaching = dd.resolve_model('pcsw.Coaching')
Household = dd.resolve_model('households.Household')
households_Type = dd.resolve_model("households.Type")
pcsw = dd.resolve_app("pcsw")

from lino_welfare.modlib.isip import models as isip

class WatchTimTests(TestCase):
    
    maxDiff = None
  
    def test00(self):
        
        
        ASD = pcsw.CoachingType(id=isip.COACHINGTYPE_ASD,name="ASD")
        ASD.save()
        
        DSBE = pcsw.CoachingType(id=isip.COACHINGTYPE_DSBE,name="DSBE")
        DSBE.save()
        
        User(username='watch_tim').save()
        User(username='alicia',coaching_type=DSBE).save()
        User(username='roger',coaching_type=ASD).save()
        User(username='edgar').save()
        households_Type(name="Eheleute",pk=1).save()
        settings.SITE.uppercase_last_name = True
        
        #~ def test01(self):
        """
        AttributeError 'NoneType' object has no attribute 'coaching_type'
        """
        self.assertDoesNotExist(Client,id=23633)
        process_line(POST_GEORGES)
        georges = Client.objects.get(id=23633)
        self.assertEqual(georges.first_name,"Georges")
        georges.first_name = "Peter"
        georges.save()
        process_line(POST_GEORGES)
        georges = Client.objects.get(id=23633)
        self.assertEqual(georges.first_name,"Georges")

        #~ def test02(self):
        """
        Company becomes Client
        
        ValidationError([u'A Partner cannot be parent for a Client']) (201302-22 12:42:07)
        A Partner in TIM has both `PAR->NoTva` nonempty and `PARATTR_N` set. 
        It currently exists in Lino as a Company but not as a Client.
        `watch_tim` then must create a Client after creating also the intermediate Person.
        The Company child must be removed.
        """
        Company(name="Müller Max Moritz",id=5088).save()
        global PUT_MAX_MORITZ
        process_line(PUT_MAX_MORITZ)
        self.assertDoesNotExist(Company,id=5088)
        #~ company = Company.objects.get(id=5088) # has not been deleted
        person = Person.objects.get(id=5088) # has been created
        client = Client.objects.get(id=5088) # has been created
        coaching = Coaching.objects.get(client=client) # one coaching has been created
        self.assertEqual(person.first_name,"Max Moritz")
        self.assertEqual(client.first_name,"Max Moritz")
        self.assertEqual(coaching.user.username,'alicia')
        self.assertEqual(coaching.primary,True)
        self.assertEqual(coaching.start_date,i2d(19910812))
        
        """
        Client becomes Company
        """
        #~ PUT_MAX_MORITZ = PUT_MAX_MORITZ.replace('"IDUSR":"ALICIA"','"IDUSR":""')
        PUT_MAX_MORITZ = PUT_MAX_MORITZ.replace('"ATTRIB":"N"','"ATTRIB":""')
        process_line(PUT_MAX_MORITZ)
        #~ company = Company.objects.get(id=5088) 
        self.assertDoesNotExist(Client,id=5088) # has been deleted
        self.assertDoesNotExist(Coaching,client_id=5088)
        

        #~ def test03(self):
        """
        Test whether watch_tim raises Exception 
        'Cannot create Client ... from PXS' when necessary.
        """
        self.assertDoesNotExist(Client,id=23635)
        try:
            process_line(POST_PXS)
            self.fail("Expected an exception")
        except Exception as e:
            self.assertEqual(str(e),"Cannot create Client 0000023635 from PXS")
        self.assertDoesNotExist(Client,id=23635)

        #~ def test04(self):
        """
        Household becomes Client
        """
        Household(name="Voldemort-Potter Harald",id=4260).save()
        process_line(PUT_PAR_POTTER)
        client = Client.objects.get(id=4260) # has been created
        self.assertDoesNotExist(Household,id=4260)
        coaching = Coaching.objects.get(client=client) # one coaching has been created
        self.assertEqual(client.first_name,"Harald")
        self.assertEqual(coaching.primary,True)
        self.assertEqual(coaching.user.username,'alicia')
        self.assertEqual(coaching.start_date,i2d(19850723))
        s = changes_to_rst(client.partner_ptr)
        #~ print s
        self.assertEqual(s,"""\
=========== ============= ============================= ============================================================================= ============= ===========
 User        Change Type   Object                        Changes                                                                       Object type   object id
----------- ------------- ----------------------------- ----------------------------------------------------------------------------- ------------- -----------
 watch_tim   Create        alicia / Voldemort-Potter H   Coaching(id=1,user=2,client=4260,start_date=1985-07-23,type=2,primary=True)   Coaching      1
 watch_tim   Add child     Harald VOLDEMORT-POTTER       pcsw.Client                                                                   Person        4260
 watch_tim   Add child     Voldemort-Potter Harald       contacts.Person                                                               Partner       4260
=========== ============= ============================= ============================================================================= ============= ===========
""")

        #~ def test05(self):
        """
        Person becomes Household 
        """
        Person(id=6283,first_name="Paul",last_name="Willekens-Delanuit").save()
        process_line(PUT_PAR_6283)
        household = Household.objects.get(id=6283) # has been created
        self.assertDoesNotExist(Person,id=6283)
          
        #~ def test06(self):
        """
        ValidationError {'first_name': [u'This field cannot be blank.']}
        """
        ln = """{"method":"PUT","alias":"PAR","id":"0000001334","time":"20121029 09:00:00",
        "user":"","data":{"IDPAR":"0000001334","FIRME":"Belgacom",
        "NAME2":"","RUE":"","CP":"1030","IDPRT":"V","PAYS":"B","TEL":"0800-44500",
        "FAX":"0800-11333","COMPTE1":"","NOTVA":"","COMPTE3":"","IDPGP":"",
        "DEBIT":"  2242.31","CREDIT":"","ATTRIB":"","IDMFC":"60","LANGUE":"F",
        "IDBUD":"","PROF":"30","CODE1":"","CODE2":"","CODE3":"",
        "DATCREA":{"__date__":{"year":1992,"month":10,"day":6}},"ALLO":"","NB1":"",
        "NB2":"","IDDEV":"","MEMO":"Foo bar","COMPTE2":"","RUENUM":"","RUEBTE":"",
        "DEBIT2":"   2242.31","CREDIT2":"",
        "IMPDATE":{"__date__":{"year":2012,"month":10,"day":24}},
        "ATTRIB2":"","CPTSYSI":"","EMAIL":"info@example.com",
        "MVIDATE":{"__date__":{"year":2012,"month":9,"day":9}},"IDUSR":"","DOMI1":""}}
        """
        self.assertDoesNotExist(Partner,id=1334)
        translation.deactivate_all()
        process_line(ln)
        obj = Partner.objects.get(id=1334) 
        self.assertDoesNotExist(Company,id=1334)
        self.assertDoesNotExist(Person,id=1334)
            #~ self.fail("Expected a ValidationError")
        #~ except ValidationError as e:
            #~ self.assertEqual(str(e),"{'first_name': [u'This field cannot be blank.']}")
        #~ self.assertDoesNotExist(Partner,id=1334)
        ln = ln.replace('"NOTVA":""','"NOTVA":"BE-0999.999.999"')
        process_line(ln)
        company = Company.objects.get(id=1334) 

        #~ def test07(self):
        """
        2013-02-28 10:05:41 ValueError('Cannot assign "u\'\'": "City.country" must be a "Country" instance.',)
        """
        ln = """{"method":"PUT","alias":"PAR","id":"0000023649","time":"20130228 10:05:41","user":"MELANIEL",
        "data":{"IDPAR":"0000023649","FIRME":"Reinders Denis","NAME2":"","RUE":"Sch<94>nefelderweg",
        "CP":"4700","IDPRT":"S","PAYS":"","TEL":"","FAX":"","COMPTE1":"","NOTVA":"","COMPTE3":"",
        "IDPGP":"","DEBIT":"","CREDIT":"","ATTRIB":"N","IDMFC":"30","LANGUE":"D","IDBUD":"",
        "PROF":"80","CODE1":"","CODE2":"","CODE3":"",
        "DATCREA":{"__date__":{"year":2013,"month":2,"day":28}},
        "ALLO":"Herr","NB1":"","NB2":"791228 123-35","IDDEV":"","MEMO":"","COMPTE2":"",
        "RUENUM":" 123","RUEBTE":"a","DEBIT2":"","CREDIT2":"",
        "IMPDATE":{"__date__":{"year":0,"month":0,"day":0}},"ATTRIB2":"","CPTSYSI":"","EMAIL":"",
        "MVIDATE":{"__date__":{"year":0,"month":0,"day":0}},"IDUSR":"","DOMI1":""}}
        """
        self.assertDoesNotExist(Client,id=23649)
        process_line(ln)
        obj = Client.objects.get(id=23649)
        self.assertEqual(obj.first_name,"Denis")
        s = changes_to_rst(obj.partner_ptr)
        #~ cannot easily test due to `modified` timestamp
        #~ print s
        #~ self.assertEqual(s,"""\
#~ =========== ============= ======================== ========================================================================================================================================================================================================================================================================================================================================================= ============= ===========
 #~ User        Change Type   Object                   Changes                                                                                                                                                                                                                                                                                                                                                   Object type   object id
#~ ----------- ------------- ------------------------ --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- ------------- -----------
 #~ watch_tim   Create        REINDERS Denis (23649)   Client(id=23649,created=2013-02-28T00:00:00,modified=2013-05-08T10:57:34.755851,name='Reinders Denis',street='Sch<94>nefelderweg',street_no='123',street_box='a',language='de',activity=80,partner_ptr=23649,first_name='Denis',last_name='Reinders',person_ptr=23649,is_cpas=True,national_id='791228 123-35',client_state=<ClientStates.newcomer:10>)   Klient        23649
#~ =========== ============= ======================== ========================================================================================================================================================================================================================================================================================================================================================= ============= ===========
#~ """)
        
        """
        20130508 Company becomes Client
        201305-03 07:49:11 INFO watch_tim : PAR:0000000005 (Company #5 (u'Air Liquide Belgium')) : Company becomes Client
        """
        
        Company(name="Air Liquide Belgium",id=5).save()
        ln = """{"method":"PUT","alias":"PAR","id":"0000000005","time":"20130503 07:36:15",
        "user":"","data":{"IDPAR":"0000000005","FIRME":"Air Liquide Belgium",
        "NAME2":"","RUE":"Quai des Vennes","CP":"4020","IDPRT":"V","PAYS":"B",
        "TEL":"04/349.89.89","FAX":"04/341.20.70","COMPTE1":"GKCCBEBB:BE57551373330235",
        "NOTVA":"BE-0441.857.467","COMPTE3":"","IDPGP":"","DEBIT":"","CREDIT":"",
        "ATTRIB":"A","IDMFC":"30","LANGUE":"F","IDBUD":"","PROF":"19",
        "CODE1":"","CODE2":"","CODE3":"",
        "DATCREA":{"__date__":{"year":1985,"month":3,"day":12}},"ALLO":"S.A.",
        "NB1":"","NB2":"","IDDEV":"","MEMO":"\\n",
        "COMPTE2":"BBRUBEBB:BE12310110444892","RUENUM":"   8","RUEBTE":"","DEBIT2":"",
        "CREDIT2":"","IMPDATE":{"__date__": {"year":2009,"month":3,"day":10}},
        "ATTRIB2":"","CPTSYSI":"","EMAIL":"",
        "MVIDATE":{"__date__":{"year":0,"month":0,"day":0}},"IDUSR":"EDGAR","DOMI1":""}}
        """
        process_line(ln)
        self.assertDoesNotExist(Client,id=5)
        obj = Company.objects.get(id=5)
        self.assertEqual(obj.name,"Air Liquide Belgium")
        s = changes_to_rst(obj.partner_ptr)
        #~ print s
        self.assertEqual(s,"""\
+-----------+-------------+---------------------+------------------------------------------------------+-------------+-----------+
| User      | Change Type | Object              | Changes                                              | Object type | object id |
+===========+=============+=====================+======================================================+=============+===========+
| watch_tim | Update      | Air Liquide Belgium | - activity_id : None --> 19                          | Company     | 5         |
|           |             |                     | - city_id : None --> 3                               |             |           |
|           |             |                     | - bank_account1 : '' --> 'GKCCBEBB:BE57551373330235' |             |           |
|           |             |                     | - fax : '' --> '04/341.20.70'                        |             |           |
|           |             |                     | - street_no : '' --> '8'                             |             |           |
|           |             |                     | - vat_id : '' --> 'BE-0441.857.467'                  |             |           |
|           |             |                     | - prefix : '' --> 'S.A.'                             |             |           |
|           |             |                     | - street : '' --> 'Quai des Vennes'                  |             |           |
|           |             |                     | - remarks : '' --> '\\n'                              |             |           |
|           |             |                     | - language : 'de' --> 'fr'                           |             |           |
|           |             |                     | - phone : '' --> '04/349.89.89'                      |             |           |
|           |             |                     | - country_id : None --> 'B'                          |             |           |
|           |             |                     | - bank_account2 : '' --> 'BBRUBEBB:BE12310110444892' |             |           |
|           |             |                     | - zip_code : '' --> '4020'                           |             |           |
+-----------+-------------+---------------------+------------------------------------------------------+-------------+-----------+
""")
        


        """
        Person becomes Company
        """
        Person(id=9932,first_name="CPAS",last_name="Andenne").save()
        ln = """{"method":"PUT","alias":"PAR","id":"0000009932","time":"20130503 07:38:16","user":"","data":{"IDPAR":"0000009932","FIRME":"Andenne, CPAS","NAME2":"","RUE":"Rue de l'Hopital","CP":"5300","IDPRT":"V","PAYS":"B","TEL":"","FAX":"","COMPTE1":"","NOTVA":"BE-0999.999.999","COMPTE3":"","IDPGP":"","DEBIT":"","CREDIT":"","ATTRIB":"","IDMFC":"","LANGUE":"F","IDBUD":"","PROF":"65","CODE1":"","CODE2":"","CODE3":"","DATCREA":{"__date__":{"year":1988,"month":12,"day":9}},"ALLO":"","NB1":"","NB2":"        0","IDDEV":"","MEMO":"","COMPTE2":"","RUENUM":"  22","RUEBTE":"","DEBIT2":"","CREDIT2":"","IMPDATE":{"__date__":{"year":0,"month":0,"day":0}},"ATTRIB2":"","CPTSYSI":"","EMAIL":"","MVIDATE":{"__date__":{"year":0,"month":0,"day":0}},"IDUSR":"","DOMI1":""}}"""
        process_line(ln)
        self.assertDoesNotExist(Client,id=9932)
        self.assertDoesNotExist(Person,id=9932)
        obj = Company.objects.get(id=9932)
        self.assertEqual(obj.name,"Andenne, CPAS")
        
        s = changes_to_rst(obj.partner_ptr)
        #~ print s
        self.assertEqual(s,"""\
=========== ============== =============== ================== ============= ===========
 User        Change Type    Object          Changes            Object type   object id
----------- -------------- --------------- ------------------ ------------- -----------
 watch_tim   Add child      Andenne, CPAS   contacts.Company   Partner       9932
 watch_tim   Remove child                   contacts.Person    Person        9932
=========== ============== =============== ================== ============= ===========
""")

        """
        A PAR without NoTVA becomes a Person, but if no first_name can 
        be detected, then it is just a simple partner
        """
        ln = """{"method":"PUT","alias":"PAR","id":"0000001267","time":"20130517 12:34:15",
        "user":"","data":{"IDPAR":"0000001267","FIRME":"Velopa","NAME2":"",
        "RUE":"Leuvenselaan","CP":"3300","IDPRT":"I","PAYS":"B","TEL":"",
        "FAX":"","COMPTE1":"","NOTVA":"","COMPTE3":"","IDPGP":"",
        "DEBIT":"","CREDIT":"","ATTRIB":"","IDMFC":"30","LANGUE":"F","IDBUD":"",
        "PROF":"15","CODE1":"","CODE2":"","CODE3":"",
        "DATCREA":{"__date__":{"year":1992,"month":1,"day":2}},"ALLO":"S.A.",
        "NB1":"","NB2":"","IDDEV":"","MEMO":"","COMPTE2":"","RUENUM":" 172",
        "RUEBTE":"","DEBIT2":"","CREDIT2":"","IMPDATE":{"__date__":{"year":1996,"month":8,"day":30}},
        "ATTRIB2":"","CPTSYSI":"","EMAIL":"",
        "MVIDATE":{"__date__":{"year":0,"month":0,"day":0}},"IDUSR":"",
        "DOMI1":""}}"""
        self.assertDoesNotExist(Partner,id=1267)
        process_line(ln)
        obj = Partner.objects.get(id=1267)
        self.assertEqual(obj.name,"Velopa")
        #~ try:
            #~ process_line(ln)
            #~ self.fail("""Expected ValidationError: {'first_name': [u'Dieses Feld darf nicht leer sein.']}""")
            #~ # NOTVA ist leer, also will watch_tim eine Person draus machen, 
            #~ # aber dazu bräuchte er auch einen Vornamen
        #~ except ValidationError as e:
            #~ pass
        #~ self.assertDoesNotExist(Partner,id=1267)
        
        ln = """{"method":"PUT","alias":"PAR","id":"0000000665","time":"20130517 12:33:58","user":"",
        "data":{"IDPAR":"0000000665","FIRME":"Petra","NAME2":"","RUE":"Beskensstraat 34","CP":"3520",
        "IDPRT":"I","PAYS":"B","TEL":"011/815911","FAX":"","COMPTE1":"","NOTVA":"BE-0426.896.703",
        "COMPTE3":"","IDPGP":"","DEBIT":"","CREDIT":"","ATTRIB":"","IDMFC":"30",
        "LANGUE":"3",
        "IDBUD":"","PROF":"12","CODE1":"","CODE2":"","CODE3":"",
        "DATCREA":{"__date__":{"year":1986,"month":8,"day":14}},"ALLO":"sprl","NB1":"","NB2":"",
        "IDDEV":"","MEMO":"","COMPTE2":"","RUENUM":"","RUEBTE":"","DEBIT2":"","CREDIT2":"",
        "IMPDATE":{"__date__":{"year":0,"month":0,"day":0}},"ATTRIB2":"","CPTSYSI":"",
        "EMAIL":"","MVIDATE":{"__date__":{"year":0,"month":0,"day":0}},"IDUSR":"","DOMI1":""}}"""
        process_line(ln)
        obj = Company.objects.get(id=665)
        self.assertEqual(obj.name,"Petra")
        
        #~ INFO PAR:0000007826 (Client #7826 (u'MUSTERMANN Peter (7826)')) : Client becomes Person
        #~ WARNING Exception 'ValidationError([u'A Person cannot be parent for a Person'])' while processing changelog line:
        Client(id=7826,first_name="Peter",last_name="Mustermann").save()
        ln = """{"method":"PUT","alias":"PAR","id":"0000007826","time":"20130517 12:35:51","user":"",
        "data":{"IDPAR":"0000007826","FIRME":"Mustermann Peter","NAME2":"","RUE":"Burgundstraße","CP":
        "4700","IDPRT":"S","PAYS":"B","TEL":"","FAX":"","COMPTE1":"","NOTVA":"",
        "COMPTE3":"","IDPGP":"","DEBIT":"","CREDIT":"","ATTRIB":"A",
        "IDMFC":"30","LANGUE":"D","IDBUD":"","PROF":"82","CODE1":"",
        "CODE2":"","CODE3":"","DATCREA":{"__date__":{"year":2006,"month":1,"day":5}},
        "ALLO":"Herrn","NB1":"","NB2":"","IDDEV":"","MEMO":"","COMPTE2":"",
        "RUENUM":"   9","RUEBTE":"","DEBIT2":"","CREDIT2":"",
        "IMPDATE":{"__date__":{"year":2009,"month":9,"day":22}},
        "ATTRIB2":"","CPTSYSI":"","EMAIL":"","MVIDATE":{"__date__":{"year":0,"month":0,"day":0}},
        "IDUSR":"ALICIA","DOMI1":""}}"""
        process_line(ln)
        self.assertDoesNotExist(Client,id=7826)
        
        """
        20130602 : datum_bis einer primären Begleitung eines Ehemaligen darf
        nicht leer sein. Wenn es das ist, soll watch_tim es auf 01.01.1990
        setzen. 
        """
        with translation.override('de'):
            self.assertDoesNotExist(Coaching,client_id=7826)
            ln = ln.replace('"NB2":""','"NB2":"940702 234-24"')
            process_line(ln)
            obj = Client.objects.get(id=7826)
            self.assertEqual(obj.name,"Mustermann Peter")
            s = coachings_to_rst(obj)
            #~ print s
            self.assertEqual(s,"""\
====================== ===== =========== ======== ======== ================== =======
 Begleitet seit         bis   Begleiter   Primär   Dienst   Beendigungsgrund   ID
---------------------- ----- ----------- -------- -------- ------------------ -------
 05.01.06                     alicia      Ja       DSBE                        2
 **Total (1 Zeilen)**                     **1**                                **0**
====================== ===== =========== ======== ======== ================== =======
""")
            ln = ln.replace('"IDPRT":"S"','"IDPRT":"I"')
            process_line(ln)
            s = coachings_to_rst(obj)
            #~ print s
            self.assertEqual(s,"""\
====================== ========== =========== ======== ======== ================== =======
 Begleitet seit         bis        Begleiter   Primär   Dienst   Beendigungsgrund   ID
---------------------- ---------- ----------- -------- -------- ------------------ -------
 05.01.06               05.01.06   alicia      Ja       DSBE                        2
 **Total (1 Zeilen)**                          **1**                                **0**
====================== ========== =========== ======== ======== ================== =======
""")


        """
        A non-client partner with empty PAR->NoTva will become a Person, not a Company.
        If the partner is in fact a company whose NoTva has just been forgotten, 
        then watch_tim will raise a ValidationError:
        """
        ln = """{"method":"POST","alias":"PAR","id":"0000087683","time":"20130610 11:26:30",
        "user":"ROGER","data":{"IDPAR":"0000087683","FIRME":"Bellavilla","NAME2":"","RUE":"",
        "CP":"","IDPRT":"V","PAYS":"","TEL":"","FAX":"","COMPTE1":"","NOTVA":"","COMPTE3":"",
        "IDPGP":"","DEBIT":"","CREDIT":"","ATTRIB":"","IDMFC":"30","LANGUE":"D","IDBUD":"",
        "PROF":"00","CODE1":"","CODE2":"","CODE3":"",
        "DATCREA":{"__date__":{"year":2013,"month":6,"day":10}},"ALLO":"","NB1":"",
        "NB2":"","IDDEV":"","MEMO":"","COMPTE2":"","RUENUM":"","RUEBTE":"","DEBIT2":"",
        "CREDIT2":"","IMPDATE":{"__date__":{"year":0,"month":0,"day":0}},"ATTRIB2":"",
        "CPTSYSI":"","EMAIL":"","MVIDATE":{"__date__":{"year":0,"month":0,"day":0}},
        "IDUSR":"","DOMI1":""}}"""
        self.assertDoesNotExist(Partner,id=87683)
        process_line(ln)
        #~ try:
            #~ self.fail("Expected ValidationError {'first_name': [u'Dieses Feld darf nicht leer sein.']}")
        #~ except ValidationError as e:
        obj = Partner.objects.get(id=87683)
        for m in Company,Person, Client, Household:
            self.assertDoesNotExist(m,id=87683)
            
        ln = """{"method":"PUT","alias":"PAR","id":"0000004124","time":"20130517 12:34:37",
        "user":"","data":{"IDPAR":"0000004124","FIRME":"Theves-Carlsberg","NAME2":"",
        "RUE":"Werthplatz 22","CP":"4700","IDPRT":"I","PAYS":"B","TEL":"","FAX":"",
        "COMPTE1":"","NOTVA":"BE-0999.999.999","COMPTE3":"","IDPGP":"","DEBIT":"",
        "CREDIT":"","ATTRIB":"W","IDMFC":"","LANGUE":"D","IDBUD":"","PROF":"80",
        "CODE1":"EP","CODE2":"","CODE3":"","DATCREA":{"__date__":{"year":1985,
        "month":4,"day":18}},"ALLO":"Eheleute","NB1":"THCA600115","NB2":"",
        "IDDEV":"","MEMO":"","COMPTE2":"","RUENUM":"","RUEBTE":"",
        "DEBIT2":"","CREDIT2":"","IMPDATE":{"__date__":{"year":0,
        "month":0,"day":0}},"ATTRIB2":"","CPTSYSI":"","EMAIL":"",
        "MVIDATE":{"__date__":{"year":0,"month":0,"day":0}},
        "IDUSR":"ROGER","DOMI1":""}}"""
        self.assertDoesNotExist(Partner,id=4124)
        process_line(ln)
        obj = Company.objects.get(id=4124)
        ln = ln.replace("BE-0999.999.999","")
        process_line(ln)
        self.assertDoesNotExist(Company,id=4124)
        obj = Household.objects.get(id=4124)
        
        
        ln = """{"method":"PUT","alias":"PAR","id":"0000001315",
        "time":"20130811 10:33:20","user":"PAC","data":{"IDPAR":"0000001315",
        "FIRME":"C2D System House","NAME2":"",
        "RUE":"Rue des Champs","CP":"4630","IDPRT":"V","PAYS":"B","TEL":"04/567.89.10",
        "FAX":"04/365.31.10","COMPTE1":"JVBABE22:BE39645678910619",
        "NOTVA":"BE-0123.456.789","COMPTE3":"","IDPGP":"",
        "DEBIT":"","CREDIT":"","ATTRIB":"","IDMFC":"30","LANGUE":"F",
        "IDBUD":"","PROF":"22","CODE1":"","CODE2":"","CODE3":"",
        "DATCREA":{"__date__":{"year":1992,"month":7,"day":24}},"ALLO":"S.A.",
        "NB1":"EUPO","NB2":"","IDDEV":"","MEMO":"","COMPTE2":"",
        "RUENUM":"   8","RUEBTE":"","DEBIT2":"","CREDIT2":"",
        "IMPDATE":{"__date__":{"year":2012,"month":10,"day":25}},
        "ATTRIB2":"","CPTSYSI":"","EMAIL":"info@c2d.be",
        "MVIDATE":{"__date__":{"year":2012,"month":1,"day":25}},
        "IDUSR":"","DOMI1":""}} """

        self.assertDoesNotExist(Partner,id=1315)
        process_line(ln)
        obj = Partner.objects.get(id=1315)
        obj = Company.objects.get(id=1315)
        for m in Person, Client, Household:
            self.assertDoesNotExist(m,id=1315)



def changes_to_rst(master):
    A = settings.SITE.modules.changes.ChangesByMaster
    return A.request(master).to_rst(column_names = 'user type object diff:30 object_type object_id')

def coachings_to_rst(master):
    A = settings.SITE.modules.pcsw.CoachingsByClient
    return A.request(master).to_rst()
