.. _welfare.tested.cal:
.. _welfare.specs.cal:

========
Calendar
========

.. How to test only this document:

    $ python setup.py test -s tests.SpecsTests.test_cal
    
    doctest init:

    >>> from lino import startup
    >>> startup('lino_welfare.projects.eupen.settings.doctests')
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
===========================
Thu 22/05/2014 (22.05.2014)
===========================
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

The **My events** table (:class:`lino_xl.lib.cal.ui.MyEvents`) shows
shows today's and all future appointments :attr:`show_appointments
<lino_xl.lib.cal.ui.Events.show_appointments>` of the user who
requests it.

Here is what it says for Alicia.

>>> rt.login('alicia').show(cal.MyEvents, language='en')
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE -REPORT_UDIFF
=========================== =========================== ===================== ==================== =================================
 When                        Client                      Calendar Event Type   Summary              Workflow
--------------------------- --------------------------- --------------------- -------------------- ---------------------------------
 *Thu 22/05/2014 at 08:30*                               Meeting               Diner                **Suggested** → [Notified]
 *Fri 23/05/2014 at 09:40*   AUSDEMWALD Alfons (116)     Appointment           Souper               **Draft** → [Notified] [Cancel]
 *Sat 24/05/2014 at 10:20*   BASTIAENSEN Laurent (117)   Evaluation            Petit-déjeuner       **Took place** → [Reset]
 *Sat 24/05/2014 at 11:10*                               External meeting      Rencontre            **Cancelled**
 *Sun 25/05/2014 at 13:30*                               Internal meeting      Consultation         **Omitted**
 *Mon 26/05/2014 at 08:30*                               External meeting      Séminaire            **Notified** → [Cancel] [Reset]
 *Mon 26/05/2014 at 09:40*                               Private               Evaluation           **Suggested** → [Notified]
 *Tue 27/05/2014 at 10:20*                               Meeting               Première rencontre   **Draft** → [Notified] [Cancel]
 *Wed 28/05/2014 at 11:10*   COLLARD Charlotte (118)     Appointment           Interview            **Took place** → [Reset]
 *Wed 28/05/2014 at 13:30*   CHANTRAINE Marc (120*)      Evaluation            Diner                **Cancelled**
 *Thu 29/05/2014 at 08:30*                               External meeting      Souper               **Omitted**
 *Fri 30/05/2014 at 09:40*                               Internal meeting      Petit-déjeuner       **Notified** → [Cancel] [Reset]
 *Mon 23/06/2014 at 09:00*   DA VINCI David (165)        Evaluation            Évaluation 1         **Suggested** → [Notified] [▽]
 *Mon 14/07/2014*            RADERMACHER Fritz (158)     Evaluation            Évaluation 6         **Suggested** → [Notified] [▽]
 *Wed 23/07/2014 at 09:00*   DA VINCI David (165)        Evaluation            Évaluation 2         **Suggested** → [Notified] [▽]
 *Thu 14/08/2014*            HILGERS Hildegard (133)     Evaluation            Évaluation 7         **Suggested** → [Notified] [▽]
 *Mon 25/08/2014 at 09:00*   DA VINCI David (165)        Evaluation            Évaluation 3         **Suggested** → [Notified] [▽]
 *Thu 25/09/2014 at 09:00*   DA VINCI David (165)        Evaluation            Évaluation 4         **Suggested** → [Notified] [▽]
 *Tue 14/10/2014*            RADERMACHER Fritz (158)     Evaluation            Évaluation 7         **Suggested** → [Notified] [▽]
 *Mon 27/10/2014 at 09:00*   DA VINCI David (165)        Evaluation            Évaluation 5         **Suggested** → [Notified] [▽]
 *Thu 27/11/2014 at 09:00*   DA VINCI David (165)        Evaluation            Évaluation 6         **Suggested** → [Notified] [▽]
 *Mon 29/12/2014 at 09:00*   DA VINCI David (165)        Evaluation            Évaluation 7         **Suggested** → [Notified] [▽]
 *Thu 29/01/2015 at 09:00*   DA VINCI David (165)        Evaluation            Évaluation 8         **Suggested** → [Notified] [▽]
 *Mon 02/03/2015 at 09:00*   DA VINCI David (165)        Evaluation            Évaluation 9         **Suggested** → [Notified] [▽]
=========================== =========================== ===================== ==================== =================================
<BLANKLINE>


These are for Hubert:

>>> rt.login('hubert').show(cal.MyEvents, language='en')
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE -REPORT_UDIFF
=========================== ========================================= ===================== =============== =================================
 When                        Client                                    Calendar Event Type   Summary         Workflow
--------------------------- ----------------------------------------- --------------------- --------------- ---------------------------------
 *Thu 22/05/2014 at 10:20*                                             External meeting      Treffen         **Suggested** → [Notified]
 *Fri 23/05/2014 at 11:10*                                             Private               Beratung        **Draft** → [Notified] [Cancel]
 *Sat 24/05/2014 at 08:30*   DERICUM Daniel (121)                      Appointment           Auswertung      **Cancelled**
 *Sat 24/05/2014 at 13:30*                                             Meeting               Seminar         **Took place** → [Reset]
 *Sun 25/05/2014 at 09:40*   DEMEULENAERE Dorothée (122)               Evaluation            Erstgespräch    **Omitted**
 *Mon 26/05/2014 at 10:20*                                             External meeting      Interview       **Notified** → [Cancel] [Reset]
 *Mon 26/05/2014 at 11:10*                                             Internal meeting      Mittagessen     **Suggested** → [Notified]
 *Tue 27/05/2014 at 13:30*                                             External meeting      Abendessen      **Draft** → [Notified] [Cancel]
 *Wed 28/05/2014 at 08:30*                                             Private               Frühstück       **Took place** → [Reset]
 *Wed 28/05/2014 at 09:00*   BRECHT Bernd (177)                        Evaluation            Évaluation 15   **Suggested** → [Notified] [▽]
 *Wed 28/05/2014 at 09:40*                                             Meeting               Treffen         **Cancelled**
 *Thu 29/05/2014 at 10:20*   DOBBELSTEIN-DEMEULENAERE Dorothée (123)   Appointment           Beratung        **Omitted**
 ...
 *Mon 09/03/2015 at 09:00*   JEANÉMART Jérôme (181)                    Evaluation            Auswertung 8    **Suggested** → [Notified] [▽]
 *Thu 19/03/2015 at 09:00*   BRECHT Bernd (177)                        Evaluation            Auswertung 9    **Suggested** → [Notified] [▽]
 *Thu 09/04/2015 at 09:00*   JEANÉMART Jérôme (181)                    Evaluation            Auswertung 9    **Suggested** → [Notified] [▽]
 *Mon 20/04/2015 at 09:00*   BRECHT Bernd (177)                        Evaluation            Auswertung 10   **Suggested** → [Notified] [▽]
=========================== ========================================= ===================== =============== =================================
<BLANKLINE>


And these for Mélanie:

>>> rt.login('melanie').show(cal.MyEvents, language='en')
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE -REPORT_UDIFF
=========================== ============================= ===================== ==================== =================================
 When                        Client                        Calendar Event Type   Summary              Workflow
--------------------------- ----------------------------- --------------------- -------------------- ---------------------------------
 *Thu 22/05/2014 at 09:40*   EVERS Eberhart (127)          Appointment           Diner                **Suggested** → [Notified]
 *Fri 23/05/2014 at 10:20*   EMONTS Daniel (128)           Evaluation            Souper               **Draft** → [Notified] [Cancel]
 *Sat 24/05/2014 at 11:10*                                 External meeting      Petit-déjeuner       **Took place** → [Reset]
 *Sat 24/05/2014 at 13:30*                                 Internal meeting      Rencontre            **Cancelled**
 *Sun 25/05/2014 at 08:30*                                 External meeting      Consultation         **Omitted**
 *Mon 26/05/2014 at 09:00*   ENGELS Edgar (129)            Evaluation            Évaluation 3         **Suggested** → [Notified] [▽]
 *Mon 26/05/2014 at 09:40*                                 Private               Séminaire            **Notified** → [Cancel] [Reset]
 *Mon 26/05/2014 at 10:20*                                 Meeting               Evaluation           **Suggested** → [Notified]
 *Tue 27/05/2014 at 11:10*   ENGELS Edgar (129)            Appointment           Première rencontre   **Draft** → [Notified] [Cancel]
 *Wed 28/05/2014 at 08:30*                                 External meeting      Diner                **Cancelled**
 *Wed 28/05/2014 at 13:30*   FAYMONVILLE Luc (130*)        Evaluation            Interview            **Took place** → [Reset]
 *Thu 29/05/2014 at 09:40*                                 Internal meeting      Souper               **Omitted**
 ...
 *Thu 19/03/2015 at 09:00*   RADERMACHER Guido (159)       Evaluation            Évaluation 9         **Suggested** → [Notified] [▽]
 *Thu 02/04/2015 at 09:00*   DUBOIS Robin (179)            Evaluation            Évaluation 8         **Suggested** → [Notified] [▽]
 *Thu 09/04/2015 at 09:00*   ÖSTGES Otto (168)             Evaluation            Évaluation 9         **Suggested** → [Notified] [▽]
 *Mon 20/04/2015 at 09:00*   RADERMACHER Guido (159)       Evaluation            Évaluation 10        **Suggested** → [Notified] [▽]
 *Mon 04/05/2015 at 09:00*   DUBOIS Robin (179)            Evaluation            Évaluation 9         **Suggested** → [Notified] [▽]
 *Mon 11/05/2015 at 09:00*   ÖSTGES Otto (168)             Evaluation            Évaluation 10        **Suggested** → [Notified] [▽]
=========================== ============================= ===================== ==================== =================================
<BLANKLINE>


These are Alicia's calendar appointments of the last two months:

>>> last_week = dict(start_date=dd.today(-30), end_date=dd.today(-1))
>>> rt.login('alicia').show(cal.MyEvents, language='en',
...     param_values=last_week)
=========================== ========================= ===================== =============== ================================
 When                        Client                    Calendar Event Type   Summary         Workflow
--------------------------- ------------------------- --------------------- --------------- --------------------------------
 *Wed 07/05/2014 at 09:00*   DA VINCI David (165)      Evaluation            Évaluation 15   **Suggested** → [Notified] [▽]
 *Wed 14/05/2014*            HILGERS Hildegard (133)   Evaluation            Évaluation 6    **Suggested** → [Notified] [▽]
=========================== ========================= ===================== =============== ================================
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
============================ ================= ================ ===============
 When                         Managed by        Summary          Workflow
---------------------------- ----------------- ---------------- ---------------
 **Mon 19/11/2012 (09:00)**   Alicia Allmanns   Évaluation 1     **Suggested**
 **Wed 19/12/2012 (09:00)**   Alicia Allmanns   Évaluation 2     **Suggested**
 **Mon 21/01/2013 (09:00)**   Alicia Allmanns   Évaluation 3     **Suggested**
 **Thu 21/02/2013 (09:00)**   Alicia Allmanns   Évaluation 4     **Suggested**
 **Thu 21/03/2013 (09:00)**   Alicia Allmanns   Évaluation 5     **Suggested**
 **Mon 22/04/2013 (09:00)**   Alicia Allmanns   Évaluation 6     **Suggested**
 **Wed 22/05/2013 (09:00)**   Alicia Allmanns   Évaluation 7     **Suggested**
 **Mon 24/06/2013 (09:00)**   Alicia Allmanns   Évaluation 8     **Suggested**
 **Wed 24/07/2013 (09:00)**   Alicia Allmanns   Évaluation 9     **Suggested**
 **Mon 26/08/2013 (09:00)**   Alicia Allmanns   Évaluation 10    **Suggested**
 **Thu 26/09/2013 (09:00)**   Alicia Allmanns   Évaluation 11    **Suggested**
 **Mon 28/10/2013 (09:00)**   Caroline Carnol   Évaluation 12    **Suggested**
 **Thu 28/11/2013 (09:00)**   Caroline Carnol   Évaluation 13    **Suggested**
 **Mon 30/12/2013 (09:00)**   Caroline Carnol   Évaluation 14    **Suggested**
 **Thu 30/01/2014 (09:00)**   Caroline Carnol   Évaluation 15    **Suggested**
 **Wed 12/03/2014 (09:00)**   Caroline Carnol   Auswertung 1     **Suggested**
 **Tue 15/04/2014 (09:00)**   Caroline Carnol   Auswertung 1     **Suggested**
 **Thu 15/05/2014 (09:00)**   Caroline Carnol   Auswertung 2     **Suggested**
 **Thu 22/05/2014**           Mélanie Mélard    Urgent problem   **Notified**
 **Thu 22/05/2014 (09:40)**   Mélanie Mélard    Diner            **Suggested**
 **Mon 16/06/2014 (09:00)**   Caroline Carnol   Auswertung 3     **Suggested**
 **Wed 16/07/2014 (09:00)**   Caroline Carnol   Auswertung 4     **Suggested**
 **Mon 18/08/2014 (09:00)**   Caroline Carnol   Auswertung 5     **Suggested**
 **Thu 18/09/2014 (09:00)**   Caroline Carnol   Auswertung 6     **Suggested**
 **Mon 20/10/2014 (09:00)**   Caroline Carnol   Auswertung 7     **Suggested**
 **Thu 20/11/2014 (09:00)**   Caroline Carnol   Auswertung 8     **Suggested**
 **Mon 22/12/2014 (09:00)**   Caroline Carnol   Auswertung 9     **Suggested**
============================ ================= ================ ===============
<BLANKLINE>


Events generated by a contract
==============================

>>> obj = isip.Contract.objects.get(id=18)
>>> rt.show(cal.EventsByController, obj, header_level=1, language="en")
======================================
Events of ISIP#18 (Edgard RADERMACHER)
======================================
============================ =============== ================= ============= ===============
 When                         Summary         Managed by        Assigned to   Workflow
---------------------------- --------------- ----------------- ------------- ---------------
 **Thu 07/02/2013 (09:00)**   Évaluation 1    Alicia Allmanns                 **Suggested**
 **Thu 07/03/2013 (09:00)**   Évaluation 2    Alicia Allmanns                 **Suggested**
 **Mon 08/04/2013 (09:00)**   Évaluation 3    Alicia Allmanns                 **Suggested**
 **Wed 08/05/2013 (09:00)**   Évaluation 4    Alicia Allmanns                 **Suggested**
 **Mon 10/06/2013 (09:00)**   Évaluation 5    Alicia Allmanns                 **Suggested**
 **Wed 10/07/2013 (09:00)**   Évaluation 6    Alicia Allmanns                 **Suggested**
 **Mon 12/08/2013 (09:00)**   Évaluation 7    Alicia Allmanns                 **Suggested**
 **Thu 12/09/2013 (09:00)**   Évaluation 8    Alicia Allmanns                 **Suggested**
 **Mon 14/10/2013 (09:00)**   Évaluation 9    Alicia Allmanns                 **Suggested**
 **Thu 14/11/2013 (09:00)**   Évaluation 10   Alicia Allmanns                 **Suggested**
============================ =============== ================= ============= ===============
<BLANKLINE>

