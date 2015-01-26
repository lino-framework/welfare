.. _welfare.tested.uploads:

=============
Uploads
=============

.. How to test only this document:

  $ python setup.py test -s tests.DocsTests.test_uploads

A technical tour into the :mod:`lino_welfare.modlib.uploads` plugin.

Lino Welfare extends the standard :mod:`lino.modlib.uploads` plugin
into a system which helps social agents to manage certain documents
about their clients. For example, integration agents want to get a
reminder when the driving license of one of their client is going to
expire.

.. contents::
   :depth: 2

About this document
===================

.. include:: /include/tested.rst

>>> from __future__ import print_function
>>> import os
>>> os.environ['DJANGO_SETTINGS_MODULE'] = \
...    'lino_welfare.projects.eupen.settings.doctests'
>>> from lino.api.doctest import *
    
This documents uses the :mod:`lino_welfare.projects.eupen` test
database:

>>> print(settings.SETTINGS_MODULE)
lino_welfare.projects.eupen.settings.doctests

>>> dd.today()
datetime.date(2014, 5, 22)


Configuring upload types
========================

This is the list of upload types:

>>> rt.login('rolf').show(uploads.UploadTypes)
======= ============================ ======== ============= ========================= ====================== ============================
 ID      Bezeichnung                  Wanted   Max. number   Ablaufwarnung (Einheit)   Ablaufwarnung (Wert)   Upload shortcut
------- ---------------------------- -------- ------------- ------------------------- ---------------------- ----------------------------
 2       Arbeitserlaubnis             Ja       1             monatlich                 2
 1       Aufenthaltserlaubnis         Ja       1             monatlich                 2
 7       Behindertenausweis           Nein     -1                                      1
 8       Diplom                       Ja       -1                                      1
 3       Führerschein                 Ja       1             monatlich                 1
 4       Identifizierendes Dokument   Ja       1             monatlich                 1                      Identifizierendes Dokument
 9       Personalausweis              Nein     -1                                      1
 5       Vertrag                      Nein     -1                                      1
 6       Ärztliche Bescheinigung      Nein     -1                                      1
 **0**                                **5**    **-1**                                  **11**
======= ============================ ======== ============= ========================= ====================== ============================
<BLANKLINE>


Two clients and their uploads
=============================

This newcomer has 2 id cards. one of these is no longer valid
(and we know it: `needed` has been unchecked). The other is
still valid but will expire in 3 days.

>>> newcomer = pcsw.Client.objects.get(pk=121)
>>> print(newcomer)
DERICUM Daniel (121)

>>> rt.login('romain').show(uploads.UploadsByClient, newcomer)
============================ ============ ======= ============== =================== =======
 Upload-Art                   Gültig bis   Nötig   Beschreibung   Hochgeladen durch   Datei
---------------------------- ------------ ------- -------------- ------------------- -------
 Identifizierendes Dokument   22.04.14     Nein                   Theresia Thelen
 Identifizierendes Dokument   25.05.14     Ja                     Theresia Thelen
 **Total (2 Zeilen)**                      **1**
============================ ============ ======= ============== =================== =======
<BLANKLINE>


>>> oldclient = pcsw.Client.objects.get(pk=124)
>>> print(unicode(oldclient))
DOBBELSTEIN Dorothée (124)

>>> rt.login('romain').show(uploads.UploadsByClient, oldclient)
====================== ============ ======= ============== =================== =======
 Upload-Art             Gültig bis   Nötig   Beschreibung   Hochgeladen durch   Datei
---------------------- ------------ ------- -------------- ------------------- -------
 Aufenthaltserlaubnis   18.03.15     Ja                     Theresia Thelen
 Arbeitserlaubnis       30.08.14     Ja                     Alicia Allmanns
 Führerschein           01.06.14     Ja                     Caroline Carnol
 **Total (3 Zeilen)**                **3**
====================== ============ ======= ============== =================== =======
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
======= ============================ ============================ ============ ============ ======= ============== =======
 ID      Klient                       Upload-Art                   Gültig von   Gültig bis   Nötig   Beschreibung   Datei
------- ---------------------------- ---------------------------- ------------ ------------ ------- -------------- -------
 9       DOBBELSTEIN Dorothée (124)   Aufenthaltserlaubnis                      18.03.15     Ja
 8       DERICUM Daniel (121)         Identifizierendes Dokument                25.05.14     Ja
 7       DERICUM Daniel (121)         Identifizierendes Dokument                22.04.14     Nein
 **0**                                                                                       **2**
======= ============================ ============================ ============ ============ ======= ============== =======
<BLANKLINE>


And the same for Caroline:

>>> rt.login('caroline').show(uploads.MyUploads)
======= ============================ ============== ============ ============ ======= ============== =======
 ID      Klient                       Upload-Art     Gültig von   Gültig bis   Nötig   Beschreibung   Datei
------- ---------------------------- -------------- ------------ ------------ ------- -------------- -------
 11      DOBBELSTEIN Dorothée (124)   Führerschein                01.06.14     Ja
 **0**                                                                         **1**
======= ============================ ============== ============ ============ ======= ============== =======
<BLANKLINE>


This is the MyExpiringUploads table for :ref:`hubert`:

>>> rt.login('hubert').show(uploads.MyExpiringUploads)
========================= ====================== =================== ============ ============ =======
 Klient                    Upload-Art             Hochgeladen durch   Gültig von   Gültig bis   Nötig
------------------------- ---------------------- ------------------- ------------ ------------ -------
 AUSDEMWALD Alfons (116)   Aufenthaltserlaubnis   Hubert Huppertz                  17.05.15     Ja
 AUSDEMWALD Alfons (116)   Arbeitserlaubnis       Hubert Huppertz                  17.05.15     Ja
 **Total (2 Zeilen)**                                                                           **2**
========================= ====================== =================== ============ ============ =======
<BLANKLINE>

:ref:`theresia` does not coach anybody, so the `MyExpiringUploads`
table is empty for her:

>>> rt.login('theresia').show(uploads.MyExpiringUploads)
<BLANKLINE>
Keine Daten anzuzeigen
<BLANKLINE>



Shortcut fields
===============

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
<a href='javascript:Lino.uploads.Uploads.detail.run(null,{ "record_id": 7 })'>Last</a>

The second item is just the comma which separates the two buttons:

>>> div.contents[1]
u', '

The second button opens the list of uploads:

>>> div.contents[2]  #doctest: +ELLIPSIS
<a href='javascript:Lino.uploads.UploadsByClient.grid.run(null,...)'>All 2 files</a>

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

>>> d.keys()
[u'record_id', u'param_values', u'base_params']

>>> d.record_id
7
>>> d.base_params
{u'mt': 54, u'type': 4, u'mk': 121}
>>> d.param_values
{u'pupload_type': None, u'puser': None, u'end_date': None, u'observed_eventHidden': u'20', u'observed_event': u'Is active', u'coached_by': None, u'pupload_typeHidden': None, u'coached_byHidden': None, u'puserHidden': None, u'start_date': None}



Uploads by client
-----------------

The following example is for client # 177
>>> obj = pcsw.Client.objects.get(pk=177)
>>> print(obj)
BRECHT Bernd (177)

>>> soup = get_json_soup('rolf', 'pcsw/Clients/177', 'UploadsByClient')
>>> print(soup.get_text())
... #doctest: +NORMALIZE_WHITESPACE
Aufenthaltserlaubnis: Arbeitserlaubnis: Führerschein: 3Identifizierendes Dokument: 4Diplom:

>>> links = soup.find_all('a')
>>> len(links)
5

>>> rt.modules.uploads.UploadsByClient._upload_area
<UploadAreas.general:90>

The first link would run the insert action on UploadsByClient, with
the owner set to this client

>>> btn = links[0]
>>> print(btn)
... #doctest: +NORMALIZE_WHITESPACE +ELLIPSIS
<a href='javascript:Lino.uploads.UploadsByClient.insert.run(null,{ ... })' 
style="vertical-align:-30%;" 
title="Neuen Datensatz erstellen"><img alt="add" 
src="/media/lino/extjs/images/mjames/add.png"/></a>

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

>>> d.keys()
[u'data_record', u'param_values', u'base_params']

>>> d.data_record
{u'phantom': True, u'data': {u'file': u'', u'owner': u'<a href="javascript:Lino.pcsw.Clients.detail.run(null,{ &quot;record_id&quot;: 177 })">BRECHT Bernd (177)</a>', u'id': None, u'userHidden': 1, u'projectHidden': 177, u'needed': True, u'disabled_fields': {u'mimetype': True}, u'type': u'Aufenthaltserlaubnis', u'start_date': None, u'description': u'', u'end_date': None, u'company': None, u'contact_role': None, u'disable_editing': False, u'companyHidden': None, u'contact_personHidden': None, u'user': u'Rolf Rompen', u'contact_roleHidden': None, u'remark': u'', u'disabled_actions': {}, u'typeHidden': 1, u'project': u'BRECHT Bernd (177)', u'contact_person': None}, u'title': u'Uploads von BRECHT Bernd (177) (Ist aktiv)'}
>>> d.base_params
{u'mt': 54, u'mk': 177, u'type_id': 1}
