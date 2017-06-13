===========
PCSW
===========

.. module:: welfare.pcsw

.. contents:: 
   :local:
   :depth: 3



Models
======

Coaching
--------

.. class:: Coaching

    A coaching is when a social agent assumes reponsibilty for a
    client for a given domain during a given period.

    .. attribute:: type

    Pointer to :class:`CoachingType`.

    .. attribute:: user

    The social agent. Pointer to :class:`ml.auth.User`.

    .. attribute:: primary

    Check this field to specify that this is the primary coaching for
    this client.  There is at most one primary coach per client.
    Enabling this field will automatically make the other coachings
    non-primary.

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
