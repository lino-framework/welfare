.. doctest docs/specs/cal.rst
.. _welfare.specs.cal:

==================================
Calendar functions in Lino Welfare
==================================

.. doctest init:

    >>> from lino import startup
    >>> startup('lino_welfare.projects.eupen.settings.doctests')
    >>> from lino.api.doctest import *

A technical tour into the :mod:`lino_welfare.modlib.cal` module.

See also :ref:`book.specs.cal`.

.. contents::
   :local:


Lifecycle of a calendar event
=============================

>>> rt.show(cal.EntryStates)
====== ============ ================ ======== ======================= ======== =================== =========
 Wert   name         Text             Symbol   Teilnehmer bearbeiten   Stabil   nicht blockierend   No auto
------ ------------ ---------------- -------- ----------------------- -------- ------------------- ---------
 10     suggested    Vorschlag        ?        Ja                      Nein     Nein                Nein
 20     draft        Entwurf          ☐        Ja                      Nein     Nein                Nein
 50     took_place   Stattgefunden    ☑        Ja                      Ja       Nein                Nein
 70     cancelled    Storniert        ☒        Nein                    Ja       Ja                  Ja
 40     published    Veröffentlicht   ☼        Ja                      Ja       Nein                Nein
====== ============ ================ ======== ======================= ======== =================== =========
<BLANKLINE>


Not for everybody
=================

Only users with the :class:`OfficeUser
<lino.modlib.office.roles.OfficeUser>` role can see the calendar
functionality.  All users with one of the following user_types can see
each other's calendars:

>>> from lino.modlib.office.roles import OfficeUser
>>> for p in users.UserTypes.items():
...     if p.has_required_roles([OfficeUser]):
...         print(p)
... #doctest: +NORMALIZE_WHITESPACE +REPORT_UDIFF
100 (Begleiter im DSBE)
110 (Sozialarbeiter DSBE (Verwalter))
120 (Sozialarbeiter DSBE (flexibel))
200 (Berater Erstempfang)
300 (Schuldenberater)
400 (Sozi)
410 (Sozialarbeiter (Verwalter))
420 (Sozialarbeiter ASD (flexibel))
500 (Buchhalter)
510 (Buchhalter (Verwalter))
900 (Verwalter)
910 (Security advisor)




Events today
============

Here is what the :class:`lino.modlib.cal.ui.EntriesByDay` table gives:

>>> rt.login('theresia').show(cal.EntriesByDay, language='en', header_level=1)
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE -REPORT_UDIFF
===========================
Thu 22/05/2014 (22.05.2014)
===========================
============ ======================== =================== ================ ============= ===================== ====== =================================
 Start time   Client                   Short description   Managed by       Assigned to   Calendar entry type   Room   Workflow
------------ ------------------------ ------------------- ---------------- ------------- --------------------- ------ ---------------------------------
 08:30:00     FAYMONVILLE Luc (130*)   Rencontre           Mélanie Mélard                 Evaluation                   [⚑] **Suggested** → [☼] [☑] [☒]
 13:30:00     ENGELS Edgar (129)       Frühstück           Judith Jousten                 Appointment                  [⚑] **Published** → [☑] [☒] [☐]
============ ======================== =================== ================ ============= ===================== ====== =================================
<BLANKLINE>


Note how Theresia can change the state only on her own event.

Users looking at their events
=============================

The **My events** table shows shows today's and all future
appointments of the user who requests it.

Here is what it says for Alicia.

>>> rt.login('alicia').show(cal.MyEntries, language='en')
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE -REPORT_UDIFF
====================================== ========================= ===================== =================== =============================
 When                                   Client                    Calendar entry type   Short description   Workflow
-------------------------------------- ------------------------- --------------------- ------------------- -----------------------------
 `Mon 26/05/2014 at 09:40 <Detail>`__                             Meeting               Diner               **Draft** → [☼] [☒]
 `Sun 01/06/2014 at 08:30 <Detail>`__                             Meeting               Diner               **Suggested** → [☼] [☒]
 `Sat 07/06/2014 at 13:30 <Detail>`__                             Meeting               Diner               **Published** → [☒] [☐]
 `Mon 23/06/2014 at 09:00 <Detail>`__   DA VINCI David (165)      Evaluation            Évaluation 1        [▽] **Suggested** → [☼] [☒]
 `Mon 14/07/2014 <Detail>`__            RADERMACHER Fritz (158)   Evaluation            Évaluation 6        [▽] **Suggested** → [☼] [☒]
 `Wed 23/07/2014 at 09:00 <Detail>`__   DA VINCI David (165)      Evaluation            Évaluation 2        [▽] **Suggested** → [☼] [☒]
 `Thu 14/08/2014 <Detail>`__            HILGERS Hildegard (133)   Evaluation            Évaluation 7        [▽] **Suggested** → [☼] [☒]
 `Mon 25/08/2014 at 09:00 <Detail>`__   DA VINCI David (165)      Evaluation            Évaluation 3        [▽] **Suggested** → [☼] [☒]
 `Thu 25/09/2014 at 09:00 <Detail>`__   DA VINCI David (165)      Evaluation            Évaluation 4        [▽] **Suggested** → [☼] [☒]
 `Tue 14/10/2014 <Detail>`__            RADERMACHER Fritz (158)   Evaluation            Évaluation 7        [▽] **Suggested** → [☼] [☒]
 `Mon 27/10/2014 at 09:00 <Detail>`__   DA VINCI David (165)      Evaluation            Évaluation 5        [▽] **Suggested** → [☼] [☒]
 `Thu 27/11/2014 at 09:00 <Detail>`__   DA VINCI David (165)      Evaluation            Évaluation 6        [▽] **Suggested** → [☼] [☒]
 `Mon 29/12/2014 at 09:00 <Detail>`__   DA VINCI David (165)      Evaluation            Évaluation 7        [▽] **Suggested** → [☼] [☒]
 `Thu 29/01/2015 at 09:00 <Detail>`__   DA VINCI David (165)      Evaluation            Évaluation 8        [▽] **Suggested** → [☼] [☒]
 `Mon 02/03/2015 at 09:00 <Detail>`__   DA VINCI David (165)      Evaluation            Évaluation 9        [▽] **Suggested** → [☼] [☒]
====================================== ========================= ===================== =================== =============================
<BLANKLINE>



These are for Hubert:

>>> rt.login('hubert').show(cal.MyEntries, language='en')
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE -REPORT_UDIFF
====================================== ======================== ===================== =================== =============================
 When                                   Client                   Calendar entry type   Short description   Workflow
-------------------------------------- ------------------------ --------------------- ------------------- -----------------------------
 `Tue 27/05/2014 at 10:20 <Detail>`__                            Internal              Abendessen          **Took place** → [☐]
 `Wed 28/05/2014 at 09:00 <Detail>`__   BRECHT Bernd (177)       Evaluation            Évaluation 15       [▽] **Suggested** → [☼] [☒]
 `Mon 02/06/2014 at 09:40 <Detail>`__                            Internal              Abendessen          **Draft** → [☼] [☒]
 `Tue 03/06/2014 <Detail>`__            DENON Denis (180*)       Evaluation            Auswertung 1        [▽] **Suggested** → [☼] [☒]
 `Wed 04/06/2014 <Detail>`__            LAMBERTZ Guido (142)     Evaluation            Évaluation 6        [▽] **Suggested** → [☼] [☒]
 `Sun 08/06/2014 at 08:30 <Detail>`__                            Internal              Abendessen          **Suggested** → [☼] [☒]
 `Thu 19/06/2014 at 09:00 <Detail>`__   JEANÉMART Jérôme (181)   Evaluation            Évaluation 15       [▽] **Suggested** → [☼] [☒]
 `Mon 14/07/2014 at 09:00 <Detail>`__   BRECHT Bernd (177)       Evaluation            Auswertung 1        [▽] **Suggested** → [☼] [☒]
 `Mon 04/08/2014 at 09:00 <Detail>`__   JEANÉMART Jérôme (181)   Evaluation            Auswertung 1        [▽] **Suggested** → [☼] [☒]
 `Tue 05/08/2014 <Detail>`__            FAYMONVILLE Luc (130*)   Evaluation            Auswertung 3        [▽] **Suggested** → [☼] [☒]
 `Tue 12/08/2014 <Detail>`__            RADERMECKER Rik (173)    Evaluation            Auswertung 2        [▽] **Suggested** → [☼] [☒]
 `Thu 14/08/2014 at 09:00 <Detail>`__   BRECHT Bernd (177)       Evaluation            Auswertung 2        [▽] **Suggested** → [☼] [☒]
 `Wed 03/09/2014 <Detail>`__            DENON Denis (180*)       Evaluation            Auswertung 2        [▽] **Suggested** → [☼] [☒]
 `Thu 04/09/2014 <Detail>`__            LAMBERTZ Guido (142)     Evaluation            Évaluation 7        [▽] **Suggested** → [☼] [☒]
 `Thu 04/09/2014 at 09:00 <Detail>`__   JEANÉMART Jérôme (181)   Evaluation            Auswertung 2        [▽] **Suggested** → [☼] [☒]
 `Mon 15/09/2014 at 09:00 <Detail>`__   BRECHT Bernd (177)       Evaluation            Auswertung 3        [▽] **Suggested** → [☼] [☒]
 `Mon 06/10/2014 at 09:00 <Detail>`__   JEANÉMART Jérôme (181)   Evaluation            Auswertung 3        [▽] **Suggested** → [☼] [☒]
 `Wed 15/10/2014 at 09:00 <Detail>`__   BRECHT Bernd (177)       Evaluation            Auswertung 4        [▽] **Suggested** → [☼] [☒]
 `Thu 06/11/2014 at 09:00 <Detail>`__   JEANÉMART Jérôme (181)   Evaluation            Auswertung 4        [▽] **Suggested** → [☼] [☒]
 `Wed 12/11/2014 <Detail>`__            RADERMECKER Rik (173)    Evaluation            Auswertung 3        [▽] **Suggested** → [☼] [☒]
 `Mon 17/11/2014 at 09:00 <Detail>`__   BRECHT Bernd (177)       Evaluation            Auswertung 5        [▽] **Suggested** → [☼] [☒]
 `Wed 03/12/2014 <Detail>`__            DENON Denis (180*)       Evaluation            Auswertung 3        [▽] **Suggested** → [☼] [☒]
 `Mon 08/12/2014 at 09:00 <Detail>`__   JEANÉMART Jérôme (181)   Evaluation            Auswertung 5        [▽] **Suggested** → [☼] [☒]
 `Wed 17/12/2014 at 09:00 <Detail>`__   BRECHT Bernd (177)       Evaluation            Auswertung 6        [▽] **Suggested** → [☼] [☒]
 `Thu 08/01/2015 at 09:00 <Detail>`__   JEANÉMART Jérôme (181)   Evaluation            Auswertung 6        [▽] **Suggested** → [☼] [☒]
 `Mon 19/01/2015 at 09:00 <Detail>`__   BRECHT Bernd (177)       Evaluation            Auswertung 7        [▽] **Suggested** → [☼] [☒]
 `Mon 09/02/2015 at 09:00 <Detail>`__   JEANÉMART Jérôme (181)   Evaluation            Auswertung 7        [▽] **Suggested** → [☼] [☒]
 `Thu 19/02/2015 at 09:00 <Detail>`__   BRECHT Bernd (177)       Evaluation            Auswertung 8        [▽] **Suggested** → [☼] [☒]
 `Tue 03/03/2015 <Detail>`__            DENON Denis (180*)       Evaluation            Auswertung 4        [▽] **Suggested** → [☼] [☒]
 `Mon 09/03/2015 at 09:00 <Detail>`__   JEANÉMART Jérôme (181)   Evaluation            Auswertung 8        [▽] **Suggested** → [☼] [☒]
 `Thu 19/03/2015 at 09:00 <Detail>`__   BRECHT Bernd (177)       Evaluation            Auswertung 9        [▽] **Suggested** → [☼] [☒]
 `Thu 09/04/2015 at 09:00 <Detail>`__   JEANÉMART Jérôme (181)   Evaluation            Auswertung 9        [▽] **Suggested** → [☼] [☒]
 `Mon 20/04/2015 at 09:00 <Detail>`__   BRECHT Bernd (177)       Evaluation            Auswertung 10       [▽] **Suggested** → [☼] [☒]
====================================== ======================== ===================== =================== =============================
<BLANKLINE>


And these for Mélanie:

>>> rt.login('melanie').show(cal.MyEntries, language='en')
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE -REPORT_UDIFF
====================================== ============================= ===================== =================== =============================
 When                                   Client                        Calendar entry type   Short description   Workflow
-------------------------------------- ----------------------------- --------------------- ------------------- -----------------------------
 `Thu 22/05/2014 at 08:30 <Detail>`__   FAYMONVILLE Luc (130*)        Evaluation            Rencontre           **Suggested** → [☼] [☑] [☒]
 `Mon 26/05/2014 at 09:00 <Detail>`__   ENGELS Edgar (129)            Evaluation            Évaluation 3        [▽] **Suggested** → [☼] [☒]
 `Wed 28/05/2014 at 13:30 <Detail>`__   HILGERS Henri (134)           Evaluation            Rencontre           **Published** → [☒] [☐]
 `Tue 03/06/2014 at 11:10 <Detail>`__   JOHNEN Johann (138)           Evaluation            Rencontre           **Cancelled**
 ...
 `Thu 02/04/2015 at 09:00 <Detail>`__   DUBOIS Robin (179)            Evaluation            Évaluation 8        [▽] **Suggested** → [☼] [☒]
 `Thu 09/04/2015 at 09:00 <Detail>`__   ÖSTGES Otto (168)             Evaluation            Évaluation 9        [▽] **Suggested** → [☼] [☒]
 `Mon 20/04/2015 at 09:00 <Detail>`__   RADERMACHER Guido (159)       Evaluation            Évaluation 10       [▽] **Suggested** → [☼] [☒]
 `Mon 04/05/2015 at 09:00 <Detail>`__   DUBOIS Robin (179)            Evaluation            Évaluation 9        [▽] **Suggested** → [☼] [☒]
 `Mon 11/05/2015 at 09:00 <Detail>`__   ÖSTGES Otto (168)             Evaluation            Évaluation 10       [▽] **Suggested** → [☼] [☒]
====================================== ============================= ===================== =================== =============================
<BLANKLINE>


These are Alicia's calendar appointments of the last two months:

>>> pv = dict(start_date=dd.today(-15), end_date=dd.today(-1))
>>> rt.login('alicia').show(cal.MyEntries, language='en',
...     param_values=pv)
====================================== ========================= ===================== =================== =============================
 When                                   Client                    Calendar entry type   Short description   Workflow
-------------------------------------- ------------------------- --------------------- ------------------- -----------------------------
 `Wed 07/05/2014 at 09:00 <Detail>`__   DA VINCI David (165)      Evaluation            Évaluation 15       [▽] **Suggested** → [☑] [☒]
 `Thu 08/05/2014 at 13:30 <Detail>`__                             Meeting               Diner               **Published** → [☑] [☒] [☐]
 `Wed 14/05/2014 <Detail>`__            HILGERS Hildegard (133)   Evaluation            Évaluation 6        [▽] **Suggested** → [☑] [☒]
 `Wed 14/05/2014 at 11:10 <Detail>`__                             Meeting               Diner               **Cancelled**
 `Tue 20/05/2014 at 10:20 <Detail>`__                             Meeting               Diner               **Took place** → [☐]
====================================== ========================= ===================== =================== =============================
<BLANKLINE>



Overdue appointments
====================

>>> rt.login('alicia').show(cal.MyOverdueAppointments, language='en')
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE -REPORT_UDIFF
============================================================================= ============================================================ ===================== =============================
 overview                                                                      Controlled by                                                Calendar entry type   Workflow
----------------------------------------------------------------------------- ------------------------------------------------------------ --------------------- -----------------------------
 `Évaluation 15 (07.04.2014 09:00) with RADERMACHER Alfons (153) <Detail>`__   `ISIP#17 (Alfons RADERMACHER) <Detail>`__                    Evaluation            [▽] **Suggested** → [☑] [☒]
 `Évaluation 14 (07.04.2014 09:00) with DA VINCI David (165) <Detail>`__       `ISIP#22 (David DA VINCI) <Detail>`__                        Evaluation            [▽] **Suggested** → [☑] [☒]
 `Évaluation 5 (14.04.2014) with RADERMACHER Fritz (158) <Detail>`__           `Art60§7 job supplyment#11 (Fritz RADERMACHER) <Detail>`__   Evaluation            [▽] **Suggested** → [☑] [☒]
 `Diner (02.05.2014 08:30) <Detail>`__                                                                                                      Meeting               **Suggested** → [☑] [☒]
 `Évaluation 15 (07.05.2014 09:00) with DA VINCI David (165) <Detail>`__       `ISIP#22 (David DA VINCI) <Detail>`__                        Evaluation            [▽] **Suggested** → [☑] [☒]
 `Évaluation 6 (14.05.2014) with HILGERS Hildegard (133) <Detail>`__           `Art60§7 job supplyment#5 (Hildegard HILGERS) <Detail>`__    Evaluation            [▽] **Suggested** → [☑] [☒]
============================================================================= ============================================================ ===================== =============================
<BLANKLINE>


Calendars and Subscriptions
===========================

A Calendar is a set of events that can be shown or hidden in the
Calendar Panel.

In Lino Welfare, we have one Calendar per User.  Or to be more
precise: 

- The :class:`User` model has a :attr:`calendar` field.

- The calendar of a calendar entry is indirectly defined by the
  Event's :attr:`user` field.

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
 8    rolf       Nein
==== ========== ===========
<BLANKLINE>


Events by client
================

This table is special in that it shows not only events directly
related to the client (i.e. :attr:`Event.project` pointing to it) but
also those where this client is among the guests.

.. the following snippet finds examples of clients where this is the
   case

    >>> sc = settings.SITE.site_config
    >>> sc.hide_events_before
    datetime.date(2014, 4, 1)

    >>> from lino.utils import mti
    >>> candidates = set()
    >>> for obj in cal.Guest.objects.filter(event__start_date__gt=sc.hide_events_before):
    ...     if obj.partner and obj.partner_id != obj.event.project_id:
    ...         if mti.get_child(obj.partner, pcsw.Client):
    ...             #print obj, obj.event.project_id, obj.partner_id
    ...             # candidates.add(obj.event.project_id)
    ...             candidates.add(obj.partner_id)
    >>> print sorted(candidates)
    []


>>> obj = pcsw.Client.objects.get(id=130)
>>> rt.show(cal.EntriesByClient, obj, header_level=1,
...     language="en", column_names="when_text user summary project")
...     #doctest: +SKIP
====================================================================
Calendar entries of FAYMONVILLE Luc (130*) (Dates 01.04.2014 to ...)
====================================================================
=========================== ================= ============== ========================
 When                        Managed by        Summary        Client
--------------------------- ----------------- -------------- ------------------------
 *Mon 05/05/2014*            Hubert Huppertz   Auswertung 2   FAYMONVILLE Luc (130*)
 *Tue 20/05/2014 at 09:40*   Judith Jousten    Interview      FAYMONVILLE Luc (130*)
 *Tue 05/08/2014*            Hubert Huppertz   Auswertung 3   FAYMONVILLE Luc (130*)
=========================== ================= ============== ========================
<BLANKLINE>

TODO: above example does not illustrate what this section wants to
show...


Events generated by a contract
==============================

>>> settings.SITE.site_config.update(hide_events_before=None)
>>> obj = isip.Contract.objects.get(id=18)
>>> rt.show(cal.EntriesByController, obj, header_level=1, language="en")
================================================
Calendar entries of ISIP#18 (Edgard RADERMACHER)
================================================
============================ =================== ================= ============= ===============
 When                         Short description   Managed by        Assigned to   Workflow
---------------------------- ------------------- ----------------- ------------- ---------------
 **Thu 07/02/2013 (09:00)**   Évaluation 1        Alicia Allmanns                 **Suggested**
 **Thu 07/03/2013 (09:00)**   Évaluation 2        Alicia Allmanns                 **Suggested**
 **Mon 08/04/2013 (09:00)**   Évaluation 3        Alicia Allmanns                 **Suggested**
 **Wed 08/05/2013 (09:00)**   Évaluation 4        Alicia Allmanns                 **Suggested**
 **Mon 10/06/2013 (09:00)**   Évaluation 5        Alicia Allmanns                 **Suggested**
 **Wed 10/07/2013 (09:00)**   Évaluation 6        Alicia Allmanns                 **Suggested**
 **Mon 12/08/2013 (09:00)**   Évaluation 7        Alicia Allmanns                 **Suggested**
 **Thu 12/09/2013 (09:00)**   Évaluation 8        Alicia Allmanns                 **Suggested**
 **Mon 14/10/2013 (09:00)**   Évaluation 9        Alicia Allmanns                 **Suggested**
 **Thu 14/11/2013 (09:00)**   Évaluation 10       Alicia Allmanns                 **Suggested**
============================ =================== ================= ============= ===============
<BLANKLINE>

Filter list of clients when creating appointment
================================================

The "Client" field of a calendar entry in :ref:`welfare` has a
filtered choice list which shows only coached clients.  "Quand on veut
ajouter un rendez-vous dans le panneau "Rendez-vous aujourd'hui", la
liste déroulante pour le choix du bénéficiaire fait référence à la
liste de l'onglet CONTACTS --> BÉNÉFICIAIRES.  Nous souhaitons que la
liste de référence soit celle de l'onglet CPAS --> BÉNÉFICIAIRES.  En
effet, cette dernière ne reprend que les dossiers actifs (attribués
aux travailleurs sociaux)."

>>> show_choices('romain', '/choices/cal/AllEntries/project')
<br/>
AUSDEMWALD Alfons (116)
BRECHT Bernd (177)
COLLARD Charlotte (118)
DENON Denis (180*)
DOBBELSTEIN Dorothée (124)
DUBOIS Robin (179)
EMONTS Daniel (128)
EMONTS-GAST Erna (152)
ENGELS Edgar (129)
EVERS Eberhart (127)
FAYMONVILLE Luc (130*)
GROTECLAES Gregory (132)
HILGERS Hildegard (133)
JACOBS Jacqueline (137)
JEANÉMART Jérôme (181)
JONAS Josef (139)
KAIVERS Karl (141)
KELLER Karl (178)
LAMBERTZ Guido (142)
LAZARUS Line (144)
MALMENDIER Marc (146)
MEESSEN Melissa (147)
RADERMACHER Alfons (153)
RADERMACHER Christian (155)
RADERMACHER Edgard (157)
RADERMACHER Guido (159)
RADERMACHER Hedi (161)
RADERMECKER Rik (173)
DA VINCI David (165)
VAN VEEN Vincent (166)
ÖSTGES Otto (168)

