.. _welfare.specs.tasks:

==============
Managing tasks
==============

.. How to test only this document:

    $ python setup.py test -s tests.SpecsTests.test_tasks
    
    doctest init:

    >>> from __future__ import print_function
    >>> import os
    >>> os.environ['DJANGO_SETTINGS_MODULE'] = \
    ...    'lino_welfare.projects.chatelet.settings.doctests'
    >>> from lino.api.doctest import *

A technical tour into the :mod:`lino_welfare.modlib.cal` module.

.. contents::
   :local:


My tasks
========

The `My tasks` table (:class:`lino.modlib.cal.ui.MyTasks`) is visible
in the admin main screen.

This table shows tasks which are due in the next **30** days.  This
value is currently as a class attribute :attr:`default_end_date_offset
<lino.modlib.cal.ui.MyTasks.default_end_date_offset>` on that table:

>>> cal.MyTasks.default_end_date_offset
30

For example Hubert has some tasks in that table:

>>> rt.login('hubert').show(cal.MyTasks)
============ ============================= ==================================== ==========================
 Date début   Résumé                        État                                 Bénéficiaire
------------ ----------------------------- ------------------------------------ --------------------------
 27/05/2014   Projet termine dans un mois   **à faire** → [accomplie] [Annulé]   RADERMACHER Edgard (157)
 12/06/2014   Projet termine dans un mois   **à faire** → [accomplie] [Annulé]   RADERMACHER Hedi (161)
============ ============================= ==================================== ==========================
<BLANKLINE>


For Alice this table is empty:

>>> rt.login('alicia').show(cal.MyTasks)
Aucun enregistrement

Actually Alice *does* have quite some tasks, but they are all more than
30 days away in the future.  If she manually sets :attr:`end_date
<lino.modlib.cal.ui.Tasks.end_date>` to blank then she sees them:

>>> pv = dict(end_date=None)
>>> rt.login('alicia').show(cal.MyTasks, param_values=pv)
============ ============================= ==================================== ============================
 Date début   Résumé                        État                                 Bénéficiaire
------------ ----------------------------- ------------------------------------ ----------------------------
 30/06/2014   Permis de travail expire le   **à faire** → [accomplie] [Annulé]   DOBBELSTEIN Dorothée (124)
 02/08/2014   Projet termine dans un mois   **à faire** → [accomplie] [Annulé]   VAN VEEN Vincent (166)
 24/09/2014   Projet termine dans un mois   **à faire** → [accomplie] [Annulé]   DUBOIS Robin (179)
 07/10/2014   Projet termine dans un mois   **à faire** → [accomplie] [Annulé]   ENGELS Edgar (129)
 22/11/2014   Projet termine dans un mois   **à faire** → [accomplie] [Annulé]   KAIVERS Karl (141)
 16/12/2014   Projet termine dans un mois   **à faire** → [accomplie] [Annulé]   MEESSEN Melissa (147)
 05/01/2015   Projet termine dans un mois   **à faire** → [accomplie] [Annulé]   RADERMACHER Fritz (158)
 30/03/2015   Projet termine dans un mois   **à faire** → [accomplie] [Annulé]   DA VINCI David (165)
============ ============================= ==================================== ============================
<BLANKLINE>

