.. _welfare.tested.misc:

Miscellaneous
=============

.. include:: /include/tested.rst

Some tests:
  
>>> from __future__ import print_function
>>> from lino.runtime import *
>>> from django.utils import translation
>>> from django.test import Client
>>> import json
>>> from lino import dd



A web request
-------------


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
 Koch              R-Cycle Sperrgutsortierzentrum (191)    Seefahrt
 Koch              Pro Aktiv V.o.G. (193)                  Unterricht
 Küchenassistent   Pro Aktiv V.o.G. (193)                  Medizin & Paramedizin
 Küchenassistent   BISA (190*)                             Reinigung
 Tellerwäscher     BISA (190*)                             Bauwesen & Gebäudepflege
 Tellerwäscher     R-Cycle Sperrgutsortierzentrum (191)    Transport
 Kellner           BISA (190*)                             Landwirtschaft & Garten
 Kellner           R-Cycle Sperrgutsortierzentrum (191)    Horeca
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
... #doctest: +NORMALIZE_WHITESPACE
{'open_url': u'/media/webdav/userdocs/appyodt/jobs.JobsOverview.odt',
 'success': True}
 
Bug fixed :blogref:`20130423`.


.. _welfare.tested.cal:

Calendars and Subscriptions
---------------------------

A Calendar is a set of events that can be shown or hidden in the Calendar Panel.

In Lino Welfare, we have one Calendar per User.

Or to be more precise: the Calendar of an event is automatically
defined by the :ddref:`cal.Event.user` field.

For example, demo user `rolf` is automatically subscribed to the following calendars:

>>> with translation.override('de'):
...    ses.show(cal.SubscriptionsByUser, ses.get_user()) #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
==== ================= ===========
 ID   Kalender          versteckt
---- ----------------- -----------
 5    Rolf Rompen       Nein
 6    Romain Raffault   Nein
 8    Robin Rood        Nein
 14   Mélanie Mélard    Nein
 23   Hubert Huppertz   Nein
 34   Alicia Allmanns   Nein
 47   Caroline Carnol   Nein
 62   Judith Jousten    Nein
 79   Kerstin Kerres    Nein
==== ================= ===========
<BLANKLINE>

This rule is application-specific. All users with one of the following
profiles can see each other's calendars:

>>> from lino.utils import rstgen
>>> print(rstgen.ul([unicode(p) for p in dd.UserProfiles.items() if p.coaching_level]))
- Begleiter im DSBE
- Integrations-Assistent (Manager)
- Berater Neuanträge
- Schuldenberater
- Sozi
- Social agent (Manager)
- Verwalter
<BLANKLINE>


