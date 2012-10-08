Klienten
========


Klienten gibt es momentan in drei Tabellen:

- Clients : allgemeine Liste, die jeder Bentuzer sehen darf.

- IntegClients : DSBE-Spezifische Kundenliste.
  Zeigt immer nur **begleitete** Kunden. 
  Die Reiter Kompetenzen, Verträge... finden sich nur hier.
  
- NewClients : spezielle Liste für Kundenverwaltung, insbesondere 
  die Zuweisung von Neuanträgen.




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
  Antrag wird überprüft und der Klient muss einem Sozi zugewiesen werden.
  
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
  
Veraltete Klienten 
--------------------

Wie alle Partner haben auch Klienten ein Ankreuzfeld "veraltet",
das unabhängig vom Zustand existiert.
Wird benutzt z.B. in folgenden Fällen:

- Der Klient wurde versehentlich als Dublette eines existierenden 
  Klienten angelegt (und darf jedoch nicht mehr gelöscht werden, 
  weil Dokumente existieren).
  


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



Screenshots
-----------

.. image:: /gen/screenshots/pcsw.Client.detail.png
  :scale: 20

.. image:: /gen/screenshots/pcsw.Client.detail.1.png
  :scale: 20
 
.. image:: /gen/screenshots/pcsw.Client.detail.2.png
  :scale: 20

