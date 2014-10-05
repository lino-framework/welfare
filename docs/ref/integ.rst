===================
Integration service
===================

.. module:: welfare.integ

The :mod:`lino_welfare.modlib.integ` package 
provides data definitions used by the Integration Service.


Tables and Layouts
==================

.. class:: UsersWithClients

  .. django2rst::

    rt.show(integ.UsersWithClients)

.. class:: ActivityReport

  Gives an overview about the work of the Integration Service during a
  given period.

.. class:: CompareRequestsTable

  This is one of the tables of the :class:`ActivityReport`.

