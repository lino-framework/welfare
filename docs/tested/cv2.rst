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

>>> rt.login('robin').show(cv.TrainingTypes)
==== =============== ================== ==================
 ID   Designation     Designation (fr)   Designation (de)
---- --------------- ------------------ ------------------
 3    Alpha           Alpha              Alpha
 1    Prequalifying   Préqualification   Prequalifying
 2    Qualifying      Qualification      Qualifying
==== =============== ================== ==================
<BLANKLINE>

>>> rt.login('robin').show(cv.EducationLevels)
============= ================== ==================
 Designation   Designation (fr)   Designation (de)
------------- ------------------ ------------------
 Bachelor      Bachelor           Bachelor
 Higher        Supérieur          Hochschule
 Master        Master             Master
 Primary       Primaire           Primär
 Secondary     Secondaire         Sekundär
============= ================== ==================
<BLANKLINE>

And the list of Study types:

>>> rt.login('robin').show(cv.StudyTypes)
==== ================= ======================= ==================== =================
 ID   Designation       Designation (fr)        Designation (de)     Education Level
---- ----------------- ----------------------- -------------------- -----------------
 4    Apprenticeship    Apprentissage           Lehre
 5    Highschool        École supérieure        Hochschule
 7    Part-time study   Cours à temps partiel   Teilzeitunterricht
 8    Remote study      Cours à distance        Fernkurs
 1    School            École                   Schule
 2    Special school    École spéciale          Sonderschule
 3    Training          Formation               Ausbildung
 6    University        Université              Universität
==== ================= ======================= ==================== =================
<BLANKLINE>

