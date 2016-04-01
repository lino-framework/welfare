.. _welfare.tour.autoevents:

=========================
Automatic calendar events
=========================

.. How to test only this document:

    $ python setup.py test -s tests.DocsTests.test_autoevents
    
    doctest init:

    >>> from lino import startup
    >>> startup('lino_welfare.projects.std.settings.doctests')
    >>> from lino.api.doctest import *

For every contract, Lino Welfare automatically generates a series of
calendar events for evaluation meetings.

.. contents::
   :local:
   :depth: 1

Technical stuff
===============

Some local settings which influence automatic generation of
calendar events:

>>> print(dd.plugins.cal.ignore_dates_before)
None
>>> print(str(dd.plugins.cal.ignore_dates_after))
2019-05-22


Evaluation events
=================

The :class:`cal.EventsByController
<lino.modlib.cal.models.EventsByController>` table shows the
evaluation events which have been generated.

For example let's look at ISIP contract #26 of the demo database.

>>> obj = isip.Contract.objects.get(pk=26)
>>> obj.exam_policy
ExamPolicy #1 ('Every month')
>>> rt.show(cal.EventsByController, obj)
========================= =============== ================= ============= ===============
 When                      Summary         Managed by        Assigned to   Workflow
------------------------- --------------- ----------------- ------------- ---------------
 *Tue 3/26/13 at 09:00*    Évaluation 1    Alicia Allmanns                 **Suggested**
 *Fri 4/26/13 at 09:00*    Évaluation 2    Alicia Allmanns                 **Suggested**
 *Mon 5/27/13 at 09:00*    Évaluation 3    Alicia Allmanns                 **Suggested**
 *Thu 6/27/13 at 09:00*    Évaluation 4    Alicia Allmanns                 **Suggested**
 *Mon 7/29/13 at 09:00*    Évaluation 5    Alicia Allmanns                 **Suggested**
 *Thu 8/29/13 at 09:00*    Évaluation 6    Alicia Allmanns                 **Suggested**
 *Mon 9/30/13 at 09:00*    Évaluation 7    Alicia Allmanns                 **Suggested**
 *Wed 10/30/13 at 09:00*   Évaluation 8    Alicia Allmanns                 **Suggested**
 *Mon 12/2/13 at 09:00*    Évaluation 9    Alicia Allmanns                 **Suggested**
 *Thu 1/2/14 at 09:00*     Évaluation 10   Alicia Allmanns                 **Suggested**
 *Mon 2/3/14 at 09:00*     Évaluation 11   Alicia Allmanns                 **Suggested**
 *Mon 3/3/14 at 09:00*     Évaluation 12   Alicia Allmanns                 **Suggested**
 *Thu 4/3/14 at 09:00*     Évaluation 13   Alicia Allmanns                 **Suggested**
 *Mon 5/5/14 at 09:00*     Évaluation 14   Alicia Allmanns                 **Suggested**
 *Thu 6/5/14 at 09:00*     Évaluation 15   Alicia Allmanns                 **Suggested**
========================= =============== ================= ============= ===============
<BLANKLINE>



.. the following verifies a related bugfix

    >>> mt = contenttypes.ContentType.objects.get_for_model(obj.__class__)
    >>> print(mt)
    ISIP
    >>> uri = '/api/cal/EventsByController?mt={0}&mk={1}&fmt=json'
    >>> uri = uri.format(mt.id, obj.id)
    >>> res = test_client.get(uri, REMOTE_USER='robin')
    >>> res.status_code
    200
    >>> d = AttrDict(json.loads(res.content))
    >>> print(d.title)
    Events of ISIP#26 (David DA VINCI)
    >>> print(len(d.rows))
    16


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

>>> ses.show(isip.ExamPolicies)
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE -REPORT_UDIFF
==================== ========================= ========================
 Designation          Designation (fr)          Designation (de)
-------------------- ------------------------- ------------------------
 Every month          Mensuel                   Every month
 Every 2 months       Bimensuel                 Alle 2 Monate
 Every 3 months       Tous les 3 mois           Alle 3 Monate
 Every 2 weeks        Tous les 14 jours         Alle 2 Wochen
 Once after 10 days   Une fois après 10 jours   Einmalig nach 10 Tagen
 Other                Autre                     Sonstige
==================== ========================= ========================
<BLANKLINE>


Coach changes while contract active
===================================

A special condition --which in reality arises quite often-- is that
the coach changes while the contract is still active.  This is why
Lino must attribute every automatic evaluation event to the *currently
responsible coach* at the event's date.

For example, let's pick up ISIP contract #1.

>>> obj = isip.Contract.objects.get(pk=1)
>>> rt.show(cal.EventsByController, obj)
========================= =============== ================= ============= ===============
 When                      Summary         Managed by        Assigned to   Workflow
------------------------- --------------- ----------------- ------------- ---------------
 *Mon 10/29/12 at 09:00*   Evaluation 1    Hubert Huppertz                 **Suggested**
 *Thu 11/29/12 at 09:00*   Evaluation 2    Hubert Huppertz                 **Suggested**
 *Mon 12/31/12 at 09:00*   Evaluation 3    Hubert Huppertz                 **Suggested**
 *Thu 1/31/13 at 09:00*    Evaluation 4    Hubert Huppertz                 **Suggested**
 *Thu 2/28/13 at 09:00*    Evaluation 5    Hubert Huppertz                 **Suggested**
 *Thu 3/28/13 at 09:00*    Evaluation 6    Mélanie Mélard                  **Suggested**
 *Mon 4/29/13 at 09:00*    Evaluation 7    Mélanie Mélard                  **Suggested**
 *Wed 5/29/13 at 09:00*    Evaluation 8    Mélanie Mélard                  **Suggested**
 *Mon 7/1/13 at 09:00*     Evaluation 9    Mélanie Mélard                  **Suggested**
 *Thu 8/1/13 at 09:00*     Evaluation 10   Mélanie Mélard                  **Suggested**
========================= =============== ================= ============= ===============
<BLANKLINE>

The above shows that appointments before 2013-11-10 are with Hubert,
while later appointments are with Caroline. How did Lino know which
coach to assign?

To find an answer, we must look at the coachings of this client:

>>> rt.show(pcsw.CoachingsByClient, obj.client)
============== ========== ================= ========= =============== ============================
 Coached from   until      Coach             Primary   Coaching type   Reason of termination
-------------- ---------- ----------------- --------- --------------- ----------------------------
 3/3/12                    Alicia Allmanns   No        General
 3/13/12        3/8/13     Hubert Huppertz   No        Integ           Transfer to colleague
 3/8/13         10/24/13   Mélanie Mélard    No        Integ           End of right on social aid
 10/24/13                  Caroline Carnol   Yes       Integ
============== ========== ================= ========= =============== ============================
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

>>> ses.show(pcsw.CoachingTypes)
================= ===================== =================== ============= ===== =====================
 Designation       Designation (fr)      Designation (de)    Integration   GSS   Role in evaluations
----------------- --------------------- ------------------- ------------- ----- ---------------------
 General           SSG                   ASD                 No            Yes   Colleague
 Integ             SI                    DSBE                Yes           No    Colleague
 Debts mediation   Médiation de dettes   Schuldnerberatung   No            No
================= ===================== =================== ============= ===== =====================
<BLANKLINE>

The above is coded in
:meth:`lino_welfare.modlib.isip.mixins.ContractBase.setup_auto_event`.

.. The following should be useful if the demo data changes, in order
   to find out which contract to take as new example.

    Display a list of demo contracts which meet this condition.

    List of coaches who ended at least one integration coaching:

    >>> integ = pcsw.CoachingType.objects.filter(does_integ=True)
    >>> l = []
    >>> for u in users.User.objects.all():
    ...     qs = pcsw.Coaching.objects.filter(user=u,
    ...             type__in=integ, end_date__isnull=False)
    ...     if qs.count():
    ...         l.append("%s (%s)" % (u.username, qs[0].end_date))
    >>> print(', '.join(l))
    ... #doctest: +ELLIPSIS -REPORT_UDIFF +NORMALIZE_WHITESPACE
    alicia (2013-10-24), caroline (2014-03-23), hubert (2013-03-08), melanie (2013-10-24)

    List of contracts (isip + jobs) whose client changed the coach during
    application period:

    >>> l = []
    >>> qs1 = isip.Contract.objects.all()
    >>> qs2 = jobs.Contract.objects.all()
    >>> for obj in list(qs1) + list(qs2):
    ...     ar = cal.EventsByController.request(master_instance=obj)
    ...     names = set([e.user.username for e in ar])
    ...     if len(names) > 1:
    ...         l.append(unicode(obj))
    >>> print(len(l))
    15
    >>> print(', '.join(l))
    ... #doctest: +ELLIPSIS -REPORT_UDIFF +NORMALIZE_WHITESPACE    
    ISIP#1 (Alfons AUSDEMWALD), ISIP#2 (Alfons AUSDEMWALD), ISIP#4
    (Dorothée DOBBELSTEIN), ISIP#9 (Luc FAYMONVILLE), ISIP#11
    (Jacqueline JACOBS), ISIP#14 (Josef JONAS), ISIP#17 (Marc
    MALMENDIER), ISIP#20 (Edgard RADERMACHER), ISIP#23 (Hedi
    RADERMACHER), ISIP#28 (Otto ÖSTGES), Art60§7 job supplyment#2
    (Denis DENON), Art60§7 job supplyment#4 (Edgar ENGELS), Art60§7
    job supplyment#9 (Melissa MEESSEN), Art60§7 job supplyment#10
    (Christian RADERMACHER), Art60§7 job supplyment#13 (Vincent VAN
    VEEN)

    >>> obj = isip.Contract.objects.get(pk=1)

    >>> print(obj.user.username)
    hubert
    
    Lino attributes the automatic evaluation events to the coach in
    charge, depending on their date.

    >>> ar = cal.EventsByController.request(master_instance=obj)
    >>> events = ["%s (%s)" % (e.start_date, e.user.first_name) for e in ar]
    >>> print(", ".join(events))
    ... #doctest: +NORMALIZE_WHITESPACE
    2012-10-29 (Hubert), 2012-11-29 (Hubert), 2012-12-31 (Hubert), 
    2013-01-31 (Hubert), 2013-02-28 (Hubert), 2013-03-28 (Mélanie), 
    2013-04-29 (Mélanie), 2013-05-29 (Mélanie), 2013-07-01 (Mélanie), 
    2013-08-01 (Mélanie)

    The above shows that appointments before 2013-11-10 are with Hubert,
    later appointments are with Mélanie.  That's what we wanted.



