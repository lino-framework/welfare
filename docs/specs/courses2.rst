.. _welfare.specs.courses2:

================
Workshops
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

We call them "workshops":

>>> with translation.override('en'):
...     print(dd.plugins.courses.verbose_name)
Workshops

>>> with translation.override('fr'):
...     print(dd.plugins.courses.verbose_name)
Ateliers

>>> rt.show(rt.actors.courses.Activities)
============ ============= ============================= ============= ======= ===============
 Date début   Désignation   Série d'ateliers              Instructeur   Local   Actions
------------ ------------- ----------------------------- ------------- ------- ---------------
 12/05/2014                 Cuisine                                             **Brouillon**
 12/05/2014                 Créativité                                          **Brouillon**
 12/05/2014                 Notre premier bébé                                  **Brouillon**
 12/05/2014                 Mathématiques                                       **Brouillon**
 12/05/2014                 Français                                            **Brouillon**
 12/05/2014                 Activons-nous!                                      **Brouillon**
 03/11/2013                 Intervention psycho-sociale                         **Brouillon**
============ ============= ============================= ============= ======= ===============
<BLANKLINE>

>>> print(rt.actors.courses.Courses.params_layout.main)
topic line user teacher state 
    room can_enroll:10 start_date end_date show_active

>>> demo_get('robin', 'choices/courses/Courses/topic', 'count rows', 0)
>>> demo_get('robin', 'choices/courses/Courses/teacher', 'count rows', 102)
>>> demo_get('robin', 'choices/courses/Courses/user', 'count rows', 12)

Yes, the demo database has no topics defined:

>>> rt.show(rt.actors.courses.Topics)
No data to display


>>> course = rt.models.courses.Course.objects.get(pk=1)
>>> print(course)
Kitchen (12/05/2014)

>>> # rt.show(rt.actors.cal.EntriesByController, course)
>>> ar = rt.actors.cal.EntriesByController.request(master_instance=course)
>>> rt.show(ar)
============================ =================== ================= ============= ===============
 When                         Short description   Managed by        Assigned to   Actions
---------------------------- ------------------- ----------------- ------------- ---------------
 **Mon 12/05/2014 (08:00)**   1                   Hubert Huppertz                 **Suggested**
 **Mon 19/05/2014 (08:00)**   2                   Hubert Huppertz                 **Suggested**
 **Mon 26/05/2014 (08:00)**   3                   Hubert Huppertz                 **Suggested**
 **Mon 02/06/2014 (08:00)**   4                   Hubert Huppertz                 **Suggested**
 **Mon 16/06/2014 (08:00)**   5                   Hubert Huppertz                 **Suggested**
============================ =================== ================= ============= ===============
<BLANKLINE>

>>> event = ar[0]
>>> print(event)
 1 (12.05.2014 08:00)

>>> rt.show(rt.actors.cal.GuestsByEvent, event)
===================== ========= =============
 Partner               Role      Actions
--------------------- --------- -------------
 Bastiaensen Laurent   Visitor   **Invited**
 Denon Denis           Visitor   **Invited**
 Dericum Daniel        Visitor   **Invited**
 Emonts-Gast Erna      Visitor   **Invited**
 Faymonville Luc       Visitor   **Invited**
 Gernegroß Germaine    Visitor   **Invited**
 Jacobs Jacqueline     Visitor   **Invited**
 Jonas Josef           Visitor   **Invited**
 Kaivers Karl          Visitor   **Invited**
 Laschet Laura         Visitor   **Invited**
 Radermacher Hedi      Visitor   **Invited**
===================== ========= =============
<BLANKLINE>



