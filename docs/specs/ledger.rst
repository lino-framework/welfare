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
:mod:`lino_welfare.modlib.ledger` (a thin extension of
:mod:`lino.modlib.ledger`), :mod:`lino.modlib.vatless` and
:mod:`lino.modlib.finan`.  

The :mod:`lino.modlib.accounts` plugin was already used before (for
:mod:`lino_welfare.modlib.debts`), but now we add a second account
chart:

>>> rt.show('accounts.AccountCharts')
========= ========= =================
 value     name      text
--------- --------- -----------------
 default   default   Default
 debts     debts     Debts mediation
========= ========= =================
<BLANKLINE>

General accounts
================

>>> rt.show(accounts.GroupsByChart, accounts.AccountCharts.default)
===== ====================== ====================== ====================== ============== =======================
 ref   Designation            Designation (fr)       Designation (de)       Account Type   Budget entries layout
----- ---------------------- ---------------------- ---------------------- -------------- -----------------------
 40    Receivables            Receivables            Receivables            Assets
 44    Liabilities            Obligations            Verpflichtungen        Assets
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
=========== ====================== ====================== ====================== ======================================
 Reference   Designation            Designation (fr)       Designation (de)       Voucher type
----------- ---------------------- ---------------------- ---------------------- --------------------------------------
 REG         Purchase invoices      Factures achat         Einkaufsrechnungen     Invoice (vatless.AccountInvoice)
 AAW         Payment instructions   Payment instructions   Payment instructions   Payment Order (finan.PaymentOrder)
 KBC         KBC                    KBC                    KBC                    Bank Statement (finan.BankStatement)
 POKBC       PO KBC                 PO KBC                 PO KBC                 Payment Order (finan.PaymentOrder)
=========== ====================== ====================== ====================== ======================================
<BLANKLINE>


The state of a voucher
=======================

Vouchers can be "draft", "registered" or "fixed". Draft vouchers can
be modified but are not yet visible as movements in the
ledger. Registered vouchers cannot be modified, but are visible as
movements in the ledger. Fixed is the same as registered, but cannot
be deregistered anymore.

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
    <span><b>Registered</b> &#8594; [&#9671;]</span>
    

Purchase invoices
=================

The demo database has one journal with **purchase invoices**,
referenced as "REG" (for German *Rechnungseingang*).

>>> jnl = rt.modules.ledger.Journal.get_by_ref('REG')
>>> jnl.voucher_type.table_class
<class 'lino.modlib.vatless.ui.InvoicesByJournal'>

The REG journal contains the following invoices:

>>> rt.show(rt.modules.vatless.InvoicesByJournal, jnl)
========= ========== =============================== ============== ========== ============ ================
 number    Date       Partner                         Amount         Due date   Author       Workflow
--------- ---------- ------------------------------- -------------- ---------- ------------ ----------------
 29        1/2/14     Niederau Eupen AG               165,28                    Robin Rood   **Registered**
 28        1/7/14     Ethias s.a.                     47,50                     Robin Rood   **Registered**
 27        1/12/14    Electrabel Customer Solutions   125,33                    Robin Rood   **Registered**
 26        1/17/14    Ragn-Sells AS                   29,95                     Robin Rood   **Registered**
 25        1/22/14    Maksu- ja tolliamet             172,83                    Robin Rood   **Registered**
 24        1/27/14    IIZI kindlustusmaakler AS       77,45                     Robin Rood   **Registered**
 23        2/1/14     Eesti Energia AS                155,28                    Robin Rood   **Registered**
 22        2/6/14     AS Matsalu Veevärk              37,50                     Robin Rood   **Registered**
 21        2/11/14    AS Express Post                 10,00                     Robin Rood   **Registered**
 20        2/16/14    Leffin Electronics              192,78                    Robin Rood   **Registered**
 19        2/21/14    Niederau Eupen AG               165,28                    Robin Rood   **Registered**
 18        2/26/14    Ethias s.a.                     47,50                     Robin Rood   **Registered**
 17        3/3/14     Electrabel Customer Solutions   125,33                    Robin Rood   **Registered**
 16        3/8/14     Ragn-Sells AS                   29,95                     Robin Rood   **Registered**
 15        3/13/14    Maksu- ja tolliamet             172,83                    Robin Rood   **Registered**
 14        3/18/14    IIZI kindlustusmaakler AS       77,45                     Robin Rood   **Registered**
 13        3/23/14    Eesti Energia AS                155,28                    Robin Rood   **Registered**
 12        3/28/14    AS Matsalu Veevärk              37,50                     Robin Rood   **Registered**
 11        4/2/14     AS Express Post                 10,00                     Robin Rood   **Registered**
 10        4/7/14     Leffin Electronics              192,78                    Robin Rood   **Registered**
 9         4/12/14    Niederau Eupen AG               165,28                    Robin Rood   **Registered**
 8         4/17/14    Ethias s.a.                     47,50                     Robin Rood   **Registered**
 7         4/22/14    Electrabel Customer Solutions   125,33                    Robin Rood   **Registered**
 6         4/27/14    Ragn-Sells AS                   29,95                     Robin Rood   **Registered**
 5         5/2/14     Maksu- ja tolliamet             172,83                    Robin Rood   **Registered**
 4         5/7/14     IIZI kindlustusmaakler AS       77,45                     Robin Rood   **Registered**
 3         5/12/14    Eesti Energia AS                155,28                    Robin Rood   **Registered**
 2         5/17/14    AS Matsalu Veevärk              37,50                     Robin Rood   **Registered**
 1         5/22/14    AS Express Post                 10,00                     Robin Rood   **Registered**
 1         12/28/13   Leffin Electronics              192,78                    Robin Rood   **Registered**
 **436**                                              **3 041,70**
========= ========== =============================== ============== ========== ============ ================
<BLANKLINE>

Let's have a closer look at one of them.  The partner (provider) is
#184, and the costs are distributed over three clients:
    
>>> obj = rt.modules.vatless.AccountInvoice.objects.get(id=3)
>>> obj.partner
Partner #184 (u'Eesti Energia AS')
>>> rt.show(rt.modules.vatless.ItemsByInvoice, obj)
============================ ============================================= ============ =============
 Client                       Account                                       Amount       Description
---------------------------- --------------------------------------------- ------------ -------------
 DENON Denis (180*)           (823/333/01) Vor. Kranken- u. Invalidengeld   29,95
 DOBBELSTEIN Dorothée (124)   (825/333/01) Vorschuss auf Familienzulage     120,00
 AUSDEMWALD Alfons (116)      (826/333/01) Vorschuss auf Arbeitslosengeld   5,33
 **Total (3 rows)**                                                         **155,28**
============================ ============================================= ============ =============
<BLANKLINE>

Note that the accounts are randomly generated. A real electricity
invoice would probably book to the same account for every item.

This invoice is registered, and ledger movements have been created:

>>> obj.state
<VoucherStates.registered:20>
>>> rt.show(rt.modules.ledger.MovementsByVoucher, obj)
========= ============================ ================== ============================================= ============ ============ ======= ===========
 Seq.No.   Client                       Partner            Account                                       Debit        Credit       Match   Satisfied
--------- ---------------------------- ------------------ --------------------------------------------- ------------ ------------ ------- -----------
 1         AUSDEMWALD Alfons (116)                         (826/333/01) Vorschuss auf Arbeitslosengeld   5,33                              No
 2         DOBBELSTEIN Dorothée (124)                      (825/333/01) Vorschuss auf Familienzulage     120,00                            No
 3         DENON Denis (180*)                              (823/333/01) Vor. Kranken- u. Invalidengeld   29,95                             No
 4                                      Eesti Energia AS   (4400) Suppliers                                           155,28               No
 **10**                                                                                                  **155,28**   **155,28**           **0**
========= ============================ ================== ============================================= ============ ============ ======= ===========
<BLANKLINE>



Purchase invoices
=================

>>> rt.login('robin').show(rt.modules.vatless.VouchersByPartner, obj.partner)
Create voucher in journal **Purchase invoices (REG)**

Our partner has sent several invoices:

>>> rt.show(rt.modules.ledger.MovementsByPartner, obj.partner)
==================== ========== ======= ============ ======= ======== ===========
 Date                 Voucher    Debit   Credit       Match   Client   Satisfied
-------------------- ---------- ------- ------------ ------- -------- -----------
 5/12/14              *REG#3*            155,28                        No
 3/23/14              *REG#13*           155,28                        No
 2/1/14               *REG#23*           155,28                        No
 **Total (3 rows)**                      **465,84**                    **0**
==================== ========== ======= ============ ======= ======== ===========
<BLANKLINE>



>>> client = rt.modules.pcsw.Client.objects.get(pk=180)
>>> print(client)
DENON Denis (180*)

Our client has invoices from different partners:

>>> rt.show(ledger.MovementsByProject, client)
===================== ========== ============================================= ========= ============ ======== ======= ===========
 Date                  Voucher    Account                                       Partner   Debit        Credit   Match   Satisfied
--------------------- ---------- --------------------------------------------- --------- ------------ -------- ------- -----------
 5/12/14               *REG#3*    (823/333/01) Vor. Kranken- u. Invalidengeld             29,95                         No
 5/7/14                *REG#4*    (832/330/02) Gesundheitsbeihilfe                        25,00                         No
 5/2/14                *REG#5*    (832/3331/01) Eingliederungseinkommen                   12,50                         No
 4/17/14               *REG#8*    (P87/000/00) Abhebung von pers. Guthaben                10,00                         No
 4/12/14               *REG#9*    (825/333/01) Vorschuss auf Familienzulage               5,33                          No
 4/7/14                *REG#10*   (832/330/03) Heizkosten- u. Energiebeihilfe             120,00                        No
 3/23/14               *REG#13*   (832/334/27) Sozialhilfe                                29,95                         No
 3/18/14               *REG#14*   (820/333/01) Vorschuss auf Vergütungen o.ä.             25,00                         No
 3/13/14               *REG#15*   (826/333/01) Vorschuss auf Arbeitslosengeld             12,50                         No
 2/26/14               *REG#18*   (832/330/03F) Fonds Gas und Elektrizität                10,00                         No
 2/21/14               *REG#19*   (832/3343/21) Beihilfe für Ausländer                    5,33                          No
 2/16/14               *REG#20*   (821/333/01) Vorschuss auf Pensionen                    120,00                        No
 2/1/14                *REG#23*   (827/333/01) Vorschuss auf Behindertenzulag             29,95                         No
 1/27/14               *REG#24*   (832/330/04) Mietkaution                                25,00                         No
 1/22/14               *REG#25*   (P82/000/00) Einn. Dritter: Weiterleitung               12,50                         No
 1/7/14                *REG#28*   (822/333/01) Vorsch. Entsch. Arbeitsunfälle             10,00                         No
 1/2/14                *REG#29*   (832/330/01) Allgemeine Beihilfen                       5,33                          No
 12/28/13              *REG#30*   (832/333/22) Mietbeihilfe                               120,00                        No
 **Total (18 rows)**                                                                      **608,34**                    **0**
===================== ========== ============================================= ========= ============ ======== ======= ===========
<BLANKLINE>


Movements
=========

>>> obj = accounts.Account.get_by_ref('820/333/01')
>>> print(unicode(obj))
(820/333/01) Vorschuss auf Vergütungen o.ä.

>>> rt.show(rt.modules.ledger.MovementsByAccount, obj)
==================== ========== ============ ======== ========= ======= ===========
 Date                 Voucher    Debit        Credit   Partner   Match   Satisfied
-------------------- ---------- ------------ -------- --------- ------- -----------
 5/22/14              *REG#1*    10,00                                   No
 4/17/14              *REG#8*    12,50                                   No
 3/18/14              *REG#14*   25,00                                   No
 2/16/14              *REG#20*   29,95                                   No
 1/12/14              *REG#27*   120,00                                  No
 **Total (5 rows)**              **197,45**                              **0**
==================== ========== ============ ======== ========= ======= ===========
<BLANKLINE>

Situation
=========

The :class:`lino.modlib.ledger.ui.Situation` report is one of the
well-known accounting documents. Since accounting in Lino Welfare is
not complete (it is just a *Nebenbuchhaltung*), there are no debtors
and thus the situation cannot be balanced.

TODO: 

- No "Actions" column in printed version.
- Report title not shown
- Report title must contain the date

>>> rt.show(ledger.Situation)  #doctest: +NORMALIZE_WHITESPACE
-------
Debtors
-------
<BLANKLINE>
List of partners (usually clients)     who are in debt towards us.
<BLANKLINE>
No data to display
---------
Creditors
---------
<BLANKLINE>
List of partners (usually suppliers)     who are giving credit to us.
<BLANKLINE>
========== ========== ================================= ============== ===============================
 Age        Due date   Partner                           Balance        Actions
---------- ---------- --------------------------------- -------------- -------------------------------
 145        12/28/13   *Leffin Electronics*              578,34         [Show debts] [Issue reminder]
 140        1/2/14     *Niederau Eupen AG*               495,84         [Show debts] [Issue reminder]
 135        1/7/14     *Ethias s.a.*                     142,50         [Show debts] [Issue reminder]
 130        1/12/14    *Electrabel Customer Solutions*   375,99         [Show debts] [Issue reminder]
 125        1/17/14    *Ragn-Sells AS*                   89,85          [Show debts] [Issue reminder]
 120        1/22/14    *Maksu- ja tolliamet*             518,49         [Show debts] [Issue reminder]
 115        1/27/14    *IIZI kindlustusmaakler AS*       232,35         [Show debts] [Issue reminder]
 110        2/1/14     *Eesti Energia AS*                465,84         [Show debts] [Issue reminder]
 105        2/6/14     *AS Matsalu Veevärk*              112,50         [Show debts] [Issue reminder]
 100        2/11/14    *AS Express Post*                 30,00          [Show debts] [Issue reminder]
 **1225**                                                **3 041,70**
========== ========== ================================= ============== ===============================
<BLANKLINE>

