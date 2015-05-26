.. _welfare.specs.ledger:
===========================================
Ledger for Lino Welfare (Sozialbuchhaltung)
===========================================

Currently just collecting ideas.

We will add two new plugins :mod:`lino_welfare.modlib.ledger` and
:mod:`lino_welfare.modlib.finan` as extensions of
:mod:`lino.modlib.ledger` and :mod:`lino.modlib.finan` respectively.

In a first step, the important thing to add is the `recipient` concept
(Zahlungsempfänger), i.e. inject two fields `recipient` and
`bank_account` into the following models:

- into the *ledger.AccountInvoice* model
- into each *finan.FinancialVoucherItem*-based model
- into the *ledger.Movement* model

Since there is a lot of injection here, I start to wonder whether we
shouldn't rather do ticket :ticket:`246` (Work around inject_field)
first.  Also e.g. to define a choosers and validation methods for
these fields.
