.. _welfare.tested.cal:

===================
Calendar (tested)
===================

.. How to test only this document:
   $ python setup.py test -s tests.DocsTests.test_cal

A technical tour into the :mod:`lino_welfare.modlib.cal` module.

.. contents::
   :local:

.. include:: /include/tested.rst

>>> from __future__ import print_function
>>> import os
>>> os.environ['DJANGO_SETTINGS_MODULE'] = \
...    'lino_welfare.projects.eupen.settings.doctests'
>>> from lino.api.doctest import *

Not for everybody
=================

Only users with the :class:`OfficeUser
<lino.modlib.office.roles.OfficeUser>` role can see the calendar
functionality.  All users with one of the following profiles can see
each other's calendars:

>>> from lino.modlib.office.roles import OfficeUser
>>> for p in users.UserProfiles.items():
...     if isinstance(p.role, OfficeUser):
...         print repr(p), unicode(p)
users.UserProfiles:100 Begleiter im DSBE
users.UserProfiles:110 Integrations-Assistent (Manager)
users.UserProfiles:200 Berater Erstempfang
users.UserProfiles:300 Schuldenberater
users.UserProfiles:400 Sozi
users.UserProfiles:410 Social agent (Manager)
users.UserProfiles.admin:900 Verwalter





Events today
============

Here is what the :class:`lino.modlib.cal.ui.EventsByDay` table gives:

>>> rt.login('theresia').show(cal.EventsByDay, language='en')
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE -REPORT_UDIFF
============ ======== ============ ================= ============= ===================== ====== ===================================
 Start time   Client   Summary      Managed by        Assigned to   Calendar Event Type   Room   Workflow
------------ -------- ------------ ----------------- ------------- --------------------- ------ -----------------------------------
 08:30:00              Diner        Alicia Allmanns                 Meeting                      **Suggested** → [Notified] [Take]
 08:30:00              Auswertung   Rolf Rompen                     Meeting                      **Suggested** → [Notified] [Take]
 09:40:00              Diner        Mélanie Mélard                  Meeting                      **Suggested** → [Notified] [Take]
 10:20:00              Treffen      Hubert Huppertz                 Meeting                      **Suggested** → [Notified] [Take]
 10:20:00              Lunch        Robin Rood                      Meeting                      **Suggested** → [Notified] [Take]
 11:10:00              Rencontre    Romain Raffault                 Meeting                      **Suggested** → [Notified] [Take]
 13:30:00              Auswertung   Judith Jousten                  Meeting                      **Suggested** → [Notified] [Take]
 13:30:00              Treffen      Theresia Thelen                 Meeting                      **Suggested** → [Notified]
============ ======== ============ ================= ============= ===================== ====== ===================================
<BLANKLINE>

Users looking at their events
=============================

For Alicia, Hubert and Mélanie.

>>> rt.login('alicia').show(cal.MyEvents, language='en')
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE -REPORT_UDIFF
========================= =========================== ===================== ==================== =================================
 When                      Client                      Calendar Event Type   Summary              Workflow
------------------------- --------------------------- --------------------- -------------------- ---------------------------------
 *Thu 5/22/14 at 08:30*                                Meeting               Diner                **Suggested** → [Notified]
 *Fri 5/23/14 at 09:40*    AUSDEMWALD Alfons (116)     Appointment           Souper               **Draft** → [Notified] [Cancel]
 *Sat 5/24/14 at 10:20*                                External meeting      Petit-déjeuner       **Took place** → [Reset]
 *Sat 5/24/14 at 11:10*                                Internal meeting      Rencontre            **Cancelled**
 *Sun 5/25/14 at 13:30*                                External meeting      Consultation         **Omitted**
 *Mon 5/26/14 at 08:30*                                Private               Séminaire            **Notified** → [Cancel] [Reset]
 *Mon 5/26/14 at 09:40*                                Meeting               Evaluation           **Suggested** → [Notified]
 *Tue 5/27/14 at 10:20*    BASTIAENSEN Laurent (117)   Appointment           Première rencontre   **Draft** → [Notified] [Cancel]
 *Wed 5/28/14 at 11:10*                                External meeting      Interview            **Took place** → [Reset]
 *Wed 5/28/14 at 13:30*                                Internal meeting      Diner                **Cancelled**
 *Thu 5/29/14 at 08:30*                                External meeting      Souper               **Omitted**
 *Fri 5/30/14 at 09:40*                                Private               Petit-déjeuner       **Notified** → [Cancel] [Reset]
 ...
========================= =========================== ===================== ==================== =================================
<BLANKLINE>

These are Alicia's calendar entries of the last two months:

>>> last_week = dict(start_date=dd.today(-30), end_date=dd.today(-1))
>>> rt.login('alicia').show(cal.MyEvents, language='en',
...     param_values=last_week)
<BLANKLINE>
No data to display
<BLANKLINE>



>>> rt.login('hubert').show(cal.MyEvents, language='en')
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE -REPORT_UDIFF
========================= ========================= ===================== ============== =================================
 When                      Client                    Calendar Event Type   Summary        Workflow
------------------------- ------------------------- --------------------- -------------- ---------------------------------
 *Thu 5/22/14 at 10:20*                              Meeting               Treffen        **Suggested** → [Notified]
 *Fri 5/23/14 at 11:10*    COLLARD Charlotte (118)   Appointment           Beratung       **Draft** → [Notified] [Cancel]
 *Sat 5/24/14 at 08:30*                              Internal meeting      Auswertung     **Cancelled**
 *Sat 5/24/14 at 13:30*                              External meeting      Seminar        **Took place** → [Reset]
 *Sun 5/25/14 at 09:40*                              External meeting      Erstgespräch   **Omitted**
 *Mon 5/26/14 at 10:20*                              Private               Interview      **Notified** → [Cancel] [Reset]
 *Mon 5/26/14 at 11:10*                              Meeting               Mittagessen    **Suggested** → [Notified]
 *Tue 5/27/14 at 13:30*    CHANTRAINE Marc (120*)    Appointment           Abendessen     **Draft** → [Notified] [Cancel]
 *Wed 5/28/14 at 08:30*                              External meeting      Frühstück      **Took place** → [Reset]
 *Wed 5/28/14 at 09:40*                              Internal meeting      Treffen        **Cancelled**
 *Thu 5/29/14 at 10:20*                              External meeting      Beratung       **Omitted**
 *Fri 5/30/14 at 11:10*                              Private               Seminar        **Notified** → [Cancel] [Reset]
 *Tue 6/3/14 at 09:00*     DENON Denis (180*)        Appointment           Termin 1       **Suggested** → [Notified]
 ...
========================= ========================= ===================== ============== =================================
<BLANKLINE>


>>> rt.login('melanie').show(cal.MyEvents, language='en')
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE -REPORT_UDIFF
========================= ========================================= ===================== ==================== =================================
 When                      Client                                    Calendar Event Type   Summary              Workflow
------------------------- ----------------------------------------- --------------------- -------------------- ---------------------------------
 *Thu 5/22/14 at 09:40*                                              Meeting               Diner                **Suggested** → [Notified]
 *Fri 5/23/14 at 10:20*    DOBBELSTEIN-DEMEULENAERE Dorothée (123)   Appointment           Souper               **Draft** → [Notified] [Cancel]
 *Sat 5/24/14 at 11:10*                                              External meeting      Petit-déjeuner       **Took place** → [Reset]
 *Sat 5/24/14 at 13:30*                                              Internal meeting      Rencontre            **Cancelled**
 *Sun 5/25/14 at 08:30*                                              External meeting      Consultation         **Omitted**
 *Mon 5/26/14 at 09:00*    ENGELS Edgar (129)                        Appointment           Termin 3             **Suggested** → [Notified]
 *Mon 5/26/14 at 09:40*                                              Private               Séminaire            **Notified** → [Cancel] [Reset]
 *Mon 5/26/14 at 10:20*                                              Meeting               Evaluation           **Suggested** → [Notified]
 *Tue 5/27/14 at 11:10*    DOBBELSTEIN Dorothée (124)                Appointment           Première rencontre   **Draft** → [Notified] [Cancel]
 *Wed 5/28/14 at 08:30*                                              Internal meeting      Diner                **Cancelled**
 *Wed 5/28/14 at 13:30*                                              External meeting      Interview            **Took place** → [Reset]
 *Thu 5/29/14 at 09:40*                                              External meeting      Souper               **Omitted**
 *Fri 5/30/14 at 10:20*                                              Private               Petit-déjeuner       **Notified** → [Cancel] [Reset]
 ...
========================= ========================================= ===================== ==================== =================================
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

