Coming
======

- Lino unterscheidet jetzt zwischen Klienten und Personen.
  Unter "Personen" stehen alle Menschen, die Lino kennt. 
  Das sind nicht nur Klienten, sondern auch Benutzer und Kontaktpersonen 
  in Firmen oder Institutionen.
  Klienten sind Personen, über die Lino mehr wissen will als über normale 
  Leute. Um einen Klienten anzulegen, 
  muss man mindestens auch die NISS kennen.

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