.. _welfare.tested.jobs:

===============
Jobs
===============

.. include:: /include/tested.rst

.. to test only this document:
  $ python setup.py test -s tests.DocsTests.test_jobs

..
    >>> from __future__ import print_function
    >>> import os
    >>> os.environ['DJANGO_SETTINGS_MODULE'] = \
    ...    'lino_welfare.projects.docs.settings.doctests'
    >>> from django.utils import translation
    >>> from lino.runtime import *
    >>> from lino.utils.instantiator import i2d
    >>> from django.test import Client
    >>> import json

We log in as Rolf:

>>> ses = rt.login('rolf')

We switch to German because the first :ref:`welfare` user was in Eupen:

>>> translation.activate('de')

Jobs
----

>>> with translation.override('de'):
...     ses.show(jobs.Jobs,column_names="function provider sector") #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
================= ====================================== ===========================
 Funktion          Stellenanbieter                        Sektor
----------------- -------------------------------------- ---------------------------
 Koch              R-Cycle Sperrgutsortierzentrum (197)    Seefahrt
 Koch              Pro Aktiv V.o.G. (199)                  Unterricht
 Küchenassistent   Pro Aktiv V.o.G. (199)                  Medizin & Paramedizin
 Küchenassistent   BISA (196)                              Reinigung
 Tellerwäscher     BISA (196)                              Bauwesen & Gebäudepflege
 Tellerwäscher     R-Cycle Sperrgutsortierzentrum (197)    Transport
 Kellner           BISA (196)                              Landwirtschaft & Garten
 Kellner           R-Cycle Sperrgutsortierzentrum (197)    Horeca
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
========== ========== ========================= ===================================== =============
 Anfang     Ende       Klient                    Firma                                 Land
---------- ---------- ------------------------- ------------------------------------- -------------
 07.02.11   07.02.11   JACOBS Jacqueline (137)   Belgisches Rotes Kreuz (100)          Estland
 04.04.11   04.04.11   FAYMONVILLE Luc (130*)    Beschützende Werkstätte Eupen (202)   Niederlande
========== ========== ========================= ===================================== =============
<BLANKLINE>


.. _welfare.jobs.CandidaturesByOffer:

Candidatures by Job Offer
-------------------------

This table shows the Candidatures which satisfy a given Job offer.

Example:

>>> obj = jobs.Offer.objects.get(pk=1)
>>> ses.show(jobs.CandidaturesByOffer.request(obj))
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
============== ========================== ======== ====================
 Anfragedatum   Klient                     Stelle   Kandidatur-Zustand
-------------- -------------------------- -------- --------------------
 02.05.14       JEANÉMART Jérôme (181)              Inaktiv
 27.06.14       GROTECLAES Gregory (132)            Arbeitet
============== ========================== ======== ====================
<BLANKLINE>


Evaluations of a contract
-------------------------

>>> translation.activate('en')
>>> obj = jobs.Contract.objects.get(pk=6)
>>> print(unicode(obj.client))
EVERS Eberhart (127)

>>> obj.active_period()
(datetime.date(2012, 11, 13), datetime.date(2014, 5, 12))

>>> obj.update_cal_rset()
ExamPolicy #3 (u'every 3 months')
>>> print(unicode(obj.update_cal_rset().event_type))
Internal meetings with client
>>> print(obj.update_cal_rset().event_type.max_conflicting)
4
>>> settings.SITE.verbose_client_info_message = True
>>> wanted = obj.get_wanted_auto_events(ses)
>>> [str(i.start_date) for i in wanted.values()]
['2013-02-13', '2013-05-13', '2013-08-13', '2013-11-13', '2014-02-13']
>>> print(ses.response['info_message'])
Generating events between 2013-02-13 and 2014-05-12.
Reached upper date limit 2014-05-12


>>> ses.show(cal.EventsByController.request(obj),
... column_names="linked_date summary")
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
====================== ===============
 When                   Summary
---------------------- ---------------
 Wed 2/13/13 (09:00)    Appointment 1
 Mon 5/13/13 (09:00)    Appointment 2
 Tue 8/13/13 (09:00)    Appointment 3
 Wed 11/13/13 (09:00)   Appointment 4
 Thu 2/13/14 (09:00)    Appointment 5
====================== ===============
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
EventType #2 (u'Internal meetings with client')
>>> e.event_type.max_conflicting
4

JobsOverview
------------

Printing the document 
:class:`welfare.jobs.JobsOverview`
caused a "NotImplementedError: <i> inside <text:p>" traceback 
when one of the jobs had a remark. 

>>> obj = ses.spawn(jobs.JobsOverview).create_instance()
>>> rv = ses.run(obj.do_print)
>>> print(rv['success'])
True
>>> print(rv['open_url'])
... #doctest: +NORMALIZE_WHITESPACE +ELLIPSIS
/.../jobs.JobsOverview.odt

This bug was fixed :blogref:`20130423`.
Note: the ``webdav/`` is only there when :attr:`ad.Site.use_java` is `True`.

