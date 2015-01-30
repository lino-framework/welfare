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
datetime.date(2015, 1, 25)



>>> rt.show(trainings.TrainingTypes)  #doctest: +SKIP
=============================
 Description
-----------------------------
 Immersion training (F70bis)
 Internal engagement
 MISIP
=============================
<BLANKLINE>

