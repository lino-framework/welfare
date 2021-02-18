.. doctest docs/specs/uploads.rst
.. _welfare.specs.uploads:

=======================
Uploads in Lino Welfare
=======================

This document describes the :mod:`lino_xl.lib.uploads` plugin as used by
:ref:`welfare`.

.. currentmodule:: lino_xl.lib.uploads

.. contents::
   :depth: 2

.. include:: /../docs/shared/include/tested.rst

>>> import lino
>>> lino.startup('lino_welfare.projects.gerd.settings.doctests')
>>> from lino.api.doctest import *

Lino Welfare uses the :mod:`lino_xl.lib.uploads` plugin together with the
:mod:`lino_xl.lib.coachings` plugin, which changes some aspects.


.. A few things that should pass, otherwise don't expect the remaining
   tests to pass:

    >>> print(settings.SETTINGS_MODULE)
    lino_welfare.projects.gerd.settings.doctests
    >>> dd.today()
    datetime.date(2014, 5, 22)

    >>> print(dd.plugins.uploads)
    lino_xl.lib.uploads (extends_models=['UploadType', 'Upload'])

.. Some of the following tests rely on the right value for the
   contenttype id of `pcsw.Client` model. If the following line
   changes, subsequent snippets need to get adapted:

    >>> contenttypes.ContentType.objects.get_for_model(pcsw.Client).id #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE -REPORT_UDIFF +SKIP
    5...

Configuring upload types
========================

This is the list of upload types:

>>> rt.login('rolf').show(uploads.UploadTypes)
==== ============================ ======== ================ ============= ========================= ====================== ============================
 ID   Bezeichnung                  Wanted   Upload-Bereich   Max. number   Ablaufwarnung (Einheit)   Ablaufwarnung (Wert)   Upload shortcut
---- ---------------------------- -------- ---------------- ------------- ------------------------- ---------------------- ----------------------------
 3    Arbeitserlaubnis             Ja       Allgemein        1             monatlich                 2
 2    Aufenthaltserlaubnis         Ja       Allgemein        1             monatlich                 2
 8    Behindertenausweis           Nein     Allgemein        -1                                      1
 9    Diplom                       Ja       Allgemein        -1                                      1
 4    Führerschein                 Ja       Allgemein        1             monatlich                 1
 5    Identifizierendes Dokument   Ja       Allgemein        1             monatlich                 1                      Identifizierendes Dokument
 10   Personalausweis              Nein     Allgemein        -1                                      1
 1    Source document              Ja       Allgemein        1             monatlich                 2
 6    Vertrag                      Nein     Allgemein        -1                                      1
 7    Ärztliche Bescheinigung      Nein     Allgemein        -1                                      1
                                                             **0**                                   **13**
==== ============================ ======== ================ ============= ========================= ====================== ============================
<BLANKLINE>



Two clients and their uploads
=============================

The following newcomer has uploaded 2 identifying documents. One of
these is no longer valid, and we know it: `needed` has been unchecked.
The other is still valid but will expire in 3 days.

>>> newcomer = pcsw.Client.objects.get(pk=121)
>>> print(newcomer)
DERICUM Daniel (121)

The UploadsByProject summary shows a summary grouped by upload type.

>>> rt.show(uploads.UploadsByProject, newcomer)
Identifizierendes Dokument: *12*, *11* / Diplom: *9* / Personalausweis: *10* / `🖿 <javascript:Lino.pcsw.Clients.show_uploads(null,false,121,{  })>`__


>>> rt.show(uploads.UploadsByProject, newcomer, nosummary=True)
============================ ============ ======= ============================ ===================
 Upload-Art                   Gültig bis   Nötig   Beschreibung                 Hochgeladen durch
---------------------------- ------------ ------- ---------------------------- -------------------
 Identifizierendes Dokument   25.05.14     Ja      Identifizierendes Dokument   Theresia Thelen
 Identifizierendes Dokument   22.04.14     Nein    Identifizierendes Dokument   Theresia Thelen
 Personalausweis              26.06.15     Nein    Personalausweis              Hubert Huppertz
 Diplom                       26.06.15     Nein    Diplom                       Hubert Huppertz
============================ ============ ======= ============================ ===================
<BLANKLINE>

Here is another client with three uploads:

>>> oldclient = pcsw.Client.objects.get(pk=124)
>>> print(str(oldclient))
DOBBELSTEIN Dorothée (124)

>>> rt.show(uploads.UploadsByProject, oldclient)
Aufenthaltserlaubnis: *13* / Arbeitserlaubnis: *14* / Führerschein: *15* / `🖿 <javascript:Lino.pcsw.Clients.show_uploads(null,false,124,{  })>`__


>>> rt.show(uploads.UploadsByProject, oldclient, nosummary=True)
====================== ============ ======= ====================== ===================
 Upload-Art             Gültig bis   Nötig   Beschreibung           Hochgeladen durch
---------------------- ------------ ------- ---------------------- -------------------
 Führerschein           01.06.14     Ja      Führerschein           Caroline Carnol
 Arbeitserlaubnis       30.08.14     Ja      Arbeitserlaubnis       Alicia Allmanns
 Aufenthaltserlaubnis   18.03.15     Ja      Aufenthaltserlaubnis   Theresia Thelen
====================== ============ ======= ====================== ===================
<BLANKLINE>


My uploads
==========

Most users can open two tables which show "their" uploads.

>>> print(str(uploads.MyUploads.label))
Meine Upload-Dateien

>>> print(str(uploads.MyExpiringUploads.label))
Meine ablaufenden Upload-Dateien


This is the :class:`MyUploads` table for Theresia:

>>> rt.login('theresia').show(uploads.MyUploads)
==== ============================ ============================ ============ ============ ======= ============================ =======
 ID   Klient                       Upload-Art                   Gültig von   Gültig bis   Nötig   Beschreibung                 Datei
---- ---------------------------- ---------------------------- ------------ ------------ ------- ---------------------------- -------
 13   DOBBELSTEIN Dorothée (124)   Aufenthaltserlaubnis                      18.03.15     Ja      Aufenthaltserlaubnis
 12   DERICUM Daniel (121)         Identifizierendes Dokument                25.05.14     Ja      Identifizierendes Dokument
 11   DERICUM Daniel (121)         Identifizierendes Dokument                22.04.14     Nein    Identifizierendes Dokument
==== ============================ ============================ ============ ============ ======= ============================ =======
<BLANKLINE>


And the same for Caroline:

>>> rt.login('caroline').show(uploads.MyUploads)
==== ============================ ============== ============ ============ ======= ============== =======
 ID   Klient                       Upload-Art     Gültig von   Gültig bis   Nötig   Beschreibung   Datei
---- ---------------------------- -------------- ------------ ------------ ------- -------------- -------
 15   DOBBELSTEIN Dorothée (124)   Führerschein                01.06.14     Ja      Führerschein
==== ============================ ============== ============ ============ ======= ============== =======
<BLANKLINE>


This is the :class:`MyExpiringUploads` table for :ref:`hubert`:

>>> rt.login('hubert').show(uploads.MyExpiringUploads)
========================= ====================== ====================== =================== ============ ============ =======
 Klient                    Upload-Art             Beschreibung           Hochgeladen durch   Gültig von   Gültig bis   Nötig
------------------------- ---------------------- ---------------------- ------------------- ------------ ------------ -------
 AUSDEMWALD Alfons (116)   Source document        Source document        Hubert Huppertz                  17.05.15     Ja
 AUSDEMWALD Alfons (116)   Aufenthaltserlaubnis   Aufenthaltserlaubnis   Hubert Huppertz                  17.05.15     Ja
========================= ====================== ====================== =================== ============ ============ =======
<BLANKLINE>

:ref:`theresia` does not coach anybody, so the :class:`MyExpiringUploads`
table is empty for her:

>>> rt.login('theresia').show(uploads.MyExpiringUploads)
Keine Daten anzuzeigen



Shortcut fields
===============


>>> id_document = uploads.UploadType.objects.get(shortcut=uploads.Shortcuts.id_document)
>>> rt.show(uploads.UploadsByType, id_document)
=================== ========================= ============================ ======= ============ ============ ======= ============================
 Hochgeladen durch   Klient                    Upload-Art                   Datei   Gültig von   Gültig bis   Nötig   Beschreibung
------------------- ------------------------- ---------------------------- ------- ------------ ------------ ------- ----------------------------
 Theresia Thelen     DERICUM Daniel (121)      Identifizierendes Dokument                        25.05.14     Ja      Identifizierendes Dokument
 Theresia Thelen     DERICUM Daniel (121)      Identifizierendes Dokument                        22.04.14     Nein    Identifizierendes Dokument
 Hubert Huppertz     COLLARD Charlotte (118)   Identifizierendes Dokument                        06.06.15     Ja      Identifizierendes Dokument
=================== ========================= ============================ ======= ============ ============ ======= ============================
<BLANKLINE>

Let's have a closer look at the `id_document` shortcut field for
some customers.

The response to this AJAX request is in JSON, and we want to inspect
the `id_document` field using `BeautifulSoup
<http://www.crummy.com/software/BeautifulSoup/bs4/doc/>`_:

>>> uri = "pcsw/Clients/{0}".format(newcomer.pk)
>>> soup = get_json_soup('romain', uri, 'id_document')

This is an upload shortcut field whose target has more than one
row. Which means that it has two buttons.

>>> div = soup.div
>>> len(div.contents)
3

The first button opens a detail window on the *last* uploaded filed:

>>> div.contents[0]
<a href='javascript:Lino.uploads.Uploads.detail.run(null,{ "record_id": 12 })'>Letzte</a>

The second item is just the comma which separates the two buttons:

>>> div.contents[1]
', '

The second button opens the list of uploads:

>>> div.contents[2]  #doctest: +ELLIPSIS
<a href='javascript:Lino.uploads.UploadsByProject.grid.run(null,...)'...>Alle 2 Dateien</a>

And as you can see, it does not use the default table
(UploadsByController) but the welfare specific table UploadsByProject.

Let's inspect these three dots (`...`) of this second button.

>>> btn = div.contents[2]
>>> dots = btn['href'][55:-1]
>>> print(dots)  #doctest: +ELLIPSIS
{ ... }

They are a big "object", which is represented in Python as a `dict`:

>>> d = AttrDict(json.loads(dots))

It has 3 keys:

>>> keys = list(d.keys())
>>> keys.sort()
>>> print(json.dumps(keys))
["base_params", "param_values", "record_id"]

>>> d.record_id
12
>>> d.base_params #doctest: +ELLIPSIS
{'mk': 121, 'mt': 56, 'type': 5}

>>> pprint(d.param_values)
... #doctest: +NORMALIZE_WHITESPACE +IGNORE_EXCEPTION_DETAIL
{'coached_by': None,
 'coached_byHidden': None,
 'end_date': None,
 'observed_event': 'Est active',
 'observed_eventHidden': '20',
 'start_date': None,
 'upload_type': None,
 'upload_typeHidden': None,
 'user': None,
 'userHidden': None}


Uploads by client
=================

:class:`UploadsByProject
<lino_welfare.modlib.uploads.UploadsByProject>` shows all the
uploads of a given client, but it has a customized
:meth:`get_slave_summary <lino.core.actors.Actor.get_slave_summary>`.

The following example is going to use client #121 as master.

>>> obj = oldclient

Here we use :func:`lino.api.doctest.get_json_soup` to inspect what the
summary view of `UploadsByProject` returns for this client.

>>> soup = get_json_soup('rolf', 'pcsw/Clients/124', 'uploads_UploadsByProject')
>>> print(soup.get_text())
... #doctest: +NORMALIZE_WHITESPACE
Source document: Aufenthaltserlaubnis: 13Arbeitserlaubnis: 14Führerschein: 15Identifizierendes Dokument: Diplom:

The HTML fragment contains five links:

>>> links = soup.find_all('a')
>>> len(links)
6


The first link would run the insert action on `UploadsByProject`, with
the owner set to this client

>>> btn = links[0]
>>> print(btn.string)
None
>>> print(btn.img['src'])
/static/images/mjames/add.png

>>> print(btn)
... #doctest: +NORMALIZE_WHITESPACE +ELLIPSIS
<a href='javascript:Lino.uploads.UploadsByProject.insert.run(null,{ ... })'
style="vertical-align:-30%;"
title="Öffnet ein Dialogfenster, um einen neuen Datensatz (Upload-Datei) zu erstellen."><img alt="add"
src="/static/images/mjames/add.png"/></a>

>>> print(links[2].get('href'))
... #doctest: +NORMALIZE_WHITESPACE +ELLIPSIS
javascript:Lino.uploads.Uploads.detail.run(null,{ "record_id": 14 })

>>> print(links[3].get('href'))
... #doctest: +NORMALIZE_WHITESPACE +ELLIPSIS
javascript:Lino.uploads.Uploads.detail.run(null,{ "record_id": 15 })


Now let's inspect the javascript of the first button

>>> dots = btn['href'][57:-1]
>>> print(dots)  #doctest: +ELLIPSIS
{ ... }

>>> d = AttrDict(json.loads(dots))

>>> pprint(d)
{'base_params': {'mk': 124, 'mt': 56, 'type_id': 1},
 'data_record': {'data': {'description': '',
                          'disabled_fields': {'file_size': True,
                                              'mimetype': True},
                          'end_date': None,
                          'file': '',
                          'needed': True,
                          'type': 'Source document',
                          'typeHidden': 1},
                 'phantom': True,
                 'title': 'Upload-Datei erstellen'},
 'param_values': {'coached_by': None,
                  'coached_byHidden': None,
                  'end_date': None,
                  'observed_event': 'Ist aktiv',
                  'observed_eventHidden': '20',
                  'start_date': None,
                  'upload_type': None,
                  'upload_typeHidden': None,
                  'user': None,
                  'userHidden': None},
 'record_id': None}
