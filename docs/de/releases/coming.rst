Die kommende Version
====================

Neue Features
-------------

- Funktion "eID-Karte einlesen" kann getestet werden. 
  Bilder liest er noch nicht ein.
  Auch manche Angaben wie z.B. die Stadt könnten Probleme machen. 

Bugfixes
--------

- Art-60-7-Konvention hatte noch kein insert_layout

- Beim Erstellen einer Art-60-7-Konvention gab es noch einige Probleme, 
  unter anderem die Tracebacks
  "'InsertRow' object has no attribute 'run'"
  und
  "'dict' object has no attribute 'status_code'".

- Nach Bearbeiten einer Zelle einer Grid sprang der Cursor wieder an 
  die erste Zelle der Tabelle.

- Schuldnerberatung. 
  Wenn im Feld "Einleitung" eines Budgets z.B. "Grüße" stand, dann wurde "Gr&uuml;&szlig;e" gedruckt.

- UsersWithClients nur für Benutzer anzeigen, die die Berechtigung haben.

- Wenn ein Klient mehr als einen Vertrag hat, die alle vergangen sind, dann gilt der 
  zuletzt begonnenen Vertrag als aktiv. Beispiel Klient 22538.
