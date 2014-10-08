===========
To-Do-Liste
===========

.. contents:: 
   :local:
   :depth: 2



Zu besprechen
=============

#.  Soll jeder einen Hilfebeschluss bestätigen können?
    Oder nur der Benutzer, der als Bestätiger da steht?

#.  GrantingsByClient : abgelaufene Beschlüsse rausfiltern?

#.  `ConfirmationsByGranting` ist eine virtuelle Tabelle, deshalb
    funktioniert dort weder Doppelklick noch Delete.

#.  Wie sollen wir das Feld "Sozialhilfeart" ersetzen durch die
    Information aus `GrantingsByClient`: den ersten Beschluss? alle
    Beschlüsse? Und welche Hilfearten sind es, die im VSE erwähnt
    werden? Lebensmittelbank ja wahrscheinlich nicht.

#.  Wenn man auf den Zeitstempel eines ausgedruckten Auszugs klickt
    (`Certifiable.printed`), sollte oft direkt das Dokument kommen, nicht
    der Auszug. Aber manchmal will man doch auch auf den Auszug. Nämlich
    dann, wenn man das Dokument neu generieren lassen will. Also ein
    zweiter Link...

#.  Brauchen wir ein vereinfachtes Detail Klienten für Empfang?

#.  Soll Lino prüfen, ob Periode der Bescheinigung auch innerhalb der
    Periode des Beschlusses liegt?


#.  Wie soll es funktionieren, wenn ein einmal festgelegter und
    offiziel mitgeteilter Termin dann doch verschoben werden muss?
    Momentan kann man den Terminzustand auf "Verlegt" setzen und dann
    auf "per Mail" klicken, und in der Mail steht dann schon ein
    entsprechender Satz.

#.  Allgemeine Historik eines Klienten (als virtuelle Tabelle, die
    ihre "Chronik-Einträge" aus diversen Quellen zusammensucht, wäre
    technisch reizvoll `history.HistoricEvents.add(name, model, field)`)

    Rückfragen: Bitte genauer definieren, welchen Zweck diese Tabelle
    erfüllen soll.  Ich habe notiert "Wann war ein Klient das letzte Mal
    da? Was ist alles passiert?", aber das reicht mir nicht. Bitte ein
    konkretes Beispiel beschreiben. 

#.  Empfangsmodul: 
    Kann ein Klient eigentlich auf zwei Agenten zugleich warten? 
    Soll Lino das verhindern? 

#. Brauchen wir eine Tabelle der EiEi-Beträge?

   ============= ========= ======
   Kategorie     Seit wann Betrag
   ============= ========= ======
   Alleinstehend 
   ============= ========= ======

   --> bis auf weiteres nicht.

#.  Wer darf auf den Button "zur Hauptadresse machen" klicken?
    --> bis auf weiteres jeder.

Ideen für wenn wir mal Zeit haben
=================================

#.  An `auto_subscribe` option for a calendar: solche Kalender
    brauchen gar nicht erst explizit abonniert zu werden.
    
#.  Einladung zu einem Termin sollte ein ical haben, damit der
    Empfänger es in seinen Calendar-client importieren kann

#.  Validierung in drei Stufen: (grün) OK, (rot) nicht OK, (orange)
    Warnung. Zum Beispiel "Achtung, diese BIC ist eine andere als die,
    die Lino vorgeschlagen hätte". Ich könnte hier mit Zeilenfarben
    arbeiten, aber dann überschneidet sich das mit der Zeilenfarbe pro
    Status.

#.  Informationen aus Tx25 in die Datenbank reinholen bzw. an nützlichen
    Stellen anzeigen.




Bekannte Fehler und Fallen
==========================

#.  Wenn man den Begleitungszeitraum einer *Person* ändert, dann merkt
    Lino nicht, falls durch diese Änderung ein Vertrag ungültig wird.

#.  Versteckte Reiter werden nicht aktualisiert.  Das ist irritierend
    beim Arbeiten mit Budgets.  Z.B. im Reiter Vorschau muss man
    generell immer noch Refresh klicken, wenn man in den anderen
    Reitern Eingaben geändert hat.
    
    > Wenn ich die Kolonnenüberschriften bei den Akteuren ändere, stehen in
    > der Dropdown der Ausgaben immer noch die alten. Nur im "eigenen Fenster"
    > sind sie aktualisiert.

#.  Wenn man auf einem Auswertungstermin (der automatisch generiert
    wurde durch eine VSE oder Art.60§7), auf "Duplizieren" klickt,
    dann dupliziert Lino ihn zwar intern, löscht ihn aber anschließend
    gleich wieder, weil die VSE die komplette Serie neu generiert. Zu
    analysieren, wann so eine Aktion da überhaupt Sinn macht.

