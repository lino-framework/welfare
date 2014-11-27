.. _welfare.tested.pcsw:

============
General PCSW
============

..
  This document is part of the test suite.
  To test only this document, run::
    $ python setup.py test -s tests.DocsTests.test_pcsw

.. include:: /include/tested.rst

..
    >>> from __future__ import print_function
    >>> import os
    >>> os.environ['DJANGO_SETTINGS_MODULE'] = \
    ...    'lino_welfare.projects.docs.settings.doctests'
    >>> from bs4 import BeautifulSoup
    >>> from lino.utils import i2d
    >>> from lino.utils.xmlgen.html import E
    >>> from lino.runtime import *
    >>> from django.test import Client
    >>> from django.utils import translation
    >>> import json
    >>> client = Client()


>>> ses = rt.login('robin')
>>> translation.activate('en')

Similar Persons
---------------

The test database contains some examples of accidental duplicate data
entry.

One fictive person exists 3 times:

- Dorothée Dobbelstein-Demeulenaere
- Dorothée Demeulenaere
- Dorothée Dobbelstein

Here we try to create a fourth one:

>>> obj = pcsw.Client(first_name=u"Dorothée", last_name="Dobbelstein")
>>> dedupe.SimilarPersons.get_words(obj)
set([u'Dobbelstein', u'Doroth\xe9e'])
>>> ses.show(dedupe.SimilarPersons, obj)
================================================= ==========
 Other                                             Workflow
------------------------------------------------- ----------
 **Mrs Dorothée DOBBELSTEIN (124)**
 **Mrs Dorothée DOBBELSTEIN-DEMEULENAERE (123)**
================================================= ==========
<BLANKLINE>

Note that *Mrs Dorothée Demeulenaere (122)* is missing. Our algorithm
detects only two of the existing three duplicates.


For the following tests we write a utility function:

>>> def check(first_name, last_name):
...     obj = pcsw.Client(first_name=first_name, last_name=last_name)
...     qs = ses.spawn(dedupe.SimilarPersons, master_instance=obj)
...     return [unicode(r) for r in qs.data_iterator]

This function returns the names of the persons that Lino would detect
as duplicates, depending on the given first_name and last_name.

>>> check("Bernard", "Bodard")
[u'Bernard BODARD (170*)']

Without our utility function the above test would be less readable:

>>> obj = pcsw.Client(first_name="Bernard", last_name="Bodard")
>>> ses.show(dedupe.SimilarPersons, obj)
=========================== ==========
 Other                       Workflow
--------------------------- ----------
 **Bernard BODARD (170*)**
=========================== ==========
<BLANKLINE>

Some users tend to mix up first and last name. Lino would detect that:

>>> check("Bodard", "Bernard")
[u'Bernard BODARD (170*)']

>>> check("Erna", "Odar")
[u'Bernard BODARD (170*)']

The following duplicates are **not yet** detected though they obviously
should. We are still experimenting...

>>> check("Bernard-Marie", "Bodard")
[]

>>> check("Marie", "Bernard-Bodard")
[]

The following duplicate is not detected because Lino doesn't yet use
phonetic algorithms:

>>> check("Bernhard", "Bodard")
[]


eID card summary
----------------

Here a test case (fixed :blogref:`20130827`) 
to test the new `eid_info` field:

>>> url = '/api/pcsw/Clients/177?an=detail&fmt=json'
>>> res = client.get(url, REMOTE_USER='rolf')
>>> print(res.status_code)
200
>>> result = json.loads(res.content)
>>> print(result.keys())
[u'navinfo', u'data', u'disable_delete', u'id', u'title']

>>> soup = BeautifulSoup(result['data']['overview'])
>>> print(soup.get_text("\n"))
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
Ansicht als
Partner
, 
Person
, Klient
Herr
Bernd 
Brecht
Deutschland
Adressen verwalten
Karte Nr. 591413288107 (Belgischer Staatsbürger), ausgestellt durch Eupen, gültig von 19.08.11 bis 19.08.16

>>> url = '/api/reception/Clients/116?an=detail&fmt=json'
>>> res = client.get(url, REMOTE_USER='rolf')
>>> result = json.loads(res.content)
>>> soup = BeautifulSoup(result['data']['overview'])
>>> print(soup.get_text("\n"))
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
Ansicht als
Partner
, 
Person
, Klient
Herr
Alfons 
Ausdemwald
Am Bahndamm
4700 Eupen
Adressen verwalten
Karte Nr. 123456789012 (C (Personalausweis für Ausländer)), ausgestellt durch Eupen
, gültig von 19.08.12 bis 18.08.13
Muss eID-Karte einlesen!


Coaching types
--------------

>>> with translation.override('de'):
...    ses.show(pcsw.CoachingTypes)
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
============================== ============================== =================================================== ======= ======= =====================
 Bezeichnung                    Bezeichnung (fr)               Bezeichnung (de)                                    DSBE    GSS     Role in evaluations
------------------------------ ------------------------------ --------------------------------------------------- ------- ------- ---------------------
 GSS (General Social Service)   SSG (Service social général)   ASD (Allgemeiner Sozialdienst)                      Nein    Ja      Colleague
 Integration service            Service intégration            DSBE (Dienst für Sozial-Berufliche Eingliederung)   Ja      Nein    Colleague
 Debts mediation                Médiation de dettes            Schuldnerberatung                                   Nein    Nein
 **Total (3 Zeilen)**                                                                                              **1**   **1**
============================== ============================== =================================================== ======= ======= =====================
<BLANKLINE>



.. _welfare.clients.parameters:

Filtering clients
-----------------

The demo database contains at least one client 
- whose client_state is "Coached"
- who has several coachings
- at least one of these coachings has been ended.

For example, let's log in as Mélanie and look at client Robin DUBOIS:

>>> ses = rt.login('melanie')
>>> pk = 179
>>> obj = pcsw.Client.objects.get(pk=pk)
>>> print(obj)
DUBOIS Robin (179)

Robin is coached:

>>> obj.client_state
<ClientStates.coached:30>

Here are Robin's coachings. Note that Mélanie stopped to coach Robin
on 08.03.2013:

>>> ses.show(pcsw.CoachingsByClient, master_instance=obj, column_names="start_date end_date user primary")
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
====================== ========== ================= ========
 Begleitet seit         bis        Begleiter         Primär 
---------------------- ---------- ----------------- --------
  03.03.12                          Hubert Huppertz   Nein
  13.03.12               08.03.13   Mélanie Mélard    Nein
  08.03.13               24.10.13   Alicia Allmanns   Nein
  24.10.13                          Hubert Huppertz   Ja
  **Total (4 Zeilen)**                                **1**
====================== ========== ================= ========
<BLANKLINE>

Another client is Dorothée Dobbelstein who is coached by three
different agents at the same time:

>>> obj = pcsw.Client.objects.get(pk=124)
>>> obj
Client #124 (u'DOBBELSTEIN Doroth\xe9e (124)')
>>> ses.show(pcsw.CoachingsByClient, master_instance=obj, column_names="start_date end_date user primary")
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
====================== ===== ================= ========
 Begleitet seit         bis   Begleiter         Primär
---------------------- ----- ----------------- --------
 24.10.13                     Mélanie Mélard    Ja
 13.12.13                     Caroline Carnol   Nein
 02.04.14                     Hubert Huppertz   Nein
 **Total (3 Zeilen)**                           **1**
====================== ===== ================= ========
<BLANKLINE>

A third client is David DA VINCI:

>>> obj = pcsw.Client.objects.get(pk=165)
>>> print(obj)
DA VINCI David (165)
>>> ses.show(pcsw.CoachingsByClient, master_instance=obj, column_names="start_date end_date user primary")
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
====================== ========== ================= ========
 Begleitet seit         bis        Begleiter         Primär
---------------------- ---------- ----------------- --------
 03.03.12                          Hubert Huppertz   Ja
 08.03.13               04.10.13   Mélanie Mélard    Nein
 04.10.13                          Alicia Allmanns   Nein
 **Total (3 Zeilen)**                                **1**
====================== ========== ================= ========
<BLANKLINE>


When Mélanie opens her :menuselection:`Integration --> Clients` list,
then she sees the following clients (Dorothée is there, but Robin
isn't):

>>> ses.show(integ.Clients, column_names="name_column")
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE -REPORT_UDIFF
=============================
 Name
-----------------------------
 BRECHT Bernd (177)
 DOBBELSTEIN Dorothée (124)
 EMONTS Daniel (128)
 ENGELS Edgar (129)
 EVERS Eberhart (127)
 HILGERS Hildegard (133)
 JACOBS Jacqueline (137)
 JEANÉMART Jérôme (181)
 KAIVERS Karl (141)
 LAMBERTZ Guido (142)
 LAZARUS Line (144)
 MEESSEN Melissa (147)
 RADERMACHER Alfons (153)
 RADERMACHER Christian (155)
 RADERMACHER Edgard (157)
 RADERMACHER Guido (159)
 RADERMECKER Rik (173)
 VAN VEEN Vincent (166)
=============================
<BLANKLINE>

Here is a list of Mélanies clients on 2013-04-01.  We get it by
manually filling that date into the
:attr:`welfare.pcsw.Clients.end_date` parameter field.  Note that

- Dorothée is **not** included since Mélanie started coaching her only
  2014-04-02
- David **is** included since Mélanie started coaching him already
  2012-03-03

>>> pv = dict(end_date=i2d(20130401))
>>> ses.show(integ.Clients, column_names="name_column", param_values=pv)
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE -REPORT_UDIFF
=========================
 Name
-------------------------
 AUSDEMWALD Alfons (116)
 ENGELS Edgar (129)
 JONAS Josef (139)
 LAMBERTZ Guido (142)
 RADERMACHER Guido (159)
 DA VINCI David (165)
=========================
<BLANKLINE>

