.. _welfare.specs.ledger:

=======================
Ledger for Lino Welfare
=======================

.. How to test only this document:

    $ python setup.py test -s tests.SpecsTests.test_ledger
    
    doctest init:

    >>> from __future__ import print_function
    >>> import os
    >>> os.environ['DJANGO_SETTINGS_MODULE'] = \
    ...    'lino_welfare.projects.std.settings.doctests'
    >>> from lino.utils.xmlgen.html import E
    >>> from lino.api.doctest import *
    >>> from lino.api import rt

This document describes the new functionalities added between May and
September 2015 as a project called "Nebenbuchhaltung
Sozialhilfeausgaben" (:ticket:`143`).

.. contents::
   :depth: 1
   :local:

Implementation notes
====================

This project integrates several plugins into Lino Welfare:
:mod:`lino.modlib.ledger`, :mod:`lino.modlib.vatless` and
:mod:`lino.modlib.finan`.  

The :mod:`lino.modlib.accounts` plugin was already used before (for
:mod:`lino_welfare.modlib.debts`), but now we add a second account
chart.

>>> rt.show('accounts.AccountCharts')
========= ========= =================
 value     name      text
--------- --------- -----------------
 default   default   Default
 debts     debts     Debts mediation
========= ========= =================
<BLANKLINE>


Vouchers
========

A **voucher** (German *Beleg*) is a document which serves as legal
proof for a transaction. A transaction is a set of accounting
**movements** whose debit equals to their credit.

Lino Welfare uses the following **voucher types**:

>>> rt.show(rt.modules.ledger.VoucherTypes)
======================== ====== ======================================
 value                    name   text
------------------------ ------ --------------------------------------
 vatless.AccountInvoice          Invoice (vatless.AccountInvoice)
 finan.JournalEntry              Journal Entry (finan.JournalEntry)
 finan.PaymentOrder              Payment Order (finan.PaymentOrder)
 finan.BankStatement             Bank Statement (finan.BankStatement)
 finan.Grouper                   Grouper (finan.Grouper)
======================== ====== ======================================
<BLANKLINE>

The first one (Invoice) is a partner-related voucher (often we simply
say **partner voucher**). That is, you select one partner per
voucher. Every partner-related voucher points to to one and only one
partner.

The other voucher types (Bank statements etc) are called **financial
vouchers**. Financial vouchers have their individual *entries*
partner-related, so the vouchers themselves are *not* related to a
single partner.

More about voucher types in
:class:`lino.modlib.ledger.choicelists.VoucherTypes`.

Journals
========

A **journal** is a sequence of numbered vouchers. All vouchers of a
given journal are of same type, but there may be more than one journal
per voucher type.  The demo database currently has the following
journals defined:

>>> rt.show(rt.modules.ledger.Journals, column_names="ref name voucher_type")
=========== =================== ================== ==================== ======================================
 Reference   Designation         Designation (fr)   Designation (de)     Voucher type
----------- ------------------- ------------------ -------------------- --------------------------------------
 PRC         Purchase invoices   Factures achat     Einkaufsrechnungen   Invoice (vatless.AccountInvoice)
 KBC         KBC                 KBC                KBC                  Bank Statement (finan.BankStatement)
 POKBC       PO KBC              PO KBC             PO KBC               Payment Order (finan.PaymentOrder)
=========== =================== ================== ==================== ======================================
<BLANKLINE>


The state of a voucher
=======================

Vouchers can be "draft" or "registered". Draft vouchers can be
modified but are not yet visible as movements in the
ledger. Registered vouchers cannot be modified, but are visible as
movements in the ledger.

>>> rt.show(rt.modules.ledger.VoucherStates)
======= ============ ============
 value   name         text
------- ------------ ------------
 10      draft        Draft
 20      registered   Registered
 30      fixed        Fixed
======= ============ ============
<BLANKLINE>

.. technical:

    The `VoucherStates` choicelist is used by two fields: one database
    field and one parameter field.

    >>> len(rt.modules.ledger.VoucherStates._fields)
    2
    >>> for f in rt.modules.ledger.VoucherStates._fields:
    ...     model = getattr(f, 'model', None)
    ...     if model:
    ...        print("%s.%s.%s" % (model._meta.app_label, model.__name__, f.name))
    ledger.Voucher.state

    >>> obj = rt.modules.vatless.AccountInvoice.objects.get(id=1)
    >>> ar = rt.login("robin").spawn(rt.modules.vatless.Invoices)
    >>> print(E.tostring(obj.workflow_buttons(ar)))
    <span><b>Registered</b> &#8594; [Deregister]</span>
    
Here is an overview of all purchase invoices contained in the demo
database:

>>> jnl = rt.modules.ledger.Journal.get_by_ref('PRC')
>>> rt.show(rt.modules.vatless.InvoicesByJournal, jnl)
========= ========= ============================ ======================== ============ ========== ============ ================
 number    Date      Client                       Partner                  Amount       Due date   Author       Workflow
--------- --------- ---------------------------- ------------------------ ------------ ---------- ------------ ----------------
 20        2/16/14   BRECHT Bernd (177)           Bäckerei Schmitz         5,33                    Robin Rood   **Registered**
 19        2/21/14                                Bäckerei Mießen          120,00                  Robin Rood   **Registered**
 18        2/26/14   AUSDEMWALD Alfons (116)      Bäckerei Ausdemwald      29,95                   Robin Rood   **Registered**
 17        3/3/14    DOBBELSTEIN Dorothée (124)   Rumma & Ko OÜ            25,00                   Robin Rood   **Registered**
 16        3/8/14    DENON Denis (180*)           Belgisches Rotes Kreuz   22,50                   Robin Rood   **Registered**
 15        3/13/14   COLLARD Charlotte (118)      Bäckerei Schmitz         5,33                    Robin Rood   **Registered**
 14        3/18/14   BRECHT Bernd (177)           Bäckerei Mießen          120,00                  Robin Rood   **Registered**
 13        3/23/14   AUSDEMWALD Alfons (116)      Bäckerei Ausdemwald      29,95                   Robin Rood   **Registered**
 12        3/28/14   DOBBELSTEIN Dorothée (124)   Rumma & Ko OÜ            25,00                   Robin Rood   **Registered**
 11        4/2/14    DENON Denis (180*)           Belgisches Rotes Kreuz   22,50                   Robin Rood   **Registered**
 10        4/7/14                                 Bäckerei Schmitz         5,33                    Robin Rood   **Registered**
 9         4/12/14   COLLARD Charlotte (118)      Bäckerei Mießen          120,00                  Robin Rood   **Registered**
 8         4/17/14   BRECHT Bernd (177)           Bäckerei Ausdemwald      29,95                   Robin Rood   **Registered**
 7         4/22/14   AUSDEMWALD Alfons (116)      Rumma & Ko OÜ            25,00                   Robin Rood   **Registered**
 6         4/27/14   DOBBELSTEIN Dorothée (124)   Belgisches Rotes Kreuz   22,50                   Robin Rood   **Registered**
 5         5/2/14    DENON Denis (180*)           Bäckerei Schmitz         5,33                    Robin Rood   **Registered**
 4         5/7/14    COLLARD Charlotte (118)      Bäckerei Mießen          120,00                  Robin Rood   **Registered**
 3         5/12/14   BRECHT Bernd (177)           Bäckerei Ausdemwald      29,95                   Robin Rood   **Registered**
 2         5/17/14   AUSDEMWALD Alfons (116)      Rumma & Ko OÜ            25,00                   Robin Rood   **Registered**
 1         5/22/14                                Belgisches Rotes Kreuz   22,50                   Robin Rood   **Registered**
 **210**                                                                   **811,12**
========= ========= ============================ ======================== ============ ========== ============ ================
<BLANKLINE>
    
>>> obj = rt.modules.vatless.AccountInvoice.objects.get(id=1)
>>> obj.state
<VoucherStates.registered:20>



>>> rt.show(rt.modules.ledger.MovementsByVoucher, obj)
========= ============================================= =========== =========== ======= ===========
 Seq.No.   Account                                       Debit       Credit      Match   Satisfied
--------- --------------------------------------------- ----------- ----------- ------- -----------
 1         (820/333/01) Vorschuss auf Vergütungen o.ä.   10,00                           No
 2         (821/333/01) Vorschuss auf Pensionen          12,50                           No
 3         (4400) Suppliers                                          22,50               No
 **6**                                                   **22,50**   **22,50**           **0**
========= ============================================= =========== =========== ======= ===========
<BLANKLINE>




Partners and Clients
====================

Every partner voucher (and every entry of a financial voucher) is
related not only to a "partner" (or "payment recipient") but also to a
"client".  Lino Welfare does not currently allow to register invoices
containing amounts for several clients at once.


Client contacts
===============

>>> rt.show('pcsw.ClientContactTypes', column_names="id name can_refund")
==== ========================= ============================ ===================== ============
 ID   Designation               Designation (fr)             Designation (de)      Can refund
---- ------------------------- ---------------------------- --------------------- ------------
 1    Pharmacy                  Pharmacie                    Apotheke              No
 2    Health insurance          Caisse d'assurance maladie   Krankenkasse          No
 3    Advocate                  Avocat                       Rechtsanwalt          No
 4    Bailiff                   Huissier                     Gerichtsvollzieher    No
 5    Debt collecting company   Debt collecting company      Inkasso-Unternehmen   No
 6    Employment office         Bureau de chômage            Arbeitsvermittler     No
 7    Physician                 Médecin                      Arzt                  Yes
 8    Family doctor             Médecin traitant             Hausarzt              Yes
 9    Dentist                   Dentiste                     Zahnarzt              Yes
 10   Pediatrician              Pédiatre                     Kinderarzt            Yes
                                                                                   **4**
==== ========================= ============================ ===================== ============
<BLANKLINE>

Purchase invoices
=================

>>> partner = rt.modules.contacts.Company.objects.get(pk=100)
>>> print(partner)
Belgisches Rotes Kreuz

>>> client = rt.modules.pcsw.Client.objects.get(pk=180)
>>> print(client)
DENON Denis (180*)

>>> rt.login('robin').show(rt.modules.vatless.VouchersByPartner, partner)
Create voucher in journal **Purchase invoices (PRC)**

>>> rt.login('robin').show(rt.modules.vatless.VouchersByProject, client)
Create voucher in journal **Purchase invoices (PRC)**

Our partner has sent several invoices for different clients:

>>> rt.show(rt.modules.ledger.MovementsByPartner, partner)
==================== ========== ======= =========== ======= ============================ ===========
 Date                 Voucher    Debit   Credit      Match   Client                       Satisfied
-------------------- ---------- ------- ----------- ------- ---------------------------- -----------
 5/22/14              *PRC#1*            22,50                                            No
 4/27/14              *PRC#6*            22,50               DOBBELSTEIN Dorothée (124)   No
 4/2/14               *PRC#11*           22,50               DENON Denis (180*)           No
 3/8/14               *PRC#16*           22,50               DENON Denis (180*)           No
 **Total (4 rows)**                      **90,00**                                        **0**
==================== ========== ======= =========== ======= ============================ ===========
<BLANKLINE>

Our client has several invoices from different partners:

>>> rt.show(ledger.MovementsByProject, client)
==================== ========== ======================== ======= =========== ======= ===========
 Date                 Voucher    Partner                  Debit   Credit      Match   Satisfied
-------------------- ---------- ------------------------ ------- ----------- ------- -----------
 5/2/14               *PRC#5*    Bäckerei Schmitz                 5,33                No
 4/2/14               *PRC#11*   Belgisches Rotes Kreuz           22,50               No
 3/8/14               *PRC#16*   Belgisches Rotes Kreuz           22,50               No
 **Total (3 rows)**                                               **50,33**           **0**
==================== ========== ======================== ======= =========== ======= ===========
<BLANKLINE>



General accounts
================

>>> rt.show(accounts.GroupsByChart, accounts.AccountCharts.default)
===== ====================== ====================== ====================== ============== =======================
 ref   Designation            Designation (fr)       Designation (de)       Account Type   Budget entries layout
----- ---------------------- ---------------------- ---------------------- -------------- -----------------------
 40    Receivables            Receivables            Receivables            Assets
 44    Suppliers              Suppliers              Suppliers              Assets
 55    Financial institutes   Financial institutes   Financial institutes   Assets
 58    Current transactions   Current transactions   Current transactions   Assets
 6     Expenses               Dépenses               Ausgaben               Expenses
 7     Revenues               Revenues               Revenues               Incomes
===== ====================== ====================== ====================== ============== =======================
<BLANKLINE>

>>> expenses = accounts.Group.objects.get(ref="6")
>>> rt.show(accounts.AccountsByGroup, expenses, column_names="ref name")
============= ================================ ================================ ================================
 Reference     Designation                      Designation (fr)                 Designation (de)
------------- -------------------------------- -------------------------------- --------------------------------
 820/333/01    Vorschuss auf Vergütungen o.ä.   Vorschuss auf Vergütungen o.ä.   Vorschuss auf Vergütungen o.ä.
 821/333/01    Vorschuss auf Pensionen          Vorschuss auf Pensionen          Vorschuss auf Pensionen
 822/333/01    Vorsch. Entsch. Arbeitsunfälle   Vorsch. Entsch. Arbeitsunfälle   Vorsch. Entsch. Arbeitsunfälle
 823/333/01    Vor. Kranken- u. Invalidengeld   Vor. Kranken- u. Invalidengeld   Vor. Kranken- u. Invalidengeld
 825/333/01    Vorschuss auf Familienzulage     Vorschuss auf Familienzulage     Vorschuss auf Familienzulage
 826/333/01    Vorschuss auf Arbeitslosengeld   Vorschuss auf Arbeitslosengeld   Vorschuss auf Arbeitslosengeld
 827/333/01    Vorschuss auf Behindertenzulag   Vorschuss auf Behindertenzulag   Vorschuss auf Behindertenzulag
 832/330/01    Allgemeine Beihilfen             Allgemeine Beihilfen             Allgemeine Beihilfen
 832/330/02    Gesundheitsbeihilfe              Gesundheitsbeihilfe              Gesundheitsbeihilfe
 832/330/03    Heizkosten- u. Energiebeihilfe   Heizkosten- u. Energiebeihilfe   Heizkosten- u. Energiebeihilfe
 832/330/03F   Fonds Gas und Elektrizität       Fonds Gas und Elektrizität       Fonds Gas und Elektrizität
 832/330/04    Mietkaution                      Mietkaution                      Mietkaution
 832/333/22    Mietbeihilfe                     Mietbeihilfe                     Mietbeihilfe
 832/3331/01   Eingliederungseinkommen          Eingliederungseinkommen          Eingliederungseinkommen
 832/334/27    Sozialhilfe                      Sozialhilfe                      Sozialhilfe
 832/3343/21   Beihilfe für Ausländer           Beihilfe für Ausländer           Beihilfe für Ausländer
 P82/000/00    Einn. Dritter: Weiterleitung     Einn. Dritter: Weiterleitung     Einn. Dritter: Weiterleitung
 P83/000/00    Unber. erh. Beträge + Erstatt.   Unber. erh. Beträge + Erstatt.   Unber. erh. Beträge + Erstatt.
 P87/000/00    Abhebung von pers. Guthaben      Abhebung von pers. Guthaben      Abhebung von pers. Guthaben
============= ================================ ================================ ================================
<BLANKLINE>


>>> obj = accounts.Account.get_by_ref('820/333/01')
>>> print(unicode(obj))
(820/333/01) Vorschuss auf Vergütungen o.ä.

>>> rt.show(rt.modules.ledger.MovementsByAccount, obj)
==================== ========== =========== ======== ========= ======= ===========
 Date                 Voucher    Debit       Credit   Partner   Match   Satisfied
-------------------- ---------- ----------- -------- --------- ------- -----------
 5/22/14              *PRC#1*    10,00                                  No
 3/8/14               *PRC#16*   12,50                                  No
 **Total (2 rows)**              **22,50**                              **0**
==================== ========== =========== ======== ========= ======= ===========
<BLANKLINE>



Relics
======

The following is no longer valid.

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

>> from lino_welfare.modlib.ledger.mixins import PaymentRecipient
>> assert issubclass(ledger.AccountInvoice, PaymentRecipient)
>> assert issubclass(finan.BankStatementItem, PaymentRecipient)
>> assert issubclass(ledger.Movement, PaymentRecipient)

Since there is a lot of injection here, I start to wonder whether we
shouldn't rather do ticket :ticket:`246` (Work around inject_field)
first.  Also e.g. to define a choosers and validation methods for
these fields.

