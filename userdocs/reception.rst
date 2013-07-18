Reception
=========

The optional reception module of Lino-Welfare 
is for managing a reception desk and a waiting queue: 
register visitors into a waiting queue 
as they present themselves at a reception desk (Empfangsschalter),
and unregister them when they leave again.

A **reception clerk** is the user at the reception desk who welcomes visitors.
His first questions are usually 
"What's your name?" or 
"Do you have a scheduled meeting with somebody?".
In the public demo database there is a user "theresia" with that profile.
  
Visitors must have a :ref:`welfare.pcsw.Client` account
(technically a :ref:`welfare.contacts.Partner` account would be 
enough, but other visitors like suppliers or board members aren't 
currently managed by the reception module).

When appropriate, Lino must now automatically 
pop up a notification to read the client's eID card.
"eID card has not yet been read!"
"Old eID card validity has expired!"

Most visitors come at the open consultation hours.
and don't have an appointment with some user.
In that case the reception clerk 
clicks "Create Appointment". 
Lino suggests the Client's primary coach as user of the appointment.
Theresia may select another social worker.
She also may specify a reason, a short one-line text.

In any case, when the clerk then clicks the Checkin button of 
that appointment. 

The reception clerk then finally says 
"Please sit down and wait until the social agent comes."


.. actor:: reception.ExpectedGuests
 
.. actor:: reception.WaitingGuests

As a social worker you consult this table to see:

- How many people are waiting for me?
- Who is waiting for me?

For example you may decide "This guy gets quickly nervous, and it 
won't take much time, so i'll let him in before the others."



