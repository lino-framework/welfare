.. doctest docs/specs/ledger.rst
   
.. _welfare.specs.ledger:

===========================
Accounting for Lino Welfare
===========================

.. doctest init:

    >>> import lino
    >>> lino.startup('lino_welfare.projects.eupen.settings.doctests')
    >>> from etgen.html import E
    >>> from lino.api.doctest import *
    >>> from lino.api import rt

This document describes the functionalities for registering and
keeping track of social aid expenses, including client-related
refunding of certain costs, disbursements of regular monthly social
aid and communication with the bank in both directions.

These will partly turn Lino Welfare into an accounting package.
Actually it produces a *subledger*, i.e. manages only *a part of* a
complete accounting system.

A first prototype was developed between May 2015 and April 2016 as
ticket :ticket:`143` ("Nebenbuchhaltung Sozialhilfeausgaben") and
related tickets. The code examples may contain German texts for
practical reasons to facilitate analysis.

This document extends the following specifications:

- :ref:`cosi.specs.accounting`
- :ref:`cosi.specs.ledger`

This document is base for the following specifications:

- :doc:`vatless` 
- :doc:`finan`.



.. contents::
   :depth: 1
   :local:

Implementation notes
====================

This project integrates several plugins into Lino Welfare which are
also used by :ref:`cosi`: 

- :mod:`lino_welfare.modlib.ledger` is a thin extension of
  :mod:`lino_xl.lib.ledger`,
- :mod:`lino_xl.lib.vatless` is for VAT-less invoices (mostly
  incoming invoices)
- :mod:`lino_xl.lib.finan` is for "financial vouchers", i.e. bank
  statements, payment orders, journal entries.
  :mod:`lino_welfare.modlib.finan` extends this and adds a voucher
  type called "Disbursement orders". A disbursement order is similar
  to a payment order, but only used internally.


Some shortcuts:

>>> Journal = rt.models.ledger.Journal
>>> Journals = rt.models.ledger.Journals



Partner versus Project
======================

Accounting in Lino Welfare is special because every transaction
usually has *two* external partners: (1) the "beneficiary" or "client"
to which this transaction must be assigned and (2) the actual
recipient (or sender) of the payment.

The :attr:`project_model <lino_xl.lib.ledger.Plugin.project_model>`
of the ledger plugin is `contacts.Client`, which means that every
ledger movement can additionally point to a *client* as the "project".

The client of a transaction can be somebody else than the partner.

The following models are called "client related"
(:class:`lino_xl.lib.ledger.mixins.ProjectRelated` (don't mix that
up with :class:`lino.mixins.ProjectRelated`), i.e. can point to a
client:

>>> from lino_xl.lib.ledger.mixins import ProjectRelated
>>> # from lino.mixins import ProjectRelated
>>> for m in rt.models_by_base(ProjectRelated):
...     print(m)
<class 'lino_xl.lib.finan.models.BankStatementItem'>
<class 'lino_xl.lib.finan.models.JournalEntry'>
<class 'lino_xl.lib.finan.models.JournalEntryItem'>
<class 'lino_xl.lib.finan.models.PaymentOrderItem'>
<class 'lino_xl.lib.ledger.models.Movement'>
<class 'lino_xl.lib.vatless.models.AccountInvoice'>
<class 'lino_xl.lib.vatless.models.InvoiceItem'>


.. _wilfried:

The "accountant" user type
=============================

A demo user with the fictive name *Wilfried Willems* has the user
user_type of an accountant
(:class:`lino_welfare.modlib.welfare.roles.LedgerUser`).

>>> p = rt.login('wilfried').get_user().user_type
>>> print(p)
500 (Buchhalter)

Accountants have no direct contact with clients and probably won't use
the calendar.  But for the first prototype they get :class:`OfficeUser
<lino.modlib.office.roles.OfficeUser>` functionality so they can
decide themselves whether they want it.

>>> from lino.modlib.office.roles import OfficeUser
>>> p.has_required_roles([OfficeUser])
True

Here is the main menu for accountants:

>>> rt.login('wilfried').show_menu(language="de")
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF -SKIP
- Kontakte : Personen,  ▶ Klienten, Organisationen, -, Partner (alle), Haushalte
- Büro : Meine Benachrichtigungen, Meine Auszüge, Ablaufende Uploads, Meine Uploads, Mein E-Mail-Ausgang, Meine Ereignisse/Notizen
- Kalender : Kalender, Meine Termine, Unbestätigte Termine, Meine Aufgaben, Meine Gäste, Meine Anwesenheiten, Meine überfälligen Termine
- Empfang : Klienten, Termine heute, Wartende Besucher, Beschäftigte Besucher, Gegangene Besucher, Meine Warteschlange
- Buchhaltung :
  - Rechnungseingänge : Rechnungseingänge (REG), Sammelrechnungen (SREG)
  - Ausgabeanweisungen : Ausgabeanweisungen (AAW)
  - Zahlungsaufträge : KBC Zahlungsaufträge (ZKBC)
- Berichte :
  - Buchhaltung : Schuldner, Gläubiger
- Konfigurierung :
  - Büro : Meine Einfügetexte
  - ÖSHZ : Hilfearten, Kategorien
- Explorer :
  - Kontakte : Partner
  - ÖSHZ : Hilfebeschlüsse, Einkommensbescheinigungen, Kostenübernahmescheine, Einfache Bescheinigungen
  - Buchhaltung : Rechnungen
  - SEPA : Bankkonten, Importierte  Bankkonten, Kontoauszüge, Transaktionen
- Site : Info


General accounts ("budgetary articles")
=======================================

Belgian public instances use so-called budgetary articles (`Articles
budgétaires
<http://www.pouvoirslocaux.irisnet.be/fr/theme/finances/docfin/la-structure-dun-article-budgetaire>`_
in French, "Haushaltsartikel" in German) for classifying their
monetary transactions.  These budgetary articles are in public sector
accounting exactly what general accounts are in private sector
accounting.  It seems BTW that the usage of the term "budgetary
articles" is being replaced by the term "accounts".

The main difference is that they are structured differently.  The demo
database currently has a mixture of "PCMN style" and "public sector
style" references because Lino Welfare doesn't yet offer full
accounting reports (:mod:`lino_xl.lib.sheets`).

>>> rt.show(ledger.Accounts)
============= ==================================
 Referenz      Bezeichnung
------------- ----------------------------------
 1000          Net income (loss)
 4             Commercial assets & liabilities
 4000          Kunden
 4300          Offene Zahlungsaufträge
 4400          Lieferanten
 4450          Auszuführende Ausgabeanweisungen
 4500          Angestellte
 4510          Geschuldete Mehrwertsteuer
 4511          Rückzahlbare Mehrwertsteuer
 4512          Abziehbare Mehrwertsteuer
 4513          Deklarierte Mehrwertsteuer
 4600          Steuerämter
 4800          Granted aids
 4900          Wartekonto
 5             Financial assets & liabilities
 5500          BestBank
 5700          Kasse
 6             Ausgaben
 60            Diplome
 6010          Einkäufe von Dienstleistungen
 6020          Investierungskäufe
 6040          Wareneinkäufe
 61            Löhne und Gehälter
 6300          Löhne und Gehälter
 6900          Net income
 7             Revenues
 7000          Verkauf
 7900          Net loss
 820/333/01    Vorschuss auf Vergütungen o.ä.
 821/333/01    Vorschuss auf Pensionen
 822/333/01    Vorsch. Entsch. Arbeitsunfälle
 823/333/01    Vor. Kranken- u. Invalidengeld
 825/333/01    Vorschuss auf Familienzulage
 826/333/01    Vorschuss auf Arbeitslosengeld
 827/333/01    Vorschuss auf Behindertenzulag
 832/330/01    Allgemeine Beihilfen
 832/330/02    Gesundheitsbeihilfe
 832/330/03    Heizkosten- u. Energiebeihilfe
 832/330/03F   Fonds Gas und Elektrizität
 832/330/04    Mietkaution
 832/333/22    Mietbeihilfe
 832/3331/01   Eingliederungseinkommen
 832/334/27    Sozialhilfe
 832/3343/21   Beihilfe für Ausländer
 P82/000/00    Einn. Dritter: Weiterleitung
 P83/000/00    Unber. erh. Beträge + Erstatt.
 P87/000/00    Abhebung von pers. Guthaben
============= ==================================
<BLANKLINE>


Vouchers
========

A **voucher** (German *Beleg*) is a document which serves as legal
proof for a transaction. A transaction is a set of accounting
**movements** whose debit equals to their credit.

Lino Welfare uses the following **voucher types**:

>>> rt.show(ledger.VoucherTypes)
=================================== ====== =================================================
 Wert                                name   Text
----------------------------------- ------ -------------------------------------------------
 vatless.InvoicesByJournal                  Rechnungen
 vatless.ProjectInvoicesByJournal           Project invoices
 finan.JournalEntriesByJournal              Diverse Buchung (finan.JournalEntriesByJournal)
 finan.PaymentOrdersByJournal               Zahlungsauftrag (finan.PaymentOrdersByJournal)
 finan.BankStatementsByJournal              Kontoauszug (finan.BankStatementsByJournal)
 finan.DisbursementOrdersByJournal          Ausgabeanweisungen
=================================== ====== =================================================
<BLANKLINE>


Invoices are partner-related vouchers (often we simply say **partner
voucher**). That is, you select one partner per voucher. Every
partner-related voucher points to to one and only one partner. 

The other voucher types (Bank statements etc) are called **financial
vouchers**. Financial vouchers have their individual *entries*
partner-related, so the vouchers themselves are *not* related to a
single partner.

There are two types of invoice: those with only one project (client)
and those with more than one projects.

More about voucher types in
:class:`lino_xl.lib.ledger.choicelists.VoucherTypes`.

Journals
========

A :class:`Journal <lino_xl.lib.edger.models.Journal>` is a sequence
of numbered vouchers. All vouchers of a given journal are of same
type, but there may be more than one journal per voucher type.  The
demo database currently has the following journals defined:

>>> rt.show(Journals, column_names="ref name voucher_type journal_group")
========== ====================== ================================================ ====================
 Referenz   Bezeichnung            Belegart                                         Journalgruppe
---------- ---------------------- ------------------------------------------------ --------------------
 REG        Rechnungseingänge      Project invoices                                 Rechnungseingänge
 SREG       Sammelrechnungen       Rechnungen                                       Rechnungseingänge
 AAW        Ausgabeanweisungen     Ausgabeanweisungen                               Ausgabeanweisungen
 ZKBC       KBC Zahlungsaufträge   Zahlungsauftrag (finan.PaymentOrdersByJournal)   Zahlungsaufträge
========== ====================== ================================================ ====================
<BLANKLINE>

A default Lino Welfare has the following **journal groups**.

>>> rt.show(ledger.JournalGroups)
====== ====== ======================
 Wert   name   Text
------ ------ ----------------------
 10     bst    Bestellungen Einkauf
 20     reg    Rechnungseingänge
 30     ffo    Forderungen
 40     anw    Ausgabeanweisungen
 50     zau    Zahlungsaufträge
====== ====== ======================
<BLANKLINE>


The state of a voucher
=======================

.. lino2rst:: print(ledger.VoucherStates.__doc__)

>>> rt.show(ledger.VoucherStates)
====== ============ ================ ========
 Wert   name         Text             Symbol
------ ------------ ---------------- --------
 10     draft        Entwurf
 20     registered   Registriert
 30     signed       Unterschrieben
 40     cancelled    Storniert
====== ============ ================ ========
<BLANKLINE>

.. technical:

    The `VoucherStates` choicelist is used by two fields: one database
    field and one parameter field.

    >>> len(ledger.VoucherStates._fields)
    2
    >>> for f in ledger.VoucherStates._fields:
    ...     print(f)
    <lino.core.choicelists.ChoiceListField: state>
    ledger.Voucher.state

    >>> obj = vatless.AccountInvoice.objects.get(id=1)
    >>> ar = rt.login("robin").spawn(vatless.Invoices)
    >>> print(tostring(ar.get_data_value(obj, 'workflow_buttons')))
    <span><b>Registriert</b> → [Entwurf]</span>
    

Movements
=========

Users can consult the movements of a given general account.

>>> obj = ledger.Account.get_by_ref('820/333/01')
>>> print(str(obj))
(820/333/01) Vorschuss auf Vergütungen o.ä.

>>> rt.show(ledger.MovementsByAccount, obj)
========== =============== ================================================================ ============ ======== =======
 Valuta     Beleg           Beschreibung                                                     Debit        Kredit   Match
---------- --------------- ---------------------------------------------------------------- ------------ -------- -------
 22.05.14   *REG 1/2014*    *AS Express Post* / *AUSDEMWALD Alfons (116)*                    10,00
 03.03.14   *SREG 6/2014*   *Electrabel Customer Solutions* / *AUSDEMWALD Alfons (116)*      25,00
 03.03.14   *SREG 6/2014*   *Electrabel Customer Solutions* / *COLLARD Charlotte (118)*      149,95
 03.03.14   *SREG 6/2014*   *Electrabel Customer Solutions* / *DOBBELSTEIN Dorothée (124)*   125,33
 03.03.14   *SREG 6/2014*   *Electrabel Customer Solutions* / *EVERS Eberhart (127)*         10,00
 03.03.14   *SREG 6/2014*   *Electrabel Customer Solutions* / *EMONTS Daniel (128)*          12,50
                            **Saldo 332.78 (6 Bewegungen)**                                  **332,78**
========== =============== ================================================================ ============ ======== =======
<BLANKLINE>


