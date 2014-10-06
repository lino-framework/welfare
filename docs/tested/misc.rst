.. _welfare.tested.misc:

Miscellaneous
=============

.. include:: /include/tested.rst

..
  This document is part of the test suite.
  To test only this document, run::
    $ python setup.py test -s tests.DocsTests.test_misc

..  
    >>> from __future__ import print_function
    >>> from lino.runtime import *
    >>> from django.utils import translation
    >>> from django.test import Client
    >>> import json
    >>> import os


.. _welfare.tested.notes:

Notes
=======

>>> client = Client()
>>> url = '/api/notes/NoteTypes/1?fmt=detail'
>>> res = client.get(url, REMOTE_USER='rolf')
>>> print(res.status_code)
200

We test whether a normal HTML response arrived:

>>> print(res.content)  #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
<!DOCTYPE html
...
Lino.notes.NoteTypes.detail.run(null,{ "record_id": "1", "base_params": {  } })
...
<BLANKLINE>
</body>
</html>



Some database content
---------------------


>>> ses = rt.login('rolf')

.. _welfare.tested.cal:

Calendars and Subscriptions
---------------------------

A Calendar is a set of events that can be shown or hidden in the
Calendar Panel.

In Lino Welfare, we have one Calendar per User.  Or to be more
precise: 

- The :ddref:`users.User` model has a :ddref:`users.User.calendar`
  field.

- The calendar of an :ddref:`cal.Event` is indirectly defined by the
  Event's :ddref:`cal.Event.user` field.

Two users can share a common calendar.  This is possible when two
colleagues really work together when receiving visitors.

A Subscription is when a given user decides that she wants to see the
calendar of another user.

Every user is, by default, subscribed to her own calendar.
For example, demo user `rolf` is automatically subscribed to the
following calendars:

>>> with translation.override('de'):
...    ses.show(cal.SubscriptionsByUser, ses.get_user()) #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
==== ========== ===========
 ID   Kalender   versteckt
---- ---------- -----------
 7    rolf       Nein
==== ========== ===========
<BLANKLINE>

Each user who has view access to the calendar.
Only UserProfile with a non-empty `office_level` can see the calendar.
All users with one of the following profiles can see each other's calendars:

>>> print('\n'.join([unicode(p) for p in dd.UserProfiles.items() if p.coaching_level]))
Begleiter im DSBE
Integrations-Assistent (Manager)
Berater Neuanträge
Schuldenberater
Sozi
Social agent (Manager)
Verwalter



Rendering some more excerpts
----------------------------

The demo fixtures also generated some excerpts:

>>> with translation.override('en'):
...     ses.show(excerpts.Excerpts, column_names="id excerpt_type owner")
==== ====================== ===========================================
 ID   Excerpt Type           Controlled by
---- ---------------------- -------------------------------------------
 1    Income confirmation    **5/22/14/116/EiEi/1**
 2    Income confirmation    **5/22/14/116/EiEi/2**
 3    Income confirmation    **5/23/14/177/Ausländerbeihilfe/3**
 4    Income confirmation    **5/23/14/177/Ausländerbeihilfe/4**
 5    Income confirmation    **5/24/14/118/Feste Beihilfe/5**
 6    Income confirmation    **5/24/14/118/Feste Beihilfe/6**
 7    Simple confirmation    **5/25/14/180/Erstattung/1**
 8    Simple confirmation    **5/25/14/180/Erstattung/2**
 9    Simple confirmation    **5/26/14/124/Übernahmeschein/3**
 10   Simple confirmation    **5/26/14/124/Übernahmeschein/4**
 11   Refund confirmation    **5/27/14/179/AMK/1**
 12   Refund confirmation    **5/27/14/179/AMK/2**
 13   Refund confirmation    **5/28/14/128/AMK(DMH)/3**
 14   Refund confirmation    **5/28/14/128/AMK(DMH)/4**
 15   Simple confirmation    **5/29/14/152/Furniture/5**
 16   Simple confirmation    **5/29/14/152/Furniture/6**
 17   Simple confirmation    **5/30/14/129/Heating costs/7**
 18   Simple confirmation    **5/30/14/129/Heating costs/8**
 19   Simple confirmation    **5/31/14/127/Food bank/9**
 20   Simple confirmation    **5/31/14/127/Food bank/10**
 21   Budget                 **Budget 1 for Xhonneux-Kasennova (228)**
 22   Job contract           **Job contract#1 (Bernd Brecht)**
 23   ISIP                   **ISIP#1 (Alfons Ausdemwald)**
 24   Presence certificate   **Guest #1 (22.05.2014)**
 25   Curriculum vitae       **AUSDEMWALD Alfons (116)**
 26   eID sheet              **AUSDEMWALD Alfons (116)**
 27   to-do list             **AUSDEMWALD Alfons (116)**
==== ====================== ===========================================
<BLANKLINE>

>>> import shutil
>>> obj = excerpts.Excerpt.objects.get(pk=23)
>>> rv = ses.run(obj.do_print)
>>> print(rv['open_url'])  #doctest: +NORMALIZE_WHITESPACE
/media/cache/appypdf/isip.Contract-1.pdf
>>> print(rv['success'])
True

The above `.pdf` file has been generated to a temporary cache
directory of the developer's computer when this document had its last
test run. The following lines the copied the file to the docs tree
which is published together with the source code and thus publicly
visible:

>>> tmppath = settings.SITE.project_dir + rv['open_url']
>>> shutil.copyfile(tmppath, 'isip.Contract-1.pdf')

Link to this copy of the resulting file:
:welfare_srcref:`/docs/tested/isip.Contract-1.pdf`

.. 

    Now the same in more generic. We write a formatter function and then
    call it on every excerpt. See the source code of this page if you want
    to see how we generated the following list:


Editing document template of an excerpt
=======================================

Here we want to see what the `edit_template` action says, especially
when called on an excerpt where Lino has two possible locations.

(Note: the following test is the reason why `is_local_project_dir` is
`True` in `lino_welfare.projects.docs.settings.doctests`.)

>>> lcd = os.path.join(settings.SITE.project_dir, 'config')
>>> # rt.makedirs_if_missing(lcd)
>>> obj = excerpts.Excerpt.objects.get(pk=1)
>>> rv = ses.run(obj.edit_template)
>>> print(rv['info_message'])
...     #doctest: +NORMALIZE_WHITESPACE +ELLIPSIS
Gonna copy ...lino_welfare/config/excerpts/Default.odt to $(PRJ)/config/excerpts/Default.odt
>>> print(rv['message'])
...     #doctest: +NORMALIZE_WHITESPACE
Before you can edit this template we must create a local copy on the server. This will exclude the template from future updates.
Sind Sie sicher?

