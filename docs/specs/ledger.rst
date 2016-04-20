.. _welfare.specs.ledger:

===========================
Accounting for Lino Welfare
===========================

.. How to test only this document:

    $ python setup.py test -s tests.SpecsTests.test_ledger
    
    doctest init:

    >>> import lino ; lino.startup('lino_welfare.projects.eupen.settings.doctests')
    >>> from lino.utils.xmlgen.html import E
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

This document is based on and extends the following specifications:

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
  :mod:`lino_cosi.lib.ledger`,
- :mod:`lino_cosi.lib.vatless` is for VAT-less invoices (mostly
  incoming invoices)
- :mod:`lino_cosi.lib.finan` is for "financial vouchers", i.e. bank
  statements, payment orders, journal entries.
  :mod:`lino_welfare.modlib.finan` extends this and adds a voucher
  type called "Disbursement orders". A disbursement order is similar
  to a payment order, but only used internally.


Some shortcuts:

>>> Journal = rt.modules.ledger.Journal
>>> Journals = rt.modules.ledger.Journals



Partner versus Project
======================

Accounting in Lino Welfare is special because every transaction
usually has *two* external partners: (1) the "beneficiary" or "client"
to which this transaction must be assigned and (2) the actual
recipient (or sender) of the payment.

The :attr:`project_model <lino_cosi.lib.ledger.Plugin.project_model>`
of the ledger plugin is `contacts.Client`, which means that every
ledger movement can additionally point to a *client* as the "project".

The client of a transaction can be somebody else than the partner.

The following models are called "client related"
(:class:`lino_cosi.lib.ledger.mixins.ProjectRelated` (don't mix that
up with :class:`lino.mixins.ProjectRelated`), i.e. can point to a
client:

>>> from lino_cosi.lib.ledger.mixins import ProjectRelated
>>> # from lino.mixins import ProjectRelated
>>> for m in rt.models_by_base(ProjectRelated):
...     print m
<class 'lino_cosi.lib.finan.models.BankStatementItem'>
<class 'lino_cosi.lib.finan.models.JournalEntry'>
<class 'lino_cosi.lib.finan.models.JournalEntryItem'>
<class 'lino_cosi.lib.finan.models.PaymentOrderItem'>
<class 'lino_cosi.lib.ledger.models.Movement'>
<class 'lino_cosi.lib.vatless.models.AccountInvoice'>
<class 'lino_cosi.lib.vatless.models.InvoiceItem'>


.. _wilfried:

The "accountant" user profile
=============================

A demo user with the fictive name *Wilfried Willems* has the user
profile of an accountant
(:class:`lino_welfare.modlib.welfare.roles.LedgerUser`).

>>> p = rt.login('wilfried').get_user().profile
>>> print(p)
Buchhalter
>>> p.role.__class__
<class 'lino_welfare.modlib.welfare.roles.LedgerUser'>

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
- Büro : Ablaufende Uploads, Meine Uploads, Mein E-Mail-Ausgang, Meine Auszüge, Meine Ereignisse/Notizen
- Kalender : Kalender, Meine Termine, Meine Aufgaben, Meine Gäste, Meine Anwesenheiten
- Empfang : Klienten, Termine heute, Wartende Besucher, Beschäftigte Besucher, Gegangene Besucher, Meine Warteschlange
- Buchhaltung :
  - Rechnungseingänge : Rechnungseingänge (REG), Sammelrechnungen (SREG)
  - Ausgabeanweisungen : Ausgabeanweisungen (AAW)
  - Zahlungsaufträge : KBC Zahlungsaufträge (ZKBC)
- Berichte :
  - Buchhaltung : Situation, Tätigkeitsbericht, Schuldner, Gläubiger
- Konfigurierung :
  - Orte : Länder
  - Büro : Meine Einfügetexte
  - ÖSHZ : Hilfearten, Kategorien
  - Lebenslauf : Sprachen
- Explorer :
  - ÖSHZ : Hilfebeschlüsse, Einkommensbescheinigungen, Kostenübernahmescheine, Einfache Bescheinigungen
  - Buchhaltung : Rechnungen
  - SEPA : Bankkonten, Importierte  Bankkonten, Kontoauszüge, Transaktionen
- Site : Info


General accounts ("budgetary articles")
=======================================

German-speaking PCSWs are used to speak about "Haushaltsartikel" (and
not "Konto").  The official name is indeed `Articles budgétaires
<http://www.pouvoirslocaux.irisnet.be/fr/theme/finances/docfin/la-structure-dun-article-budgetaire>`_.
It seems that the usage of the term "budgetary articles" is being
replaced by the term "accounts".

Anyway, these budgetary articles are in social sector accounting
exactly what general accounts are in private sector accounting.

The account chart is made of two models: :class:`Account
<lino_cosi.lib.accounts.models.Account>` and :class:`Group
<lino_cosi.lib.accounts.models.Group>`.

>>> rt.show(accounts.Groups)
===== ======================== ===========
 ref   Bezeichnung              Kontenart
----- ------------------------ -----------
 40    Receivables              Vermögen
 44    Verpflichtungen          Vermögen
 55    Finanzinstitute          Vermögen
 58    Laufende Transaktionen   Vermögen
 6     Ausgaben                 Ausgaben
 7     Revenues                 Einkünfte
===== ======================== ===========
<BLANKLINE>

Some expenses accounts:

>>> expenses = accounts.Group.objects.get(ref="6")
>>> rt.show(accounts.AccountsByGroup, expenses, column_names="ref name")
============= ================================
 Referenz      Bezeichnung
------------- --------------------------------
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
============= ================================
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
:class:`lino_cosi.lib.ledger.choicelists.VoucherTypes`.

Journals
========

A :class:`Journal <lino_cosi.lib.edger.models.Journal>` is a sequence
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
====== ============ ================
 Wert   name         Text
------ ------------ ----------------
 10     draft        Entwurf
 20     registered   Registriert
 30     signed       Unterschrieben
====== ============ ================
<BLANKLINE>

.. technical:

    The `VoucherStates` choicelist is used by two fields: one database
    field and one parameter field.

    >>> len(ledger.VoucherStates._fields)
    2
    >>> for f in ledger.VoucherStates._fields:
    ...     model = getattr(f, 'model', None)
    ...     if model:
    ...        print("%s.%s.%s" % (model._meta.app_label, model.__name__, f.name))
    ledger.Voucher.state

    >>> obj = vatless.AccountInvoice.objects.get(id=1)
    >>> ar = rt.login("robin").spawn(vatless.Invoices)
    >>> print(E.tostring(ar.get_data_value(obj, 'workflow_buttons')))
    <span><b>Registriert</b> &#8594; [Entregistrieren]</span>
    

Movements
=========

Users can consult the movements of a given general account.

>>> obj = accounts.Account.get_by_ref('820/333/01')
>>> print(unicode(obj))
(820/333/01) Vorschuss auf Vergütungen o.ä.

>>> rt.show(ledger.MovementsByAccount, obj)
====================== ========== ===================================================== ============ ======== ======= ============
 Buchungsdatum          Beleg      Beschreibung                                          Debit        Kredit   Match   Befriedigt
---------------------- ---------- ----------------------------------------------------- ------------ -------- ------- ------------
 22.05.14               *REG 1*    *AS Express Post* / *AUSDEMWALD Alfons (116)*         10,00                         Ja
 16.02.14               *SREG 7*   *Leffin Electronics* / *AUSDEMWALD Alfons (116)*      29,95                         Ja
 16.02.14               *SREG 7*   *Leffin Electronics* / *DOBBELSTEIN Dorothée (124)*   5,33                          Ja
 16.02.14               *SREG 7*   *Leffin Electronics* / *COLLARD Charlotte (118)*      120,00                        Ja
 16.02.14               *SREG 7*   *Leffin Electronics* / *EMONTS Daniel (128)*          25,00                         Ja
 16.02.14               *SREG 7*   *Leffin Electronics* / *EVERS Eberhart (127)*         12,50                         Ja
 **Total (6 Zeilen)**                                                                    **202,78**
====================== ========== ===================================================== ============ ======== ======= ============
<BLANKLINE>


Situation
=========

The :class:`lino_cosi.lib.ledger.ui.Situation` report is one of the
well-known accounting documents. Since accounting in Lino Welfare is
not complete (it is just a *Nebenbuchhaltung*), there are no debtors
(Schuldner) and the situation is not expected to be balanced.

>>> rt.show(ledger.Situation)  #doctest: +NORMALIZE_WHITESPACE
---------
Schuldner
---------
<BLANKLINE>
List of partners who are in debt towards us (usually customers).
<BLANKLINE>
Keine Daten anzuzeigen
---------
Gläubiger
---------
<BLANKLINE>
List of partners who are giving credit to us (usually suppliers).
<BLANKLINE>
========== ============== =============================== ========== ============== ===============================
 Alter      Zahlungsziel   Partner                         ID         Saldo          Aktionen
---------- -------------- ------------------------------- ---------- -------------- -------------------------------
 129        13.01.14       Electrabel Customer Solutions   226        562,78         [Show debts] [Issue reminder]
 129        13.01.14       Ethias s.a.                     227        93,44          [Show debts] [Issue reminder]
 129        13.01.14       Leffin Electronics              229        210,61         [Show debts] [Issue reminder]
 129        13.01.14       Niederau Eupen AG               228        342,78         [Show debts] [Issue reminder]
 98         13.02.14       AS Express Post                 220        232,78         [Show debts] [Issue reminder]
 98         13.02.14       AS Matsalu Veevärk              221        217,78         [Show debts] [Issue reminder]
 98         13.02.14       Eesti Energia AS                222        262,78         [Show debts] [Issue reminder]
 98         13.02.14       IIZI kindlustusmaakler AS       223        220,23         [Show debts] [Issue reminder]
 98         13.02.14       Maksu- ja tolliamet             224        372,78         [Show debts] [Issue reminder]
 98         13.02.14       Ragn-Sells AS                   225        142,68         [Show debts] [Issue reminder]
 **1104**                                                  **2245**   **2 658,64**
========== ============== =============================== ========== ============== ===============================
<BLANKLINE>


TODO in above report: 

- Hide "Actions" column in printed version.
- :ticket:`666` (Report title not shown, Report title must contain the date, ...)



.. _welfare.specs.r20160105:


>>> 1+1
2

Some choices requests
=====================

>>> ContentType = contenttypes.ContentType
>>> InvoiceItem = vatless.InvoiceItem
>>> BankStatement = finan.BankStatement
>>> kw = dict()
>>> fields = 'count rows'
>>> mt = ContentType.objects.get_for_model(InvoiceItem).pk
>>> demo_get(
...    'wilfried', 'choices/vatless/ItemsByProjectInvoice/account',
...    fields, 19, mt=mt, mk=1, **kw)

>>> mt = ContentType.objects.get_for_model(BankStatement).pk
>>> demo_get(
...    'wilfried', 'choices/finan/ItemsByBankStatement/match',
...    fields, 81, mt=mt, mk=132, **kw)

