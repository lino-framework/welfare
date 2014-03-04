.. _welfare.beid:

==============
Read eID cards
==============

There are two situations where you can read an eID card:
(1) as a quick link on the welcome screen, or
(2) as an action on an existing Client.

**The first method** is used when you don't know whether the card holder
is already in the database. 

You call this method by clicking on the 
quick link labelled :ddref:`pcsw.Client.read_beid`.

Lino reads the data on the card, does some database lookups and then
decides what to do:

- create a new client 
- update an existing client

For both actions it will ask your confirmation first.

Comparison is based on the :ddref:`pcsw.Client.national_id`.  If you
know that the national id of a client has changed, then you must first
manually update this field. Otherwise Lino will create a new client
record.

It is possible that Lino refuses to create a new client:

- When a client exists with the same name (first and last) and am
  *empty* :ddref:`pcsw.Client.national_id`.


**The second method** is when you know the client and have selected
their data record in Lino. 

You call this method either by clicking on the `Must read eID card!`_
text, or by clicking by your own choice on the
:ddref:`pcsw.Client.read_beid` action in the toolbar or the context
menu.

Lino reads the data on the card, compares it with the current record,
and suggests to update your record in case there are differences.


Must read eID card!
-------------------

This text appears in the info box of a clients detail view when (1) no
eID card has ever been read or (2) the card has been read but validity
has expired.

