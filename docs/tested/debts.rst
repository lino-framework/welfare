.. _welfare.tested.debts:

Debts mediation
===============

Import names of installed apps (here we are going to use "accounts" and "debts"):

>>> from lino.runtime import *

For example we can verify here that the demo database has three Budgets:

>>> debts.Budget.objects.count()
3

"Log in" as user `rolf`:

>>> ses = settings.SITE.login('rolf')

This has e.g. the effect of switching to German.

>>> obj = debts.Budget.objects.get(pk=3)
>>> ses.show(obj.BudgetSummary())
========================================================= ==============
 Beschreibung                                              Betrag
--------------------------------------------------------- --------------
 Monatliche Einkünfte                                      5 000,00
 Jährliche Einkünfte (2 400,00 / 12)                       200,00
 Monatliche Ausgaben                                       -565,00
 Monatliche Reserve für jährliche Ausgaben (236,00 / 12)   -19,67
 Raten der laufenden Kredite                               -45,00
 **Finanzielle Situation**                                 **4 570,33**
========================================================= ==============
<BLANKLINE>


The following table shows the new feature (:blogref:`20130325`) 
of how Lino shows remarks in the printed version: they are added 
to the description between parentheses (e.g. "Freizeit & Unterhaltung"),
and if several entries were grouped into a same printable 
row (e.g. "Fahrtkosten") separated by commas.

>>> groups = list(obj.account_groups())
>>> ses.show(obj.entries_by_group(ses,groups[2]))
=================================== ============ ====== ====== ============
 Beschreibung                        Gemeinsam    Herr   Frau   Total
----------------------------------- ------------ ------ ------ ------------
 Miete                               41,00                      41,00
 Wasser                              47,00                      47,00
 Festnetz-Telefon und Internet       5,00                       5,00
 Handy                               10,00                      10,00
 Fahrtkosten (Seminar, Kino)         30,00                      30,00
 TEC Busabonnement                   20,00                      20,00
 Benzin                              26,00                      26,00
 Unterhalt Auto                      31,00                      31,00
 Schulkosten                         36,00                      36,00
 Tagesmutter & Kleinkindbetreuung    41,00                      41,00
 Gesundheit                          47,00                      47,00
 Ernährung                           5,00                       5,00
 Hygiene                             10,00                      10,00
 Krankenkassenbeiträge               15,00                      15,00
 Gewerkschaftsbeiträge               20,00                      20,00
 Unterhaltszahlungen                 26,00                      26,00
 Pensionssparen                      31,00                      31,00
 Tabak                               36,00                      36,00
 Freizeit & Unterhaltung (Seminar)   41,00                      41,00
 Haustiere                           47,00                      47,00
 **Total (20 Zeilen)**               **565,00**                 **565,00**
=================================== ============ ====== ====== ============
<BLANKLINE>


Work in progress
----------------

The rest of this document is work in progress.
Lino doesn't yet have a satisfying API for doing such things,
and I'm using the occasion to work on that.


>>> expenses = accounts.AccountTypes.expenses
>>> # settings.SITE.catch_layout_exceptions = False
>>> # ses.show(accounts.Accounts.request(known_values=dict(type=expenses)),column_names="ref name")

A Preview:


.. py2rst:: 

   from lino.utils.xmlgen.html import E
   print ".. raw:: html"
   print ""
   e = debts.Budget.objects.get(pk=3).to_html()
   print "   " + E.tostring(e)
