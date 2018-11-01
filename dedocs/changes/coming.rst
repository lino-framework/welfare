================
Kommende Version
================

Vorankündigungen für die kommende Version.

NB: Für diese Version gibt es noch keine Vorschau.

TODO

- :ticket:`2619` Vertragspartner einer VSE per Doppelklick eingeben.

  Vorschläg : Für die nächste Version ein insert_layout definieren mit
  den Feldern company und contact_person. Ein summary view mit
  Insert-Button (wie bei den Notizen) scheint mir hier Overkill, weil
  es selten mehr als 15 Vertragspartner gibt.
  

Zu testen  
  
- Das Detail einer Anwesenheit ist jetzt in einem kleineren Fenster,
  denn der größte Teil des Bildschirms war sowieso unbenutzt.  Und in
  manchen Ansichten zeigte Lino nicht `Klient` sondern `Partner` an.
  Obwohl in Lino Welfare werden Anwesenheiten nur für Klienten erfasst
  werden, nie für andere Leute.
  (20181008)

Vorschläge für neue Features

- Desktop Notifications (:ticket:`923`).  Vorteile: (1) akustisches
  Signal, (2) kommt auch dann, wenn Lino minimiert ist, (3) belastet
  den Server nicht unnötig.
  Diese Änderung sollte vor der Einführung von den Benutzern
  ausprobiert werden können, denn DN bedeuten eine Änderung des
  Benutzerverhaltens: statt den Lino-Bildschirm offen zu halten und ab
  und zu drauf zu schauen, müssen sie sich daran gewöhnen, auf
  Desktop-Notifications zu achten. Davon abgesehen ist die
  Konfiguration der Clients nicht trivial: Wie lange bleiben sie am
  Bildschirm sichtbar? Kann man ihre Dauer auf "endlos" stellen?  Wie
  kann man ein akustisches Signal einstellen? Wie gehen die Benutzer
  bisher mit "Meine Mitteilungen" in Lino um?

- Neue Tabelle :class:`lino.modlib.users.UserRoles` könnte
  hilfreich sein beim Formulieren von Änderungswünschen
  bzgl. Zugriffsrechten. (20181008)

- Lino könnte jetzt row-level edit locking für Klienten.
  
- Optional auf Anfrage: intelligente Ansicht Termine auch für
  cal.EntriesByClient?

  
