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

Here is the list of all demo excerpts. 

>>> rt.show(excerpts.Excerpts, language="en", column_names="id excerpt_type owner project company language")
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
==== ======================== ================================================ ========================= ========================== ==========
 ID   Excerpt Type             Controlled by                                    Client                    Recipient (Organization)   Language
---- ------------------------ ------------------------------------------------ ------------------------- -------------------------- ----------
 1    Simple confirmation      *Clothes bank/5/22/14/238/19*                    FRISCH Paul (238)         Belgisches Rotes Kreuz     de
 2    Income confirmation      *EiEi/9/29/12/116/1*                             AUSDEMWALD Alfons (116)                              de
 3    Refund confirmation      *AMK/5/27/14/139/1*                              JONAS Josef (139)                                    fr
 4    Finanzielle Situation    *Budget 1 for Gerkens-Kasennova*
 5    Art61 job supplyment     *Art61 job supplyment#1 (Daniel EMONTS)*         EMONTS Daniel (128)
 6    Art60§7 job supplyment   *Art60§7 job supplyment#1 (Charlotte COLLARD)*   COLLARD Charlotte (118)   BISA                       fr
 7    ISIP                     *ISIP#1 (Alfons AUSDEMWALD)*                     AUSDEMWALD Alfons (116)
 8    Presence certificate     *Participant #1 (22.05.2014)*                    AUSDEMWALD Alfons (116)                              de
 9    Curriculum vitae         *AUSDEMWALD Alfons (116)*                        AUSDEMWALD Alfons (116)                              de
 10   File sheet               *AUSDEMWALD Alfons (116)*                        AUSDEMWALD Alfons (116)                              de
 11   eID sheet                *AUSDEMWALD Alfons (116)*                        AUSDEMWALD Alfons (116)                              de
 12   Action plan              *AUSDEMWALD Alfons (116)*                        AUSDEMWALD Alfons (116)                              de
 13   Art60§7 job supplyment   *Art60§7 job supplyment#6 (Hildegard HILGERS)*   HILGERS Hildegard (133)   Pro Aktiv V.o.G.           de
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
