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

Models
======

.. class:: AidType

  .. attribute:: board

  Pointer to the default :class:`ml.boards.Board` for aid projects of
  this type.

  .. attribute:: excerpt_type

.. class:: Category

.. class:: Aid

  .. attribute:: board

  Pointer to the :class:`ml.boards.Board` which decided to allocate
  this aid project.


.. class:: Helper


Tables and Layouts
==================

.. class:: AidsByClient

