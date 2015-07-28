.. _welfare.tested.addresses:

=========================
Multiple postal addresses
=========================


.. How to test only this document:

  $ python setup.py test -s tests.SpecsTests.test_addresses


.. contents::
   :depth: 2

About this document
===================

.. include:: /include/tested.rst

This document uses the :mod:`lino_welfare.projects.eupen` test
database:

>>> from __future__ import print_function
>>> import os
>>> os.environ['DJANGO_SETTINGS_MODULE'] = \
...    'lino_welfare.projects.eupen.settings.doctests'
>>> from lino.api.doctest import *
>>> from django.db.models import Q
>>> print(settings.SETTINGS_MODULE)
lino_welfare.projects.eupen.settings.doctests

These are the partners in the demo database with more than one
address:

>>> lst = [p.id for p in contacts.Partner.objects.filter(
...     addresses_by_partner__primary=False).distinct()]

>>> len(lst)
44
>>> print(lst)
[102, 103, 113, 114, 116, 117, 119, 120, 122, 123, 125, 126, 128, 129, 131, 132, 134, 135, 137, 138, 140, 141, 143, 144, 146, 147, 149, 190, 194, 196, 198, 199, 201, 202, 213, 214, 216, 218, 222, 223, 225, 226, 228, 229]

Here are the addresses of one of these partners (123):

>>> obj = contacts.Partner.objects.get(id=123)
>>> rt.show(addresses.AddressesByPartner, obj)
====================== =========== =========================== ========
 Adressenart            Bemerkung   Adresse                     Primär
---------------------- ----------- --------------------------- --------
 Offizielle Adresse                 Bahnhofstraße, 4700 Eupen   Ja
 Referenzadresse                    August-Thonnar-Str. 14      Nein
 **Total (2 Zeilen)**                                           **1**
====================== =========== =========================== ========
<BLANKLINE>

