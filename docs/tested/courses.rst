.. _welfare.tested.courses:

Courses
=======

.. include:: /include/tested.rst

.. 
  >>> from lino.runtime import *

>>> ses = settings.SITE.login('rolf')
>>> ses.set_language('fr')

catch_layout_exceptions
-----------------------

Some general documentation about `catch_layout_exceptions`. 
This should rather be somewhere in the general Lino documentation, 
probably in :ref:`layouts_tutorial`,
but this document isn't yet tested, so we do it here.

This setting tells Lino what to do when
it encounters a wrong fieldname in a layout specification.
It will anyway raise an Exception, but the difference is 
is the content of the error message.

The default value for this setting is True.
In that case the error message reports only a summary of the 
original exception and tells you in which layout it happens.
Because that's your application code and probably the place where
the bug is hidden.

For example:

>>> ses.show(courses.PendingCourseRequests,limit=5,
...      column_names="personX content urgent address person.coachings")
Traceback (most recent call last):
  ...
KeyError: "Unknown element 'personX' referred in layout <ListLayout on courses.PendingCourseRequests>."

>>> ses.show(courses.PendingCourseRequests,limit=5,
...      column_names="person__foo content urgent address person.coachings")
Traceback (most recent call last):
  ...
KeyError: "Unknown element 'person__foo (Invalid RemoteField pcsw.Client.person__foo (no field foo in pcsw.Client))' referred in layout <ListLayout on courses.PendingCourseRequests>."


>>> ses.show(courses.PendingCourseRequests,
...      column_names="person content urgent address person__foo")
Traceback (most recent call last):
  ...
KeyError: "Unknown element 'person__foo (Invalid RemoteField pcsw.Client.person__foo (no field foo in pcsw.Client))' referred in layout <ListLayout on courses.PendingCourseRequests>."

>>> settings.SITE.catch_layout_exceptions = False
>>> ses.show(courses.PendingCourseRequests,
...      column_names="person content urgent address person__foo")
Traceback (most recent call last):
  ...
Exception: Invalid RemoteField pcsw.Client.person__foo (no field foo in pcsw.Client)


Changed since 20130422
----------------------

Yes it was a nice feature to silently ignore non installed app_labels
but mistakenly specifying "person.first_name" instead of "person__first_name"
did not raise an error. Now it does:

>>> ses.show(courses.PendingCourseRequests,limit=5,
...      column_names="person.first_name content urgent address")
Traceback (most recent call last):
  ...
KeyError: "Unknown element 'person.first_name' referred in layout <ListLayout on courses.PendingCourseRequests>."


And then the following example failed because Lino simply wasn't yet 
able to render RemoteFields as rst.

>>> ses.show(courses.PendingCourseRequests,limit=5,
...      column_names="person__first_name content urgent address")
========= ============= ======================= =====================
 Prénom    Contenu       cause professionnelle   Address
--------- ------------- ----------------------- ---------------------
 Emil      Französisch   Non                     Allemagne
 Rik       Deutsch       Non                     Amsterdam, Pays-Bas
 Otto      Französisch   Non                     4730 Raeren
 Vincent   Deutsch       Non                     4730 Raeren
 Didier    Französisch   Non                     4730 Raeren
========= ============= ======================= =====================
<BLANKLINE>

New virtualfield `dsbe.Client.coachings` shows all active coachings
of that client:

>>> ses.show(courses.PendingCourseRequests,limit=5,
...      column_names="person content address person__coaches")
======================== ============= ===================== ==================================================
 Client                   Contenu       Address               Accompagnants
------------------------ ------------- --------------------- --------------------------------------------------
 EIERSCHAL Emil (175)     Französisch   Allemagne             Hubert Huppertz
 RADERMECKER Rik (173)    Deutsch       Amsterdam, Pays-Bas   Alicia Allmanns
 ÖSTGES Otto (168)        Französisch   4730 Raeren           Mélanie Mélard
 VAN VEEN Vincent (166)   Deutsch       4730 Raeren           Hubert Huppertz, Mélanie Mélard, Caroline Carnol
 DI RUPO Didier (164)     Französisch   4730 Raeren           Hubert Huppertz, Alicia Allmanns
======================== ============= ===================== ==================================================
<BLANKLINE>

The last column `coachings` (Accompagnements) is also a new feature:
it is a RemoteField ponting to a VirtualField. Very subtle!

