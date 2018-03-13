================
Kommende Version
================

Zur Zeit unter **testlino** einsehbar.

- **Kontauszüge um den Jahreswechsel herum** wurden bisher nicht
  importiert, weil Lino da einen Fehlalarm "different years" auslöste.
  In der testlino kann man das jetzt noch nicht sehen, aber wenn die
  neue Version aktiviert worden ist, müssten die fehlenden Auszüge
  automatisch (nach dem nächsten Import) erscheinen.

- `Prüfung Datumsbereich Beschlüsse & Bescheinigungen`_ (siehe unten)
  
- Die Mitarbeiter des Sekretariats/Backoffice/Empfang (Benutzerart 210
  "Empfangsschalter") können jetzt auch die Reiter "Kalender" und
  "Verträge" sehen.

- In Klienten kann man jetzt wieder **per Schnellsuche nach Adresse
  und Nationalregisternummer** suchen (so wie es früher schon mal
  war).

- Tipp : um einen Klienten nach seiner ID (Partnernummer) zu finden,
  kann man im Schnellsuch-Feld ein "#" vor die Nummer setzen.  Das
  Gleiche gilt auch für Verträge, Auszüge etc.


- Lino schlug par défaut "Pflegemutter" statt "Mutter" vor.

- Beim Einfügen eines Termins vom Klienten aus ist das Dialogfenster
  optimiert: Enddatum steht dort jetzt nicht mehr, und die Eintragsart
  wurde hinzugefügt.

- Eine ungefragte Änderung: Es gibt jetzt einen Quicklink `[Suchen]`,
  mit dem man eine **Schnellsuche in allen Tabellen** auf einmal
  durchführen kann. Momentan ist die Funktion nur sichtbar für
  Systemverwalter. Feedback erwünscht.

- Deutlichere Fehlermeldung im Fall eines Problems bei der Verbindung
  zur Datenbank.

- Die Buttons im Fenster "Meine Einstellungen" sind jetzt oben (wie
  gewohnt) statt unten. Und jetzt haben sie auch alle einen Hilfetext.


Prüfung Datumsbereich Beschlüsse & Bescheinigungen
--------------------------------------------------

Wir haben die Erklärung für :ticket:`1354` gefunden : es ist üblich,
dass ein Hilfebeschluss zunächst ohne Enddatum registriert wird, und
dass daraus dann eine Serie von Bestätigungen ebenfalls ohne Enddatum
erstellt werden. Wenn dann irgendwann der Beschluss abgeschlossen
wird, dann setzt der verantwortliche Sozi auf dem Beschluss ein
Enddatum ein und erstellt ggf einen neuen Beschluss. Was Lino in
diesem Moment nicht meldete, war, dass dadurch -zumindest für Lino-
alle Bescheinigungen ungültig wurden, deren Enddatum leer war : Wenn
der Beschluss ein bekanntes Enddatum hat, dann darf die Bescheinigung
nicht ohne Enddatum sein. Diese Regel hat bis März 2017 regelmäßig zum
Verlust von Bescheinigungen geführt, weil Lino den Regelverstoß erst
bei der Datenmigration bemerkte und betroffene Bescheinigungen
löschte. Ich berichtete dann zwar immer, dass wieder eine Serie von
ungültigen Bescheinigungen gelöscht worden waren, aber weil keiner
eine Ahnung hatte, worum es genau ging, habt ihr euch erst Anfang 2017
erstmals beschwert, dass manche Bescheinigungen nicht mehr in Lino
drin sind. Woraufhin ich die -wie wir annahmen allzu strenge- Regel
entfernt habe. Aber seitdem hatten die Benutzer Narrenfreiheit und
haben dann auch prompt versehentlich neue Bescheinigungen zu alten
Hilfebeschlüssen ausgedruckt.

Soweit die Erklärung. Jetzt die Lösung bzw. der Anfang davon.

1) ich habe die Regel entschärft : wenn der Beschluss ein Enddatum
   hat, dann darf das Enddatum der Bescheinigung leer sein. Wenn sie
   eines hat, dann darf es nicht nach dem Enddatum des Beschlusses
   liegen.

2) mit der entschärften Regel haben wir den Integritätstest
   (checkdata) neu laufen lassen. Dadurch wurden die ursprünglich 682
   Fehlwarnungen auf ein paar Dutzend echte Warnungen reduziert.

TODO: Ich sollte die (entschärfte) Prüfung wieder auf "hart" schalten,
damit Lino es schon bei der Eingabe prüft und nicht erst im
nächtlichen checkdata.

Aber was machen wir dann mit diesen paar Dutzend echten Warnungen?
Beispiel: AMK/01.10.14/22346/4232. Also das sind Bescheinigungen,
deren Datenbereich tatsächlich ungültig ist. Wenn wir die
(entschärfte) Prüfung wieder auf hart schalten, dann würden diese echt
falschen Bescheinigungen wieder gelöscht.  Was sagt ihr dazu? Ich sehe
zwei Möglichkeiten:

a) Das wollen wir nicht, denn die sind ja ausgestellt worden und
   rausgegangen. Also Lino muss ein System kriegen, mit dem man
   solche Datenprobleme dann "absegnen" kann, also dass man Lino
   irgendwie mitteilt "Ja, Bescheinigung X verstößt gegen die Regel,
   aber wir drücken da ausnahmsweise ein Auge zu".

b) Es ist uns egal, wenn Lino diese Bescheinigungen
   löscht. Hauptsache, dass die entschärfte Regel wieder aktiviert
   wird und es zukünftig nicht mehr zu solchen echten Fehlern kommt.

