.. _welfare.tested.households:

==========
Households
==========

.. How to test only this document:

    $ python setup.py test -s tests.SpecsTests.test_households

    doctest init:

    >>> from __future__ import print_function
    >>> import os
    >>> os.environ['DJANGO_SETTINGS_MODULE'] = \
    ...    'lino_welfare.projects.std.settings.doctests'
    >>> from lino.api.doctest import *

A technical tour into the :mod:`lino_welfare.modlib.households` module.


.. contents::
   :local:



.. _paulfrisch:

Paul Frisch
===========

Mr. Paul Frisch is a fictive client for which the demo database
contains fictive family links.

>>> paul = contacts.Person.objects.get(first_name="Paul", last_name="Frisch")
>>> print(paul.id)
240
>>> print(paul)
Mr Paul FRISCH

>>> client = Client()
>>> def check(uri, fieldname):
...     url = '/api/%s?fmt=json&an=detail' % uri
...     res = client.get(url, REMOTE_USER='rolf')
...     assert res.status_code == 200
...     d = json.loads(res.content)
...     return d['data'][fieldname]

>>> soup = BeautifulSoup(check('contacts/Persons/240', 'LinksByHuman'))
>>> links = soup.find_all('a')
>>> len(links)
21

>>> print(links[1].get('href'))
... #doctest: +NORMALIZE_WHITESPACE
javascript:Lino.contacts.Persons.detail.run(null,{ "record_id": 248 })

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
Mr Hubert FRISCH
>>> ses = rt.login('rolf')
>>> ses.show(households.SiblingsByPerson, master_instance=obj)
========== =================== =============== ==================== ============ =========== ============ ========
 Age        Role                Dependency      Person               First name   Last name   Birth date   Gender
---------- ------------------- --------------- -------------------- ------------ ----------- ------------ --------
 80 years   Head of household   Not at charge   Mr Hubert FRISCH     Hubert       Frisch      1933-07-21   Male
 79 years   Partner             Not at charge   Mrs Gaby FROGEMUTH   Gaby         Frogemuth   1934-08-04   Female
========== =================== =============== ==================== ============ =========== ============ ========
<BLANKLINE>

Paul Frisch is married with Petra Zweith and has a child from divorced
marriage with Paula Einzig.

>>> obj = contacts.Person.objects.get(name="Frisch Paul")
>>> print(obj)
Mr Paul FRISCH
>>> ses.show(households.SiblingsByPerson, master_instance=obj)
========== =================== ================ ==================== ============ =========== ============ ========
 Age        Role                Dependency       Person               First name   Last name   Birth date   Gender
---------- ------------------- ---------------- -------------------- ------------ ----------- ------------ --------
 46 years   Head of household   Not at charge    Mr Paul FRISCH       Paul         Frisch      1967-06-19   Male
 45 years   Partner             Not at charge    Mrs Petra ZWEITH     Petra        Zweith      1968-12-19   Female
 16 years   Child               At full charge   Mr Philippe FRISCH   Philippe     Frisch      1997-06-19   Male
 14 years   Child               At full charge   Mrs Clara FRISCH     Clara        Frisch      1999-06-19   Female
 12 years   Child               At full charge   Mr Dennis FRISCH     Dennis       Frisch      2001-06-19   Male
========== =================== ================ ==================== ============ =========== ============ ========
<BLANKLINE>

Here is their :class:`welfare.households.RefundsByPerson`:

>>> ses.show(households.RefundsByPerson, master_instance=obj)
==================== ======== ================= ===========
 Age                  Gender   Person            Amount
-------------------- -------- ----------------- -----------
 46 years             Male     Paul FRISCH       20,00
 45 years             Female   Petra ZWEITH      20,00
 16 years             Male     Philippe FRISCH   10,00
 14 years             Female   Clara FRISCH      10,00
 12 years             Male     Dennis FRISCH     10,00
 **Total (5 rows)**                              **70,00**
==================== ======== ================= ===========
<BLANKLINE>


Ludwig Frisch is married with Laura Loslever and they live together
with their two children.

>>> obj = contacts.Person.objects.get(name="Frisch Ludwig")
>>> print(obj)
Mr Ludwig FRISCH
>>> ses.show(households.SiblingsByPerson, master_instance=obj)
========== =================== ================ ==================== ============ =========== ============ ========
 Age        Role                Dependency       Person               First name   Last name   Birth date   Gender
---------- ------------------- ---------------- -------------------- ------------ ----------- ------------ --------
 46 years   Partner             Not at charge    Mrs Laura LOSLEVER   Laura        Loslever    1968-04-27   Female
 46 years   Head of household   Not at charge    Mr Ludwig FRISCH     Ludwig       Frisch      1968-06-01   Male
 12 years   Child               At full charge   Mrs Melba FRISCH     Melba        Frisch      2002-04-05   Female
 6 years    Child               At full charge   Mrs Irma FRISCH      Irma         Frisch      2008-03-24   Female
========== =================== ================ ==================== ============ =========== ============ ========
<BLANKLINE>


Here is their :class:`welfare.households.RefundsByPerson`:

>>> ses.show(households.RefundsByPerson, master_instance=obj)
==================== ======== ================ ===========
 Age                  Gender   Person           Amount
-------------------- -------- ---------------- -----------
 46 years             Female   Laura LOSLEVER   20,00
 46 years             Male     Ludwig FRISCH    20,00
 12 years             Female   Melba FRISCH     10,00
 6 years              Female   Irma FRISCH      10,00
 **Total (4 rows)**                             **60,00**
==================== ======== ================ ===========
<BLANKLINE>


Inspecting the MembersByPerson panel
====================================

The following code caused an exception "ParameterStore of LayoutHandle
for ParamsLayout on pcsw.Clients expects a list of 12 values but got
16" on :blogref:`20140429`.

>>> print(pcsw.Client.objects.get(pk=179))
DUBOIS Robin (179)

>>> client = Client()
>>> url = '/api/integ/Clients/179?pv=30&pv=5&pv=&pv=29.04.2014&pv=29.04.2014&pv=&pv=&pv=&pv=&pv=&pv=false&pv=&pv=&pv=1&pv=false&pv=false&an=detail&rp=ext-comp-1351&fmt=json'
>>> res = test_client.get(url, REMOTE_USER='rolf')
>>> print(res.status_code)
200

The response to this AJAX request is in JSON:

>>> d = json.loads(res.content)

We test the MembersByPerson panel. It contains a summary:

>>> print(d['data']['MembersByPerson'])
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
<div>DUBOIS Robin (179) ist<ul><li><a href="javascript:Lino.households.Members.set_primary(...)...</div>

Since this is not very human-readable, we are going to analyze it with
`BeautifulSoup <http://beautiful-soup-4.readthedocs.org/en/latest>`_.

>>> soup = BeautifulSoup(d['data']['MembersByPerson'])

>>> print(soup.get_text(' ', strip=True))
... #doctest: +NORMALIZE_WHITESPACE +REPORT_CDIFF
DUBOIS Robin (179) ist ☐ Vorstand in Robin & Mélanie Dubois-Mélard Haushalt erstellen : Ehepartner / Geschieden / Faktischer Haushalt / Legale Wohngemeinschaft / Getrennt / Sonstige

>>> links = soup.find_all('a')

It contains eight links:

>>> len(links)
8

The first link is the disabled checkbox for the :attr:`primary
<lino.modlib.households.models.Member.primary>` field:

>>> print(links[0].string)
... #doctest: +NORMALIZE_WHITESPACE
☐

Clicking on this would run the following JavaScript:

>>> print(links[0].get('href'))
javascript:Lino.households.Members.set_primary("ext-comp-1351",9,{  })

The next link is the name of the household, and clicking on it would
equally execute some Javascript code:

>>> print(links[1].string)
Robin & Mélanie Dubois-Mélard
>>> print(links[1].get('href'))
javascript:Lino.households.Households.detail.run("ext-comp-1351",{ "record_id": 236 })


The third link is:

>>> print(links[2].string)
Ehepartner
>>> print(links[2].get('href'))
... #doctest: +NORMALIZE_WHITESPACE +ELLIPSIS
javascript:Lino.contacts.Persons.create_household.run("ext-comp-1351",{
"field_values": { 
  "head": "DUBOIS Robin (179)", "headHidden": 179, 
  "typeHidden": 1, 
  "partner": null, "partnerHidden": null, 
  "type": "Ehepartner" 
}, "param_values": { 
  "also_obsolete": false, "gender": null, "genderHidden": null 
}, "base_params": {  } })


The :func:`lino.api.doctest.get_json_soup` automates this trick:

>>> soup = get_json_soup('rolf', 'integ/Clients/179', 'MembersByPerson')
>>> links = soup.find_all('a')
>>> len(links)
8
