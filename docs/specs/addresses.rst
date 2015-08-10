.. _welfare.tested.addresses:

=========================
Multiple postal addresses
=========================


.. How to test only this document:

    $ python setup.py test -s tests.SpecsTests.test_addresses
    
    doctest init:

    >>> from __future__ import print_function
    >>> import os
    >>> os.environ['DJANGO_SETTINGS_MODULE'] = \
    ...    'lino_welfare.projects.eupen.settings.doctests'
    >>> from lino.api.doctest import *
    >>> from django.db.models import Q

.. contents::
   :depth: 2


These are the partners in the demo database with more than one
address:

>>> lst = [p.id for p in contacts.Partner.objects.filter(
...     addresses_by_partner__primary=False).distinct()]

>>> len(lst)
48
>>> print(lst)  #doctest: +NORMALIZE_WHITESPACE
[102, 103, 113, 114, 116, 117, 119, 120, 122, 123, 125, 126, 128, 129,
131, 132, 134, 135, 137, 138, 140, 141, 143, 144, 146, 147, 149, 190,
192, 195, 198, 199, 201, 202, 204, 210, 212, 213, 215, 216, 218, 220,
224, 225, 227, 228, 230, 231]

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

