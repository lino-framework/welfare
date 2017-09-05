.. _welfare.specs.xcourses:

================
External courses
================

.. to test only this document:

    $ doctest docs/specs/courses.rst
    
    doctest init:
    
    >>> from lino import startup
    >>> startup('lino_welfare.projects.eupen.settings.doctests')
    >>> from lino.api.doctest import *
    >>> ses = settings.SITE.login('rolf')


.. contents:: 
    :local:
    :depth: 1


This is about *external* courses
:mod:`lino_welfare.modlib.xcourses.models` (not :doc:`courses2`).

>>> rt.models.xcourses.__name__
'lino_welfare.modlib.xcourses.models'

Requesting for JSON data
========================

>>> json_fields = 'count rows title success no_data_text param_values'
>>> kw = dict(fmt='json', limit=10, start=0)
>>> demo_get('rolf', 'api/xcourses/CourseProviders', json_fields, 2, **kw)

>>> json_fields = 'count rows title success no_data_text'
>>> demo_get('rolf', 'api/xcourses/CourseOffers', json_fields, 3, **kw)

>>> ContentType = rt.modules.contenttypes.ContentType
>>> json_fields = 'count rows title success no_data_text param_values'
>>> demo_get('rolf', 'api/xcourses/PendingCourseRequests', json_fields, 20, **kw)


Course providers
================

>>> ses.show(xcourses.CourseProviders)
======= ============ ================ ========= ===== ===== =========
 Name    Adresse      E-Mail-Adresse   Telefon   GSM   ID    Sprache
------- ------------ ---------------- --------- ----- ----- ---------
 KAP     4700 Eupen                                    231
 Oikos   4700 Eupen                                    230
======= ============ ================ ========= ===== ===== =========
<BLANKLINE>

Course offers
=============

>>> ses.show(xcourses.CourseOffers)
==== ========================= =========== ============= ============== ==============
 ID   Name                      Gastrolle   Kursinhalt    Kursanbieter   Beschreibung
---- ------------------------- ----------- ------------- -------------- --------------
 1    Deutsch für Anfänger                  Deutsch       Oikos
 2    Deutsch für Anfänger                  Deutsch       KAP
 3    Français pour débutants               Französisch   KAP
==== ========================= =========== ============= ============== ==============
<BLANKLINE>

>>> ses.show(xcourses.CourseRequests)  #doctest: +ELLIPSIS
==== ============================= ============= ============= ============== ============================== ========= =============== =========== ==========
 ID   Klient                        Kursangebot   Kursinhalt    Anfragedatum   professionelle Eingliederung   Zustand   Kurs gefunden   Bemerkung   Enddatum
---- ----------------------------- ------------- ------------- -------------- ------------------------------ --------- --------------- ----------- ----------
 20   RADERMACHER Edgard (157)                    Französisch   14.04.14       Nein                           Offen
 19   RADERMACHER Christian (155)                 Deutsch       16.04.14       Nein                           Offen
 18   RADERMACHER Alfons (153)                    Französisch   18.04.14       Nein                           Offen
 ...
 2    COLLARD Charlotte (118)                     Französisch   20.05.14       Nein                           Offen
 1    AUSDEMWALD Alfons (116)                     Deutsch       22.05.14       Nein                           Offen
==== ============================= ============= ============= ============== ============================== ========= =============== =========== ==========
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

>>> ses.show(xcourses.PendingCourseRequests,
...      column_names="personX content urgent address person.coachings")
Traceback (most recent call last):
  ...
Exception: lino.core.layouts.ColumnsLayout on lino_welfare.modlib.xcourses.models.PendingCourseRequests has no data element 'personX'


>>> ses.show(xcourses.PendingCourseRequests,
...      column_names="person__foo content urgent address person.coachings")
Traceback (most recent call last):
  ...
Exception: lino.core.layouts.ColumnsLayout on lino_welfare.modlib.xcourses.models.PendingCourseRequests has no data element 'person__foo (Invalid RemoteField pcsw.Client.person__foo (no field foo in pcsw.Client))'


>>> ses.show(xcourses.PendingCourseRequests,
...      column_names="person content urgent address person__foo")
Traceback (most recent call last):
  ...
Exception: lino.core.layouts.ColumnsLayout on lino_welfare.modlib.xcourses.models.PendingCourseRequests has no data element 'person__foo (Invalid RemoteField pcsw.Client.person__foo (no field foo in pcsw.Client))'

>>> settings.SITE.catch_layout_exceptions = False
>>> ses.show(xcourses.PendingCourseRequests,
...      column_names="person content urgent address person__foo")
Traceback (most recent call last):
  ...
Exception: Invalid RemoteField pcsw.Client.person__foo (no field foo in pcsw.Client)


Changed since 20130422
======================

Yes it was a nice feature to silently ignore non installed app_labels
but mistakenly specifying "person.first_name" instead of
"person__first_name" did not raise an error. Now it does:

>>> ses.show(xcourses.PendingCourseRequests,
...      column_names="person.first_name content urgent address")
Traceback (most recent call last):
  ...
Exception: lino.core.layouts.ColumnsLayout on lino_welfare.modlib.xcourses.models.PendingCourseRequests has no data element 'person.first_name'

And then the following example failed because Lino simply wasn't yet 
able to render RemoteFields as rst.

>>> with translation.override('fr'):
...    ses.show(xcourses.PendingCourseRequests, limit=5,
...       column_names="person__first_name content urgent address")
=========== ============= ======================= =================================
 Prénom      Contenu       cause professionnelle   Adresse
----------- ------------- ----------------------- ---------------------------------
 Edgard      Französisch   Non                     4730 Raeren
 Christian   Deutsch       Non                     4730 Raeren
 Alfons      Französisch   Non                     4730 Raeren
 Erna        Deutsch       Non                     4730 Raeren
 Melissa     Französisch   Non                     Herbesthaler Straße, 4700 Eupen
=========== ============= ======================= =================================
<BLANKLINE>

The virtual field `dsbe.Client.coachings` shows all active coachings
of a client:

>>> with translation.override('fr'):
...    ses.show(xcourses.PendingCourseRequests,limit=5,
...      column_names="person content person__coaches")
============================= ============= ==================================================
 Bénéficiaire                  Contenu       Intervenants
----------------------------- ------------- --------------------------------------------------
 RADERMACHER Edgard (157)      Französisch   Hubert Huppertz, Mélanie Mélard, Alicia Allmanns
 RADERMACHER Christian (155)   Deutsch       Caroline Carnol, Mélanie Mélard
 RADERMACHER Alfons (153)      Französisch   Mélanie Mélard
 EMONTS-GAST Erna (152)        Deutsch       Alicia Allmanns, Hubert Huppertz
 MEESSEN Melissa (147)         Französisch   Hubert Huppertz, Mélanie Mélard
============================= ============= ==================================================
<BLANKLINE>

The last column `coachings` ("Interventants") is also a new feature:
it is a RemoteField pointing to a VirtualField. 

