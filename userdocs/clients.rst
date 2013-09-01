.. _welfare.clients:

=======
Clients
=======

(N.B.: Benutzer in Eupen siehe auch :ref:`welfare.watch_tim`)

Ce module comprend les fonctionnalités autour des entités suivantes:

.. actors_overview:: 
    contacts.Partners
    pcsw.Clients
    pcsw.Coachings
    
    
    
Ein Klient ist eine Person, für die wir eine Serie von 
zusätzlichen Daten erfassen.

Für Klienten gibt es drei **Tabellenansichten**, 
die sich lediglich durch Kolonnenreihenfolge 
und Filterparameter unterscheiden:

- "Alle Klienten" 
  (Menü :menuselection:`Kontakte --> Klienten`) : 
  allgemeine Liste, die jeder Benutzer sehen darf.

- DSBE-Klienten
  (Menü :menuselection:`DSBE --> Klienten`)
  spezielle Liste für die Kollegen im DSBE.
  Zeigt immer nur **begleitete** Kunden. 
  Hier kann man keine neuen Klienten anlegen.
  Die Reiter Kompetenzen, Verträge... finden sich nur hier.
  
- Neue Klienten
  (Menü :menuselection:`Neuanträge --> Klienten`):
  spezielle Liste für die Zuweisung von Neuanträgen.

N.B. 
Das Detail, das bei Doppelklick angezeigt wird, 
ist bei allen drei Ansichten das Gleiche. 
Das hängt vom :ref:`welfare.users.UserProfile` ab.



Référence
=========

.. actor:: pcsw.Client
.. actor:: pcsw.ClientContactType
.. actor:: pcsw.ClientContact
.. actor:: pcsw.CoachingType
.. actor:: pcsw.CoachingEnding
.. actor:: pcsw.Coaching
.. actor:: pcsw.AidType
.. actor:: pcsw.PersonGroup





Anhang
==============

- Workflow : Arbeitsablauf
- Life cycle : Lebenzyklus
- engl. "State" = Bearbeitungszustand




