Coming
======

TODO
----

Was ich noch machen muss:

- Aktions-Dialoge (wird benötigt für Aktion "Ablehnen" eines Neuantrags)

- watch_tim

- Datenübernahme macht noch ein paar Warnungen

- Ausdruck Art. 60§7-Übersicht produziert leeres PDF

- Personensuchen und Begleitungen

- Benutzer ohne Gruppe ``integ`` sehen trotzdem die DSBE-spezifische 
  Tabelle "Benutzer und ihre Klienten" im Hauptbildschirm.
  
- Wenn Admin als Alicia arbeitet, sieht er in `Meine Begleitunge`  
  dennoch nur die Seinen, nicht die von Alicia.


Feedback erwünscht
------------------

Wo ich bei Gelegenheit auf deine Ideen hoffe:

- Arbeitsablauf Klienten und Begleitungen testen und dokumentieren.
  Siehe :doc:`/user/clients`.

- Das Hauptmenü ist stellenweise verwirrend. Konkrete Ideen?

- Alicia (z.B.) hat nach der Migration 80 Einträge in To-Do-Liste. 
  Das ist nicht realistisch.



Nach dem Release
----------------

- Verträge .odt : 
  `self.contact.person` ersetzen durch `self.contact_person` 
  `self.contact.type` ersetzen durch `self.contact_role` 


Lösung gemeldeter Probleme
--------------------------

- Kontaktperson löschen geht nicht.
  "Bei einer Firma wechselt der Direktor. 
  In den Kontaktpersonen der Firma wollen wir den alten 
  Direktor nicht mehr sehen,
  aber es gibt Verträge, bei denen er die Firma vertritt."
  --> in den Verträgen (VSE und Art 60-7) wurde das bisherige 
  Feld `contact` ersetzt durch zwei Felder `contact_person` 
  und `contact_function`. 
  Benutzung wie bisher, aber man kann jetzt in der Tabelle 
  ContactsByCompany Zeilen löschen, 
  auch wenn ein Vertrag mit dieser Kontaktperson existiert. 
  Oder wenn eine Kontaktperson vom GF zum Direktor avanciert, 
  kann man dort nun einfach das "GF" durch "Direktor" ersetzen, ohne 
  dass anschließend alle alten Verträge (nach einem "Cache löschen") 
  mit "Direktor" gedruckt würden.
  
- Tx25 hat ein paar neue TI handler.
  
- Bug "Imbiss Firat": watch_tim konnte seit 20120728 nicht mehr von 
  Person nach Firma konvertieren. Also z.B. wenn man die MWSt-Nr 
  eines Partners in TIM löschte. Dann kam die Fehlermeldung 
  "Aus TIM importierte Partner d\xfcrfen nicht gelöscht werden."

- AG-Sperren: Feld "Begründung" darf jetzt leer sein.  

- Wenn hochgeladene Datei Sonderzeichen im Namen hat, werden diese ab jetzt auf dem Server durch Unterstriche ersetzt (statt dass Lino im "Bitte warten..."-Modus steckenbleibt und der Systemverwalter per E-Mail einen Traceback  `UnicodeEncodeError 'ascii' codec can't encode character u'...' in position ...: ordinal not in range(128)` kriegt.

- "Ich habe 7 Kunden die unter VSE sind für einen Sprachkurs.
  Aber in meiner Liste "Klienten" sind die Spalten "Vertrag beginnt" 
  und "Vertrag endet" leer" 
  -->
  "Das war ein Bug. Die VSEs dieser Leute beginnen erst in der Zukunft,
  und Lino denkt sich dann "die sind noch nicht aktiv, die interessieren
  keinen". Was natürlich falsch ist."
  Behoben.



Neue Features
--------------

- Willkommensgruß. Die Idee ist, dass dort idealerweise keine Warnungen stehen sollten.

- Lino unterscheidet jetzt zwischen Klienten und Personen.
  Unter "Personen" verstehen wir *alle Menschen, die Lino kennt*. 
  Das sind nicht nur Klienten, sondern auch Benutzer, 
  Kontaktpersonen in Firmen oder Institutionen usw.
  "Klienten" sind Personen, über die Lino mehr wissen will als über normale 
  Leute. 
  
  Im Detail einer Person gibt es ein Feld "ist Klient". 
  Damit kann man eine bestehende Person zu einem Klienten machen.
  
- Neue Tabelle "Klientenkontakte" ersetzt und erweitert die bisherigen Felder 
  `Ansprechpartner ADG`, `Krankenkasse`, und `Apotheke`.
  
- Neue Tabelle "Begleitungen" ersetzt die bisherigen Felder `Begleitet von/bis` und 
  `Begleiter 1 und 2`. "Begleitungsart" ist Synonym für "Dienst" (umbenennen?).
  Eine *primäre* Begleitung ist, was aus `TIM->IdUsr` importiert wurden.
  
- Arbeitsablauf Klienten und Begleitungen. 
  haben ein neues Feld "Status". 
  Das frühere Feld `is_active` wurde ersetzt durch Status "Begleitet", 
  das frühere Feld `newcomer` durch Status "Neuantrag".
  Siehe :doc:`/user/clients`.
  
- Neue Tabelle "Änderungen" auf Klienten und Verträgen zeigt 
  geloggte Änderungen im Webinterface statt in der `system.log`.

- Neue Felder "Erstellt am/um" und "Letzte Änderung" pro `Partner`.
  
- :menuselection:`Neuanträge --> Neue Klienten` hat jetzt einen Reiter "Neuanträge", 
  wo Caroline u.a. die "verfügbaren Begleiter" sehen kann und per Mausklick zuweisen kann.
  

Nebenwirkungen  
--------------

- Das Menü "Meine Klienten" hat jetzt kein Untermenü mehr mit allen 
  Integrationsphasen, weil man das jetzt in den Parametern von 
  "Meine Klienten" angeben kann. 
  
- Die automatische Erinnerung "Begleitung endet in 1 Monat" wird momentan 
  nicht gemacht. Ist das schlimm?
  
- Diverse Umstrukturierungen im Hauptmenü.  
  
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
  
- Note that version number jumps down from 1.4.10 to 0.1.0
  Lino (the framework) changes to version 1.5.0, but this is no longer relevant 
  for database migrations. Lino/Welfare starts with 0.1.0.
  
