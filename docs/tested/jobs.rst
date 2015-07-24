.. _welfare.tested.jobs:

===============
Jobs
===============

.. to test only this document:

    $ python setup.py test -s tests.DocsTests.test_jobs
    
    doctest initialization:
    
    >>> from __future__ import print_function
    >>> import os
    >>> os.environ['DJANGO_SETTINGS_MODULE'] = \
    ...    'lino_welfare.projects.eupen.settings.doctests'
    >>> from lino.api.doctest import *


A tested tour into :mod:`lino_welfare.modlib.jobs`.

.. contents::
   :local:
   :depth: 1


We log in as Rolf:

>>> ses = rt.login('rolf')

Jobs
====

The central concept added by this module is a table of **jobs**.

>>> with translation.override('de'):
...     ses.show(jobs.Jobs, column_names="function provider sector")
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
================= ================================ ==========================
 Funktion          Stellenanbieter                  Sektor
----------------- -------------------------------- --------------------------
 Kellner           BISA                             Landwirtschaft & Garten
 Kellner           R-Cycle Sperrgutsortierzentrum   Horeca
 Koch              R-Cycle Sperrgutsortierzentrum   Seefahrt
 Koch              Pro Aktiv V.o.G.                 Unterricht
 Küchenassistent   Pro Aktiv V.o.G.                 Medizin & Paramedizin
 Küchenassistent   BISA                             Reinigung
 Tellerwäscher     BISA                             Bauwesen & Gebäudepflege
 Tellerwäscher     R-Cycle Sperrgutsortierzentrum   Transport
================= ================================ ==========================
<BLANKLINE>


Job providers
=============

>>> ses.show(jobs.JobProviders)
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
================================ ============ ======== ========= ===== ===== =========
 Name                             Adresse      E-Mail   Telefon   GSM   ID    Sprache
-------------------------------- ------------ -------- --------- ----- ----- ---------
 BISA                             4700 Eupen                            196   fr
 Pro Aktiv V.o.G.                 4700 Eupen                            199   de
 R-Cycle Sperrgutsortierzentrum   4700 Eupen                            197   en
================================ ============ ======== ========= ===== ===== =========
<BLANKLINE>

.. _welfare.jobs.Offers:

Job Offers
==========


>>> # settings.SITE.catch_layout_exceptions = False
>>> ses.show(jobs.Offers)  #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
======================== ================== ========================= ========== ================ ============== =============
 Name                     Stellenanbieter    Sektor                    Funktion   Beginn Auswahl   Ende Auswahl   Beginndatum
------------------------ ------------------ ------------------------- ---------- ---------------- -------------- -------------
 Übersetzer DE-FR (m/w)   Pro Aktiv V.o.G.   Landwirtschaft & Garten   Kellner    22.01.14         02.05.14       01.06.14
======================== ================== ========================= ========== ================ ============== =============
<BLANKLINE>


.. _welfare.jobs.ExperiencesByOffer:

Experiences by Job Offer
------------------------

This table shows the Experiences which satisfy a given Job offer.

Example:

>>> obj = jobs.Offer.objects.get(pk=1)
>>> ses.show(jobs.ExperiencesByOffer, obj)
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
============ ========== ==================== =============================== ==========================
 Beginnt am   Enddatum   Klient               Firma                           Land
------------ ---------- -------------------- ------------------------------- --------------------------
 07.02.11     07.03.11   LAZARUS Line (144)   Belgisches Rotes Kreuz          Afghanistan
 04.04.11     04.04.13   JONAS Josef (139)    Beschützende Werkstätte Eupen   Britische Jungferninseln
============ ========== ==================== =============================== ==========================
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


Show all contracts
------------------

The demo database contains 16 job supplyment contracts:

>>> ses.show(jobs.Contracts)  #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
==== ================================================== ============== ============== ========================= ===========================
 ID   Stelle                                             Laufzeit von   Laufzeit bis   Verantwortlicher (DSBE)   Art
---- -------------------------------------------------- -------------- -------------- ------------------------- ---------------------------
 1    Kellner bei BISA                                   04.10.12       03.10.13       Alicia Allmanns           Sozialökonomie
 2    Kellner bei R-Cycle Sperrgutsortierzentrum         14.10.12       13.04.14       Alicia Allmanns           mit Rückerstattung Schule
 3    Koch bei R-Cycle Sperrgutsortierzentrum            03.11.12       02.11.13       Alicia Allmanns           Sozialökonomie - majoré
 4    Koch bei Pro Aktiv V.o.G.                          03.11.13       03.11.14       Hubert Huppertz           Sozialökonomie
 5    Küchenassistent bei Pro Aktiv V.o.G.               13.11.12       12.11.14       Alicia Allmanns           Stadt Eupen
 6    Küchenassistent bei BISA                           03.12.12       02.12.14       Alicia Allmanns           Sozialökonomie - majoré
 7    Tellerwäscher bei BISA                             13.12.12       12.12.13       Alicia Allmanns           mit Rückerstattung
 8    Tellerwäscher bei R-Cycle Sperrgutsortierzentrum   13.12.13       13.12.14       Mélanie Mélard            Stadt Eupen
 9    Kellner bei BISA                                   02.01.13       01.01.14       Alicia Allmanns           Sozialökonomie
 10   Kellner bei R-Cycle Sperrgutsortierzentrum         02.01.14       02.01.15       Mélanie Mélard            mit Rückerstattung Schule
 11   Koch bei R-Cycle Sperrgutsortierzentrum            12.01.13       11.01.15       Alicia Allmanns           Sozialökonomie - majoré
 12   Koch bei Pro Aktiv V.o.G.                          01.02.13       31.01.15       Alicia Allmanns           Sozialökonomie
 13   Küchenassistent bei Pro Aktiv V.o.G.               11.02.13       10.02.14       Mélanie Mélard            Stadt Eupen
 14   Küchenassistent bei BISA                           11.02.14       11.02.15       Hubert Huppertz           Sozialökonomie - majoré
 15   Tellerwäscher bei BISA                             03.03.13       02.03.14       Alicia Allmanns           mit Rückerstattung
 16   Tellerwäscher bei R-Cycle Sperrgutsortierzentrum   03.03.14       03.03.15       Hubert Huppertz           Stadt Eupen
==== ================================================== ============== ============== ========================= ===========================
<BLANKLINE>



Evaluations of a contract
-------------------------

>>> obj = jobs.Contract.objects.get(pk=6)
>>> print(unicode(obj.client))
LAMBERTZ Guido (142)

>>> obj.active_period()
(datetime.date(2012, 12, 3), datetime.date(2014, 12, 2))

>>> obj.update_cal_rset()
ExamPolicy #3 (u'alle 3 Monate')

>>> print(unicode(obj.update_cal_rset().event_type))
Termin
>>> print(obj.update_cal_rset().event_type.max_conflicting)
4
>>> settings.SITE.verbose_client_info_message = True
>>> wanted = obj.get_wanted_auto_events(ses)
>>> [str(i.start_date) for i in wanted.values()]
['2013-03-04', '2013-06-04', '2013-09-04', '2013-12-04', '2014-03-04', '2014-06-04', '2014-09-04']
>>> print(ses.response['info_message'])
Generating events between 2013-03-04 and 2014-12-02.
Reached upper date limit 2014-12-02


>>> ses.show(cal.EventsByController.request(obj),
... column_names="linked_date summary")
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
========================== ==================
 Wann                       Kurzbeschreibung
-------------------------- ------------------
 **Mo. 04.03.13 (09:00)**   Termin 1
 **Di. 04.06.13 (09:00)**   Termin 2
 **Mi. 04.09.13 (09:00)**   Termin 3
 **Mi. 04.12.13 (09:00)**   Termin 4
 **Di. 04.03.14 (09:00)**   Termin 5
 **Mi. 04.06.14 (09:00)**   Termin 6
 **Do. 04.09.14 (09:00)**   Termin 7
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

