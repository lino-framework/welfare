.. _welfare.tested.newcomers:

Newcomers
=============

.. include:: /include/tested.rst

.. to test only this document:

  $ python setup.py test -s tests.DocsTests.test_newcomers


.. include:: /include/tested.rst

.. contents::
   :depth: 2


..
    >>> from __future__ import print_function
    >>> import os
    >>> os.environ['DJANGO_SETTINGS_MODULE'] = \
    ...    'lino_welfare.projects.eupen.settings.doctests'
    >>> from lino.api.doctest import *


>>> ses = settings.SITE.login('rolf')

>>> ses.show('newcomers.NewClients')
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
==================================== =========== ============ ================================ =============== ===== ================================= ========== ======== ========= ===== ================ =========
 Name                                 Zustand     Vermittler   Fachbereich                      NR-Nummer       GSM   Adresse                           Alter      E-Mail   Telefon   ID    Sozialhilfeart   Sprache
------------------------------------ ----------- ------------ -------------------------------- --------------- ----- --------------------------------- ---------- -------- --------- ----- ---------------- ---------
 BASTIAENSEN Laurent (117)            Neuantrag                Finanzielle Begleitung           971207 001-67         Am Berg, 4700 Eupen               16 Jahre                      117                    de
 BRAUN Bruno (257)                    Neuantrag                                                                                                         40 Jahre                      257                    de
 DEMEULENAERE Dorothée (122)          Neuantrag                Ausländerbeihilfe                960127 002-47         Auf'm Rain, 4700 Eupen            18 Jahre                      122                    de
 DERICUM Daniel (121)                 Neuantrag                DSBE                             950221 001-20         August-Thonnar-Str., 4700 Eupen   19 Jahre                      121                    de
 DOBBELSTEIN Dorothée (124)           Begleitet                Finanzielle Begleitung           940904 002-72         Bahnhofsgasse, 4700 Eupen         19 Jahre                      124                    fr
 EIERSCHAL Emil (175)                 Neuantrag                Laufende Beihilfe                930412 001-68         Deutschland                       21 Jahre                      175                    de
 EMONTSPOOL Erwin (151)               Neuantrag                DSBE                             910602 001-49         4730 Raeren                       22 Jahre                      151                    de
 ERNST Berta (125)                    Neuantrag                Laufende Beihilfe                900627 002-53         Bergkapellstraße, 4700 Eupen      23 Jahre                      125                    fr
 FRISCH Paul (238)                    Neuantrag                                                                                                         46 Jahre                      238                    de
 GERNEGROß Germaine (131)             Neuantrag                Laufende Beihilfe                880816 002-64         Buchenweg, 4700 Eupen             25 Jahre                      131                    de
 GROTECLAES Gregory (132)             Begleitet                Eingliederungseinkommen (EiEi)   880228 001-51         Edelstraße, 4700 Eupen            26 Jahre                      132                    de
 HILGERS Henri (134)                  Neuantrag                Ausländerbeihilfe                870911 001-07         Euregiostraße, 4700 Eupen         26 Jahre                      134                    de
 INGELS Irene (135)                   Neuantrag                Finanzielle Begleitung           861006 002-45         Feldstraße, 4700 Eupen            27 Jahre                      135                    de
 JANSEN Jérémy (136)                  Neuantrag                Laufende Beihilfe                851031 001-51         Gewerbestraße, 4700 Eupen         28 Jahre                      136                    de
 KASENNOVA Tatjana (221)              Neuantrag                DSBE                             830115 002-37         4701 Kettenis                     31 Jahre                      221                    de
 KELLER Karl (178)                    Begleitet                Ausländerbeihilfe                820729 001-27         Deutschland                       31 Jahre                      178                    de
 LAHM Lisa (176)                      Neuantrag                Eingliederungseinkommen (EiEi)   820209 002-09         Deutschland                       32 Jahre                      176                    de
 LAMBERTZ Guido (142)                 Begleitet                Laufende Beihilfe                810823 001-96         Haasstraße, 4700 Eupen            32 Jahre                      142                    de
 LASCHET Laura (143)                  Neuantrag                Eingliederungseinkommen (EiEi)   810306 002-85         Habsburgerweg, 4700 Eupen         33 Jahre                      143                    de
 MARTELAER Mark (172)                 Neuantrag                DSBE                             790426 001-33         Amsterdam, Niederlande            35 Jahre                      172                    de
 MEIER Marie-Louise (149)             Neuantrag                Laufende Beihilfe                780521 002-71         Hisselsgasse, 4700 Eupen          36 Jahre                      149                    de
 RADERMACHER Alfons (153)             Begleitet                Finanzielle Begleitung           771202 001-88         4730 Raeren                       36 Jahre                      153                    fr
 RADERMACHER Berta (154)              Neuantrag                Laufende Beihilfe                770615 002-43         4730 Raeren                       36 Jahre                      154                    fr
 RADERMACHER Daniela (156)            Neuantrag                DSBE                             760710 002-82         4730 Raeren                       37 Jahre                      156                    de
 RADERMACHER Inge (162)               Neuantrag                DSBE                             730924 002-01         4730 Raeren                       40 Jahre                      162                    de
 VANDENMEULENBOS Marie-Louise (174)   Neuantrag                Finanzielle Begleitung           721019 002-40         Amsterdam, Niederlande            41 Jahre                      174                    de
 DA VINCI David (165)                 Begleitet                Finanzielle Begleitung           720502 001-31         4730 Raeren                       42 Jahre                      165                    de
 DI RUPO Didier (164)                 Neuantrag                Ausländerbeihilfe                711114 001-80         4730 Raeren                       42 Jahre                      164                    de
==================================== =========== ============ ================================ =============== ===== ================================= ========== ======== ========= ===== ================ =========
<BLANKLINE>
