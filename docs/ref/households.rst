===========
Households
===========

.. module:: welfare.households

The :mod:`lino_welfare.modlib.households` app is an extension of 
:mod:`ml.households` which adds some PCSW-specific features.

Tables
======

.. class:: RefundsByPerson
  
  Used by :xfile:`clothing_refund.body.html`.
  Example data:

  .. django2rst::

    obj = pcsw.Client.objects.get(name="Frisch Paul")
    rt.show(households.RefundsByPerson, obj)

