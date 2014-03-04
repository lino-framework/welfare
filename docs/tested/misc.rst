.. _welfare.tested.misc:

Miscellaneous
=============

.. include:: /include/tested.rst

Some tests:
  
>>> from __future__ import print_function
>>> from lino.runtime import *
>>> from django.utils import translation
>>> from django.test import Client
>>> import json



A web request
-------------


>>> client = Client()
>>> url = '/api/notes/NoteTypes/1?fmt=detail'
>>> res = client.get(url, REMOTE_USER='rolf')
>>> print(res.status_code)
200

We test whether a normal HTML response arrived:
>>> print(res.content)  #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
<!DOCTYPE html
...
Lino.notes.NoteTypes.detail.run(null,{ "record_id": "1", "base_params": {  } })
...
<BLANKLINE>
</body>
</html>



Some database content
---------------------


>>> ses = settings.SITE.login('rolf')
>>> with translation.override('de'):
...     ses.show(jobs.Jobs,column_names="name provider sector") #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
================= ====================================== ===========================
 Name              Stellenanbieter                        Sektor
----------------- -------------------------------------- ---------------------------
 Kellner           BISA (190*)                             Landwirtschaft & Garten
 Kellner           R-Cycle Sperrgutsortierzentrum (191)    Horeca
 Koch              R-Cycle Sperrgutsortierzentrum (191)    Seefahrt
 Koch              Pro Aktiv V.o.G. (193)                  Unterricht
 Küchenassistent   Pro Aktiv V.o.G. (193)                  Medizin & Paramedizin
 Küchenassistent   BISA (190*)                             Reinigung
 Tellerwäscher     BISA (190*)                             Bauwesen & Gebäudepflege
 Tellerwäscher     R-Cycle Sperrgutsortierzentrum (191)    Transport
================= ====================================== ===========================
<BLANKLINE>

JobsOverview
------------

Printing the document 
:ref:`welfare.jobs.JobsOverview`
caused a "NotImplementedError: <i> inside <text:p>" traceback 
when one of the jobs had a remark. 

>>> obj = ses.spawn(jobs.JobsOverview).create_instance()
>>> print(ses.run(obj.do_print)) 
... #doctest: +NORMALIZE_WHITESPACE
{'open_url': u'/media/webdav/userdocs/appyodt/jobs.JobsOverview.odt',
 'success': True}
 
Bug fixed :blogref:`20130423`.


Teams
-----

>>> with translation.override('de'):
...    ses.show(users.Teams) #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
==== ============================== ============================== ===================================================
 ID   Bezeichnung                    Bezeichnung (fr)               Bezeichnung (de)
---- ------------------------------ ------------------------------ ---------------------------------------------------
 1    GSS (General Social Service)   SSG (Service social général)   ASD (Allgemeiner Sozialdienst)
 2    Integration service            Service intégration            DSBE (Dienst für Sozial-Berufliche Eingliederung)
 3    Debts mediation                Médiation de dettes            Schuldnerberatung
==== ============================== ============================== ===================================================
<BLANKLINE>


>>> with translation.override('de'):
...    ses.show(pcsw.CoachingTypes)
============================== ============================== ===================================================
 Bezeichnung                    Bezeichnung (fr)               Bezeichnung (de)
------------------------------ ------------------------------ ---------------------------------------------------
 GSS (General Social Service)   SSG (Service social général)   ASD (Allgemeiner Sozialdienst)
 Integration service            Service intégration            DSBE (Dienst für Sozial-Berufliche Eingliederung)
 Debts mediation                Médiation de dettes            Schuldnerberatung
============================== ============================== ===================================================
<BLANKLINE>

