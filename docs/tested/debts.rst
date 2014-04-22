.. _welfare.tested.debts:

Debts mediation
===============

.. include:: /include/tested.rst

The following statements import some often-used global names::

>>> from django.utils import translation
>>> from lino.runtime import *
>>> from pprint import pprint
>>> from django.test import Client
>>> import json

We switch to German because the first PCSW with Lino was the one in Eupen:

>>> translation.activate('de')

We can now refer to every installed app via it's `app_label`.
For example here is how we can verify here that the demo database 
has three Budgets:

>>> debts.Budget.objects.count()
3

Or we can retrieve budget no. 3 from the database:

>>> obj = debts.Budget.objects.get(pk=3)
>>> obj
Budget #3 (u'Budget Nr. 3 f\xfcr Dubois-\xc4rgerlich (183)')

So far this was standard Django API. To use Lino's extended API we 
first need to "log in" as user `rolf`:

>>> ses = settings.SITE.login('rolf')

Here is the textual representation of the "Expenses" panel:

>>> # settings.SITE.catch_layout_exceptions = False
>>> ses.show(debts.ExpensesByBudget.request(obj),
...   column_names="account description amount remark",
...   limit=10)
... #doctest: +NORMALIZE_WHITESPACE
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

>>> ses.show(debts.PrintLiabilitiesByBudget.request(obj))
================================= ==================== ==================== ============ ============== ============== ============ ==============
 Partner                           Beschreibung         Gerichtsvollzieher   Monatsrate   Gemeinsam      Herr           Frau         Total
--------------------------------- -------------------- -------------------- ------------ -------------- -------------- ------------ --------------
 Bernd Brechts Bücherladen (108)   Zahlungsrückstände                                     1 200,00                                   1 200,00
 Reinhards Baumschule (109)        Kredite                                                               1 500,00                    1 500,00
 Moulin Rouge (110*)               Schulden                                  15,00                                      300,00       300,00
 Auto École Verte (111)            Zahlungsrückstände                        30,00        600,00                                     600,00
 **Total (4 Zeilen)**                                                        **45,00**    **1 800,00**   **1 500,00**   **300,00**   **3 600,00**
================================= ==================== ==================== ============ ============== ============== ============ ==============
<BLANKLINE>

>>> ses.show(debts.DistByBudget.request(obj))
================================= ==================== ============== ============ ====================================
 Kreditor                          Beschreibung         Schuld         %            Betrag der monatlichen Rückzahlung
--------------------------------- -------------------- -------------- ------------ ------------------------------------
 Bernd Brechts Bücherladen (108)   Zahlungsrückstände   1 200,00       44,44        53,33
 Reinhards Baumschule (109)        Kredite              1 500,00       55,56        66,67
 **Total (2 Zeilen)**                                   **2 700,00**   **100,00**   **120,00**
================================= ==================== ============== ============ ====================================
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
>>> obj.clear_cache()
>>> print(ses.run(obj.do_print)) #doctest: +NORMALIZE_WHITESPACE
{'refresh': True, 
'open_url': u'/media/webdav/userdocs/appyodt/debts.Budget-3.odt', 
'message': u'Dokument Budget Nr. 3 f\xfcr Dubois-\xc4rgerlich (183) wurde generiert.', 
'success': True}


Something in French
-------------------

>>> with translation.override('fr'):
...    ses.show(debts.DistByBudget.request(obj))
================================= ==================== ============== ============ =======================
 Créancier                         Description          Dette          %            Remboursement mensuel
--------------------------------- -------------------- -------------- ------------ -----------------------
 Bernd Brechts Bücherladen (108)   Zahlungsrückstände   1 200,00       44,44        53,33
 Reinhards Baumschule (109)        Kredite              1 500,00       55,56        66,67
 **Total (2 lignes)**                                   **2 700,00**   **100,00**   **120,00**
================================= ==================== ============== ============ =======================
<BLANKLINE>

Or the same in English:

>>> with translation.override('en'):
...     ses.show(debts.DistByBudget.request(obj))
================================= ==================== ============== ============ ===========================
 Creditor                          Description          Debt           %            Monthly payback suggested
--------------------------------- -------------------- -------------- ------------ ---------------------------
 Bernd Brechts Bücherladen (108)   Zahlungsrückstände   1 200,00       44,44        53,33
 Reinhards Baumschule (109)        Kredite              1 500,00       55,56        66,67
 **Total (2 rows)**                                     **2 700,00**   **100,00**   **120,00**
================================= ==================== ============== ============ ===========================
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



Work in progress
----------------

The rest of this document is work in progress.
Lino doesn't yet have a satisfying API for doing such things,
and I'm using the occasion to work on that.


>>> expenses = accounts.AccountTypes.expenses
>>> # settings.SITE.catch_layout_exceptions = False
>>> # ses.show(accounts.Accounts.request(known_values=dict(type=expenses)),column_names="ref name")

A Preview:

.. django2rst:: 

   from lino.utils.xmlgen.html import E
   print(".. raw:: html")
   print("")
   e = debts.Budget.objects.get(pk=3).to_html()
   print("   " + E.tostring(e))



