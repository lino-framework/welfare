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
======================================================= ======== =============== =========================== ====================== ================= ================================
 Modell                                                  Primär   Bescheinigend   Bezeichnung                 Konstruktionsmethode   Vorlage           Textkörper-Vorlage
------------------------------------------------------- -------- --------------- --------------------------- ---------------------- ----------------- --------------------------------
 **aids.IncomeConfirmation (Einkommensbescheinigung)**   Ja       Ja              Einkommensbescheinigung                            Default.odt       certificate.body.html
 **aids.RefundConfirmation (Kostenübernahmeschein)**     Ja       Ja              Kostenübernahmeschein                              Default.odt       certificate.body.html
 **aids.SimpleConfirmation (Einfache Bescheinigung)**    Ja       Ja              Einfache Bescheinigung                             Default.odt       certificate.body.html
 **cal.Guest (Teilnehmer)**                              Ja       Nein            Anwesenheitsbescheinigung                          Default.odt       presence_certificate.body.html
 **debts.Budget (Budget)**                               Ja       Ja              Finanzielle Situation                              Default.odt
 **isip.Contract (VSE)**                                 Ja       Ja              VSE                                                Default.odt
 **jobs.Contract (Art.60§7-Konvention)**                 Ja       Ja              Art.60§7-Konvention                                Default.odt
 **pcsw.Client (Klient)**                                Nein     Nein            Aktionsplan                                        Default.odt       pac.body.html
 **pcsw.Client (Klient)**                                Nein     Nein            Curriculum vitae            AppyRtfBuildMethod     cv.odt
 **pcsw.Client (Klient)**                                Ja       Nein            eID-Inhalt                                         eid-content.odt
 **Total (10 Zeilen)**                                   **8**    **6**
======================================================= ======== =============== =========================== ====================== ================= ================================
<BLANKLINE>
