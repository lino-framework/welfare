===========
Social aids
===========

.. module:: welfare.aids

The :mod:`lino_welfare.modlib.aids` package provides data definitions
for managing "social aids". An "aid" here means the decision that some
client gets some kind of aid during a given lapse of time.

Choicelists
===========

.. class:: AidRegimes

  (Currently not used)

.. class:: ConfirmationTypes

.. django2rst::

  rt.show(aids.ConfirmationTypes)


Models
======

.. class:: AidType

  .. attribute:: board

  Pointer to the default :class:`ml.boards.Board` for aid projects of
  this type.

  .. attribute:: excerpt_type

  .. attribute:: confirmation_type

  Pointer to :class:`ConfirmationTypes`.

.. class:: Confirmable

  .. attribute:: signer

  The agent who has signed or is expected to sign this item.

.. class:: Granting(Confirmable)

.. class:: Confirmation(Confirmable)

.. class:: SimpleConfirmation

.. class:: IncomeConfirmation

.. class:: RefundConfirmation

.. class:: Category

.. class:: Aid

  .. attribute:: board

  Pointer to the :class:`ml.boards.Board` which decided to allocate
  this aid project.


.. class:: Helper


Tables and Layouts
==================

.. class:: AidsByClient

