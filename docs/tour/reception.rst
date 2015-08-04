.. _welfare.tour.reception:


Tour of Lino Welfare
====================

.. |fa-external-link| raw:: html

   <i class="fa fa-external-link"></i>


Imagine you are the reception clerk.
A visitor enters.

- Visitor: My name is xxx and I'd like to get social help.

    - Clerk: Can I have your id card please? 
    - Search manually by name. Create manually a client record.
    - Read the id card.  If the person has a client record in our
      database, then Lino opens the the detail of this record. Otherwise
      it asks whether to create the client.

 
- Visitor: "My name is xxx, I have an appointment with Roger."
  (You know that Roger is one of the social agents.)

  - Open the :ddref:`reception.Clients` table
    (:menuselection:`Reception --> Clients`) and find the client.

  - Select the :ddref:`reception.Clients.create_visit` action.

  - Consult the :ddref:`reception.WaitingVisitors` table in your
    welcome screen (if necessary, click on the |fa-external-link| icon).


  - Click on "Checkin"

