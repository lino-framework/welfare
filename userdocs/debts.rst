.. _welfare.debts:

===================
Debts mediation
===================

Debts Mediation (Schuldnerberatung, Médiation de dettes)

This app enables social consultants to create "Budgets".
A :ddref:`debts.Budget` collects financial 
information like monthly income, monthly expenses and debts 
of a household or a person, then print out a document which serves 
as base for the consultation and discussion with debtors.


Scénarios
=========

- En tant que conseiller dettes je commence à remplir, avec le client, 
  les données d'un budget. Le client n'a pas 
  toutes les informations nécessaires avec lui. 
  Comment puis-je lui imprimer une version spéciale du budget, 
  destinée à être utilisée pour remplir manuellement sur papier 
  les chiffres manquants pour les encoder la prochaine fois?
  
  - Activer le champ :ref:`welfare.debts.Budget.print_empty_rows`
  - Cliquer sur :ref:`welfare.ui.detail.Save`


.. actor:: debts.Actor

.. actor:: debts.Budget


.. _welfare.debts.Budget.print_empty_rows:

Print empty rows
----------------

.. _welfare.debts.Budget.ignore_yearly_incomes:

Ignore yearly incomes
---------------------



.. actor:: debts.MyBudgets
.. actor:: debts.ResultByBudget
.. actor:: debts.Entry
.. actor:: debts.EntriesByBudget


.. actor:: debts.DebtsByBudget

Slave table in the "Summary" tab of a :ddref:`debts.Budget` detail.

Shows the "simple" debts in this budget (those who have not yet been
transferred to a debt collection agency).


.. actor:: debts.BailiffDebtsByBudget

Slave table in the "Summary" tab of a :ddref:`debts.Budget` detail.

Shows the debts in this budget which have been transferred to a debt
collection agency.


