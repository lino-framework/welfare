.. _welfare.tested.excerpts:

=============
Excerpts
=============

.. How to test only this document:

    $ python setup.py test -s tests.SpecsTests.test_excerpts
    
    doctest init:

    >>> from __future__ import print_function
    >>> import os
    >>> os.environ['DJANGO_SETTINGS_MODULE'] = \
    ...    'lino_welfare.projects.eupen.settings.doctests'
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
======================================================= ======== =============== =========================== ====================== ================= ================================
 Modell                                                  Primär   Bescheinigend   Bezeichnung                 Konstruktionsmethode   Vorlage           Textkörper-Vorlage
------------------------------------------------------- -------- --------------- --------------------------- ---------------------- ----------------- --------------------------------
 *aids.IncomeConfirmation (Einkommensbescheinigung)*     Ja       Ja              Einkommensbescheinigung                            Default.odt       certificate.body.html
 *aids.RefundConfirmation (Kostenübernahmeschein)*       Ja       Ja              Kostenübernahmeschein                              Default.odt       certificate.body.html
 *aids.SimpleConfirmation (Einfache Bescheinigung)*      Ja       Ja              Einfache Bescheinigung                             Default.odt       certificate.body.html
 *art61.Contract (Art.61-Konvention)*                    Ja       Ja              Art.61-Konvention                                                    contract.body.html
 *cal.Guest (Teilnehmer)*                                Ja       Nein            Anwesenheitsbescheinigung                          Default.odt       presence_certificate.body.html
 *cbss.IdentifyPersonRequest (IdentifyPerson-Anfrage)*   Ja       Ja              IdentifyPerson-Anfrage
 *cbss.ManageAccessRequest (ManageAccess-Anfrage)*       Ja       Ja              ManageAccess-Anfrage
 *cbss.RetrieveTIGroupsRequest (Tx25-Anfrage)*           Ja       Ja              Tx25-Anfrage
 *debts.Budget (Budget)*                                 Ja       Ja              Finanzielle Situation
 *isip.Contract (VSE)*                                   Ja       Ja              VSE
 *jobs.Contract (Art.60§7-Konvention)*                   Ja       Ja              Art.60§7-Konvention
 *pcsw.Client (Klient)*                                  Ja       Nein            Aktenblatt                                         file_sheet.odt
 *pcsw.Client (Klient)*                                  Nein     Nein            Aktionsplan                                        Default.odt       pac.body.html
 *pcsw.Client (Klient)*                                  Nein     Nein            Curriculum vitae            AppyRtfBuildMethod     cv.odt
 *pcsw.Client (Klient)*                                  Nein     Nein            eID-Inhalt                                         eid-content.odt
 **Total (15 Zeilen)**                                   **12**   **10**
======================================================= ======== =============== =========================== ====================== ================= ================================
<BLANKLINE>



Demo excerpts
=============

Here is the list of all demo excerpts. 

>>> rt.show(excerpts.AllExcerpts, language="en", column_names="id excerpt_type owner project company language")
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE -REPORT_UDIFF
==== ======================== ================================================ ========================= ========================== ==========
 ID   Excerpt Type             Controlled by                                    Client                    Recipient (Organization)   Language
---- ------------------------ ------------------------------------------------ ------------------------- -------------------------- ----------
 12   Action plan              *AUSDEMWALD Alfons (116)*                        AUSDEMWALD Alfons (116)                              de
 11   eID sheet                *AUSDEMWALD Alfons (116)*                        AUSDEMWALD Alfons (116)                              de
 10   File sheet               *AUSDEMWALD Alfons (116)*                        AUSDEMWALD Alfons (116)                              de
 9    Curriculum vitae         *AUSDEMWALD Alfons (116)*                        AUSDEMWALD Alfons (116)                              de
 8    Presence certificate     *Participant #1 (22.05.2014)*                    AUSDEMWALD Alfons (116)                              de
 7    ISIP                     *ISIP#1 (Alfons AUSDEMWALD)*                     AUSDEMWALD Alfons (116)
 6    Art60§7 job supplyment   *Art60§7 job supplyment#1 (Charlotte COLLARD)*   COLLARD Charlotte (118)   BISA                       fr
 5    Art61 job supplyment     *Art61 job supplyment#1 (Daniel EMONTS)*         EMONTS Daniel (128)
 4    Finanzielle Situation    *Budget 1 for Gerkens-Kasennova*
 3    Refund confirmation      *AMK/5/27/14/139/1*                              JONAS Josef (139)                                    fr
 2    Income confirmation      *EiEi/9/29/12/116/1*                             AUSDEMWALD Alfons (116)                              de
 1    Simple confirmation      *Clothes bank/5/22/14/238/19*                    FRISCH Paul (238)         Belgisches Rotes Kreuz     de
==== ======================== ================================================ ========================= ========================== ==========
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
