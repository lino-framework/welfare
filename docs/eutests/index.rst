==============
End user tests
==============

General checks
==============

- Play around
- Can I read a Belgian eid card?
- Does autorefresh work?

Clients and contracts
=====================

Select Contacts --> Clients.
Click + to create a new client (e.g. "Tom Tester")
Click Manage addresses. Add an address in a new city (e.g. "Tomtown").
Lino should automatically create the city
and send an email to Django admins.

Add some data for the new client the detail view:

- language knowledge
- career tab
- create several contracts and print them (to pdf) :

  - one "PIIS"
  - one "Mise à l'emploi art60§7"

- Create an aid granting

Organizations and course providers
==================================

- Create a new organization
- Convert it into a course provider
- Create a course
- add Tom Tester as a candidate to that course
