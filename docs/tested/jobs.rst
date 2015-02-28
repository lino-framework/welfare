.. _welfare.tested.jobs:

===============
Jobs
===============

.. include:: /include/tested.rst

.. to test only this document:

  $ python setup.py test -s tests.DocsTests.test_jobs

About this document
===================

>>> from __future__ import print_function
>>> import os
>>> os.environ['DJANGO_SETTINGS_MODULE'] = \
...    'lino_welfare.projects.eupen.settings.doctests'
>>> from lino.api.doctest import *

We log in as Rolf:

>>> ses = rt.login('rolf')

Jobs
----

>>> with translation.override('de'):
...     ses.show(jobs.Jobs, column_names="function provider sector")
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
================= ====================================== ===========================
 Funktion          Stellenanbieter                        Sektor
----------------- -------------------------------------- ---------------------------
 Kellner           BISA (196)                              Landwirtschaft & Garten
 Kellner           R-Cycle Sperrgutsortierzentrum (197)    Horeca
 Koch              R-Cycle Sperrgutsortierzentrum (197)    Seefahrt
 Koch              Pro Aktiv V.o.G. (199)                  Unterricht
 Küchenassistent   Pro Aktiv V.o.G. (199)                  Medizin & Paramedizin
 Küchenassistent   BISA (196)                              Reinigung
 Tellerwäscher     BISA (196)                              Bauwesen & Gebäudepflege
 Tellerwäscher     R-Cycle Sperrgutsortierzentrum (197)    Transport
================= ====================================== ===========================
<BLANKLINE>


.. _welfare.jobs.Offers:

Job Offers
----------


>>> # settings.SITE.catch_layout_exceptions = False
>>> jobs.Offers.show() #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
==== ========================== ========== ======================== ======================== ================ ============== =============
 ID   Sektor                     Funktion   Name                     Stellenanbieter          Beginn Auswahl   Ende Auswahl   Beginndatum
---- -------------------------- ---------- ------------------------ ------------------------ ---------------- -------------- -------------
 1     Landwirtschaft & Garten   Kellner    Übersetzer DE-FR (m/w)   Pro Aktiv V.o.G. (...)   ...              ...            ...     
==== ========================== ========== ======================== ======================== ================ ============== =============
<BLANKLINE>


.. _welfare.jobs.ExperiencesByOffer:

Experiences by Job Offer
------------------------

This table shows the Experiences which satisfy a given Job offer.

Example:

>>> obj = jobs.Offer.objects.get(pk=1)
>>> ses.show(jobs.ExperiencesByOffer.request(obj)) #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
============ ========== ==================== ===================================== ==========================
 Beginnt am   Enddatum   Klient               Firma                                 Land
------------ ---------- -------------------- ------------------------------------- --------------------------
 07.02.11     07.02.11   LAZARUS Line (144)   Belgisches Rotes Kreuz (100)          Afghanistan
 04.04.11     04.04.11   JONAS Josef (139)    Beschützende Werkstätte Eupen (202)   Britische Jungferninseln
============ ========== ==================== ===================================== ==========================
<BLANKLINE>



.. _welfare.jobs.CandidaturesByOffer:

Candidatures by Job Offer
-------------------------

This table shows the Candidatures which satisfy a given Job offer.

Example:

>>> obj = jobs.Offer.objects.get(pk=1)
>>> ses.show(jobs.CandidaturesByOffer.request(obj))
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
============== ======================= ======== ====================
 Anfragedatum   Klient                  Stelle   Kandidatur-Zustand
-------------- ----------------------- -------- --------------------
 02.05.14       MALMENDIER Marc (146)            Inaktiv
 27.06.14       KAIVERS Karl (141)               Arbeitet
============== ======================= ======== ====================
<BLANKLINE>


Evaluations of a contract
-------------------------

>>> obj = jobs.Contract.objects.get(pk=6)
>>> print(unicode(obj.client))
HILGERS Hildegard (133)

>>> obj.active_period()
(datetime.date(2014, 5, 13), datetime.date(2015, 5, 13))

>>> obj.update_cal_rset()
ExamPolicy #3 (u'alle 3 Monate')

>>> print(unicode(obj.update_cal_rset().event_type))
Termin
>>> print(obj.update_cal_rset().event_type.max_conflicting)
4
>>> settings.SITE.verbose_client_info_message = True
>>> wanted = obj.get_wanted_auto_events(ses)
>>> [str(i.start_date) for i in wanted.values()]
['2014-08-13', '2014-11-13', '2015-02-13', '2015-05-13']
>>> print(ses.response['info_message'])
Generating events between 2014-08-13 and 2015-05-13.
Reached upper date limit 2015-05-13


>>> ses.show(cal.EventsByController.request(obj),
... column_names="linked_date summary")
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
========================== ==================
 Wann                       Kurzbeschreibung
-------------------------- ------------------
 **Mi. 13.08.14 (09:00)**   Termin 1
 **Do. 13.11.14 (09:00)**   Termin 2
 **Fr. 13.02.15 (09:00)**   Termin 3
 **Mi. 13.05.15 (09:00)**   Termin 4
========================== ==================
<BLANKLINE>


Mélanie has two appointments on 2014-09-15 (TODO: this test currently
fails because coaching stories have changed. Currently there's no
similar case in the demo data. See :ticket:`13`):

>>> d = i2d(20140915)
>>> pv = dict(start_date=d, end_date=d)
>>> ses.show(cal.EventsByDay.request(param_values=pv),
...     column_names="user summary project")
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +SKIP
================ =============== =========================
 Managed by       Summary         Client
---------------- --------------- -------------------------
 Mélanie Mélard   Appointment 3   FAYMONVILLE Luc (130*)
 Mélanie Mélard   Appointment 5   JACOBS Jacqueline (137)
================ =============== =========================
<BLANKLINE>

This is because the EventType of these automatically generated
evaluation appointments is configured to allow for up to 4
conflicting events:

>>> e = cal.EventsByDay.request(param_values=pv).data_iterator[0]
>>> e.event_type
EventType #3 (u'Termin')
>>> e.event_type.max_conflicting
4


JobsOverview
------------

Printing the document 
:class:`welfare.jobs.JobsOverview`
caused a "NotImplementedError: <i> inside <text:p>" traceback 
when one of the jobs had a remark. 

>>> settings.SITE.default_build_method = "appyodt"
>>> obj = ses.spawn(jobs.JobsOverview).create_instance()
>>> rv = ses.run(obj.do_print)
>>> print(rv['success'])
True
>>> print(rv['open_url'])
... #doctest: +NORMALIZE_WHITESPACE +ELLIPSIS
/.../jobs.JobsOverview.odt

This bug was fixed :blogref:`20130423`.
Note: the ``webdav/`` is only there when :attr:`ad.Site.use_java` is `True`.

