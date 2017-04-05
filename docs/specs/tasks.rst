.. _welfare.specs.tasks:

==============
Managing tasks
==============

.. How to test only this document:

    $ python setup.py test -s tests.SpecsTests.test_tasks
    
    doctest init:

    >>> from lino import startup
    >>> startup('lino_welfare.projects.chatelet.settings.doctests')
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
============ ============================= =========================== ==========================
 Date début   Description brève             Actions                     Bénéficiaire
------------ ----------------------------- --------------------------- --------------------------
 27/05/2014   Projet termine dans un mois   **à faire** → [☑] [☒] [⚠]   RADERMACHER Edgard (157)
 12/06/2014   Projet termine dans un mois   **à faire** → [☑] [☒] [⚠]   RADERMACHER Hedi (161)
============ ============================= =========================== ==========================
<BLANKLINE>


For Alice this table is empty:

>>> rt.login('alicia').show(cal.MyTasks)
Aucun enregistrement

Actually Alice *does* have quite some tasks, but they are all more than
30 days away in the future.  If she manually sets :attr:`end_date
<lino.modlib.cal.ui.Tasks.end_date>` to blank then she sees them:

>>> pv = dict(end_date=None)
>>> rt.login('alicia').show(cal.MyTasks, param_values=pv)
============ ============================= =========================== ============================
 Date début   Description brève             Actions                     Bénéficiaire
------------ ----------------------------- --------------------------- ----------------------------
 30/06/2014   Permis de travail expire le   **à faire** → [☑] [☒] [⚠]   DOBBELSTEIN Dorothée (124)
 02/08/2014   Projet termine dans un mois   **à faire** → [☑] [☒] [⚠]   VAN VEEN Vincent (166)
 24/09/2014   Projet termine dans un mois   **à faire** → [☑] [☒] [⚠]   DUBOIS Robin (179)
 07/10/2014   Projet termine dans un mois   **à faire** → [☑] [☒] [⚠]   ENGELS Edgar (129)
 22/11/2014   Projet termine dans un mois   **à faire** → [☑] [☒] [⚠]   KAIVERS Karl (141)
 16/12/2014   Projet termine dans un mois   **à faire** → [☑] [☒] [⚠]   MEESSEN Melissa (147)
 05/01/2015   Projet termine dans un mois   **à faire** → [☑] [☒] [⚠]   RADERMACHER Fritz (158)
 30/03/2015   Projet termine dans un mois   **à faire** → [☑] [☒] [⚠]   DA VINCI David (165)
============ ============================= =========================== ============================
<BLANKLINE>

