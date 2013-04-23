.. _welfare.tested.misc:

Miscellaneous
=============

.. include:: /include/tested.rst

Some tests:
  
>>> from lino.runtime import *
>>> from pprint import pprint
>>> ses = settings.SITE.login('rolf')
>>> ses.set_language('de')
>>> ses.show(jobs.Jobs,column_names="name provider sector") #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
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

Printing the document :ref:`welfare.jobs.NewJobsOverview`
caused a "NotImplementedError: <i> inside <text:p>" traceback 
when one of the jobs had a remark. 

>>> obj = ses.spawn(jobs.NewJobsOverview).create_instance()
>>> pprint(ses.run(obj.do_print)) #doctest: +NORMALIZE_WHITESPACE
{'open_url': u'/media/userdocs/appyodt/jobs.NewJobsOverview.odt',
 'success': True}
 
Bug fixed :blogref:`20130423`.


Teams
-----

>>> ses.show(users.Teams) #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
==== =================================================== ============================== ===============================
 ID   Bezeichnung                                         Bezeichnung (fr)               Bezeichnung (nl)
---- --------------------------------------------------- ------------------------------ -------------------------------
 1    ASD (Allgemeiner Sozialdienst)                      SSG (Service social général)   ASD (Algemene Sociale Dienst)
 2    DSBE (Dienst für Sozial-Berufliche Eingliederung)   Service intégration
 3    Schuldnerberatung                                   Médiation de dettes
==== =================================================== ============================== ===============================
<BLANKLINE>


>>> ses.show(pcsw.CoachingTypes)
=================================================== ============================== =============================== ====
 Bezeichnung                                         Bezeichnung (fr)               Bezeichnung (nl)                ID
--------------------------------------------------- ------------------------------ ------------------------------- ----
 ASD (Allgemeiner Sozialdienst)                      SSG (Service social général)   ASD (Algemene Sociale Dienst)   1
 DSBE (Dienst für Sozial-Berufliche Eingliederung)   Service intégration                                            2
 Schuldnerberatung                                   Médiation de dettes                                            3
=================================================== ============================== =============================== ====
<BLANKLINE>


The following helped to discover a bug on :blogref:`20130421`. 
Symptom was that the `coming_reminders`
and
`missed_reminders`
virtual fields of :class:`lino.modlib.cal.models.Home` 
showed also events of other users.
For example, Rolf suddenly had 137 events:

>>> events = ses.spawn(cal.MyEvents,master_instance=ses.get_user())
>>> print events.master_instance
Rolf Rompen
>>> print events.get_total_count()
137

This should be 7, not 137.

I first expected the
:meth:`lino.core.requests.BaseRequest.spawn` method to ignore the 
`master_instance` keyword, but could not reproduce any error.
Then I discovered that it is because MyEvents no longer inherits 
from ByUser and thus no longer automatically filters 
from master_instance. If I filter it myself, I get a reasonable
number of events:

>>> events = ses.spawn(cal.MyEvents,user=ses.get_user())
>>> print events.get_total_count()
12

Why MyEvents no longer inherits from ByUser? 
This is expected behaviour, not a bug: it's because 
in MyEvents the user should be able to switch to 
other user's MyEvents view by activating the parameter panel 
and selecting another iser.
