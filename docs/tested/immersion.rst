.. _welfare.tested.immersion:

===================
Immersion trainings
===================

.. How to test only this document:

  $ python setup.py test -s tests.DocsTests.test_immersion

A technical tour into the :mod:`lino_welfare.modlib.immersion` plugin.


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

These are the training types defined in
:mod:`lino_welfare.modlib.immersion.fixtures.std`:

>>> rt.show(immersion.ContractTypes)  #doctest: -SKIP
===================== =========================== =====================
 Designation           Designation (fr)            Designation (de)
--------------------- --------------------------- ---------------------
 Immersion training    Stage d'immersion           Immersion training
 Internal engagement   Mise en situation interne   Internal engagement
 MISIP                 MISIP                       MISIP
===================== =========================== =====================
<BLANKLINE>


Demo data
=========

:class:`lino_welfare.modlib.isip.models.ExamPolicy`

>>> rt.show(immersion.Contracts)
==== ========================== ============== =============== ================== =========================
 ID   Client                     applies from   applies until   responsible (IS)   Immersion training type
---- -------------------------- -------------- --------------- ------------------ -------------------------
 1    GROTECLAES Gregory (131)   5/22/14        7/21/14         Alicia Allmanns    Immersion training
 2    EMONTS Erich (149)         6/21/14        10/19/14        Alicia Allmanns    Internal engagement
 3    RADERMACHER Inge (161)     7/21/14        1/17/15         Alicia Allmanns    MISIP
==== ========================== ============== =============== ================== =========================
<BLANKLINE>
