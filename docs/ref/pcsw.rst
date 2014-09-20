===========
PCSW
===========

.. module:: welfare.pcsw

The :mod:`lino_welfare.modlib.pcsw` package provides data definitions
for PCSW specific objects like Client and Coaching.


Choicelists
===========

.. class:: ClientStates

  The list of possible choices for the :attr:`Client.client_state` field.
  Default configuration is as follows:

  .. django2rst::

     rt.show(pcsw.ClientStates)

  Any person who asks to meet with an agent for consultation will be
  registered into the database.  At the beginning the client is a
  **newcomer**. When the client introduces an application for a
  specific help, he can become **refused** or **coached**. When a
  coached client has no more active coaching, or when a newcomer does
  not come back after his first visit, then somebody with appropriate
  rights should mark the client as **former**.

.. class:: CivilState

.. class:: ResidenceType


.. class:: ClientEvents

.. class:: RefusalReasons



Models
======

.. class:: PersonGroup
.. class:: Activity

.. class:: DispenseReason

.. class:: Dispense

.. class:: ExclusionType

.. class:: Exclusion

.. class:: AidType

.. class:: ClientContactType

.. class:: ClientContact

.. class:: CoachingType

.. class:: CoachingEnding


.. class:: Client

    Inherits from :class:`ml.contacts.Person` and
    :class:`ml.beid.BeIdCardHolder`.

    .. attribute:: group

    Pointer to the intergration phase this client currently belongs to.
    See :class:`welfare.pcsw.Persongroup`.

    .. attribute:: client_state
    
    See :class:`ClientStates`.

.. class:: Coaching

    .. attribute:: primary

    Check this field to specify that this is the primary coaching for
    this client.  There is at most one primary coach per client.
    Enabling this field will automatically make the other coachings
    non-primary.

Tables and Layouts
==================

.. class:: Clients

    Usage examples see also :ref:`Filtering clients
    <welfare.clients.parameters>`.

    **Filter parameters**

    .. attribute:: client_state
    .. attribute:: coached_by

    Show only those clients for which a :class:`Coaching` by that user
    and in the observed period exists.

    .. attribute:: and_coached_by
    .. attribute:: start_date
    .. attribute:: end_date

    **Observed period**

    The observed period consists of the date range specified by the two fields

    - If both fields are empty, it means "today".

.. class:: CoachingsByClient


Actions
=======

.. class:: RefuseClient

.. class:: EndCoaching
