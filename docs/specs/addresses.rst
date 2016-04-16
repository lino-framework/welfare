.. _welfare.specs.addresses:

=========================
Multiple postal addresses
=========================


.. How to test only this document:

    $ python setup.py test -s tests.SpecsTests.test_addresses
    
    doctest init:

    >>> from lino import startup
    >>> startup('lino_welfare.projects.eupen.settings.doctests')
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
[102, 103, 113, 114, 116, 117, 119, 120, 122, 123, 125, 126, 128, 129, 131, 132, 134, 135, 137, 138, 140, 141, 143, 144, 146, 147, 149, 182, 186, 188, 190, 191, 193, 194, 201, 202, 204, 205, 207, 208, 211, 214, 216, 217, 219, 228, 230, 231]

Here are the addresses of one of these partners (123):

>>> obj = contacts.Partner.objects.get(id=123)
>>> rt.show(addresses.AddressesByPartner, obj)
==================== =========== =========================== ========
 Adressenart          Bemerkung   Adresse                     Primär
-------------------- ----------- --------------------------- --------
 Offizielle Adresse               Bahnhofstraße, 4700 Eupen   Ja
 Referenzadresse                  August-Thonnar-Str. 14      Nein
==================== =========== =========================== ========
<BLANKLINE>

