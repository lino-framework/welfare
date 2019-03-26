.. doctest docs/specs/autoevents.rst
.. _welfare.tour.autoevents:
.. _welfare.specs.autoevents:

=========================
Automatic calendar events
=========================

For every contract, Lino Welfare automatically generates a series of
calendar events for evaluation meetings.

.. contents::
   :local:
   :depth: 1


.. include:: /include/tested.rst

>>> from lino import startup
>>> startup('lino_welfare.projects.gerd.settings.doctests')
>>> from lino.api.doctest import *
>>> translation.activate("en")

           

Plugin configuration
====================

Some local settings which influence automatic generation of
calendar events:

>>> print(dd.plugins.cal.ignore_dates_before)
None
>>> print(str(dd.plugins.cal.ignore_dates_after))
2019-05-22


Evaluation events
=================

The :class:`EntriesByController
<lino_xl.lib.cal.ui.EntriesByController>` table shows the evaluation
events which have been generated.

>>> settings.SITE.site_config.update(hide_events_before=None)

For example let's look at ISIP contract #26 of the demo database.

>>> obj = isip.Contract.objects.get(pk=26)
>>> obj.exam_policy
ExamPolicy #1 ('Every month')
>>> rt.show(cal.EntriesByController, obj)
========================== =================== ================ ======== =================
 When                       Short description   Managed by       No.      Workflow
-------------------------- ------------------- ---------------- -------- -----------------
 *Mon 11/05/2015 (09:00)*   Évaluation 10       Mélanie Mélard   10       **? Suggested**
 *Thu 09/04/2015 (09:00)*   Évaluation 9        Mélanie Mélard   9        **? Suggested**
 *Mon 09/03/2015 (09:00)*   Évaluation 8        Mélanie Mélard   8        **? Suggested**
 *Mon 09/02/2015 (09:00)*   Évaluation 7        Mélanie Mélard   7        **? Suggested**
 *Thu 08/01/2015 (09:00)*   Évaluation 6        Mélanie Mélard   6        **? Suggested**
 *Mon 08/12/2014 (09:00)*   Évaluation 5        Mélanie Mélard   5        **? Suggested**
 *Thu 06/11/2014 (09:00)*   Évaluation 4        Mélanie Mélard   4        **? Suggested**
 *Mon 06/10/2014 (09:00)*   Évaluation 3        Mélanie Mélard   3        **? Suggested**
 *Thu 04/09/2014 (09:00)*   Évaluation 2        Mélanie Mélard   2        **? Suggested**
 *Mon 04/08/2014 (09:00)*   Évaluation 1        Mélanie Mélard   1        **? Suggested**
 **Total (10 rows)**                                             **55**
========================== =================== ================ ======== =================
<BLANKLINE>

Note how Lino avoids Sundays and Saturdays by moving to the following
Monday.


.. the following verifies a related bugfix

    >>> mt = contenttypes.ContentType.objects.get_for_model(obj.__class__)
    >>> print(mt)
    ISIP
    >>> uri = '/api/cal/EntriesByController?mt={0}&mk={1}&fmt=json'
    >>> uri = uri.format(mt.id, obj.id)
    >>> test_client.force_login(rt.login('robin').user)
    >>> res = test_client.get(uri, REMOTE_USER='robin')
    >>> res.status_code
    200
    >>> d = AttrDict(json.loads(res.content))
    >>> print(d.title)
    Calendar entries of ISIP#26 (Otto ÖSTGES)
    >>> print(len(d.rows))
    11


Configuration
=============

The frequence of the evaluation meetings depends on the *evaluation
policy* :attr:`exam_policy
<lino_welfare.modlib.isip.mixins.ContractTypeBase.exam_policy>` used
for this contract.

You can configure the list of allowed examination policies via the
:menuselection:`Configure --> Integration --> Examination policies`
command.

>>> ses = rt.login('robin')
>>> translation.activate('en')

>>> ses.get_user().user_type.hidden_languages = None
>>> ses.show(isip.ExamPolicies)
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE -REPORT_UDIFF
====================== ========================= ====================
 Designation            Designation (fr)          Designation (en)
---------------------- ------------------------- --------------------
 Monatlich              Mensuel                   Every month
 Alle 2 Monate          Bimensuel                 Every 2 months
 Alle 3 Monate          Tous les 3 mois           Every 3 months
 Alle 2 Wochen          Tous les 14 jours         Every 2 weeks
 Einmal nach 10 Tagen   Une fois après 10 jours   Once after 10 days
 Sonstige               Autre                     Other
====================== ========================= ====================
<BLANKLINE>


Coach changes while contract active
===================================

A special condition --which in reality arises quite often-- is that
the coach changes while the contract is still active.  This is why
Lino must attribute every automatic evaluation event to the *currently
responsible coach* at the event's date.

For example, let's pick up ISIP contract #1.

>>> obj = isip.Contract.objects.get(pk=1)
>>> rt.show(cal.EntriesByController, obj)
========================== =================== ================= ======== =================
 When                       Short description   Managed by        No.      Workflow
-------------------------- ------------------- ----------------- -------- -----------------
 *Thu 01/08/2013 (09:00)*   Auswertung 10       Mélanie Mélard    10       **? Suggested**
 *Mon 01/07/2013 (09:00)*   Auswertung 9        Mélanie Mélard    9        **? Suggested**
 *Wed 29/05/2013 (09:00)*   Auswertung 8        Mélanie Mélard    8        **? Suggested**
 *Mon 29/04/2013 (09:00)*   Auswertung 7        Mélanie Mélard    7        **? Suggested**
 *Thu 28/03/2013 (09:00)*   Auswertung 6        Mélanie Mélard    6        **? Suggested**
 *Thu 28/02/2013 (09:00)*   Auswertung 5        Hubert Huppertz   5        **? Suggested**
 *Thu 31/01/2013 (09:00)*   Auswertung 4        Hubert Huppertz   4        **? Suggested**
 *Mon 31/12/2012 (09:00)*   Auswertung 3        Hubert Huppertz   3        **? Suggested**
 *Thu 29/11/2012 (09:00)*   Auswertung 2        Hubert Huppertz   2        **? Suggested**
 *Mon 29/10/2012 (09:00)*   Auswertung 1        Hubert Huppertz   1        **? Suggested**
 **Total (10 rows)**                                              **55**
========================== =================== ================= ======== =================
<BLANKLINE>

The above shows that appointments before 2013-03-08 are with Hubert, while
later appointments are with Caroline. How did Lino know which coach to assign?
To find an answer, we must look at the coachings of this client:

>>> rt.show('coachings.CoachingsByClient', obj.client)
============== ============ ================= ========= =============== ============================
 Coached from   until        Coach             Primary   Coaching type   Reason of termination
-------------- ------------ ----------------- --------- --------------- ----------------------------
 03/03/2012                  Alicia Allmanns   No        General
 13/03/2012     08/03/2013   Hubert Huppertz   No        Integ           Transfer to colleague
 08/03/2013     24/10/2013   Mélanie Mélard    No        Integ           End of right on social aid
 24/10/2013                  Caroline Carnol   Yes       Integ
============== ============ ================= ========= =============== ============================
<BLANKLINE>


ISIP contract #21 was signed by Hubert for a period from 2013-02-16
until 2014-06-11.

>>> print(obj.user.username)
hubert
>>> print(obj.applies_from)
2012-09-29
>>> print(obj.applies_until)
2013-08-07

So there was no coaching at all defined for this client when the
contract started. This is theoretically not possible, but Lino does
not prevent us from creating such a contract.

This is why Hubert got responsible for the first evaluation meetings.
On 2013-11-10 Caroline started to coach this client, but this didn't
change the responsible user since this coaching was for the General
social service which is not considered integration work.

The **currently responsible coach** is the user for which there is an
active *integration coaching*.  An **integration coaching** is a
coaching whose type has its :attr:`does_integ
<lino_welfare.modlib.pcsw.coaching.CoachingType.does_integ>` field set
to `True`. You can configure this via :menuselection:`Configure -->
PCSW --> Coaching types`. The default configuration is as follows:

>>> ses.show('coachings.CoachingTypes')
=================== ===================== ================== ============= ===== =====================
 Designation         Designation (fr)      Designation (en)   Integration   GSS   Role in evaluations
------------------- --------------------- ------------------ ------------- ----- ---------------------
 ASD                 SSG                   General            No            Yes   Colleague
 DSBE                SI                    Integ              Yes           No    Colleague
 Schuldnerberatung   Médiation de dettes   Debts mediation    No            No
=================== ===================== ================== ============= ===== =====================
<BLANKLINE>

The above is coded in
:meth:`lino_welfare.modlib.isip.ContractBase.setup_auto_event`.

.. The following should be useful if the demo data changes, in order
   to find out which contract to take as new example.

    Display a list of demo contracts which meet this condition.

    List of coaches who ended at least one integration coaching:

    >>> integ = coachings.CoachingType.objects.filter(does_integ=True)
    >>> l = []
    >>> for u in users.User.objects.all():
    ...     qs = coachings.Coaching.objects.filter(user=u,
    ...             type__in=integ, end_date__isnull=False)
    ...     if qs.count():
    ...         l.append("%s (%s)" % (u.username, qs[0].end_date))
    >>> print(', '.join(l))
    ... #doctest: +ELLIPSIS -REPORT_UDIFF +NORMALIZE_WHITESPACE
    alicia (2014-03-23), caroline (2013-03-08), hubert (2013-03-08), melanie (2013-10-24)
    
    List of contracts (isip + jobs) whose client changed the coach during
    application period:

    >>> l = []
    >>> qs1 = isip.Contract.objects.all()
    >>> qs2 = jobs.Contract.objects.all()
    >>> for obj in list(qs1) + list(qs2):
    ...     ar = cal.EntriesByController.request(master_instance=obj)
    ...     names = set([e.user.username for e in ar])
    ...     if len(names) > 1:
    ...         l.append(str(obj))
    >>> print(len(l))
    14
    >>> print(', '.join(l))
    ... #doctest: +ELLIPSIS -REPORT_UDIFF +NORMALIZE_WHITESPACE
    ISIP#1 (Alfons AUSDEMWALD), ISIP#2 (Alfons AUSDEMWALD), ISIP#4
    (Eberhart EVERS), ISIP#7 (Edgar ENGELS), ISIP#12 (Line LAZARUS),
    ISIP#14 (Melissa MEESSEN), ISIP#19 (Guido RADERMACHER), ISIP#24
    (Otto ÖSTGES), ISIP#27 (Bernd BRECHT), ISIP#29 (Robin DUBOIS),
    ISIP#32 (Jérôme JEANÉMART), Art60§7 job supplyment#6 (Guido
    LAMBERTZ), Art60§7 job supplyment#12 (Vincent VAN VEEN), Art60§7
    job supplyment#13 (Rik RADERMECKER)

    >>> obj = isip.Contract.objects.get(pk=1)

    >>> print(obj.user.username)
    hubert
    
    Lino attributes the automatic evaluation events to the coach in
    charge, depending on their date.

    >>> ar = cal.EntriesByController.request(master_instance=obj)
    >>> events = ["%s (%s)" % (e.start_date, e.user.first_name) for e in ar]
    >>> print(", ".join(events))
    ... #doctest: +NORMALIZE_WHITESPACE
    2013-08-01 (Mélanie), 2013-07-01 (Mélanie), 2013-05-29 (Mélanie),
    2013-04-29 (Mélanie), 2013-03-28 (Mélanie), 2013-02-28 (Hubert),
    2013-01-31 (Hubert), 2012-12-31 (Hubert), 2012-11-29 (Hubert),
    2012-10-29 (Hubert)

    
    The above shows that appointments before 2013-11-10 are with Hubert,
    later appointments are with Mélanie.  That's what we wanted.



