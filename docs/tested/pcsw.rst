.. _welfare.tested.pcsw:

..
  This document is part of the test suite.
  To test only this document, run::
    $ python setup.py test -s tests.DocsTests.test_pcsw

General PCSW
============

.. include:: /include/tested.rst

Some administrative stuff:

>>> from __future__ import print_function
>>> from lino.runtime import *
>>> from django.test import Client
>>> from django.utils import translation
>>> import json
>>> client = Client()

>>> ses = settings.SITE.login('robin')


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
 **Mrs Dorothée Dobbelstein (123)**
 **Mrs Dorothée Dobbelstein-Demeulenaere (122)**
================================================= ==========
<BLANKLINE>

Note that *Mrs Dorothée Demeulenaere (121)* is missing. Our algorithm
detects only two of the existing three duplicates.


For the following tests we write a utility function:

>>> def check(first_name, last_name):
...     obj = pcsw.Client(first_name=first_name, last_name=last_name)
...     qs = ses.spawn(dedupe.SimilarPersons, master_instance=obj)
...     return [unicode(r) for r in qs.data_iterator]

This function returns the names of the persons that Lino would detect
as duplicates, depending on the given first_name and last_name.

>>> check("Bernard", "Bodard")
[u'Bernard Bodard (169)']

Without our utility function the above test would be less readable:

>>> obj = pcsw.Client(first_name="Bernard", last_name="Bodard")
>>> ses.show(dedupe.SimilarPersons, obj)
========================== ==========
 Other                      Workflow
-------------------------- ----------
 **Bernard Bodard (169)**
========================== ==========
<BLANKLINE>

Some users tend to mix up first and last name. Lino would detect that:

>>> check("Bodard", "Bernard")
[u'Bernard Bodard (169)']

>>> check("Erna", "Odar")
[u'Bernard Bodard (169)']

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

UsersWithClients
----------------

>>> ses.show(integ.UsersWithClients)
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
==================== ============ =========== ======== ======= ========= ================= ================ ========
 Coach                Evaluation   Formation   Search   Work    Standby   Primary clients   Active clients   Total
-------------------- ------------ ----------- -------- ------- --------- ----------------- ---------------- --------
 Alicia Allmanns                   1                    1       1         2                 3                5
 Hubert Huppertz      3            2           3        4       4         11                16               23
 Mélanie Mélard       4            4           2        2       3         12                15               20
 **Total (3 rows)**   **7**        **7**       **5**    **7**   **8**     **25**            **34**           **48**
==================== ============ =========== ======== ======= ========= ================= ================ ========
<BLANKLINE>


Printing UsersWithClients to pdf
--------------------------------

User problem report:

  | pdf-Dokument aus Startseite erstellen:
  | kommt leider nur ein leeres Dok-pdf bei raus auf den 30/09/2011 datiert

The following lines reproduced this problem 
(and passed when it was fixed):

>>> url = 'http://127.0.0.1:8000/api/integ/UsersWithClients?an=as_pdf'
>>> res = client.get(url,REMOTE_USER='rolf')  #doctest: +SKIP
>>> print(res.status_code)  #doctest: +SKIP
200
>>> result = json.loads(res.content)  #doctest: +SKIP
>>> print(result)  #doctest: +SKIP
{u'open_url': u'/media/cache/appypdf/127.0.0.1/integ.UsersWithClients.pdf', u'success': True}



eID card summary
----------------

Here a test case (fixed :blogref:`20130827`) 
to test the new `eid_info` field:

>>> url = '/api/pcsw/Clients/176?an=detail&fmt=json'
>>> res = client.get(url,REMOTE_USER='rolf')
>>> print(res.status_code)
200
>>> result = json.loads(res.content)
>>> print(result.keys())
[u'navinfo', u'data', u'disable_delete', u'id', u'title']
>>> print(result['data']['client_info'][0])
<div><div style="font-size:18px;font-weigth:bold;vertical-align:bottom;text-align:middle">Herr<br />Bernd <b>Brecht</b><br />Deutschland</div><br /><div class="lino-info">Karte Nr. 591413288107 (Belgischer Staatsb&#252;rger), ausgestellt durch Eupen, g&#252;ltig von 19.08.11 bis 19.08.16</div></div>

>>> url = '/api/reception/Clients/115?an=detail&fmt=json'
>>> res = client.get(url,REMOTE_USER='rolf')
>>> result = json.loads(res.content)
>>> "Muss eID-Karte einlesen" in result['data']['client_info'][0]
True


Coaching types
--------------

>>> with translation.override('de'):
...    ses.show(pcsw.CoachingTypes)
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
============================== ============================== ===================================================
 Bezeichnung                    Bezeichnung (fr)               Bezeichnung (de)
------------------------------ ------------------------------ ---------------------------------------------------
 GSS (General Social Service)   SSG (Service social général)   ASD (Allgemeiner Sozialdienst)
 Integration service            Service intégration            DSBE (Dienst für Sozial-Berufliche Eingliederung)
 Debts mediation                Médiation de dettes            Schuldnerberatung
============================== ============================== ===================================================
<BLANKLINE>

