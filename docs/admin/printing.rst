===========================
Configuring print templates
===========================

.. How to test only this document:
   $ python setup.py test -s tests.AdminTests.test_printing

This document explains everything you need to know about how to
configure print templates in Lino Welfare.

.. contents::
   :local:

.. Initialize

    >>> from __future__ import print_function
    >>> import os
    >>> os.environ['DJANGO_SETTINGS_MODULE'] = \
    ...    'lino_welfare.projects.std.settings.doctests'
    >>> from lino.api.doctest import *

Excerpt-based versus direct printing
====================================

While most database models in Lino Welfare are being printed using
excerpts (see :ref:`lino.admin.excerpts`), some models still use the
more primitive direct printing method (:ref:`lino.admin.printable`).
Here is a list of these models:

>>> from lino.mixins.printable import Printable
>>> for m in rt.models_by_base(Printable):
...     if m is not rt.modules.excerpts.Excerpt:
...         print dd.full_model_name(m)
cbss.IdentifyPersonRequest
cbss.ManageAccessRequest
cbss.RetrieveTIGroupsRequest
outbox.Mail
notes.Note
cal.Event

We did not yet test what happens if you define an excerpt type for one
of the above models.

A logical consequence is that printing an object of one of above
models will *not* appear in any history of excerpts.


Main templates
==============

All main templates of a Lino Welfare default configuration are
LibreOffice `.odt` files because they use some subclass of
:class:`lino.mixins.printable.AppyBuildMethod` as :attr:`build_method
<lino.mixins.printable.PrintableType.build_method>`.

See :lino:`Appy POD template syntax </admin/appy_templates>` for
documentation about the syntax and context variables available for
designing the template itself.


Excerpt types
=============  

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
 Art61 job supplyment     Yes       Yes          Default.odt       contract.body.html
 Participant              Yes       No           Default.odt       presence_certificate.body.html
 Budget                   Yes       Yes          Default.odt
 Immersion training       Yes       Yes          Default.odt       immersion.body.html
 ISIP                     Yes       Yes          Default.odt
 Art60§7 job supplyment   Yes       Yes          Default.odt
 Client                   No        No           Default.odt       pac.body.html
 Client                   No        No           cv.odt
 Client                   Yes       No           file_sheet.odt
 Client                   No        No           eid-content.odt
 **Total (13 rows)**      **10**    **8**
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

