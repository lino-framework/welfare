.. doctest docs/specs/clients.rst
   
.. _welfare.clients.parameters:
.. _welfare.specs.clients:

=================
Filtering clients
=================

This document describes and tests some ways of filtering clients.

Most code is in :mod:`lino_welfare.modlib.pcsw` plugin.


.. contents::
   :depth: 2
   :local:

.. include:: /../docs/shared/include/tested.rst
  
>>> from lino import startup
>>> startup('lino_welfare.projects.gerd.settings.doctests')
>>> from lino.api.doctest import *

>>> ClientEvents = pcsw.ClientEvents
>>> ses = rt.login("hubert")


      

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
==========================
 Name
--------------------------
 BRECHT Bernd (177)
 COLLARD Charlotte (118)
 EMONTS Daniel (128)
 EMONTS-GAST Erna (152)
 EVERS Eberhart (127)
 HILGERS Hildegard (133)
 JACOBS Jacqueline (137)
 JEANÉMART Jérôme (181)
 JONAS Josef (139)
 LAMBERTZ Guido (142)
 MALMENDIER Marc (146)
 MEESSEN Melissa (147)
 RADERMACHER Edgard (157)
 RADERMACHER Hedi (161)
 RADERMECKER Rik (173)
 VAN VEEN Vincent (166)
 ÖSTGES Otto (168)
==========================
<BLANKLINE>



Filtering clients about their coachings
=======================================

>>> translation.activate('en')

The demo database contains 13 clients whe meet the following
conditions:

- the client_state is "Coached"
- client has more than 2 coachings
- at least one of these coachings has been ended

>>> from django.db.models import Count
>>> qs = pcsw.Client.objects.filter(client_state=pcsw.ClientStates.coached)
>>> qs = qs.annotate(coachings_count=Count('coachings_by_client'))
>>> qs = qs.filter(coachings_count__gt=2)
>>> qs = qs.filter(coachings_by_client__end_date__isnull=False)
>>> qs = qs.order_by('id')
>>> qs.count()
13
>>> [obj.pk for obj in qs]
[116, 127, 129, 133, 139, 144, 147, 155, 159, 166, 173, 179, 181]

Let's look at some of these clients more in detail.

>>> def show_coachings(pk):
...     obj = pcsw.Client.objects.get(pk=pk)
...     ses.show('coachings.CoachingsByClient', master_instance=obj, column_names="start_date end_date user primary", header_level=4)

>>> show_coachings(179)
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
Coachings of DUBOIS Robin (179) (Is active)
===========================================
============== ============ ================= =========
 Coached from   until        Coach             Primary
-------------- ------------ ----------------- ---------
 03/03/2012                  Alicia Allmanns   Yes
 08/03/2013     04/10/2013   Hubert Huppertz   No
 04/10/2013                  Mélanie Mélard    No
============== ============ ================= =========
<BLANKLINE>

We can see that Robin is currently coached by Alica and Mélanie, and
that Hubert stopped coaching him on 04.10.2013:


Same view for some other clients:

>>> show_coachings(116)
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
Coachings of AUSDEMWALD Alfons (116) (Is active)
================================================
============== ============ ================= =========
 Coached from   until        Coach             Primary
-------------- ------------ ----------------- ---------
 03/03/2012                  Alicia Allmanns   No
 13/03/2012     08/03/2013   Hubert Huppertz   No
 08/03/2013     24/10/2013   Mélanie Mélard    No
 24/10/2013                  Caroline Carnol   Yes
============== ============ ================= =========
<BLANKLINE>


>>> show_coachings(166)
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
Coachings of VAN VEEN Vincent (166) (Is active)
===============================================
============== ============ ================= =========
 Coached from   until        Coach             Primary
-------------- ------------ ----------------- ---------
 03/03/2012                  Hubert Huppertz   Yes
 08/03/2013     04/10/2013   Mélanie Mélard    No
 04/10/2013                  Caroline Carnol   No
============== ============ ================= =========
<BLANKLINE>


>>> print(dd.fds(dd.today()))
22/05/2014

When Mélanie opens her :menuselection:`Integration --> Clients` list,
then she sees the following clients:

>>> ses = rt.login('melanie')
>>> ses.show(integ.Clients, column_names="name_column", header_level=4)
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE -REPORT_UDIFF
Integration Clients (Coached, Coached by Mélanie Mélard)
========================================================
=============================
 Name
-----------------------------
 BRECHT Bernd (177)
 COLLARD Charlotte (118)
 DOBBELSTEIN Dorothée (124)
 DUBOIS Robin (179)
 EMONTS Daniel (128)
 ENGELS Edgar (129)
 GROTECLAES Gregory (132)
 JACOBS Jacqueline (137)
 KAIVERS Karl (141)
 KELLER Karl (178)
 LAZARUS Line (144)
 MALMENDIER Marc (146)
 MEESSEN Melissa (147)
 RADERMACHER Alfons (153)
 RADERMACHER Christian (155)
 RADERMACHER Edgard (157)
 RADERMACHER Guido (159)
 RADERMACHER Hedi (161)
 ÖSTGES Otto (168)
=============================
<BLANKLINE>

Robin is there, but Alfons and Vincent aren't.

Here is a list of Mélanies clients on 2013-10-01.  Mélanie can get
this by manually filling that date into the
:attr:`lino_welfare.modlib.pcsw.Clients.end_date` parameter field.
      
>>> pv = dict(end_date=i2d(20131001))
>>> ses.show(integ.Clients, column_names="name_column", param_values=pv, header_level=4)
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE -REPORT_UDIFF
Integration Clients (Coached, Coached by Mélanie Mélard)
========================================================
=========================
 Name
-------------------------
 AUSDEMWALD Alfons (116)
 ENGELS Edgar (129)
 EVERS Eberhart (127)
 HILGERS Hildegard (133)
 LAZARUS Line (144)
 RADERMACHER Guido (159)
 VAN VEEN Vincent (166)
=========================
<BLANKLINE>


Note that

- Robin is *not* included since Mélanie started coaching him only
  later.
- Vincent *is* now included since Mélanie was coaching him then.



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
 COLLARD Charlotte (118)
 DEMEULENAERE Dorothée (122)
 DERICUM Daniel (121)
 DOBBELSTEIN Dorothée (124)
 DOBBELSTEIN-DEMEULENAERE Dorothée (123)
 ERNST Berta (125)
 EVERTZ Bernd (126)
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
=========================
 Name
-------------------------
 AUSDEMWALD Alfons (116)
 EVERTZ Bernd (126)
=========================
<BLANKLINE>


