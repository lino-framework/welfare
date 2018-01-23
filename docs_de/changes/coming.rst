================
Kommende Version
================

- Die Mitarbeiter des Sekretariats/Backoffice/Empfang können jetzt
  zusätzlich die Reiter "Kalender" und "Verträge" sehen.

- In Klienten kann man jetzt per Schnellsuche wieder nach Adresse und
  Nationalregisternummer suchen (so wie es früher schon mal war).

- Tipp : um einen Klienten nach seiner Partnernummer zu finden, kann
  man im Schnellsuche-Feld ein "#" vor die Nummer setzen.

- Ungefragte Änderung: Es gibt jetzt einen Quicklink `[Suchen]`, mit
  dem man eine Schnellsuche in allen Tabellen auf einmal durchführen
  kann. Feedback erwünscht.

- Deutlichere Fehlermeldung im Fall eines Problems bei der Verbindung
  zur Datenbank.

- `Prüfung Datumsbereich Beschlüsse & Bescheinigungen`_  

  

Prüfung Datumsbereich Beschlüsse & Bescheinigungen
--------------------------------------------------

Wir haben endlich die Erklärung für :ticket:`1354` gefunden : es ist
üblich, dass ein Hilfebeschluss zunächst ohne Enddatum registriert
wird, und dass daraus dann eine Serie von Bestätigungen ebenfalls
ohne Enddatum erstellt werden. Wenn dann irgendwann der Beschluss
abgeschlossen wird, dann setzt der verantwortliche Sozi auf dem
Beschluss ein Enddatum ein und erstellt ggf einen neuen
Beschluss. Was Lino in diesem Moment nicht meldete, war, dass
dadurch -zumindest für Lino- alle Bescheinigungen ungültig wurden,
deren Enddatum leer war : Wenn der Beschluss ein bekanntes Enddatum
hat, dann darf die Bescheinigung nicht ohne Enddatum sein. Diese
Regel hat bis März 2017 regelmäßig zum Verlust von Bescheinigungen
geführt, weil Lino den Regelverstoß erst bei der Datenmigration
bemerkte und betroffene Bescheinigungen löschte. Ich schrieb dir
dann zwar immer, dass auch wieder eine Serie von ungültigen
Bescheinigungen gelöscht worden waren, aber weil keiner eine Ahnung
hatte, worum es genau ging, habt ihr euch erst Anfang 2017 erstmals
beschwert, dass manche Bescheinigungen nicht mehr in Lino drin sind,
obschon sie eindeutig in Lino erstellt und gedruckt worden
waren. Woraufhin ich die -wie wir annahmen allzu strenge- Regel
entfernt habe. Seitdem hatten die Benutzer Narrenfreiheit und haben
dann auch prompt versehentlich neue Bescheinigungen zu alten
Hilfebeschlüssen ausgedruckt.

Soweit die Erklärung. Jetzt mein Lösungsvorschlag.

  1) ich entschärfe die Regel : wenn der Beschluss ein Enddatum hat,
     dann darf das Enddatum der Bescheinigung leer sein. Wenn sie
     eines hat, dann darf es nicht nach dem Enddatum des Beschlusses
     liegen.

  2) mit der entschärften Regel lassen wir den Integritätstest
     (checkdata) neu laufen. Dadurch werden die momentan 682
     Fehlwarnungen auf ein paar Dutzend echte Warnungen reduziert.

  3) Ich schalte die (entschärfte) Prüfung wieder auf "hart" (also
     Lino prüft es schon bei der Eingabe, nicht erst im nächtlichen
     checkdata).

Frage an euch : Aber was machen wir dann mit diesen paar Dutzend
echten Warnungen? Beispiel: AMK/01.10.14/22346/4232. Also das sind
Bescheinigungen, deren Datenbereich tatsächlich ungültig ist. Wenn
wir die (entschärfte) Prüfung wieder auf hart schalten, dann würden
diese echt falschen Bescheinigungen wieder gelöscht.

a) Das wollen wir nicht, denn die sind ja ausgestellt worden und
   rausgegangen. Also Lino muss ein System kriegen, mit dem man
   solche Datenprobleme dann "absegnen" kann, also dass man Lino
   irgendwie mitteilt "Ja, Bescheinigung X verstößt gegen die Regel,
   aber wir drücken da ausnahmsweise ein Auge zu".

b) Es ist uns egal, wenn Lino diese Bescheinigungen
   löscht. Hauptsache, dass die entschärfte Regel wieder aktiviert
   wird und es zukünftig nicht mehr zu solchen echten Fehlern kommt.

