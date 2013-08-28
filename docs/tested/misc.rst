.. _welfare.tested.misc:

Miscellaneous
=============

.. include:: /include/tested.rst

Some tests:
  
>>> from lino.runtime import *
>>> from django.utils import translation
>>> from pprint import pprint
>>> ses = settings.SITE.login('rolf')
>>> with translation.override('de'):
...     ses.show(jobs.Jobs,column_names="name provider sector") #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
================= ================================ ===========================
 Name              Stellenanbieter                  Sektor
----------------- -------------------------------- ---------------------------
 Kellner           BISA                              Landwirtschaft & Garten
 Kellner           R-Cycle Sperrgutsortierzentrum    Horeca
 Koch              R-Cycle Sperrgutsortierzentrum    Seefahrt
 Koch              Pro Aktiv V.o.G.                  Unterricht
 Küchenassistent   Pro Aktiv V.o.G.                  Medizin & Paramedizin
 Küchenassistent   BISA                              Reinigung
 Tellerwäscher     BISA                              Bauwesen & Gebäudepflege
 Tellerwäscher     R-Cycle Sperrgutsortierzentrum    Transport
================= ================================ ===========================
<BLANKLINE>

JobsOverview
------------

Printing the document 
:ref:`welfare.jobs.JobsOverview`
caused a "NotImplementedError: <i> inside <text:p>" traceback 
when one of the jobs had a remark. 

>>> obj = ses.spawn(jobs.JobsOverview).create_instance()
>>> pprint(ses.run(obj.do_print)) #doctest: +NORMALIZE_WHITESPACE
{'open_url': u'/media/userdocs/appyodt/jobs.JobsOverview.odt',
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
============================== ============================== =================================================== ====
 Bezeichnung                    Bezeichnung (fr)               Bezeichnung (de)                                    ID
------------------------------ ------------------------------ --------------------------------------------------- ----
 GSS (General Social Service)   SSG (Service social général)   ASD (Allgemeiner Sozialdienst)                      1
 Integration service            Service intégration            DSBE (Dienst für Sozial-Berufliche Eingliederung)   2
 Debts mediation                Médiation de dettes            Schuldnerberatung                                   3
============================== ============================== =================================================== ====
<BLANKLINE>


The following helped to discover a bug on :blogref:`20130421`. 
Symptom was that the `coming_reminders`
and
`missed_reminders`
virtual fields of :class:`lino.modlib.cal.models.Home` 
showed also events of other users.
For example, Rolf suddenly had more than 100 events 
(the exact count was 137 to 140 depending on the day of the month 
where the demo database has been generated)
instead of about 7:

>>> events = ses.spawn(cal.MyEvents,master_instance=ses.get_user())
>>> print events.master_instance
Rolf Rompen
>>> events.get_total_count() < 100
True

I first expected the
:meth:`lino.core.requests.BaseRequest.spawn` method to ignore the 
`master_instance` keyword, but could not reproduce any error.
Then I discovered that it is because MyEvents no longer inherits 
from ByUser and thus no longer automatically filters 
from master_instance. If I filter it myself, I get a reasonable
number of events:

>>> events = ses.spawn(cal.MyEvents,user=ses.get_user())
>>> print events.get_total_count()
10

Why MyEvents no longer inherits from ByUser? 
This is expected behaviour, not a bug: it's because 
in MyEvents the user should be able to switch to 
other user's MyEvents view by activating the parameter panel 
and selecting another iser.
