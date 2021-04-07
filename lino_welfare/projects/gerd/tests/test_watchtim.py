# -*- coding: UTF-8 -*-
# Copyright 2013-2017 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

"""This module contains tests for the :mod:`watch_tim
<lino_welfare.management.commands.watch_tim>` command.

You can run only these tests by issuing::

  $ cd lino_welfare/projects/eupen
  $ python manage.py test tests.test_watchtim
  
The module contains a single huge test case because we don't want
Django to recreate a virgin test database for each of them.

"""

from __future__ import unicode_literals

from builtins import str
import logging
logger = logging.getLogger(__name__)

from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import translation

from lino.api import dd, rt
from lino.utils import i2d
from lino.utils.djangotest import TestCase

from lino_welfare.modlib.welfare.management.commands.watch_tim import process_line


POST_GEORGES = """{"method":"POST","alias":"PAR","id":"0000023633","time":"20130220 08:55:30",\
"user":"MELANIE","data":{"IDPAR":"0000023633","FIRME":"Schneider Georges","NAME2":"",\
"RUE":"","CP":"","IDPRT":"S","PAYS":"B","TEL":"","FAX":"","COMPTE1":"","NOTVA":"",\
"COMPTE3":"","IDPGP":"","DC.debit":"","DC.credit":"","ATTRIB":"N","IDMFC":"30","LANGUE":"D",\
"IDBUD":"","PROF":"80","CODE1":"","CODE2":"","CODE3":"",\
"DATCREA":{"__date__":{"year":2013,"month":2,"day":20}},"ALLO":"","NB1":"","NB2":"",\
"IDDEV":"","MEMO":"","COMPTE2":"","RUENUM":"","RUEBTE":"","DEBIT2":"","CREDIT2":"",\
"IMPDATE": {"__date__":{"year":0,"month":0,"day":0}},"ATTRIB2":"","CPTSYSI":"",\
"EMAIL":"","MVIDATE":{"__date__":{"year":0,"month":0,"day":0}},"IDUSR":"","DOMI1":""}}"""

PUT_MAX_MORITZ = """{"method":"PUT","alias":"PAR","id":"0000005088","time":"20130222 12:06:01",
"user":"MELANIE","data":{"IDPAR":"0000005088","FIRME":"Müller Max Moritz","NAME2":"",
"RUE":"Werthplatz 12","CP":"4700","IDPRT":"I","PAYS":"B","TEL":"","FAX":"",
"COMPTE1":"001-1234567-89","NOTVA":"BE-0999.999.999","COMPTE3":"","IDPGP":"",
"DC.debit":"","DC.credit":"","ATTRIB":"N","IDMFC":"","LANGUE":"D","IDBUD":"",
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
"NOTVA":"BE-0999.999.999","COMPTE3":"","IDPGP":"","DC.debit":"","DC.credit":"","ATTRIB":"N","IDMFC":"",
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
"DC.debit":"","DC.credit":"","ATTRIB":"A","IDMFC":"","LANGUE":"D","IDBUD":"","PROF":"80","CODE1":"",
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
Coaching = dd.resolve_model('coachings.Coaching')
Household = dd.resolve_model('households.Household')
households_Type = dd.resolve_model("households.Type")
pcsw = dd.resolve_app("pcsw")
isip = dd.resolve_app("isip")

from lino_welfare.modlib.isip import models as isip


class TestCase(TestCase):

    maxDiff = None

    def test00(self):

        ASD = rt.models.coachings.CoachingType(
            id=isip.COACHINGTYPE_ASD, name="ASD")
        ASD.save()

        DSBE = rt.models.coachings.CoachingType(
            id=isip.COACHINGTYPE_DSBE, name="DSBE")
        DSBE.save()

        User(username='watch_tim').save()
        User(username='alicia', coaching_type=DSBE).save()
        User(username='roger', coaching_type=ASD).save()
        User(username='edgar').save()
        households_Type(name="Eheleute", pk=1).save()
        settings.SITE.uppercase_last_name = True

        #~ def test01(self):
        """
        AttributeError 'NoneType' object has no attribute 'coaching_type'
        """
        self.assertDoesNotExist(Client, id=23633)
        process_line(POST_GEORGES)
        georges = Client.objects.get(id=23633)
        self.assertEqual(georges.first_name, "Georges")
        georges.first_name = "Peter"
        georges.save()
        process_line(POST_GEORGES)
        georges = Client.objects.get(id=23633)
        self.assertEqual(georges.first_name, "Georges")

        ar = rt.models.changes.ChangesByMaster.request(georges)
        self.assertEqual(ar.get_total_count(), 0)

        # Company becomes Client
        
        # ValidationError([u'A Partner cannot be parent for a Client']) (201302-22 12:42:07)

        # A Partner in TIM has both `PAR->NoTva` nonempty and
        # `PARATTR_N` set.  It currently exists in Lino as a Company but
        # not as a Client.  `watch_tim` then must create a Client after
        # creating also the intermediate Person.  The Company child must
        # be removed.

        obj = Company(name="Müller Max Moritz", id=5088)
        obj.save()

        ar = rt.models.changes.ChangesByMaster.request(obj)
        self.assertEqual(ar.get_total_count(), 0)
        
        global PUT_MAX_MORITZ
        process_line(PUT_MAX_MORITZ)
        self.assertDoesNotExist(Company, id=5088)
        # ~ company = Company.objects.get(id=5088) # has not been deleted
        person = Person.objects.get(id=5088)  # has been created
        client = Client.objects.get(id=5088)  # has been created
        # one coaching has been created
        coaching = Coaching.objects.get(client=client)
        self.assertEqual(person.first_name, "Max Moritz")
        self.assertEqual(client.first_name, "Max Moritz")
        self.assertEqual(coaching.user.username, 'alicia')
        self.assertEqual(coaching.primary, True)
        self.assertEqual(coaching.start_date, i2d(19910812))

        """
        Client becomes Company
        """
        #~ PUT_MAX_MORITZ = PUT_MAX_MORITZ.replace('"IDUSR":"ALICIA"','"IDUSR":""')
        PUT_MAX_MORITZ = PUT_MAX_MORITZ.replace('"ATTRIB":"N"', '"ATTRIB":""')
        process_line(PUT_MAX_MORITZ)
        #~ company = Company.objects.get(id=5088)
        self.assertDoesNotExist(Client, id=5088)  # has been deleted
        self.assertDoesNotExist(Coaching, client_id=5088)

        #~ def test03(self):
        """
        Test whether watch_tim raises Exception 
        'Cannot create Client ... from PXS' when necessary.
        """
        self.assertDoesNotExist(Client, id=23635)
        try:
            process_line(POST_PXS)
            self.fail("Expected an exception")
        except Exception as e:
            self.assertEqual(
                str(e), "Cannot create Client 0000023635 from PXS")
        self.assertDoesNotExist(Client, id=23635)

        #~ def test04(self):
        """
        Household becomes Client
        """
        Household(name="Voldemort-Potter Harald", id=4260).save()
        process_line(PUT_PAR_POTTER)
        client = Client.objects.get(id=4260)  # has been created
        self.assertDoesNotExist(Household, id=4260)
        # one coaching has been created
        coaching = Coaching.objects.get(client=client)
        self.assertEqual(client.first_name, "Harald")
        self.assertEqual(coaching.primary, True)
        self.assertEqual(coaching.user.username, 'alicia')
        self.assertEqual(coaching.start_date, i2d(19850723))
        with translation.override('en'):
            s = changes_to_rst(client.partner_ptr)
        # print s
        self.assertEqual(s, """\
=========== ============= ==================================== ============================================================================= ============= ===========
 User        Change Type   Object                               Changes                                                                       Object type   object id
----------- ------------- ------------------------------------ ----------------------------------------------------------------------------- ------------- -----------
 watch_tim   Create        *alicia / Voldemort-Potter H*        Coaching(id=2,start_date=1985-07-23,user=2,client=4260,type=2,primary=True)   Coaching      2
 watch_tim   Add child     *Eheleute Harald VOLDEMORT-POTTER*   pcsw.Client                                                                   Person        4260
 watch_tim   Add child     *Voldemort-Potter Harald*            contacts.Person                                                               Partner       4260
=========== ============= ==================================== ============================================================================= ============= ===========

""")

        #~ def test05(self):
        """
        Person becomes Household 
        """
        Person(id=6283, first_name="Paul",
               last_name="Willekens-Delanuit").save()
        process_line(PUT_PAR_6283)
        household = Household.objects.get(id=6283)  # has been created
        self.assertDoesNotExist(Person, id=6283)

        #~ def test06(self):
        """
        ValidationError {'first_name': [u'This field cannot be blank.']}
        """
        ln = """{"method":"PUT","alias":"PAR","id":"0000001334","time":"20121029 09:00:00",
        "user":"","data":{"IDPAR":"0000001334","FIRME":"Belgacom",
        "NAME2":"","RUE":"","CP":"1030","IDPRT":"V","PAYS":"B","TEL":"0800-44500",
        "FAX":"0800-11333","COMPTE1":"","NOTVA":"","COMPTE3":"","IDPGP":"",
        "DC.debit":"  2242.31","DC.credit":"","ATTRIB":"","IDMFC":"60","LANGUE":"F",
        "IDBUD":"","PROF":"30","CODE1":"","CODE2":"","CODE3":"",
        "DATCREA":{"__date__":{"year":1992,"month":10,"day":6}},"ALLO":"","NB1":"",
        "NB2":"","IDDEV":"","MEMO":"Foo bar","COMPTE2":"","RUENUM":"","RUEBTE":"",
        "DEBIT2":"   2242.31","CREDIT2":"",
        "IMPDATE":{"__date__":{"year":2012,"month":10,"day":24}},
        "ATTRIB2":"","CPTSYSI":"","EMAIL":"info@example.com",
        "MVIDATE":{"__date__":{"year":2012,"month":9,"day":9}},"IDUSR":"","DOMI1":""}}
        """
        self.assertDoesNotExist(Partner, id=1334)
        translation.deactivate_all()
        process_line(ln)
        obj = Partner.objects.get(id=1334)
        self.assertDoesNotExist(Company, id=1334)
        self.assertDoesNotExist(Person, id=1334)
            #~ self.fail("Expected a ValidationError")
        #~ except ValidationError as e:
            #~ self.assertEqual(str(e),"{'first_name': [u'This field cannot be blank.']}")
        #~ self.assertDoesNotExist(Partner,id=1334)
        ln = ln.replace('"NOTVA":""', '"NOTVA":"BE-0999.999.999"')
        process_line(ln)
        company = Company.objects.get(id=1334)

        #~ def test07(self):
        """
        2013-02-28 10:05:41 ValueError('Cannot assign "u\'\'": "Place.country" must be a "Country" instance.',)
        """
        ln = """{"method":"PUT","alias":"PAR","id":"0000023649","time":"20130228 10:05:41","user":"MELANIEL",
        "data":{"IDPAR":"0000023649","FIRME":"Reinders Denis","NAME2":"","RUE":"Sch<94>nefelderweg",
        "CP":"4700","IDPRT":"S","PAYS":"","TEL":"","FAX":"","COMPTE1":"","NOTVA":"","COMPTE3":"",
        "IDPGP":"","DC.debit":"","DC.credit":"","ATTRIB":"N","IDMFC":"30","LANGUE":"D","IDBUD":"",
        "PROF":"80","CODE1":"","CODE2":"","CODE3":"",
        "DATCREA":{"__date__":{"year":2013,"month":2,"day":28}},
        "ALLO":"Herr","NB1":"","NB2":"791228 123-35","IDDEV":"","MEMO":"","COMPTE2":"",
        "RUENUM":" 123","RUEBTE":"a","DEBIT2":"","CREDIT2":"",
        "IMPDATE":{"__date__":{"year":0,"month":0,"day":0}},"ATTRIB2":"","CPTSYSI":"","EMAIL":"",
        "MVIDATE":{"__date__":{"year":0,"month":0,"day":0}},"IDUSR":"","DOMI1":""}}
        """
        self.assertDoesNotExist(Client, id=23649)
        process_line(ln)
        obj = Client.objects.get(id=23649)
        self.assertEqual(obj.first_name, "Denis")
        with translation.override('en'):
            s = changes_to_rst(obj.partner_ptr)
        #~ skipped because cannot easily test due to `modified` timestamp
        #~ print s
        #~ self.assertEqual(s,"""\
#~ =========== ============= ======================== ====================
 #~ User        Change Type   Object                   Changes                                                                                                                                                                                                                                                                                                                                                   Object type   object id
#~ ----------- ------------- ------------------------ --------------------
 #~ watch_tim   Create        REINDERS Denis (23649)   Client(id=23649,created=2013-02-28T00:00:00,modified=2013-05-08T10:57:34.755851,name='Reinders Denis',street='Sch<94>nefelderweg',street_no='123',street_box='a',language='de',activity=80,partner_ptr=23649,first_name='Denis',last_name='Reinders',person_ptr=23649,is_cpas=True,national_id='791228 123-35',client_state=<ClientStates.newcomer:10>)   Klient        23649
#~ =========== ============= ======================== ====================
#~ """)

        """
        20130508 Company becomes Client
        201305-03 07:49:11 INFO watch_tim : PAR:0000000005 (Company #5 (u'Air Liquide Belgium')) : Company becomes Client
        """

        Company(name="Air Liquide Belgium", id=5).save()
        ln = """{"method":"PUT","alias":"PAR","id":"0000000005","time":"20130503 07:36:15",
        "user":"","data":{"IDPAR":"0000000005","FIRME":"Air Liquide Belgium",
        "NAME2":"","RUE":"Quai des Vennes","CP":"4020","IDPRT":"V","PAYS":"B",
        "TEL":"04/349.89.89","FAX":"04/341.20.70","COMPTE1":"GKCCBEBB:BE57551373330235",
        "NOTVA":"BE-0441.857.467","COMPTE3":"","IDPGP":"","DC.debit":"","DC.credit":"",
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
        self.assertDoesNotExist(Client, id=5)
        obj = Company.objects.get(id=5)
        self.assertEqual(obj.name, "Air Liquide Belgium")
        with translation.override('en'):
            s = changes_to_rst(obj.partner_ptr)
        # print s
        self.assertEqual(s, """\
+-----------+-------------+----------------------------+--------------------------------------------------------+--------------+-----------+
| User      | Change Type | Object                     | Changes                                                | Object type  | object id |
+===========+=============+============================+========================================================+==============+===========+
| watch_tim | Update      | *S.A. Air Liquide Belgium* | - activity_id : None --> 19                            | Organization | 5         |
|           |             |                            | - bank_account1 : None --> 'GKCCBEBB:BE57551373330235' |              |           |
|           |             |                            | - bank_account2 : None --> 'BBRUBEBB:BE12310110444892' |              |           |
|           |             |                            | - city_id : None --> 3                                 |              |           |
|           |             |                            | - country_id : None --> 'B'                            |              |           |
|           |             |                            | - fax : '' --> '04/341.20.70'                          |              |           |
|           |             |                            | - language : '' --> 'fr'                               |              |           |
|           |             |                            | - phone : '' --> '04/349.89.89'                        |              |           |
|           |             |                            | - prefix : '' --> 'S.A.'                               |              |           |
|           |             |                            | - street : '' --> 'Quai des Vennes'                    |              |           |
|           |             |                            | - street_no : '' --> '8'                               |              |           |
|           |             |                            | - vat_id : '' --> 'BE-0441.857.467'                    |              |           |
|           |             |                            | - zip_code : '' --> '4020'                             |              |           |
+-----------+-------------+----------------------------+--------------------------------------------------------+--------------+-----------+

""")

        """
        Person becomes Company
        """
        Person(id=9932, first_name="CPAS", last_name="Andenne").save()
        ln = """{"method":"PUT","alias":"PAR","id":"0000009932","time":"20130503 07:38:16","user":"","data":{"IDPAR":"0000009932","FIRME":"Andenne, CPAS","NAME2":"","RUE":"Rue de l'Hopital","CP":"5300","IDPRT":"V","PAYS":"B","TEL":"","FAX":"","COMPTE1":"","NOTVA":"BE-0999.999.999","COMPTE3":"","IDPGP":"","DC.debit":"","DC.credit":"","ATTRIB":"","IDMFC":"","LANGUE":"F","IDBUD":"","PROF":"65","CODE1":"","CODE2":"","CODE3":"","DATCREA":{"__date__":{"year":1988,"month":12,"day":9}},"ALLO":"","NB1":"","NB2":"        0","IDDEV":"","MEMO":"","COMPTE2":"","RUENUM":"  22","RUEBTE":"","DEBIT2":"","CREDIT2":"","IMPDATE":{"__date__":{"year":0,"month":0,"day":0}},"ATTRIB2":"","CPTSYSI":"","EMAIL":"","MVIDATE":{"__date__":{"year":0,"month":0,"day":0}},"IDUSR":"","DOMI1":""}}"""
        process_line(ln)
        self.assertDoesNotExist(Client, id=9932)
        self.assertDoesNotExist(Person, id=9932)
        obj = Company.objects.get(id=9932)
        self.assertEqual(obj.name, "Andenne, CPAS")

        with translation.override('en'):
            s = changes_to_rst(obj.partner_ptr)
        #~ print s
        self.assertEqual(s, """\
=========== ============== ================= ================== ============= ===========
 User        Change Type    Object            Changes            Object type   object id
----------- -------------- ----------------- ------------------ ------------- -----------
 watch_tim   Add child      *Andenne, CPAS*   contacts.Company   Partner       9932
 watch_tim   Remove child                     contacts.Person    Person        9932
=========== ============== ================= ================== ============= ===========

""")

        """
        A PAR without NoTVA becomes a Person, but if no first_name can 
        be detected, then it is just a simple partner
        """
        ln = """{"method":"PUT","alias":"PAR","id":"0000001267","time":"20130517 12:34:15",
        "user":"","data":{"IDPAR":"0000001267","FIRME":"Velopa","NAME2":"",
        "RUE":"Leuvenselaan","CP":"3300","IDPRT":"I","PAYS":"B","TEL":"",
        "FAX":"","COMPTE1":"","NOTVA":"","COMPTE3":"","IDPGP":"",
        "DC.debit":"","DC.credit":"","ATTRIB":"","IDMFC":"30","LANGUE":"F","IDBUD":"",
        "PROF":"15","CODE1":"","CODE2":"","CODE3":"",
        "DATCREA":{"__date__":{"year":1992,"month":1,"day":2}},"ALLO":"S.A.",
        "NB1":"","NB2":"","IDDEV":"","MEMO":"","COMPTE2":"","RUENUM":" 172",
        "RUEBTE":"","DEBIT2":"","CREDIT2":"","IMPDATE":{"__date__":{"year":1996,"month":8,"day":30}},
        "ATTRIB2":"","CPTSYSI":"","EMAIL":"",
        "MVIDATE":{"__date__":{"year":0,"month":0,"day":0}},"IDUSR":"",
        "DOMI1":""}}"""
        self.assertDoesNotExist(Partner, id=1267)
        process_line(ln)
        obj = Partner.objects.get(id=1267)
        self.assertEqual(obj.name, "Velopa")
        #~ try:
            #~ process_line(ln)
            #~ self.fail("""Expected ValidationError: {'first_name': [u'Dieses Feld darf nicht leer sein.']}""")
            # ~ # NOTVA ist leer, also will watch_tim eine Person draus machen,
            # ~ # aber dazu bräuchte er auch einen Vornamen
        #~ except ValidationError as e:
            #~ pass
        #~ self.assertDoesNotExist(Partner,id=1267)

        ln = """{"method":"PUT","alias":"PAR","id":"0000000665","time":"20130517 12:33:58","user":"",
        "data":{"IDPAR":"0000000665","FIRME":"Petra","NAME2":"","RUE":"Beskensstraat 34","CP":"3520",
        "IDPRT":"I","PAYS":"B","TEL":"011/815911","FAX":"","COMPTE1":"","NOTVA":"BE-0426.896.703",
        "COMPTE3":"","IDPGP":"","DC.debit":"","DC.credit":"","ATTRIB":"","IDMFC":"30",
        "LANGUE":"3",
        "IDBUD":"","PROF":"12","CODE1":"","CODE2":"","CODE3":"",
        "DATCREA":{"__date__":{"year":1986,"month":8,"day":14}},"ALLO":"sprl","NB1":"","NB2":"",
        "IDDEV":"","MEMO":"","COMPTE2":"","RUENUM":"","RUEBTE":"","DEBIT2":"","CREDIT2":"",
        "IMPDATE":{"__date__":{"year":0,"month":0,"day":0}},"ATTRIB2":"","CPTSYSI":"",
        "EMAIL":"","MVIDATE":{"__date__":{"year":0,"month":0,"day":0}},"IDUSR":"","DOMI1":""}}"""
        process_line(ln)
        obj = Company.objects.get(id=665)
        self.assertEqual(obj.name, "Petra")

        # ~ INFO PAR:0000007826 (Client #7826 (u'MUSTERMANN Peter (7826)')) : Client becomes Person
        #~ WARNING Exception 'ValidationError([u'A Person cannot be parent for a Person'])' while processing changelog line:
        Client(id=7826, first_name="Peter", last_name="Mustermann").save()
        ln = """{"method":"PUT","alias":"PAR","id":"0000007826","time":"20130517 12:35:51","user":"",
        "data":{"IDPAR":"0000007826","FIRME":"Mustermann Peter","NAME2":"","RUE":"Burgundstraße","CP":
        "4700","IDPRT":"S","PAYS":"B","TEL":"","FAX":"","COMPTE1":"","NOTVA":"",
        "COMPTE3":"","IDPGP":"","DC.debit":"","DC.credit":"","ATTRIB":"A",
        "IDMFC":"30","LANGUE":"D","IDBUD":"","PROF":"82","CODE1":"",
        "CODE2":"","CODE3":"","DATCREA":{"__date__":{"year":2006,"month":1,"day":5}},
        "ALLO":"Herrn","NB1":"","NB2":"","IDDEV":"","MEMO":"","COMPTE2":"",
        "RUENUM":"   9","RUEBTE":"","DEBIT2":"","CREDIT2":"",
        "IMPDATE":{"__date__":{"year":2009,"month":9,"day":22}},
        "ATTRIB2":"","CPTSYSI":"","EMAIL":"","MVIDATE":{"__date__":{"year":0,"month":0,"day":0}},
        "IDUSR":"ALICIA","DOMI1":""}}"""
        process_line(ln)
        self.assertDoesNotExist(Client, id=7826)

        """
        20130602 : datum_bis einer primären Begleitung eines Ehemaligen darf
        nicht leer sein. Wenn es das ist, soll watch_tim es auf PAR->DatCrea
        setzen. 
        """
        with translation.override('de'):
            self.assertDoesNotExist(Coaching, client_id=7826)
            ln = ln.replace('"NB2":""', '"NB2":"940702 234-24"')
            process_line(ln)
            obj = Client.objects.get(id=7826)
            self.assertEqual(obj.name, "Mustermann Peter")
            s = coachings_to_rst(obj)
            #~ print s
            self.assertEqual(s, """\
================ ===== =========== ======== ======== ==================
 Begleitet seit   bis   Begleiter   Primär   Dienst   Beendigungsgrund
---------------- ----- ----------- -------- -------- ------------------
 05.01.06               alicia      Ja       DSBE
================ ===== =========== ======== ======== ==================

""")

            """
            Kunde wurde in TIM nach Inaktive versetzt:
            """
            ln = ln.replace('"IDPRT":"S"', '"IDPRT":"I"')
            process_line(ln)
            s = coachings_to_rst(obj)
            #~ print s
            self.assertEqual(s, """\
================ ========== =========== ======== ======== ==================
 Begleitet seit   bis        Begleiter   Primär   Dienst   Beendigungsgrund
---------------- ---------- ----------- -------- -------- ------------------
 05.01.06         05.01.06   alicia      Ja       DSBE
================ ========== =========== ======== ======== ==================

""")

            """
            20131029 
            Begleitung wird in Lino manuell als nicht primär markiert.
            Dann wird Kunde in TIM (1) zurück nach S versetzt und (2) 
            von ALICIA zu ROGER.
            """
            coaching = rt.models.coachings.Coaching.objects.get(client=obj, primary=True)
            coaching.primary = False
            coaching.save()
            s = coachings_to_rst(obj)
            #~ print s
            self.assertEqual(s, """\
================ ========== =========== ======== ======== ==================
 Begleitet seit   bis        Begleiter   Primär   Dienst   Beendigungsgrund
---------------- ---------- ----------- -------- -------- ------------------
 05.01.06         05.01.06   alicia      Nein     DSBE
================ ========== =========== ======== ======== ==================

""")

            ln = ln.replace('"IDPRT":"I"', '"IDPRT":"S"')
            process_line(ln)
            s = coachings_to_rst(obj)
            #~ print s
            self.assertEqual(s, """\
================ ========== =========== ======== ======== ==================
 Begleitet seit   bis        Begleiter   Primär   Dienst   Beendigungsgrund
---------------- ---------- ----------- -------- -------- ------------------
 05.01.06         05.01.06   alicia      Nein     DSBE
 05.01.06                    alicia      Ja       DSBE
================ ========== =========== ======== ======== ==================

""")
            ln = ln.replace('"IDUSR":"ALICIA"', '"IDUSR":"ROGER"')
            process_line(ln)
            s = coachings_to_rst(obj)
            #~ print s
            self.assertEqual(s, """\
================ ========== =========== ======== ======== ==================
 Begleitet seit   bis        Begleiter   Primär   Dienst   Beendigungsgrund
---------------- ---------- ----------- -------- -------- ------------------
 05.01.06         05.01.06   alicia      Nein     DSBE
 05.01.06         17.05.13   alicia      Nein     DSBE
 17.05.13                    roger       Ja       ASD
================ ========== =========== ======== ======== ==================

""")

        """
        A non-client partner with empty PAR->NoTva will become a Person, not a Company.
        If the partner is in fact a company whose NoTva has just been forgotten, 
        then watch_tim will raise a ValidationError:
        """
        ln = """{"method":"POST","alias":"PAR","id":"0000087683","time":"20130610 11:26:30",
        "user":"ROGER","data":{"IDPAR":"0000087683","FIRME":"Bellavilla","NAME2":"","RUE":"",
        "CP":"","IDPRT":"V","PAYS":"","TEL":"","FAX":"","COMPTE1":"","NOTVA":"","COMPTE3":"",
        "IDPGP":"","DC.debit":"","DC.credit":"","ATTRIB":"","IDMFC":"30","LANGUE":"D","IDBUD":"",
        "PROF":"00","CODE1":"","CODE2":"","CODE3":"",
        "DATCREA":{"__date__":{"year":2013,"month":6,"day":10}},"ALLO":"","NB1":"",
        "NB2":"","IDDEV":"","MEMO":"","COMPTE2":"","RUENUM":"","RUEBTE":"","DEBIT2":"",
        "CREDIT2":"","IMPDATE":{"__date__":{"year":0,"month":0,"day":0}},"ATTRIB2":"",
        "CPTSYSI":"","EMAIL":"","MVIDATE":{"__date__":{"year":0,"month":0,"day":0}},
        "IDUSR":"","DOMI1":""}}"""
        self.assertDoesNotExist(Partner, id=87683)
        process_line(ln)
        #~ try:
            #~ self.fail("Expected ValidationError {'first_name': [u'Dieses Feld darf nicht leer sein.']}")
        #~ except ValidationError as e:
        obj = Partner.objects.get(id=87683)
        for m in Company, Person, Client, Household:
            self.assertDoesNotExist(m, id=87683)

        ln = """{"method":"PUT","alias":"PAR","id":"0000004124","time":"20130517 12:34:37",
        "user":"","data":{"IDPAR":"0000004124","FIRME":"Theves-Carlsberg","NAME2":"",
        "RUE":"Werthplatz 22","CP":"4700","IDPRT":"I","PAYS":"B","TEL":"","FAX":"",
        "COMPTE1":"","NOTVA":"BE-0999.999.999","COMPTE3":"","IDPGP":"","DC.debit":"",
        "DC.credit":"","ATTRIB":"W","IDMFC":"","LANGUE":"D","IDBUD":"","PROF":"80",
        "CODE1":"EP","CODE2":"","CODE3":"","DATCREA":{"__date__":{"year":1985,
        "month":4,"day":18}},"ALLO":"Eheleute","NB1":"THCA600115","NB2":"",
        "IDDEV":"","MEMO":"","COMPTE2":"","RUENUM":"","RUEBTE":"",
        "DEBIT2":"","CREDIT2":"","IMPDATE":{"__date__":{"year":0,
        "month":0,"day":0}},"ATTRIB2":"","CPTSYSI":"","EMAIL":"",
        "MVIDATE":{"__date__":{"year":0,"month":0,"day":0}},
        "IDUSR":"ROGER","DOMI1":""}}"""
        self.assertDoesNotExist(Partner, id=4124)
        process_line(ln)
        obj = Company.objects.get(id=4124)
        ln = ln.replace("BE-0999.999.999", "")
        process_line(ln)
        self.assertDoesNotExist(Company, id=4124)
        obj = Household.objects.get(id=4124)

        ln = """{"method":"PUT","alias":"PAR","id":"0000001315",
        "time":"20130811 10:33:20","user":"PAC","data":{"IDPAR":"0000001315",
        "FIRME":"C2D System House","NAME2":"",
        "RUE":"Rue des Champs","CP":"4630","IDPRT":"V","PAYS":"B","TEL":"04/567.89.10",
        "FAX":"04/365.31.10","COMPTE1":"JVBABE22:BE39645678910619",
        "NOTVA":"BE-0123.456.789","COMPTE3":"","IDPGP":"",
        "DC.debit":"","DC.credit":"","ATTRIB":"","IDMFC":"30","LANGUE":"F",
        "IDBUD":"","PROF":"22","CODE1":"","CODE2":"","CODE3":"",
        "DATCREA":{"__date__":{"year":1992,"month":7,"day":24}},"ALLO":"S.A.",
        "NB1":"EUPO","NB2":"","IDDEV":"","MEMO":"","COMPTE2":"",
        "RUENUM":"   8","RUEBTE":"","DEBIT2":"","CREDIT2":"",
        "IMPDATE":{"__date__":{"year":2012,"month":10,"day":25}},
        "ATTRIB2":"","CPTSYSI":"","EMAIL":"info@c2d.be",
        "MVIDATE":{"__date__":{"year":2012,"month":1,"day":25}},
        "IDUSR":"","DOMI1":""}} """

        self.assertDoesNotExist(Partner, id=1315)
        process_line(ln)
        obj = Partner.objects.get(id=1315)
        obj = Company.objects.get(id=1315)
        for m in Person, Client, Household:
            self.assertDoesNotExist(m, id=1315)

        """{"method":"PUT","alias":"PAR","id":"0000001588","time":"20131001 10:38:08",
        "user":"PAC","data":{"IDPAR":"0000001588","FIRME":"Zentrum f.Aus- u. Weiterbildung des",
        "NAME2":"Mittelstandes","RUE":"Limburgerweg","CP":"4700","IDPRT":"V","PAYS":"B",
        "TEL":"087/59.39.89","FAX":"087/55.27.95","COMPTE1":"BBRUBEBB:BE16340143185374",
        "NOTVA":"BE-0999.999.999","COMPTE3":"","IDPGP":"","DC.debit":"","DC.credit":"",
        "ATTRIB":"","IDMFC":"30","LANGUE":"D","IDBUD":"","PROF":"62","CODE1":"",
        "CODE2":"","CODE3":"","DATCREA":{"__date__":{"year":1994,"month":11,"day":16}},
        "ALLO":"G.o.E.","NB1":"","NB2":"","IDDEV":"","MEMO":"\n",
        "COMPTE2":"BKCPBEB1CPB:BE39129056571619","RUENUM":"   2","RUEBTE":"","DEBIT2":"",
        "CREDIT2":"","IMPDATE":{"__date__":{"year":2011,"month":10,"day":17}},
        "ATTRIB2":"","CPTSYSI":"","EMAIL":"zawm@zawm.be",
        "MVIDATE":{"__date__":{"year":0,"month":0,"day":0}},"IDUSR":"","DOMI1":""}}"""

        """{"method":"PUT","alias":"PAR","id":"0000022307","time":"20131002 14:40:27","user":"GERD",
        "data":{"IDPAR":"0000022307","FIRME":"Lerho Renée","NAME2":"","RUE":"Lütticher Strasse 321 /A",
        "CP":"4721","IDPRT":"S","PAYS":"B","TEL":"","FAX":"","COMPTE1":"","NOTVA":"","COMPTE3":"",
        "IDPGP":"","DC.debit":"","DC.credit":"","ATTRIB":"","IDMFC":"30","LANGUE":"D","IDBUD":"","PROF":"91",
        "CODE1":"","CODE2":"","CODE3":"","DATCREA":{"__date__":{"year":2010,"month":9,"day":1}},"ALLO":"","NB1":"",
        "NB2":"941128 176-65","IDDEV":"","MEMO":"","COMPTE2":"",
        "RUENUM":" 000","RUEBTE":"","DEBIT2":"","CREDIT2":"",
        "IMPDATE":{"__date__":{"year":0,"month":0,"day":0}},
        "ATTRIB2":"","CPTSYSI":"","EMAIL":"",
        "MVIDATE":{"__date__":{"year":0,"month":0,"day":0}},"IDUSR":"ALICIA","DOMI1":""}}"""

        """{"method":"PUT","alias":"PXS","id":"0000022307","time":"20131002 14:41:26","user":"GERD",
        "data":{"IDPAR":"0000022307","NAME":"Lerho Renée",
        "GEBDAT":{"__date__":{"year":1994,"month":11,"day":28}},"APOTHEKE":"","HILFE":"",
        "ANTEIL":"","IDMUT":"137","VOLLMACHT":{"__date__":{"year":0,"month":0,"day":0}},
        "LAUFZEIT":{"__date__":{"year":0,"month":0,"day":0}},"DRINGEND":"","MONATLICH":"",
        "SOZIAL":"","MIETE":"","MAF":"","REFERENZ":"","MEMO":"","SEXE":"W","GENERIKA":"",
        "IDPRT":"S","CARDNUMBER":"591438120107","VALID1":{"__date__":{"year":2011,
        "month":9,"day":21}},"VALID2":{"__date__":{"year":2016,"month":9,"day":21}},
        "CARDTYPE":1,"NATIONALIT":"B","BIRTHPLACE":"Eupen","NOBLECOND":"",
        "CARDISSUER":"Eupen"}}
        """


def changes_to_rst(master):
    A = settings.SITE.models.changes.ChangesByMaster
    return A.request(master).to_rst(
        column_names='user type object diff:30 object_type object_id')


def coachings_to_rst(master):
    A = settings.SITE.models.coachings.CoachingsByClient
    return A.request(master).to_rst()
