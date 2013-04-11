.. _welfare.tested.misc:

Miscellaneous
=============

.. include:: /include/tested.rst
  
>>> from lino.runtime import *
>>> ses = settings.SITE.login('rolf')
>>> ses.set_language('de')
>>> ses.show(jobs.Jobs,column_names="name provider sector") #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
================= ================================ ===========================
 Name              Stellenanbieter                  Sektor
----------------- -------------------------------- ---------------------------
 Kellner           BISA                              Landwirtschaft & Garten
 Kellner           R-Cycle Sperrgutsortierzentrum    Horeca
 Koch              R-Cycle Sperrgutsortierzentrum    Seefahrt
 Koch              Pro Aktiv V.o.G.                  Unterricht
 Küchenassistent   Pro Aktiv V.o.G.                  Medizin & Paramedizin
 Küchenassistent   BISA                              Reinigung
 Tellerwäscher     BISA                              Bauwesen & Gebäudepflege
 Tellerwäscher     R-Cycle Sperrgutsortierzentrum    Transport
================= ================================ ===========================
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
