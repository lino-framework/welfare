.. _welfare.specs.vatless:

=================
Incoming invoices
=================

.. How to test only this document:

    $ python setup.py test -s tests.SpecsTests.test_vatless
    
    doctest init:

    >>> import lino ; lino.startup('lino_welfare.projects.eupen.settings.doctests')
    >>> from lino.utils.xmlgen.html import E
    >>> from lino.api.doctest import *
    >>> from lino.api import rt

This document is based on and extends the following specifications:

- :ref:`welfare.specs.ledger`

.. contents::
   :depth: 1
   :local:



Incoming invoices
=================

In Lino Welfare, **incoming invoices** are different from "real"
incoming invoices in that their recipient is some client of the
center, not to the center itself. The center has no direct legal
obligation, it just agrees (or not) to pay these invoices in the name
of their client.

There are two types of incoming invoices: "simple" and "collective".
The demo database has two journals with *incoming invoices*, one for
each type, referenced as "REG" (for German *Rechnungseingang*) and
SREG (*Sammelrechnungen*).

>>> REG = ledger.Journal.get_by_ref('REG')
>>> REG.voucher_type.table_class
<class 'lino_cosi.lib.vatless.ui.ProjectInvoicesByJournal'>

>>> SREG = ledger.Journal.get_by_ref('SREG')
>>> SREG.voucher_type.table_class
<class 'lino_cosi.lib.vatless.ui.InvoicesByJournal'>

The REG journal contains the following invoices:

>>> rt.show(REG.voucher_type.table_class, REG)
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


Collective invoices
===================

The SREG journal contains the following invoices:

>>> rt.show(SREG.voucher_type.table_class, SREG)
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


Incoming invoices, partners and clients
=======================================

Let's have a closer look at an incoming invoice:
    
>>> obj = SREG.voucher_type.model.objects.get(number=3, journal=SREG)

The partner of this invoice is Ethias:

>>> obj.partner
Partner #227 ('Ethias s.a.')

It is a collective invoice whose costs are distributed over five
clients:

>>> rt.login('wilfried').show(rt.modules.vatless.ItemsByInvoice, obj)
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
============================ =================================== =========== ============== ============
 Klient                       Haushaltsartikel                    Betrag      Beschreibung   Bearbeiten
---------------------------- ----------------------------------- ----------- -------------- ------------
 EMONTS Daniel (128)          (832/330/01) Allgemeine Beihilfen   5,33
 AUSDEMWALD Alfons (116)      (832/330/01) Allgemeine Beihilfen   10,00
 COLLARD Charlotte (118)      (832/330/01) Allgemeine Beihilfen   12,50
 DOBBELSTEIN Dorothée (124)   (832/330/01) Allgemeine Beihilfen   25,00
 EVERS Eberhart (127)         (832/330/01) Allgemeine Beihilfen   29,95
 **Total (5 Zeilen)**                                             **82,78**
============================ =================================== =========== ============== ============
<BLANKLINE>


This invoice is registered, and ledger movements have been created:

>>> obj.state
<VoucherStates.registered:20>
>>> rt.show(rt.modules.ledger.MovementsByVoucher, obj)
========== ============================ ============= =================================== =========== =========== ============ =========
 Seq.-Nr.   Klient                       Partner       Haushaltsartikel                    Debit       Kredit      Match        Cleared
---------- ---------------------------- ------------- ----------------------------------- ----------- ----------- ------------ ---------
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
 **55**                                                                                    **82,78**   **82,78**
========== ============================ ============= =================================== =========== =========== ============ =========
<BLANKLINE>


The first five movements are *cleared* because their account is not
:attr:`clearable <lino_cosi.lib.accounts.Account.clearable>`.

>>> cost_account = rt.modules.accounts.Account.objects.get(ref="832/330/01")
>>> cost_account.clearable
False

The other five movements go into the suppliers account, which is
clearable:

>>> suppliers_account = rt.modules.accounts.Account.objects.get(ref="4400")
>>> suppliers_account.clearable
True

The match rules table defines how to clear these movements:

>>> rt.show(ledger.MatchRulesByAccount, suppliers_account)
==========================
 Journal
--------------------------
 Ausgabeanweisungen (AAW)
==========================
<BLANKLINE>

This rule means: "Uncleared amounts in the suppliers account may be
cleared by the AAW (disbursement instructions) journal".

Since AAW is a financial journal, our story continues in :doc:`finan`.





Registering new incoming invoices
=================================

It is possible to create new invoices from the detail view of a partner.

The partner is usually some company.

>>> obj.partner
Partner #227 ('Ethias s.a.')

>>> rt.login('rolf').show(rt.modules.vatless.VouchersByPartner, obj.partner)
Beleg erstellen in Journal **Sammelrechnungen (SREG)**, **Rechnungseingänge (REG)**

Our partner has sent several movements which are not yet
*cleared*. The first two movements are invoices which have been
admitted for payment (i.e. a disbursement instruction (AAW) has been
registered), but the payment has not yet been executed.

>>> rt.show(rt.modules.ledger.MovementsByPartner, obj.partner)
====================== =================== ==================================================================== ======= =========== ============ =========
 Buchungsdatum          Beleg               Beschreibung                                                         Debit   Kredit      Match        Cleared
---------------------- ------------------- -------------------------------------------------------------------- ------- ----------- ------------ ---------
 22.05.14               *AAW19 (2014-05)*   *(4450) Auszuführende Ausgabeanweisungen* / *EVERS Eberhart (127)*           5,33        **REG#28**   Nein
 22.05.14               *AAW21 (2014-05)*   *(4450) Auszuführende Ausgabeanweisungen* / *EMONTS Daniel (128)*            5,33        **REG#18**   Nein
 17.04.14               *SREG3 (2014-04)*   *(4400) Lieferanten* / *EMONTS Daniel (128)*                                 5,33        **SREG#8**   Nein
 17.04.14               *SREG3 (2014-04)*   *(4400) Lieferanten* / *AUSDEMWALD Alfons (116)*                             10,00       **SREG#8**   Nein
 17.04.14               *SREG3 (2014-04)*   *(4400) Lieferanten* / *DOBBELSTEIN Dorothée (124)*                          25,00       **SREG#8**   Nein
 17.04.14               *SREG3 (2014-04)*   *(4400) Lieferanten* / *COLLARD Charlotte (118)*                             12,50       **SREG#8**   Nein
 17.04.14               *SREG3 (2014-04)*   *(4400) Lieferanten* / *EVERS Eberhart (127)*                                29,95       **SREG#8**   Nein
 **Total (7 Zeilen)**                                                                                                    **93,44**
====================== =================== ==================================================================== ======= =========== ============ =========
<BLANKLINE>

Let's look at one of these movements via its client.

>>> client = rt.modules.pcsw.Client.objects.get(pk=128)
>>> print(client)
EMONTS Daniel (128)

Our client has invoices from different partners:

>>> rt.show(ledger.MovementsByProject, client)
======================= =================== ============================================================================================== ============== ============== ============== =========
 Buchungsdatum           Beleg               Beschreibung                                                                                   Debit          Kredit         Match          Cleared
----------------------- ------------------- ---------------------------------------------------------------------------------------------- -------------- -------------- -------------- ---------
 22.05.14                *AAW1 (2014-05)*    *(4450) Auszuführende Ausgabeanweisungen* / Allgemeine Beihilfen / *Emonts Daniel*             648,91                        **AAW#31:5**   Nein
 22.05.14                *AAW2 (2014-05)*    *(4450) Auszuführende Ausgabeanweisungen* / Heizkosten- u. Energiebeihilfe / *Emonts Daniel*   817,36                        **AAW#32:5**   Nein
 22.05.14                *AAW3 (2014-05)*    *(4450) Auszuführende Ausgabeanweisungen* / Fonds Gas und Elektrizität / *Emonts Daniel*       544,91                        **AAW#33:5**   Nein
 22.05.14                *AAW4 (2014-05)*    *(4450) Auszuführende Ausgabeanweisungen* / Eingliederungseinkommen / *Emonts Daniel*          800,08                        **AAW#34:5**   Nein
 22.05.14                *AAW5 (2014-05)*    *(4450) Auszuführende Ausgabeanweisungen* / Sozialhilfe / *Emonts Daniel*                      648,91                        **AAW#35:5**   Nein
 22.05.14                *AAW6 (2014-05)*    *(4450) Auszuführende Ausgabeanweisungen* / Beihilfe für Ausländer / *Emonts Daniel*           817,36                        **AAW#36:5**   Nein
 22.05.14                *AAW19 (2014-05)*   *(4450) Auszuführende Ausgabeanweisungen* / *Niederau Eupen AG*                                               120,00         **SREG#29**    Nein
 22.05.14                *AAW20 (2014-05)*   *(4450) Auszuführende Ausgabeanweisungen* / *Ragn-Sells AS*                                                   29,95          **SREG#26**    Nein
 22.05.14                *AAW20 (2014-05)*   *(4450) Auszuführende Ausgabeanweisungen* / *Eesti Energia AS*                                                54,95          **SREG#23**    Nein
 22.05.14                *AAW20 (2014-05)*   *(4450) Auszuführende Ausgabeanweisungen* / *AS Express Post*                                                 10,00          **REG#21**     Nein
 22.05.14                *AAW21 (2014-05)*   *(4450) Auszuführende Ausgabeanweisungen* / *Leffin Electronics*                                              25,00          **SREG#20**    Nein
 22.05.14                *AAW21 (2014-05)*   *(4450) Auszuführende Ausgabeanweisungen* / *Ethias s.a.*                                                     5,33           **REG#18**     Nein
 22.05.14                *AAW21 (2014-05)*   *(4450) Auszuführende Ausgabeanweisungen* / *Electrabel Customer Solutions*                                   12,50          **SREG#17**    Nein
 22.05.14                *AAW21 (2014-05)*   *(4450) Auszuführende Ausgabeanweisungen* / *Ragn-Sells AS*                                                   29,95          **REG#16**     Nein
 22.05.14                *AAW22 (2014-05)*   *(4450) Auszuführende Ausgabeanweisungen* / *IIZI kindlustusmaakler AS*                                       10,00          **SREG#14**    Nein
 22.05.14                *AAW22 (2014-05)*   *(4450) Auszuführende Ausgabeanweisungen* / *Eesti Energia AS*                                                25,00          **REG#13**     Nein
 22.05.14                *AAW22 (2014-05)*   *(4450) Auszuführende Ausgabeanweisungen* / *AS Express Post*                                                 15,33          **SREG#11**    Nein
 22.05.14                *ZKBC1 (2014-05)*   *(4400) Lieferanten* / *Emonts Daniel*                                                                        648,91         **AAW#43:5**   Nein
 22.05.14                *ZKBC1 (2014-05)*   *(4400) Lieferanten* / *Emonts Daniel*                                                                        817,36         **AAW#44:5**   Nein
 22.05.14                *ZKBC1 (2014-05)*   *(4400) Lieferanten* / *Emonts Daniel*                                                                        544,91         **AAW#45:5**   Nein
 22.05.14                *ZKBC1 (2014-05)*   *(4400) Lieferanten* / *Emonts Daniel*                                                                        800,08         **AAW#46:5**   Nein
 22.05.14                *ZKBC1 (2014-05)*   *(4400) Lieferanten* / *Emonts Daniel*                                                                        648,91         **AAW#47:5**   Nein
 22.05.14                *ZKBC1 (2014-05)*   *(4400) Lieferanten* / *Emonts Daniel*                                                                        817,36         **AAW#48:5**   Nein
 17.05.14                *SREG1 (2014-05)*   *(4400) Lieferanten* / *AS Matsalu Veevärk*                                                                   29,95          **SREG#2**     Nein
 02.05.14                *SREG2 (2014-05)*   *(4400) Lieferanten* / *Maksu- ja tolliamet*                                                                  120,00         **SREG#5**     Nein
 17.04.14                *SREG3 (2014-04)*   *(4400) Lieferanten* / *Ethias s.a.*                                                                          5,33           **SREG#8**     Nein
 **Total (26 Zeilen)**                                                                                                                      **4 277,53**   **4 770,82**
======================= =================== ============================================================================================== ============== ============== ============== =========
<BLANKLINE>

