.. _welfare.tested.jobs:

Jobs
===============

.. include:: /include/tested.rst

The following statements import some often-used global names::

>>> # -*- coding: UTF-8 -*-
>>> from __future__ import print_function
>>> import os
>>> os.environ['DJANGO_SETTINGS_MODULE'] = 'lino_welfare.settings.test'
>>> from django.utils import translation
>>> from lino.runtime import *
>>> from django.test import Client
>>> import json

We switch to German because the first PCSW with Lino was the one in Eupen:

>>> ses = settings.SITE.login('rolf')

We switch to German because the first PCSW with Lino was the one in Eupen:

>>> translation.activate('de')


.. _welfare.jobs.Offers:

Job Offers
----------


>>> # settings.SITE.catch_layout_exceptions = False
>>> jobs.Offers.show()
==== ========= ========== ======================== ================== ================ ============== =============
 ID   Sektor    Funktion   Name                     Stellenanbieter    Beginn Auswahl   Ende Auswahl   Beginndatum
---- --------- ---------- ------------------------ ------------------ ---------------- -------------- -------------
 1     Textil   Kellner    Übersetzer DE-FR (m/w)   Pro Aktiv V.o.G.   16.08.13                        15.09.13
==== ========= ========== ======================== ================== ================ ============== =============
<BLANKLINE>


.. _welfare.jobs.ExperiencesByOffer:

Experiences by Job Offer
------------------------

This table shows the Experiences which satisfy a given Job offer.

Example:

>>> obj = jobs.Offer.objects.get(pk=1)
>>> ses.show(jobs.ExperiencesByOffer.request(obj))
==== ========= ========== ==================== ========================== ============= ========= ========== ========== =============
 ID   Sektor    Funktion   Klient               Firma                      Bezeichnung   Land      begonnen   beendet    Bemerkungen
---- --------- ---------- -------------------- -------------------------- ------------- --------- ---------- ---------- -------------
 18    Textil   Kellner    BRECHT Bernd (176)   Werkstatt Cardijn V.o.G.                 Belgien   27.06.10   27.06.10
==== ========= ========== ==================== ========================== ============= ========= ========== ========== =============
<BLANKLINE>


.. _welfare.jobs.CandidaturesByOffer:

Candidatures by Job Offer
-------------------------

This table shows the Candidatures which satisfy a given Job offer.

Example:

>>> obj = jobs.Offer.objects.get(pk=1)
>>> ses.show(jobs.CandidaturesByOffer.request(obj))
==== ========= ========== ======================== ======== ============== =========== =======================
 ID   Sektor    Funktion   Klient                   Stelle   Anfragedatum   Bemerkung   Kandidatur-Zustand
---- --------- ---------- ------------------------ -------- -------------- ----------- -----------------------
 1     Textil   Kellner    DUBOIS Robin (178)                08.05.13                   Aktiv
 2     Textil   Kellner    EMONTS Daniel (127)               10.05.13                   Probezeit
 3     Textil   Kellner    EMONTS-GAST Erna (151)            12.05.13                   Probezeit ohne Erfolg
 4     Textil   Kellner    ENGELS Edgar (128)                14.05.13                   Arbeitet
==== ========= ========== ======================== ======== ============== =========== =======================
<BLANKLINE>


