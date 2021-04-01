====================
Alte Release-Notizen
====================

.. toctree::
   :maxdepth: 1
   :glob:

   2017*
   1.*


Version 1.1.25 (released :blogref:`20150918`)
=============================================

- Changed license from BSD to AGPL (:ticket:`528`)
- Miscellaneous bugfixes

Version 1.1.24 (released :blogref:`20150901`)
=============================================

- Changed Development Status from beta to stable.
- Lots of changes, especially the murder bug (:blogref:`20150831`)



Version 1.1.23 (released :blogref:`20150825`)
=============================================


Version 1.1.21
===============

- 20150130 : new field `jobs.ContractType.full_name`


Version 1.1.19 
====================================

- After the upgrade you can uninstall the `north` and `djangosite`
  packages since Lino no longer needs them.
- Changes in database see :meth:`migrate_from_1_1_18
  <lino_welfare.migrate.Migrator.migrate_from_1_1_18>`.

Database migration as usual, but you must manually edit your
:xfile:`restore.py` file:

- Replace "from north.dpy" by "from lino.utils.dpy".
- Replace "from north.dbutils" by "from lino.core.dbutils".



Version 1.1.14 (released 2014-06-24)
====================================

- A :class:`welfare.isip.Contract` can now have more than one external
  partner. New table :class:`welfare.isip.PartnersByContract`

Version 1.1.13 released (2014-06-20)
====================================

- Configuring :mod:`lino.modlib.excerpts` is getting user-friendly.


Version 1.1.12 (released 2014-05-27)
====================================

- User documentation in German see :doc:`1.1.12`

- Manuell nach Migration:

  - `migrate_from_1_1_10.py` ausführen

  - ExamPolicies: Wochentage ankreuzen.

  - Drei UploadTypes (Führerschein, als "wanted" markieren.

  - SiteConfig --> Constants : Neue Felder ausfüllen

  - Prüfen, ob manuell bearbeitete Lebenläufe übernommen wurden.

  - Notizart "Lebenslauf" löschen. 

  - Neue Klientenkontaktart "Inkassounternehmen" erstellen.  Diese und
    auch "Gerichtsvollzieher" kriegen die neue Checkbox "Beitreiber"
    angekreuzt.

  - Alle bestehenden Inkassounternehmen als solche markieren

.. _welfare_1_1_11:

Version 1.1.11 (intermediate unreleased version)
================================================

(was needed for a data migration in chatelet)  

Version 1.1.10 (released :blogref:`20131007`)
=============================================

Just some bugfixes:

- Man geht bei den Neuzugängen auf Partner 23995 und versucht ihn
  abzulehnen ... Paf kommt der Internal Server Error!
- Expected a list of 12 values, but got [u'01.09.2013', u'false', u'false', u'']  

- `jobs.JobsOverview` zeigt Kandidaten jetzt mit 
  "NAME Vorname (Nummer)" statt nur NAME.

- das Feld PAR->Name2 aus TIM wurde von watch_tim bisher einfach ignoriert.
  Kommt jetzt in das neue Feld "Adresszeile vor Straße".  

Version 1.1.9 (released :blogref:`20130924`)
============================================

Changed :meth:`Client.get_active_contract 
<lino_welfare.modlib.pcsw.models.Client.get_active_contract>`
as requested by the users: "Don't look into the past or future, 
only today matters".


Weitere Arbeiten im Modul :mod:`Empfang <welfare.reception>`.

Änderungen im Menü : 
Die Menübefehle 
:menuselection:`DSBE --> Übersicht Art.60§7-Konventionen`
und
:menuselection:`DSBE --> Tätigkeitsbericht`
befinden sich jetzt unter 
:menuselection:`Listings --> DSBE`.
Siehe auch den neuen Abschnitt 
`welfare.de.admin_main`
im Benutzerhandbuch.



Bugs fixed:

- Tätigkeitsberiicht, Übersicht Art-60§7-Konventionen und sonstige 
  HtmlBoxen wurden nicht angezeigt.
  
- Übersicht Art-60§7-Konventionen : wenn man im Parameter-Panel 
  eine Stellenart auswählte, kam Fehlermeldung 
  "'JobType' object is not iterable"

Sonstige:

- Neuanträge werden jetzt immer grün angezeigt, 
  Ehemalige und Abgelehnte immer gelb.
  Klienten, die als veraltet markiert sind, werden jetzt generell 
  mit einem Sternchen hinter der Partnernummer angezeigt.
  
- :menuselection:`Neuanträge --> Klienten`: 
   "Neue Klienten seit" war par défaut leer statt "vor einem Monat".
   Reihenfolge und Bezeichnungen der Felder für Filterparameter optimiert. 
   
- Ausdruck nach PDF : hier kann man jetzt zwischen Hoch- und Querformat 
  wählen. Und in Partnerlisten gibt es eine dritte Auswählmöglichkeit 
  "Etiketten".

- Neuer Management-Befehl dump2py sollte ab jetzt für Backups verwendet 
  werden statt dumpdata.

  

Version 1.1.8 (released :blogref:`20130723`)
============================================

- Neues Modul "Empfang" (:mod:`welfare.reception` und Änderungen im
  Kalendermodul.

  Neues Benutzerprofil "Empfangsschalter".
  Neues Menü :menuselection:`Empfang` mit den 
  Befehlen 
  :class:`welfare.reception.Clients`
  :class:`reception.ExpectedGuests`
  und :class:`reception.WaitingVisitors` 

  Konfigurierung: 
  `cal.Calendar` hat jetzt ein neues Feld 
  `invite_client`, welches für 
  Klientengespräche angekreuzt ist
  (zumindest in der Demo-Datenbank. Produktionsdaten nach Release manuell 
  anpassen). 
  SiteConfig hat drei neue Felder:
  client_calender client_guestrole und team_guestrole

- Filter-Panel in Klientenliste:
  Zwei neue Beobachtungskriterien "VSE" und "Art-60§7-Konvention".
  Ermöglicht Antworten auf Fragen im Stil
  "Nur Klienten anzeigen, die am 12.03.2012 einen VSE laufen hatten."
  (Hubert 20130603 14:48)

- Menübefehl :menuselection:`Schuldnerberatung --> Budget-Vorlage` 
  jetzt auch für Kerstin sichtbar.

-  Menübefehle :menuselection:`Konfigurierung --> DSBE --> Funktionen` 
   und einige andere jetzt auch für Melanie wieder sichtbar.

- `courses.PendingCourseRequests`: 
  Fixed a bug which caused a traceback 
  "Cannot resolve keyword 'provider' into field."
  when filtering on course provider in PendingCourseRequests.
  Added a new filter parameter "Course offer".
      
- Auswahllisten auf ChoiceLists mit *blank=True* haben jetzt 
  auch einen leeren Eintrag.

- Re-built a new self-signed `DavLink.jar` file included with Lino 
  because the old one had expired. (:blogref:`20130704`)
  
- Wenn man als jemand anderer gearbeitet hatte und dann zurück als 
  "ich selbst" schalten wollte,
  dann kam manchmal ein JS-Fehler 
  "Uncaught TypeError: Cannot read property 'main_item' of null".
  (:blogref:`20130704`)
  
- Export nach CSV funktionierte nicht 
  in Tabellen, die mindestens ein DisplayField hatten
  (:blogref:`20130719`).
  
- Ändern der Reihenfolge der Einträge eines Budgets:
  hier waren diverse Bugs.
  
  Overridden `get_siblings` for `debts.Entry` so that up/down 
  actions no longer fail when seqno's are spread accross 
  different account_types.
  (:blogref:`20130613`)
  
  Außerdem (:blogref:`20130706`):

    - die erste Zeile hatte unlogischerweise einen Up-Button
      und die letzte einen Down-Button. Jetzt nicht mehr.
    - Statt der Wörter "Up" und "Down" sieht man jetzt zwei grüne Pfeile.
    - in "Verpflichtungen" und "Vermögen" fehlten die move_buttons

- `daemoncommand.py` and Django 1.5

  


Version 1.1.7 (released :blogref:`20130604`)
============================================

- Weiter mit dem `Tätigkeitsbericht <integ.ActivityReport>`.

- Fixed: 
  Server error 500 beim Versuch, eine Tabelle als csv-Datei 
  (nach Excel) zu exportieren.
  
- Fixed:
  Server error 500 beim Versuch, eine Aufgabe als erledigt zu markieren
  
- watch_tim : datum_bis einer primären Begleitung eines Ehemaligen darf
  nicht leer sein. Wenn es das ist, setzt watch_tim es jetzt 
  auf 01.01.1990 setzen. 
  
  - `bis` : entweder leer (wenn es eine aktive Begleitung ist) 
    oder 01.01.1990 (wenn es ein Neuzugänge oder ehemaliger Klient ist)
  
  
Version 1.1.6 (released :blogref:`20130527`)
============================================

- Erweiterungen in den Parameter-Panels für 
  `Klienten <pcsw.Client>`, 
  `VSEs  <isip.Contract>`
  und 
  `Art.60§7-Konventionen  <jobs.Contract>`.
  Neues Parameter-Panel für Tabelle
  `Begleitungen`(`pcsw.Coaching`,)
  
  Theoretisch müssten alle besprochenen Datenbank-Abfragen 
  :blogref:`20130516` jetzt machbar sein.
  Aber der Tätigkeitsbericht (sh. nächster Punkt) ist eine automatische 
  Hintereinanderreihung von solchen Abfragen.

- Neues Listing `Tätigkeitsbericht <integ.ActivityReport>`. 
  Inhaltlich basiert das auf unserem Analysegespräch,
  ist aber zu verstehen als Arbeitsgrundlage 
  und Demonstration der neuen technischen Möglichkeiten.
  Die Benutzer sollten mir nun schrittweise mitteilen, 
  welche Informationen zu viel sind und welche fehlen.
  
  Der Tätigkeitsbericht ist das erste Anwendungsbeispiel für die 
  geniale neue Klasse :class:`lino.mixins.Report`. 
  Ein Report ist eine in Python definierte Serie von Sektionen, 
  freien Texten und Lino-Tabellen und kann sowohl am Bildschirm 
  als auch als `.pdf` oder `.odt` gerendert werden.

- Neuimplementierung der Startseite: die Größe der einzelnen 
  Bildschirmkomponenten wird jetzt korrekt dargestellt. 
  Nebenwirkungen:
  
  - "Verpasste Erinnerungen" ist nicht mehr da
    (darauf hat m.E. sowieso niemand je geschaut).
  - `Benutzer und ihre Klienten <integ.UsersWithClients>` 
    kann man nicht mehr
    direkt "im eigenem Fenster öffnen" (aber dafür gibt es ja
    den Menübefehl
    :menuselection:`Listings --> Benutzer und ihre Klienten`).



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
    
- Subtle changes in `welfare.watch_tim`.

Version 1.1.4 (released :blogref:`20130512`)
============================================

- `jobs.JobsOverview` : 
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

- :mod:`welfare.debts` : neue Kolonne :guilabel:`Gerichtsvollzieher` 
  in :class:`welfare.debts.Entry` : Alle Schulden können potentiell 
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
  und der Dokumentation (`welfare.watch_tim`).

  


Version 1.1.3 (released :blogref:`20130505`)
============================================

- Im "Resultat" einer Tx25 (:class:`cbss.RetrieveTIGroupsRequest`  
  wurde nichts angezeigt. Behoben.

- `courses.PendingCourseRequests`. 
  (:menuselection:`Kurse --> Offene Kursanfragen`) 
  hat jetzt zwei neue Kolonnen "Arbeitsablauf" und "Begleiter".
  Ausserdem ein umfangreiches Panel für Filterkriterien. 
  Kursanfragen haben einen neuen Zustand "Inaktiv". 
  Zustand "Kandidat" umbenannt nach "Offen".
  
- Ausdruck `jobs.JobsOverview` 
  (:menuselection:`DSBE --> Übersicht Art60*7`)
  funktioniert jetzt.
  Diese Liste ist im Menü "DSBE" und nicht im Menü "Listings".
  Ich habe vor, das Menü "Listings" demnächst komplett 
  rauszuschmeissen.
  
- Verständlichere Benutzermeldung wenn man VSE erstellen will und 
  die Vertragsart anzugeben vergisst.
  
- Adding a new account in `accounts.Accounts`
  caused an internal server error `DoesNotExist`.
  
- Wenn in TIM eine PLZ bearbeitet wurde, loggt watch_tim
  jetzt statt einer Exception "PLZ no such controller"  
  nur eine info() dass die Änderung ignoriert wird.
  
- In `debts.EntriesByBudget` kann man die Zeilen jetzt 
  rauf und runterschieben. Experimentell. 
  Ich warte auf erste Eindrücke.
  Im Kontenplan lässt sich so ein Auf und Ab nur schwer rechtfertigen.
  Eigentlich brauchen wir die Notion von Budget-Vorlagen: ein betimmtes 
  Budget wird als Vorlag deklariert, und 

- :menuselection:`Site --> About` didn't display
  the application's version.
  
- `auto_fit_column_widths` was ignored when a table was being 
  displayed as the main grid of a window.
  
- Beim Ausdruck eines `debts.Budget`: 
  fehlte in der Tabelle "Guthaben, Schulden, Verpflichtungen" 
  die Kolonne "Monatsrate".

- `StrangeClients` produced a traceback
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

- The `Merge` action on `pcsw.Client` and 
  `contacts.Company` had disappeared. 
  Fixed.
  
  Also this action is no longer disabled for imported partners.
  
- The new method :meth:`lino.core.model.Model.subclasses_graph`
  generates a graphviz directive which shows this model and the 
  submodels.
  the one and only usage example is visible in the 
  `Lino-Welfare user manual
  <https://welfare-user.lino-framework.org/fr/clients.html#partenaire>`_
  See :blogref:`20130401`.

Version 1.1.1 (released 2013-03-29)
===================================

- Changes before 1.1.1 are not listed here.
  See the developers blog and/or the Mercurial log.

  

