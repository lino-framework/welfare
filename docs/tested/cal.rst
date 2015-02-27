.. _welfare.tested.cal:

===================
Calendar (tested)
===================

.. How to test only this document:

  $ python setup.py test -s tests.DocsTests.test_cal

A technical tour into the :mod:`lino_welfare.modlib.cal` module.

.. contents::
   :depth: 2

A tested document
=================

This document is part of the Lino Welfare test suite and has been
tested using doctest with the following initialization code:

>>> from __future__ import print_function
>>> import os
>>> os.environ['DJANGO_SETTINGS_MODULE'] = \
...    'lino_welfare.projects.eupen.settings.doctests'
>>> from lino.api.doctest import *



>>> rt.login('theresia').show(cal.EventsByDay, language='en')
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE -REPORT_UDIFF
============ ========================= ============ ================= ============= ================ ====== ===================================
 Start time   Client                    Summary      Managed by        Assigned to   Event Type       Room   Workflow
------------ ------------------------- ------------ ----------------- ------------- ---------------- ------ -----------------------------------
 08:30:00     AUSDEMWALD Alfons (116)   Diner        Alicia Allmanns                 Appointment             **Suggested** → [Notified] [Take]
 08:30:00     ENGELS Edgar (129)        Auswertung   Rolf Rompen                     Appointment             **Suggested** → [Notified] [Take]
 09:40:00                               Diner        Mélanie Mélard                  Calendar entry          **Suggested** → [Notified] [Take]
 10:20:00                               Treffen      Hubert Huppertz                 Calendar entry          **Suggested** → [Notified] [Take]
 10:20:00                               Lunch        Robin Rood                      Calendar entry          **Suggested** → [Notified] [Take]
 11:10:00                               Rencontre    Romain Raffault                 Calendar entry          **Suggested** → [Notified] [Take]
 13:30:00                               Auswertung   Judith Jousten                  Calendar entry          **Suggested** → [Notified] [Take]
 13:30:00                               Treffen      Theresia Thelen                 Calendar entry          **Suggested** → [Notified]
============ ========================= ============ ================= ============= ================ ====== ===================================
<BLANKLINE>

>>> rt.login('alicia').show(cal.MyEvents, language='en')
=========================== =========================== ================ ==================== =================================
 When                        Client                      Event Type       Summary              Workflow
--------------------------- --------------------------- ---------------- -------------------- ---------------------------------
 **May 22, 2014 at 08:30**   AUSDEMWALD Alfons (116)     Appointment      Diner                **Suggested** → [Notified]
 **May 23, 2014 at 09:40**                               Calendar entry   Souper               **Draft** → [Notified] [Cancel]
 **May 24, 2014 at 10:20**                               Calendar entry   Petit-déjeuner       **Took place** → [Reset]
 **May 24, 2014 at 11:10**                               Calendar entry   Rencontre            **Cancelled**
 **May 25, 2014 at 13:30**                               Calendar entry   Consultation         **Omitted**
 **May 26, 2014 at 08:30**   BASTIAENSEN Laurent (117)   Appointment      Séminaire            **Notified** → [Cancel] [Reset]
 **May 26, 2014 at 09:40**                               Calendar entry   Evaluation           **Suggested** → [Notified]
 **May 27, 2014 at 10:20**                               Calendar entry   Première rencontre   **Draft** → [Notified] [Cancel]
 **May 28, 2014 at 11:10**                               Calendar entry   Interview            **Took place** → [Reset]
 **May 28, 2014 at 13:30**                               Calendar entry   Diner                **Cancelled**
 **May 29, 2014 at 08:30**   COLLARD Charlotte (118)     Appointment      Souper               **Omitted**
 **May 30, 2014 at 09:40**                               Calendar entry   Petit-déjeuner       **Notified** → [Cancel] [Reset]
=========================== =========================== ================ ==================== =================================
<BLANKLINE>

These are Alicia's calendar entries of the last two months:

>>> last_week = dict(start_date=dd.today(-30), end_date=dd.today(-1))
>>> rt.login('alicia').show(cal.MyEvents, language='en',
...     param_values=last_week)
=========================== ========================= ============= ========== ============================
 When                        Client                    Event Type    Summary    Workflow
--------------------------- ------------------------- ------------- ---------- ----------------------------
 **May 7, 2014 at 09:00**    DUBOIS Robin (179)        Appointment   Termin 4   **Suggested** → [Notified]
 **May 14, 2014 at 09:00**   AUSDEMWALD Alfons (116)   Appointment   Termin 9   **Suggested** → [Notified]
=========================== ========================= ============= ========== ============================
<BLANKLINE>



>>> rt.login('hubert').show(cal.MyEvents, language='en')
=========================== ======================== ================ ============== =================================
 When                        Client                   Event Type       Summary        Workflow
--------------------------- ------------------------ ---------------- -------------- ---------------------------------
 **May 22, 2014 at 10:20**                            Calendar entry   Treffen        **Suggested** → [Notified]
 **May 23, 2014 at 11:10**                            Calendar entry   Beratung       **Draft** → [Notified] [Cancel]
 **May 24, 2014 at 08:30**   CHANTRAINE Marc (120*)   Appointment      Auswertung     **Cancelled**
 **May 24, 2014 at 13:30**                            Calendar entry   Seminar        **Took place** → [Reset]
 **May 25, 2014 at 09:40**                            Calendar entry   Erstgespräch   **Omitted**
 **May 26, 2014 at 10:20**                            Calendar entry   Interview      **Notified** → [Cancel] [Reset]
 **May 26, 2014 at 11:10**                            Calendar entry   Mittagessen    **Suggested** → [Notified]
 **May 27, 2014 at 13:30**                            Calendar entry   Abendessen     **Draft** → [Notified] [Cancel]
 **May 28, 2014 at 08:30**   DERICUM Daniel (121)     Appointment      Frühstück      **Took place** → [Reset]
 **May 28, 2014 at 09:40**                            Calendar entry   Treffen        **Cancelled**
 **May 29, 2014 at 10:20**                            Calendar entry   Beratung       **Omitted**
 **May 30, 2014 at 11:10**                            Calendar entry   Seminar        **Notified** → [Cancel] [Reset]
 **June 5, 2014 at 09:00**   EVERS Eberhart (127)     Appointment      Termin 9       **Suggested** → [Notified]
=========================== ======================== ================ ============== =================================
<BLANKLINE>

>>> rt.login('melanie').show(cal.MyEvents, language='en')
=========================== ==================== ================ ==================== =================================
 When                        Client               Event Type       Summary              Workflow
--------------------------- -------------------- ---------------- -------------------- ---------------------------------
 **May 22, 2014 at 09:40**                        Calendar entry   Diner                **Suggested** → [Notified]
 **May 23, 2014 at 10:20**                        Calendar entry   Souper               **Draft** → [Notified] [Cancel]
 **May 24, 2014 at 11:10**                        Calendar entry   Petit-déjeuner       **Took place** → [Reset]
 **May 24, 2014 at 13:30**                        Calendar entry   Rencontre            **Cancelled**
 **May 25, 2014 at 08:30**   ERNST Berta (125)    Appointment      Consultation         **Omitted**
 **May 26, 2014 at 09:00**   ENGELS Edgar (129)   Appointment      Termin 3             **Suggested** → [Notified]
 **May 26, 2014 at 09:00**   KAIVERS Karl (141)   Appointment      Termin 2             **Suggested** → [Notified]
 **May 26, 2014 at 09:40**                        Calendar entry   Séminaire            **Notified** → [Cancel] [Reset]
 **May 26, 2014 at 10:20**                        Calendar entry   Evaluation           **Suggested** → [Notified]
 **May 27, 2014 at 11:10**                        Calendar entry   Première rencontre   **Draft** → [Notified] [Cancel]
 **May 28, 2014 at 08:30**   EVERTZ Bernd (126)   Appointment      Diner                **Cancelled**
 **May 28, 2014 at 13:30**                        Calendar entry   Interview            **Took place** → [Reset]
 **May 29, 2014 at 09:40**                        Calendar entry   Souper               **Omitted**
 **May 30, 2014 at 10:20**                        Calendar entry   Petit-déjeuner       **Notified** → [Cancel] [Reset]
=========================== ==================== ================ ==================== =================================
<BLANKLINE>
