.. _welfare.tested.excerpts:

=============
Excerpts
=============

.. How to test only this document:

  $ python setup.py test -s tests.DocsTests.test_excerpts


.. contents::
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
======================================================= ======== =============== =========================== ====================== ================= ================================
 Modell                                                  Primär   Bescheinigend   Bezeichnung                 Konstruktionsmethode   Vorlage           Textkörper-Vorlage
------------------------------------------------------- -------- --------------- --------------------------- ---------------------- ----------------- --------------------------------
 **aids.IncomeConfirmation (Einkommensbescheinigung)**   Ja       Ja              Einkommensbescheinigung                            Default.odt       certificate.body.html
 **aids.RefundConfirmation (Kostenübernahmeschein)**     Ja       Ja              Kostenübernahmeschein                              Default.odt       certificate.body.html
 **aids.SimpleConfirmation (Einfache Bescheinigung)**    Ja       Ja              Einfache Bescheinigung                             Default.odt       certificate.body.html
 **art61.Contract (Art.61-Konvention)**                  Ja       Ja              Art.61-Konvention                                  Default.odt
 **cal.Guest (Teilnehmer)**                              Ja       Nein            Anwesenheitsbescheinigung                          Default.odt       presence_certificate.body.html
 **debts.Budget (Budget)**                               Ja       Ja              Finanzielle Situation                              Default.odt
 **isip.Contract (VSE)**                                 Ja       Ja              VSE                                                Default.odt
 **jobs.Contract (Art.60§7-Konvention)**                 Ja       Ja              Art.60§7-Konvention                                Default.odt
 **pcsw.Client (Klient)**                                Ja       Nein            Aktenblatt                                         file_sheet.odt
 **pcsw.Client (Klient)**                                Nein     Nein            Aktionsplan                                        Default.odt       pac.body.html
 **pcsw.Client (Klient)**                                Nein     Nein            Curriculum vitae            AppyRtfBuildMethod     cv.odt
 **pcsw.Client (Klient)**                                Nein     Nein            eID-Inhalt                                         eid-content.odt
 **Total (12 Zeilen)**                                   **9**    **7**
======================================================= ======== =============== =========================== ====================== ================= ================================
<BLANKLINE>


Demo excerpts
=============

Here is the list of all demo excerpts. It shows e.g. how the language
of an excerpt depends on the recipient and the client.

>>> rt.show(excerpts.Excerpts, language="en")
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
==== ======================== ================================================== ============================= =============================== ========== ============
 ID   Excerpt Type             Controlled by                                      Client                        Recipient (Organization)        Language   build time
---- ------------------------ -------------------------------------------------- ----------------------------- ------------------------------- ---------- ------------
 1    Income confirmation      **EiEi/9/29/12/116/1**                             AUSDEMWALD Alfons (116)                                       de
 2    Income confirmation      **EiEi/8/9/14/116/4**                              AUSDEMWALD Alfons (116)                                       de
 3    Income confirmation      **EiEi/10/19/12/127/7**                            EVERS Eberhart (127)                                          en
 4    Income confirmation      **EiEi/8/29/14/127/10**                            EVERS Eberhart (127)                                          en
 5    Income confirmation      **EiEi/2/22/14/129/13**                            ENGELS Edgar (129)                                            de
 6    Income confirmation      **EiEi/11/18/12/137/16**                           JACOBS Jacqueline (137)                                       de
 7    Income confirmation      **EiEi/3/24/14/141/19**                            KAIVERS Karl (141)                                            en
 8    Income confirmation      **EiEi/10/17/13/144/22**                           LAZARUS Line (144)                                            de
 9    Income confirmation      **EiEi/4/13/14/147/25**                            MEESSEN Melissa (147)                                         de
 10   Income confirmation      **EiEi/1/7/13/157/28**                             RADERMACHER Edgard (157)                                      de
 11   Income confirmation      **EiEi/1/17/13/159/31**                            RADERMACHER Guido (159)                                       de
 12   Income confirmation      **EiEi/1/27/13/165/34**                            DA VINCI David (165)                                          de
 13   Income confirmation      **EiEi/6/2/14/168/37**                             ÖSTGES Otto (168)                                             fr
 14   Income confirmation      **EiEi/2/26/13/179/40**                            DUBOIS Robin (179)                                            de
 15   Income confirmation      **EiEi/3/8/13/181/43**                             JEANÉMART Jérôme (181)                                        fr
 16   Income confirmation      **EiEi/5/22/14/116/46**                            AUSDEMWALD Alfons (116)                                       de
 17   Income confirmation      **EiEi/5/22/14/118/47**                            COLLARD Charlotte (118)                                       de
 18   Income confirmation      **EiEi/5/22/14/118/48**                            COLLARD Charlotte (118)                                       de
 19   Income confirmation      **Ausländerbeihilfe/8/8/13/116/2**                 AUSDEMWALD Alfons (116)                                       de
 20   Income confirmation      **Ausländerbeihilfe/8/8/13/116/3**                 AUSDEMWALD Alfons (116)                                       de
 21   Income confirmation      **Ausländerbeihilfe/10/9/12/124/5**                DOBBELSTEIN Dorothée (124)                                    fr
 22   Income confirmation      **Ausländerbeihilfe/10/9/12/124/6**                DOBBELSTEIN Dorothée (124)                                    fr
 23   Income confirmation      **Ausländerbeihilfe/8/28/13/127/8**                EVERS Eberhart (127)                                          en
 24   Income confirmation      **Ausländerbeihilfe/8/28/13/127/9**                EVERS Eberhart (127)                                          en
 25   Income confirmation      **Ausländerbeihilfe/10/29/12/129/11**              ENGELS Edgar (129)                                            de
 26   Income confirmation      **Ausländerbeihilfe/10/29/12/129/12**              ENGELS Edgar (129)                                            de
 27   Income confirmation      **Ausländerbeihilfe/11/8/12/132/14**               GROTECLAES Gregory (132)                                      de
 28   Income confirmation      **Ausländerbeihilfe/11/8/12/132/15**               GROTECLAES Gregory (132)                                      de
 29   Income confirmation      **Ausländerbeihilfe/11/28/12/141/17**              KAIVERS Karl (141)                                            en
 30   Income confirmation      **Ausländerbeihilfe/11/28/12/141/18**              KAIVERS Karl (141)                                            en
 31   Income confirmation      **Ausländerbeihilfe/12/8/12/144/20**               LAZARUS Line (144)                                            de
 32   Income confirmation      **Ausländerbeihilfe/12/8/12/144/21**               LAZARUS Line (144)                                            de
 33   Income confirmation      **Ausländerbeihilfe/12/18/12/147/23**              MEESSEN Melissa (147)                                         de
 34   Income confirmation      **Ausländerbeihilfe/12/18/12/147/24**              MEESSEN Melissa (147)                                         de
 35   Income confirmation      **Ausländerbeihilfe/12/28/12/153/26**              RADERMACHER Alfons (153)                                      fr
 36   Income confirmation      **Ausländerbeihilfe/12/28/12/153/27**              RADERMACHER Alfons (153)                                      fr
 37   Income confirmation      **Ausländerbeihilfe/11/16/13/157/29**              RADERMACHER Edgard (157)                                      de
 38   Income confirmation      **Ausländerbeihilfe/11/16/13/157/30**              RADERMACHER Edgard (157)                                      de
 39   Income confirmation      **Ausländerbeihilfe/5/13/14/159/32**               RADERMACHER Guido (159)                                       de
 40   Income confirmation      **Ausländerbeihilfe/5/13/14/159/33**               RADERMACHER Guido (159)                                       de
 41   Income confirmation      **Ausländerbeihilfe/2/6/13/168/35**                ÖSTGES Otto (168)                                             fr
 42   Income confirmation      **Ausländerbeihilfe/2/6/13/168/36**                ÖSTGES Otto (168)                                             fr
 43   Income confirmation      **Ausländerbeihilfe/2/16/13/177/38**               BRECHT Bernd (177)                                            de
 44   Income confirmation      **Ausländerbeihilfe/2/16/13/177/39**               BRECHT Bernd (177)                                            de
 45   Income confirmation      **Ausländerbeihilfe/1/5/14/179/41**                DUBOIS Robin (179)                                            de
 46   Income confirmation      **Ausländerbeihilfe/1/5/14/179/42**                DUBOIS Robin (179)                                            de
 47   Income confirmation      **Ausländerbeihilfe/7/2/14/181/44**                JEANÉMART Jérôme (181)                                        fr
 48   Income confirmation      **Ausländerbeihilfe/7/2/14/181/45**                JEANÉMART Jérôme (181)                                        fr
 49   Income confirmation      **Ausländerbeihilfe/5/23/14/124/49**               DOBBELSTEIN Dorothée (124)                                    fr
 50   Income confirmation      **Ausländerbeihilfe/5/23/14/127/50**               EVERS Eberhart (127)                                          en
 51   Income confirmation      **Ausländerbeihilfe/5/23/14/127/51**               EVERS Eberhart (127)                                          en
 52   Income confirmation      **Feste Beihilfe/5/24/14/128/52**                  EMONTS Daniel (128)                                           de
 53   Income confirmation      **Feste Beihilfe/5/24/14/129/53**                  ENGELS Edgar (129)                                            de
 54   Income confirmation      **Feste Beihilfe/5/24/14/129/54**                  ENGELS Edgar (129)                                            de
 55   Simple confirmation      **Erstattung/5/25/14/130/1**                       FAYMONVILLE Luc (130*)                                        de
 56   Simple confirmation      **Erstattung/5/25/14/132/2**                       GROTECLAES Gregory (132)                                      de
 57   Simple confirmation      **Erstattung/5/25/14/132/3**                       GROTECLAES Gregory (132)                                      de
 58   Simple confirmation      **Übernahmeschein/5/26/14/133/4**                  HILGERS Hildegard (133)                                       de
 59   Simple confirmation      **Übernahmeschein/5/26/14/137/5**                  JACOBS Jacqueline (137)                                       de
 60   Simple confirmation      **Übernahmeschein/5/26/14/137/6**                  JACOBS Jacqueline (137)                                       de
 61   Refund confirmation      **AMK/5/27/14/139/1**                              JONAS Josef (139)                                             fr
 62   Refund confirmation      **AMK/5/27/14/139/2**                              JONAS Josef (139)                                             fr
 63   Refund confirmation      **AMK/5/27/14/139/3**                              JONAS Josef (139)                                             fr
 64   Refund confirmation      **AMK/5/27/14/141/4**                              KAIVERS Karl (141)                                            en
 65   Refund confirmation      **AMK/5/27/14/141/5**                              KAIVERS Karl (141)                                            en
 66   Refund confirmation      **AMK/5/27/14/141/6**                              KAIVERS Karl (141)                                            en
 67   Refund confirmation      **DMH/5/28/14/142/7**                              LAMBERTZ Guido (142)                                          de
 68   Refund confirmation      **DMH/5/28/14/142/8**                              LAMBERTZ Guido (142)                                          de
 69   Refund confirmation      **DMH/5/28/14/142/9**                              LAMBERTZ Guido (142)                                          de
 70   Refund confirmation      **DMH/5/28/14/144/10**                             LAZARUS Line (144)                                            de
 71   Refund confirmation      **DMH/5/28/14/144/11**                             LAZARUS Line (144)                                            de
 72   Refund confirmation      **DMH/5/28/14/144/12**                             LAZARUS Line (144)                                            de
 73   Simple confirmation      **Furniture/5/29/14/146/7**                        MALMENDIER Marc (146)                                         de
 74   Simple confirmation      **Furniture/5/29/14/147/8**                        MEESSEN Melissa (147)                                         de
 75   Simple confirmation      **Furniture/5/29/14/147/9**                        MEESSEN Melissa (147)                                         de
 76   Simple confirmation      **Heating costs/5/30/14/152/10**                   EMONTS-GAST Erna (152)                                        fr
 77   Simple confirmation      **Heating costs/5/30/14/153/11**                   RADERMACHER Alfons (153)                                      fr
 78   Simple confirmation      **Heating costs/5/30/14/153/12**                   RADERMACHER Alfons (153)                                      fr
 79   Simple confirmation      **Food bank/5/31/14/155/13**                       RADERMACHER Christian (155)                                   en
 80   Simple confirmation      **Food bank/5/31/14/157/14**                       RADERMACHER Edgard (157)                                      de
 81   Simple confirmation      **Food bank/5/31/14/157/15**                       RADERMACHER Edgard (157)                                      de
 82   Simple confirmation      **Clothes bank/6/1/14/159/16**                     RADERMACHER Guido (159)                                       de
 83   Simple confirmation      **Clothes bank/6/1/14/161/17**                     RADERMACHER Hedi (161)                                        de
 84   Simple confirmation      **Clothes bank/6/1/14/161/18**                     RADERMACHER Hedi (161)                                        de
 85   Simple confirmation      **Clothes bank/5/22/14/238/19**                    FRISCH Paul (238)             Belgisches Rotes Kreuz (100*)   de
 86   Finanzielle Situation    **Budget 1 for Gerkens-Kasennova (230)**
 87   Art61 job supplyment     **Art61 job supplyment#1 (Daniel EMONTS)**         EMONTS Daniel (128)           Belgisches Rotes Kreuz (100*)   de
 88   Art60§7 job supplyment   **Art60§7 job supplyment#1 (Charlotte COLLARD)**   COLLARD Charlotte (118)       BISA (196)                      fr
 89   ISIP                     **ISIP#1 (Alfons AUSDEMWALD)**                     AUSDEMWALD Alfons (116)
 90   Presence certificate     **Participant #1 (22.05.2014)**                    AUSDEMWALD Alfons (116)                                       de
 91   Curriculum vitae         **AUSDEMWALD Alfons (116)**                        AUSDEMWALD Alfons (116)                                       de
 92   File sheet               **AUSDEMWALD Alfons (116)**                        AUSDEMWALD Alfons (116)                                       de
 93   eID sheet                **AUSDEMWALD Alfons (116)**                        AUSDEMWALD Alfons (116)                                       de
 94   Action plan              **AUSDEMWALD Alfons (116)**                        AUSDEMWALD Alfons (116)                                       de
==== ======================== ================================================== ============================= =============================== ========== ============
<BLANKLINE>



As for the default language of an excerpt: the recipient overrides the
owner.  Excerpt 88 (the only example) is in *French* because the
recipient (BISA) speaks French and although the owner (Charlotte)
speaks *German*:

>>> print(contacts.Partner.objects.get(id=196).language)
fr
>>> print(contacts.Partner.objects.get(id=118).language)
de
