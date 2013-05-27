.. _welfare.changes: 

========================
Changes in Lino-Welfare
========================

See the author's :ref:`Developer Blog <blog>`
to get detailed news.
The final truth about what's going on is only 
`The Source Code <http://code.google.com/p/lino/source/list>`_.


Version 1.1.6 (coming)
============================================

- Fixed: 
  Beim Ausdruckversuch einer Excelliste bei Klienten Suchfilter kommt
  Fehlermeldung... "Server Error (500)"

- Neues Listing "Tätigkeitsbericht".
  Inhaltlich ist das momentan ein Sammelsurium 
  dessen, was ich von unserem Analysegespräch behalten habe.
  Zu verstehen als Arbeitsgrundlage und Demonstration dessen, was
  technisch möglich ist.

- Erweiterungen in den Parameter-Panels für Klienten, VSEs 
  und Art.60§7-Konventionen.
  Neues Parameter-Panel für Begleitungen.
  Theoretisch müssten alle besprochenen Datenbank-Abfragen 
  manuell machbar sein.
  Der Tätigkeitsbericht ist ja eigentlich nur eine automatische 
  Hintereinanderreihung von solchen Abfragen.

- Neuimplementierung der Startseite:
  - Größe der einzelnen Bildschirmkomponenten ist jetzt korrekt.
  - "Verpasste Erinnerungen" ist nicht mehr da
    (da hat sowieso nie jemand nach geschaut).
  - "Benutzer und ihre Klienten" kann man nicht mehr
    direkt "im eigenem Fenster öffnen", sondern dazu muss man 
    :menuselection:`Listings --> Benutzer und ihre Klienten` 
    aufrufen.





Version 1.1.5 (released :blogref:`20130520`)
============================================

Statistik DSBE:

2)  Neue Felder in der Tabelle "Vertragsbeendigungsgründe":

    - Checkbox "Art.60-7"
    - Checkbox "VSE"
    - Checkbox "Erfolg" --> ob es sich um eine "erfolgreiche" Beendigung
      im Sinne des Tätigkeitsberichts handelt.
    - Checkbox "vorzeitig" --> ob Beendigungsdatum ausgefüllt sein muss

3)  Neues Feld "Ausbildungsart" eines VSE (isip.Contract.study_type). 
    Pro VSE-Vertragsart eine
    Checkbox "Ausbildungsart" (isip.ContractType.needs_study_type), 
    die besagt, ob man dieses Feld ausfüllen muss oder nicht.
    Die Liste der möglichen Ausbildungsarten ist die gleiche wie die, 
    für den Lebenslauf im Reiter "Ausbildung" der Klienten.
    (Falls nötig könnten wir auch eine eigene Tabelle dafür machen.)

4)  Neues Feld "Beendigungsgrund" einer Begleitung.
    Neue Tabelle "Begleitungsbeendigungsgründe" mit Einträgen wie z.B.
    "Übergabe an Kollege", "Einstellung des Anrechts auf SH", "Umzug in
    andere Gemeinde", "Hat selber Arbeit gefunden",... Ein Feld:
    - Dienst (optional) --> wenn ausgefüllt, darf dieser Grund nur für
    Begleitungen in diesem Dienst angegeben werden)

5)  Neue Tabelle "Dispenzen" ("Befreiungen von der Verfügbarkeit auf dem
    Arbeitsmarkt") pro Klient : Datum von / Datum bis / Grund, sowie
    Konfigurationstabelle der Dispenzgründe (z.B. "Gesundheitlich",
    "Studium/Ausbildung", "Familiär", "Sonstige",....)

Miscellaneous:

-   bugfix 'City' object has no attribute '_change_watcher_spec'
    :blogref:`20130520`
    
- Subtle changes in :ref:`welfare.watch_tim`.

Version 1.1.4 (released :blogref:`20130512`)
============================================

- :ref:`welfare.jobs.NewJobsOverview` : 
  Seitenwechsel zwischen die verschiedenen Kategorien 
  (Majorés, Intern, usw.).
  
  Genauer gesagt ist es jetzt so, dass Lino einen Seitenwechsel 
  innerhalb der Tabellen unterdrückt. Falls zwei Kategorien auf 
  eine Seite passen, kommt kein Seitenwechsel.

- Neues Feld SiteConfig.debts_master_budget ("Budget-Kopiervorlage").

  Die Standard-Perioden und Standard-Beträge im Kontenplan sind noch 
  sichtbar, werden aber nur benutzt 
  solange keine Kopiervorlage angegeben ist. 
  In den Site-Parametern wird ein "leeres" Budget ausgewählt, 
  das wir nach dem Upgrade eigens dazu anlegen.
  Aber der näcshten Version kommen die Standard-Perioden und 
  Standard-Beträge im Kontenplan ganz raus.
  Der neue Menübefehl 
  :menuselection:`Konfigurierung --> Schuldnerberatung --> Budget-Kopiervorlage`,
  und der ist auch für Kerstin sichtbar.

- :ref:`welfare.debts` : neue Kolonne :guilabel:`Gerichtsvollzieher` 
  in in :ref:`welfare.debts.Entries` : Alle Schulden können potentiell 
  irgendwann zum GV gehen, und dann wird diese Kolonne ausgefüllt 
  (indem man dort den GV auswählt).

- Beim Ausdruck unter der Tabelle "Guthaben, Schulden, Verpflichtungen" eine 
  weitere Tabelle "Gerichtsvollzieher", in der nur GV-Schulden sind.

- In :menuselection:`Konfigurierung --> Site-Parameter` gibt es ein neues Feld 
  "Gerichtsvollzieher", in dem anzugeben ist, welche Klientenkontaktart
  als "Gerichtsvollzieher" anzusehen ist. 
  Wenn dieses Feld leer ist, werden in der Auswahlliste des GV einer 
  Schuld alle Organisationen angezeigt.
  
- "Duplizieren ist total buggy" : zumindest in der momentanen 
  Version kriege ich keine Probleme reproduziert.
  Ich höre auf mit aktiver Suche und warte mal auf euer Feedback 
  nach dem nächsten Release.
  
- Ein Bug, den niemand bemerkt hatte: Lino-Welfare protokollierte
  keinerlei Änderungen mehr. Behoben.

- Unerwünschte Neuzugänge.
  Ein Lauf mit tim2lino und watch_tim hatte ca 200 "Neuzugänge" geschaffen, 
  die eigentlich gar keine waren. Subtile Änderungen in 
  :mod:`watchtim <lino_welfare.management.commands.watchtim>`
  und der Dokumentation (:ref:`welfare.watch_tim`).

  


Version 1.1.3 (released :blogref:`20130505`)
============================================

- Im "Resultat" einer Tx25 (:ref:`welfare.cbss.RetrieveTIGroupsRequest`  
  wurde nichts angezeigt. Behoben.

- :ref:`welfare.courses.PendingCourseRequests`. 
  (:menuselection:`Kurse --> Offene Kursanfragen`) 
  hat jetzt zwei neue Kolonnen "Arbeitsablauf" und "Begleiter".
  Ausserdem ein umfangreiches Panel für Filterkriterien. 
  Kursanfragen haben einen neuen Zustand "Inaktiv". 
  Zustand "Kandidat" umbenannt nach "Offen".
  
- Ausdruck :ref:`welfare.jobs.NewJobsOverview` 
  (:menuselection:`DSBE --> Übersicht Art60*7`)
  funktioniert jetzt.
  Diese Liste ist im Menü "DSBE" und nicht im Menü "Listings".
  Ich habe vor, das Menü "Listings" demnächst komplett 
  rauszuschmeissen.
  
- Verständlichere Benutzermeldung wenn man VSE erstellen will und 
  die Vertragsart anzugeben vergisst.
  
- Adding a new account in :ref:`welfare.accounts.Accounts`
  caused an internal server error `DoesNotExist`.
  
- Wenn in TIM eine PLZ bearbeitet wurde, loggt watch_tim
  jetzt statt einer Exception "PLZ no such controller"  
  nur eine info() dass die Änderung ignoriert wird.
  
- In :ref:`welfare.debts.EntriesByBudget` kann man die Zeilen jetzt 
  rauf und runterschieben. Experimentell. 
  Ich warte auf erste Eindrücke.
  Im Kontenplan lässt sich so ein Auf und Ab nur schwer rechtfertigen.
  Eigentlich brauchen wir die Notion von Budget-Vorlagen: ein betimmtes 
  Budget wird als Vorlag deklariert, und 

- :menuselection:`Site --> About` didn't display
  the application's version.
  
- `auto_fit_column_widths` was ignored when a table was being 
  displayed as the main grid of a window.
  
- Beim Ausdruck eines :ref:`welfare.debts.Budget`: 
  fehlte in der Tabelle "Guthaben, Schulden, Verpflichtungen" 
  die Kolonne "Monatsrate".

- :ref:`welfare.pcsw.ClientsTest` produced a traceback
  `'NoneType' object has no attribute 'strip'` for Clients 
  with national_id is None.
  


Version 1.1.2 (released :blogref:`20130422`)
============================================


- fixed problems reported by users

  - pdf-Dokument aus Startseite (UsersWithClients) erstellen:
    kommt leider nur ein leeres Dok-pdf bei raus

  - excel-Dokument  aus Startseite erstellen:
    kommt zwar ein Dok bei raus, aber leider nur mit Kode-Zahlen als 
    Titel / nicht die eigentlichen Spalten-Titel, wie in der Übersicht
    Startseite. etwas unpraktisch, da die Titel der Spalten 
    neu eingetippt werden müssen.
    
  - Could not print Tx25 documents
    ("'Site' object has no attribute 'getlanguage_info'")
    
  - (and maybe some more...)

- The `Merge` action on :ref:`welfare.pcsw.Client` and 
  :ref:`welfare.contacts.Company` had disappeared. 
  Fixed.
  
  Also this action is no longer disabled for imported partners.
  
- The new method :meth:`lino.core.model.Model.subclasses_graph`
  generates a graphviz directive which shows this model and the 
  submodels.
  the one and only usage example is visible in the 
  `Lino-Welfare user manual
  <http://welfare-user.lino-framework.org/fr/clients.html#partenaire>`_
  See :blogref:`20130401`.

Version 1.1.1 (released 2013-03-29)
===================================

- Changes before 1.1.1 are not listed here.
  See the developers blog and/or the Mercurial log.

  

