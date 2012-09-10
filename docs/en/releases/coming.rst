Coming
======

TODO

- Ist Person.is_client jetzt readonly auf importierten Personen? 

- statt "AJAX communication failed" sollte er zumindest sagen 
  "IntegrityError: column national_id is not unique", oder (die Luxus-Version) 
  "Kann Person X nicht zu einem Klienten machen, weil Klient Y noch keine NISS bekommen hat"
  
- Tabellen "Coachings" (Begleitungen) und "Thirds" ("Drittpartner" oder "Externe Kontakte") 
  und ThirdType


DONE

- Lino unterscheidet jetzt zwischen Klienten und Personen.
  Unter "Personen" verstehen wir *alle Menschen, die Lino kennt*. 
  Das sind nicht nur Klienten, sondern auch die Benutzer, 
  alle Kontaktpersonen in Firmen oder Institutionen,
  ...
  "Klienten" sind Personen, über die Lino mehr wissen will als über normale 
  Leute. Um einen Klienten anzulegen, 
  muss man mindestens auch die NISS eingeben.
  
  Im Detail einer Person gibt es ein Feld "ist Klient". 
  Damit kann man eine bestehende Person zu einem Klienten machen.
  
- Neues Feld Status eines Klienten. 
  is_active ersetzt durch ClientStates.active, 
  newcomer ersetzt durch ClientStates.newcomer.
  
- Neue Tabelle "Begleitungen" ersetzt die bisherigen Felder `Begleitet von/bis` und 
  `Begleiter 1 und 2`. Siehe auch Begleitungsart (primär, sekundär). 

- Neue Felder "Erstellt am/um" und "Letzte Änderung" pro `Partner`.
  
- Tx25 : ein paar neue TI handler.  
  
- Bug "Imbiss Firat": watch_tim konnte seit 20120728 nicht mehr von 
  Person nach Firma konvertieren. Also z.B. wenn man die MWSt-Nr 
  eines Partners in TIM löschte. Dann kam die Fehlermeldung 
  "Aus TIM importierte Partner d\xfcrfen nicht gelöscht werden."

- countries.City.type und Partner.region.
  Visible in Detail of "All Partners" : Lino now features a field "region" 
  to specify addresses. For Belgian addresses it contains the *province*.
  This field is not usually present in Belgian sites because it's not needed 
  in our small country. But for a U.S. address 
  for example it would contain the state.

- Es gibt eine neue Tabelle "Kontenpläne" (Account Charts), in der bis 
  auf weiteres jedoch nur ein einziger Kontenplan "debts Default" steht. 
  Später kommt dort mindestens ein weiterer Kontenplan "Buchhaltung" hinzu.

- Database migration is automatic.
  Details see :func:`lino_welfare.modlib.pcsw.migrate.migrate_from_1_4_10`.
  
- Note that version number jumps down from 1.4.10 to 0.1
  Lino (the framework) changes to version 1.5.0, but this is no longer relevant 
  for database migrations. Lino/Welfare starts with 0.1.
  