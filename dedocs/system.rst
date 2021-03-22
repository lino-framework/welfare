.. doctest welfare_de/system.rst
.. _welfare.de.system:

====================
Systemkonfigurierung
====================


.. contents::
   :local:


Site-Parameter
==============

Menü :menuselection:`Konfigurierung --> System --> Site-Parameter`

- Site-Besitzer : das ÖSHZ, das diese Lino-Instanz betreibt.

- Nächste Partnernummer :  die Nummer, die beim Erstellen eines neuen
  Partners (egal welcher Art) als interne ID vergeben werden soll.

- Lokales Arbeitsamt :

- Budget-Kopiervorlage : das Budget, das als Kopiervorlage für neue Budgets dient.

- Sekretär : die Person, die als erster Unterzeichner fungiert.
- Präsident : die Person, die als zweiter Unterzeichner fungiert

  In dieser Auswahlliste stehen nur Personen, die für den `Site-Besitzer` als
  Kontaktperson mit der Funktion des ersten bzw. zweiten Unterzeichners haben.

  Für alle neu erstellten Verträge werden diese beiden Felder beim Erstellen in
  den betreffenden Vertrag kopiert.  Also wenn eines dieser Felder hier gändert
  wird, gilt die Änderung nur für Verträge, die nach dieser Änderung erstellt
  wurden. Die im Vertrag verwendeten Datumsfelder werden dabei nicht
  berücksichtigt.  Also wenn z.B. am Tag nach der Änderung des Präsidenten in
  der Konfigurierung noch ein Vertrag erfasst wird, der zwei Tage zuvor noch
  vom alten Präsidenten unterschrieben worden war, dann trägt Lino den neuen
  Präsidenten ein.

  Die Kopien dieser beiden Felder sind nicht sichtbar im Detail jedes einzelnen
  Vertrags.  Man kann sie für bestehende Verträge dennoch sehen und ggf.
  bearbeiten, indem man über :menuselection:`Explorer --> DSBE --> VSEs` bzw.
  :menuselection:`Explorer --> DSBE --> Art.60§7-Konventionen` die Tabelle
  öffnet und die beiden Kolonnen dort sichtbar schaltet.

  In den Hilfebestätigungen werden diese Felder nicht benutzt (dort steht immer
  "für den Präsidenten" und dann der Name des Benutzers.

- Funktion des ersten Unterzeichners : enthält üblicherweise "Sekretär"
- Funktion des zweiten Unterzeichners : enthält üblicherweise "Präsident/in"

  Die hier zur Auswahl verfügbaren Funktionen stehen unter
  :menuselection:`Konfigurierung --> Kontakte --> Funktionen`.


Benutzer
========

Sie auch
`The Lino Welfare Standard User Types <http://www.lino-framework.org/specs/welfare/usertypes.html>`__

Hilfetexte
==========

Hier könnte man für jedes einzelne Datenfeld einen eigenen Hilfetext
definieren. Wird nicht benutzt.  Die Hilfetexte werden durch den
Anwendungsentwickler im Programmcode gewartet.
