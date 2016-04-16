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
======================= ================================ =============== ================== ==== ========= =============
 Belegdatum              Interne Referenz                 Total           Ausführungsdatum   ID   number    Zustand
----------------------- -------------------------------- --------------- ------------------ ---- --------- -------------
 13.04.14                                                 553,39                             76   22        Registriert
 13.03.14                                                 585,84                             75   21        Registriert
 13.02.14                                                 483,01                             74   20        Registriert
 13.01.14                                                 350,61                             73   19        Registriert
 22.05.14                Beihilfe für Ausländer           3 628,62                           36   6         Registriert
 22.05.14                Sozialhilfe                      3 460,17                           35   5         Registriert
 22.05.14                Eingliederungseinkommen          3 611,34                           34   4         Registriert
 22.05.14                Fonds Gas und Elektrizität       3 356,17                           33   3         Registriert
 22.05.14                Heizkosten- u. Energiebeihilfe   3 628,62                           32   2         Registriert
 22.05.14                Allgemeine Beihilfen             3 460,17                           31   1         Registriert
 22.04.14                Beihilfe für Ausländer           3 611,34                           42   12        Registriert
 22.04.14                Sozialhilfe                      3 356,17                           41   11        Registriert
 22.04.14                Eingliederungseinkommen          3 628,62                           40   10        Registriert
 22.04.14                Fonds Gas und Elektrizität       3 460,17                           39   9         Registriert
 22.04.14                Heizkosten- u. Energiebeihilfe   3 611,34                           38   8         Registriert
 22.04.14                Allgemeine Beihilfen             3 356,17                           37   7         Registriert
 23.03.14                Beihilfe für Ausländer           3 628,62                           48   18        Registriert
 23.03.14                Sozialhilfe                      3 460,17                           47   17        Registriert
 23.03.14                Eingliederungseinkommen          3 611,34                           46   16        Registriert
 23.03.14                Fonds Gas und Elektrizität       3 356,17                           45   15        Registriert
 23.03.14                Heizkosten- u. Energiebeihilfe   3 628,62                           44   14        Registriert
 23.03.14                Allgemeine Beihilfen             3 460,17                           43   13        Registriert
 **Total (22 Zeilen)**                                    **65 286,84**                           **253**
======================= ================================ =============== ================== ==== ========= =============
<BLANKLINE>


Payment orders
==============

>>> ZKBC = ledger.Journal.get_by_ref('ZKBC')

The ZKBC journal contains the following statements:

>>> rt.show(ZKBC.voucher_type.table_class, ZKBC)
====================== ================== =============== ================== ===== ======== =============
 Belegdatum             Interne Referenz   Total           Ausführungsdatum   ID    number   Zustand
---------------------- ------------------ --------------- ------------------ ----- -------- -------------
 21.04.14                                  21 145,09                          104   1        Registriert
 **Total (1 Zeilen)**                      **21 145,09**                            **1**
====================== ================== =============== ================== ===== ======== =============
<BLANKLINE>


>>> obj = ZKBC.voucher_type.model.objects.get(number=1, journal=ZKBC)
>>> rt.modules.finan.ItemsByPaymentOrder.request(obj)

>>> AAW.voucher_type.get_items_table()

>>> rt.login('wilfried').show(finan.ItemsByPaymentOrder, obj)
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF




