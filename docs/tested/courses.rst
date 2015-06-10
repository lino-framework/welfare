.. _welfare.tested.courses:

Courses
=======

.. include:: /include/tested.rst

.. to test only this document:
  $ python setup.py test -s tests.DocsTests.test_courses

.. 
  >>> from django.utils import translation
  >>> from lino.api.shell import *

>>> ses = settings.SITE.login('rolf')

catch_layout_exceptions
-----------------------

Some general documentation about `catch_layout_exceptions`. 
This should rather be somewhere in the general Lino documentation, 
probably in :ref:`layouts_tutorial`,
but this document isn't yet tested, so we do it here.

This setting tells Lino what to do when it encounters a wrong
fieldname in a layout specification.  It will anyway raise an
Exception, but the difference is is the content of the error message.

The default value for this setting is True.
In that case the error message reports only a summary of the 
original exception and tells you in which layout it happens.
Because that's your application code and probably the place where
the bug is hidden.

For example:

>>> ses.show(courses.PendingCourseRequests,
...      column_names="personX content urgent address person.coachings")
Traceback (most recent call last):
  ...
Exception: ColumnsLayout on courses.PendingCourseRequests has no data element 'personX'


>>> ses.show(courses.PendingCourseRequests,
...      column_names="person__foo content urgent address person.coachings")
Traceback (most recent call last):
  ...
Exception: ColumnsLayout on courses.PendingCourseRequests has no data element 'person__foo (Invalid RemoteField pcsw.Client.person__foo (no field foo in pcsw.Client))'


>>> ses.show(courses.PendingCourseRequests,
...      column_names="person content urgent address person__foo")
Traceback (most recent call last):
  ...
Exception: ColumnsLayout on courses.PendingCourseRequests has no data element 'person__foo (Invalid RemoteField pcsw.Client.person__foo (no field foo in pcsw.Client))'

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

>>> ses.show(courses.PendingCourseRequests,
...      column_names="person.first_name content urgent address")
Traceback (most recent call last):
  ...
Exception: ColumnsLayout on courses.PendingCourseRequests has no data element 'person.first_name'

And then the following example failed because Lino simply wasn't yet 
able to render RemoteFields as rst.

>>> with translation.override('fr'):
...    ses.show(courses.PendingCourseRequests, limit=5,
...       column_names="person__first_name content urgent address")
======== ============= ======================= ===========================
 Prénom   Contenu       cause professionnelle   Adresse
-------- ------------- ----------------------- ---------------------------
 Line     Französisch   Non                     Heidberg, 4700 Eupen
 Guido    Deutsch       Non                     Haasstraße, 4700 Eupen
 Karl     Französisch   Non                     Allemagne
 Karl     Deutsch       Non                     Haasberg, 4700 Eupen
 Josef    Französisch   Non                     Gülcherstraße, 4700 Eupen
======== ============= ======================= ===========================
<BLANKLINE>

The virtual field `dsbe.Client.coachings` shows all active coachings
of a client:

>>> with translation.override('fr'):
...    ses.show(courses.PendingCourseRequests,limit=5,
...      column_names="person content person__coaches")
====================== ============= =================================================
 Bénéficiaire           Contenu       Intervenants
---------------------- ------------- -------------------------------------------------
 LAZARUS Line (144)     Französisch   Mélanie Mélard, Hubert Huppertz, Mélanie Mélard
 LAMBERTZ Guido (142)   Deutsch       Mélanie Mélard, Hubert Huppertz
 KELLER Karl (178)      Französisch   Hubert Huppertz
 KAIVERS Karl (141)     Deutsch       Mélanie Mélard, Alicia Allmanns
 JONAS Josef (139)      Französisch   Caroline Carnol, Hubert Huppertz
====================== ============= =================================================
<BLANKLINE>

The last column `coachings` ("Interventants") is also a new feature:
it is a RemoteField pointing to a VirtualField. 

