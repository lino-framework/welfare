===============
Auszüge
===============


.. **Vorbemerkung für Eupener**

  Im Dezember 2015 wird im ÖSHZ Eupen der Empfang von TIM nach Lino
  umsteigen.  Das, was in TIM als "Bescheinigungen" lief, haben wir
  für Lino ziemlich stark umgekrempelt.  Auf den ersten Blick scheint
  das alles viel komplizierter und unflexibler als in TIM.
  Sozialarbeiter gehen lieber mit Menschen um als mit Computern.

  Aber wir haben Grund zur Hoffnung, dass ihr schon auf den zweiten
  Blick --nach Eingewöhnung-- erkennen werdet, dass das neue System
  mit den Hilfebeschlüssen und standardisierten Bescheinigungen eure
  tägliche Arbeit *spürbar erleichtert*.

  Und nicht nur das: weil das neue System deutlich strukturierter ist,
  wird es euch langfristig helfen, eure Arbeit *besser* zu machen,
  also euren Klienten besser zu helfen.



Was ist ein Auszug?
===================

Wenn man mit Lino etwas druckt, nennt Lino das einen **Auszug aus
seiner Datenbank**.  Jeder Ausdruck wird als *Auszug* in der Tabelle
der *Auszüge* gespeichert.

Statt **Auszug** kann man also in der Praxis einfachheitshalber auch
**Ausdruck** sagen.  Aber es ist eben nicht genau das Gleiche.  Ein
Auszug kann entweder "ausgedruckt" sein oder auch nicht -- wobei
Letzteres natürlich anormal ist und wahrscheinlich irgendeinen
technischen Grund hat. Ungedruckte Auszüge werden voraussichtlich in
Zukunft mal jede Nacht automatisch gelöscht.

Ein Auszug hat folgende Datenfelder:

- Autor : welcher Bentuzer den Auszug erstellt hat.
- Auszugsart : welche Auszugsart es ist. Siehe Auszugsarten_
- Klient : welchem Klienten der Auszug zugewiesen ist.


Auszugsarten sind :menuselection:`Konfigurierung
--> Büro --> Auszugsarten` konfigurierbar.

Auszugsarten
============

Pro Auszugsart gibt es folgende Datenfelder:

- ID
- Bezeichnung
- Modell
- Konstruktionsmethode : welche Druckmethode verwendet wird.
- Vorlage : Welche Vorlage beim Ausdruck verwendet wird
- Textkörper-Vorlage
- E-Mail-Vorlage
- Ecerpt-Shortcur
- Primär
- Kontakt drucken
- Bescheinigend
- Empfänger drucken
- Backward compatible
- Als Anhang per E-Mail


Anwesenheitsbescheinigung
=========================

Um eine Anwesenheitsbescheinigung auszustellen, muss der Klient
"anwesend" gewesen sein.  Also es muss ein :term:`Termin` oder eine
:term:`Visite` existieren, für die dieser Klient als Gast eingetragen
ist.  Diese Einträge sind es, die man sieht im Feld "Termine" des
Reiters "Person" im Detail des Klienten.


Hilfebestätigungen
==================

Siehe :doc:`aids`.

.. _welfare.excerpts.examples.de:

Beispiele von von Ausdrucken aus der Demo-Datenbank
===================================================

Hier einige Beispiele von Ausdrucken aus der Demo-Datenbank.

.. lino2rst::

   from lino_xl.lib.excerpts.doctools import show_excerpts
   print(show_excerpts())

Siehe auch die technische Dokumentation in :ref:`welfare.specs.aids`.
