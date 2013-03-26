.. _welfare.tested.misc:

Miscellaneous
=============

>>> from lino.runtime import *
>>> ses = settings.SITE.login('rolf')
>>> ses.show(jobs.NewJobsOverview) #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
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


>>> ses.show(users.Teams) #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
==== =================================================== ============================== ===============================
 ID   Bezeichnung                                         Bezeichnung (fr)               Bezeichnung (nl)
---- --------------------------------------------------- ------------------------------ -------------------------------
 1    ASD (Allgemeiner Sozialdienst)                      SSG (Service social général)   ASD (Algemene Sociale Dienst)
 2    DSBE (Dienst für Sozial-Berufliche Eingliederung)   Service intégration
 3    Schuldnerberatung                                   Médiation de dettes
==== =================================================== ============================== ===============================
<BLANKLINE>


>>> ses.show(pcsw.CoachingTypes) #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
=================================================== ============================== =============================== ====
 Bezeichnung                                         Bezeichnung (fr)               Bezeichnung (nl)               ID
--------------------------------------------------- ------------------------------ ------------------------------- ----
 ASD (Allgemeiner Sozialdienst)                      SSG (Service social général)   ASD (Algemene Sociale Dienst)   1
 DSBE (Dienst für Sozial-Berufliche Eingliederung)   Service intégration                                            2
 Schuldnerberatung                                   Médiation de dettes                                            3
=================================================== ============================== =============================== ====
<BLANKLINE>
