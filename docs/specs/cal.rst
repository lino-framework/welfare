.. _welfare.tested.cal:
.. _welfare.specs.cal:

===================
Calendar (tested)
===================

.. How to test only this document:

    $ python setup.py test -s tests.SpecsTests.test_cal
    
    doctest init:

    >>> from __future__ import print_function
    >>> import os
    >>> os.environ['DJANGO_SETTINGS_MODULE'] = \
    ...    'lino_welfare.projects.eupen.settings.doctests'
    >>> from lino.api.doctest import *

A technical tour into the :mod:`lino_welfare.modlib.cal` module.

.. contents::
   :local:


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
... #doctest: +NORMALIZE_WHITESPACE +REPORT_UDIFF
users.UserProfiles:100 Begleiter im DSBE
users.UserProfiles:110 Begleiter im DSBE (Manager)
users.UserProfiles:120 Begleiter im DSBE (+Erstempfang)
users.UserProfiles:200 Berater Erstempfang
users.UserProfiles:300 Schuldenberater
users.UserProfiles:400 Sozi
users.UserProfiles:410 Sozi (Manager)
users.UserProfiles:500 Buchhalter
users.UserProfiles:510 Accountant (Manager)
users.UserProfiles.admin:900 Verwalter




Events today
============

Here is what the :class:`lino.modlib.cal.ui.EventsByDay` table gives:

>>> rt.login('theresia').show(cal.EventsByDay, language='en', header_level=1)
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE -REPORT_UDIFF
========================
Thu 5/22/14 (22.05.2014)
========================
============ ====================== ============ ================= ============= ===================== ====== ============================
 Start time   Client                 Summary      Managed by        Assigned to   Calendar Event Type   Room   Workflow
------------ ---------------------- ------------ ----------------- ------------- --------------------- ------ ----------------------------
 08:30:00                            Diner        Alicia Allmanns                 Meeting                      **Suggested** → [Take]
 08:30:00                            Auswertung   Rolf Rompen                     Internal meeting             **Suggested** → [Take]
 09:40:00     EVERS Eberhart (127)   Diner        Mélanie Mélard                  Appointment                  **Suggested** → [Take]
 10:20:00                            Treffen      Hubert Huppertz                 External meeting             **Suggested** → [Take]
 10:20:00     JOHNEN Johann (138)    Lunch        Robin Rood                      Evaluation                   **Suggested** → [Take]
 11:10:00                            Rencontre    Romain Raffault                 Private                      **Suggested** → [Take]
 13:30:00                            Auswertung   Judith Jousten                  External meeting             **Suggested** → [Take]
 13:30:00                            Treffen      Theresia Thelen                 Meeting                      **Suggested** → [Notified]
============ ====================== ============ ================= ============= ===================== ====== ============================
<BLANKLINE>

Note how Theresia cannot [Take] her own event (because she has it
already), and how she set only her own event to [Notified].

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
 *Sat 5/24/14 at 10:20*    BASTIAENSEN Laurent (117)   Evaluation            Petit-déjeuner       **Took place** → [Reset]
 *Sat 5/24/14 at 11:10*                                External meeting      Rencontre            **Cancelled**
 *Sun 5/25/14 at 13:30*                                Internal meeting      Consultation         **Omitted**
 *Mon 5/26/14 at 08:30*                                External meeting      Séminaire            **Notified** → [Cancel] [Reset]
 *Mon 5/26/14 at 09:40*                                Private               Evaluation           **Suggested** → [Notified]
 *Tue 5/27/14 at 10:20*                                Meeting               Première rencontre   **Draft** → [Notified] [Cancel]
 *Wed 5/28/14 at 11:10*    COLLARD Charlotte (118)     Appointment           Interview            **Took place** → [Reset]
 *Wed 5/28/14 at 13:30*    CHANTRAINE Marc (120*)      Evaluation            Diner                **Cancelled**
 *Thu 5/29/14 at 08:30*                                External meeting      Souper               **Omitted**
 *Fri 5/30/14 at 09:40*                                Internal meeting      Petit-déjeuner       **Notified** → [Cancel] [Reset]
  ...
========================= =========================== ===================== ==================== =================================
<BLANKLINE>

These are Alicia's calendar entries of the last two months:

>>> last_week = dict(start_date=dd.today(-30), end_date=dd.today(-1))
>>> rt.login('alicia').show(cal.MyEvents, language='en',
...     param_values=last_week)
======================= ========================= ===================== =============== ============================
 When                    Client                    Calendar Event Type   Summary         Workflow
----------------------- ------------------------- --------------------- --------------- ----------------------------
 *Wed 5/7/14 at 09:00*   DA VINCI David (165)      Evaluation            Évaluation 15   **Suggested** → [Notified]
 *Tue 5/13/14*           HILGERS Hildegard (133)   Evaluation            Évaluation 6    **Suggested** → [Notified]
======================= ========================= ===================== =============== ============================
<BLANKLINE>


These are Hubert's calendar entries of the last two months:

>>> rt.login('hubert').show(cal.MyEvents, language='en')
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE -REPORT_UDIFF
========================= ========================================= ===================== =============== =================================
 When                      Client                                    Calendar Event Type   Summary         Workflow
------------------------- ----------------------------------------- --------------------- --------------- ---------------------------------
 *Thu 5/22/14 at 10:20*                                              External meeting      Treffen         **Suggested** → [Notified]
 *Fri 5/23/14 at 11:10*                                              Private               Beratung        **Draft** → [Notified] [Cancel]
 *Sat 5/24/14 at 08:30*    DERICUM Daniel (121)                      Appointment           Auswertung      **Cancelled**
 *Sat 5/24/14 at 13:30*                                              Meeting               Seminar         **Took place** → [Reset]
 *Sun 5/25/14 at 09:40*    DEMEULENAERE Dorothée (122)               Evaluation            Erstgespräch    **Omitted**
 *Mon 5/26/14 at 10:20*                                              External meeting      Interview       **Notified** → [Cancel] [Reset]
 *Mon 5/26/14 at 11:10*                                              Internal meeting      Mittagessen     **Suggested** → [Notified]
 *Tue 5/27/14 at 13:30*                                              External meeting      Abendessen      **Draft** → [Notified] [Cancel]
 *Wed 5/28/14 at 08:30*                                              Private               Frühstück       **Took place** → [Reset]
 *Wed 5/28/14 at 09:00*    BRECHT Bernd (177)                        Evaluation            Évaluation 15   **Suggested** → [Notified]
 *Wed 5/28/14 at 09:40*                                              Meeting               Treffen         **Cancelled**
 *Thu 5/29/14 at 10:20*    DOBBELSTEIN-DEMEULENAERE Dorothée (123)   Appointment           Beratung        **Omitted**
 *Fri 5/30/14 at 11:10*    DOBBELSTEIN Dorothée (124)                Evaluation            Seminar         **Notified** → [Cancel] [Reset]
 *Tue 6/3/14*              DENON Denis (180*)                        Evaluation            Auswertung 1    **Suggested** → [Notified]
 *Wed 6/4/14*              LAMBERTZ Guido (142)                      Evaluation            Évaluation 6    **Suggested** → [Notified]
 *Thu 6/19/14 at 09:00*    JEANÉMART Jérôme (181)                    Evaluation            Évaluation 15   **Suggested** → [Notified]
 *Mon 7/14/14 at 09:00*    BRECHT Bernd (177)                        Evaluation            Auswertung 1    **Suggested** → [Notified]
 *Mon 8/4/14 at 09:00*     JEANÉMART Jérôme (181)                    Evaluation            Auswertung 1    **Suggested** → [Notified]
 *Tue 8/5/14*              FAYMONVILLE Luc (130*)                    Evaluation            Auswertung 3    **Suggested** → [Notified]
 *Tue 8/12/14*             RADERMECKER Rik (173)                     Evaluation            Auswertung 2    **Suggested** → [Notified]
 *Thu 8/14/14 at 09:00*    BRECHT Bernd (177)                        Evaluation            Auswertung 2    **Suggested** → [Notified]
 *Wed 9/3/14*              DENON Denis (180*)                        Evaluation            Auswertung 2    **Suggested** → [Notified]
 *Thu 9/4/14*              LAMBERTZ Guido (142)                      Evaluation            Évaluation 7    **Suggested** → [Notified]
 *Thu 9/4/14 at 09:00*     JEANÉMART Jérôme (181)                    Evaluation            Auswertung 2    **Suggested** → [Notified]
 *Mon 9/15/14 at 09:00*    BRECHT Bernd (177)                        Evaluation            Auswertung 3    **Suggested** → [Notified]
 *Mon 10/6/14 at 09:00*    JEANÉMART Jérôme (181)                    Evaluation            Auswertung 3    **Suggested** → [Notified]
 *Wed 10/15/14 at 09:00*   BRECHT Bernd (177)                        Evaluation            Auswertung 4    **Suggested** → [Notified]
 *Thu 11/6/14 at 09:00*    JEANÉMART Jérôme (181)                    Evaluation            Auswertung 4    **Suggested** → [Notified]
 *Wed 11/12/14*            RADERMECKER Rik (173)                     Evaluation            Auswertung 3    **Suggested** → [Notified]
 *Mon 11/17/14 at 09:00*   BRECHT Bernd (177)                        Evaluation            Auswertung 5    **Suggested** → [Notified]
 *Wed 12/3/14*             DENON Denis (180*)                        Evaluation            Auswertung 3    **Suggested** → [Notified]
 *Mon 12/8/14 at 09:00*    JEANÉMART Jérôme (181)                    Evaluation            Auswertung 5    **Suggested** → [Notified]
 *Wed 12/17/14 at 09:00*   BRECHT Bernd (177)                        Evaluation            Auswertung 6    **Suggested** → [Notified]
 *Thu 1/8/15 at 09:00*     JEANÉMART Jérôme (181)                    Evaluation            Auswertung 6    **Suggested** → [Notified]
 *Mon 1/19/15 at 09:00*    BRECHT Bernd (177)                        Evaluation            Auswertung 7    **Suggested** → [Notified]
 *Mon 2/9/15 at 09:00*     JEANÉMART Jérôme (181)                    Evaluation            Auswertung 7    **Suggested** → [Notified]
 *Thu 2/19/15 at 09:00*    BRECHT Bernd (177)                        Evaluation            Auswertung 8    **Suggested** → [Notified]
 *Tue 3/3/15*              DENON Denis (180*)                        Evaluation            Auswertung 4    **Suggested** → [Notified]
 *Mon 3/9/15 at 09:00*     JEANÉMART Jérôme (181)                    Evaluation            Auswertung 8    **Suggested** → [Notified]
 *Thu 3/19/15 at 09:00*    BRECHT Bernd (177)                        Evaluation            Auswertung 9    **Suggested** → [Notified]
 *Thu 4/9/15 at 09:00*     JEANÉMART Jérôme (181)                    Evaluation            Auswertung 9    **Suggested** → [Notified]
 *Mon 4/20/15 at 09:00*    BRECHT Bernd (177)                        Evaluation            Auswertung 10   **Suggested** → [Notified]
========================= ========================================= ===================== =============== =================================
<BLANKLINE>


>>> rt.login('melanie').show(cal.MyEvents, language='en')
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE -REPORT_UDIFF
========================= ============================= ===================== ==================== =================================
 When                      Client                        Calendar Event Type   Summary              Workflow
------------------------- ----------------------------- --------------------- -------------------- ---------------------------------
 *Thu 5/22/14 at 09:40*    EVERS Eberhart (127)          Appointment           Diner                **Suggested** → [Notified]
 *Fri 5/23/14 at 10:20*    EMONTS Daniel (128)           Evaluation            Souper               **Draft** → [Notified] [Cancel]
 *Sat 5/24/14 at 11:10*                                  External meeting      Petit-déjeuner       **Took place** → [Reset]
 *Sat 5/24/14 at 13:30*                                  Internal meeting      Rencontre            **Cancelled**
 *Sun 5/25/14 at 08:30*                                  External meeting      Consultation         **Omitted**
 *Mon 5/26/14 at 09:00*    ENGELS Edgar (129)            Evaluation            Évaluation 3         **Suggested** → [Notified]
 *Mon 5/26/14 at 09:40*                                  Private               Séminaire            **Notified** → [Cancel] [Reset]
 *Mon 5/26/14 at 10:20*                                  Meeting               Evaluation           **Suggested** → [Notified]
 *Tue 5/27/14 at 11:10*    ENGELS Edgar (129)            Appointment           Première rencontre   **Draft** → [Notified] [Cancel]
 *Wed 5/28/14 at 08:30*                                  External meeting      Diner                **Cancelled**
 *Wed 5/28/14 at 13:30*    FAYMONVILLE Luc (130*)        Evaluation            Interview            **Took place** → [Reset]
 *Thu 5/29/14 at 09:40*                                  Internal meeting      Souper               **Omitted**
 *Fri 5/30/14 at 10:20*                                  External meeting      Petit-déjeuner       **Notified** → [Cancel] [Reset]
 *Thu 6/5/14 at 09:00*     LAZARUS Line (144)            Evaluation            Évaluation 2         **Suggested** → [Notified]
 ...
========================= ============================= ===================== ==================== =================================
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


Events by client
================

This table is special in that it shows not only events directly
related to the client (i.e. :attr:`Event.project` pointing to it) but
also those where this client is among the guests.

>>> candidates = set()
>>> for obj in cal.Guest.objects.all():
...     if obj.partner and obj.partner_id != obj.event.project_id:
...         #print obj, obj.event.project_id, obj.partner_id
...         candidates.add(obj.event.project_id)
>>> print sorted(candidates)
[116, 127, 129, 133, 144, 146, 147, 157, 159, 166, 168, 173, 177, 179, 181]


>>> obj = pcsw.Client.objects.get(pk=127)
>>> rt.show(cal.EventsByClient, obj, header_level=1, language="en")
==============================
Events of EVERS Eberhart (127)
==============================
========================== ================= ================ ===============
 When                       Managed by        Summary          Workflow
-------------------------- ----------------- ---------------- ---------------
 **Mon 11/19/12 (09:00)**   Alicia Allmanns   Évaluation 1     **Suggested**
 **Wed 12/19/12 (09:00)**   Alicia Allmanns   Évaluation 2     **Suggested**
 **Mon 1/21/13 (09:00)**    Alicia Allmanns   Évaluation 3     **Suggested**
 **Thu 2/21/13 (09:00)**    Alicia Allmanns   Évaluation 4     **Suggested**
 **Thu 3/21/13 (09:00)**    Alicia Allmanns   Évaluation 5     **Suggested**
 **Mon 4/22/13 (09:00)**    Alicia Allmanns   Évaluation 6     **Suggested**
 **Wed 5/22/13 (09:00)**    Alicia Allmanns   Évaluation 7     **Suggested**
 **Mon 6/24/13 (09:00)**    Alicia Allmanns   Évaluation 8     **Suggested**
 **Wed 7/24/13 (09:00)**    Alicia Allmanns   Évaluation 9     **Suggested**
 **Mon 8/26/13 (09:00)**    Alicia Allmanns   Évaluation 10    **Suggested**
 **Thu 9/26/13 (09:00)**    Alicia Allmanns   Évaluation 11    **Suggested**
 **Mon 10/28/13 (09:00)**   Caroline Carnol   Évaluation 12    **Suggested**
 **Thu 11/28/13 (09:00)**   Caroline Carnol   Évaluation 13    **Suggested**
 **Mon 12/30/13 (09:00)**   Caroline Carnol   Évaluation 14    **Suggested**
 **Thu 1/30/14 (09:00)**    Caroline Carnol   Évaluation 15    **Suggested**
 **Wed 3/12/14 (09:00)**    Caroline Carnol   Auswertung 1     **Suggested**
 **Tue 4/15/14 (09:00)**    Caroline Carnol   Auswertung 1     **Suggested**
 **Thu 5/15/14 (09:00)**    Caroline Carnol   Auswertung 2     **Suggested**
 **Thu 5/22/14**            Mélanie Mélard    Urgent problem   **Notified**
 **Thu 5/22/14 (09:40)**    Mélanie Mélard    Diner            **Suggested**
 **Mon 6/16/14 (09:00)**    Caroline Carnol   Auswertung 3     **Suggested**
 **Wed 7/16/14 (09:00)**    Caroline Carnol   Auswertung 4     **Suggested**
 **Mon 8/18/14 (09:00)**    Caroline Carnol   Auswertung 5     **Suggested**
 **Thu 9/18/14 (09:00)**    Caroline Carnol   Auswertung 6     **Suggested**
 **Mon 10/20/14 (09:00)**   Caroline Carnol   Auswertung 7     **Suggested**
 **Thu 11/20/14 (09:00)**   Caroline Carnol   Auswertung 8     **Suggested**
 **Mon 12/22/14 (09:00)**   Caroline Carnol   Auswertung 9     **Suggested**
========================== ================= ================ ===============
<BLANKLINE>
