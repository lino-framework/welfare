.. _welfare.clients.parameters:
.. _welfare.specs.clients:

=================
Filtering clients
=================

This document describes and tests some ways of filtering clients.

Most code is in :mod:`lino_welfare.modlib.pcsw` plugin.


.. How to test only this document:

    $ python setup.py test -s tests.SpecsTests.test_clients
    
    doctest init
    
    >>> from lino import startup
    >>> startup('lino_welfare.projects.std.settings.doctests')
    >>> from lino.api.doctest import *

    >>> ClientEvents = pcsw.ClientEvents
    >>> ses = rt.login("hubert")



.. contents::
   :depth: 2
   :local:

Default lists of coached clients
================================

>>> ses.show(pcsw.CoachedClients, column_names="name_column")
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE -REPORT_UDIFF
=============================
 Name
-----------------------------
 AUSDEMWALD Alfons (116)
 BRECHT Bernd (177)
 COLLARD Charlotte (118)
 DOBBELSTEIN Dorothée (124)
 DUBOIS Robin (179)
 EMONTS Daniel (128)
 EMONTS-GAST Erna (152)
 ENGELS Edgar (129)
 EVERS Eberhart (127)
 GROTECLAES Gregory (132)
 HILGERS Hildegard (133)
 JACOBS Jacqueline (137)
 JEANÉMART Jérôme (181)
 JONAS Josef (139)
 KAIVERS Karl (141)
 KELLER Karl (178)
 LAMBERTZ Guido (142)
 LAZARUS Line (144)
 MALMENDIER Marc (146)
 MEESSEN Melissa (147)
 RADERMACHER Alfons (153)
 RADERMACHER Christian (155)
 RADERMACHER Edgard (157)
 RADERMACHER Guido (159)
 RADERMACHER Hedi (161)
 RADERMECKER Rik (173)
 DA VINCI David (165)
 VAN VEEN Vincent (166)
 ÖSTGES Otto (168)
=============================
<BLANKLINE>

>>> ses.show(integ.Clients, column_names="name_column")
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE -REPORT_UDIFF
============================
 Name
----------------------------
 BRECHT Bernd (177)
 COLLARD Charlotte (118)
 DOBBELSTEIN Dorothée (124)
 DUBOIS Robin (179)
 EMONTS-GAST Erna (152)
 EVERS Eberhart (127)
 GROTECLAES Gregory (132)
 JEANÉMART Jérôme (181)
 JONAS Josef (139)
 KELLER Karl (178)
 LAMBERTZ Guido (142)
 LAZARUS Line (144)
 MALMENDIER Marc (146)
 MEESSEN Melissa (147)
 RADERMACHER Edgard (157)
 RADERMACHER Hedi (161)
 DA VINCI David (165)
 VAN VEEN Vincent (166)
 ÖSTGES Otto (168)
============================
<BLANKLINE>



Filtering clients about their coachings
=======================================

The demo database contains at least one client which meets the
following conditions:

- the client_state is "Coached"
- has several coachings
- at least one of these coachings has been ended.

For example, let's log in as Mélanie and look at client Robin DUBOIS:

>>> pk = 179
>>> obj = pcsw.Client.objects.get(pk=pk)
>>> print(obj)
DUBOIS Robin (179)

Robin is coached:

>>> obj.client_state
<ClientStates.coached:30>

>>> translation.activate('de')

Here are Robin's coachings. Note that Mélanie stopped to coach Robin
on 08.03.2013:

>>> ses.show('coachings.CoachingsByClient', master_instance=obj, column_names="start_date end_date user primary")
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
================ ========== ================= ========
 Begleitet seit   bis        Begleiter         Primär 
---------------- ---------- ----------------- --------
  03.03.12                    Hubert Huppertz   Nein
  13.03.12         08.03.13   Mélanie Mélard    Nein
  08.03.13         24.10.13   Alicia Allmanns   Nein
  24.10.13                    Hubert Huppertz   Ja
================ ========== ================= ========
<BLANKLINE>

Another client is Dorothée Dobbelstein who is coached by three
different agents at the same time:

>>> obj = pcsw.Client.objects.get(pk=124)
>>> obj
Client #124 ('DOBBELSTEIN Doroth\xe9e (124)')
>>> ses.show('coachings.CoachingsByClient', master_instance=obj, column_names="start_date end_date user primary")
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
================ ===== ================= ========
 Begleitet seit   bis   Begleiter         Primär
---------------- ----- ----------------- --------
 24.10.13               Mélanie Mélard    Ja
 13.12.13               Caroline Carnol   Nein
 02.04.14               Hubert Huppertz   Nein
================ ===== ================= ========
<BLANKLINE>

A third client is David DA VINCI:

>>> obj = pcsw.Client.objects.get(pk=165)
>>> print(obj)
DA VINCI David (165)
>>> ses.show('coachings.CoachingsByClient', master_instance=obj, column_names="start_date end_date user primary")
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
================ ========== ================= ========
 Begleitet seit   bis        Begleiter         Primär
---------------- ---------- ----------------- --------
 03.03.12                    Hubert Huppertz   Ja
 08.03.13         04.10.13   Mélanie Mélard    Nein
 04.10.13                    Alicia Allmanns   Nein
================ ========== ================= ========
<BLANKLINE>


>>> translation.activate('en')

>>> ses = rt.login('melanie')

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



Filtering clients about their notes
===================================


>>> ses = rt.login('robin')

Coached clients who have at least one note:

>>> pv = dict(observed_event=ClientEvents.note)
>>> ses.show(pcsw.CoachedClients, column_names="name_column", param_values=pv)
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE -REPORT_UDIFF
============================
 Name
----------------------------
 AUSDEMWALD Alfons (116)
 BRECHT Bernd (177)
 COLLARD Charlotte (118)
 DOBBELSTEIN Dorothée (124)
============================
<BLANKLINE>

All clients who have at least one note:

>>> pv = dict(client_state=None, observed_event=ClientEvents.note)
>>> ses.show(pcsw.CoachedClients, column_names="name_column", param_values=pv)
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE -REPORT_UDIFF
=========================================
 Name
-----------------------------------------
 AUSDEMWALD Alfons (116)
 BASTIAENSEN Laurent (117)
 BRECHT Bernd (177)
 COLLARD Charlotte (118)
 DEMEULENAERE Dorothée (122)
 DERICUM Daniel (121)
 DOBBELSTEIN Dorothée (124)
 DOBBELSTEIN-DEMEULENAERE Dorothée (123)
=========================================
<BLANKLINE>


Coached clients who have at least one note dated 2013-07-25 or later:

>>> pv = dict(start_date=i2d(20130725), observed_event=ClientEvents.note)
>>> ses.show(pcsw.CoachedClients, column_names="name_column", param_values=pv)
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE -REPORT_UDIFF
=========================
 Name
-------------------------
 AUSDEMWALD Alfons (116)
=========================
<BLANKLINE>

.. show the SQL when debugging:
    >>> # ar = ses.spawn(pcsw.CoachedClients, param_values=pv)
    >>> # print(ar.data_iterator.query)
    >>> # ses.show(ar, column_names="name_column")

All clients who have at least one note dated 2013-07-25 or later:

>>> pv = dict(start_date=i2d(20130725), observed_event=ClientEvents.note)
>>> pv.update(client_state=None)
>>> ses.show(pcsw.CoachedClients, column_names="name_column", param_values=pv)
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE -REPORT_UDIFF
=========================================
 Name
-----------------------------------------
 AUSDEMWALD Alfons (116)
 DOBBELSTEIN-DEMEULENAERE Dorothée (123)
=========================================
<BLANKLINE>


Filtering clients about their career
====================================


All clients who were learning between 2011-03-11 and 2012-03-11 (at least):

>>> pv = dict(start_date=i2d(20110311), end_date=i2d(20120311), observed_event=ClientEvents.learning)
>>> pv.update(client_state=None)
>>> ses.show(pcsw.CoachedClients, column_names="name_column", param_values=pv)
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE -REPORT_UDIFF
==========================
 Name
--------------------------
 EVERS Eberhart (127)
 KELLER Karl (178)
 MALMENDIER Marc (146)
 MEESSEN Melissa (147)
 RADERMACHER Alfons (153)
 DA VINCI David (165)
 VAN VEEN Vincent (166)
==========================
<BLANKLINE>

Just as a random sample, let's verify one of these clients.  Vincent
van Veen does have a training, but that started only two days later:

>>> obj = pcsw.Client.objects.get(pk=166)
>>> ses.show(cv.TrainingsByPerson, obj, column_names="type start_date end_date")
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE -REPORT_UDIFF
================ ============ ============
 Education Type   Start date   End date
---------------- ------------ ------------
 Alpha            13/03/2011   13/03/2012
================ ============ ============
<BLANKLINE>

And he has no studies:

>>> ses.show(cv.StudiesByPerson, obj, column_names="type start_date end_date")
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE -REPORT_UDIFF
<BLANKLINE>
No data to display
<BLANKLINE>

... but here is a work experience which matches exactly our query:

>>> ses.show(cv.ExperiencesByPerson, obj, column_names="start_date end_date")
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE -REPORT_UDIFF
============ ============
 Start date   End date
------------ ------------
 11/03/2011   11/03/2012
============ ============
<BLANKLINE>
