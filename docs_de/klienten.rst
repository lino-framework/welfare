Klienten
========

Ein Klient ist eine Person, für die wir eine Serie von zusätzlichen
Daten erfassen.

Für Klienten gibt es drei **Tabellenansichten**, die sich durch
Kolonnenreihenfolge und Filterparameter unterscheiden:

- "Alle Klienten" 
  (Menü :menuselection:`Kontakte --> Klienten`) : 
  allgemeine Liste, die jeder Benutzer sehen darf.

- DSBE-Klienten
  (Menü :menuselection:`DSBE --> Klienten`)
  spezielle Liste für die Kollegen im DSBE.
  Zeigt immer nur **begleitete** Kunden. 
  Hier kann man keine neuen Klienten anlegen.

- Neue Klienten
  (Menü :menuselection:`Neuanträge --> Klienten`):
  spezielle Liste für die Zuweisung von Neuanträgen.

N.B.  Das Detail, das bei Doppelklick angezeigt wird, ist bei allen
drei Ansichten das Gleiche.  *Was* im Detail alles angezeigt wird
(bzw. was nicht), das hängt jedoch von den Zugriffsrechten ab (sh.
*Benutzerprofil*, :attr:`ml.users.User.profile`).

Eine vierte Tabellenansicht ist :menuselection:`Empfang --> Klienten`:
das ist eine spezielle Liste für den Empfangsschalter, die ihr eigenes
Detail-Layout hat.

Technische Details sind in Englisch unter :class:`welfare.pcsw.Client`
dokumentiert.
