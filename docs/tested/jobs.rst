.. _welfare.tested.jobs:

Jobs
===============

.. include:: /include/tested.rst

.. to test only this document:
  $ python setup.py test -s tests.DocsTests.test_jobs

..
    >>> # -*- coding: UTF-8 -*-
    >>> from __future__ import print_function
    >>> import os
    >>> os.environ['DJANGO_SETTINGS_MODULE'] = 'lino_welfare.projects.docs.settings.test'
    >>> from django.utils import translation
    >>> from lino.runtime import *
    >>> from django.test import Client
    >>> import json

We log in as Rolf:

>>> ses = settings.SITE.login('rolf')

We switch to German because the first PCSW with Lino was the one in Eupen:

>>> translation.activate('de')


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
========== ========== ========================= ================================================ =============
 begonnen   beendet    Klient                    Firma                                            Land
---------- ---------- ------------------------- ------------------------------------------------ -------------
 ...        ...        JACOBS Jacqueline (136)   Rumma & Ko OÜ (100)                              Estland
 ...        ...        FAYMONVILLE Luc (129)     Mutualité Chrétienne de Verviers - Eupen (232)   Niederlande
========== ========== ========================= ================================================ =============
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
 ...            JEANÉMART Jérôme (180*)             Aktiv
 ...            GROTECLAES Gregory (131)            Arbeitet
============== ========================== ======== ====================
<BLANKLINE>


>>> obj = jobs.Contract.objects.get(pk=12)
>>> obj.active_period()
(datetime.date(2013, 12, 13), datetime.date(2015, 12, 12))
>>> obj.update_cal_rset()
ExamPolicy #3 (u'alle 3 Monate')
>>> settings.SITE.verbose_client_info_message = True
>>> wanted = obj.get_wanted_auto_events(ses)
>>> [i.start_date.strftime('%Y-%m-%d') for i in wanted.values()]
['2014-06-16', '2014-09-16', '2014-12-16', '2015-03-16', '2015-06-16', '2015-09-16']
>>> print(ses.response['info_message'])
Reached upper date limit 2015-12-12
>>> ses.show(cal.EventsByController.request(obj), column_names="when_text description")
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
========================== ================== ===========================================
 Wann                       Kurzbeschreibung   Arbeitsablauf
-------------------------- ------------------ -------------------------------------------
 2014 Juni 13 (Fr.) 09:00   Evaluation 2       **Vorgeschlagen** → [Notified] [Annehmen]
 2014 Sep. 13 (Sa.) 09:00   Evaluation 3       **Vorgeschlagen** → [Notified] [Annehmen]
 2014 Dez. 13 (Sa.) 09:00   Evaluation 4       **Vorgeschlagen** → [Notified] [Annehmen]
 2015 Mär. 13 (Fr.) 09:00   Evaluation 5       **Vorgeschlagen** → [Notified] [Annehmen]
 2015 Juni 13 (Sa.) 09:00   Evaluation 6       **Vorgeschlagen** → [Notified] [Annehmen]
 2015 Sep. 13 (So.) 09:00   Evaluation 7       **Vorgeschlagen** → [Notified] [Annehmen]
========================== ================== ===========================================
<BLANKLINE>
