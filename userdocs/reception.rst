.. _welfare.reception:

Reception
=========

The reception module of Lino Welfare 
is for managing a reception desk and a waiting queue.

Visitors are "checked in" as they present themselves at the 
reception desk,
then they wait in a lounge until an agent receives them,
and finally they are "checked out" when they leave the building.

Social agents have a possibility to see how many and which 
clients are waiting for them.
(:ddref:`reception.MyWaitingVisitors`)

A **reception clerk** is the user at the reception desk who welcomes 
visitors.
The reception clerk asks questions like
"What's your name?" or 
"Do you have an appointment with a social agent?".
See :ddref:`lino.UserTypes`.

 

Vocabulary note: 
Visitors are instances of the :ddref:`cal.Guest` model
when they are being managed by the reception module,
i.e. when they have been at least checked in.

Visitors must be registered as a :ddref:`pcsw.Client`.
Technically a :ddref:`contacts.Partner` account would be 
enough, but other "visitors" like suppliers or board members aren't 
managed by the reception module of Lino Welfare.

Lino notifies the user to read the client's eID card
if this is necessary, e.g. because "eID card has not yet been read!"
or "Old eID card validity has expired!"

Most visitors come at the open consultation hours.
and don't have an appointment with some user.
We call this a "visit" or "prompt event".
In that case the reception clerk 
clicks "Create Visit", confirms the selected agent and enters a
"reason" (a short one-line text).
This will automatically create two records: an 
:ddref:`cal.Event` and a :ddref:`cal.Guest`.


A **visit** or **prompt event** is an unplanned :ddref:`cal.Event`. 
An **appointment** is a planned (scheduled) :ddref:`cal.Event`.

In any case, when the clerk then the Checkin button of 
that appointment. 


.. actor:: reception.Clients

      The button "Find date with..." is needed when you want to 
      find and create a date for that client with an agent who is 
      *not* coaching this client.

.. actor:: reception.CoachingsByClient

      This is the table of Coachings in the detail of 
      :ddref:`reception.Clients`.


.. actor:: reception.ExpectedGuests

 
.. actor:: reception.WaitingVisitors

    This table shows the list of all visitors who have checked in and 
    are waiting to be received.
    Yes.

.. actor:: reception.MyWaitingVisitors

    As a social worker you consult this table to see:

    - How many people are waiting for me?
    - Who is waiting for me?

    For example you may decide "This guy gets quickly nervous, and it 
    won't take much time, so i'll let him in before the others."

    This table inherits from :ddref:`reception.WaitingVisitors`,
    but shows only the visitors waiting for the requesting user.
    And is available only to social workers.

.. actor:: reception.AppointmentsByPartner

