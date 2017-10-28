.. doctest docs/admin/printing.rst
.. _welfare.admin.printing:

===========================
Configuring print templates
===========================

.. Initialize doctest:

    >>> from lino import startup
    >>> startup('lino_welfare.projects.std.settings.doctests')
    >>> from lino.api.doctest import *
    

This document explains everything you need to know about how to
configure print templates in Lino Welfare.

.. contents::
   :local:

Which database objects are printable?
=====================================

While most database models in Lino Welfare are being printed using
excerpts (see `Excerpt types`_ below), some models still use the more
primitive direct printing method (see :ref:`lino.admin.printing`):

- :class:`notes.Note <lino_welfare.modlib.notes.models.Note>`,
  :class:`cal.Event<lino_welfare.modlib.cal.models.Event>` and
  :class:`outbox.Mail <lino.modlib.outbox.models.Mail>`.

- and of course :class:`excerpts.Excerpt
  <lino.modlib.excerpts.models.Excerpt>` itself

.. Here is a list of these models:

    >>> from lino.modlib.printing.mixins import Printable
    >>> for m in rt.models_by_base(Printable):
    ...     print m
    <class 'lino_welfare.modlib.aids.models.Granting'>
    <class 'lino_welfare.modlib.aids.models.IncomeConfirmation'>
    <class 'lino_welfare.modlib.aids.models.RefundConfirmation'>
    <class 'lino_welfare.modlib.aids.models.SimpleConfirmation'>
    <class 'lino_welfare.modlib.art61.models.Contract'>
    <class 'lino_welfare.modlib.cal.models.Event'>
    <class 'lino_welfare.modlib.cal.models.Guest'>
    <class 'lino_xl.lib.cal.models.RecurrentEvent'>
    <class 'lino_xl.lib.cal.models.Subscription'>
    <class 'lino_welfare.modlib.cal.models.Task'>
    <class 'lino_welfare.modlib.cbss.models.IdentifyPersonRequest'>
    <class 'lino_welfare.modlib.cbss.models.ManageAccessRequest'>
    <class 'lino_welfare.modlib.cbss.models.RetrieveTIGroupsRequest'>
    <class 'lino.modlib.checkdata.models.Problem'>
    <class 'lino_xl.lib.coachings.models.Coaching'>
    <class 'lino_welfare.modlib.contacts.models.Company'>
    <class 'lino_welfare.modlib.contacts.models.Partner'>
    <class 'lino_welfare.modlib.contacts.models.Person'>
    <class 'lino_welfare.projects.chatelet.modlib.courses.models.Course'>
    <class 'lino_welfare.projects.chatelet.modlib.courses.models.Enrolment'>
    <class 'lino_xl.lib.courses.models.Topic'>
    <class 'lino.modlib.dashboard.models.Widget'>
    <class 'lino_welfare.modlib.debts.models.Budget'>
    <class 'lino_welfare.modlib.esf.models.ClientSummary'>
    <class 'lino_xl.lib.excerpts.models.Excerpt'>
    <class 'lino_xl.lib.finan.models.BankStatement'>
    <class 'lino_xl.lib.finan.models.JournalEntry'>
    <class 'lino_xl.lib.finan.models.PaymentOrder'>
    <class 'lino_welfare.modlib.households.models.Household'>
    <class 'lino_welfare.modlib.immersion.models.Contract'>
    <class 'lino_welfare.modlib.isip.models.Contract'>
    <class 'lino_welfare.modlib.jobs.models.Contract'>
    <class 'lino_welfare.modlib.jobs.models.JobProvider'>
    <class 'lino_xl.lib.ledger.models.Voucher'>
    <class 'lino_welfare.modlib.newcomers.models.Competence'>
    <class 'lino_welfare.modlib.notes.models.Note'>
    <class 'lino.modlib.notify.models.Message'>
    <class 'lino_xl.lib.outbox.models.Mail'>
    <class 'lino_welfare.modlib.pcsw.models.Client'>
    <class 'lino_xl.lib.polls.models.Poll'>
    <class 'lino_xl.lib.polls.models.Response'>
    <class 'lino.modlib.tinymce.models.TextFieldTemplate'>
    <class 'lino_xl.lib.uploads.models.Upload'>
    <class 'lino.modlib.users.models.Authority'>
    <class 'lino_xl.lib.vatless.models.AccountInvoice'>
    <class 'lino_welfare.modlib.xcourses.models.CourseProvider'>

A logical consequence is that printing an object of one of above
models will *not* appear in the history of excerpts.

We did not yet test what happens if you define an excerpt type for one
of the above models.

For configuring the printing of these models, see
:ref:`lino.admin.printing`.


Main templates
==============

All main templates of a Lino Welfare default configuration are
LibreOffice `.odt` files because they use some subclass of
:class:`lino.modlib.printing.mixins.printable.AppyBuildMethod` as
:attr:`build_method
<lino.modlib.printing.mixins.printable.PrintableType.build_method>`.

See :lino:`Appy POD template syntax </admin/appy_templates>` for
documentation about the syntax and context variables available for
designing the template itself.


Excerpt types
=============  

See :ref:`lino.admin.excerpts` for a general introduction to
excerpt-based printing.

This is the list of excerpt types:

>>> rt.show(excerpts.ExcerptTypes,
... column_names="content_type primary certifying template body_template")
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
======================== ========= ============ ============================= ================================
 Model                    Primary   Certifying   Template                      Body template
------------------------ --------- ------------ ----------------------------- --------------------------------
 Income confirmation      Yes       Yes          Default.odt                   certificate.body.html
 Refund confirmation      Yes       Yes          Default.odt                   certificate.body.html
 Simple confirmation      Yes       Yes          Default.odt                   certificate.body.html
 Art61 job supplyment     Yes       Yes                                        contract.body.html
 Presence                 Yes       No           Default.odt                   presence_certificate.body.html
 IdentifyPerson Request   Yes       Yes
 ManageAccess Request     Yes       Yes
 Tx25 Request             Yes       Yes
 Partner                  No        No           payment_reminder.weasy.html
 Person                   No        No           TermsConditions.odt
 Enrolment                Yes       Yes                                        enrolment.body.html
 Budget                   Yes       Yes
 ESF Summary              Yes       Yes
 Bank Statement           Yes       Yes
 Journal Entry            Yes       Yes
 Payment Order            Yes       Yes
 Immersion training       Yes       Yes                                        immersion.body.html
 ISIP                     Yes       Yes
 Art60§7 job supplyment   Yes       Yes
 Client                   No        No           Default.odt                   pac.body.html
 Client                   No        No           cv.odt
 Client                   Yes       No           file_sheet.odt
 Client                   No        No           eid-content.odt
======================== ========= ============ ============================= ================================
<BLANKLINE>


Aid confirmations
=================

When printing *aid confirmations* (models inheriting from
:class:`aids.Confirmation
<lino_welfare.modlib.aids.mixins.Confirmation>`), Lino adds another
rule:

    The body template to be used when printing an *aid confirmation*
    is usually not configured on the *excerpt type* but on the *aid
    type*.  :attr:`AidType.body_template
    <lino_welfare.modlib.aids.models.AidType.body_template>` overrides
    :attr:`ExcerptType.body_template
    <lino.modlib.excerpts.models.ExcerptType.body_template>`.

