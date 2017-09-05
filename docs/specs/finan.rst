.. _welfare.specs.finan:

==================================
Financial vouchers in Lino Welfare
==================================

.. How to test only this document:

    $ doctest docs/specs/finan.rst
    
    doctest init:

    >>> import lino ; lino.startup('lino_welfare.projects.eupen.settings.doctests')
    >>> from lino.utils.xmlgen.html import E
    >>> from lino.api.doctest import *

This document describes specific aspecs of *financial vouchers* in
:ref:`welfare`, as implemented by the :mod:`lino_welfare.lib.finan`
plugin.  

It is based on the following other specifications:

- :ref:`cosi.specs.accounting`
- :ref:`cosi.specs.ledger`
- :ref:`specs.cosi.finan`
- :ref:`welfare.specs.ledger`


Table of contents:

.. contents::
   :depth: 1
   :local:


Disbursment orders
==================


>>> AAW = ledger.Journal.get_by_ref('AAW')

>>> print(AAW.voucher_type.model)
<class 'lino_xl.lib.finan.models.PaymentOrder'>

The AAW journal contains the following statements:

>>> rt.show(AAW.voucher_type.table_class, AAW)
======================= =============== ================================ =============== ================== ================= =================
 Nr.                     Buchungsdatum   Interne Referenz                 Total           Ausführungsdatum   Buchungsperiode   Workflow
----------------------- --------------- -------------------------------- --------------- ------------------ ----------------- -----------------
 22/2014                 13.04.14                                         -553,39                            2014-04           **Registriert**
 21/2014                 13.03.14                                         -585,84                            2014-03           **Registriert**
 20/2014                 13.02.14                                         -483,01                            2014-02           **Registriert**
 19/2014                 13.01.14                                         -350,61                            2014-01           **Registriert**
 18/2014                 23.03.14        Beihilfe für Ausländer           3 628,62                           2014-03           **Registriert**
 17/2014                 23.03.14        Sozialhilfe                      3 460,17                           2014-03           **Registriert**
 16/2014                 23.03.14        Eingliederungseinkommen          3 611,34                           2014-03           **Registriert**
 15/2014                 23.03.14        Fonds Gas und Elektrizität       3 356,17                           2014-03           **Registriert**
 14/2014                 23.03.14        Heizkosten- u. Energiebeihilfe   3 628,62                           2014-03           **Registriert**
 13/2014                 23.03.14        Allgemeine Beihilfen             3 460,17                           2014-03           **Registriert**
 12/2014                 22.04.14        Beihilfe für Ausländer           3 611,34                           2014-04           **Registriert**
 11/2014                 22.04.14        Sozialhilfe                      3 356,17                           2014-04           **Registriert**
 10/2014                 22.04.14        Eingliederungseinkommen          3 628,62                           2014-04           **Registriert**
 9/2014                  22.04.14        Fonds Gas und Elektrizität       3 460,17                           2014-04           **Registriert**
 8/2014                  22.04.14        Heizkosten- u. Energiebeihilfe   3 611,34                           2014-04           **Registriert**
 7/2014                  22.04.14        Allgemeine Beihilfen             3 356,17                           2014-04           **Registriert**
 6/2014                  22.05.14        Beihilfe für Ausländer           3 628,62                           2014-05           **Registriert**
 5/2014                  22.05.14        Sozialhilfe                      3 460,17                           2014-05           **Registriert**
 4/2014                  22.05.14        Eingliederungseinkommen          3 611,34                           2014-05           **Registriert**
 3/2014                  22.05.14        Fonds Gas und Elektrizität       3 356,17                           2014-05           **Registriert**
 2/2014                  22.05.14        Heizkosten- u. Energiebeihilfe   3 628,62                           2014-05           **Registriert**
 1/2014                  22.05.14        Allgemeine Beihilfen             3 460,17                           2014-05           **Registriert**
 **Total (22 Zeilen)**                                                    **61 341,14**
======================= =============== ================================ =============== ================== ================= =================
<BLANKLINE>


Payment orders
==============

>>> ZKBC = ledger.Journal.get_by_ref('ZKBC')

(remaining tests are temporarily skipped after 20170525. TODO:
reactivate them and find out why the payment order is not being
generated)


The ZKBC journal contains the following payment orders:

>>> rt.show(ZKBC.voucher_type.table_class, ZKBC)  #doctest: -SKIP
====================== =============== ================== =============== ================== ================= =================
 Nr.                    Buchungsdatum   Interne Referenz   Total           Ausführungsdatum   Buchungsperiode   Workflow
---------------------- --------------- ------------------ --------------- ------------------ ----------------- -----------------
 4/2014                 21.04.14                           20 521,42                          2014-04           **Registriert**
 3/2014                 21.03.14                           -758,29                            2014-03           **Registriert**
 2/2014                 21.02.14                           -620,84                            2014-02           **Registriert**
 1/2014                 21.01.14                           -350,61                            2014-01           **Registriert**
 **Total (4 Zeilen)**                                      **18 791,68**
====================== =============== ================== =============== ================== ================= =================
<BLANKLINE>

TODO: Note that it is not normal to have negative totals in above
list.  See :ticket:`1985`.


>>> obj = ZKBC.voucher_type.model.objects.get(number=1, journal=ZKBC)  #doctest: -SKIP
>>> rt.login('wilfried').show(finan.ItemsByPaymentOrder, obj)  #doctest: -SKIP
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
======== ============================ =============================== ========== ===================== ========= ============ ==================
 Nr.      Klient                       Zahlungsempfänger               Workflow   Bankkonto             Match     Betrag       Externe Referenz
-------- ---------------------------- ------------------------------- ---------- --------------------- --------- ------------ ------------------
 1        EVERS Eberhart (127)         Leffin Electronics                         BE38 2480 1735 7572   REG 20    12,50
 2        EMONTS Daniel (128)          Niederau Eupen AG                          BE98 3480 3103 3293   SREG 10   120,00
 3        AUSDEMWALD Alfons (116)      Niederau Eupen AG                          BE98 3480 3103 3293   SREG 10   15,33
 4        DOBBELSTEIN Dorothée (124)   Niederau Eupen AG                          BE98 3480 3103 3293   SREG 10   25,00
 5        COLLARD Charlotte (118)      Niederau Eupen AG                          BE98 3480 3103 3293   SREG 10   22,50
 6        EVERS Eberhart (127)         Niederau Eupen AG                          BE98 3480 3103 3293   SREG 10   29,95
 7        EVERS Eberhart (127)         Ethias s.a.                                BE79 8270 8180 3833   REG 19    5,33
 8        COLLARD Charlotte (118)      Electrabel Customer Solutions              BE46 0003 2544 8336   REG 18    120,00
 **36**                                                                                                           **350,61**
======== ============================ =============================== ========== ===================== ========= ============ ==================
<BLANKLINE>


>>> kw = dict()
>>> fields = 'count rows'
>>> obj = ZKBC.voucher_type.model.objects.get(number=1, journal=ZKBC)  #doctest: -SKIP
>>> demo_get(
...    'wilfried', 'choices/finan/ItemsByPaymentOrder/match',
...    fields, 94, mk=obj.pk, **kw)  #doctest: -SKIP

