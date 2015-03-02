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
============ ======== ============ ================= ============= ================ ====== ===================================
 Start time   Client   Summary      Managed by        Assigned to   Event Type       Room   Workflow
------------ -------- ------------ ----------------- ------------- ---------------- ------ -----------------------------------
 08:30:00              Diner        Alicia Allmanns                 Calendar entry          **Suggested** → [Notified] [Take]
 08:30:00              Auswertung   Rolf Rompen                     Calendar entry          **Suggested** → [Notified] [Take]
 09:40:00              Diner        Mélanie Mélard                  Calendar entry          **Suggested** → [Notified] [Take]
 10:20:00              Treffen      Hubert Huppertz                 Calendar entry          **Suggested** → [Notified] [Take]
 10:20:00              Lunch        Robin Rood                      Calendar entry          **Suggested** → [Notified] [Take]
 11:10:00              Rencontre    Romain Raffault                 Calendar entry          **Suggested** → [Notified] [Take]
 13:30:00              Auswertung   Judith Jousten                  Calendar entry          **Suggested** → [Notified] [Take]
 13:30:00              Treffen      Theresia Thelen                 Calendar entry          **Suggested** → [Notified]
============ ======== ============ ================= ============= ================ ====== ===================================
<BLANKLINE>

>>> rt.login('alicia').show(cal.MyEvents, language='en')
=========================== =========================== ================ ==================== =================================
 When                        Client                      Event Type       Summary              Workflow
--------------------------- --------------------------- ---------------- -------------------- ---------------------------------
 **May 22, 2014 at 08:30**                               Calendar entry   Diner                **Suggested** → [Notified]
 **May 23, 2014 at 09:40**   AUSDEMWALD Alfons (116)     Appointment      Souper               **Draft** → [Notified] [Cancel]
 **May 24, 2014 at 10:20**                               Calendar entry   Petit-déjeuner       **Took place** → [Reset]
 **May 24, 2014 at 11:10**                               Calendar entry   Rencontre            **Cancelled**
 **May 25, 2014 at 13:30**                               Calendar entry   Consultation         **Omitted**
 **May 26, 2014 at 08:30**                               Calendar entry   Séminaire            **Notified** → [Cancel] [Reset]
 **May 26, 2014 at 09:40**                               Calendar entry   Evaluation           **Suggested** → [Notified]
 **May 27, 2014 at 10:20**   BASTIAENSEN Laurent (117)   Appointment      Première rencontre   **Draft** → [Notified] [Cancel]
 **May 28, 2014 at 11:10**                               Calendar entry   Interview            **Took place** → [Reset]
 **May 28, 2014 at 13:30**                               Calendar entry   Diner                **Cancelled**
 **May 29, 2014 at 08:30**                               Calendar entry   Souper               **Omitted**
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
=========================== ========================= ================ ============== =================================
 When                        Client                    Event Type       Summary        Workflow
--------------------------- ------------------------- ---------------- -------------- ---------------------------------
 **May 22, 2014 at 10:20**                             Calendar entry   Treffen        **Suggested** → [Notified]
 **May 23, 2014 at 11:10**   COLLARD Charlotte (118)   Appointment      Beratung       **Draft** → [Notified] [Cancel]
 **May 24, 2014 at 08:30**                             Calendar entry   Auswertung     **Cancelled**
 **May 24, 2014 at 13:30**                             Calendar entry   Seminar        **Took place** → [Reset]
 **May 25, 2014 at 09:40**                             Calendar entry   Erstgespräch   **Omitted**
 **May 26, 2014 at 10:20**                             Calendar entry   Interview      **Notified** → [Cancel] [Reset]
 **May 26, 2014 at 11:10**                             Calendar entry   Mittagessen    **Suggested** → [Notified]
 **May 27, 2014 at 13:30**   CHANTRAINE Marc (120*)    Appointment      Abendessen     **Draft** → [Notified] [Cancel]
 **May 28, 2014 at 08:30**                             Calendar entry   Frühstück      **Took place** → [Reset]
 **May 28, 2014 at 09:40**                             Calendar entry   Treffen        **Cancelled**
 **May 29, 2014 at 10:20**                             Calendar entry   Beratung       **Omitted**
 **May 30, 2014 at 11:10**                             Calendar entry   Seminar        **Notified** → [Cancel] [Reset]
 **June 5, 2014 at 09:00**   EVERS Eberhart (127)      Appointment      Termin 9       **Suggested** → [Notified]
=========================== ========================= ================ ============== =================================
<BLANKLINE>


>>> rt.login('melanie').show(cal.MyEvents, language='en')
=========================== ========================================= ================ ==================== =================================
 When                        Client                                    Event Type       Summary              Workflow
--------------------------- ----------------------------------------- ---------------- -------------------- ---------------------------------
 **May 22, 2014 at 09:40**                                             Calendar entry   Diner                **Suggested** → [Notified]
 **May 23, 2014 at 10:20**   DOBBELSTEIN-DEMEULENAERE Dorothée (123)   Appointment      Souper               **Draft** → [Notified] [Cancel]
 **May 24, 2014 at 11:10**                                             Calendar entry   Petit-déjeuner       **Took place** → [Reset]
 **May 24, 2014 at 13:30**                                             Calendar entry   Rencontre            **Cancelled**
 **May 25, 2014 at 08:30**                                             Calendar entry   Consultation         **Omitted**
 **May 26, 2014 at 09:00**   ENGELS Edgar (129)                        Appointment      Termin 3             **Suggested** → [Notified]
 **May 26, 2014 at 09:00**   KAIVERS Karl (141)                        Appointment      Termin 2             **Suggested** → [Notified]
 **May 26, 2014 at 09:40**                                             Calendar entry   Séminaire            **Notified** → [Cancel] [Reset]
 **May 26, 2014 at 10:20**                                             Calendar entry   Evaluation           **Suggested** → [Notified]
 **May 27, 2014 at 11:10**   DOBBELSTEIN Dorothée (124)                Appointment      Première rencontre   **Draft** → [Notified] [Cancel]
 **May 28, 2014 at 08:30**                                             Calendar entry   Diner                **Cancelled**
 **May 28, 2014 at 13:30**                                             Calendar entry   Interview            **Took place** → [Reset]
 **May 29, 2014 at 09:40**                                             Calendar entry   Souper               **Omitted**
 **May 30, 2014 at 10:20**                                             Calendar entry   Petit-déjeuner       **Notified** → [Cancel] [Reset]
=========================== ========================================= ================ ==================== =================================
<BLANKLINE>



Calendars and Subscriptions
===========================

A Calendar is a set of events that can be shown or hidden in the
Calendar Panel.

In Lino Welfare, we have one Calendar per User.  Or to be more
precise: 

- The :ddref:`users.User` model has a :ddref:`users.User.calendar`
  field.

- The calendar of an :ddref:`cal.Event` is indirectly defined by the
  Event's :ddref:`cal.Event.user` field.

Two users can share a common calendar.  This is possible when two
colleagues really work together when receiving visitors.

A Subscription is when a given user decides that she wants to see the
calendar of another user.

Every user is, by default, subscribed to her own calendar.
For example, demo user `rolf` is automatically subscribed to the
following calendars:

>>> ses = rt.login('rolf')
>>> with translation.override('de'):
...    ses.show(cal.SubscriptionsByUser, ses.get_user()) #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
==== ========== ===========
 ID   Kalender   versteckt
---- ---------- -----------
 7    rolf       Nein
==== ========== ===========
<BLANKLINE>

Each user who has view access to the calendar.
Only UserProfile with a non-empty `office_level` can see the calendar.
All users with one of the following profiles can see each other's calendars:

>>> print('\n'.join([unicode(p) for p in users.UserProfiles.items() if p.coaching_level]))
Begleiter im DSBE
Integrations-Assistent (Manager)
Berater Erstempfang
Schuldenberater
Sozi
Social agent (Manager)
Verwalter

