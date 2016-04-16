.. _welfare.admin.printing:

===========================
Configuring print templates
===========================

.. How to test only this document:

     $ python setup.py test -s tests.AdminTests.test_printing

   Initialize doctest:

    >>> import os
    >>> os.environ['DJANGO_SETTINGS_MODULE'] = \
    ...    'lino_welfare.projects.std.settings.doctests'
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
    <class 'lino_welfare.modlib.cal.models.Event'>
    <class 'lino_xl.lib.excerpts.models.Excerpt'>
    <class 'lino_welfare.modlib.notes.models.Note'>
    <class 'lino_xl.lib.outbox.models.Mail'>

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
======================== ========= ============ ================= ================================
 Model                    Primary   Certifying   Template          Body template
------------------------ --------- ------------ ----------------- --------------------------------
 Income confirmation      Yes       Yes          Default.odt       certificate.body.html
 Refund confirmation      Yes       Yes          Default.odt       certificate.body.html
 Simple confirmation      Yes       Yes          Default.odt       certificate.body.html
 Art61 job supplyment     Yes       Yes                            contract.body.html
 Participant              Yes       No           Default.odt       presence_certificate.body.html
 IdentifyPerson Request   Yes       Yes
 ManageAccess Request     Yes       Yes
 Tx25 Request             Yes       Yes
 Partner                  No        No                             payment_reminder.body.html
 Budget                   Yes       Yes
 FSE Summary              Yes       Yes
 Immersion training       Yes       Yes                            immersion.body.html
 ISIP                     Yes       Yes
 Art60§7 job supplyment   Yes       Yes
 Client                   No        No           Default.odt       pac.body.html
 Client                   No        No           cv.odt
 Client                   Yes       No           file_sheet.odt
 Client                   No        No           eid-content.odt
======================== ========= ============ ================= ================================
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

