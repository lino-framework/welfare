.. _welfare.tested.trainings:

===================
Immersion trainings
===================

.. How to test only this document:

  $ python setup.py test -s tests.DocsTests.test_trainings

A technical tour into the :mod:`lino_welfare.modlib.trainings` plugin.


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
    
This documents uses the :mod:`lino_welfare.projects.eupen` test
database:

>>> print(settings.SETTINGS_MODULE)
lino_welfare.projects.chatelet.settings.doctests

>>> dd.today()
datetime.date(2014, 5, 22)


Configuration
=============

>>> rt.show(trainings.TrainingTypes)  #doctest: -SKIP
=====================
 Description
---------------------
 Immersion training
 Internal engagement
 MISIP
=====================
<BLANKLINE>


Demo data
=========

:class:`lino_welfare.modlib.isip.models.ExamPolicy`

>>> rt.show(trainings.Trainings)
==== ========================== ================== ============ =================== =========================
 ID   Bénéficiaire               Début de contrat   Fin prévue   Responsable (SSG)   Immersion training type
---- -------------------------- ------------------ ------------ ------------------- -------------------------
 1    GROTECLAES Gregory (131)   22/05/2014         21/07/2014   Alicia Allmanns     Immersion training
 2    EMONTS Erich (149)         21/06/2014         19/10/2014   Alicia Allmanns     Internal engagement
 3    RADERMACHER Inge (161)     21/07/2014         17/01/2015   Alicia Allmanns     MISIP
==== ========================== ================== ============ =================== =========================
<BLANKLINE>
