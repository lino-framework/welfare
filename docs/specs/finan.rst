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



Bank statements
===============


>>> KBC = ledger.Journal.get_by_ref('KBC')

The KBC journal contains the following statements:

>>> rt.show(KBC.voucher_type.table_class, KBC)
====================== ===== ======== =============== =============== ============= ==================
 Belegdatum             ID    number   Alter Saldo     Neuer Saldo     Zustand       Autor
---------------------- ----- -------- --------------- --------------- ------------- ------------------
 29.04.14               132   2        21 145,09       42 168,90       Registriert   Wilfried Willems
 29.03.14               131   1                        21 145,09       Registriert   Theresia Thelen
 **Total (2 Zeilen)**         **3**    **21 145,09**   **63 313,99**
====================== ===== ======== =============== =============== ============= ==================
<BLANKLINE>

>>> obj = KBC.voucher_type.model.objects.get(number=1, journal=KBC)
>>> rt.login('wilfried').show(finan.ItemsByBankStatement, obj)
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
======================= ====================== ========================================= ========== ================== =============== ========= =============== ==========
 date                    Partner                Haushaltsartikel                          Match      Externe Referenz   Eingang         Ausgabe   Arbeitsablauf   Seq.-Nr.
----------------------- ---------------------- ----------------------------------------- ---------- ------------------ --------------- --------- --------------- ----------
                         Ausdemwald Alfons      (4450) Auszuführende Ausgabeanweisungen   AAW#43:1                      648,91                                    1
                         Collard Charlotte      (4450) Auszuführende Ausgabeanweisungen   AAW#43:2                      817,36                                    2
                         Dobbelstein Dorothée   (4450) Auszuführende Ausgabeanweisungen   AAW#43:3                      544,91                                    3
                         Evers Eberhart         (4450) Auszuführende Ausgabeanweisungen   AAW#43:4                      800,08                                    4
                         Emonts Daniel          (4450) Auszuführende Ausgabeanweisungen   AAW#43:5                      648,91                                    5
                         Ausdemwald Alfons      (4450) Auszuführende Ausgabeanweisungen   AAW#44:1                      817,36                                    6
                         Collard Charlotte      (4450) Auszuführende Ausgabeanweisungen   AAW#44:2                      544,91                                    7
                         Dobbelstein Dorothée   (4450) Auszuführende Ausgabeanweisungen   AAW#44:3                      800,08                                    8
                         Evers Eberhart         (4450) Auszuführende Ausgabeanweisungen   AAW#44:4                      648,91                                    9
                         Emonts Daniel          (4450) Auszuführende Ausgabeanweisungen   AAW#44:5                      817,36                                    10
                         Ausdemwald Alfons      (4450) Auszuführende Ausgabeanweisungen   AAW#45:1                      544,91                                    11
                         Collard Charlotte      (4450) Auszuführende Ausgabeanweisungen   AAW#45:2                      800,08                                    12
                         Dobbelstein Dorothée   (4450) Auszuführende Ausgabeanweisungen   AAW#45:3                      648,91                                    13
                         Evers Eberhart         (4450) Auszuführende Ausgabeanweisungen   AAW#45:4                      817,36                                    14
                         Emonts Daniel          (4450) Auszuführende Ausgabeanweisungen   AAW#45:5                      544,91                                    15
                         Ausdemwald Alfons      (4450) Auszuführende Ausgabeanweisungen   AAW#46:1                      800,08                                    16
                         Collard Charlotte      (4450) Auszuführende Ausgabeanweisungen   AAW#46:2                      648,91                                    17
                         Dobbelstein Dorothée   (4450) Auszuführende Ausgabeanweisungen   AAW#46:3                      817,36                                    18
                         Evers Eberhart         (4450) Auszuführende Ausgabeanweisungen   AAW#46:4                      544,91                                    19
                         Emonts Daniel          (4450) Auszuführende Ausgabeanweisungen   AAW#46:5                      800,08                                    20
                         Ausdemwald Alfons      (4450) Auszuführende Ausgabeanweisungen   AAW#47:1                      648,91                                    21
                         Collard Charlotte      (4450) Auszuführende Ausgabeanweisungen   AAW#47:2                      817,36                                    22
                         Dobbelstein Dorothée   (4450) Auszuführende Ausgabeanweisungen   AAW#47:3                      544,91                                    23
                         Evers Eberhart         (4450) Auszuführende Ausgabeanweisungen   AAW#47:4                      800,08                                    24
                         Emonts Daniel          (4450) Auszuführende Ausgabeanweisungen   AAW#47:5                      648,91                                    25
                         Ausdemwald Alfons      (4450) Auszuführende Ausgabeanweisungen   AAW#48:1                      817,36                                    26
                         Collard Charlotte      (4450) Auszuführende Ausgabeanweisungen   AAW#48:2                      544,91                                    27
                         Dobbelstein Dorothée   (4450) Auszuführende Ausgabeanweisungen   AAW#48:3                      800,08                                    28
                         Evers Eberhart         (4450) Auszuführende Ausgabeanweisungen   AAW#48:4                      648,91                                    29
                         Emonts Daniel          (4450) Auszuführende Ausgabeanweisungen   AAW#48:5                      817,36                                    30
 **Total (30 Zeilen)**                                                                                                  **21 145,09**                             **465**
======================= ====================== ========================================= ========== ================== =============== ========= =============== ==========
<BLANKLINE>




