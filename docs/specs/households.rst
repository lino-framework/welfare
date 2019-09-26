.. doctest docs/specs/households.rst
.. _welfare.specs.households:
.. include:: /../docs/shared/include/defs.rst

==========
Households
==========

.. currentmodule:: lino_welfare.modlib.households

The :mod:`lino_welfare.modlib.households` plugin extends
:mod:`lino.modlib.households` by adding some PCSW-specific features.


.. contents::
   :local:

.. include:: /shared/include/tested.rst

>>> from lino import startup
>>> startup('lino_welfare.projects.gerd.settings.doctests')
>>> from lino.api.doctest import *
>>> import datetime


Added features
==============

.. class:: RefundsByPerson

    Shows the members of the primary household of this person together with an
    amount which depends on whether that member is adult or not.

    This is a special form of :class:`lino_xl.lib.households.SiblingsByPerson`,
    used e.g. in :xfile:`aids/Confirmation/clothes_bank.body.html`.

    It has two configurable attributes:

    .. attribute:: child_tariff

        The amount to refund for children (household members less than
        :attr:`lino_xl.lib.households.Plugin.adult_age` years old).

    .. attribute:: adult_tariff

        The amount to refund for children (household members who are
        :attr:`lino_xl.lib.households.Plugin.adult_age` years or older).

    The values of these attributes are hard-coded and defaul to 10 and 20:

    >>> rt.models.households.RefundsByPerson.child_tariff
    Decimal('10')
    >>> rt.models.households.RefundsByPerson.adult_tariff
    Decimal('20')

    You might change them locally e.g. in the
    :attr:`lino.core.site.Site.custom_layouts` module.


    .. attribute:: person_info

        The full name of the household member.

    .. attribute:: amount

        The amount to pay. This is either :attr:`child_tariff` or
        :attr:`adult_tarif` depending on the age of the household member.

    See the examples below.


.. function:: get_household_summary(person, today=None, adult_age=None)

    Return a string which expresses the household composition in a few
    words. See `The household summary`_.

    Note that members without `birth_date` are considered children.


.. _paulfrisch:

Paul Frisch
===========

Mr. Paul Frisch is a fictive client for which the demo database
contains fictive family links.

>>> paul = contacts.Person.objects.get(first_name="Paul", last_name="Frisch")
>>> print(paul.id)
240
>>> print(paul)
Herr Paul FRISCH

His primary household consists of 2 adults and 3 children:

>>> print(rt.models.households.get_household_summary(paul))
2 Erwachsene und 3 Kinder



>>> test_client.force_login(rt.login('rolf').user)

>>> def check(uri, fieldname):
...     url = '/api/%s?fmt=json&an=detail' % uri
...     res = test_client.get(url, REMOTE_USER='rolf')
...     assert res.status_code == 200
...     d = json.loads(res.content)
...     if not fieldname in d['data']:
...         raise Exception("20181023 '{}' not in {}".format(
...             fieldname, d['data'].keys()))
...     return d['data'][fieldname]

>>> uri = 'contacts/Persons/{}'.format(paul.id)
>>> html = check(uri, 'humanlinks_LinksByHuman')
>>> soup = BeautifulSoup(html, 'lxml')
>>> links = soup.find_all('a')
>>> len(links)
23

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
Adoptivsohn Pflegevater / Pflegesohn Ehemann Partner Stiefvater /
Stiefsohn Bruder Vetter Onkel / Neffe Verwandter Sonstiger

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


>>> ses.show(households.RefundsByPerson, master_instance=obj)
========== ======== ==================== ===========
 Age        Gender   Person               Amount
---------- -------- -------------------- -----------
 46 years   Male     Paul FRISCH          20,00
 45 years   Female   Petra ZWEITH         20,00
 16 years   Male     Philippe FRISCH      10,00
 14 years   Female   Clara FRISCH         10,00
 12 years   Male     Dennis FRISCH        10,00
                     **Total (5 rows)**   **70,00**
========== ======== ==================== ===========
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
 45 years   Head of household   Not at charge    Mr Ludwig FRISCH     Ludwig       Frisch      1968-06-01   Male
 12 years   Child               At full charge   Mrs Melba FRISCH     Melba        Frisch      2002-04-05   Female
 6 years    Child               At full charge   Mrs Irma FRISCH      Irma         Frisch      2008-03-24   Female
========== =================== ================ ==================== ============ =========== ============ ========
<BLANKLINE>


Here is what Ludwig's LinksByHuman panel shows:

>>> ses.show(humanlinks.LinksByHuman, master_instance=obj)
Ludwig is
Father of `Irma <Detail>`__ (6 years)
Father of `Melba <Detail>`__ (12 years)
Husband of `Laura LOSLEVER <Detail>`__ (46 years)
Son of `Gaby FROGEMUTH <Detail>`__ (79 years)
Son of `Hubert <Detail>`__ (80 years)
<BLANKLINE>
Create relationship as **Father**/**Son** **Adoptive father**/**Adopted son** **Foster father**/**Foster son** **Husband** **Partner** **Stepfather**/**Stepson** **Brother** **Cousin** **Uncle**/**Nephew** **Relative** **Other**


Here is his :class:`RefundsByPerson` table:

>>> ses.show(households.RefundsByPerson, master_instance=obj)
========== ======== ==================== ===========
 Age        Gender   Person               Amount
---------- -------- -------------------- -----------
 46 years   Female   Laura LOSLEVER       20,00
 45 years   Male     Ludwig FRISCH        20,00
 12 years   Female   Melba FRISCH         10,00
 6 years    Female   Irma FRISCH          10,00
                     **Total (4 rows)**   **60,00**
========== ======== ==================== ===========
<BLANKLINE>

An edge case
============

The following edge case failed before 20170206:

>>> ses.show(humanlinks.LinksByHuman)
<BLANKLINE>


.. _welfare.specs.households.20190326:

Melba getting adult
===================

The :class:`RefundsByPerson` table depends on the current date, which is
2014-05-22 for this demo:

>>> dd.today()
datetime.date(2014, 5, 22)

The demo date is stored in a site attribute :attr:`the_demo_date
<lino.core.site.Site.the_demo_date>`:

>>> settings.SITE.the_demo_date
datetime.date(2014, 5, 22)

Let's have a look at Ludwig's :class:`RefundsByPerson` table when Melba gets
adult.  The default configuration says that you get adult at 18:

>>> dd.plugins.households.adult_age
18

In 2019 Melba is 17, still a child:

>>> settings.SITE.the_demo_date = datetime.date(2019, 5, 22)
>>> ses.show(households.RefundsByPerson, master_instance=obj)
========== ======== ==================== ===========
 Age        Gender   Person               Amount
---------- -------- -------------------- -----------
 51 years   Female   Laura LOSLEVER       20,00
 50 years   Male     Ludwig FRISCH        20,00
 17 years   Female   Melba FRISCH         10,00
 11 years   Female   Irma FRISCH          10,00
                     **Total (4 rows)**   **60,00**
========== ======== ==================== ===========
<BLANKLINE>

But in 2020 she is 18, now her refunded amount is that of an adult:

>>> settings.SITE.the_demo_date = datetime.date(2020, 5, 22)
>>> ses.show(households.RefundsByPerson, master_instance=obj)
========== ======== ==================== ===========
 Age        Gender   Person               Amount
---------- -------- -------------------- -----------
 52 years   Female   Laura LOSLEVER       20,00
 51 years   Male     Ludwig FRISCH        20,00
 18 years   Female   Melba FRISCH         20,00
 12 years   Female   Irma FRISCH          10,00
                     **Total (4 rows)**   **70,00**
========== ======== ==================== ===========
<BLANKLINE>

Note: Before 20190326 above table gave an amount of 10,00 for Melba because of
a bug (you got adult only one year after the age specified in
:attr:`lino_xl.lib.households.Plugin.adult_age`).

For the following tests we set :attr:`the_demo_date
<lino.core.site.Site.the_demo_date>` back to its original value:

>>> settings.SITE.the_demo_date = datetime.date(2014, 5, 22)



Inspecting the MembersByPerson panel
====================================

The following code caused an exception "ParameterStore of LayoutHandle
for ParamsLayout on pcsw.Clients expects a list of 12 values but got
16" on :blogref:`20140429`.

>>> print(pcsw.Client.objects.get(pk=179))
DUBOIS Robin (179)

>>> print(len(integ.Clients.params_layout.get_layout_handle()._store_fields))
16

>>> url = '/api/integ/Clients/179?'
>>> url += 'pv=30&pv=5&pv=&pv=29.04.2014&pv=29.04.2014&pv=&pv=&pv=&pv=&pv=&pv=false&pv=&pv=&pv=1&pv=false&pv=false'
>>> url += '&an=detail&rp=ext-comp-1351&fmt=json'
>>> res = test_client.get(url, REMOTE_USER='rolf')
>>> print(res.status_code)
200

The response to this AJAX request is in JSON:

>>> d = json.loads(res.content)

We test the MembersByPerson panel. It contains a summary:

>>> print(d['data']['households_MembersByPerson'])
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
<div>DUBOIS Robin (179) ist<ul><li><a href="javascript:Lino.households.Members.set_primary(...)...</div>

Since this is not very human-readable, we are going to analyze it with
`BeautifulSoup <http://beautiful-soup-4.readthedocs.org/en/latest>`_.

>>> soup = BeautifulSoup(d['data']['households_MembersByPerson'], 'lxml')

>>> print(soup.get_text(' ', strip=True))
... #doctest: +NORMALIZE_WHITESPACE +REPORT_CDIFF
DUBOIS Robin (179) ist ☐ Vorstand in Robin & Lisa Dubois-Lahm (Getrennt)
Bestehendem Haushalt beitreten oder einen neuen erstellen .

>>> links = soup.find_all('a')

It contains eight links:

>>> len(links)
4

The first link is the disabled checkbox for the :attr:`primary
<lino.modlib.households.models.Member.primary>` field:

>>> print(links[0].string)
... #doctest: +NORMALIZE_WHITESPACE
☐

Clicking on this would run the following JavaScript:

>>> print(links[0].get('href'))
javascript:Lino.households.Members.set_primary("ext-comp-1351",false,9,{  })

The next link is the name of the household, and clicking on it would
equally execute some Javascript code:

>>> print(links[1].string)
Robin & Lisa Dubois-Lahm (Getrennt)
>>> print(links[1].get('href'))
javascript:Lino.households.Households.detail.run("ext-comp-1351",{ "record_id": 236 })


The third link is:

>>> print(links[2].string)
Bestehendem Haushalt beitreten
>>> print(links[2].get('href'))
... #doctest: +NORMALIZE_WHITESPACE +ELLIPSIS
javascript:Lino.households.MembersByPerson.insert.run("ext-comp-1351",{ "base_params": { "person": 179 }, "data_record": { "data": { "disabled_fields": { "birth_date": true, "first_name": true, "gender": true, "last_name": true }, "household": null, "householdHidden": null, "person": "DUBOIS Robin (179)", "personHidden": 179, "primary": false, "role": "Kind", "roleHidden": "05" }, "phantom": true, "title": "Einf\u00fcgen in Mitgliedschaft in Haushalten" }, "param_values": { "aged_from": null, "aged_to": null, "end_date": null, "gender": null, "genderHidden": null, "start_date": null } })


The :func:`lino.api.doctest.get_json_soup` automates this trick:

>>> soup = get_json_soup('rolf', 'integ/Clients/179', 'households_MembersByPerson')
>>> links = soup.find_all('a')
>>> len(links)
4


The household summary
=====================

The utility function `get_household_summary
<lino_welfare.modlib.households.models.get_household_summary>`_ is
used for printing certain aid confirmations. Some examples:

>>> for cli in pcsw.Client.objects.order_by('id'):
...     s = households.get_household_summary(cli)
...     if not s.endswith("ist in keinem Haushalt"):
...         print(u"{} : {}".format(cli, s))
VANDENMEULENBOS Marie-Louise (174) : 2 Erwachsene
LAHM Lisa (176) : 2 Erwachsene
DUBOIS Robin (179) : 2 Erwachsene
DENON Denis (180*) : 1 Erwachsener und 1 Kind
JEANÉMART Jérôme (181) : 2 Erwachsene
KASENNOVA Tatjana (213) : 1 Erwachsener und 1 Kind
FRISCH Paul (240) : 2 Erwachsene und 3 Kinder
BRAUN Bruno (259) : BRAUN Bruno (259) ist in mehreren Haushalten zugleich





Member objects
==============

The following code snippet was used to reproduce :ticket:`844`:

>>> translation.activate('en')
>>> Member = households.Member
>>> print(Member())
Member object

>>> person = contacts.Person.objects.get(pk=259)
>>> print(Member(person=person))
Mr Bruno BRAUN (Child)

>>> print(Member(person=person, role=households.MemberRoles.head))
Mr Bruno BRAUN (Head of household)
