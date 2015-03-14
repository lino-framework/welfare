.. _welfare.tested.pcsw:

============
General PCSW
============

..
  This document is part of the test suite.
  To test only this document, run::

    $ python setup.py test -s tests.DocsTests.test_pcsw

A technical tour into the :mod:`lino_welfare.modlib.pcsw` module.

.. include:: /include/tested.rst

.. contents::
   :depth: 2


..
    >>> from __future__ import print_function
    >>> import os
    >>> os.environ['DJANGO_SETTINGS_MODULE'] = \
    ...    'lino_welfare.projects.std.settings.doctests'
    >>> from lino.api.doctest import *


>>> ses = rt.login('robin')
>>> translation.activate('en')

StrangeClients
==============


>>> ses.show(pcsw.StrangeClients, param_values=dict(similar_persons=True))
+-----------------------------------------+----------------------------------------------------------------------------+-----------------+
| Name                                    | Error message                                                              | Primary coach   |
+=========================================+============================================================================+=================+
| AUSDEMWALD Alfons (116)                 | Neither valid eId data nor alternative identifying document                | Caroline Carnol |
+-----------------------------------------+----------------------------------------------------------------------------+-----------------+
| BASTIAENSEN Laurent (117)               | Neither valid eId data nor alternative identifying document                |                 |
+-----------------------------------------+----------------------------------------------------------------------------+-----------------+
| BRAUN Bruno (257)                       | Neither valid eId data nor alternative identifying document                |                 |
+-----------------------------------------+----------------------------------------------------------------------------+-----------------+
| COLLARD Charlotte (118)                 | Neither valid eId data nor alternative identifying document                | Hubert Huppertz |
+-----------------------------------------+----------------------------------------------------------------------------+-----------------+
| DEMEULENAERE Dorothée (122)             | 1 similar clients: DOBBELSTEIN-DEMEULENAERE Dorothée (123);                |                 |
|                                         | Neither valid eId data nor alternative identifying document                |                 |
+-----------------------------------------+----------------------------------------------------------------------------+-----------------+
| DOBBELSTEIN Dorothée (124)              | 1 similar clients: DOBBELSTEIN-DEMEULENAERE Dorothée (123);                | Mélanie Mélard  |
|                                         | Neither valid eId data nor alternative identifying document                |                 |
+-----------------------------------------+----------------------------------------------------------------------------+-----------------+
| DOBBELSTEIN-DEMEULENAERE Dorothée (123) | 2 similar clients: DEMEULENAERE Dorothée (122), DOBBELSTEIN Dorothée (124) | Mélanie Mélard  |
+-----------------------------------------+----------------------------------------------------------------------------+-----------------+
| DUBOIS Robin (179)                      | Neither valid eId data nor alternative identifying document                | Hubert Huppertz |
+-----------------------------------------+----------------------------------------------------------------------------+-----------------+
| EIERSCHAL Emil (175)                    | Neither valid eId data nor alternative identifying document                |                 |
+-----------------------------------------+----------------------------------------------------------------------------+-----------------+
| EMONTS Daniel (128)                     | Neither valid eId data nor alternative identifying document                | Mélanie Mélard  |
+-----------------------------------------+----------------------------------------------------------------------------+-----------------+
| EMONTS-GAST Erna (152)                  | 1 similar clients: EMONTSPOOL Erwin (151);                                 | Hubert Huppertz |
|                                         | Neither valid eId data nor alternative identifying document                |                 |
+-----------------------------------------+----------------------------------------------------------------------------+-----------------+
| EMONTSPOOL Erwin (151)                  | 1 similar clients: EMONTS-GAST Erna (152);                                 |                 |
|                                         | Neither valid eId data nor alternative identifying document                |                 |
+-----------------------------------------+----------------------------------------------------------------------------+-----------------+
| ENGELS Edgar (129)                      | Neither valid eId data nor alternative identifying document                | Mélanie Mélard  |
+-----------------------------------------+----------------------------------------------------------------------------+-----------------+
| ERNST Berta (125)                       | Neither valid eId data nor alternative identifying document                |                 |
+-----------------------------------------+----------------------------------------------------------------------------+-----------------+
| EVERS Eberhart (127)                    | Neither valid eId data nor alternative identifying document                | Alicia Allmanns |
+-----------------------------------------+----------------------------------------------------------------------------+-----------------+
| FRISCH Paul (238)                       | Neither valid eId data nor alternative identifying document                |                 |
+-----------------------------------------+----------------------------------------------------------------------------+-----------------+
| GERNEGROß Germaine (131)                | Neither valid eId data nor alternative identifying document                |                 |
+-----------------------------------------+----------------------------------------------------------------------------+-----------------+
| GROTECLAES Gregory (132)                | Neither valid eId data nor alternative identifying document                | Alicia Allmanns |
+-----------------------------------------+----------------------------------------------------------------------------+-----------------+
| HILGERS Henri (134)                     | Neither valid eId data nor alternative identifying document                |                 |
+-----------------------------------------+----------------------------------------------------------------------------+-----------------+
| HILGERS Hildegard (133)                 | Neither valid eId data nor alternative identifying document                | Mélanie Mélard  |
+-----------------------------------------+----------------------------------------------------------------------------+-----------------+
| INGELS Irene (135)                      | Neither valid eId data nor alternative identifying document                |                 |
+-----------------------------------------+----------------------------------------------------------------------------+-----------------+
| JACOBS Jacqueline (137)                 | Neither valid eId data nor alternative identifying document                | Caroline Carnol |
+-----------------------------------------+----------------------------------------------------------------------------+-----------------+
| JANSEN Jérémy (136)                     | Neither valid eId data nor alternative identifying document                |                 |
+-----------------------------------------+----------------------------------------------------------------------------+-----------------+
| JEANÉMART Jérôme (181)                  | Neither valid eId data nor alternative identifying document                | Hubert Huppertz |
+-----------------------------------------+----------------------------------------------------------------------------+-----------------+
| JONAS Josef (139)                       | Neither valid eId data nor alternative identifying document                | Hubert Huppertz |
+-----------------------------------------+----------------------------------------------------------------------------+-----------------+
| KAIVERS Karl (141)                      | Neither valid eId data nor alternative identifying document                | Mélanie Mélard  |
+-----------------------------------------+----------------------------------------------------------------------------+-----------------+
| KASENNOVA Tatjana (221)                 | Neither valid eId data nor alternative identifying document                |                 |
+-----------------------------------------+----------------------------------------------------------------------------+-----------------+
| KELLER Karl (178)                       | Neither valid eId data nor alternative identifying document                | Hubert Huppertz |
+-----------------------------------------+----------------------------------------------------------------------------+-----------------+
| LAHM Lisa (176)                         | Neither valid eId data nor alternative identifying document                |                 |
+-----------------------------------------+----------------------------------------------------------------------------+-----------------+
| LAMBERTZ Guido (142)                    | Neither valid eId data nor alternative identifying document                | Mélanie Mélard  |
+-----------------------------------------+----------------------------------------------------------------------------+-----------------+
| LASCHET Laura (143)                     | Neither valid eId data nor alternative identifying document                |                 |
+-----------------------------------------+----------------------------------------------------------------------------+-----------------+
| LAZARUS Line (144)                      | Neither valid eId data nor alternative identifying document                | Mélanie Mélard  |
+-----------------------------------------+----------------------------------------------------------------------------+-----------------+
| MALMENDIER Marc (146)                   | Neither valid eId data nor alternative identifying document                | Hubert Huppertz |
+-----------------------------------------+----------------------------------------------------------------------------+-----------------+
| MARTELAER Mark (172)                    | Neither valid eId data nor alternative identifying document                |                 |
+-----------------------------------------+----------------------------------------------------------------------------+-----------------+
| MEESSEN Melissa (147)                   | Neither valid eId data nor alternative identifying document                | Mélanie Mélard  |
+-----------------------------------------+----------------------------------------------------------------------------+-----------------+
| MEIER Marie-Louise (149)                | Neither valid eId data nor alternative identifying document                |                 |
+-----------------------------------------+----------------------------------------------------------------------------+-----------------+
| RADERMACHER Alfons (153)                | Neither valid eId data nor alternative identifying document                | Mélanie Mélard  |
+-----------------------------------------+----------------------------------------------------------------------------+-----------------+
| RADERMACHER Berta (154)                 | Neither valid eId data nor alternative identifying document                |                 |
+-----------------------------------------+----------------------------------------------------------------------------+-----------------+
| RADERMACHER Christian (155)             | Neither valid eId data nor alternative identifying document                | Alicia Allmanns |
+-----------------------------------------+----------------------------------------------------------------------------+-----------------+
| RADERMACHER Daniela (156)               | Neither valid eId data nor alternative identifying document                |                 |
+-----------------------------------------+----------------------------------------------------------------------------+-----------------+
| RADERMACHER Edgard (157)                | Neither valid eId data nor alternative identifying document                | Caroline Carnol |
+-----------------------------------------+----------------------------------------------------------------------------+-----------------+
| RADERMACHER Guido (159)                 | Neither valid eId data nor alternative identifying document                | Mélanie Mélard  |
+-----------------------------------------+----------------------------------------------------------------------------+-----------------+
| RADERMACHER Hedi (161)                  | Neither valid eId data nor alternative identifying document                | Caroline Carnol |
+-----------------------------------------+----------------------------------------------------------------------------+-----------------+
| RADERMACHER Inge (162)                  | Neither valid eId data nor alternative identifying document                |                 |
+-----------------------------------------+----------------------------------------------------------------------------+-----------------+
| RADERMECKER Rik (173)                   | Neither valid eId data nor alternative identifying document                | Mélanie Mélard  |
+-----------------------------------------+----------------------------------------------------------------------------+-----------------+
| VANDENMEULENBOS Marie-Louise (174)      | 1 similar clients: MEIER Marie-Louise (149);                               |                 |
|                                         | Neither valid eId data nor alternative identifying document                |                 |
+-----------------------------------------+----------------------------------------------------------------------------+-----------------+
| DA VINCI David (165)                    | Neither valid eId data nor alternative identifying document                | Hubert Huppertz |
+-----------------------------------------+----------------------------------------------------------------------------+-----------------+
| DI RUPO Didier (164)                    | Neither valid eId data nor alternative identifying document                |                 |
+-----------------------------------------+----------------------------------------------------------------------------+-----------------+
| VAN VEEN Vincent (166)                  | Neither valid eId data nor alternative identifying document                | Hubert Huppertz |
+-----------------------------------------+----------------------------------------------------------------------------+-----------------+
| ÖSTGES Otto (168)                       | Neither valid eId data nor alternative identifying document                | Hubert Huppertz |
+-----------------------------------------+----------------------------------------------------------------------------+-----------------+
<BLANKLINE>


The MyStrangeClients table (here e.g. Alicia's) shows only those
strange client for whom i am the primary coach:

>>> rt.login('alicia').show(pcsw.MyStrangeClients)
============================= ============================================================= =================
 Name                          Error message                                                 Primary coach
----------------------------- ------------------------------------------------------------- -----------------
 AUSDEMWALD Alfons (116)       Neither valid eId data nor alternative identifying document   Caroline Carnol
 EVERS Eberhart (127)          Neither valid eId data nor alternative identifying document   Alicia Allmanns
 GROTECLAES Gregory (132)      Neither valid eId data nor alternative identifying document   Alicia Allmanns
 JEANÉMART Jérôme (181)        Neither valid eId data nor alternative identifying document   Hubert Huppertz
 KAIVERS Karl (141)            Neither valid eId data nor alternative identifying document   Mélanie Mélard
 RADERMACHER Christian (155)   Neither valid eId data nor alternative identifying document   Alicia Allmanns
 DA VINCI David (165)          Neither valid eId data nor alternative identifying document   Hubert Huppertz
============================= ============================================================= =================
<BLANKLINE>



eID card summary
----------------

Here a test case (fixed :blogref:`20130827`) 
to test the new `eid_info` field:

>>> soup = get_json_soup('rolf', 'pcsw/Clients/177', 'overview')
>>> print(soup.get_text("\n"))
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
Ansicht als 
Partner
, 
Person
, Klient
Herr
Bernd 
Brecht
Deutschland
Adressen verwalten
Karte Nr. 591413288107 (Belgischer Staatsbürger), ausgestellt durch Eupen, gültig von 19.08.11 bis 19.08.16

>>> soup = get_json_soup('rolf', 'pcsw/Clients/116', 'overview')
>>> print(soup.get_text("\n"))
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
Ansicht als
Partner
, 
Person
, Klient
Herr
Alfons 
Ausdemwald
Am Bahndamm
4700 Eupen
Adressen verwalten
Karte Nr. 123456789012 (C (Personalausweis für Ausländer)), ausgestellt durch Eupen
, gültig von 19.08.12 bis 18.08.13
Muss eID-Karte einlesen!


Coaching types
--------------

>>> with translation.override('de'):
...    ses.show(pcsw.CoachingTypes)
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE -REPORT_UDIFF
====================== ===================== =================== ======= ======= =====================
 Bezeichnung            Bezeichnung (fr)      Bezeichnung (de)    DSBE    GSS     Role in evaluations
---------------------- --------------------- ------------------- ------- ------- ---------------------
 General                SSG                   ASD                 Nein    Ja      Kollege
 Integ                  SI                    DSBE                Ja      Nein    Kollege
 Debts mediation        Médiation de dettes   Schuldnerberatung   Nein    Nein
 **Total (3 Zeilen)**                                             **1**   **1**
====================== ===================== =================== ======= ======= =====================
<BLANKLINE>


.. _welfare.clients.parameters:

Filtering clients
-----------------

The demo database contains at least one client 

- whose client_state is "Coached"
- who has several coachings
- at least one of these coachings has been ended.

For example, let's log in as Mélanie and look at client Robin DUBOIS:

>>> ses = rt.login('melanie')
>>> pk = 179
>>> obj = pcsw.Client.objects.get(pk=pk)
>>> print(obj)
DUBOIS Robin (179)

Robin is coached:

>>> obj.client_state
<ClientStates.coached:30>

Here are Robin's coachings. Note that Mélanie stopped to coach Robin
on 08.03.2013:

>>> ses.show(pcsw.CoachingsByClient, master_instance=obj, column_names="start_date end_date user primary")
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
====================== ========== ================= ========
 Begleitet seit         bis        Begleiter         Primär 
---------------------- ---------- ----------------- --------
  03.03.12                          Hubert Huppertz   Nein
  13.03.12               08.03.13   Mélanie Mélard    Nein
  08.03.13               24.10.13   Alicia Allmanns   Nein
  24.10.13                          Hubert Huppertz   Ja
  **Total (4 Zeilen)**                                **1**
====================== ========== ================= ========
<BLANKLINE>

Another client is Dorothée Dobbelstein who is coached by three
different agents at the same time:

>>> obj = pcsw.Client.objects.get(pk=124)
>>> obj
Client #124 (u'DOBBELSTEIN Doroth\xe9e (124)')
>>> ses.show(pcsw.CoachingsByClient, master_instance=obj, column_names="start_date end_date user primary")
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
====================== ===== ================= ========
 Begleitet seit         bis   Begleiter         Primär
---------------------- ----- ----------------- --------
 24.10.13                     Mélanie Mélard    Ja
 13.12.13                     Caroline Carnol   Nein
 02.04.14                     Hubert Huppertz   Nein
 **Total (3 Zeilen)**                           **1**
====================== ===== ================= ========
<BLANKLINE>

A third client is David DA VINCI:

>>> obj = pcsw.Client.objects.get(pk=165)
>>> print(obj)
DA VINCI David (165)
>>> ses.show(pcsw.CoachingsByClient, master_instance=obj, column_names="start_date end_date user primary")
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
====================== ========== ================= ========
 Begleitet seit         bis        Begleiter         Primär
---------------------- ---------- ----------------- --------
 03.03.12                          Hubert Huppertz   Ja
 08.03.13               04.10.13   Mélanie Mélard    Nein
 04.10.13                          Alicia Allmanns   Nein
 **Total (3 Zeilen)**                                **1**
====================== ========== ================= ========
<BLANKLINE>


When Mélanie opens her :menuselection:`Integration --> Clients` list,
then she sees the following clients (Dorothée is there, but Robin
isn't):

>>> ses.show(integ.Clients, column_names="name_column")
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE -REPORT_UDIFF
=============================
 Name
-----------------------------
 BRECHT Bernd (177)
 DOBBELSTEIN Dorothée (124)
 EMONTS Daniel (128)
 ENGELS Edgar (129)
 EVERS Eberhart (127)
 HILGERS Hildegard (133)
 JACOBS Jacqueline (137)
 JEANÉMART Jérôme (181)
 KAIVERS Karl (141)
 LAMBERTZ Guido (142)
 LAZARUS Line (144)
 MEESSEN Melissa (147)
 RADERMACHER Alfons (153)
 RADERMACHER Christian (155)
 RADERMACHER Edgard (157)
 RADERMACHER Guido (159)
 RADERMECKER Rik (173)
 VAN VEEN Vincent (166)
=============================
<BLANKLINE>

Here is a list of Mélanies clients on 2013-04-01.  We get it by
manually filling that date into the
:attr:`welfare.pcsw.Clients.end_date` parameter field.  Note that

- Dorothée is **not** included since Mélanie started coaching her only
  2014-04-02
- David **is** included since Mélanie started coaching him already
  2012-03-03

>>> pv = dict(end_date=i2d(20130401))
>>> ses.show(integ.Clients, column_names="name_column", param_values=pv)
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE -REPORT_UDIFF
=========================
 Name
-------------------------
 AUSDEMWALD Alfons (116)
 ENGELS Edgar (129)
 JONAS Josef (139)
 LAMBERTZ Guido (142)
 RADERMACHER Guido (159)
 DA VINCI David (165)
=========================
<BLANKLINE>



Creating a new client
=====================


>>> url = '/api/pcsw/Clients/-99999?an=insert&fmt=json'
>>> res = test_client.get(url, REMOTE_USER='rolf')
>>> res.status_code
200
>>> d = AttrDict(json.loads(res.content))
>>> d.keys()
[u'phantom', u'data', u'title']
>>> d.phantom
True
>>> print(d.title)
Einfügen in Klienten (Begleitet)

There are a lot of data fields:

>>> len(d.data.keys())
67


The detail action
=================

The following would have detected a bug which caused the MTI navigator
to not work (bug has been fixed :blogref:`20150227`) :

>>> from lino.utils.xmlgen.html import E
>>> p = contacts.Person.objects.get(pk=178)
>>> cli = pcsw.Client.objects.get(pk=178)

>>> ses = rt.login('robin')
>>> ar = contacts.Partners.request_from(ses)
>>> print(cli.get_detail_action(ses))
<BoundAction(pcsw.Clients, <ShowDetailAction detail (u'Detail')>)>
>>> print(cli.get_detail_action(ar))
<BoundAction(pcsw.Clients, <ShowDetailAction detail (u'Detail')>)>

And this tests a potential source of problems in `E.tostring` which I
removed at the same time:

>>> ses = rt.login('robin', renderer=settings.SITE.kernel.extjs_renderer)
>>> ar = contacts.Partners.request_from(ses)
>>> ar.renderer = settings.SITE.kernel.extjs_renderer
>>> print(E.tostring(ar.obj2html(p)))
<a href="javascript:Lino.contacts.Persons.detail.run(null,{ &quot;record_id&quot;: 178 })">Herr Karl KELLER (178)</a>

>>> print(E.tostring(ar.obj2html(cli)))
<a href="javascript:Lino.pcsw.Clients.detail.run(null,{ &quot;record_id&quot;: 178 })">KELLER Karl (178)</a>
>>> print(settings.SITE.kernel.extjs_renderer.instance_handler(ar, cli))
Lino.pcsw.Clients.detail.run(null,{ "record_id": 178 })
>>> print(E.tostring(p.get_mti_buttons(ar)))
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE -REPORT_UDIFF
<a href="javascript:Lino.contacts.Partners.detail.run(null,{
&quot;record_id&quot;: 178 })">Partner</a>, <b>Person</b>, <a
href="javascript:Lino.pcsw.Clients.detail.run(null,{
&quot;record_id&quot;: 178 })">Klient</a> [<a
href="javascript:Lino.contacts.Partners.del_client(null,178,{
})">&#10060;</a>]


Combined first names
====================

Normal people need *two* matching words.  And by "words" we mean the
phonetic reductions of the words in their first and last name (not
middle).

>>> alf = pcsw.Client.objects.get(pk=116)
>>> alf.name
u'Ausdemwald Alfons'
>>> alf.get_dupable_words('name')
[u'ASTM', u'ALFN']

>>> alf.dupable_matches_required()
2

Marie-Louise is a frist name with two words. Such people need *three*
instead of the usual *two* matching words:

>>> mlv = pcsw.Client.objects.get(pk=174)
>>> mlv.name
u'Vandenmeulenbos Marie-Louise'
>>> mlv.get_dupable_words('name')
[u'FNTN', u'MR', u'LS']
>>> mlv.dupable_matches_required()
3

>>> mlm = pcsw.Client.objects.get(pk=149)
>>> mlm.name
u'Meier Marie-Louise'
>>> mlm.get_dupable_words('name')
[u'MR', u'MR', u'LS']
>>> mlm.dupable_matches_required()
3

Another problem is that "Meier" and "Marie" have the same phonetic
reduction "MR". This is why M-L Vandenmeulenbos is still wrongly
detected as being similar to M-L Meier:

>>> mlv.find_similar_instances()
[Client #149 (u'MEIER Marie-Louise (149)')]

While M-L Meier does not 

>>> mlm.find_similar_instances()
[]


