.. include:: /../docs/shared/include/defs.rst

=====================
Manual testing suites
=====================


General checks
==============

- Does autorefresh work?  After clicking the button once, Lino starts to send an
  AJAX request every minute. Note :ticket:`2742`.

- Open your user preferences. change your language. Verify that the user
  interface language changes.  Switch back to your preferred language.


eidreader
=========

- Read a Belgian eid card. Let Lino create the client. Manually modify the birth
  date of the client. Re-read the id card. Lino asks to update. Say No. Check
  that the birth date has remained at the manual value. Re-read the id card. Now
  say Yes. Delete the client.


Clients and contracts
=====================

Select Contacts --> Clients.
Click |insert| to create a new client "Tom Tester"
Click Manage addresses. Add an address in a new city (e.g. "Tomtown").
Lino should automatically create the city
and send an email to Django admins.

Add some data for the new client the detail view:

- language knowledge
- Career tab
- Create an aid granting
- create several contracts and print them (to pdf) :

  - one "PIIS"
  - one Job supplyment ("Art. 60§7")


Organizations and course providers
==================================

- Create a new organization
- Convert it into a course provider
- Create a course
- add Tom Tester as a candidate to that course

Calendar
========

Reception
=========

Debt mediation
==============
