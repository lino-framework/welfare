.. _welfare.tested.notes:

=============
Notes
=============

.. How to test only this document:

    $ python setup.py test -s tests.DocsTests.test_notes

    doctest init:

    >>> from __future__ import print_function
    >>> import os
    >>> os.environ['DJANGO_SETTINGS_MODULE'] = \
    ...    'lino_welfare.projects.std.settings.doctests'
    >>> from lino.api.doctest import *

.. contents:: 
   :local:
   :depth: 2


Permalink to the detail of a note type
======================================

>>> url = '/api/notes/NoteTypes/1?fmt=detail'
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
>>> fm = rt.modules.notes.NoteType.objects.get(**flt)
>>> ses = rt.login('rolf')
>>> ses.show(notes.NotesByType, fm, column_names="id project")
===== =========================================
 ID    Klient
----- -----------------------------------------
 19    DOBBELSTEIN Dorothée (124)
 30    DOBBELSTEIN-DEMEULENAERE Dorothée (123)
 41    AUSDEMWALD Alfons (116)
 52    BASTIAENSEN Laurent (117)
 63    BRECHT Bernd (177)
 74    CHANTRAINE Marc (120*)
 85    COLLARD Charlotte (118)
 96    DEMEULENAERE Dorothée (122)
 107   DENON Denis (180*)
===== =========================================
<BLANKLINE>

Client 124 has a first meeting, while client 125 doesn't:

>>> rt.modules.pcsw.Client.objects.get(pk=124).get_first_meeting()
Note #19 (u'Ereignis/Notiz #19')
>>> rt.modules.pcsw.Client.objects.get(pk=125).get_first_meeting()


