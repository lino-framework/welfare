.. doctest docs/specs/uploads.rst
.. _welfare.specs.uploads:

=============
Uploads
=============

.. doctest init:
    >>> from __future__ import unicode_literals
    >>> import lino
    >>> lino.startup('lino_welfare.projects.eupen.settings.doctests')
    >>> from lino.api.doctest import *

A technical tour into the :mod:`lino_welfare.modlib.uploads` plugin.

Lino Welfare extends the standard :mod:`lino_xl.lib.uploads` plugin
into a system which helps social agents to manage certain documents
about their clients. For example, integration agents want to get a
reminder when the driving license of one of their client is going to
expire.

.. contents::
   :depth: 2

    
.. A few things that should pass, otherwise don't expect the remaining
   tests to pass:

    >>> print(settings.SETTINGS_MODULE)
    lino_welfare.projects.eupen.settings.doctests
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
 2    Arbeitserlaubnis             Ja       Allgemein        1             monatlich                 2
 1    Aufenthaltserlaubnis         Ja       Allgemein        1             monatlich                 2
 7    Behindertenausweis           Nein     Allgemein        -1                                      1
 8    Diplom                       Ja       Allgemein        -1                                      1
 3    Führerschein                 Ja       Allgemein        1             monatlich                 1
 4    Identifizierendes Dokument   Ja       Allgemein        1             monatlich                 1                      Identifizierendes Dokument
 9    Personalausweis              Nein     Allgemein        -1                                      1
 5    Vertrag                      Nein     Allgemein        -1                                      1
 6    Ärztliche Bescheinigung      Nein     Allgemein        -1                                      1
                                                             **-1**                                  **11**
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

>>> rt.show(uploads.UploadsByClient, newcomer)
Identifizierendes Dokument: *8*

>>> rt.show(uploads.UploadsByClient, newcomer, nosummary=True)
============================ ============ ======= ============================ ===================
 Upload-Art                   Gültig bis   Nötig   Beschreibung                 Hochgeladen durch
---------------------------- ------------ ------- ---------------------------- -------------------
 Identifizierendes Dokument   25.05.14     Ja      Identifizierendes Dokument   Theresia Thelen
 Identifizierendes Dokument   22.04.14     Nein    Identifizierendes Dokument   Theresia Thelen
============================ ============ ======= ============================ ===================
<BLANKLINE>

Here is another client with three uploads:

>>> oldclient = pcsw.Client.objects.get(pk=124)
>>> print(str(oldclient))
DOBBELSTEIN Dorothée (124)

>>> rt.show(uploads.UploadsByClient, oldclient)
Aufenthaltserlaubnis: *9*
<BLANKLINE>
Arbeitserlaubnis: *10*
<BLANKLINE>
Führerschein: *11*


>>> rt.show(uploads.UploadsByClient, oldclient, nosummary=True)
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
Meine Uploads

>>> print(str(uploads.MyExpiringUploads.label))
Ablaufende Uploads

This is the MyUploads table for Theresia:

>>> rt.login('theresia').show(uploads.MyUploads)
==== ============================ ============================ ============ ============ ======= ============================ =======
 ID   Klient                       Upload-Art                   Gültig von   Gültig bis   Nötig   Beschreibung                 Datei
---- ---------------------------- ---------------------------- ------------ ------------ ------- ---------------------------- -------
 9    DOBBELSTEIN Dorothée (124)   Aufenthaltserlaubnis                      18.03.15     Ja      Aufenthaltserlaubnis
 8    DERICUM Daniel (121)         Identifizierendes Dokument                25.05.14     Ja      Identifizierendes Dokument
 7    DERICUM Daniel (121)         Identifizierendes Dokument                22.04.14     Nein    Identifizierendes Dokument
==== ============================ ============================ ============ ============ ======= ============================ =======
<BLANKLINE>


And the same for Caroline:

>>> rt.login('caroline').show(uploads.MyUploads)
==== ============================ ============== ============ ============ ======= ============== =======
 ID   Klient                       Upload-Art     Gültig von   Gültig bis   Nötig   Beschreibung   Datei
---- ---------------------------- -------------- ------------ ------------ ------- -------------- -------
 11   DOBBELSTEIN Dorothée (124)   Führerschein                01.06.14     Ja      Führerschein
==== ============================ ============== ============ ============ ======= ============== =======
<BLANKLINE>


This is the MyExpiringUploads table for :ref:`hubert`:

>>> rt.login('hubert').show(uploads.MyExpiringUploads)
========================= ====================== ====================== =================== ============ ============ =======
 Klient                    Upload-Art             Beschreibung           Hochgeladen durch   Gültig von   Gültig bis   Nötig
------------------------- ---------------------- ---------------------- ------------------- ------------ ------------ -------
 AUSDEMWALD Alfons (116)   Aufenthaltserlaubnis   Aufenthaltserlaubnis   Hubert Huppertz                  17.05.15     Ja
 AUSDEMWALD Alfons (116)   Arbeitserlaubnis       Arbeitserlaubnis       Hubert Huppertz                  17.05.15     Ja
========================= ====================== ====================== =================== ============ ============ =======
<BLANKLINE>

:ref:`theresia` does not coach anybody, so the `MyExpiringUploads`
table is empty for her:

>>> rt.login('theresia').show(uploads.MyExpiringUploads)
Keine Daten anzuzeigen



Shortcut fields
===============


>>> id_document = uploads.UploadType.objects.get(shortcut=uploads.Shortcuts.id_document)
>>> rt.show(uploads.UploadsByType, id_document)
=================== ====================== ============================ ======= ============ ============ ============================
 Hochgeladen durch   Klient                 Upload-Art                   Datei   Gültig von   Gültig bis   Beschreibung
------------------- ---------------------- ---------------------------- ------- ------------ ------------ ----------------------------
 Theresia Thelen     DERICUM Daniel (121)   Identifizierendes Dokument                        25.05.14     Identifizierendes Dokument
 Theresia Thelen     DERICUM Daniel (121)   Identifizierendes Dokument                        22.04.14     Identifizierendes Dokument
 Hubert Huppertz     BRECHT Bernd (177)     Identifizierendes Dokument                        27.05.15     Identifizierendes Dokument
=================== ====================== ============================ ======= ============ ============ ============================
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
<a href='javascript:Lino.uploads.Uploads.detail.run(null,{ "record_id": 8 })'>Last</a>

The second item is just the comma which separates the two buttons:

>>> sixprint(div.contents[1]) #doctest: +IGNORE_EXCEPTION_DETAIL
', '

The second button opens the list of uploads:

>>> div.contents[2]  #doctest: +ELLIPSIS
<a href='javascript:Lino.uploads.UploadsByClient.grid.run(null,...)'...>All 2 files</a>

And as you can see, it does not use the default table
(UploadsByController) but the welfare specific table UploadsByClient.

Now let's inspect these three dots (`...`) of this second button.

>>> btn = div.contents[2]
>>> dots = btn['href'][54:-1]
>>> print(dots)  #doctest: +ELLIPSIS 
{ ... }

They are a big "object" (in Python we call it a `dict`):

>>> d = AttrDict(json.loads(dots))

It has 3 keys:

>>> keys = list(d.keys())
>>> keys.sort()
>>> print(json.dumps(keys))
["base_params", "param_values", "record_id"]

>>> d.record_id
8
>>> d.base_params['mt'] #doctest: +ELLIPSIS
5...
>>> d.base_params['type']
4
>>> d.base_params['mk']
121

>>> pprint(sixprint(json.dumps(d.param_values)))  #doctest: +NORMALIZE_WHITESPACE +IGNORE_EXCEPTION_DETAIL
'{"userHidden": null, "upload_typeHidden": null, "end_date": null, "observed_eventHidden": "20", "observed_event": "Est active", "coached_by": null, "upload_type": null, "coached_byHidden": null, "start_date": null, "user": null}'
    None


Uploads by client
=================

:class:`UploadsByClient
<lino_welfare.modlib.uploads.models.UploadsByClient>` shows all the
uploads of a given client, but it has a customized
:meth:`get_slave_summary <lino.core.actors.Actor.get_slave_summary>`.

The following example is going to use client #177 as master.

>>> obj = pcsw.Client.objects.get(pk=177)
>>> print(obj)
BRECHT Bernd (177)

Here we use :func:`lino.api.doctest.get_json_soup` to inspect what the
summary view of `UploadsByClient` returns for this client.

>>> soup = get_json_soup('rolf', 'pcsw/Clients/177', 'uploads_UploadsByClient')
>>> print(soup.get_text())
... #doctest: +NORMALIZE_WHITESPACE
Aufenthaltserlaubnis: Arbeitserlaubnis: Führerschein: 3Identifizierendes Dokument: 4Diplom:

The HTML fragment contains five links:

>>> links = soup.find_all('a')
>>> len(links)
5

The first link would run the insert action on `UploadsByClient`, with
the owner set to this client

>>> btn = links[0]
>>> print(btn.string)
None
>>> print(btn.img['src'])
/static/images/mjames/add.png

>>> print(btn)
... #doctest: +NORMALIZE_WHITESPACE +ELLIPSIS
<a href='javascript:Lino.uploads.UploadsByClient.insert.run(null,{ ... })' 
style="vertical-align:-30%;" 
title="Neuen Datensatz erstellen"><img alt="add" 
src="/static/images/mjames/add.png"/></a>

>>> print(links[2].get('href'))
... #doctest: +NORMALIZE_WHITESPACE +ELLIPSIS
javascript:Lino.uploads.Uploads.detail.run(null,{ "record_id": 3 })

>>> print(links[3].get('href'))
... #doctest: +NORMALIZE_WHITESPACE +ELLIPSIS
javascript:Lino.uploads.Uploads.detail.run(null,{ "record_id": 4 })


Now let's inspect the javascript of the first button

>>> dots = btn['href'][56:-1]
>>> print(dots)  #doctest: +ELLIPSIS 
{ ... }

They are a big "object" (in Python we call it a `dict`):

>>> d = AttrDict(json.loads(dots))

It has 3 keys:

>>> len(d)
3

>>> len(d.param_values)
10

>>> d.base_params['mt'] #doctest: +ELLIPSIS
5...
>>> d.base_params['mk'] #doctest: +ELLIPSIS
177
>>> d.base_params['type_id'] #doctest: +ELLIPSIS
1

>>> data_record_keys = list(rmu(d.data_record.keys()))
>>> data_record_keys.sort()
>>> data_record_keys
['data', 'phantom', 'title']
>>> d.data_record['phantom']
True
>>> print(d.data_record['title'])
Einfügen in Uploads von BRECHT Bernd (177) (Ist aktiv)

>>> data_record_data_keys = list(rmu(d.data_record['data'].keys()))
>>> data_record_data_keys.sort()
>>> data_record_data_keys
['company', 'companyHidden', 'contact_person', 'contact_personHidden', 'contact_role', 'contact_roleHidden', 'description', 'disable_editing', 'disabled_fields', 'end_date', 'file', 'id', 'needed', 'owner', 'project', 'projectHidden', 'remark', 'start_date', 'type', 'typeHidden', 'user', 'userHidden']

>>> data_record_data = rmu(d.data_record['data'])
>>> sixprint(data_record_data)
... #doctest: +NORMALIZE_WHITESPACE +REPORT_UDIFF
{'company': None
 'companyHidden': None
 'contact_person': None
 'contact_personHidden': None
 'contact_role': None
 'contact_roleHidden': None
 'description': ''
 'disable_editing': False
 'disabled_fields': {'mimetype': True}
 'end_date': None
 'file': ''
 'id': None
 'needed': True
 'owner': '&lt;a href="javascript:Lino.pcsw.Clients.detail.run(null,{ &amp;quot;record_id&amp;quot;: 177 })"&gt;BRECHT Bernd (177)&lt;/a&gt;'
 'project': 'BRECHT Bernd (177)'
 'projectHidden': 177
 'remark': ''
 'start_date': None
 'type': 'Aufenthaltserlaubnis'
 'typeHidden': 1
 'user': 'Rolf Rompen'
 'userHidden': 1}
