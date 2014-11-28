======
Preise
======

Preise in Eurocent pro Einwohner zzgl. MWSt

- Grundfunktionen_ : 16
- DSBE_ : 15
- Kalender_ : 8
- Kurse_ : 8
- Neuzugänge_ : 5
- Haushalte_ : 5
- Empfang_ : 5
- Hilfebescheinigungen_ : 7
- Schuldnerberatung_ : 7
- Umfragen_ : 8
- Ateliers_ : 8


Grundfunktionen
===============

- Kontakte : Partner, Personen, Organisationen, Klienten, Adressen
- Begleitungen, Dienste
- Notizen
- uploads : Dateien hochladen
- excerpts : Ausdrucke, Historik
- outbox : E-Mails verschicken
- Export nach Calc oder Excel


Haushalte
=========

Partnerart "Haushalte", Haushaltszusammensetzungen, Familiäre Beziehungen
(:mod:`ml.households`, :mod:`ml.humanlinks`)


DSBE
====

- Lebensläufe (:mod:`welfare.cv`)
- VSEs, Stellenanbieter und Art.60§7-Konventionen
  (:mod:`welfare.isip`, :mod:`welfare.jobs`)
- DSBE-Statistiken (:mod:`welfare.integ`)

Kalender
========

Terminplanung, Gästelisten, Einladungen, Anwesenheiten

Empfang
=======

Am Empfangsschalter wird registriert, wer ankommt und zu wem er will.
Die Sozialarbeiter können von ihrem Bildschirm aus sehen, welche Klienten
im Warteraum sitzen.
(:mod:`welfare.reception`)

Neuzugänge
==========

Die Mitarbeiter werden in Fachbereiche aufgeteilt.  Neue Anträge auf
Sozialhilfe werden nach konfigurierbaren Parametern auf die
Mitarbeiter verteilt.

(:mod:`welfare.newcomers`)


Hilfebescheinigungen
====================

Hilfebeschlüsse in Lino erfassen und
Bescheinigungen drucken.  (:mod:`welfare.aids`)

Kurse
=====

Klienten werden in Kurse eintragen. 
Kursanfragen. Kandidatenliste an Kursanbieter. 
Historik der Teilnahmen und Resultate.


Schuldnerberatung
=================

Budgets erstellen und ausdrucken  (:mod:`welfare.debts`)

Umfragen
========

Man konfiguriert sich Fragebögen, die man mit den Klienten beantwortet.

Ateliers
========

Ähnlich wie Kurse_, aber der "Kursanbieter" ist das ÖSHZ selber.
Optional können pro Atelier Termine im Kalender generiert und
Anwesenheiten erfasst werden.


Optionen
========


- :mod:`ml.extensible` : Grafischer Kalender 
- **eId-Karten einlesen** :mod:`ml.beid`, :ref:`eidreader`
- :mod:`welfare.cbss` : Kommunikation mit Zentralbank (BCSS, ZDSS)
- :ref:`davlink` : Writer oder Word starten von Lino aus
