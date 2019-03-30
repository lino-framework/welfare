.. doctest docs/specs/welfare/courses.rst
.. _welfare.specs.courses2:

=======================
``courses`` : Workshops
=======================

This is about *internal* courses (:mod:`lino_welcht.lib.courses`), not to mixed
up with :mod:`lino_welcht.lib.xcourses`.


.. contents:: 
    :local:
    :depth: 1

.. include:: /../docs/shared/include/tested.rst

>>> from lino import startup
>>> startup('lino_welfare.projects.mathieu.settings.doctests')
>>> from lino.api.doctest import *

>>> dd.plugins.courses
lino_welcht.lib.courses (extends_models=['Course', 'Line', 'Enrolment'])

We call them "workshops":

>>> with translation.override('en'):
...     print(dd.plugins.courses.verbose_name)
Workshops

>>> with translation.override('fr'):
...     print(dd.plugins.courses.verbose_name)
Ateliers


>>> rt.show(rt.models.courses.Activities)
============ ============= ============================= ============= ======= ===============
 Date début   Désignation   Série d'ateliers              Instructeur   Local   Workflow
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

>>> print(rt.models.courses.Courses.params_layout.main)
topic line user teacher state 
    room can_enroll:10 start_date end_date show_exposed

>>> demo_get('robin', 'choices/courses/Courses/topic', 'count rows', 0)
>>> demo_get('robin', 'choices/courses/Courses/teacher', 'count rows', 102)
>>> demo_get('robin', 'choices/courses/Courses/user', 'count rows', 12)

Yes, the demo database has no topics defined:

>>> rt.show(rt.models.courses.Topics)
No data to display


>>> course = rt.models.courses.Course.objects.get(pk=1)
>>> print(course)
Kitchen (12/05/2014)

>>> # rt.show(rt.models.cal.EntriesByController, course)
>>> ar = rt.models.cal.EntriesByController.request(master_instance=course)
>>> rt.show(ar)
========================== =================== ================= ======== =================
 When                       Short description   Managed by        No.      Workflow
-------------------------- ------------------- ----------------- -------- -----------------
 *Mon 16/06/2014 (08:00)*   5                   Hubert Huppertz   5        **? Suggested**
 *Mon 02/06/2014 (08:00)*   4                   Hubert Huppertz   4        **? Suggested**
 *Mon 26/05/2014 (08:00)*   3                   Hubert Huppertz   3        **? Suggested**
 *Mon 19/05/2014 (08:00)*   2                   Hubert Huppertz   2        **? Suggested**
 *Mon 12/05/2014 (08:00)*   1                   Hubert Huppertz   1        **? Suggested**
 **Total (5 rows)**                                               **15**
========================== =================== ================= ======== =================
<BLANKLINE>


>>> event = ar[4]
>>> print(event)
 1 (12.05.2014 08:00)

>>> rt.show(rt.models.cal.GuestsByEvent, event)
===================== ========= ============= ========
 Partner               Role      Workflow      Remark
--------------------- --------- ------------- --------
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
===================== ========= ============= ========
<BLANKLINE>



>>> with translation.override('fr'):
...   show_fields(rt.models.courses.Course, 'start_date end_date')
+---------------+--------------+------------------------------------------------------------+
| Internal name | Verbose name | Help text                                                  |
+===============+==============+============================================================+
| start_date    | Date début   | La date (de début) de la première rencontre à générer.     |
+---------------+--------------+------------------------------------------------------------+
| end_date      | Date de fin  | La date de fin de la première rencontre à générer.         |
|               |              | Laisser vide si les rencontres durent moins d'une journée. |
+---------------+--------------+------------------------------------------------------------+


Don't read on
=============

Verify that users can create new courses:

>>> url = '/api/courses/MyCourses?an=insert'
>>> response = test_client.get(url, REMOTE_USER='romain')
>>> response.status_code
200

