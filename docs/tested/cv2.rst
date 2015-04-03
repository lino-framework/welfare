.. _welfare.tested.cv2:

==================
CV's (new version)
==================

.. How to test only this document:

  $ python setup.py test -s tests.DocsTests.test_cv2

A technical tour into the
:mod:`lino_welfare.projects.chatelet.modlib.cv` plugin.

Lino Welfare extends the standard :mod:`lino.modlib.uploads` plugin
into a system which helps social agents to manage certain documents
about their clients. For example, integration agents want to get a
reminder when the driving license of one of their client is going to
expire.

.. contents::
   :depth: 2

About this document
===================

.. include:: /include/tested.rst

>>> from __future__ import print_function
>>> import os
>>> os.environ['DJANGO_SETTINGS_MODULE'] = \
...    'lino_welfare.projects.chatelet.settings.doctests'
>>> from lino.api.doctest import *
    
This documents uses the :mod:`lino_welfare.projects.chatelet` test
database:

>>> print(settings.SETTINGS_MODULE)
lino_welfare.projects.chatelet.settings.doctests

>>> dd.today()
datetime.date(2014, 5, 22)


Configuration data
========================

This is the list of training types:

>>> rt.login('robin').show(cv.EducationLevels)
==================== ================== ================== ======= ==========
 Designation          Designation (fr)   Designation (de)   Study   Training
-------------------- ------------------ ------------------ ------- ----------
 Bachelor             Bachelor           Bachelor           Yes     No
 Higher               Supérieur          Hochschule         Yes     No
 Master               Master             Master             Yes     No
 Primary              Primaire           Primär             Yes     No
 Secondary            Secondaire         Sekundär           Yes     No
 **Total (5 rows)**                                         **5**   **0**
==================== ================== ================== ======= ==========
<BLANKLINE>

And the list of Study types:

>>> rt.login('robin').show(cv.StudyTypes)
======= ================= ======================= ==================== ======= ========== =================
 ID      Designation       Designation (fr)        Designation (de)     Study   Training   Education Level
------- ----------------- ----------------------- -------------------- ------- ---------- -----------------
 11      Alpha             Alpha                   Alpha                No      Yes
 4       Apprenticeship    Apprentissage           Lehre                Yes     No
 5       Highschool        École supérieure        Hochschule           Yes     No
 7       Part-time study   Cours à temps partiel   Teilzeitunterricht   Yes     No
 9       Prequalifying     Préqualification        Prequalifying        No      Yes
 10      Qualifying        Qualification           Qualifying           No      Yes
 8       Remote study      Cours à distance        Fernkurs             Yes     No
 1       School            École                   Schule               Yes     No
 2       Special school    École spéciale          Sonderschule         Yes     No
 3       Training          Formation               Ausbildung           Yes     No
 6       University        Université              Universität          Yes     No
 **0**                                                                  **8**   **3**
======= ================= ======================= ==================== ======= ========== =================
<BLANKLINE>


>>> for m, f in rt.modules.cv.StudyType._lino_ddh.fklist:
...     print dd.full_model_name(m), f.name
cv.Training type
cv.Study type
isip.Contract study_type

>>> kw = dict()
>>> fields = 'count rows'
>>> demo_get('rolf', 'choices/cv/Training/type', fields, 3, **kw)
>>> demo_get('rolf', 'choices/cv/Study/type', fields, 8, **kw)
>>> demo_get('rolf', 'choices/isip/Contract/study_type', fields, 11, **kw)
