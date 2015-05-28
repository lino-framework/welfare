.. _welfare.specs.ledger:
===========================================
Ledger for Lino Welfare (Sozialbuchhaltung)
===========================================

This document describes the new functionalities implemented as a
project called "Sozialbuchhaltung" and started in May 2015.

.. contents::
   :depth: 1
   :local:

A tested document
=================

This document is being tested using doctest with the following
initializations:

>>> from __future__ import print_function
>>> import os
>>> os.environ['DJANGO_SETTINGS_MODULE'] = \
...    'lino_welfare.projects.std.settings.doctests'
>>> from lino.api.doctest import *

Implementation notes
====================

This project adds two new plugins :mod:`lino_welfare.modlib.ledger`
and :mod:`lino_welfare.modlib.finan`, which are extensions of
:mod:`lino.modlib.ledger` and :mod:`lino.modlib.finan` respectively.

A first important thing to add is the `recipient` concept
(Zahlungsempfänger), i.e. inject two fields `recipient` and
`bank_account` into the following models:

- into the *ledger.AccountInvoice* model
- into each *finan.FinancialVoucherItem*-based model
- into the *ledger.Movement* model

This is implemented as the
:class:`lino_welfare.modlib.ledger.mixins.PaymentRecipient` mixin.

>>> from lino_welfare.modlib.ledger.mixins import PaymentRecipient
>>> assert issubclass(ledger.AccountInvoice, PaymentRecipient)
>>> assert issubclass(finan.BankStatementItem, PaymentRecipient)
>>> assert issubclass(ledger.Movement, PaymentRecipient)

Since there is a lot of injection here, I start to wonder whether we
shouldn't rather do ticket :ticket:`246` (Work around inject_field)
first.  Also e.g. to define a choosers and validation methods for
these fields.
