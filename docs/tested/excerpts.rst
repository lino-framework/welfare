.. _welfare.tested.excerpts:

=============
Excerpts
=============

.. How to test only this document:

  $ python setup.py test -s tests.DocsTests.test_excerpts


.. contents::
   :local:
   :depth: 2

About this document
===================

.. include:: /include/tested.rst

This documents uses the :mod:`lino_welfare.projects.eupen` test
database:

>>> from __future__ import print_function
>>> import os
>>> os.environ['DJANGO_SETTINGS_MODULE'] = \
...    'lino_welfare.projects.eupen.settings.doctests'
>>> from lino.api.doctest import *
>>> print(settings.SETTINGS_MODULE)
lino_welfare.projects.eupen.settings.doctests


Configuring excerpts
====================

This is the list of excerpt types:

>>> rt.show(excerpts.ExcerptTypes)
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
===================================================== ======== =============== =========================== ====================== ================= ================================
 Modell                                                  Primär   Bescheinigend   Bezeichnung                 Konstruktionsmethode   Vorlage           Textkörper-Vorlage
----------------------------------------------------- -------- --------------- --------------------------- ---------------------- ----------------- --------------------------------
 *aids.IncomeConfirmation (Einkommensbescheinigung)*   Ja       Ja              Einkommensbescheinigung                            Default.odt       certificate.body.html
 *aids.RefundConfirmation (Kostenübernahmeschein)*     Ja       Ja              Kostenübernahmeschein                              Default.odt       certificate.body.html
 *aids.SimpleConfirmation (Einfache Bescheinigung)*    Ja       Ja              Einfache Bescheinigung                             Default.odt       certificate.body.html
 *art61.Contract (Art.61-Konvention)*                  Ja       Ja              Art.61-Konvention                                  Default.odt       contract.body.html
 *cal.Guest (Teilnehmer)*                              Ja       Nein            Anwesenheitsbescheinigung                          Default.odt       presence_certificate.body.html
 *debts.Budget (Budget)*                               Ja       Ja              Finanzielle Situation                              Default.odt
 *isip.Contract (VSE)*                                 Ja       Ja              VSE                                                Default.odt
 *jobs.Contract (Art.60§7-Konvention)*                 Ja       Ja              Art.60§7-Konvention                                Default.odt
 *pcsw.Client (Klient)*                                Ja       Nein            Aktenblatt                                         file_sheet.odt
 *pcsw.Client (Klient)*                                Nein     Nein            Aktionsplan                                        Default.odt       pac.body.html
 *pcsw.Client (Klient)*                                Nein     Nein            Curriculum vitae            AppyRtfBuildMethod     cv.odt
 *pcsw.Client (Klient)*                                Nein     Nein            eID-Inhalt                                         eid-content.odt
 **Total (12 Zeilen)**                                 **9**    **7**
===================================================== ======== =============== =========================== ====================== ================= ================================
<BLANKLINE>


Demo excerpts
=============

Here is the list of all demo excerpts. It shows e.g. how the language
of an excerpt depends on the recipient and the client.

>>> rt.show(excerpts.Excerpts, language="en")
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
==== ======================== ================================================ ============================= ========================== ========== ============
 ID   Excerpt Type             Controlled by                                    Client                        Recipient (Organization)   Language   build time
---- ------------------------ ------------------------------------------------ ----------------------------- -------------------------- ---------- ------------
 1    Income confirmation      *EiEi/9/29/12/116/1*                             AUSDEMWALD Alfons (116)                                  de
 2    Income confirmation      *EiEi/8/9/14/116/4*                              AUSDEMWALD Alfons (116)                                  de
 3    Income confirmation      *EiEi/10/19/12/127/7*                            EVERS Eberhart (127)                                     en
 4    Income confirmation      *EiEi/2/22/14/129/10*                            ENGELS Edgar (129)                                       de
 5    Income confirmation      *EiEi/11/18/12/137/13*                           JACOBS Jacqueline (137)                                  de
 6    Income confirmation      *EiEi/3/24/14/141/16*                            KAIVERS Karl (141)                                       en
 7    Income confirmation      *EiEi/10/17/13/144/19*                           LAZARUS Line (144)                                       de
 8    Income confirmation      *EiEi/4/13/14/147/22*                            MEESSEN Melissa (147)                                    de
 9    Income confirmation      *EiEi/1/7/13/157/25*                             RADERMACHER Edgard (157)                                 de
 10   Income confirmation      *EiEi/5/13/14/159/28*                            RADERMACHER Guido (159)                                  de
 11   Income confirmation      *EiEi/2/6/13/168/31*                             ÖSTGES Otto (168)                                        fr
 12   Income confirmation      *EiEi/2/16/13/177/34*                            BRECHT Bernd (177)                                       de
 13   Income confirmation      *EiEi/1/5/14/179/37*                             DUBOIS Robin (179)                                       de
 14   Income confirmation      *EiEi/7/2/14/181/40*                             JEANÉMART Jérôme (181)                                   fr
 15   Income confirmation      *EiEi/5/22/14/116/41*                            AUSDEMWALD Alfons (116)                                  de
 16   Income confirmation      *EiEi/5/22/14/116/42*                            AUSDEMWALD Alfons (116)                                  de
 17   Income confirmation      *EiEi/5/22/14/118/43*                            COLLARD Charlotte (118)                                  de
 18   Income confirmation      *Ausländerbeihilfe/8/8/13/116/2*                 AUSDEMWALD Alfons (116)                                  de
 19   Income confirmation      *Ausländerbeihilfe/8/8/13/116/3*                 AUSDEMWALD Alfons (116)                                  de
 20   Income confirmation      *Ausländerbeihilfe/10/9/12/124/5*                DOBBELSTEIN Dorothée (124)                               fr
 21   Income confirmation      *Ausländerbeihilfe/10/9/12/124/6*                DOBBELSTEIN Dorothée (124)                               fr
 22   Income confirmation      *Ausländerbeihilfe/10/29/12/129/8*               ENGELS Edgar (129)                                       de
 23   Income confirmation      *Ausländerbeihilfe/10/29/12/129/9*               ENGELS Edgar (129)                                       de
 24   Income confirmation      *Ausländerbeihilfe/11/8/12/132/11*               GROTECLAES Gregory (132)                                 de
 25   Income confirmation      *Ausländerbeihilfe/11/8/12/132/12*               GROTECLAES Gregory (132)                                 de
 26   Income confirmation      *Ausländerbeihilfe/11/28/12/141/14*              KAIVERS Karl (141)                                       en
 27   Income confirmation      *Ausländerbeihilfe/11/28/12/141/15*              KAIVERS Karl (141)                                       en
 28   Income confirmation      *Ausländerbeihilfe/12/8/12/144/17*               LAZARUS Line (144)                                       de
 29   Income confirmation      *Ausländerbeihilfe/12/8/12/144/18*               LAZARUS Line (144)                                       de
 30   Income confirmation      *Ausländerbeihilfe/12/18/12/147/20*              MEESSEN Melissa (147)                                    de
 31   Income confirmation      *Ausländerbeihilfe/12/18/12/147/21*              MEESSEN Melissa (147)                                    de
 32   Income confirmation      *Ausländerbeihilfe/12/28/12/153/23*              RADERMACHER Alfons (153)                                 fr
 33   Income confirmation      *Ausländerbeihilfe/12/28/12/153/24*              RADERMACHER Alfons (153)                                 fr
 34   Income confirmation      *Ausländerbeihilfe/1/17/13/159/26*               RADERMACHER Guido (159)                                  de
 35   Income confirmation      *Ausländerbeihilfe/1/17/13/159/27*               RADERMACHER Guido (159)                                  de
 36   Income confirmation      *Ausländerbeihilfe/1/27/13/165/29*               DA VINCI David (165)                                     de
 37   Income confirmation      *Ausländerbeihilfe/1/27/13/165/30*               DA VINCI David (165)                                     de
 38   Income confirmation      *Ausländerbeihilfe/6/2/14/168/32*                ÖSTGES Otto (168)                                        fr
 39   Income confirmation      *Ausländerbeihilfe/6/2/14/168/33*                ÖSTGES Otto (168)                                        fr
 40   Income confirmation      *Ausländerbeihilfe/2/26/13/179/35*               DUBOIS Robin (179)                                       de
 41   Income confirmation      *Ausländerbeihilfe/2/26/13/179/36*               DUBOIS Robin (179)                                       de
 42   Income confirmation      *Ausländerbeihilfe/3/8/13/181/38*                JEANÉMART Jérôme (181)                                   fr
 43   Income confirmation      *Ausländerbeihilfe/3/8/13/181/39*                JEANÉMART Jérôme (181)                                   fr
 44   Income confirmation      *Ausländerbeihilfe/5/23/14/124/44*               DOBBELSTEIN Dorothée (124)                               fr
 45   Income confirmation      *Ausländerbeihilfe/5/23/14/124/45*               DOBBELSTEIN Dorothée (124)                               fr
 46   Income confirmation      *Ausländerbeihilfe/5/23/14/127/46*               EVERS Eberhart (127)                                     en
 47   Income confirmation      *Feste Beihilfe/5/24/14/128/47*                  EMONTS Daniel (128)                                      de
 48   Income confirmation      *Feste Beihilfe/5/24/14/128/48*                  EMONTS Daniel (128)                                      de
 49   Income confirmation      *Feste Beihilfe/5/24/14/129/49*                  ENGELS Edgar (129)                                       de
 50   Simple confirmation      *Erstattung/5/25/14/130/1*                       FAYMONVILLE Luc (130*)                                   de
 51   Simple confirmation      *Erstattung/5/25/14/130/2*                       FAYMONVILLE Luc (130*)                                   de
 52   Simple confirmation      *Erstattung/5/25/14/132/3*                       GROTECLAES Gregory (132)                                 de
 53   Simple confirmation      *Übernahmeschein/5/26/14/133/4*                  HILGERS Hildegard (133)                                  de
 54   Simple confirmation      *Übernahmeschein/5/26/14/133/5*                  HILGERS Hildegard (133)                                  de
 55   Simple confirmation      *Übernahmeschein/5/26/14/137/6*                  JACOBS Jacqueline (137)                                  de
 56   Refund confirmation      *AMK/5/27/14/139/1*                              JONAS Josef (139)                                        fr
 57   Refund confirmation      *AMK/5/27/14/139/2*                              JONAS Josef (139)                                        fr
 58   Refund confirmation      *AMK/5/27/14/139/3*                              JONAS Josef (139)                                        fr
 59   Refund confirmation      *AMK/5/27/14/141/4*                              KAIVERS Karl (141)                                       en
 60   Refund confirmation      *AMK/5/27/14/141/5*                              KAIVERS Karl (141)                                       en
 61   Refund confirmation      *AMK/5/27/14/141/6*                              KAIVERS Karl (141)                                       en
 62   Refund confirmation      *DMH/5/28/14/142/7*                              LAMBERTZ Guido (142)                                     de
 63   Refund confirmation      *DMH/5/28/14/142/8*                              LAMBERTZ Guido (142)                                     de
 64   Refund confirmation      *DMH/5/28/14/142/9*                              LAMBERTZ Guido (142)                                     de
 65   Refund confirmation      *DMH/5/28/14/144/10*                             LAZARUS Line (144)                                       de
 66   Refund confirmation      *DMH/5/28/14/144/11*                             LAZARUS Line (144)                                       de
 67   Refund confirmation      *DMH/5/28/14/144/12*                             LAZARUS Line (144)                                       de
 68   Simple confirmation      *Furniture/5/29/14/146/7*                        MALMENDIER Marc (146)                                    de
 69   Simple confirmation      *Furniture/5/29/14/146/8*                        MALMENDIER Marc (146)                                    de
 70   Simple confirmation      *Furniture/5/29/14/147/9*                        MEESSEN Melissa (147)                                    de
 71   Simple confirmation      *Heating costs/5/30/14/152/10*                   EMONTS-GAST Erna (152)                                   fr
 72   Simple confirmation      *Heating costs/5/30/14/152/11*                   EMONTS-GAST Erna (152)                                   fr
 73   Simple confirmation      *Heating costs/5/30/14/153/12*                   RADERMACHER Alfons (153)                                 fr
 74   Simple confirmation      *Food bank/5/31/14/155/13*                       RADERMACHER Christian (155)                              en
 75   Simple confirmation      *Food bank/5/31/14/155/14*                       RADERMACHER Christian (155)                              en
 76   Simple confirmation      *Food bank/5/31/14/157/15*                       RADERMACHER Edgard (157)                                 de
 77   Simple confirmation      *Clothes bank/6/1/14/159/16*                     RADERMACHER Guido (159)                                  de
 78   Simple confirmation      *Clothes bank/6/1/14/159/17*                     RADERMACHER Guido (159)                                  de
 79   Simple confirmation      *Clothes bank/6/1/14/161/18*                     RADERMACHER Hedi (161)                                   de
 80   Simple confirmation      *Clothes bank/5/22/14/238/19*                    FRISCH Paul (238)             Belgisches Rotes Kreuz     de
 81   Finanzielle Situation    *Budget 1 for Gerkens-Kasennova*
 82   Art61 job supplyment     *Art61 job supplyment#1 (Daniel EMONTS)*         EMONTS Daniel (128)
 83   Art60§7 job supplyment   *Art60§7 job supplyment#1 (Charlotte COLLARD)*   COLLARD Charlotte (118)       BISA                       fr
 84   ISIP                     *ISIP#1 (Alfons AUSDEMWALD)*                     AUSDEMWALD Alfons (116)
 85   Presence certificate     *Participant #1 (22.05.2014)*                    AUSDEMWALD Alfons (116)                                  de
 86   Curriculum vitae         *AUSDEMWALD Alfons (116)*                        AUSDEMWALD Alfons (116)                                  de
 87   File sheet               *AUSDEMWALD Alfons (116)*                        AUSDEMWALD Alfons (116)                                  de
 88   eID sheet                *AUSDEMWALD Alfons (116)*                        AUSDEMWALD Alfons (116)                                  de
 89   Action plan              *AUSDEMWALD Alfons (116)*                        AUSDEMWALD Alfons (116)                                  de
==== ======================== ================================================ ============================= ========================== ========== ============
<BLANKLINE>


As for the default language of an excerpt: the recipient overrides the
owner.  Excerpt 88 (the only example) is in *French* because the
recipient (BISA) speaks French and although the owner (Charlotte)
speaks *German*:

>>> print(contacts.Partner.objects.get(id=196).language)
fr
>>> print(contacts.Partner.objects.get(id=118).language)
de
