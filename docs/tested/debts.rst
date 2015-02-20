.. _welfare.tested.debts:

Debts mediation
===============

.. include:: /include/tested.rst

.. to test only this document:
  $ python setup.py test -s tests.DocsTests.test_debts

..
    >>> from django.utils import translation
    >>> from lino.runtime import *
    >>> from django.test import Client
    >>> import json

We switch to German because the first PCSW with Lino was the one in Eupen:

>>> translation.activate('de')

We can now refer to every installed app via it's `app_label`.
For example here is how we can verify here that the demo database 
has 14 Budgets:

>>> debts.Budget.objects.count()
14

Or we can retrieve budget no. 3 from the database:

>>> obj = debts.Budget.objects.get(pk=3)
>>> obj
Budget #3 (u'Budget Nr. 3 f\xfcr Jean\xe9mart-Thelen (232)')

So far this was standard Django API. To use Lino's extended API we 
first need to "log in" as user `rolf`:

>>> ses = rt.login('rolf')

Here is the textual representation of the "Expenses" panel:

>>> ses.show(debts.ExpensesByBudget.request(obj),
...   column_names="account description amount remark",
...   limit=10)
... #doctest: +NORMALIZE_WHITESPACE
====================================== ====================== ============ ===========
 Konto                                  Beschreibung           Betrag       Bemerkung
-------------------------------------- ---------------------- ------------ -----------
 (3010) Miete                           Rent                   41,00
 (3011) Wasser                          Water                  47,00
 (3012) Strom                           Electricity
 (3020) Festnetz-Telefon und Internet   Telephone & Internet   5,00
 (3021) Handy                           Cell phone             10,00
 (3030) Fahrtkosten                     Transport costs        15,00        Shopping
 (3030) Fahrtkosten                     Transport costs        15,00        Cinema
 (3031) TEC Busabonnement               Public transport       20,00
 (3032) Benzin                          Fuel                   26,00
 (3033) Unterhalt Auto                  Car maintenance        31,00
 **Total (35 Zeilen)**                                         **210,00**
====================================== ====================== ============ ===========
<BLANKLINE>

Note that the above table contains a mixture of German and English
texts because our **current language** is German while the **partner**
speaks English:

>>> print(obj.partner.language)
<BLANKLINE>

Description and Remark have been entererd for this particular Budget
instance and are therefore in the partner's language. Everything else
depends on the current user language.

Here are some more slave tables.

>>> ses.show(debts.ResultByBudget.request(obj))
========================================================= ==============
 Beschreibung                                              Betrag
--------------------------------------------------------- --------------
 Monatliche Einkünfte                                      5 000,00
 Monatliche Ausgaben                                       -565,00
 Monatliche Reserve für jährliche Ausgaben (236,00 / 12)   -19,67
 Raten der laufenden Kredite                               -45,00
 **Restbetrag für Kredite und Zahlungsrückstände**         **4 370,33**
========================================================= ==============
<BLANKLINE>

>>> obj.include_yearly_incomes = True
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
================================= ==============
 Beschreibung                      Betrag
--------------------------------- --------------
 Kredite (verteilbar)              1 500,00
 Schulden                          300,00
 Zahlungsrückstände (verteilbar)   1 200,00
 Zahlungsrückstände                600,00
 **Schulden**                      **3 600,00**
================================= ==============
<BLANKLINE>

>>> with translation.override('en'):
...     ses.show(debts.PrintLiabilitiesByBudget.request(obj))
================================= ========= ============== ============== ============== ============ ==============
 Partner                           Remarks   Monthly rate   Common         Mr.            Mrs.         Total
--------------------------------- --------- -------------- -------------- -------------- ------------ --------------
 Hans Flott & Co (108)                                      1 200,00                                   1 200,00
 Bernd Brechts Bücherladen (109)                                           1 500,00                    1 500,00
 Reinhards Baumschule (110*)                 15,00                                        300,00       300,00
 Moulin Rouge (111)                          30,00          600,00                                     600,00
 **Total (4 rows)**                          **45,00**      **1 800,00**   **1 500,00**   **300,00**   **3 600,00**
================================= ========= ============== ============== ============== ============ ==============
<BLANKLINE>

>>> with translation.override('en'):
...     ses.show(debts.DistByBudget.request(obj))
================================= ================= ============== ============ ===========================
 Creditor                          Description       Debt           %            Monthly payback suggested
--------------------------------- ----------------- -------------- ------------ ---------------------------
 Hans Flott & Co (108)             Invoices to pay   1 200,00       44,44        53,33
 Bernd Brechts Bücherladen (109)   Loans             1 500,00       55,56        66,67
 **Total (2 rows)**                                  **2 700,00**   **100,00**   **120,00**
================================= ================= ============== ============ ===========================
<BLANKLINE>

The following table shows how Lino renders remarks in the printed
version: they are added to the description between parentheses
(e.g. "Spare time"), and if several entries were grouped into a same
printable row (e.g. "Fahrtkosten"), they are separated by commas.

>>> groups = list(obj.account_groups())
>>> with translation.override('en'):
...     ses.show(obj.entries_by_group(ses, groups[2]))
====================== ================== =============== ============ ===== ====== ============
 Description            Remarks            Yearly amount   Common       Mr.   Mrs.   Total
---------------------- ------------------ --------------- ------------ ----- ------ ------------
 Rent                                                      41,00                     41,00
 Water                                                     47,00                     47,00
 Telephone & Internet                                      5,00                      5,00
 Cell phone                                                10,00                     10,00
 Transport costs        Shopping, Cinema                   30,00                     30,00
 Public transport                                          20,00                     20,00
 Fuel                                                      26,00                     26,00
 Car maintenance                                           31,00                     31,00
 School                                                    36,00                     36,00
 Babysitting                                               41,00                     41,00
 Health                                                    47,00                     47,00
 Food                                                      5,00                      5,00
 Hygiene                                                   10,00                     10,00
 Health insurance                                          15,00                     15,00
 Labour fees                                               20,00                     20,00
 Unterhaltszahlungen                                       26,00                     26,00
 Retirement savings                                        31,00                     31,00
 Tobacco                                                   36,00                     36,00
 Spare time             Seminar                            41,00                     41,00
 Pets                                                      47,00                     47,00
 **Total (20 rows)**                                       **565,00**                **565,00**
====================== ================== =============== ============ ===== ====== ============
<BLANKLINE>


Something in French
-------------------

>>> with translation.override('fr'):
...    ses.show(debts.DistByBudget.request(obj))
================================= ================= ============== ============ =======================
 Créancier                         Description       Dette          %            Remboursement mensuel
--------------------------------- ----------------- -------------- ------------ -----------------------
 Hans Flott & Co (108)             Invoices to pay   1 200,00       44,44        53,33
 Bernd Brechts Bücherladen (109)   Loans             1 500,00       55,56        66,67
 **Total (2 lignes)**                                **2 700,00**   **100,00**   **120,00**
================================= ================= ============== ============ =======================
<BLANKLINE>

Or the same in English:

>>> with translation.override('en'):
...     ses.show(debts.DistByBudget.request(obj))
================================= ================= ============== ============ ===========================
 Creditor                          Description       Debt           %            Monthly payback suggested
--------------------------------- ----------------- -------------- ------------ ---------------------------
 Hans Flott & Co (108)             Invoices to pay   1 200,00       44,44        53,33
 Bernd Brechts Bücherladen (109)   Loans             1 500,00       55,56        66,67
 **Total (2 rows)**                                  **2 700,00**   **100,00**   **120,00**
================================= ================= ============== ============ ===========================
<BLANKLINE>

Note that the Description still shows German words because these are stored per Budget, 
and Budget #3 is addressed to a German-speaking partner.


A web request
-------------

The following snippet reproduces a one-day bug 
discovered :blogref:`20130527`:

>>> client = Client()
>>> url = '/api/debts/Budgets/3?fmt=json&an=detail'
>>> res = client.get(url,REMOTE_USER='rolf')
>>> print(res.status_code)
200
>>> result = json.loads(res.content)
>>> print(result.keys())
[u'navinfo', u'data', u'disable_delete', u'id', u'title']


Editability of tables 
---------------------

The following is to check whether the editable attribute inherited 
correctly.

>>> debts.Budgets.editable
True
>>> debts.EntriesByBudget.editable
True
>>> debts.DistByBudget.editable
False
>>> debts.LiabilitiesByBudget.editable
True
>>> debts.PrintLiabilitiesByBudget.editable
False



