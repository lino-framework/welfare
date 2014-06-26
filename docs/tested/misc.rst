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
    >>> from lino import dd


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


>>> ses = settings.SITE.login('rolf')
>>> with translation.override('de'):
...     ses.show(jobs.Jobs,column_names="function provider sector") #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
================= ====================================== ===========================
 Funktion          Stellenanbieter                        Sektor
----------------- -------------------------------------- ---------------------------
 Koch              R-Cycle Sperrgutsortierzentrum (226)    Seefahrt
 Koch              Pro Aktiv V.o.G. (228)                  Unterricht
 Küchenassistent   Pro Aktiv V.o.G. (228)                  Medizin & Paramedizin
 Küchenassistent   BISA (225)                              Reinigung
 Tellerwäscher     BISA (225)                              Bauwesen & Gebäudepflege
 Tellerwäscher     R-Cycle Sperrgutsortierzentrum (226)    Transport
 Kellner           BISA (225)                              Landwirtschaft & Garten
 Kellner           R-Cycle Sperrgutsortierzentrum (226)    Horeca
================= ====================================== ===========================
<BLANKLINE>


JobsOverview
------------

Printing the document 
:ref:`welfare.jobs.JobsOverview`
caused a "NotImplementedError: <i> inside <text:p>" traceback 
when one of the jobs had a remark. 

>>> obj = ses.spawn(jobs.JobsOverview).create_instance()
>>> print(ses.run(obj.do_print)) 
... #doctest: +NORMALIZE_WHITESPACE +ELLIPSIS
{'open_url': u'...jobs.JobsOverview.pdf',
 'success': True}
 
Bug fixed :blogref:`20130423`.


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
==== ====================== ========================================
 ID   Excerpt Type           Controlled by
---- ---------------------- ----------------------------------------
 1    Budget                 **Budget 1 for Jeanémart-Lahm (181)**
 2    Art.60§7 contract      **Art.60§7 contract#1 (Bernd Brecht)**
 3    ISIP                   **ISIP#1 (Alfons Ausdemwald)**
 4    Aid certificate        **Aid #1**
 5    Presence certificate   **Guest #1 (22.05.2014)**
 6    Curriculum vitae       **AUSDEMWALD Alfons (115)**
 7    eID sheet              **AUSDEMWALD Alfons (115)**
 8    to-do list             **AUSDEMWALD Alfons (115)**
==== ====================== ========================================
<BLANKLINE>

>>> import shutil
>>> obj = excerpts.Excerpt.objects.get(pk=3)
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
:srcref:`/docs/tested/isip.Contract-1.pdf`

Now the same in more generic. We write a formatter function and then
call it on every excerpt. See the source code of this page if you want
to see how we generated the following list:

.. django2rst::

    import os
    import shutil
    from atelier import rstgen
    ses = dd.login()
    def asli(obj):
        rv = ses.run(obj.do_print)
        tmppath = settings.SITE.project_dir + rv['open_url']
        head, tail = os.path.split(tmppath)
        tail = 'tested/' + tail
        try:
            shutil.copyfile(tmppath, tail)
        except IOError:
            pass
        kw = dict(tail=tail)
        # kw.update(text="**%s** (%s)" % (obj.owner, obj.excerpt_type))
        kw.update(type=obj.excerpt_type)
        kw.update(owner=obj.owner)
        return "%(type)s :srcref:`%(owner)s <docs/%(tail)s>`" % kw
    
    print(rstgen.ul([asli(o) for o in excerpts.Excerpt.objects.all()]))
   

