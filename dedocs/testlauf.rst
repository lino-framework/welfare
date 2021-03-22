==========================
Allgemeine Testanweisungen
==========================

- Auf einem Klienten mehrere VSEs und Art60§7 erstellen und ausdrucken.
- Einen Hilfebeschluss erstellen und einen VSE, der darauf verweist.



Navigation im Detail-Fenster
----------------------------

- Anmelden als Administrator
- :menuselection:`Kontakte --> Klienten`.
- Doppelklick auf einem Klienten der Liste, der nicht importiert ist.

- Beachte oben rechts die *message area* des Navigators:
  dort steht etwas im Stil "Record 4 von 57".

- Im Reiter "Sonstiges" das Feld "veraltet" einschalten.

- Sich den Namen des Klienten merken und dann Speichern.
  Nach dem Speichern prüfen:

- ist der Klient noch der Gleiche?
- wurden alle vier Navigationsbuttons deaktiviert?
- steht die message area des Navigators auf "No navigation"?


Speichern
---------

- :menuselection:`Kontakte --> Partner (alle)`.

- Doppelklick auf dem ersten Partner der Liste

- Im Navigator ist der Button "Vorige Seite" deaktiviert, die anderen drei Buttons nicht

- Auf einem *aus TIM importierten* Partner:

  - Ohne vorher was zu ändern den Speichern-Button klicken.
    Dadurch sollte sich nichts verändern und es dürfte keine Änderung
    im Änderungslog erscheinen.



- Auf einem Partner, der nicht importiert ist:

  - Checkbox "veraltet" ankreuzen, Speichern. Bleibt sie angeschaltet?
  - Wieder ausschalten und wieder speichern. Bleibt sie ausgeschaltet?


Sprachkenntnisse
----------------

- Im Reiter "Sprachen" eine neue Sprache in "Sprachkenntnisse" eingeben.
  Die Änderung wird gleich nach Verlassen der Zelle in der :xfile:`system.log`
  erscheinen.
  Dann den Speichern-Button der Person klicken.
  Dabei sollte nichts passieren und es dürfte *keine Änderung*
  in der :xfile:`system.log` erscheinen.
  :blogref:`20110406`

Polymorphie
-----------

- Detail einer Organisation aufrufen, die *kein Kursanbieter* ist.

  Ohne vorher was zu ändern den Speichern-Button klicken.
  Dabei sollte nichts passieren und es dürfte *keine Änderung* in der system.log erscheinen.
  :blogref:`20110406`

  Checkbox "Kursanbieter" einschalten und speichern.
  Die Checkbox sollte angeschaltet bleiben.

  In einem zweiten Browserfenster :menuselection:`Kurse-->Kursanbieter` aufrufen:
  die Firma sollte dort nun sichtbar sein.

  Checkbox "Kursanbieter" wieder ausschalten und speichern.
  Die Checkbox sollte ausgeschaltet bleiben.

  Im zweiten Browserfenster auf "Refresh" klicken :
  Firma sollte aus der Liste verschwunden sein.

  :blogref:`20110406`

Einfügetexte
------------

- Notiz erstellen. Im Inhalt ein bisschen eintippen,
  einige Einfügetexte einfügen, speichern, drucken.
  Nach den Drucken sind die meisten Felder schreibgeschützt (blau).
  Auf :guilabel:`Cache löschen` klicken (Felder werden wieder bearbeitbar).
  Eine kleine Änderung im Inhalt machen, speichern, drucken.
  Prüfen, ob Änderung auch im Ausdruck sichtbar ist.

- Eine weitere Notiz erstellen.
  Folgenden Textabschnitt (Quelle: Wikipedia) kopieren und einfügen:

    **Interpunktionsregeln bei Aufzählungen**

    Grundsätzlich werden aus Sicht der Interpunktionsregeln Aufzählungszeichen so behandelt, als seien sie nicht vorhanden. Das heißt, dass Interpunktion so gesetzt werden muss, als gäbe es keine typografische Gliederung.

    Beispiel:

      Der Mann erblickte ein gelbes Auto, einen schwarzen Hund, eine grüne Handtasche und ein braunes Pferd in seiner Küche.

    Dieser Satz wird zu folgendem:

      Der Mann erblickte

      - ein gelbes Auto,
      - einen schwarzen Hund,
      - eine grüne Handtasche
      - und ein braunes Pferd

      in seiner Küche.

  Speichern & drucken.
