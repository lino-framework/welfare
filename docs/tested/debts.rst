.. _welfare.tested.debts:

Debts mediation
===============

.. include:: /include/tested.rst

Import names of installed apps (here we are going to use "accounts" and "debts"):

>>> from lino.runtime import *

For example we can verify here that the demo database has three Budgets:

>>> debts.Budget.objects.count()
3

"Log in" as user `rolf`:

>>> ses = settings.SITE.login('rolf')

This has e.g. the effect of switching to German.

Let's look at budget no. 3.

>>> obj = debts.Budget.objects.get(pk=3)

Here is the textual representation of the "Expenses" panel:

>>> settings.SITE.catch_layout_exceptions = False
>>> ses.show(debts.ExpensesByBudget.request(obj),
...   column_names="account description amount remark",
...   limit=10)
====================================== =============================== ============ ===========
 Konto                                  Beschreibung                    Betrag       Bemerkung
-------------------------------------- ------------------------------- ------------ -----------
 (3010) Miete                           Miete                           41,00
 (3011) Wasser                          Wasser                          47,00
 (3012) Strom                           Strom
 (3020) Festnetz-Telefon und Internet   Festnetz-Telefon und Internet   5,00
 (3021) Handy                           Handy                           10,00
 (3030) Fahrtkosten                     Fahrtkosten                     15,00        Seminar
 (3030) Fahrtkosten                     Fahrtkosten                     15,00        Kino
 (3031) TEC Busabonnement               TEC Busabonnement               20,00
 (3032) Benzin                          Benzin                          26,00
 (3033) Unterhalt Auto                  Unterhalt Auto                  31,00
 **Total (35 Zeilen)**                                                  **210,00**
====================================== =============================== ============ ===========
<BLANKLINE>


Here are some more slave tables.

>>> ses.show(debts.ResultByBudget.request(obj))
========================================================= ==============
 Beschreibung                                              Betrag
--------------------------------------------------------- --------------
 Monatliche Einkünfte                                      5 000,00
 Jährliche Einkünfte (2 400,00 / 12)                       200,00
 Monatliche Ausgaben                                       -565,00
 Monatliche Reserve für jährliche Ausgaben (236,00 / 12)   -19,67
 Raten der laufenden Kredite                               -45,00
 **Restbetrag für Kredite und Zahlungsrückstände**         **4 570,33**
========================================================= ==============
<BLANKLINE>

>>> ses.show(debts.DebtsByBudget.request(obj))
======================= ==============
 Beschreibung            Betrag
----------------------- --------------
 Kredite (verteilbar)    1 200,00
 Schulden (verteilbar)   1 500,00
 Gerichtsvollzieher      300,00
 Zahlungsrückstände      600,00
 **Schulden**            **3 600,00**
======================= ==============
<BLANKLINE>

The following table shows the new feature (:blogref:`20130325`) 
of how Lino renders remarks in the printed version: they are added 
to the description between parentheses (e.g. "Freizeit & Unterhaltung"),
and if several entries were grouped into a same printable 
row (e.g. "Fahrtkosten") separated by commas.

>>> groups = list(obj.account_groups())
>>> ses.show(obj.entries_by_group(groups[2]))
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



Printing a Budget
-----------------

>>> obj = debts.Budget.objects.get(pk=3)
>>> from pprint import pprint
>>> pprint(ses.run(obj.do_clear_cache))
{'message': 'Budget Nr. 3 f\xc3\xbcr Altenberg-Charlier printable cache has been cleared.',
 'refresh': True,
 'success': True}
>>> pprint(ses.run(obj.do_print)) #doctest: +NORMALIZE_WHITESPACE
{'message': u'Dokument Budget Nr. 3 f\xfcr Altenberg-Charlier wurde generiert.',
 'open_url': '/media/userdocs/appyodt/debts.Budget-3.odt',
 'refresh': True,
 'success': True}



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
