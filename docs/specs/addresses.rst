.. doctest docs/specs/addresses.rst
.. _welfare.specs.addresses:

=========================
Multiple postal addresses
=========================

How :ref:`welfare` uses :mod:`lino_xl.lib.addresses`.

.. doctest init:

    >>> from lino import startup
    >>> startup('lino_welfare.projects.gerd.settings.doctests')
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
[100, 102, 104, 113, 115, 116, 118, 119, 121, 122, 124, 125, 127, 128, 130, 131, 133, 134, 136, 137, 139, 140, 142, 143, 145, 146, 148, 149, 185, 186, 189, 190, 192, 193, 200, 201, 203, 204, 206, 207, 210, 211, 215, 216, 218, 219, 229, 230]

Here are the addresses of one of these partners (119):

>>> obj = contacts.Partner.objects.get(id=119)
>>> rt.show(addresses.AddressesByPartner, obj)
==================== =========== ====================== ========
 Adressenart          Bemerkung   Adresse                Primär
-------------------- ----------- ---------------------- --------
 Offizielle Adresse               Auenweg, 4700 Eupen    Ja
 Ungeprüfte Adresse               Auf dem Spitzberg 11   Nein
==================== =========== ====================== ========
<BLANKLINE>
