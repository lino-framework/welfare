.. _welfare.specs.courses2:

================
Internal courses
================

.. to test only this document:

    $ python setup.py test -s tests.SpecsTests.test_courses2
    
    doctest init:
    
    >>> from lino import startup
    >>> startup('lino_welfare.projects.chatelet.settings.doctests')
    >>> from lino.api.doctest import *


.. contents:: 
    :local:
    :depth: 1


This is about *internal* courses
(:mod:`lino_welfare.projects.chatelet.modlib.courses.models`), not
:doc:`courses`.

>>> rt.modules.courses.__name__
'lino_welfare.projects.chatelet.modlib.courses.models'


>>> rt.show(courses.Courses)
============ ======================= ============================ ============= ======= ===============
 Date début   Inscriptions jusqu'au   Série d'ateliers             Instructeur   Local   État
------------ ----------------------- ---------------------------- ------------- ------- ---------------
 12/05/2014                           Cuisine                                            **Brouillon**
 12/05/2014                           Créativité                                         **Brouillon**
 12/05/2014                           Notre premier bébé                                 **Brouillon**
 12/05/2014                           Mathématiques                                      **Brouillon**
 12/05/2014                           Français                                           **Brouillon**
 12/05/2014                           Activons-nous!                                     **Brouillon**
 03/11/2013                           Psycho-social intervention                         **Brouillon**
============ ======================= ============================ ============= ======= ===============
<BLANKLINE>

>>> print(rt.modules.courses.Courses.params_layout.main)
topic line teacher state can_enroll:10     start_date end_date

>>> demo_get('robin', 'choices/courses/Courses/topic', 'count rows', 0)
>>> demo_get('robin', 'choices/courses/Courses/teacher', 'count rows', 102)
>>> demo_get('robin', 'choices/courses/Courses/user', 'count rows', 11)


Yes, the demo database has no topics defined:

>>> rt.show(courses.Topics)
No data to display


