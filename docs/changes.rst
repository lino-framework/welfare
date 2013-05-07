.. _welfare.changes: 

========================
Changes in Lino-Welfare
========================

See the author's :ref:`Developer Blog <blog>`
to get detailed news.
The final truth about what's going on is only 
`The Source Code <http://code.google.com/p/lino/source/list>`_
(hosted on `Googlecode <http://code.google.com/p/lino>`__).


Version 1.1.4 (coming)
============================================

- master_budget : Kopiervorlage für neue Budgets.
  Die Standard-Perioden und Standard-Beträge im Kontenplan sind nocht 
  sichtbar, werden aber ignoriert und kommen demnächst ganz raus
  (muss ich die automatisiert übernehmen?)

- :ref:`welfare.debts` : neue Kolonne :guilabel:`Gerichtsvollzieher` 
  in in :ref:`welfare.debts.Entries` : Alle Schulden können potentiell 
  irgendwann zum GV gehen, und dann wird diese Kolonne ausgefüllt 
  (indem man dort den GV auswählt).

- Beim Ausdruck unter der Tabelle "Guthaben, Schulden, Verpflichtungen" eine 
  weitere Tabelle "Gerichtsvollzieher", in der nur GV-Schulden sind.

- In Konfigurierung --> Site-Parameter gibt es ein neues Feld 
  "Gerichtsvollzieher", in dem anzugeben ist, welche Klientenkontaktart
  als "Gerichtsvollzieher" anzusehen ist. 
  Wenn dieses Feld leer ist, werden in der Auswahlliste des GV einer 
  Schuld alle Organisationen angezeigt.
  
- "Duplizieren ist total buggy" : zumindest in der momentanen 
  Development-Version kriege ich keine Probleme reproduziert.
  Ich höre auf mit aktiver Suche und warte mal auf euer Feedback 
  nach dem nächsten Release.


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

  

