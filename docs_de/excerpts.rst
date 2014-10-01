===============
Bescheinigungen
===============


.. glossary::
  :sorted:


  Visite

    Als **Visite** bezeichnen wir einen Termin, der nicht vorgesehen war


  Termin 

    Als **Termin** bezeichnen wir einen Kalendereintrag, der zwischen
    zwei oder mehr Personen als Treffpunkt abgesprochen ist.




Anwesenheitsbescheinigung
=========================

Um eine Anwesenheitsbescheinigung auszustellen, muss der Klient
"anwesend" gewesen sein.  Also es muss ein Termin oder eine Visite
existieren, für die dieser Klient als Gast eingetragen ist. Diese
Einträge sind es, die man sieht im Feld "Termine" des Reiters "Person"
im Detail des Klienten.


Hilfebestätigungen
==================

Es gibt auch Hilfearten (z.B. “Erstattung”), für die nie eine
Bescheinigung gedruckt wird. Deren Feld `Bescheinigungsart`
(:attr:`confirmation_type <welfare.aids.AitType.confirmation_type>`
ist leer.

Lino unterscheidet zwischen Hilfe\ *beschlüssen* und Hilfe\
*bestätigungen*.  Ein Hilfebeschluss (:class:`welfare.aids.Granting`)
ist eher "prinzipiell", während eine Bestätigung detailliierter ist.
besagt, dass ein Klient während einer bestimmten Periode 

:class:`welfare.aids.Confirmation`

- Einen “Bestätiger” soll es nicht nur pro Bescheinigung, sondern auch
  pro Beschluss geben. Bestätiger der Beschlusses ist par défaut der
  Primärbegleiter, Bestätiger einer Bescheinigung ist der des
  Beschlusses.

- Bestätiger immer auch in jedem insert_layout sichtbar

- Lebensmittelbank: Empfänger (Rotes Kreuz) fehlt (d.h. neue Felder
  company und contact_person in AidType)

- Übernahmescheine:

- Pro Bescheinigung auch die Apotheke sehen und ändern können (d.h.:
  Neue Felder AidType.pharmacy_type und RefundConfirmation.pharmacy.
  (ist allerdings noch nicht vorbelegt aus Klientenkontakt)




- Einkommensbestätigung EiEi
- AMK
- Lebensmittelausgabe
