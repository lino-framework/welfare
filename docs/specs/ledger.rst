.. _welfare.specs.ledger:

=======================
Ledger for Lino Welfare
=======================

.. How to test only this document:

    $ python setup.py test -s tests.SpecsTests.test_ledger
    
    doctest init:

    >>> from __future__ import print_function
    >>> import lino ; lino.startup('lino_welfare.projects.eupen.settings.doctests')
    >>> from lino.utils.xmlgen.html import E
    >>> from lino.api.doctest import *
    >>> from lino.api import rt

This document describes the functionalities for registering social aid
expenses like client-related payments of monthly social aid and
refunding of certain costs, including communication with the bank in
both directions.  This will partly turn Lino Welfare into an
accounting package (or at least a subledger).

A first prototype was developed between May and December 2015 as
ticket :ticket:`143` ("Nebenbuchhaltung Sozialhilfeausgaben") and
child tickets. The code examples contain German texts for practical
reasons to facilitate analysis.

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


>>> rt.show(ledger.VoucherTypes)
=================================== ====== =====================================================
 Wert                                name   Text
----------------------------------- ------ -----------------------------------------------------
 finan.JournalEntriesByJournal              Diverse Buchung (finan.JournalEntriesByJournal)
 finan.PaymentOrdersByJournal               Zahlungsauftrag (finan.PaymentOrdersByJournal)
 finan.BankStatementsByJournal              Kontoauszug (finan.BankStatementsByJournal)
 finan.DisbursementOrdersByJournal          Zahlungsauftrag (finan.DisbursementOrdersByJournal)
 vatless.InvoicesByJournal                  Rechnung (vatless.InvoicesByJournal)
 vatless.ProjectInvoicesByJournal           Rechnung (vatless.ProjectInvoicesByJournal)
=================================== ====== =====================================================
<BLANKLINE>


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
  - Finanzjournale : KBC (KBC)
- Berichte :
  - Buchhaltung : Situation, Tätigkeitsbericht, Schuldner, Gläubiger
- Konfigurierung :
  - Orte : Länder
  - Büro : Meine Einfügetexte
  - ÖSHZ : Hilfearten, Kategorien
  - Lebenslauf : Sprachen
- Explorer :
  - ÖSHZ : Hilfebeschlüsse, Einkommensbescheinigungen, Kostenübernahmescheine, Einfache Bescheinigungen
  - Buchhaltung : Journalgruppen, Rechnungen
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

>>> rt.show(rt.modules.ledger.VoucherTypes)
==================================== ====== ======================================================
 Wert                                 name   Text
------------------------------------ ------ ------------------------------------------------------
 finan.JournalEntriesByJournal               Diverse Buchung (finan.JournalEntriesByJournal)
 finan.PaymentOrdersByJournal                Zahlungsauftrag (finan.PaymentOrdersByJournal)
 finan.BankStatementsByJournal               Kontoauszug (finan.BankStatementsByJournal)
 finan.PaymentInstructionsByJournal          Zahlungsauftrag (finan.PaymentInstructionsByJournal)
 vatless.InvoicesByJournal                   Rechnung (vatless.InvoicesByJournal)
 vatless.ProjectInvoicesByJournal            Rechnung (vatless.ProjectInvoicesByJournal)
==================================== ====== ======================================================
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

>>> rt.show(rt.modules.ledger.Journals, column_names="ref name voucher_type journal_group")
========== ====================== ======================================================
 Referenz   Bezeichnung            Belegart
---------- ---------------------- ------------------------------------------------------
 REG        Rechnungseingänge      Rechnung (vatless.ProjectInvoicesByJournal)
 SREG       Sammelrechnungen       Rechnung (vatless.InvoicesByJournal)
 AAW        Zahlungsanweisungen    Zahlungsauftrag (finan.PaymentInstructionsByJournal)
 KBC        KBC                    Kontoauszug (finan.BankStatementsByJournal)
 ZKBC       KBC Zahlungsaufträge   Zahlungsauftrag (finan.PaymentOrdersByJournal)
========== ====================== ======================================================
<BLANKLINE>

A default Lino Welfare has the following **journal groups**.

>>> rt.show(ledger.JournalGroups)
====== ====== =======================
 Wert   name   Text
------ ------ -----------------------
 10     bst    Bestellungen Einkauf
 20     reg    Rechnungseingänge
 30     ffo    Forderungen
 40     anw    Ausgabeanweisungen
 50     zau    Zahlungsaufträge
 60     tre    Finanzjournale
 70     hhh    Haushalt und Rechnung
 80     dom    Domizilierungen
 90     clo    Abschlussbuchungen
====== ====== =======================
<BLANKLINE>



The state of a voucher
=======================

Vouchers can be "draft", "registered" or "fixed". Draft vouchers can
be modified but are not yet visible as movements in the
ledger. Registered vouchers cannot be modified, but are visible as
movements in the ledger. Fixed is the same as registered, but cannot
be deregistered anymore.

>>> rt.show(rt.modules.ledger.VoucherStates)
====== ============ =============
 Wert   name         Text
------ ------------ -------------
 10     draft        Entwurf
 20     registered   Registriert
 30     fixed        Fixed
====== ============ =============
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
    >>> print(E.tostring(ar.get_data_value(obj, 'workflow_buttons')))
    <span><b>Registriert</b> &#8594; [Entregistrieren]</span>
    

Simple incoming invoices
========================

The demo database has two journals with **incoming invoices**,
referenced as "REG" (for German *Rechnungseingang*) and SREG
(*Sammelrechnungen*).

>>> jnl = rt.modules.ledger.Journal.get_by_ref('REG')

The REG journal contains the following invoices:

>>> # rt.show(rt.modules.vatless.InvoicesByJournal, jnl)
>>> rt.show(jnl.voucher_type.table_class, jnl)
========= ============ ============================ =============================== ============ ============== ================== =================
 number    Belegdatum   Klient                       Partner                         Betrag       Zahlungsziel   Autor              Arbeitsablauf
--------- ------------ ---------------------------- ------------------------------- ------------ -------------- ------------------ -----------------
 1         27.12.13     EVERS Eberhart (127)         Leffin Electronics              12,50        27.01.14       Wilfried Willems   **Registriert**
 19        06.01.14     EVERS Eberhart (127)         Ethias s.a.                     5,33         06.02.14       Wilfried Willems   **Registriert**
 18        11.01.14     COLLARD Charlotte (118)      Electrabel Customer Solutions   120,00       11.02.14       Wilfried Willems   **Registriert**
 17        21.01.14     EVERS Eberhart (127)         Maksu- ja tolliamet             120,00       21.02.14       Wilfried Willems   **Registriert**
 16        26.01.14     COLLARD Charlotte (118)      IIZI kindlustusmaakler AS       29,95        26.02.14       Wilfried Willems   **Registriert**
 15        05.02.14     COLLARD Charlotte (118)      AS Matsalu Veevärk              12,50        08.03.14       Wilfried Willems   **Registriert**
 14        10.02.14     EMONTS Daniel (128)          AS Express Post                 10,00        13.03.14       Wilfried Willems   **Registriert**
 13        20.02.14     COLLARD Charlotte (118)      Niederau Eupen AG               10,00        23.03.14       Wilfried Willems   **Registriert**
 12        25.02.14     EMONTS Daniel (128)          Ethias s.a.                     5,33         28.03.14       Wilfried Willems   **Registriert**
 11        07.03.14     EMONTS Daniel (128)          Ragn-Sells AS                   29,95        07.04.14       Wilfried Willems   **Registriert**
 10        12.03.14     DOBBELSTEIN Dorothée (124)   Maksu- ja tolliamet             25,00        12.04.14       Wilfried Willems   **Registriert**
 9         22.03.14     EMONTS Daniel (128)          Eesti Energia AS                25,00        22.04.14       Wilfried Willems   **Registriert**
 8         27.03.14     DOBBELSTEIN Dorothée (124)   AS Matsalu Veevärk              12,50        27.04.14       Wilfried Willems   **Registriert**
 7         06.04.14     DOBBELSTEIN Dorothée (124)   Leffin Electronics              5,33         07.05.14       Wilfried Willems   **Registriert**
 6         11.04.14     AUSDEMWALD Alfons (116)      Niederau Eupen AG               120,00       12.05.14       Wilfried Willems   **Registriert**
 5         21.04.14     DOBBELSTEIN Dorothée (124)   Electrabel Customer Solutions   120,00       22.05.14       Wilfried Willems   **Registriert**
 4         26.04.14     AUSDEMWALD Alfons (116)      Ragn-Sells AS                   29,95        27.05.14       Wilfried Willems   **Registriert**
 3         06.05.14     AUSDEMWALD Alfons (116)      IIZI kindlustusmaakler AS       12,50        06.06.14       Wilfried Willems   **Registriert**
 2         11.05.14     EVERS Eberhart (127)         Eesti Energia AS                10,00        11.06.14       Wilfried Willems   **Registriert**
 1         21.05.14     AUSDEMWALD Alfons (116)      AS Express Post                 10,00        21.06.14       Wilfried Willems   **Registriert**
 **191**                                                                             **725,84**
========= ============ ============================ =============================== ============ ============== ================== =================
<BLANKLINE>


Collective incoming invoices
============================

>>> jnl = rt.modules.ledger.Journal.get_by_ref('SREG')

The SREG journal contains the following invoices:

>>> rt.show(jnl.voucher_type.table_class, jnl)
======== ============ =============================== ============== ============== ================== =================
 number   Belegdatum   Partner                         Betrag         Zahlungsziel   Autor              Arbeitsablauf
-------- ------------ ------------------------------- -------------- -------------- ------------------ -----------------
 10       01.01.14     Niederau Eupen AG               212,78         01.02.14       Wilfried Willems   **Registriert**
 9        16.01.14     Ragn-Sells AS                   82,78          16.02.14       Wilfried Willems   **Registriert**
 8        31.01.14     Eesti Energia AS                227,78         03.03.14       Wilfried Willems   **Registriert**
 7        15.02.14     Leffin Electronics              192,78         18.03.14       Wilfried Willems   **Registriert**
 6        02.03.14     Electrabel Customer Solutions   322,78         02.04.14       Wilfried Willems   **Registriert**
 5        17.03.14     IIZI kindlustusmaakler AS       177,78         17.04.14       Wilfried Willems   **Registriert**
 4        01.04.14     AS Express Post                 212,78         02.05.14       Wilfried Willems   **Registriert**
 3        16.04.14     Ethias s.a.                     82,78          17.05.14       Wilfried Willems   **Registriert**
 2        01.05.14     Maksu- ja tolliamet             227,78         01.06.14       Wilfried Willems   **Registriert**
 1        16.05.14     AS Matsalu Veevärk              192,78         16.06.14       Wilfried Willems   **Registriert**
 **55**                                                **1 932,80**
======== ============ =============================== ============== ============== ================== =================
<BLANKLINE>


Let's have a closer look at one of them.  
    
>>> obj = jnl.voucher_type.model.objects.get(number=3, journal=jnl)

The partner is #222, and the costs are distributed over three clients:

>>> obj.partner
Partner #227 (u'Ethias s.a.')

>>> rt.login('wilfried').show(rt.modules.vatless.ItemsByProjectInvoice, obj)
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF -SKIP
=================================== =========== ============== ============
 Haushaltsartikel                    Betrag      Beschreibung   Bearbeiten
----------------------------------- ----------- -------------- ------------
 (832/330/01) Allgemeine Beihilfen   5,33
 (832/330/01) Allgemeine Beihilfen   10,00
 (832/330/01) Allgemeine Beihilfen   12,50
 (832/330/01) Allgemeine Beihilfen   25,00
 (832/330/01) Allgemeine Beihilfen   29,95
 **Total (5 Zeilen)**                **82,78**
=================================== =========== ============== ============
<BLANKLINE>


This invoice is registered, and ledger movements have been created:

>>> obj.state
<VoucherStates.registered:20>
>>> rt.show(rt.modules.ledger.MovementsByVoucher, obj)
========== ============================ ============= =================================== =========== =========== ============ ============
 Seq.-Nr.   Klient                       Partner       Haushaltsartikel                    Debit       Kredit      Match        Befriedigt
---------- ---------------------------- ------------- ----------------------------------- ----------- ----------- ------------ ------------
 1                                                     (832/330/01) Allgemeine Beihilfen   12,50                                Ja
 2                                                     (832/330/01) Allgemeine Beihilfen   5,33                                 Ja
 3                                                     (832/330/01) Allgemeine Beihilfen   29,95                                Ja
 4                                                     (832/330/01) Allgemeine Beihilfen   25,00                                Ja
 5                                                     (832/330/01) Allgemeine Beihilfen   10,00                                Ja
 6          EMONTS Daniel (128)          Ethias s.a.   (4400) Lieferanten                              5,33        **SREG#8**   Nein
 7          AUSDEMWALD Alfons (116)      Ethias s.a.   (4400) Lieferanten                              10,00       **SREG#8**   Nein
 8          DOBBELSTEIN Dorothée (124)   Ethias s.a.   (4400) Lieferanten                              25,00       **SREG#8**   Nein
 9          COLLARD Charlotte (118)      Ethias s.a.   (4400) Lieferanten                              12,50       **SREG#8**   Nein
 10         EVERS Eberhart (127)         Ethias s.a.   (4400) Lieferanten                              29,95       **SREG#8**   Nein
 **55**                                                                                    **82,78**   **82,78**                **5**
========== ============================ ============= =================================== =========== =========== ============ ============
<BLANKLINE>


Incoming invoices
=================

It is possible to create new invoices from the detail view of a partner.

>>> obj.partner
Partner #227 (u'Ethias s.a.')

>>> rt.login('rolf').show(rt.modules.vatless.VouchersByPartner, obj.partner)
Beleg erstellen in Journal **Sammelrechnungen (SREG)**, **Rechnungseingänge (REG)**

Our partner has sent several invoices. The first two movements are
invoice which have been admitted for payment (a payment instruction,
AAW, has been registered) but the payment has not yet been executed.


>>> rt.show(rt.modules.ledger.MovementsByPartner, obj.partner)
====================== ========== ===================================================================== ======= =========== ============ ============
 Buchungsdatum          Beleg      Beschreibung                                                          Debit   Kredit      Match        Befriedigt
---------------------- ---------- --------------------------------------------------------------------- ------- ----------- ------------ ------------
 22.05.14               *AAW#73*   *(4450) Auszuführende Zahlungsanweisungen* / *EVERS Eberhart (127)*           5,33        **REG#28**   Nein
 22.05.14               *AAW#75*   *(4450) Auszuführende Zahlungsanweisungen* / *EMONTS Daniel (128)*            5,33        **REG#18**   Nein
 17.04.14               *SREG#8*   *(4400) Lieferanten* / *EMONTS Daniel (128)*                                  5,33        **SREG#8**   Nein
 17.04.14               *SREG#8*   *(4400) Lieferanten* / *AUSDEMWALD Alfons (116)*                              10,00       **SREG#8**   Nein
 17.04.14               *SREG#8*   *(4400) Lieferanten* / *DOBBELSTEIN Dorothée (124)*                           25,00       **SREG#8**   Nein
 17.04.14               *SREG#8*   *(4400) Lieferanten* / *COLLARD Charlotte (118)*                              12,50       **SREG#8**   Nein
 17.04.14               *SREG#8*   *(4400) Lieferanten* / *EVERS Eberhart (127)*                                 29,95       **SREG#8**   Nein
 **Total (7 Zeilen)**                                                                                            **93,44**                **0**
====================== ========== ===================================================================== ======= =========== ============ ============
<BLANKLINE>



>>> client = rt.modules.pcsw.Client.objects.get(pk=128)
>>> print(client)
EMONTS Daniel (128)

Our client has invoices from different partners:

>>> rt.show(ledger.MovementsByProject, client)
======================= ========== =============================================================================================== ============== ============ ============== ============
 Buchungsdatum           Beleg      Beschreibung                                                                                    Debit          Kredit       Match          Befriedigt
----------------------- ---------- ----------------------------------------------------------------------------------------------- -------------- ------------ -------------- ------------
 22.05.14                *AAW#31*   *(4450) Auszuführende Zahlungsanweisungen* / Allgemeine Beihilfen / *Emonts Daniel*             648,91                      **AAW#31:5**   Nein
 22.05.14                *AAW#32*   *(4450) Auszuführende Zahlungsanweisungen* / Heizkosten- u. Energiebeihilfe / *Emonts Daniel*   817,36                      **AAW#32:5**   Nein
 22.05.14                *AAW#33*   *(4450) Auszuführende Zahlungsanweisungen* / Fonds Gas und Elektrizität / *Emonts Daniel*       544,91                      **AAW#33:5**   Nein
 22.05.14                *AAW#34*   *(4450) Auszuführende Zahlungsanweisungen* / Eingliederungseinkommen / *Emonts Daniel*          800,08                      **AAW#34:5**   Nein
 22.05.14                *AAW#35*   *(4450) Auszuführende Zahlungsanweisungen* / Sozialhilfe / *Emonts Daniel*                      648,91                      **AAW#35:5**   Nein
 22.05.14                *AAW#36*   *(4450) Auszuführende Zahlungsanweisungen* / Beihilfe für Ausländer / *Emonts Daniel*           817,36                      **AAW#36:5**   Nein
 22.05.14                *AAW#73*   *(4450) Auszuführende Zahlungsanweisungen* / *Niederau Eupen AG*                                               120,00       **SREG#29**    Nein
 22.05.14                *AAW#74*   *(4450) Auszuführende Zahlungsanweisungen* / *Ragn-Sells AS*                                                   29,95        **SREG#26**    Nein
 22.05.14                *AAW#74*   *(4450) Auszuführende Zahlungsanweisungen* / *Eesti Energia AS*                                                54,95        **SREG#23**    Nein
 22.05.14                *AAW#74*   *(4450) Auszuführende Zahlungsanweisungen* / *AS Express Post*                                                 10,00        **REG#21**     Nein
 22.05.14                *AAW#75*   *(4450) Auszuführende Zahlungsanweisungen* / *Leffin Electronics*                                              25,00        **SREG#20**    Nein
 22.05.14                *AAW#75*   *(4450) Auszuführende Zahlungsanweisungen* / *Ethias s.a.*                                                     5,33         **REG#18**     Nein
 22.05.14                *AAW#75*   *(4450) Auszuführende Zahlungsanweisungen* / *Electrabel Customer Solutions*                                   12,50        **SREG#17**    Nein
 22.05.14                *AAW#75*   *(4450) Auszuführende Zahlungsanweisungen* / *Ragn-Sells AS*                                                   29,95        **REG#16**     Nein
 22.05.14                *AAW#76*   *(4450) Auszuführende Zahlungsanweisungen* / *IIZI kindlustusmaakler AS*                                       10,00        **SREG#14**    Nein
 22.05.14                *AAW#76*   *(4450) Auszuführende Zahlungsanweisungen* / *Eesti Energia AS*                                                25,00        **REG#13**     Nein
 22.05.14                *AAW#76*   *(4450) Auszuführende Zahlungsanweisungen* / *AS Express Post*                                                 15,33        **SREG#11**    Nein
 17.05.14                *SREG#2*   *(4400) Lieferanten* / *AS Matsalu Veevärk*                                                                    29,95        **SREG#2**     Nein
 02.05.14                *SREG#5*   *(4400) Lieferanten* / *Maksu- ja tolliamet*                                                                   120,00       **SREG#5**     Nein
 17.04.14                *SREG#8*   *(4400) Lieferanten* / *Ethias s.a.*                                                                           5,33         **SREG#8**     Nein
 **Total (20 Zeilen)**                                                                                                              **4 277,53**   **493,29**                  **0**
======================= ========== =============================================================================================== ============== ============ ============== ============
<BLANKLINE>


Bank statements
===============


>>> jnl = rt.modules.ledger.Journal.get_by_ref('KBC')

The KBC journal contains the following statements:

>>> rt.show(jnl.voucher_type.table_class, jnl)
====================== ===== ======== ============= =============== ============= ==================
 Belegdatum             ID    number   Alter Saldo   Neuer Saldo     Zustand       Autor
---------------------- ----- -------- ------------- --------------- ------------- ------------------
 29.04.14               132   1                      21 023,81       Registriert   Wilfried Willems
 **Total (1 Zeilen)**         **1**                  **21 023,81**
====================== ===== ======== ============= =============== ============= ==================
<BLANKLINE>

>>> obj = jnl.voucher_type.model.objects.get(number=1, journal=jnl)
>>> rt.login('wilfried').show(rt.modules.finan.ItemsByBankStatement, obj)
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
======================= ====================== ========================================== ========== =========== =============== ========= =============== ==========
 date                    Partner                Haushaltsartikel                           Match      Bemerkung   Eingang         Ausgabe   Arbeitsablauf   Seq.-Nr.
----------------------- ---------------------- ------------------------------------------ ---------- ----------- --------------- --------- --------------- ----------
                         Ausdemwald Alfons      (4450) Auszuführende Zahlungsanweisungen   AAW#37:1               544,91                                    1
                         Collard Charlotte      (4450) Auszuführende Zahlungsanweisungen   AAW#37:2               800,08                                    2
                         Dobbelstein Dorothée   (4450) Auszuführende Zahlungsanweisungen   AAW#37:3               648,91                                    3
                         Evers Eberhart         (4450) Auszuführende Zahlungsanweisungen   AAW#37:4               817,36                                    4
                         Emonts Daniel          (4450) Auszuführende Zahlungsanweisungen   AAW#37:5               544,91                                    5
                         Ausdemwald Alfons      (4450) Auszuführende Zahlungsanweisungen   AAW#38:1               800,08                                    6
                         Collard Charlotte      (4450) Auszuführende Zahlungsanweisungen   AAW#38:2               648,91                                    7
                         Dobbelstein Dorothée   (4450) Auszuführende Zahlungsanweisungen   AAW#38:3               817,36                                    8
                         Evers Eberhart         (4450) Auszuführende Zahlungsanweisungen   AAW#38:4               544,91                                    9
                         Emonts Daniel          (4450) Auszuführende Zahlungsanweisungen   AAW#38:5               800,08                                    10
                         Ausdemwald Alfons      (4450) Auszuführende Zahlungsanweisungen   AAW#39:1               648,91                                    11
                         Collard Charlotte      (4450) Auszuführende Zahlungsanweisungen   AAW#39:2               817,36                                    12
                         Dobbelstein Dorothée   (4450) Auszuführende Zahlungsanweisungen   AAW#39:3               544,91                                    13
                         Evers Eberhart         (4450) Auszuführende Zahlungsanweisungen   AAW#39:4               800,08                                    14
                         Emonts Daniel          (4450) Auszuführende Zahlungsanweisungen   AAW#39:5               648,91                                    15
                         Ausdemwald Alfons      (4450) Auszuführende Zahlungsanweisungen   AAW#40:1               817,36                                    16
                         Collard Charlotte      (4450) Auszuführende Zahlungsanweisungen   AAW#40:2               544,91                                    17
                         Dobbelstein Dorothée   (4450) Auszuführende Zahlungsanweisungen   AAW#40:3               800,08                                    18
                         Evers Eberhart         (4450) Auszuführende Zahlungsanweisungen   AAW#40:4               648,91                                    19
                         Emonts Daniel          (4450) Auszuführende Zahlungsanweisungen   AAW#40:5               817,36                                    20
                         Ausdemwald Alfons      (4450) Auszuführende Zahlungsanweisungen   AAW#41:1               544,91                                    21
                         Collard Charlotte      (4450) Auszuführende Zahlungsanweisungen   AAW#41:2               800,08                                    22
                         Dobbelstein Dorothée   (4450) Auszuführende Zahlungsanweisungen   AAW#41:3               648,91                                    23
                         Evers Eberhart         (4450) Auszuführende Zahlungsanweisungen   AAW#41:4               817,36                                    24
                         Emonts Daniel          (4450) Auszuführende Zahlungsanweisungen   AAW#41:5               544,91                                    25
                         Ausdemwald Alfons      (4450) Auszuführende Zahlungsanweisungen   AAW#42:1               800,08                                    26
                         Collard Charlotte      (4450) Auszuführende Zahlungsanweisungen   AAW#42:2               648,91                                    27
                         Dobbelstein Dorothée   (4450) Auszuführende Zahlungsanweisungen   AAW#42:3               817,36                                    28
                         Evers Eberhart         (4450) Auszuführende Zahlungsanweisungen   AAW#42:4               544,91                                    29
                         Emonts Daniel          (4450) Auszuführende Zahlungsanweisungen   AAW#42:5               800,08                                    30
 **Total (30 Zeilen)**                                                                                            **21 023,81**                             **465**
======================= ====================== ========================================== ========== =========== =============== ========= =============== ==========
<BLANKLINE>




Movements
=========

Users can consult to movements of a given general account.

>>> obj = accounts.Account.get_by_ref('820/333/01')
>>> print(unicode(obj))
(820/333/01) Vorschuss auf Vergütungen o.ä.

>>> rt.show(rt.modules.ledger.MovementsByAccount, obj)
====================== =========== ====================== ============ ======== ======= ============
 Buchungsdatum          Beleg       Beschreibung           Debit        Kredit   Match   Befriedigt
---------------------- ----------- ---------------------- ------------ -------- ------- ------------
 22.05.14               *REG#1*     *AS Express Post*      10,00                         Ja
 16.02.14               *SREG#20*   *Leffin Electronics*   29,95                         Ja
 16.02.14               *SREG#20*   *Leffin Electronics*   5,33                          Ja
 16.02.14               *SREG#20*   *Leffin Electronics*   120,00                        Ja
 16.02.14               *SREG#20*   *Leffin Electronics*   25,00                         Ja
 16.02.14               *SREG#20*   *Leffin Electronics*   12,50                         Ja
 **Total (6 Zeilen)**                                      **202,78**                    **6**
====================== =========== ====================== ============ ======== ======= ============
<BLANKLINE>


Situation
=========

The :class:`lino.modlib.ledger.ui.Situation` report is one of the
well-known accounting documents. Since accounting in Lino Welfare is
not complete (it is just a *Nebenbuchhaltung*), there are no debtors
(Schuldner) and the situation cannot be balanced.

>>> rt.show(ledger.Situation)  #doctest: +NORMALIZE_WHITESPACE
---------
Schuldner
---------
<BLANKLINE>
List of partners who are in debt towards us (usually customers).
<BLANKLINE>
========= ============== ====================== ========= =============== ===============================
 Alter     Zahlungsziel   Partner                ID        Saldo           Aktionen
--------- -------------- ---------------------- --------- --------------- -------------------------------
 60        23.03.14       Ausdemwald Alfons      116       4 277,53        [Show debts] [Issue reminder]
 60        23.03.14       Collard Charlotte      118       4 173,53        [Show debts] [Issue reminder]
 60        23.03.14       Dobbelstein Dorothée   124       4 156,25        [Show debts] [Issue reminder]
 60        23.03.14       Emonts Daniel          128       4 277,53        [Show debts] [Issue reminder]
 60        23.03.14       Evers Eberhart         127       4 260,25        [Show debts] [Issue reminder]
 **300**                                         **613**   **21 145,09**
========= ============== ====================== ========= =============== ===============================
<BLANKLINE>
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


Some choices requests
=====================

>>> ContentType = rt.modules.contenttypes.ContentType
>>> InvoiceItem = rt.modules.vatless.InvoiceItem
>>> BankStatement = rt.modules.finan.BankStatement
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

