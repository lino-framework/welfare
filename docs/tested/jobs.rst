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
==== ========================== ========== ======================== ================== ================ ============== =============
 ID   Sektor                     Funktion   Name                     Stellenanbieter    Beginn Auswahl   Ende Auswahl   Beginndatum
---- -------------------------- ---------- ------------------------ ------------------ ---------------- -------------- -------------
 1     Landwirtschaft & Garten   Kellner    Übersetzer DE-FR (m/w)   Pro Aktiv V.o.G.   08.05.13         16.08.13       15.09.13
==== ========================== ========== ======================== ================== ================ ============== =============
<BLANKLINE>


.. _welfare.jobs.ExperiencesByOffer:

Experiences by Job Offer
------------------------

This table shows the Experiences which satisfy a given Job offer.

Example:

>>> obj = jobs.Offer.objects.get(pk=1)
>>> ses.show(jobs.ExperiencesByOffer.request(obj))
========== ========== ========================= ================= =============
 begonnen   beendet    Klient                    Firma             Land
---------- ---------- ------------------------- ----------------- -------------
 24.05.10   24.05.10   JACOBS Jacqueline (136)   Rumma & Ko OÜ     Estland
 19.07.10   19.07.10   FAYMONVILLE Luc (129)     Bosten-Bocken A   Niederlande
========== ========== ========================= ================= =============
<BLANKLINE>


.. _welfare.jobs.CandidaturesByOffer:

Candidatures by Job Offer
-------------------------

This table shows the Candidatures which satisfy a given Job offer.

Example:

>>> obj = jobs.Offer.objects.get(pk=1)
>>> ses.show(jobs.CandidaturesByOffer.request(obj))
============== ========================== ======== ====================
 Anfragedatum   Klient                     Stelle   Kandidatur-Zustand
-------------- -------------------------- -------- --------------------
 16.08.13       JEANÉMART Jérôme (180*)             Aktiv
 11.10.13       GROTECLAES Gregory (131)            Arbeitet
============== ========================== ======== ====================
<BLANKLINE>


