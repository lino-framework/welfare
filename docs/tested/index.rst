.. _welfare.tested:

Tested documents
================

This section contains just some doctests, its primary goal is to 
get tested.
OTOH these are instructions you can re-play interactively in any Django 
shell on your own database, or write them to a script and run it 
using `manage.py run`.


>>> from lino.runtime import *
>>> obj = debts.Budget.objects.get(pk=3)
>>> print obj.BudgetSummary().to_rst()
========================================================= ==============
 Beschreibung                                              Betrag
--------------------------------------------------------- --------------
 Monatliche Einkünfte                                      5 000,00
 Jährliche Einkünfte (2 400,00 / 12)                       200,00
 Monatliche Ausgaben                                       -550,00
 Monatliche Reserve für jährliche Ausgaben (236,00 / 12)   -19,67
 Raten der laufenden Kredite                               -45,00
 **Finanzielle Situation**                                 **4 585,33**
========================================================= ==============
<BLANKLINE>


>>> print jobs.NewJobsOverview.to_rst(username='rolf') #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
+--------------------------------------------------------------+------------------------------+-----------------+-----------------+
| Stelle                                                       | Arbeitet                     | Kandidaten      | Probezeit       |
+==============================================================+==============================+=================+=================+
| **Kellner** bei **BISA** (1)                                 | **RADERMACHER** bis ...      | **BASTIAENSEN** | **EMONTSPOOL**  |
|                                                              |                              |                 |                 |
|                                                              | **CHANTRAINE** bis ...       | **ÖSTGES**      |                 |
+--------------------------------------------------------------+------------------------------+-----------------+-----------------+
| **Kellner** bei **R-Cycle Sperrgutsortierzentrum** (1)       | **VAN VEEN** bis ...         | **JANSEN**      | **CHANTRAINE**  |
|                                                              |                              |                 |                 |
|                                                              | **DOBBELSTEIN** bis ...      | **BASTIAENSEN** | **RADERMECKER** |
+--------------------------------------------------------------+------------------------------+-----------------+-----------------+
| **Koch** bei **R-Cycle Sperrgutsortierzentrum** (1)          | **RADERMECKER** bis ...      | **RADERMACHER** | **JOHNEN**      |
|                                                              |                              |                 |                 |
|                                                              | **FAYMONVILLE** bis ...      |                 | **CHANTRAINE**  |
+--------------------------------------------------------------+------------------------------+-----------------+-----------------+
| **Koch** bei **Pro Aktiv V.o.G.** (1)                        | **DUBOIS** bis ...           | **DOBBELSTEIN** | **RADERMACHER** |
|                                                              |                              |                 |                 |
|                                                              | **HILGERS** bis ...          | **BRECHT**      |                 |
+--------------------------------------------------------------+------------------------------+-----------------+-----------------+
| **Küchenassistent** bei **Pro Aktiv V.o.G.** (1)             | **JEANÉMART** bis ...        | **LAMBERTZ**    | **EVERTZ**      |
|                                                              |                              |                 |                 |
|                                                              | **JOUSTEN** bis ...          | **DOBBELSTEIN** | **DUBOIS**      |
+--------------------------------------------------------------+------------------------------+-----------------+-----------------+
| **Küchenassistent** bei **BISA** (1)                         | **LAZARUS** bis ...          | **RADERMACHER** | **LAZARUS**     |
|                                                              |                              |                 |                 |
|                                                              |                              |                 | **EVERTZ**      |
+--------------------------------------------------------------+------------------------------+-----------------+-----------------+
| **Tellerwäscher** bei **BISA** (1)                           | **MEIER** bis ...            | **FAYMONVILLE** | **DI RUPO**     |
|                                                              |                              |                 |                 |
|                                                              |                              | **SAFFRE**      |                 |
+--------------------------------------------------------------+------------------------------+-----------------+-----------------+
| **Tellerwäscher** bei **R-Cycle Sperrgutsortierzentrum** (1) | **RADERMACHER** bis ...      | **MEIER**       | **GROTECLAES**  |
|                                                              |                              |                 |                 |
|                                                              |                              | **FAYMONVILLE** | **KASENNOVA**   |
+--------------------------------------------------------------+------------------------------+-----------------+-----------------+
<BLANKLINE>


>>> print users.Teams.to_rst(username='rolf') #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
==== =================================================== ============================== ===============================
 ID   Beschreibung                                        Beschreibung (fr)              Beschreibung (nl)
---- --------------------------------------------------- ------------------------------ -------------------------------
 1    ASD (Allgemeiner Sozialdienst)                      SSG (Service social général)   ASD (Algemene Sociale Dienst)
 2    DSBE (Dienst für Sozial-Berufliche Eingliederung)   Service intégration
 3    Schuldnerberatung                                   Médiation de dettes
==== =================================================== ============================== ===============================
<BLANKLINE>


>>> print pcsw.CoachingTypes.to_rst(username='rolf') #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
=================================================== ============================== =============================== ====
 Beschreibung                                        Beschreibung (fr)              Beschreibung (nl)               ID
--------------------------------------------------- ------------------------------ ------------------------------- ----
 ASD (Allgemeiner Sozialdienst)                      SSG (Service social général)   ASD (Algemene Sociale Dienst)   1
 DSBE (Dienst für Sozial-Berufliche Eingliederung)   Service intégration                                            2
 Schuldnerberatung                                   Médiation de dettes                                            3
=================================================== ============================== =============================== ====
<BLANKLINE>
