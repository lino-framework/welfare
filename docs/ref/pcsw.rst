===========
PCSW
===========

.. module:: welfare.pcsw

The :mod:`lino_welfare.modlib.pcsw` package provides data definitions
for PCSW specific objects like Client and Coaching.


Choicelists
===========

.. class:: ClientStates

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

.. class:: Coaching

  .. attribute:: primary

  Check this field to specify that this is the primary coaching for
  this client.  There is at most one primary coach per client.
  Enabling this field will automatically make the other coachings
  non-primary.

Tables and Layouts
==================

.. class:: CoachingsByClient


Actions
=======

.. class:: RefuseClient

.. class:: EndCoaching
