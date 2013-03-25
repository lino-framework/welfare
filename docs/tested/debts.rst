.. _welfare.tested.debts:

Debts mediation
===============

..
  >>> from lino.runtime import *

The demo database has three Budgets:

>>> debts.Budget.objects.count()
3

>>> obj = debts.Budget.objects.get(pk=3)
>>> print obj.BudgetSummary().to_rst()
========================================================= ==============
 Beschreibung                                              Betrag
--------------------------------------------------------- --------------
 Monatliche Einkünfte                                      5 000,00
 Jährliche Einkünfte (2 400,00 / 12)                       200,00
 Monatliche Ausgaben                                       -565,00
 Monatliche Reserve für jährliche Ausgaben (236,00 / 12)   -19,67
 Raten der laufenden Kredite                               -45,00
 **Finanzielle Situation**                                 **4 585,33**
========================================================= ==============
<BLANKLINE>


