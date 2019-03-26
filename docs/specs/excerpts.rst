.. doctest docs/specs/excerpts.rst
.. _welfare.specs.excerpts:

==========================================
Usage of database excerpts in Lino Welfare
==========================================

.. doctest init:

    >>> import lino
    >>> lino.startup('lino_welfare.projects.gerd.settings.doctests')
    >>> from lino.api.doctest import *


.. contents::
   :local:
   :depth: 2


Configuring excerpts
====================

See also :ref:`lino.admin.printing`.

Here is a more complete list of excerpt types:

>>> rt.show(excerpts.ExcerptTypes)
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
======================================================= ======== =============== =========================== ===================== ============================= ================================
 Modell                                                  Primär   Bescheinigend   Bezeichnung                 Druckmethode          Vorlage                       Textkörper-Vorlage
------------------------------------------------------- -------- --------------- --------------------------- --------------------- ----------------------------- --------------------------------
 *aids.IncomeConfirmation (Einkommensbescheinigung)*     Ja       Ja              Einkommensbescheinigung                           Default.odt                   certificate.body.html
 *aids.RefundConfirmation (Kostenübernahmeschein)*       Ja       Ja              Kostenübernahmeschein                             Default.odt                   certificate.body.html
 *aids.SimpleConfirmation (Einfache Bescheinigung)*      Ja       Ja              Einfache Bescheinigung                            Default.odt                   certificate.body.html
 *art61.Contract (Art.61-Konvention)*                    Ja       Ja              Art.61-Konvention                                                               contract.body.html
 *cal.Guest (Anwesenheit)*                               Ja       Nein            Anwesenheitsbescheinigung                         Default.odt                   presence_certificate.body.html
 *cbss.IdentifyPersonRequest (IdentifyPerson-Anfrage)*   Ja       Ja              IdentifyPerson-Anfrage
 *cbss.ManageAccessRequest (ManageAccess-Anfrage)*       Ja       Ja              ManageAccess-Anfrage
 *cbss.RetrieveTIGroupsRequest (Tx25-Anfrage)*           Ja       Ja              Tx25-Anfrage
 *contacts.Partner (Partner)*                            Nein     Nein            Zahlungserinnerung          WeasyPdfBuildMethod   payment_reminder.weasy.html
 *contacts.Person (Person)*                              Nein     Nein            Nutzungsbestimmungen        AppyPdfBuildMethod    TermsConditions.odt
 *debts.Budget (Budget)*                                 Ja       Ja              Finanzielle Situation
 *esf.ClientSummary (ESF Summary)*                       Ja       Ja              Training report             WeasyPdfBuildMethod
 *finan.BankStatement (Kontoauszug)*                     Ja       Ja              Kontoauszug
 *finan.JournalEntry (Diverse Buchung)*                  Ja       Ja              Diverse Buchung
 *finan.PaymentOrder (Zahlungsauftrag)*                  Ja       Ja              Zahlungsauftrag
 *isip.Contract (VSE)*                                   Ja       Ja              VSE
 *jobs.Contract (Art.60§7-Konvention)*                   Ja       Ja              Art.60§7-Konvention
 *pcsw.Client (Klient)*                                  Ja       Nein            Aktenblatt                                        file_sheet.odt
 *pcsw.Client (Klient)*                                  Nein     Nein            Aktionsplan                                       Default.odt                   pac.body.html
 *pcsw.Client (Klient)*                                  Nein     Nein            Curriculum vitae            AppyRtfBuildMethod    cv.odt
 *pcsw.Client (Klient)*                                  Nein     Nein            eID-Inhalt                                        eid-content.odt
======================================================= ======== =============== =========================== ===================== ============================= ================================
<BLANKLINE>


Demo excerpts
=============

Here is a list of all demo excerpts. 

>>> rt.show(excerpts.AllExcerpts, language="en", column_names="id excerpt_type owner project company language")
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
==== ======================== ===================================================== ============================= ================================ ==========
 ID   Excerpt Type             Controlled by                                         Client                        Recipient (Organization)         Language
---- ------------------------ ----------------------------------------------------- ----------------------------- -------------------------------- ----------
 69   Action plan              *AUSDEMWALD Alfons (116)*                             AUSDEMWALD Alfons (116)                                        de
 68   eID sheet                *AUSDEMWALD Alfons (116)*                             AUSDEMWALD Alfons (116)                                        de
 67   File sheet               *AUSDEMWALD Alfons (116)*                             AUSDEMWALD Alfons (116)                                        de
 66   Curriculum vitae         *AUSDEMWALD Alfons (116)*                             AUSDEMWALD Alfons (116)                                        de
 65   Presence certificate     *Presence #1 (22.05.2014)*                            AUSDEMWALD Alfons (116)                                        de
 64   Payment reminder         *Belgisches Rotes Kreuz*                                                                                             de
 63   Art60§7 job supplyment   *Art60§7 job supplyment#16 (Denis DENON)*             DENON Denis (180*)            R-Cycle Sperrgutsortierzentrum   de
 62   Art60§7 job supplyment   *Art60§7 job supplyment#15 (Denis DENON)*             DENON Denis (180*)            BISA                             de
 61   Art60§7 job supplyment   *Art60§7 job supplyment#14 (Rik RADERMECKER)*         RADERMECKER Rik (173)         BISA                             de
 60   Art60§7 job supplyment   *Art60§7 job supplyment#13 (Rik RADERMECKER)*         RADERMECKER Rik (173)         Pro Aktiv V.o.G.                 de
 59   Art60§7 job supplyment   *Art60§7 job supplyment#12 (Vincent VAN VEEN)*        VAN VEEN Vincent (166)        Pro Aktiv V.o.G.                 de
 58   Art60§7 job supplyment   *Art60§7 job supplyment#11 (Fritz RADERMACHER)*       RADERMACHER Fritz (158)       R-Cycle Sperrgutsortierzentrum   de
 57   Art60§7 job supplyment   *Art60§7 job supplyment#10 (Christian RADERMACHER)*   RADERMACHER Christian (155)   R-Cycle Sperrgutsortierzentrum   de
 56   Art60§7 job supplyment   *Art60§7 job supplyment#9 (Christian RADERMACHER)*    RADERMACHER Christian (155)   BISA                             de
 55   Art60§7 job supplyment   *Art60§7 job supplyment#8 (Marc MALMENDIER)*          MALMENDIER Marc (146)         R-Cycle Sperrgutsortierzentrum   de
 54   Art60§7 job supplyment   *Art60§7 job supplyment#7 (Marc MALMENDIER)*          MALMENDIER Marc (146)         BISA                             de
 53   Art60§7 job supplyment   *Art60§7 job supplyment#6 (Guido LAMBERTZ)*           LAMBERTZ Guido (142)          BISA                             de
 52   Art60§7 job supplyment   *Art60§7 job supplyment#5 (Hildegard HILGERS)*        HILGERS Hildegard (133)       Pro Aktiv V.o.G.                 de
 51   Art60§7 job supplyment   *Art60§7 job supplyment#4 (Luc FAYMONVILLE)*          FAYMONVILLE Luc (130*)        Pro Aktiv V.o.G.                 de
 50   Art60§7 job supplyment   *Art60§7 job supplyment#3 (Luc FAYMONVILLE)*          FAYMONVILLE Luc (130*)        R-Cycle Sperrgutsortierzentrum   de
 49   Art60§7 job supplyment   *Art60§7 job supplyment#2 (Bernd EVERTZ)*             EVERTZ Bernd (126)            R-Cycle Sperrgutsortierzentrum   de
 48   Art60§7 job supplyment   *Art60§7 job supplyment#1 (Charlotte COLLARD)*        COLLARD Charlotte (118)       BISA                             de
 47   ISIP                     *ISIP#33 (Jérôme JEANÉMART)*                          JEANÉMART Jérôme (181)                                         de
 46   ISIP                     *ISIP#32 (Jérôme JEANÉMART)*                          JEANÉMART Jérôme (181)                                         de
 45   ISIP                     *ISIP#31 (Robin DUBOIS)*                              DUBOIS Robin (179)                                             de
 44   ISIP                     *ISIP#30 (Robin DUBOIS)*                              DUBOIS Robin (179)                                             de
 43   ISIP                     *ISIP#29 (Robin DUBOIS)*                              DUBOIS Robin (179)                                             de
 42   ISIP                     *ISIP#28 (Bernd BRECHT)*                              BRECHT Bernd (177)                                             de
 41   ISIP                     *ISIP#27 (Bernd BRECHT)*                              BRECHT Bernd (177)                                             de
 40   ISIP                     *ISIP#26 (Otto ÖSTGES)*                               ÖSTGES Otto (168)                                              de
 39   ISIP                     *ISIP#25 (Otto ÖSTGES)*                               ÖSTGES Otto (168)                                              de
 38   ISIP                     *ISIP#24 (Otto ÖSTGES)*                               ÖSTGES Otto (168)                                              de
 37   ISIP                     *ISIP#23 (David DA VINCI)*                            DA VINCI David (165)                                           de
 36   ISIP                     *ISIP#22 (David DA VINCI)*                            DA VINCI David (165)                                           de
 35   ISIP                     *ISIP#21 (Guido RADERMACHER)*                         RADERMACHER Guido (159)                                        de
 34   ISIP                     *ISIP#20 (Guido RADERMACHER)*                         RADERMACHER Guido (159)                                        de
 33   ISIP                     *ISIP#19 (Guido RADERMACHER)*                         RADERMACHER Guido (159)                                        de
 32   ISIP                     *ISIP#18 (Edgard RADERMACHER)*                        RADERMACHER Edgard (157)                                       de
 31   ISIP                     *ISIP#17 (Alfons RADERMACHER)*                        RADERMACHER Alfons (153)                                       de
 30   ISIP                     *ISIP#16 (Melissa MEESSEN)*                           MEESSEN Melissa (147)                                          de
 29   ISIP                     *ISIP#15 (Melissa MEESSEN)*                           MEESSEN Melissa (147)                                          de
 28   ISIP                     *ISIP#14 (Melissa MEESSEN)*                           MEESSEN Melissa (147)                                          de
 27   ISIP                     *ISIP#13 (Line LAZARUS)*                              LAZARUS Line (144)                                             de
 26   ISIP                     *ISIP#12 (Line LAZARUS)*                              LAZARUS Line (144)                                             de
 25   ISIP                     *ISIP#11 (Karl KAIVERS)*                              KAIVERS Karl (141)                                             de
 24   ISIP                     *ISIP#10 (Jacqueline JACOBS)*                         JACOBS Jacqueline (137)                                        de
 23   ISIP                     *ISIP#9 (Gregory GROTECLAES)*                         GROTECLAES Gregory (132)                                       de
 22   ISIP                     *ISIP#8 (Edgar ENGELS)*                               ENGELS Edgar (129)                                             de
 21   ISIP                     *ISIP#7 (Edgar ENGELS)*                               ENGELS Edgar (129)                                             de
 20   ISIP                     *ISIP#6 (Eberhart EVERS)*                             EVERS Eberhart (127)                                           de
 19   ISIP                     *ISIP#5 (Eberhart EVERS)*                             EVERS Eberhart (127)                                           de
 18   ISIP                     *ISIP#4 (Eberhart EVERS)*                             EVERS Eberhart (127)                                           de
 17   ISIP                     *ISIP#3 (Dorothée DOBBELSTEIN)*                       DOBBELSTEIN Dorothée (124)                                     de
 16   ISIP                     *ISIP#2 (Alfons AUSDEMWALD)*                          AUSDEMWALD Alfons (116)                                        de
 15   ISIP                     *ISIP#1 (Alfons AUSDEMWALD)*                          AUSDEMWALD Alfons (116)                                        de
 14   Payment Order            *AAW 1/2014*                                                                                                         de
 13   Financial situation      *Budget 1 for Gerd & Tatjana Gerkens-Kasennova*                                                                      de
 12   Art61 job supplyment     *Art61 job supplyment#7 (Karl KELLER)*                KELLER Karl (178)                                              de
 11   Art61 job supplyment     *Art61 job supplyment#6 (Hedi RADERMACHER)*           RADERMACHER Hedi (161)                                         de
 10   Art61 job supplyment     *Art61 job supplyment#5 (Hedi RADERMACHER)*           RADERMACHER Hedi (161)                                         de
 9    Art61 job supplyment     *Art61 job supplyment#4 (Erna EMONTS-GAST)*           EMONTS-GAST Erna (152)                                         de
 8    Art61 job supplyment     *Art61 job supplyment#3 (Josef JONAS)*                JONAS Josef (139)                                              de
 7    Art61 job supplyment     *Art61 job supplyment#2 (Josef JONAS)*                JONAS Josef (139)                                              de
 6    Art61 job supplyment     *Art61 job supplyment#1 (Daniel EMONTS)*              EMONTS Daniel (128)                                            de
 5    Simple confirmation      *Erstattung/25/05/2014/130/1*                         FAYMONVILLE Luc (130*)                                         de
 4    Refund confirmation      *AMK/27/05/2014/139/1*                                JONAS Josef (139)                                              fr
 3    Income confirmation      *EiEi/29/09/2012/116/1*                               AUSDEMWALD Alfons (116)                                        de
 2    Terms & conditions       *Mr Albert ADAM*                                                                                                     de
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


The default template for excerpts
==================================

.. xfile:: excerpts/Default.odt

This template should be customized locally to contain the site owner's
layout.

          
The template inserts the recipient address using this appy.pod code::

    do text
    from html(this.get_address_html(5, **{'class':"Recipient"})

This code is inserted as a command in some paragraph whose content in
the template can be anything since it will be replaced by the computed
text.

>>> obj = aids.SimpleConfirmation.objects.get(pk=19)
>>> print(obj.get_address_html(5, **{'class':"Recipient"}))
<p class="Recipient">Belgisches Rotes Kreuz<br/>Hillstraße 1<br/>4700 Eupen<br/><br/></p>

That paragraph should also contain another comment::

    do text if this.excerpt_type.print_recipient
    
There should of course be a paragraph style "Recipient" with proper
margins and spacing set.

