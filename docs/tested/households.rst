.. _welfare.tested.households:

Households
==========

.. include:: /include/tested.rst

..
  This document is part of the test suite.
  To test only this document, run::
    $ python setup.py test -s tests.DocsTests.test_households

Preparatory stuff:

>>> from __future__ import print_function
>>> import os
>>> os.environ['DJANGO_SETTINGS_MODULE'] = \
...    'lino_welfare.projects.docs.settings.doctests'
>>> from lino.runtime import *
>>> from django.utils import translation
>>> from django.test import Client
>>> import json
>>> from bs4 import BeautifulSoup
>>> ses = rt.login('rolf')

.. _paulfrisch:

Paul Frisch
-----------

Mr. Paul Frisch is a fictive client for which the demo database
contains fictive family links.

>>> print(contacts.Person.objects.get(first_name="Paul", last_name="Frisch"))
Mr Paul Frisch (236)

>>> client = Client()
>>> def check(uri, fieldname):
...     url = '/api/%s?fmt=json&an=detail' % uri
...     res = client.get(url, REMOTE_USER='rolf')
...     assert res.status_code == 200
...     d = json.loads(res.content)
...     return d['data'][fieldname]

>>> soup = BeautifulSoup(check('contacts/Persons/236', 'LinksByHuman'))
>>> links = soup.find_all('a')
>>> len(links)
21

>>> print(links[1].get('href'))
... #doctest: +NORMALIZE_WHITESPACE
javascript:Lino.contacts.Persons.detail.run(null,{ "record_id": 244 })

These are the family relationships of Paul Frisch:

>>> print(soup.get_text(' ', strip=True))
... #doctest: +NORMALIZE_WHITESPACE +REPORT_CDIFF
Paul ist Vater von Dennis (12 Jahre) Vater von Clara (14 Jahre) Vater
von Philippe (16 Jahre) Vater von Peter (26 Jahre) Ehemann von Petra
ZWEITH (45 Jahre) Sohn von Gaby FROGEMUTH (79 Jahre) Sohn von Hubert
(80 Jahre) Beziehung erstellen als Vater / Sohn Adoptivvater /
Adoptivsohn Ehemann Partner Stiefvater / Stiefsohn Bruder Vetter Onkel
/ Neffe Verwandter Sonstiger

The previous AJAX call caused Django's translation machine to switch
to German. Switch back to English.

>>> translation.activate('en')

Paul's father Hubert is married with Gaby and they live
together. Their children have moved out.

>>> obj = contacts.Person.objects.get(name="Frisch Hubert")
>>> print(obj)
Mr Hubert Frisch (234)
>>> ses.show(households.SiblingsByPerson, master_instance=obj)
========== =================== =============== ========================== ============ =========== ============ ========
 Age        Role                Dependency      Person                     First name   Last name   Birth date   Gender
---------- ------------------- --------------- -------------------------- ------------ ----------- ------------ --------
 80 years   Head of household   Not at charge   Mr Hubert Frisch (234)     Hubert       Frisch      1933-07-21   Male
 79 years   Partner             Not at charge   Mrs Gaby Frogemuth (235)   Gaby         Frogemuth   1934-08-04   Female
========== =================== =============== ========================== ============ =========== ============ ========
<BLANKLINE>

Paul Frisch is married with Petra Zweith and has a child from divorced
marriage with Paula Einzig.

>>> obj = contacts.Person.objects.get(name="Frisch Paul")
>>> print(obj)
Mr Paul Frisch (236)
>>> ses.show(households.SiblingsByPerson, master_instance=obj)
========== =================== ================ ========================== ============ =========== ============ ========
 Age        Role                Dependency       Person                     First name   Last name   Birth date   Gender
---------- ------------------- ---------------- -------------------------- ------------ ----------- ------------ --------
 46 years   Head of household   Not at charge    Mr Paul Frisch (236)       Paul         Frisch      1967-06-19   Male
 45 years   Partner             Not at charge    Mrs Petra Zweith (242)     Petra        Zweith      1968-12-19   Female
 16 years   Child               At full charge   Mr Philippe Frisch (243)   Philippe     Frisch      1997-06-19   Male
 14 years   Child               At full charge   Mrs Clara Frisch (244)     Clara        Frisch      1999-06-19   Female
 12 years   Child               At full charge   Mr Dennis Frisch (246)     Dennis       Frisch      2001-06-19   Male
========== =================== ================ ========================== ============ =========== ============ ========
<BLANKLINE>

Here is their :class:`welfare.households.RefundsByPerson`:

>>> ses.show(households.RefundsByPerson, master_instance=obj)
==================== ======== ================= ===========
 Age                  Gender   Person            Amount
-------------------- -------- ----------------- -----------
 46 years             Male     Paul Frisch       20,00
 45 years             Female   Petra Zweith      20,00
 16 years             Male     Philippe Frisch   10,00
 14 years             Female   Clara Frisch      10,00
 12 years             Male     Dennis Frisch     10,00
 **Total (5 rows)**                              **70,00**
==================== ======== ================= ===========
<BLANKLINE>


Ludwig Frisch is married with Laura Loslever and they live together
with their two children.

>>> obj = contacts.Person.objects.get(name="Frisch Ludwig")
>>> print(obj)
Mr Ludwig Frisch (237)
>>> ses.show(households.SiblingsByPerson, master_instance=obj)
========== =================== ================ ========================== ============ =========== ============ ========
 Age        Role                Dependency       Person                     First name   Last name   Birth date   Gender
---------- ------------------- ---------------- -------------------------- ------------ ----------- ------------ --------
 46 years   Partner             Not at charge    Mrs Laura Loslever (247)   Laura        Loslever    1968-04-27   Female
 46 years   Head of household   Not at charge    Mr Ludwig Frisch (237)     Ludwig       Frisch      1968-06-01   Male
 12 years   Child               At full charge   Mrs Melba Frisch (248)     Melba        Frisch      2002-04-05   Female
 6 years    Child               At full charge   Mrs Irma Frisch (249)      Irma         Frisch      2008-03-24   Female
========== =================== ================ ========================== ============ =========== ============ ========
<BLANKLINE>


Here is their :class:`welfare.households.RefundsByPerson`:

>>> ses.show(households.RefundsByPerson, master_instance=obj)
==================== ======== ================ ===========
 Age                  Gender   Person           Amount
-------------------- -------- ---------------- -----------
 46 years             Female   Laura Loslever   20,00
 46 years             Male     Ludwig Frisch    20,00
 12 years             Female   Melba Frisch     10,00
 6 years              Female   Irma Frisch      10,00
 **Total (4 rows)**                             **60,00**
==================== ======== ================ ===========
<BLANKLINE>
