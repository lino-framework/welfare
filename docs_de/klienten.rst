.. _welfare.de.clients:

========
Klienten
========

Ein Klient ist eine Person, für die wir eine Serie von zusätzlichen
Daten erfassen.


Tabellenansichten
=================

Eine Tabellenansicht der Klienten sieht ungefähr so aus:

.. image:: /tour/contacts.Clients.grid.png

Merke: **Begleitete Klienten** sind **weiß** dargestellt,  **Neuanträge** sind **grün** und **ehemalige Klienten** sind **gelb**.

Für Klienten gibt es mehrere **Tabellenansichten**, die sich durch
Kolonnenreihenfolge und Filterparameter unterscheiden:

.. 
  actors_overview:: pcsw.Clients integ.Clients reception.Clients
                     newcomers.NewClients debts.Clients

- :menupath:`pcsw.Clients` :
  allgemeine Liste, die jeder Benutzer sehen darf.

- :menupath:`integ.Clients` :
  spezielle Liste für die Kollegen im DSBE.
  Zeigt immer nur **begleitete** Kunden. 
  Hier kann man keine neuen Klienten anlegen.

- :menupath:`newcomers.NewClients` :
  spezielle Liste für die Zuweisung von Neuanträgen.

- :menupath:`reception.Clients` : 
  Liste für den Empfangsschalter.


Detail-Ansicht
==============

Das Detail, das bei Doppelklick angezeigt wird, ist für alle
Klientenansichten das Gleiche.  *Was* im Detail alles angezeigt wird
(bzw. was nicht), das hängt jedoch von den Zugriffsrechten ab.

  .. image:: /tour/contacts.Clients.detail.png

Hier drei interessante Felder:

.. show_fields:: pcsw.Client
   unemployed_since seeking_since unavailable_until

Und hier sind sie alle:

.. show_fields:: pcsw.Client
   :debug:


Technisches
===========

Technische Details in Englisch unter 

- `welfare.specs.pcsw`
- :class:`lino_welfare.modlib.pcsw.models.Client`

