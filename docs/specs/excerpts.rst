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
 76   Action plan              *AUSDEMWALD Alfons (116)*                             AUSDEMWALD Alfons (116)                                        de
 75   eID sheet                *AUSDEMWALD Alfons (116)*                             AUSDEMWALD Alfons (116)                                        de
 74   File sheet               *AUSDEMWALD Alfons (116)*                             AUSDEMWALD Alfons (116)                                        de
 73   Curriculum vitae         *AUSDEMWALD Alfons (116)*                             AUSDEMWALD Alfons (116)                                        de
 72   Presence certificate     *Presence #1 (22.05.2014)*                            AUSDEMWALD Alfons (116)                                        de
 71   Payment reminder         *Belgisches Rotes Kreuz*                                                                                             de
 70   Art60§7 job supplyment   *Art60§7 job supplyment#16 (Denis DENON)*             DENON Denis (180*)            R-Cycle Sperrgutsortierzentrum   de
 69   Art60§7 job supplyment   *Art60§7 job supplyment#15 (Denis DENON)*             DENON Denis (180*)            BISA                             de
 ...
 56   Art60§7 job supplyment   *Art60§7 job supplyment#2 (Bernd EVERTZ)*             EVERTZ Bernd (126)            R-Cycle Sperrgutsortierzentrum   de
 55   Art60§7 job supplyment   *Art60§7 job supplyment#1 (Charlotte COLLARD)*        COLLARD Charlotte (118)       BISA                             de
 54   ISIP                     *ISIP#33 (Jérôme JEANÉMART)*                          JEANÉMART Jérôme (181)                                         de
 53   ISIP                     *ISIP#32 (Jérôme JEANÉMART)*                          JEANÉMART Jérôme (181)                                         de
 ...
 23   ISIP                     *ISIP#2 (Alfons AUSDEMWALD)*                          AUSDEMWALD Alfons (116)                                        de
 22   ISIP                     *ISIP#1 (Alfons AUSDEMWALD)*                          AUSDEMWALD Alfons (116)                                        de
 21   Payment Order            *AAW 1/2014*                                                                                                         de
 20   Financial situation      *Budget 1 for Gerd & Tatjana Gerkens-Kasennova*                                                                      de
 19   Art61 job supplyment     *Art61 job supplyment#7 (Karl KELLER)*                KELLER Karl (178)                                              de
 ...
 13   Art61 job supplyment     *Art61 job supplyment#1 (Daniel EMONTS)*              EMONTS Daniel (128)                                            de
 12   Terms & conditions       *Mr Albert ADAM*                                                                                                     de
 11   Simple confirmation      *Clothes bank/22/05/2014/240/19*                      FRISCH Paul (240)             Belgisches Rotes Kreuz           de
 10   Simple confirmation      *Clothes bank/01/06/2014/159/16*                      RADERMACHER Guido (159)                                        de
 9    Simple confirmation      *Food bank/31/05/2014/155/13*                         RADERMACHER Christian (155)                                    en
 8    Simple confirmation      *Heating costs/30/05/2014/152/10*                     EMONTS-GAST Erna (152)                                         fr
 7    Simple confirmation      *Furniture/29/05/2014/146/7*                          MALMENDIER Marc (146)                                          de
 6    Refund confirmation      *DMH/28/05/2014/142/7*                                LAMBERTZ Guido (142)                                           de
 5    Refund confirmation      *AMK/27/05/2014/139/1*                                JONAS Josef (139)                                              fr
 4    Simple confirmation      *Erstattung/25/05/2014/130/1*                         FAYMONVILLE Luc (130*)                                         de
 3    Income confirmation      *Feste Beihilfe/24/05/2014/128/56*                    EMONTS Daniel (128)                                            de
 2    Income confirmation      *Ausländerbeihilfe/08/08/2013/116/2*                  AUSDEMWALD Alfons (116)                                        de
 1    Income confirmation      *EiEi/29/09/2012/116/1*                               AUSDEMWALD Alfons (116)                                        de
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

This template should be customized locally to contain the :term:`site
operator`'s layout.


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
