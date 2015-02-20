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


>>> rt.show(excerpts.Excerpts)
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
==== =========================== =============================================== ============================= =============================== ========= ============
 ID   Auszugsart                  Verknüpft mit                                   Klient                        Empfänger (Organisation)        Sprache   Druckdatum
---- --------------------------- ----------------------------------------------- ----------------------------- ------------------------------- --------- ------------
 1    Einkommensbescheinigung     **EiEi/29.09.12/116/1**                         AUSDEMWALD Alfons (116)                                       de
 2    Einkommensbescheinigung     **EiEi/09.08.14/116/4**                         AUSDEMWALD Alfons (116)                                       de
 3    Einkommensbescheinigung     **EiEi/19.10.12/127/7**                         EVERS Eberhart (127)                                          nl
 4    Einkommensbescheinigung     **EiEi/29.08.14/127/10**                        EVERS Eberhart (127)                                          nl
 5    Einkommensbescheinigung     **EiEi/22.02.14/129/13**                        ENGELS Edgar (129)                                            de
 6    Einkommensbescheinigung     **EiEi/18.11.12/137/16**                        JACOBS Jacqueline (137)                                       de
 7    Einkommensbescheinigung     **EiEi/24.03.14/141/19**                        KAIVERS Karl (141)                                            nl
 8    Einkommensbescheinigung     **EiEi/17.10.13/144/22**                        LAZARUS Line (144)                                            de
 9    Einkommensbescheinigung     **EiEi/13.04.14/147/25**                        MEESSEN Melissa (147)                                         de
 10   Einkommensbescheinigung     **EiEi/07.01.13/157/28**                        RADERMACHER Edgard (157)                                      de
 11   Einkommensbescheinigung     **EiEi/17.01.13/159/31**                        RADERMACHER Guido (159)                                       de
 12   Einkommensbescheinigung     **EiEi/27.01.13/165/34**                        DA VINCI David (165)                                          de
 13   Einkommensbescheinigung     **EiEi/02.06.14/168/37**                        ÖSTGES Otto (168)                                             fr
 14   Einkommensbescheinigung     **EiEi/26.02.13/179/40**                        DUBOIS Robin (179)                                            de
 15   Einkommensbescheinigung     **EiEi/08.03.13/181/43**                        JEANÉMART Jérôme (181)                                        fr
 16   Einkommensbescheinigung     **EiEi/22.05.14/116/46**                        AUSDEMWALD Alfons (116)                                       de
 17   Einkommensbescheinigung     **EiEi/22.05.14/118/47**                        COLLARD Charlotte (118)                                       de
 18   Einkommensbescheinigung     **EiEi/22.05.14/118/48**                        COLLARD Charlotte (118)                                       de
 19   Einkommensbescheinigung     **Ausländerbeihilfe/08.08.13/116/2**            AUSDEMWALD Alfons (116)                                       de
 20   Einkommensbescheinigung     **Ausländerbeihilfe/08.08.13/116/3**            AUSDEMWALD Alfons (116)                                       de
 21   Einkommensbescheinigung     **Ausländerbeihilfe/09.10.12/124/5**            DOBBELSTEIN Dorothée (124)                                    fr
 22   Einkommensbescheinigung     **Ausländerbeihilfe/09.10.12/124/6**            DOBBELSTEIN Dorothée (124)                                    fr
 23   Einkommensbescheinigung     **Ausländerbeihilfe/28.08.13/127/8**            EVERS Eberhart (127)                                          nl
 24   Einkommensbescheinigung     **Ausländerbeihilfe/28.08.13/127/9**            EVERS Eberhart (127)                                          nl
 25   Einkommensbescheinigung     **Ausländerbeihilfe/29.10.12/129/11**           ENGELS Edgar (129)                                            de
 26   Einkommensbescheinigung     **Ausländerbeihilfe/29.10.12/129/12**           ENGELS Edgar (129)                                            de
 27   Einkommensbescheinigung     **Ausländerbeihilfe/08.11.12/132/14**           GROTECLAES Gregory (132)                                      de
 28   Einkommensbescheinigung     **Ausländerbeihilfe/08.11.12/132/15**           GROTECLAES Gregory (132)                                      de
 29   Einkommensbescheinigung     **Ausländerbeihilfe/28.11.12/141/17**           KAIVERS Karl (141)                                            nl
 30   Einkommensbescheinigung     **Ausländerbeihilfe/28.11.12/141/18**           KAIVERS Karl (141)                                            nl
 31   Einkommensbescheinigung     **Ausländerbeihilfe/08.12.12/144/20**           LAZARUS Line (144)                                            de
 32   Einkommensbescheinigung     **Ausländerbeihilfe/08.12.12/144/21**           LAZARUS Line (144)                                            de
 33   Einkommensbescheinigung     **Ausländerbeihilfe/18.12.12/147/23**           MEESSEN Melissa (147)                                         de
 34   Einkommensbescheinigung     **Ausländerbeihilfe/18.12.12/147/24**           MEESSEN Melissa (147)                                         de
 35   Einkommensbescheinigung     **Ausländerbeihilfe/28.12.12/153/26**           RADERMACHER Alfons (153)                                      fr
 36   Einkommensbescheinigung     **Ausländerbeihilfe/28.12.12/153/27**           RADERMACHER Alfons (153)                                      fr
 37   Einkommensbescheinigung     **Ausländerbeihilfe/16.11.13/157/29**           RADERMACHER Edgard (157)                                      de
 38   Einkommensbescheinigung     **Ausländerbeihilfe/16.11.13/157/30**           RADERMACHER Edgard (157)                                      de
 39   Einkommensbescheinigung     **Ausländerbeihilfe/13.05.14/159/32**           RADERMACHER Guido (159)                                       de
 40   Einkommensbescheinigung     **Ausländerbeihilfe/13.05.14/159/33**           RADERMACHER Guido (159)                                       de
 41   Einkommensbescheinigung     **Ausländerbeihilfe/06.02.13/168/35**           ÖSTGES Otto (168)                                             fr
 42   Einkommensbescheinigung     **Ausländerbeihilfe/06.02.13/168/36**           ÖSTGES Otto (168)                                             fr
 43   Einkommensbescheinigung     **Ausländerbeihilfe/16.02.13/177/38**           BRECHT Bernd (177)                                            de
 44   Einkommensbescheinigung     **Ausländerbeihilfe/16.02.13/177/39**           BRECHT Bernd (177)                                            de
 45   Einkommensbescheinigung     **Ausländerbeihilfe/05.01.14/179/41**           DUBOIS Robin (179)                                            de
 46   Einkommensbescheinigung     **Ausländerbeihilfe/05.01.14/179/42**           DUBOIS Robin (179)                                            de
 47   Einkommensbescheinigung     **Ausländerbeihilfe/02.07.14/181/44**           JEANÉMART Jérôme (181)                                        fr
 48   Einkommensbescheinigung     **Ausländerbeihilfe/02.07.14/181/45**           JEANÉMART Jérôme (181)                                        fr
 49   Einkommensbescheinigung     **Ausländerbeihilfe/23.05.14/124/49**           DOBBELSTEIN Dorothée (124)                                    fr
 50   Einkommensbescheinigung     **Ausländerbeihilfe/23.05.14/127/50**           EVERS Eberhart (127)                                          nl
 51   Einkommensbescheinigung     **Ausländerbeihilfe/23.05.14/127/51**           EVERS Eberhart (127)                                          nl
 52   Einkommensbescheinigung     **Feste Beihilfe/24.05.14/128/52**              EMONTS Daniel (128)                                           de
 53   Einkommensbescheinigung     **Feste Beihilfe/24.05.14/129/53**              ENGELS Edgar (129)                                            de
 54   Einkommensbescheinigung     **Feste Beihilfe/24.05.14/129/54**              ENGELS Edgar (129)                                            de
 55   Einfache Bescheinigung      **Erstattung/25.05.14/130/1**                   FAYMONVILLE Luc (130*)                                        de
 56   Einfache Bescheinigung      **Erstattung/25.05.14/132/2**                   GROTECLAES Gregory (132)                                      de
 57   Einfache Bescheinigung      **Erstattung/25.05.14/132/3**                   GROTECLAES Gregory (132)                                      de
 58   Einfache Bescheinigung      **Übernahmeschein/26.05.14/133/4**              HILGERS Hildegard (133)                                       de
 59   Einfache Bescheinigung      **Übernahmeschein/26.05.14/137/5**              JACOBS Jacqueline (137)                                       de
 60   Einfache Bescheinigung      **Übernahmeschein/26.05.14/137/6**              JACOBS Jacqueline (137)                                       de
 61   Kostenübernahmeschein       **AMK/27.05.14/139/1**                          JONAS Josef (139)                                             fr
 62   Kostenübernahmeschein       **AMK/27.05.14/139/2**                          JONAS Josef (139)                                             fr
 63   Kostenübernahmeschein       **AMK/27.05.14/139/3**                          JONAS Josef (139)                                             fr
 64   Kostenübernahmeschein       **AMK/27.05.14/141/4**                          KAIVERS Karl (141)                                            nl
 65   Kostenübernahmeschein       **AMK/27.05.14/141/5**                          KAIVERS Karl (141)                                            nl
 66   Kostenübernahmeschein       **AMK/27.05.14/141/6**                          KAIVERS Karl (141)                                            nl
 67   Kostenübernahmeschein       **DMH/28.05.14/142/7**                          LAMBERTZ Guido (142)                                          de
 68   Kostenübernahmeschein       **DMH/28.05.14/142/8**                          LAMBERTZ Guido (142)                                          de
 69   Kostenübernahmeschein       **DMH/28.05.14/142/9**                          LAMBERTZ Guido (142)                                          de
 70   Kostenübernahmeschein       **DMH/28.05.14/144/10**                         LAZARUS Line (144)                                            de
 71   Kostenübernahmeschein       **DMH/28.05.14/144/11**                         LAZARUS Line (144)                                            de
 72   Kostenübernahmeschein       **DMH/28.05.14/144/12**                         LAZARUS Line (144)                                            de
 73   Einfache Bescheinigung      **Möbellager/29.05.14/146/7**                   MALMENDIER Marc (146)                                         de
 74   Einfache Bescheinigung      **Möbellager/29.05.14/147/8**                   MEESSEN Melissa (147)                                         de
 75   Einfache Bescheinigung      **Möbellager/29.05.14/147/9**                   MEESSEN Melissa (147)                                         de
 76   Einfache Bescheinigung      **Heizkosten/30.05.14/152/10**                  EMONTS-GAST Erna (152)                                        fr
 77   Einfache Bescheinigung      **Heizkosten/30.05.14/153/11**                  RADERMACHER Alfons (153)                                      fr
 78   Einfache Bescheinigung      **Heizkosten/30.05.14/153/12**                  RADERMACHER Alfons (153)                                      fr
 79   Einfache Bescheinigung      **Lebensmittelbank/31.05.14/155/13**            RADERMACHER Christian (155)                                   nl
 80   Einfache Bescheinigung      **Lebensmittelbank/31.05.14/157/14**            RADERMACHER Edgard (157)                                      de
 81   Einfache Bescheinigung      **Lebensmittelbank/31.05.14/157/15**            RADERMACHER Edgard (157)                                      de
 82   Einfache Bescheinigung      **Kleiderkammer/01.06.14/159/16**               RADERMACHER Guido (159)                                       de
 83   Einfache Bescheinigung      **Kleiderkammer/01.06.14/161/17**               RADERMACHER Hedi (161)                                        de
 84   Einfache Bescheinigung      **Kleiderkammer/01.06.14/161/18**               RADERMACHER Hedi (161)                                        de
 85   Einfache Bescheinigung      **Kleiderkammer/22.05.14/238/19**               FRISCH Paul (238)             Belgisches Rotes Kreuz (100*)   de
 86   Finanzielle Situation       **Budget Nr. 1 für Gerkens-Kasennova (230)**
 87   Art.61-Konvention           **Art.61-Konvention#1 (Daniel EMONTS)**         EMONTS Daniel (128)           Belgisches Rotes Kreuz (100*)   de
 88   Art.60§7-Konvention         **Art.60§7-Konvention#1 (Charlotte COLLARD)**   COLLARD Charlotte (118)       BISA (196)                      fr
 89   VSE                         **VSE#1 (Alfons AUSDEMWALD)**                   AUSDEMWALD Alfons (116)
 90   Anwesenheitsbescheinigung   **Teilnehmer #1 (22.05.2014)**                  AUSDEMWALD Alfons (116)                                       de
 91   Curriculum vitae            **AUSDEMWALD Alfons (116)**                     AUSDEMWALD Alfons (116)                                       de
 92   Aktenblatt                  **AUSDEMWALD Alfons (116)**                     AUSDEMWALD Alfons (116)                                       de
 93   eID-Inhalt                  **AUSDEMWALD Alfons (116)**                     AUSDEMWALD Alfons (116)                                       de
 94   Aktionsplan                 **AUSDEMWALD Alfons (116)**                     AUSDEMWALD Alfons (116)                                       de
==== =========================== =============================================== ============================= =============================== ========= ============
<BLANKLINE>


As for the default language of an excerpt: the recipient overrides the
owner.  Excerpt 88 (the only example) is in *French* because the
recipient (BISA) speaks French and although the owner (Charlotte)
speaks *German*:

>>> print(contacts.Partner.objects.get(id=196).language)
fr
>>> print(contacts.Partner.objects.get(id=118).language)
de
