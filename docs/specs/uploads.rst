.. _welfare.specs.uploads:

=============
Uploads
=============

.. How to test only this document:

    $ python setup.py test -s tests.SpecsTests.test_uploads

    doctest init:
    
    >>> import lino
    >>> lino.startup('lino_welfare.projects.eupen.settings.doctests')
    >>> from lino.api.doctest import *

A technical tour into the :mod:`lino_welfare.modlib.uploads` plugin.

Lino Welfare extends the standard :mod:`lino.modlib.uploads` plugin
into a system which helps social agents to manage certain documents
about their clients. For example, integration agents want to get a
reminder when the driving license of one of their client is going to
expire.

.. contents::
   :depth: 2

    
A few things that should pass, otherwise don't expect the remaining
tests to pass:

>>> print(settings.SETTINGS_MODULE)
lino_welfare.projects.eupen.settings.doctests
>>> dd.today()
datetime.date(2014, 5, 22)

.. Some of the following tests rely on the right value for the
   contenttype id of `pcsw.Client` model. If the following line
   changes, subsequent snippets need to get adapted:

    >>> contenttypes.ContentType.objects.get_for_model(pcsw.Client).id
    55

Configuring upload types
========================

This is the list of upload types:

>>> rt.login('rolf').show(uploads.UploadTypes)
==== ============================ ======== ============= ========================= ====================== ============================
 ID   Bezeichnung                  Wanted   Max. number   Ablaufwarnung (Einheit)   Ablaufwarnung (Wert)   Upload shortcut
---- ---------------------------- -------- ------------- ------------------------- ---------------------- ----------------------------
 2    Arbeitserlaubnis             Ja       1             monatlich                 2
 1    Aufenthaltserlaubnis         Ja       1             monatlich                 2
 7    Behindertenausweis           Nein     -1                                      1
 8    Diplom                       Ja       -1                                      1
 3    Führerschein                 Ja       1             monatlich                 1
 4    Identifizierendes Dokument   Ja       1             monatlich                 1                      Identifizierendes Dokument
 9    Personalausweis              Nein     -1                                      1
 5    Vertrag                      Nein     -1                                      1
 6    Ärztliche Bescheinigung      Nein     -1                                      1
                                            **-1**                                  **11**
==== ============================ ======== ============= ========================= ====================== ============================
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
>>> print(unicode(oldclient))
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

>>> print(unicode(uploads.MyUploads.label))
Meine Uploads

>>> print(unicode(uploads.MyExpiringUploads.label))
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

>>> div.contents[1]
u', '

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

>>> print(json.dumps(d.keys()))
["record_id", "param_values", "base_params"]

>>> d.record_id
8
>>> d.base_params
{u'mt': 55, u'type': 4, u'mk': 121}
>>> print(json.dumps(d.param_values))  #doctest: +NORMALIZE_WHITESPACE
{"userHidden": null, "upload_typeHidden": null, "end_date": null,
"observed_eventHidden": "20", "observed_event": "Est active",
"coached_by": null, "upload_type": null, "coached_byHidden": null,
"start_date": null, "user": null}



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

>>> d.base_params
{u'mt': 55, u'mk': 177, u'type_id': 1}

>>> d.data_record.keys()
[u'phantom', u'data', u'title']
>>> d.data_record['phantom']
True
>>> print(d.data_record['title'])
Einfügen in Uploads von BRECHT Bernd (177) (Ist aktiv)

>>> d.data_record['data'].keys()
[u'file', u'owner', u'id', u'userHidden', u'projectHidden', u'needed', u'disabled_fields', u'type', u'start_date', u'description', u'end_date', u'company', u'contact_role', u'disable_editing', u'companyHidden', u'contact_personHidden', u'user', u'contact_roleHidden', u'remark', u'disabled_actions', u'typeHidden', u'project', u'contact_person']

>>> d.data_record['data']
{u'file': u'', u'owner': u'&lt;a href="javascript:Lino.pcsw.Clients.detail.run(null,{ &amp;quot;record_id&amp;quot;: 177 })"&gt;BRECHT Bernd (177)&lt;/a&gt;', u'id': None, u'userHidden': 1, u'projectHidden': 177, u'needed': True, u'disabled_fields': {u'mimetype': True}, u'type': u'Aufenthaltserlaubnis', u'start_date': None, u'description': u'', u'end_date': None, u'company': None, u'contact_role': None, u'disable_editing': False, u'companyHidden': None, u'contact_personHidden': None, u'user': u'Rolf Rompen', u'contact_roleHidden': None, u'remark': u'', u'disabled_actions': {}, u'typeHidden': 1, u'project': u'BRECHT Bernd (177)', u'contact_person': None}
