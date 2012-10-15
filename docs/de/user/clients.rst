========
Klienten
========


Klienten
========

Klienten gibt es momentan in drei Tabellen, die sich durch Kolonnenreihenfolge 
und Filterparameter unterscheiden:

- "Alle Klienten" 
  (Menü :menuselection:`ÖSHZ --> Klienten`) : 
  allgemeine Liste, die jeder Benutzer sehen darf.

- DSBE-Klienten
  (Menü :menuselection:`DSBE --> Klienten`)
  Zeigt immer nur **begleitete** Kunden. 
  Hier kann man keine neuen Klienten anlegen.
  Die Reiter Kompetenzen, Verträge... finden sich nur hier.
  
- Neue Klienten
  (Menü :menuselection:`Neuanträge --> Klienten`):
  spezielle Liste für die Zuweisung von Neuanträgen.

N.B. 
Das Detail, das bei Doppelklick angezeigt wird, 
ist bei allen drei Listen das Gleiche. 
Das hängt vom :doc:`Benutzerprofil </user/userprofiles>` ab.





Arbeitsabläufe
==============

Wortschatz:

- Workflow : Arbeitsablauf
- Life cycle : Lebenzyklus
- engl. "State" = Zustand oder Stadium

  


Arbeitsablauf eines Klienten
----------------------------

.. graphviz:: 
   
   digraph foo {
      newcomer -> refused [label="Neuantrag ablehnen"];
      newcomer -> coached [label="Begleiter zuweisen"];
      refused -> newcomer [label="Neuantrag wiederholen"];
      coached -> newcomer [label="Begleitung abbrechen"];
      coached -> former [label="Begleitung beenden"];
      invalid -> newcomer [label="NISS wurde korrigiert"];
      
      newcomer [label="Neuantrag"];
      refused [label="Abgelehnt"];
      invalid [label="Ungültig"];
      former [label="Ehemalig"];
      coached [label="Begleitet"];
   }





Der Zustand eines Klienten kann sein:

- **Neuantrag** : 
  Die Person hat Antrag auf Begleitung gestellt. 
  Antrag wird überprüft und der Klient muss einem Sachbearbeiter 
  oder Sozi zugewiesen werden.
  
  Im Detail-Reiter 
  :screen:`Neuanträge <pcsw.Client.detail.newcomers>`
  kann man einem Neuzugang 
  einen **Begleiter zuweisen**, wodurch der Klient ins Stadium "Begleitet" wechelt.
  
- **Abgelehnt** : 
  Die Prüfung des Antrags hat ergeben, dass diese Person kein Anrecht 
  auf Begleitung durch unser ÖSHZ hat.
  
- **Begleitet** :
  Damit ein Klient im Status "Begleitet" sein kann, muss mindestens 
  eine aktive Begleitung existieren
  (diese Regel gilt jedoch nicht für importierte Klienten).

- **Ehemalig** :
  Es existiert keine *aktive* Begleitung.
  
- **Ungültig** :
  Klient ist laut TIM weder Ehemalig noch Neuantrag, 
  hat aber keine gültige NISS.
  
  
  


Begleitungen
------------

.. graphviz:: 
   :caption: Arbeitsablauf einer Begleitung
   
   digraph foo {
      suggested -> refused [label="[ablehnen]"];
      standby -> refused;
      suggested -> active [label="[akzeptieren]"];
      standby -> active [label="[reaktivieren]"];
      active -> standby;
      standby -> ended [label="[beenden]"];
      active -> ended [label="[beenden]"];
      
      active [label="Aktiv"];
      suggested [label="Vorgeschlagen"];
      refused [label="Abgelehnt"];
      standby [label="Standby"];
      ended [label="Beendet"];
   }


Veraltete Klienten 
--------------------

Wie alle Partner haben auch Klienten ein Ankreuzfeld "veraltet",
das unabhängig vom Zustand existiert.
Wird benutzt z.B. in folgenden Fällen:

- Der Klient wurde versehentlich als Dublette eines existierenden 
  Klienten angelegt (und darf jedoch nicht mehr gelöscht werden, 
  weil Dokumente existieren).
  

Regeln
------
  
- Ein Neuantrag kann keine Begleitungen haben. 
  (Ein Klient mit Begleitungen, selbst abgeschlossene, 
  kann nicht wieder zum Neuantrag werden. 
  Höchstens zu einem Ehemaligen.)
  
- Wenn ein Klient ins Stadium Ehemalig wechselt, werden automatisch 
  alle laufenden Begleitungen beendet.
  Ein Ehemaliger kann keine *laufenden* Begleitungen haben.
  
- Nur Benutzer mit einem unleeren Feld 
  `Begleitungsart (Dienst)` in den Benutzereinstellungen
  dürfen manuell Begleitungen erstellen.
  
- Wenn man ein Coaching manuell erstellt, 
  wird `Beginndatum` aufs Tagesdatum 
  und `Begleitungsart (Dienst)` auf die des Benutzers ausgefüllt.
  
- Importierte Klienten haben eine importierte primäre 
  Begleitung, die nicht geändert werden kann.
  

Screenshots
===========

.. screenshot:: pcsw.Client.detail.newcomers

Neuanträge
----------



.. image:: /gen/screenshots/pcsw.Client.detail.png
  :scale: 20

.. image:: /gen/screenshots/pcsw.Client.detail.1.png
  :scale: 20
 
.. image:: /gen/screenshots/pcsw.Client.detail.2.png
  :scale: 20

