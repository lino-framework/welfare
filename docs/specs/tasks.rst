.. doctest docs/specs/tasks.rst
.. _welfare.specs.tasks:

==============
Managing tasks
==============

A technical tour into the :mod:`lino_welfare.modlib.cal` module.

.. contents::
   :local:

.. include:: /../docs/shared/include/tested.rst

>>> from lino import startup
>>> startup('lino_welfare.projects.mathieu.settings.doctests')
>>> from lino.api.doctest import *


My tasks
========

The `My tasks` table (:class:`lino_xl.lib.cal.MyTasks`) is visible
in the dashboard.

This table shows tasks which are due in the next **30** days.  This
value is currently as a class attribute :attr:`default_end_date_offset
<lino.modlib.cal.MyTasks.default_end_date_offset>` on that table:

>>> cal.MyTasks.default_end_date_offset
30

For example Hubert has some tasks in that table:

>>> rt.login('hubert').show(cal.MyTasks)
========== ============ ============================= ============================= ==========================
 Priorité   Date début   Description brève             Workflow                      Bénéficiaire
---------- ------------ ----------------------------- ----------------------------- --------------------------
 Normale    12/06/2014   Projet termine dans un mois   **☐ à faire** → [☑] [☒] [⚠]   RADERMACHER Hedi (161)
 Normale    27/05/2014   Projet termine dans un mois   **☐ à faire** → [☑] [☒] [⚠]   RADERMACHER Edgard (157)
========== ============ ============================= ============================= ==========================
<BLANKLINE>


Here is the same table for Alice (with a task that is started *before* today):

>>> rt.login('alicia').show(cal.MyTasks)
========== ============ ============================= ============================= ======================
 Priorité   Date début   Description brève             Workflow                      Bénéficiaire
---------- ------------ ----------------------------- ----------------------------- ----------------------
 Normale    21/05/2014   Projet termine dans un mois   **☐ à faire** → [☑] [☒] [⚠]   DA VINCI David (165)
========== ============ ============================= ============================= ======================
<BLANKLINE>


Actually Alice has more open tasks, but they are all more than 30 days away in
the future.  If she manually sets :attr:`end_date
<lino.modlib.cal.Tasks.end_date>` to blank then she sees them:

>>> pv = dict(end_date=None)
>>> rt.login('alicia').show(cal.MyTasks, param_values=pv)
========== ============ ============================= ============================= ============================
 Priorité   Date début   Description brève             Workflow                      Bénéficiaire
---------- ------------ ----------------------------- ----------------------------- ----------------------------
 Normale    30/03/2015   Projet termine dans un mois   **☐ à faire** → [☑] [☒] [⚠]   DA VINCI David (165)
 Normale    05/01/2015   Projet termine dans un mois   **☐ à faire** → [☑] [☒] [⚠]   RADERMACHER Fritz (158)
 Normale    16/12/2014   Projet termine dans un mois   **☐ à faire** → [☑] [☒] [⚠]   MEESSEN Melissa (147)
 Normale    22/11/2014   Projet termine dans un mois   **☐ à faire** → [☑] [☒] [⚠]   KAIVERS Karl (141)
 Normale    07/10/2014   Projet termine dans un mois   **☐ à faire** → [☑] [☒] [⚠]   ENGELS Edgar (129)
 Normale    24/09/2014   Projet termine dans un mois   **☐ à faire** → [☑] [☒] [⚠]   DUBOIS Robin (179)
 Normale    02/08/2014   Projet termine dans un mois   **☐ à faire** → [☑] [☒] [⚠]   VAN VEEN Vincent (166)
 Normale    30/06/2014   Permis de travail expire le   **☐ à faire** → [☑] [☒] [⚠]   DOBBELSTEIN Dorothée (124)
 Normale    21/05/2014   Projet termine dans un mois   **☐ à faire** → [☑] [☒] [⚠]   DA VINCI David (165)
========== ============ ============================= ============================= ============================
<BLANKLINE>

