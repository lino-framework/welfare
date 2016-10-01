.. _welfare.specs.excerpts:

==========================================
Usage of database excerpts in Lino Welfare
==========================================

.. How to test only this document:

    $ python setup.py test -s tests.SpecsTests.test_excerpts
    
    doctest init:

    >>> import lino
    >>> lino.startup('lino_welfare.projects.eupen.settings.doctests')
    >>> from lino.api.doctest import *


.. contents::
   :local:
   :depth: 2


Configuring excerpts
====================

See also :doc:`/admin/printing`.

Here is a more complete list of excerpt types:

>>> rt.show(excerpts.ExcerptTypes)
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
======================================================= ======== =============== =========================== ====================== ============================= ================================
 Modell                                                  Primär   Bescheinigend   Bezeichnung                 Konstruktionsmethode   Vorlage                       Textkörper-Vorlage
------------------------------------------------------- -------- --------------- --------------------------- ---------------------- ----------------------------- --------------------------------
 *aids.IncomeConfirmation (Einkommensbescheinigung)*     Ja       Ja              Einkommensbescheinigung                            Default.odt                   certificate.body.html
 *aids.RefundConfirmation (Kostenübernahmeschein)*       Ja       Ja              Kostenübernahmeschein                              Default.odt                   certificate.body.html
 *aids.SimpleConfirmation (Einfache Bescheinigung)*      Ja       Ja              Einfache Bescheinigung                             Default.odt                   certificate.body.html
 *art61.Contract (Art.61-Konvention)*                    Ja       Ja              Art.61-Konvention                                                                contract.body.html
 *cal.Guest (Anwesenheit)*                               Ja       Nein            Anwesenheitsbescheinigung                          Default.odt                   presence_certificate.body.html
 *cbss.IdentifyPersonRequest (IdentifyPerson-Anfrage)*   Ja       Ja              IdentifyPerson-Anfrage
 *cbss.ManageAccessRequest (ManageAccess-Anfrage)*       Ja       Ja              ManageAccess-Anfrage
 *cbss.RetrieveTIGroupsRequest (Tx25-Anfrage)*           Ja       Ja              Tx25-Anfrage
 *contacts.Partner (Partner)*                            Nein     Nein            Zahlungserinnerung          WeasyPdfBuildMethod    payment_reminder.weasy.html
 *debts.Budget (Budget)*                                 Ja       Ja              Finanzielle Situation
 *esf.ClientSummary (ESF Summary)*                       Ja       Ja              Training report             WeasyPdfBuildMethod
 *finan.BankStatement (Kontoauszug)*                     Ja       Ja              Kontoauszug
 *finan.JournalEntry (Diverse Buchung)*                  Ja       Ja              Diverse Buchung
 *finan.PaymentOrder (Zahlungsauftrag)*                  Ja       Ja              Zahlungsauftrag
 *isip.Contract (VSE)*                                   Ja       Ja              VSE
 *jobs.Contract (Art.60§7-Konvention)*                   Ja       Ja              Art.60§7-Konvention
 *pcsw.Client (Klient)*                                  Ja       Nein            Aktenblatt                                         file_sheet.odt
 *pcsw.Client (Klient)*                                  Nein     Nein            Aktionsplan                                        Default.odt                   pac.body.html
 *pcsw.Client (Klient)*                                  Nein     Nein            Curriculum vitae            AppyRtfBuildMethod     cv.odt
 *pcsw.Client (Klient)*                                  Nein     Nein            eID-Inhalt                                         eid-content.odt
======================================================= ======== =============== =========================== ====================== ============================= ================================
<BLANKLINE>



Demo excerpts
=============

Here is a list of all demo excerpts. 

>>> rt.show(excerpts.AllExcerpts, language="en", column_names="id excerpt_type owner project company language")
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
==== ======================== ===================================================== ============================= ================================ ==========
 ID   Excerpt Type             Controlled by                                         Client                        Recipient (Organization)         Language
---- ------------------------ ----------------------------------------------------- ----------------------------- -------------------------------- ----------
 68   Action plan              *AUSDEMWALD Alfons (116)*                             AUSDEMWALD Alfons (116)                                        de
 67   eID sheet                *AUSDEMWALD Alfons (116)*                             AUSDEMWALD Alfons (116)                                        de
 66   File sheet               *AUSDEMWALD Alfons (116)*                             AUSDEMWALD Alfons (116)                                        de
 65   Curriculum vitae         *AUSDEMWALD Alfons (116)*                             AUSDEMWALD Alfons (116)                                        de
 64   Presence certificate     *Presence #1 (22.05.2014)*                            AUSDEMWALD Alfons (116)                                        de
 63   Payment reminder         *Belgisches Rotes Kreuz*                                                                                             de
 62   Art60§7 job supplyment   *Art60§7 job supplyment#16 (Denis DENON)*             DENON Denis (180*)            R-Cycle Sperrgutsortierzentrum   de
 61   Art60§7 job supplyment   *Art60§7 job supplyment#15 (Denis DENON)*             DENON Denis (180*)            BISA                             de
 60   Art60§7 job supplyment   *Art60§7 job supplyment#14 (Rik RADERMECKER)*         RADERMECKER Rik (173)         BISA                             de
 59   Art60§7 job supplyment   *Art60§7 job supplyment#13 (Rik RADERMECKER)*         RADERMECKER Rik (173)         Pro Aktiv V.o.G.                 de
 58   Art60§7 job supplyment   *Art60§7 job supplyment#12 (Vincent VAN VEEN)*        VAN VEEN Vincent (166)        Pro Aktiv V.o.G.                 de
 57   Art60§7 job supplyment   *Art60§7 job supplyment#11 (Fritz RADERMACHER)*       RADERMACHER Fritz (158)       R-Cycle Sperrgutsortierzentrum   de
 56   Art60§7 job supplyment   *Art60§7 job supplyment#10 (Christian RADERMACHER)*   RADERMACHER Christian (155)   R-Cycle Sperrgutsortierzentrum   de
 55   Art60§7 job supplyment   *Art60§7 job supplyment#9 (Christian RADERMACHER)*    RADERMACHER Christian (155)   BISA                             de
 54   Art60§7 job supplyment   *Art60§7 job supplyment#8 (Marc MALMENDIER)*          MALMENDIER Marc (146)         R-Cycle Sperrgutsortierzentrum   de
 53   Art60§7 job supplyment   *Art60§7 job supplyment#7 (Marc MALMENDIER)*          MALMENDIER Marc (146)         BISA                             de
 52   Art60§7 job supplyment   *Art60§7 job supplyment#6 (Guido LAMBERTZ)*           LAMBERTZ Guido (142)          BISA                             de
 51   Art60§7 job supplyment   *Art60§7 job supplyment#5 (Hildegard HILGERS)*        HILGERS Hildegard (133)       Pro Aktiv V.o.G.                 de
 50   Art60§7 job supplyment   *Art60§7 job supplyment#4 (Luc FAYMONVILLE)*          FAYMONVILLE Luc (130*)        Pro Aktiv V.o.G.                 de
 49   Art60§7 job supplyment   *Art60§7 job supplyment#3 (Luc FAYMONVILLE)*          FAYMONVILLE Luc (130*)        R-Cycle Sperrgutsortierzentrum   de
 48   Art60§7 job supplyment   *Art60§7 job supplyment#2 (Bernd EVERTZ)*             EVERTZ Bernd (126)            R-Cycle Sperrgutsortierzentrum   de
 47   Art60§7 job supplyment   *Art60§7 job supplyment#1 (Charlotte COLLARD)*        COLLARD Charlotte (118)       BISA                             de
 46   ISIP                     *ISIP#33 (Jérôme JEANÉMART)*                          JEANÉMART Jérôme (181)
 45   ISIP                     *ISIP#32 (Jérôme JEANÉMART)*                          JEANÉMART Jérôme (181)
 44   ISIP                     *ISIP#31 (Robin DUBOIS)*                              DUBOIS Robin (179)
 43   ISIP                     *ISIP#30 (Robin DUBOIS)*                              DUBOIS Robin (179)
 42   ISIP                     *ISIP#29 (Robin DUBOIS)*                              DUBOIS Robin (179)
 41   ISIP                     *ISIP#28 (Bernd BRECHT)*                              BRECHT Bernd (177)
 40   ISIP                     *ISIP#27 (Bernd BRECHT)*                              BRECHT Bernd (177)
 39   ISIP                     *ISIP#26 (Otto ÖSTGES)*                               ÖSTGES Otto (168)
 38   ISIP                     *ISIP#25 (Otto ÖSTGES)*                               ÖSTGES Otto (168)
 37   ISIP                     *ISIP#24 (Otto ÖSTGES)*                               ÖSTGES Otto (168)
 36   ISIP                     *ISIP#23 (David DA VINCI)*                            DA VINCI David (165)
 35   ISIP                     *ISIP#22 (David DA VINCI)*                            DA VINCI David (165)
 34   ISIP                     *ISIP#21 (Guido RADERMACHER)*                         RADERMACHER Guido (159)
 33   ISIP                     *ISIP#20 (Guido RADERMACHER)*                         RADERMACHER Guido (159)
 32   ISIP                     *ISIP#19 (Guido RADERMACHER)*                         RADERMACHER Guido (159)
 31   ISIP                     *ISIP#18 (Edgard RADERMACHER)*                        RADERMACHER Edgard (157)
 30   ISIP                     *ISIP#17 (Alfons RADERMACHER)*                        RADERMACHER Alfons (153)
 29   ISIP                     *ISIP#16 (Melissa MEESSEN)*                           MEESSEN Melissa (147)
 28   ISIP                     *ISIP#15 (Melissa MEESSEN)*                           MEESSEN Melissa (147)
 27   ISIP                     *ISIP#14 (Melissa MEESSEN)*                           MEESSEN Melissa (147)
 26   ISIP                     *ISIP#13 (Line LAZARUS)*                              LAZARUS Line (144)
 25   ISIP                     *ISIP#12 (Line LAZARUS)*                              LAZARUS Line (144)
 24   ISIP                     *ISIP#11 (Karl KAIVERS)*                              KAIVERS Karl (141)
 23   ISIP                     *ISIP#10 (Jacqueline JACOBS)*                         JACOBS Jacqueline (137)
 22   ISIP                     *ISIP#9 (Gregory GROTECLAES)*                         GROTECLAES Gregory (132)
 21   ISIP                     *ISIP#8 (Edgar ENGELS)*                               ENGELS Edgar (129)
 20   ISIP                     *ISIP#7 (Edgar ENGELS)*                               ENGELS Edgar (129)
 19   ISIP                     *ISIP#6 (Eberhart EVERS)*                             EVERS Eberhart (127)
 18   ISIP                     *ISIP#5 (Eberhart EVERS)*                             EVERS Eberhart (127)
 17   ISIP                     *ISIP#4 (Eberhart EVERS)*                             EVERS Eberhart (127)
 16   ISIP                     *ISIP#3 (Dorothée DOBBELSTEIN)*                       DOBBELSTEIN Dorothée (124)
 15   ISIP                     *ISIP#2 (Alfons AUSDEMWALD)*                          AUSDEMWALD Alfons (116)
 14   ISIP                     *ISIP#1 (Alfons AUSDEMWALD)*                          AUSDEMWALD Alfons (116)
 13   Payment Order            *AAW 1*                                                                                                              de
 12   Financial situation      *Budget 1 for Gerkens-Kasennova*
 11   Art61 job supplyment     *Art61 job supplyment#7 (Karl KELLER)*                KELLER Karl (178)
 10   Art61 job supplyment     *Art61 job supplyment#6 (Hedi RADERMACHER)*           RADERMACHER Hedi (161)
 9    Art61 job supplyment     *Art61 job supplyment#5 (Hedi RADERMACHER)*           RADERMACHER Hedi (161)
 8    Art61 job supplyment     *Art61 job supplyment#4 (Erna EMONTS-GAST)*           EMONTS-GAST Erna (152)
 7    Art61 job supplyment     *Art61 job supplyment#3 (Josef JONAS)*                JONAS Josef (139)
 6    Art61 job supplyment     *Art61 job supplyment#2 (Josef JONAS)*                JONAS Josef (139)
 5    Art61 job supplyment     *Art61 job supplyment#1 (Daniel EMONTS)*              EMONTS Daniel (128)
 4    Simple confirmation      *Erstattung/25/05/2014/130/1*                         FAYMONVILLE Luc (130*)                                         de
 3    Refund confirmation      *AMK/27/05/2014/139/1*                                JONAS Josef (139)                                              fr
 2    Income confirmation      *EiEi/29/09/2012/116/1*                               AUSDEMWALD Alfons (116)                                        de
 1    Simple confirmation      *Clothes bank/22/05/2014/240/19*                      FRISCH Paul (240)             Belgisches Rotes Kreuz           de
==== ======================== ===================================================== ============================= ================================ ==========
<BLANKLINE>


As for the default language of an excerpt: the recipient overrides the
owner.

The above list no longer shows well how the language of an excerpt
depends on the recipient and the client.  That would need some more
excerpts.  Excerpt 88 (the only example) is in *French* because the
recipient (BISA) speaks French and although the owner (Charlotte)
speaks *German*:

>>> print(contacts.Partner.objects.get(id=196).language)
fr
>>> print(contacts.Partner.objects.get(id=118).language)
de

