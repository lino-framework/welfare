.. _welfare.specs.finan:

===================
Financial documents
===================

.. How to test only this document:

    $ python setup.py test -s tests.SpecsTests.test_finan
    
    doctest init:

    >>> import lino ; lino.startup('lino_welfare.projects.eupen.settings.doctests')
    >>> from lino.utils.xmlgen.html import E
    >>> from lino.api.doctest import *

This document is based on and extends the following specifications:

- :ref:`welfare.specs.ledger`

.. contents::
   :depth: 1
   :local:


Disbursment orders
==================


>>> AAW = ledger.Journal.get_by_ref('AAW')

The AAW journal contains the following statements:

>>> rt.show(AAW.voucher_type.table_class, AAW)
========= ============ ================================ =============== ================== =============
 Nr.       Belegdatum   Interne Referenz                 Total           Ausführungsdatum   Zustand
--------- ------------ -------------------------------- --------------- ------------------ -------------
 22        13.04.14                                      -553,39                            Registriert
 21        13.03.14                                      -585,84                            Registriert
 20        13.02.14                                      -483,01                            Registriert
 19        13.01.14                                      -350,61                            Registriert
 6         22.05.14     Beihilfe für Ausländer           3 628,62                           Registriert
 5         22.05.14     Sozialhilfe                      3 460,17                           Registriert
 4         22.05.14     Eingliederungseinkommen          3 611,34                           Registriert
 3         22.05.14     Fonds Gas und Elektrizität       3 356,17                           Registriert
 2         22.05.14     Heizkosten- u. Energiebeihilfe   3 628,62                           Registriert
 1         22.05.14     Allgemeine Beihilfen             3 460,17                           Registriert
 12        22.04.14     Beihilfe für Ausländer           3 611,34                           Registriert
 11        22.04.14     Sozialhilfe                      3 356,17                           Registriert
 10        22.04.14     Eingliederungseinkommen          3 628,62                           Registriert
 9         22.04.14     Fonds Gas und Elektrizität       3 460,17                           Registriert
 8         22.04.14     Heizkosten- u. Energiebeihilfe   3 611,34                           Registriert
 7         22.04.14     Allgemeine Beihilfen             3 356,17                           Registriert
 18        23.03.14     Beihilfe für Ausländer           3 628,62                           Registriert
 17        23.03.14     Sozialhilfe                      3 460,17                           Registriert
 16        23.03.14     Eingliederungseinkommen          3 611,34                           Registriert
 15        23.03.14     Fonds Gas und Elektrizität       3 356,17                           Registriert
 14        23.03.14     Heizkosten- u. Energiebeihilfe   3 628,62                           Registriert
 13        23.03.14     Allgemeine Beihilfen             3 460,17                           Registriert
 **253**                                                 **61 341,14**
========= ============ ================================ =============== ================== =============
<BLANKLINE>


Payment orders
==============

>>> ZKBC = ledger.Journal.get_by_ref('ZKBC')

The ZKBC journal contains the following statements:

>>> rt.show(ZKBC.voucher_type.table_class, ZKBC)
======= ============ ================== =============== ================== =============
 Nr.     Belegdatum   Interne Referenz   Total           Ausführungsdatum   Zustand
------- ------------ ------------------ --------------- ------------------ -------------
 1       21.04.14                        21 145,09                          Registriert
 **1**                                   **21 145,09**
======= ============ ================== =============== ================== =============
<BLANKLINE>


>>> obj = ZKBC.voucher_type.model.objects.get(number=1, journal=ZKBC)
>>> rt.login('wilfried').show(finan.ItemsByPaymentOrder, obj)
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
========= ============================ ====================== =============== ==================================== ========== =============== ==================
 Nr.       Klient                       Zahlungsempfänger      Arbeitsablauf   Bankkonto                            Match      Betrag          Externe Referenz
--------- ---------------------------- ---------------------- --------------- ------------------------------------ ---------- --------------- ------------------
 1         AUSDEMWALD Alfons (116)      Ausdemwald Alfons                      BG45 LMDF 6875 2666 8474 93          AAW#43:1   648,91
 2         COLLARD Charlotte (118)      Collard Charlotte                      CY94 5951 8993 3551 8874 2318 3914   AAW#43:2   817,36
 3         DOBBELSTEIN Dorothée (124)   Dobbelstein Dorothée                   DK09 0573 4385 9143 85               AAW#43:3   544,91
 4         EVERS Eberhart (127)         Evers Eberhart                         DO34 8944 3429 6388 1766 4829 8583   AAW#43:4   800,08
 5         EMONTS Daniel (128)          Emonts Daniel                          DO87 9470 5313 8589 9175 5390 3987   AAW#43:5   648,91
 6         AUSDEMWALD Alfons (116)      Ausdemwald Alfons                      BG45 LMDF 6875 2666 8474 93          AAW#44:1   817,36
 7         COLLARD Charlotte (118)      Collard Charlotte                      CY94 5951 8993 3551 8874 2318 3914   AAW#44:2   544,91
 8         DOBBELSTEIN Dorothée (124)   Dobbelstein Dorothée                   DK09 0573 4385 9143 85               AAW#44:3   800,08
 9         EVERS Eberhart (127)         Evers Eberhart                         DO34 8944 3429 6388 1766 4829 8583   AAW#44:4   648,91
 10        EMONTS Daniel (128)          Emonts Daniel                          DO87 9470 5313 8589 9175 5390 3987   AAW#44:5   817,36
 11        AUSDEMWALD Alfons (116)      Ausdemwald Alfons                      BG45 LMDF 6875 2666 8474 93          AAW#45:1   544,91
 12        COLLARD Charlotte (118)      Collard Charlotte                      CY94 5951 8993 3551 8874 2318 3914   AAW#45:2   800,08
 13        DOBBELSTEIN Dorothée (124)   Dobbelstein Dorothée                   DK09 0573 4385 9143 85               AAW#45:3   648,91
 14        EVERS Eberhart (127)         Evers Eberhart                         DO34 8944 3429 6388 1766 4829 8583   AAW#45:4   817,36
 15        EMONTS Daniel (128)          Emonts Daniel                          DO87 9470 5313 8589 9175 5390 3987   AAW#45:5   544,91
 16        AUSDEMWALD Alfons (116)      Ausdemwald Alfons                      BG45 LMDF 6875 2666 8474 93          AAW#46:1   800,08
 17        COLLARD Charlotte (118)      Collard Charlotte                      CY94 5951 8993 3551 8874 2318 3914   AAW#46:2   648,91
 18        DOBBELSTEIN Dorothée (124)   Dobbelstein Dorothée                   DK09 0573 4385 9143 85               AAW#46:3   817,36
 19        EVERS Eberhart (127)         Evers Eberhart                         DO34 8944 3429 6388 1766 4829 8583   AAW#46:4   544,91
 20        EMONTS Daniel (128)          Emonts Daniel                          DO87 9470 5313 8589 9175 5390 3987   AAW#46:5   800,08
 21        AUSDEMWALD Alfons (116)      Ausdemwald Alfons                      BG45 LMDF 6875 2666 8474 93          AAW#47:1   648,91
 22        COLLARD Charlotte (118)      Collard Charlotte                      CY94 5951 8993 3551 8874 2318 3914   AAW#47:2   817,36
 23        DOBBELSTEIN Dorothée (124)   Dobbelstein Dorothée                   DK09 0573 4385 9143 85               AAW#47:3   544,91
 24        EVERS Eberhart (127)         Evers Eberhart                         DO34 8944 3429 6388 1766 4829 8583   AAW#47:4   800,08
 25        EMONTS Daniel (128)          Emonts Daniel                          DO87 9470 5313 8589 9175 5390 3987   AAW#47:5   648,91
 26        AUSDEMWALD Alfons (116)      Ausdemwald Alfons                      BG45 LMDF 6875 2666 8474 93          AAW#48:1   817,36
 27        COLLARD Charlotte (118)      Collard Charlotte                      CY94 5951 8993 3551 8874 2318 3914   AAW#48:2   544,91
 28        DOBBELSTEIN Dorothée (124)   Dobbelstein Dorothée                   DK09 0573 4385 9143 85               AAW#48:3   800,08
 29        EVERS Eberhart (127)         Evers Eberhart                         DO34 8944 3429 6388 1766 4829 8583   AAW#48:4   648,91
 30        EMONTS Daniel (128)          Emonts Daniel                          DO87 9470 5313 8589 9175 5390 3987   AAW#48:5   817,36
 **465**                                                                                                                       **21 145,09**
========= ============================ ====================== =============== ==================================== ========== =============== ==================
<BLANKLINE>



>>> kw = dict()
>>> fields = 'count rows'
>>> obj = ZKBC.voucher_type.model.objects.get(number=1, journal=ZKBC)
>>> demo_get(
...    'wilfried', 'choices/finan/ItemsByPaymentOrder/match',
...    fields, 140, mk=obj.pk, **kw)

