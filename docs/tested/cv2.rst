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
datetime.date(2015, 1, 25)


Configuration data
========================

This is the list of training types:

>>> rt.login('romain').show(cv.TrainingTypes)
==== ==================
 ID   Description
---- ------------------
 3    Alpha
 1    Préqualification
 2    Qualification
==== ==================
<BLANKLINE>

>>> rt.login('romain').show(cv.EducationLevels)
=============
 Description
-------------
 Bachelor
 Master
 Primaire
 Secondaire
 Supérieur
=============
<BLANKLINE>

And the list of Study types:

>>> rt.login('romain').show(cv.StudyTypes)
==== ======================= ===================
 ID   Description             Niveau académique
---- ----------------------- -------------------
 4    Apprentissage
 8    Cours à distance
 7    Cours à temps partiel
 3    Formation
 6    Université
 1    École
 2    École spéciale
 5    École supérieure
==== ======================= ===================
<BLANKLINE>

