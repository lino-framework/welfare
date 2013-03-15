To-do list
==========

#.  implement the fields Client.applies_from and applies_until as :ref:`summary_fields`. 

#.  Wenn man den Begleitungszeitraum einer *Person* ändert, dann merkt Lino nicht,
    falls durch diese Änderung ein Vertrag ungültig wird.

#.  Wie soll es funktionieren, wenn ein einmal festgelegter und offiziel 
    mitgeteilter Termin dann doch verschoben werden muss?
    Momentan kann man den Terminzustand auf "Verlegt" setzen und dann auf 
    "per Mail" klicken, und in der Mail steht dann schon ein entsprechender Satz.

#.  Wenn `invite_team_members` angekreuzt ist und Gäste automatisch erstellt 
    werden, dann stehen die trotzdem noch nicht auf "Eingeladen".

#.  Brauchen wir die Notion von "Teams"? Oder besser Partnerlisten?
    Momentan ist die Konfigurierung etwas skurril: 
    jeder Benutzer stellt sich "sein Team" zusammen.
    Pro Kalender sollte neben `invite_team_members` auch stehen, 
    welches das Team ist.
    
#.  Und in einem könnten wir auch eine Option `auto_subscribe` 
    in Calendar machen: solche Kalender brauchen gar nicht erst 
    explizit abonniert zu werden.
    
#.  Einladung sollte ein ical haben, damit der Empfänger es in seinen
    Calendar-client importieren kann

#.  Wenn man auf einem Auswertungstermin (der automatisch generiert wurde 
    durch eine VSE oder VBE), auf "Duplizieren" klickt, dann dupliziert Lino 
    ihn zwar intern, löscht ihn aber anschließend gleich wieder, weil die 
    VSE die komplette Serie neu generiert. Zu analysieren, wann so eine 
    Aktion da überhaupt Sinn macht. 

#.  Versteckte Reiter werden nicht aktualisiert. 
    Das ist irritierend beim Arbeiten mit Budgets. 
    Z.B. im Reiter Vorschau muss man generell immer noch Refresh klicken, 
    wenn man in den anderen Reitern Eingaben geändert hat. Oder
    
    > Wenn ich die Kolonnenüberschriften bei den Akteuren ändere, stehen in
    > der Dropdown der Ausgaben immer noch die alten. Nur im "eigenen Fenster"
    > sind sie aktualisiert.

