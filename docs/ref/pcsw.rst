===========
PCSW
===========

.. module:: welfare.pcsw

The :mod:`lino_welfare.modlib.pcsw` package provides data definitions
for PCSW specific objects. 

Most important models are :class:`Client` and :class:`Coaching`.

.. contents:: 
   :local:
   :depth: 3



Models
======

Client
------

.. class:: Client

    Inherits from :class:`ml.contacts.Person` and
    :class:`ml.beid.BeIdCardHolder`.

    .. attribute:: cvs_emitted

    A virtual field displaying a group of shortcut links for managing CVs
    (Curriculum Vitaes).  

    This field is an excerpts shortcut
    (:class:`ml.excerpts.Shortcuts`) and works only if the database
    has an :class:`ExcerptType <ml.excerpts.ExcerptType>` whose
    `shortcut` points to it.

    .. attribute:: group

    Pointer to :class:`PersonGroup`.
    The intergration phase of this client.  
    
    The :class:`UsersWithClients <welfare.integ.UsersWithClients>`
    table groups clients using this field.


    .. attribute:: client_state
    
    Pointer to :class:`ClientStates`.

   

    .. attribute:: client_contact_type
    
    Pointer to :class:`PersonGroup`.

Coaching
--------

.. class:: Coaching

    A coaching is when a social agent assumes reponsibilty for a
    client for a given domain during a given period.

    .. attribute:: type

    Pointer to :class:`CoachingType`.

    .. attribute:: user

    The social agent. Pointer to :class:`ml.users.User`.

    .. attribute:: primary

    Check this field to specify that this is the primary coaching for
    this client.  There is at most one primary coach per client.
    Enabling this field will automatically make the other coachings
    non-primary.

ClientContact
-------------

.. class:: ClientContact

    A typed link between a :class:`Client` and a an external partner
    (a :class:`ml.contacts.Company` and/or a
    :class:`ml.contacts.Person`).

    Inherits from :class:`ml.contacts.ContactRelated`.

    .. attribute:: client

    The client who uses this link. Pointer to :class:`Client`.

    .. attribute:: company

    The company being linked. 

    .. attribute:: type

    The type of this link. Pointer to :class:`ClientContactType`.


.. class:: Dispense

.. class:: Exclusion



.. class:: PersonGroup

  TODO: Rename this table to `IntegrationPhase`.

  .. django2rst:: 

      rt.show(pcsw.PersonGroups)


.. class:: Activity

  Used only in Welfare à la Eupen

.. class:: DispenseReason

  .. django2rst:: 

      rt.show(pcsw.DispenseReasons)


.. class:: ExclusionType

  .. django2rst:: rt.show(pcsw.ExclusionTypes)


.. class:: AidType

  TODO: Remove this table and replace it by :mod:`welfare.aids`.

.. class:: ClientContactType

  .. django2rst:: rt.show(pcsw.ClientContactTypes)

.. class:: CoachingType

  .. django2rst:: rt.show(pcsw.CoachingTypes)

.. class:: CoachingEnding

  .. django2rst:: rt.show(pcsw.CoachingEndings)




Choicelists
===========

.. class:: ClientStates

  The list of possible choices for the :attr:`Client.client_state` field.
  Default configuration is as follows:

  .. django2rst:: rt.show(pcsw.ClientStates)

  Any person who asks to meet with an agent for consultation will be
  registered into the database.  At the beginning the client is a
  **newcomer**. When the client introduces an application for a
  specific help, he can become **refused** or **coached**. When a
  coached client has no more active coaching, or when a newcomer does
  not come back after his first visit, then somebody with appropriate
  rights should mark the client as **former**.

.. class:: CivilState

  .. django2rst:: 

      rt.show(pcsw.CivilState)

.. class:: ResidenceType

  .. django2rst:: 

      rt.show(pcsw.ResidenceType)


.. class:: ClientEvents

  .. django2rst:: 

      rt.show(pcsw.ClientEvents)

.. class:: RefusalReasons

  .. django2rst:: 

      rt.show(pcsw.RefusalReasons)




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
