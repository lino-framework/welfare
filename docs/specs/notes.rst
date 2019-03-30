.. doctest docs/specs/notes.rst
.. _welfare.specs.notes:

=============
Notes
=============

.. contents:: 
   :local:
   :depth: 2

.. include:: /../docs/shared/include/tested.rst
             
>>> from lino import startup
>>> startup('lino_welfare.projects.gerd.settings.doctests')
>>> from lino.api.doctest import *
>>> translation.activate("en")


Permalink to the detail of a note type
======================================

>>> url = '/api/notes/NoteTypes/1?fmt=detail'
>>> test_client.force_login(rt.login('rolf').user)
>>> res = test_client.get(url, REMOTE_USER='rolf')
>>> print(res.status_code)
200

We test whether a normal HTML response arrived:

>> print(res.content)  #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
<!DOCTYPE html ...
Lino.notes.NoteTypes.detail.run(null,{ "record_id": "1", "base_params": {  } })
...</body>
</html>


The first meeting
=================

We can use the :meth:`lino_welfare.modlib.pcsw.Client.get_first_meeting`
method for getting the last note about a given client and of given
type.

>>> from django.utils.translation import ugettext_lazy as _
>>> flt = dd.str2kw("name", _("First meeting"))
>>> fm = rt.models.notes.NoteType.objects.get(**flt)
>>> ses = rt.login('rolf')
>>> ses.show(notes.NotesByType, fm, column_names="id project")
===== =========================================
 ID    Klient
----- -----------------------------------------
 19    ERNST Berta (125)
 30    EVERTZ Bernd (126)
 41    AUSDEMWALD Alfons (116)
 52    BASTIAENSEN Laurent (117)
 63    COLLARD Charlotte (118)
 74    CHANTRAINE Marc (120*)
 85    DERICUM Daniel (121)
 96    DEMEULENAERE Dorothée (122)
 107   DOBBELSTEIN-DEMEULENAERE Dorothée (123)
===== =========================================
<BLANKLINE>


Client 125 has a first meeting, while client 124 doesn't:

>>> rt.models.pcsw.Client.objects.get(pk=125).get_first_meeting()
Note #19 ('Ereignis/Notiz #19')
>>> rt.models.pcsw.Client.objects.get(pk=124).get_first_meeting()


