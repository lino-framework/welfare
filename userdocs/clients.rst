.. _welfare.clients:

=======
Clients
=======

(N.B.: Benutzer in Eupen siehe auch :ref:`welfare.watch_tim`)

.. contents:: 
   :local:
   :depth: 2


.. actor:: pcsw.Client

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
    Was im Detail alles angezeigt wird, 
    hängt jedoch vom :ddref:`users.User.profile` ab.
    

.. actor:: pcsw.Coaching

.. actor:: pcsw.ClientContact

.. actor:: pcsw.ClientContactType
.. actor:: pcsw.CoachingType
.. actor:: pcsw.CoachingEnding
.. actor:: pcsw.AidType
.. actor:: pcsw.PersonGroup

.. actor:: pcsw.CivilState

    List of possible choices for the 
    :ddref:`pcsw.Client.civil_state` field
    of a :ddref:`pcsw.Client`.
    
    .. django2rst::
        
        settings.SITE.login('robin').show(cv.CefLevel)





