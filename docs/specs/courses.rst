.. _welfare.specs.courses:

================
External courses
================

.. to test only this document:

    $ python setup.py test -s tests.SpecsTests.test_courses
    
    doctest init:
    
    >>> from lino import startup
    >>> startup('lino_welfare.projects.std.settings.doctests')
    >>> from lino.api.doctest import *
    >>> ses = settings.SITE.login('rolf')


.. contents:: 
    :local:
    :depth: 1


This is about *external* courses
:mod:`lino_welfare.modlib.courses.models` (not :doc:`courses2`).

>>> rt.models.courses.__name__
'lino_welfare.modlib.courses.models'

Requesting for JSON data
========================

>>> json_fields = 'count rows title success no_data_text param_values'
>>> kw = dict(fmt='json', limit=10, start=0)
>>> demo_get('rolf', 'api/courses/CourseProviders', json_fields, 3, **kw)

>>> json_fields = 'count rows title success no_data_text'
>>> demo_get('rolf', 'api/courses/CourseOffers', json_fields, 4, **kw)

>>> ContentType = rt.modules.contenttypes.ContentType
>>> json_fields = 'count rows title success no_data_text param_values'
>>> demo_get('rolf', 'api/courses/PendingCourseRequests', json_fields, 19, **kw)


Course providers
================

>>> ses.show(courses.CourseProviders)
======= ============ ======== ========= ===== ===== =========
 Name    Adresse      E-Mail   Telefon   GSM   ID    Sprache
------- ------------ -------- --------- ----- ----- ---------
 KAP     4700 Eupen                            231
 Oikos   4700 Eupen                            230
======= ============ ======== ========= ===== ===== =========
<BLANKLINE>

Course offers
=============

>>> ses.show(courses.CourseOffers)
==== ========================= =========== ============= ============== =============
 ID   Name                      Gastrolle   Kursinhalt    Kursanbieter   description
---- ------------------------- ----------- ------------- -------------- -------------
 1    Deutsch für Anfänger                  Deutsch       Oikos
 2    Deutsch für Anfänger                  Deutsch       KAP
 3    Français pour débutants               Französisch   KAP
==== ========================= =========== ============= ============== =============
<BLANKLINE>

>>> ses.show(courses.CourseRequests)  #doctest: +ELLIPSIS
==== ============================ ============= ============= ============== ============================== ========= =============== =========== ==========
 ID   Klient                       Kursangebot   Kursinhalt    Anfragedatum   professionelle Eingliederung   Zustand   Kurs gefunden   Bemerkung   Enddatum
---- ---------------------------- ------------- ------------- -------------- ------------------------------ --------- --------------- ----------- ----------
 20   LAZARUS Line (144)                         Französisch   14.04.14       Nein                           Offen
 19   LAMBERTZ Guido (142)                       Deutsch       16.04.14       Nein                           Offen
 18   KELLER Karl (178)                          Französisch   18.04.14       Nein                           Offen
 ...
 2    BRECHT Bernd (177)                         Französisch   20.05.14       Nein                           Offen
 1    AUSDEMWALD Alfons (116)                    Deutsch       22.05.14       Nein                           Offen
==== ============================ ============= ============= ============== ============================== ========= =============== =========== ==========
<BLANKLINE>



catch_layout_exceptions
=======================

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
======================

Yes it was a nice feature to silently ignore non installed app_labels
but mistakenly specifying "person.first_name" instead of
"person__first_name" did not raise an error. Now it does:

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

