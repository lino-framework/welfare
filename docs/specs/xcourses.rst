.. doctest docs/specs/xcourses.rst
.. _welfare.specs.xcourses:

================
External courses
================

.. doctest init:

    >>> from lino import startup
    >>> startup('lino_welfare.projects.gerd.settings.doctests')
    >>> from lino.api.doctest import *
    >>> ses = settings.SITE.login('rolf')


.. contents::
    :local:
    :depth: 1


This is about *external* courses
:mod:`lino_welfare.modlib.xcourses.models` (not :mod:`lino_welfare.modlib.courses`).

>>> rt.models.xcourses.__name__
'lino_welfare.modlib.xcourses.models'

Requesting for JSON data
========================

>>> json_fields = 'count rows title success no_data_text param_values'
>>> kw = dict(fmt='json', limit=10, start=0)
>>> demo_get('rolf', 'api/xcourses/CourseProviders', json_fields, 3, **kw)

>>> json_fields = 'count rows title success no_data_text'
>>> demo_get('rolf', 'api/xcourses/CourseOffers', json_fields, 4, **kw)

>>> ContentType = rt.models.contenttypes.ContentType
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



Changed 20130422
================

The following example failed because Lino simply wasn't yet
able to render RemoteFields as rst.

>>> with translation.override('fr'):
...    ses.show(xcourses.PendingCourseRequests, limit=5,
...       column_names="person__first_name content urgent address")
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
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
