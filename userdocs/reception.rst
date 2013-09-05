.. _welfare.reception:

Reception
=========

The reception module of Lino-Welfare 
is for managing a reception desk and a waiting queue.

Visitors are "checked in" as they present themselves at a 
reception desk,
then they wait in a lounge until an agent "receives" them,
and finally they are "checked out" when they leave the building.

Social agents have a possibility to see how many and which 
clients are waiting for them.

A **reception clerk** is the user at the reception desk who welcomes 
visitors.
In the public demo database there is a user "theresia" with that profile.
Theresia's first questions are usually 
"What's your name?" or 
"Do you have an appointment with a social agent?".
  
Visitors must have a :ref:`welfare.pcsw.Client` account.
Technically a :ref:`welfare.contacts.Partner` account would be 
enough, but other visitors like suppliers or board members aren't 
managed by the reception module.

Lino notifies the user to read the client's eID card
if this is necessary, e.g. because "eID card has not yet been read!"
or "Old eID card validity has expired!"

Most visitors come at the open consultation hours.
and don't have an appointment with some user.
We call this a "visit".
In that case the reception clerk 
clicks "Create Visit", confirms the selected agent and enters a
"reason" (a short one-line text).
This will automatically create two records: an 
:ddref:`cal.Event` and a :ddref:`cal.Guest`.


A **visit** is an unplanned calendar event. 
An **appointment** is a planned (scheduled) calendar event.


In any case, when the clerk then clicks the Checkin button of 
that appointment. 

The reception clerk then finally says 
"Please sit down and wait until the social agent comes."


.. actor:: reception.Clients

      The button "Find date with..." is needed when you want to 
      find and create a date for that client with an agent who is 
      *not* coaching this client.

.. actor:: reception.CoachingsByClient

      This is the table of Coachings in the detail of 
      :ddref:`reception.Clients`.


.. actor:: reception.ExpectedGuests

 
.. actor:: reception.WaitingGuests

As a social worker you consult this table to see:

- How many people are waiting for me?
- Who is waiting for me?

For example you may decide "This guy gets quickly nervous, and it 
won't take much time, so i'll let him in before the others."


.. actor:: reception.AppointmentsByGuest
