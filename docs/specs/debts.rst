.. doctest docs/specs/debts.rst
.. _welfare.specs.debts:

===============
Debts mediation
===============
   
The :mod:`lino_welfare.modlib.debts` modules adds functionality for
managing "budgets".

.. currentmodule:: lino_welfare.modlib.debts
    
.. contents::
   :local:
   :depth: 1

.. include:: /../docs/shared/include/tested.rst

>>> import lino
>>> lino.startup('lino_welfare.projects.gerd.settings.doctests')
>>> from lino.api.doctest import *

>>> ses = rt.login('robin')


Budgets
=======
    
A :class:`Budget <lino_welfare.modlib.debts.Budget>` is a document
based on financial data about a person or household.  It is just about
entering this data and then printing it.

The demo database has 14 such documents with fictive generated data:

>>> debts.Budget.objects.count()
14

For the following examples we will use budget no. 3:

>>> translation.activate('en')
>>> obj = debts.Budget.objects.get(pk=3)
>>> print(str(obj))
Budget 3 for Jérôme & Theresia Jeanémart-Thelen



Actors
======

This budget has 3 actors:

>>> len(obj.get_actors())
3

Every actor is an instance of :class:`Actor
<lino_welfare.modlib.debts.models.Actor>`, which is designed to be
used in templates. For example, every actor has four attributes
`header`, `person`, `client` and `household`:

>>> u = attrtable(obj.get_actors(), 'header person client household')
>>> print(u)
======== ===================== ======================== ========================================================
 header   person                client                   household
-------- --------------------- ------------------------ --------------------------------------------------------
 Common   None                  None                     Jérôme & Theresia Jeanémart-Thelen (Factual household)
 Herr     Mr Jérôme JEANÉMART   JEANÉMART Jérôme (181)   None
 Frau     Mrs Theresia THELEN   None                     None
======== ===================== ======================== ========================================================
<BLANKLINE>


Data entry panels
=================

Here is the textual representation of the "Expenses" panel:

>>> ses.show(debts.ExpensesByBudget, obj,
...   column_names="account description amount remark",
...   limit=10)
... #doctest: +NORMALIZE_WHITESPACE
============================= =============================== ============ ===========
 Account                       Description                     Amount       Remark
----------------------------- ------------------------------- ------------ -----------
 (3010) Rent                   Miete                           41,00
 (3011) Water                  Wasser                          47,00
 (3012) Electricity            Strom
 (3020) Telephone & Internet   Festnetz-Telefon und Internet   5,00
 (3021) Cell phone             Handy                           10,00
 (3030) Transport costs        Fahrtkosten                     15,00        Kino
 (3030) Transport costs        Fahrtkosten                     15,00        Einkaufen
 (3031) Public transport       TEC Busabonnement               20,00
 (3032) Fuel                   Benzin                          26,00
 (3033) Car maintenance        Unterhalt Auto                  31,00
 **Total (35 rows)**                                           **210,00**
============================= =============================== ============ ===========
<BLANKLINE>

Note that the above table contains a mixture of German and English
texts because our **current language** is German while the **partner**
speaks English:

>>> print(obj.partner.language)
<BLANKLINE>

Description and Remark have been entererd for this particular Budget
instance and are therefore in the partner's language. Everything else
depends on the current user language.


The summary panel
=================

Here are some more slave tables.

>>> ses.show(debts.ResultByBudget, obj)
=================================================== ==============
 Description                                         Amount
--------------------------------------------------- --------------
 Monthly incomes                                     5 000,00
 Monthly expenses                                    -565,00
 Monthly reserve for yearly expenses (236,00 / 12)   -19,67
 Monthly installment for running credits             -45,00
 **Remaining for credits and debts**                 **4 370,33**
=================================================== ==============
<BLANKLINE>

>>> obj.include_yearly_incomes = True
>>> ses.show(debts.ResultByBudget, obj)
=================================================== ==============
 Description                                         Amount
--------------------------------------------------- --------------
 Monthly incomes                                     5 000,00
 Yearly incomes (2 400,00 / 12)                      200,00
 Monthly expenses                                    -565,00
 Monthly reserve for yearly expenses (236,00 / 12)   -19,67
 Monthly installment for running credits             -45,00
 **Remaining for credits and debts**                 **4 570,33**
=================================================== ==============
<BLANKLINE>

>>> ses.show(debts.DebtsByBudget, obj)
================================= ==============
 Description                       Amount
--------------------------------- --------------
 Loans                             300,00
 Debts                             600,00
 Invoices to pay (distributable)   900,00
 Bailiff (distributable)           1 200,00
 Cash agency (distributable)       1 500,00
 **Liabilities**                   **4 500,00**
================================= ==============
<BLANKLINE>

>>> ses.show(debts.DebtsByBudget, obj, language="de")
================================== ==============
 Beschreibung                       Betrag
---------------------------------- --------------
 Kredite                            300,00
 Schulden                           600,00
 Zahlungsrückstände (verteilbar)    900,00
 Gerichtsvollzieher (verteilbar)    1 200,00
 Inkasso-Unternehmen (verteilbar)   1 500,00
 **Verpflichtungen**                **4 500,00**
================================== ==============
<BLANKLINE>

>>> ses.show(debts.DistByBudget, obj, language="de")
====================== ===================== ============== ============ ====================================
 Kreditor               Beschreibung          Schuld         %            Betrag der monatlichen Rückzahlung
---------------------- --------------------- -------------- ------------ ------------------------------------
 Auto École Verte       Zahlungsrückstände    900,00         25,00        30,00
 ÖSHZ Kettenis          Gerichtsvollzieher    1 200,00       33,33        40,00
 BISA                   Inkasso-Unternehmen   1 500,00       41,67        50,00
 **Total (3 Zeilen)**                         **3 600,00**   **100,00**   **120,00**
====================== ===================== ============== ============ ====================================
<BLANKLINE>

The printed document
====================

The following table shows how Lino renders remarks in the printed
version: they are added to the description between parentheses
(e.g. "Spare time"), and if several entries were grouped into a same
printable row (e.g. "Fahrtkosten"), they are separated by commas.

>>> groups = list(obj.entry_groups(ses))
>>> ses.show(groups[0].action_request)
... #doctest: -REPORT_UDIFF
==================== ========= ======== ====== ============== ==============
 Description          Remarks   Common   Herr   Frau           Total
-------------------- --------- -------- ------ -------------- --------------
 Gehälter                                       800,00         800,00
 Renten                                         1 000,00       1 000,00
 Integrationszulage                             1 200,00       1 200,00
 Ersatzeinkünfte                                1 400,00       1 400,00
 Alimente
 Essen-Schecks                                  200,00         200,00
 Andere                                         400,00         400,00
 **Total (7 rows)**                             **5 000,00**   **5 000,00**
==================== ========= ======== ====== ============== ==============
<BLANKLINE>

>>> ses.show(groups[1].action_request, language="de")
... #doctest: +REPORT_UDIFF
================================== ================= =============== ============ ====== ====== ============
 Beschreibung                       Bemerkungen       Jährl. Betrag   Gemeinsam    Herr   Frau   Total
---------------------------------- ----------------- --------------- ------------ ------ ------ ------------
 Miete                                                492,00          41,00                      41,00
 Wasser                                               564,00          47,00                      47,00
 Strom
 Festnetz-Telefon und Internet                        60,00           5,00                       5,00
 Handy                                                120,00          10,00                      10,00
 Fahrtkosten                        Kino, Einkaufen   360,00          30,00                      30,00
 TEC Busabonnement                                    240,00          20,00                      20,00
 Benzin                                               312,00          26,00                      26,00
 Unterhalt Auto                                       372,00          31,00                      31,00
 Schulkosten                                          432,00          36,00                      36,00
 Tagesmutter & Kleinkindbetreuung                     492,00          41,00                      41,00
 Gesundheit                                           564,00          47,00                      47,00
 Kleidung
 Ernährung                                            60,00           5,00                       5,00
 Hygiene                                              120,00          10,00                      10,00
 Krankenkassenbeiträge                                180,00          15,00                      15,00
 Gewerkschaftsbeiträge                                240,00          20,00                      20,00
 Unterhaltszahlungen                                  312,00          26,00                      26,00
 Pensionssparen                                       372,00          31,00                      31,00
 Tabak                                                432,00          36,00                      36,00
 Freizeit & Unterhaltung            Seminar           492,00          41,00                      41,00
 Haustiere                                            564,00          47,00                      47,00
 Sonstige
 **Total (23 Zeilen)**                                **6 780,00**    **565,00**                 **565,00**
================================== ================= =============== ============ ====== ====== ============
<BLANKLINE>


>>> ses.show(groups[2].action_request, language="de")
... #doctest: +REPORT_UDIFF
==================================== =========== ====== ============ ============
 Beschreibung                         Gemeinsam   Herr   Frau         Total
------------------------------------ ----------- ------ ------------ ------------
 Urlaubsgeld (600.00 / 12)                               50,00        50,00
 Jahresendzulage (800.00 / 12)                           66,67        66,67
 Gewerkschaftsprämie (1000.00 / 12)                      83,33        83,33
 **Total (3 Zeilen)**                                    **200,00**   **200,00**
==================================== =========== ====== ============ ============
<BLANKLINE>



Something in French
===================

>>> ses.show(debts.DistByBudget, obj, language="fr")
====================== ===================== ============== ============ =======================
 Créancier              Description           Dette          %            Remboursement mensuel
---------------------- --------------------- -------------- ------------ -----------------------
 Auto École Verte       Zahlungsrückstände    900,00         25,00        30,00
 ÖSHZ Kettenis          Gerichtsvollzieher    1 200,00       33,33        40,00
 BISA                   Inkasso-Unternehmen   1 500,00       41,67        50,00
 **Total (3 lignes)**                         **3 600,00**   **100,00**   **120,00**
====================== ===================== ============== ============ =======================
<BLANKLINE>

Or the same in English:

>>> with translation.override('en'):
...     ses.show(debts.DistByBudget, obj)
==================== ===================== ============== ============ ===========================
 Creditor             Description           Debt           %            Monthly payback suggested
-------------------- --------------------- -------------- ------------ ---------------------------
 Auto École Verte     Zahlungsrückstände    900,00         25,00        30,00
 ÖSHZ Kettenis        Gerichtsvollzieher    1 200,00       33,33        40,00
 BISA                 Inkasso-Unternehmen   1 500,00       41,67        50,00
 **Total (3 rows)**                         **3 600,00**   **100,00**   **120,00**
==================== ===================== ============== ============ ===========================
<BLANKLINE>

Note that the Description still shows German words because these are stored per Budget, 
and Budget #3 is addressed to a German-speaking partner.


A web request
=============

The following snippet reproduces a one-day bug 
discovered :blogref:`20130527`:

>>> url = '/api/debts/Budgets/3?fmt=json&an=detail'
>>> test_client.force_login(rt.login('rolf').user)
>>> res = test_client.get(url,REMOTE_USER='rolf')
>>> print(res.status_code)
200
>>> result = json.loads(res.content)
>>> print(' '.join(sorted(result.keys())))
data disable_delete id navinfo param_values title


Editability of tables
=====================

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
>>> debts.PrintEntriesByBudget.editable
False




The stories
===========

Here is now (almost) the whole content of a printed budget.

>>> obj = debts.Budget.objects.get(pk=4)

>>> ses.story2rst(obj.data_story(ses))
... #doctest: +NORMALIZE_WHITESPACE +REPORT_UDIFF
~~~~~~~~~~~~~~~~~~~~
Monatliche Einkünfte
~~~~~~~~~~~~~~~~~~~~
<BLANKLINE>
====================== ============= =========== ====== ============== ==============
 Beschreibung           Bemerkungen   Gemeinsam   Herr   Frau           Total
---------------------- ------------- ----------- ------ -------------- --------------
 Gehälter                                                1 200,00       1 200,00
 Renten                                                  1 400,00       1 400,00
 Integrationszulage
 Ersatzeinkünfte                                         200,00         200,00
 Alimente                                                400,00         400,00
 Essen-Schecks                                           600,00         600,00
 Andere                                                  800,00         800,00
 **Total (7 Zeilen)**                                    **4 600,00**   **4 600,00**
====================== ============= =========== ====== ============== ==============
<BLANKLINE>
~~~~~~~~~~~~~~~~~~~
Monatliche Ausgaben
~~~~~~~~~~~~~~~~~~~
<BLANKLINE>
================================== ================= =============== ============ ====== ====== ============
 Beschreibung                       Bemerkungen       Jährl. Betrag   Gemeinsam    Herr   Frau   Total
---------------------------------- ----------------- --------------- ------------ ------ ------ ------------
 Miete                                                120,00          10,00                      10,00
 Wasser                                               180,00          15,00                      15,00
 Strom                                                240,00          20,00                      20,00
 Festnetz-Telefon und Internet                        312,00          26,00                      26,00
 Handy                                                372,00          31,00                      31,00
 Fahrtkosten                        Einkaufen, Kino   864,00          72,00                      72,00
 TEC Busabonnement                                    492,00          41,00                      41,00
 Benzin                                               564,00          47,00                      47,00
 Unterhalt Auto
 Schulkosten                                          60,00           5,00                       5,00
 Tagesmutter & Kleinkindbetreuung                     120,00          10,00                      10,00
 Gesundheit                                           180,00          15,00                      15,00
 Kleidung                                             240,00          20,00                      20,00
 Ernährung                                            312,00          26,00                      26,00
 Hygiene                                              372,00          31,00                      31,00
 Krankenkassenbeiträge                                432,00          36,00                      36,00
 Gewerkschaftsbeiträge                                492,00          41,00                      41,00
 Unterhaltszahlungen                                  564,00          47,00                      47,00
 Pensionssparen
 Tabak                                                60,00           5,00                       5,00
 Freizeit & Unterhaltung            Kino              120,00          10,00                      10,00
 Haustiere                                            180,00          15,00                      15,00
 Sonstige                                             240,00          20,00                      20,00
 **Total (23 Zeilen)**                                **6 516,00**    **543,00**                 **543,00**
================================== ================= =============== ============ ====== ====== ============
<BLANKLINE>
~~~~~~~~~~~~~~~~~~~
Jährliche Einkünfte
~~~~~~~~~~~~~~~~~~~
<BLANKLINE>
==================================== =========== ====== ============ ============
 Beschreibung                         Gemeinsam   Herr   Frau         Total
------------------------------------ ----------- ------ ------------ ------------
 Urlaubsgeld (1000.00 / 12)                              83,33        83,33
 Jahresendzulage (1200.00 / 12)                          100,00       100,00
 Gewerkschaftsprämie (1400.00 / 12)                      116,67       116,67
 **Total (3 Zeilen)**                                    **300,00**   **300,00**
==================================== =========== ====== ============ ============
<BLANKLINE>
~~~~~~~
Steuern
~~~~~~~
<BLANKLINE>
====================== ============= =============== =========== ====== ====== ===========
 Beschreibung           Bemerkungen   Jährl. Betrag   Gemeinsam   Herr   Frau   Total
---------------------- ------------- --------------- ----------- ------ ------ -----------
 Gemeindesteuer                       26,00           2,17                      2,17
 Kanalisationssteuer                  31,00           2,58                      2,58
 Müllsteuer                           36,00           3,00                      3,00
 Autosteuer                           41,00           3,42                      3,42
 Immobiliensteuer                     47,00           3,92                      3,92
 Andere
 **Total (6 Zeilen)**                 **181,00**      **15,08**                 **15,08**
====================== ============= =============== =========== ====== ====== ===========
<BLANKLINE>
~~~~~~~~~~~~~~
Versicherungen
~~~~~~~~~~~~~~
<BLANKLINE>
======================= ============= =============== =========== ====== ====== ==========
 Beschreibung            Bemerkungen   Jährl. Betrag   Gemeinsam   Herr   Frau   Total
----------------------- ------------- --------------- ----------- ------ ------ ----------
 Feuer                                 5,00            0,42                      0,42
 Familienhaftpflicht                   10,00           0,83                      0,83
 Auto                                  15,00           1,25                      1,25
 Lebensversicherung                    20,00           1,67                      1,67
 Andere Versicherungen                 26,00           2,17                      2,17
 **Total (5 Zeilen)**                  **76,00**       **6,33**                  **6,33**
======================= ============= =============== =========== ====== ====== ==========
<BLANKLINE>
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Schulden, Zahlungsrückstände, Kredite
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
<BLANKLINE>
====================== ============= ============ ============ ====== ====== ============
 Partner                Bemerkungen   Monatsrate   Gemeinsam    Herr   Frau   Total
---------------------- ------------- ------------ ------------ ------ ------ ------------
 Pro Aktiv V.o.G.                                  900,00                     900,00
 **Total (1 Zeilen)**                              **900,00**                 **900,00**
====================== ============= ============ ============ ====== ====== ============
<BLANKLINE>
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Gerichtsvollzieher und Inkasso
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
<BLANKLINE>
====================== ========================== ============= ============ =========== ============== ============== ==============
 Schuldeneintreiber     Partner                    Bemerkungen   Monatsrate   Gemeinsam   Herr           Frau           Total
---------------------- -------------------------- ------------- ------------ ----------- -------------- -------------- --------------
 Cashback sprl          Werkstatt Cardijn V.o.G.                                          1 200,00                      1 200,00
 Money Wizard AS        Behindertenstätten Eupen                                                         1 500,00       1 500,00
 **Total (2 Zeilen)**                                                                     **1 200,00**   **1 500,00**   **2 700,00**
====================== ========================== ============= ============ =========== ============== ============== ==============
<BLANKLINE>



>>> ses.story2rst(obj.summary_story(ses))
... #doctest: +NORMALIZE_WHITESPACE -REPORT_UDIFF
--------------------
Einnahmen & Ausgaben
--------------------
<BLANKLINE>
========================================================= ==============
 Beschreibung                                              Betrag
--------------------------------------------------------- --------------
 Monatliche Einkünfte                                      4 600,00
 Monatliche Ausgaben                                       -543,00
 Monatliche Reserve für jährliche Ausgaben (257,00 / 12)   -21,42
 **Restbetrag für Kredite und Zahlungsrückstände**         **4 035,58**
========================================================= ==============
<BLANKLINE>
---------------
Verpflichtungen
---------------
<BLANKLINE>
================================== ==============
 Beschreibung                       Betrag
---------------------------------- --------------
 Zahlungsrückstände (verteilbar)    900,00
 Gerichtsvollzieher (verteilbar)    1 200,00
 Inkasso-Unternehmen (verteilbar)   1 500,00
 **Verpflichtungen**                **3 600,00**
================================== ==============
<BLANKLINE>
------------------
Schuldenverteilung
------------------
<BLANKLINE>
========================== ===================== ============== ============ ====================================
 Kreditor                   Beschreibung          Schuld         %            Betrag der monatlichen Rückzahlung
-------------------------- --------------------- -------------- ------------ ------------------------------------
 Pro Aktiv V.o.G.           Zahlungsrückstände    900,00         25,00        30,00
 Werkstatt Cardijn V.o.G.   Gerichtsvollzieher    1 200,00       33,33        40,00
 Behindertenstätten Eupen   Inkasso-Unternehmen   1 500,00       41,67        50,00
 **Total (3 Zeilen)**                             **3 600,00**   **100,00**   **120,00**
========================== ===================== ============== ============ ====================================
<BLANKLINE>


Filtering budgets
=================

The :menuselection:`Explorer --> Debt mediation --> Budgets` nenu
command shows the table of all budgets.

>>> kwargs = dict(column_names="id user date partner dist_amount")
>>> ses.show(debts.Budgets, **kwargs)
==== ================== ========== ================================================= =====================
 ID   Autor              Datum      Partner                                           Verteilbarer Betrag
---- ------------------ ---------- ------------------------------------------------- ---------------------
 1    Kerstin Kerres     22.05.14   Gerd & Tatjana Gerkens-Kasennova                  120,00
 2    Patrick Paraneau   22.05.14   Hubert & Judith Huppertz-Jousten                  120,00
 3    Romain Raffault    22.05.14   Jérôme & Theresia Jeanémart-Thelen                120,00
 4    Rolf Rompen        22.05.14   Denis & Mélanie Denon-Mélard                      120,00
 5    Robin Rood         22.05.14   Robin & Lisa Dubois-Lahm                          120,00
 6    Kerstin Kerres     22.05.14   Jérôme & Marie-Louise Jeanémart-Vandenmeulenbos   120,00
 7    Patrick Paraneau   22.05.14   Hubert & Gaby Frisch-Frogemuth                    120,00
 8    Romain Raffault    22.05.14   Paul & Paula Frisch-Einzig                        120,00
 9    Rolf Rompen        22.05.14   Paul & Petra Frisch-Zweith                        120,00
 10   Robin Rood         22.05.14   Ludwig & Laura Frisch-Loslever                    120,00
 11   Kerstin Kerres     22.05.14   Albert & Eveline Adam-Evrard                      120,00
 12   Patrick Paraneau   22.05.14   Albert & Françoise Adam-Freisen                   120,00
 13   Romain Raffault    22.05.14   Bruno & Eveline Braun-Evrard                      120,00
 14   Rolf Rompen        22.05.14   Bruno & Françoise Braun-Freisen                   120,00
                                                                                      **1 680,00**
==== ================== ========== ================================================= =====================
<BLANKLINE>


The nenu command :menuselection:`Debts mediation --> My budgets` shows
the budgets authored by the requesting user.


>>> ses.show(debts.MyBudgets, **kwargs)
==== ============ ========== ================================ =====================
 ID   Autor        Datum      Partner                          Verteilbarer Betrag
---- ------------ ---------- -------------------------------- ---------------------
 5    Robin Rood   22.05.14   Robin & Lisa Dubois-Lahm         120,00
 10   Robin Rood   22.05.14   Ludwig & Laura Frisch-Loslever   120,00
                                                               **240,00**
==== ============ ========== ================================ =====================
<BLANKLINE>


In order to see the budgets issued by other users, users can manually
select that other user in the filter parameter "Author".

>>> pv = dict(user=users.User.objects.get(username='kerstin'))
>>> kwargs.update(param_values=pv)
>>> ses.show(debts.Budgets, **kwargs)
==== ================ ========== ================================================= =====================
 ID   Autor            Datum      Partner                                           Verteilbarer Betrag
---- ---------------- ---------- ------------------------------------------------- ---------------------
 1    Kerstin Kerres   22.05.14   Gerd & Tatjana Gerkens-Kasennova                  120,00
 6    Kerstin Kerres   22.05.14   Jérôme & Marie-Louise Jeanémart-Vandenmeulenbos   120,00
 11   Kerstin Kerres   22.05.14   Albert & Eveline Adam-Evrard                      120,00
                                                                                    **360,00**
==== ================ ========== ================================================= =====================
<BLANKLINE>


Models
======

.. class:: Account

    An **account** is an item of an account chart used to collect
    ledger transactions or other accountable items.

    .. attribute:: name

        The multilingual designation of this account, as the users see
        it.


    .. attribute:: group

        The *account group* to which this account belongs.  This must
        point to an instance of :class:`Group`.
    
    .. attribute:: seqno

        The sequence number of this account within its :attr:`group`.
    
    .. attribute:: ref

        An optional unique name which can be used to reference a given
        account.

    .. attribute:: type

        The *account type* of this account.  This must
        point to an item of
        :class:`lino_welfare.modlib.debts.AccountTypes`.
    
           
.. class:: Budget
           
    A document which expresses the financial situation of a partner at
    a given date.

.. class:: Actor

    An **actor** of a budget is a partner who is part of the household
    for which the budget has been established.

           
.. class:: Entry
           
    A detail row of a :class:`Budget`.

    .. attribute:: budget

    The :class:`Budget` who contains this entry.

    .. attribute:: amount

        The amount of money. An empty amount is different from a zero
        amount in that the latter will be printed while the former
        not.

    .. attribute:: account

        The related :class:`Account`.

           

           
