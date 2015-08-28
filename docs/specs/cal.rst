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
users.UserProfiles.admin:900 Verwalter




Events today
============

Here is what the :class:`lino.modlib.cal.ui.EventsByDay` table gives:

>>> rt.login('theresia').show(cal.EventsByDay, language='en', header_level=1)
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE -REPORT_UDIFF
========================
Thu 5/22/14 (22.05.2014)
========================
============ ======== ============ ================= ============= ===================== ====== ============================
 Start time   Client   Summary      Managed by        Assigned to   Calendar Event Type   Room   Workflow
------------ -------- ------------ ----------------- ------------- --------------------- ------ ----------------------------
 08:30:00              Diner        Alicia Allmanns                 Meeting                      **Suggested** → [Take]
 08:30:00              Auswertung   Rolf Rompen                     Meeting                      **Suggested** → [Take]
 09:40:00              Diner        Mélanie Mélard                  Meeting                      **Suggested** → [Take]
 10:20:00              Treffen      Hubert Huppertz                 Meeting                      **Suggested** → [Take]
 10:20:00              Lunch        Robin Rood                      Meeting                      **Suggested** → [Take]
 11:10:00              Rencontre    Romain Raffault                 Meeting                      **Suggested** → [Take]
 13:30:00              Auswertung   Judith Jousten                  Meeting                      **Suggested** → [Take]
 13:30:00              Treffen      Theresia Thelen                 Meeting                      **Suggested** → [Notified]
============ ======== ============ ================= ============= ===================== ====== ============================
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
======================== ========================= ===================== =========== ============================
 When                     Client                    Calendar Event Type   Summary     Workflow
------------------------ ------------------------- --------------------- ----------- ----------------------------
 *Wed 5/7/14 at 09:00*    DA VINCI David (165)      Appointment           Termin 15   **Suggested** → [Notified]
 *Tue 5/13/14 at 09:00*   HILGERS Hildegard (133)   Appointment           Termin 6    **Suggested** → [Notified]
======================== ========================= ===================== =========== ============================
<BLANKLINE>


These are Hubert's calendar entries of the last two months:

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
 *Wed 5/28/14 at 09:00*    BRECHT Bernd (177)        Appointment           Termin 15      **Suggested** → [Notified]
 *Wed 5/28/14 at 09:40*                              Internal meeting      Treffen        **Cancelled**
 *Thu 5/29/14 at 10:20*                              External meeting      Beratung       **Omitted**
 *Fri 5/30/14 at 11:10*                              Private               Seminar        **Notified** → [Cancel] [Reset]
 *Tue 6/3/14 at 09:00*     DENON Denis (180*)        Appointment           Termin 1       **Suggested** → [Notified]
 *Wed 6/4/14 at 09:00*     LAMBERTZ Guido (142)      Appointment           Termin 6       **Suggested** → [Notified]
 *Thu 6/19/14 at 09:00*    JEANÉMART Jérôme (181)    Appointment           Termin 15      **Suggested** → [Notified]
 *Mon 7/14/14 at 09:00*    BRECHT Bernd (177)        Appointment           Termin 1       **Suggested** → [Notified]
 *Mon 8/4/14 at 09:00*     JEANÉMART Jérôme (181)    Appointment           Termin 1       **Suggested** → [Notified]
 *Tue 8/5/14 at 09:00*     FAYMONVILLE Luc (130*)    Appointment           Termin 3       **Suggested** → [Notified]
 *Tue 8/12/14 at 09:00*    RADERMECKER Rik (173)     Appointment           Termin 2       **Suggested** → [Notified]
 *Thu 8/14/14 at 09:00*    BRECHT Bernd (177)        Appointment           Termin 2       **Suggested** → [Notified]
 *Wed 9/3/14 at 09:00*     DENON Denis (180*)        Appointment           Termin 2       **Suggested** → [Notified]
 *Thu 9/4/14 at 09:00*     LAMBERTZ Guido (142)      Appointment           Termin 7       **Suggested** → [Notified]
 *Thu 9/4/14 at 09:00*     JEANÉMART Jérôme (181)    Appointment           Termin 2       **Suggested** → [Notified]
 *Mon 9/15/14 at 09:00*    BRECHT Bernd (177)        Appointment           Termin 3       **Suggested** → [Notified]
 *Mon 10/6/14 at 09:00*    JEANÉMART Jérôme (181)    Appointment           Termin 3       **Suggested** → [Notified]
 *Wed 10/15/14 at 09:00*   BRECHT Bernd (177)        Appointment           Termin 4       **Suggested** → [Notified]
 *Thu 11/6/14 at 09:00*    JEANÉMART Jérôme (181)    Appointment           Termin 4       **Suggested** → [Notified]
 *Wed 11/12/14 at 09:00*   RADERMECKER Rik (173)     Appointment           Termin 3       **Suggested** → [Notified]
 *Mon 11/17/14 at 09:00*   BRECHT Bernd (177)        Appointment           Termin 5       **Suggested** → [Notified]
 *Wed 12/3/14 at 09:00*    DENON Denis (180*)        Appointment           Termin 3       **Suggested** → [Notified]
 *Mon 12/8/14 at 09:00*    JEANÉMART Jérôme (181)    Appointment           Termin 5       **Suggested** → [Notified]
 *Wed 12/17/14 at 09:00*   BRECHT Bernd (177)        Appointment           Termin 6       **Suggested** → [Notified]
 *Thu 1/8/15 at 09:00*     JEANÉMART Jérôme (181)    Appointment           Termin 6       **Suggested** → [Notified]
 *Mon 1/19/15 at 09:00*    BRECHT Bernd (177)        Appointment           Termin 7       **Suggested** → [Notified]
 *Mon 2/9/15 at 09:00*     JEANÉMART Jérôme (181)    Appointment           Termin 7       **Suggested** → [Notified]
 *Thu 2/19/15 at 09:00*    BRECHT Bernd (177)        Appointment           Termin 8       **Suggested** → [Notified]
 *Tue 3/3/15 at 09:00*     DENON Denis (180*)        Appointment           Termin 4       **Suggested** → [Notified]
 *Mon 3/9/15 at 09:00*     JEANÉMART Jérôme (181)    Appointment           Termin 8       **Suggested** → [Notified]
 *Thu 3/19/15 at 09:00*    BRECHT Bernd (177)        Appointment           Termin 9       **Suggested** → [Notified]
 *Thu 4/9/15 at 09:00*     JEANÉMART Jérôme (181)    Appointment           Termin 9       **Suggested** → [Notified]
 *Mon 4/20/15 at 09:00*    BRECHT Bernd (177)        Appointment           Termin 10      **Suggested** → [Notified]
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
 **Mon 11/19/12 (09:00)**   Alicia Allmanns   Termin 1         **Suggested**
 **Wed 12/19/12 (09:00)**   Alicia Allmanns   Termin 2         **Suggested**
 **Mon 1/21/13 (09:00)**    Alicia Allmanns   Termin 3         **Suggested**
 **Thu 2/21/13 (09:00)**    Alicia Allmanns   Termin 4         **Suggested**
 **Thu 3/21/13 (09:00)**    Alicia Allmanns   Termin 5         **Suggested**
 **Mon 4/22/13 (09:00)**    Alicia Allmanns   Termin 6         **Suggested**
 **Wed 5/22/13 (09:00)**    Alicia Allmanns   Termin 7         **Suggested**
 **Mon 6/24/13 (09:00)**    Alicia Allmanns   Termin 8         **Suggested**
 **Wed 7/24/13 (09:00)**    Alicia Allmanns   Termin 9         **Suggested**
 **Mon 8/26/13 (09:00)**    Alicia Allmanns   Termin 10        **Suggested**
 **Thu 9/26/13 (09:00)**    Alicia Allmanns   Termin 11        **Suggested**
 **Mon 10/28/13 (09:00)**   Caroline Carnol   Termin 12        **Suggested**
 **Thu 11/28/13 (09:00)**   Caroline Carnol   Termin 13        **Suggested**
 **Mon 12/30/13 (09:00)**   Caroline Carnol   Termin 14        **Suggested**
 **Thu 1/30/14 (09:00)**    Caroline Carnol   Termin 15        **Suggested**
 **Wed 3/12/14 (09:00)**    Caroline Carnol   Termin 1         **Suggested**
 **Tue 4/15/14 (09:00)**    Caroline Carnol   Termin 1         **Suggested**
 **Thu 5/15/14 (09:00)**    Caroline Carnol   Termin 2         **Suggested**
 **Thu 5/22/14**            Mélanie Mélard    Urgent problem   **Notified**
 **Fri 5/23/14 (09:40)**    Rolf Rompen       Erstgespräch     **Draft**
 **Mon 6/16/14 (09:00)**    Caroline Carnol   Termin 3         **Suggested**
 **Wed 7/16/14 (09:00)**    Caroline Carnol   Termin 4         **Suggested**
 **Mon 8/18/14 (09:00)**    Caroline Carnol   Termin 5         **Suggested**
 **Thu 9/18/14 (09:00)**    Caroline Carnol   Termin 6         **Suggested**
 **Mon 10/20/14 (09:00)**   Caroline Carnol   Termin 7         **Suggested**
 **Thu 11/20/14 (09:00)**   Caroline Carnol   Termin 8         **Suggested**
 **Mon 12/22/14 (09:00)**   Caroline Carnol   Termin 9         **Suggested**
========================== ================= ================ ===============
<BLANKLINE>