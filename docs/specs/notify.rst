.. _welfare.specs.notify:

=============================
Notifications in Lino Welfare
=============================

.. How to test only this document:

    $ python setup.py test -s tests.SpecsTests.test_notify

    doctest init:

    >>> from lino import startup
    >>> startup('lino_welfare.projects.std.settings.doctests')
    >>> from lino.api.doctest import *

.. contents:: 
   :local:
   :depth: 2



Testing the client workflow
===========================

Automatic tests are in :mod:`lino_welfare.projects.std.tests.test_notify`.

Some processes are not yet covered by any automatic test because they
contain Javascript dialogs.  So here is a manual test suite.

The following instructions are for :mod:`lino_welfare.projects.eupen`,
but similar steps are in :mod:`lino_welfare.projects.chatelet`.

- Install :ref:`welfare`, go to the
  :file:`lino_welfare/projects/eupen` directory, run
  :manage:`prep` followed by :manage:`runserver`.

- Instead of logging in as Theresia, Caroline etc, consider logging in
  as Robin and then *act as* Theresia, Caroline.  The advantage is
  that your menus and labels will be in English.


Managing newcomer requests
--------------------------

:class:`AssignCoach
<lino_welfare.modlib.newcomers.AssignCoach>` and :class:`RefuseClient
<lino_welfare.modlib.pcsw.models.RefuseClient>`)

- Act as Caroline

- Select :menuselection:`Newcomers --> New Clients`,
  double-click on **Emil EIERSCHAL**, select the `Coaches` tab.

- In the `Available coaches` panel, click on `Assign` next to Hubert.
  Confirm dialog by clicking `OK`.  Note that the console says::

    Notify 1 users that EIERSCHAL Emil (175) zugewiesen zu Hubert Huppertz

- Note that the Workflow field now says "Coached --> Former"

- Switch to the "History" tab and verify that a system note has been
  created.

- Close the detail window and reopen it on Bruno BRAUN (another
  client).  Select the `Coaches` tab.  In the `Workflow` field click
  on `Refuse`.  Select "PCSW is not competent" as `Refusal reason`
  from the selection list.  Confirm dialog by clicking `OK`.

- Switch to the "History" tab and verify that a system note has been
  created.

- Act as Hubert and verify that he has a welcome message "You have 1
  unseen notifications".  Click on this message and verify that the
  "About" field of the notification is a clickable pointer to the
  client *Emil EIERSCHAL*.

  No notification is sent for RefuseClient since there is no coaching.


As a reception clerk, receive a waiting visitor
(:class:`ReceiveVisitor <lino_xl.lib.reception.ReceiveVisitor>`)


- Click on the first client listed in `Waiting visitors` (**EMONTS
  Daniel**).
- That client is waiting for Hubert.  Click `Receive` in the
  `Appointments` panel.  You get a confirmation :message:`Emonts
  Daniel begins consultation with Hubert Huppertz. Are you sure?`.
  Click OK. Note that they are now `Busy`.
- Close the detail window. Note that Daniel is no longer listed in
  `Waiting visitors`.


As a reception clerk, check out a visitor who leaves the center
(:class:`CheckoutVisitor <lino_xl.lib.reception.CheckoutVisitor>`)

- From the main menu, select :menuselection:`Reception --> Busy
  visitors`.

- Find Daniel Emonts. Click on `Checkout`. Confirm the message
  :message:`Emonts Daniel leaves after meeting with Hubert
  Huppertz. Are you sure?`


As a reception clerk, check in a visitor with appointment
(:class:`CheckinVisitor <lino_xl.lib.reception.CheckinVisitor>`)

- Note that the demo data is not very realistic here.

- Click on the first client mentioned in **Waiting visitors**.

- Click `Checkin` on one of the appointments mentioned there

- Confirm the dialog

- Note that a system note has been created.

EndCoaching

- :class:`EndCoaching <lino_welfare.modlib.pcsw.coaching.EndCoaching>`
  seems no longer used

- :class:`CreateClientVisit <lino_welfare.modlib.reception.CreateClientVisit>` 
- :class:`CreateCoachingVisit
  <lino_welfare.modlib.reception.CreateCoachingVisit>`




Managing Notifications
======================

I added filter parameters for :class:`Messages
<lino.modlib.notify.models.Messages>`.

I was not possible until now to override the `verbose_name` of the
:attr:`owner` field of a :class:`Controllable
<lino.modlib.gfks.mixins.Controllable>`.  Now it is possible using
:meth:`update_controller_field
<lino.modlib.gfks.mixins.Controllable.update_controller_field>`.


>>> ses = rt.login("robin")
>>> ses.show(rt.actors.notify.AllMessages)
===================== ======================================= ================== ====== =====================
 Created               Subject                                 Recipient          seen   sent
--------------------- --------------------------------------- ------------------ ------ ---------------------
 2014-05-22 05:48:00   The database has been initialized.      nicolas                   2014-05-22 05:48:00
 2014-05-22 05:48:00   La base de données a été initialisée.   Alicia Allmanns           2014-05-22 05:48:00
 2014-05-22 05:48:00   The database has been initialized.      Caroline Carnol           2014-05-22 05:48:00
 2014-05-22 05:48:00   The database has been initialized.      Hubert Huppertz           2014-05-22 05:48:00
 2014-05-22 05:48:00   The database has been initialized.      Judith Jousten            2014-05-22 05:48:00
 2014-05-22 05:48:00   The database has been initialized.      Kerstin Kerres            2014-05-22 05:48:00
 2014-05-22 05:48:00   La base de données a été initialisée.   Mélanie Mélard            2014-05-22 05:48:00
 2014-05-22 05:48:00   The database has been initialized.      Patrick Paraneau          2014-05-22 05:48:00
 2014-05-22 05:48:00   La base de données a été initialisée.   Romain Raffault           2014-05-22 05:48:00
 2014-05-22 05:48:00   Die Datenbank wurde initialisiert.      Rolf Rompen               2014-05-22 05:48:00
 2014-05-22 05:48:00   The database has been initialized.      Robin Rood                2014-05-22 05:48:00
 2014-05-22 05:48:00   The database has been initialized.      Theresia Thelen           2014-05-22 05:48:00
 2014-05-22 05:48:00   The database has been initialized.      Wilfried Willems          2014-05-22 05:48:00
===================== ======================================= ================== ====== =====================
<BLANKLINE>

>>> ses.show(rt.actors.notify.MyMessages)
===================== ==================================== ============== ==========
 Created               Subject                              Message Type   Workflow
--------------------- ------------------------------------ -------------- ----------
 2014-05-22 05:48:00   The database has been initialized.   System event   [✓]
===================== ==================================== ============== ==========
<BLANKLINE>

