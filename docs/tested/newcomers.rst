.. _welfare.tested.newcomers:

Newcomers
=============

.. include:: /include/tested.rst

.. to test only this document:
  $ python setup.py test -s tests.DocsTests.test_newcomers

..  
    >>> from __future__ import print_function
    >>> from lino.runtime import *
    >>> from django.utils import translation
    >>> from django.test import Client

>>> ses = settings.SITE.login('rolf')
>>> translation.activate('en')

>>> ses.show(jobs.Jobs,column_names="name provider sector") #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
================ ====================================== =============================
 Name             Job Provider                           Job Sector
---------------- -------------------------------------- -----------------------------
 Cook             R-Cycle Sperrgutsortierzentrum (226)   Maritime
 Cook             Pro Aktiv V.o.G. (228)                 Education
 Cook assistant   Pro Aktiv V.o.G. (228)                 Medical & paramedical
 Cook assistant   BISA (225)                             Cleaning
 Dishwasher       BISA (225)                             Construction & buildings
 Dishwasher       R-Cycle Sperrgutsortierzentrum (226)   Transport
 Waiter           BISA (225)                             Agriculture & horticulture
 Waiter           R-Cycle Sperrgutsortierzentrum (226)   Tourism
================ ====================================== =============================
<BLANKLINE>


>>> with translation.override('de'):
...    ses.show(pcsw.CoachingTypes)
============================== ============================== =================================================== ======= =======
 Bezeichnung                    Bezeichnung (fr)               Bezeichnung (de)                                    DSBE    GSS
------------------------------ ------------------------------ --------------------------------------------------- ------- -------
 GSS (General Social Service)   SSG (Service social général)   ASD (Allgemeiner Sozialdienst)                      Nein    Ja
 Integration service            Service intégration            DSBE (Dienst für Sozial-Berufliche Eingliederung)   Ja      Nein
 Debts mediation                Médiation de dettes            Schuldnerberatung                                   Nein    Nein
 **Total (3 Zeilen)**                                                                                              **1**   **1**
============================== ============================== =================================================== ======= =======
<BLANKLINE>

