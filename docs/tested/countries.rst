.. _welfare.tested.countries:

=============
Countries
=============

.. How to test only this document:

  $ python setup.py test -s tests.DocsTests.test_countries


.. contents::
   :local:
   :depth: 2

About this document
===================

This documents uses the :mod:`lino_welfare.projects.eupen` test
database:

>>> from __future__ import print_function
>>> import os
>>> os.environ['DJANGO_SETTINGS_MODULE'] = \
...    'lino_welfare.projects.eupen.settings.doctests'
>>> from lino.api.doctest import *



>>> countries.Country.objects.all().count()
270

>>> countries.Country.objects.filter(actual_country__isnull=True).count()
266

>>> qs = countries.Country.objects.filter(actual_country__isnull=False)
>>> for obj in qs:
...     print obj.pk, obj.name, obj.inscode, obj.actual_country.name
BYAA Byelorussian SSR Soviet Socialist Republic  Belarus
DEDE German Federal Republic 103 Deutschland
DDDE German Democratic Republic 170 Deutschland
SUHH USSR, Union of Soviet Socialist Republics  Russische Föderation

>>> for m, f in rt.modules.countries.Country._lino_ddh.fklist:
...     print dd.full_model_name(m), f.name
addresses.Address country
cv.Training country
cv.Study country
cv.Experience country
contacts.Partner country
pcsw.Client nationality
countries.Country actual_country
countries.Place country


>>> kw = dict()
>>> fields = 'count rows'
>>> demo_get(
...    'rolf', 'choices/addresses/Address/country', fields, 266, **kw)
>>> demo_get(
...    'rolf', 'choices/contacts/Partners/country', fields, 266, **kw)
>>> demo_get(
...    'rolf', 'choices/pcsw/Clients/country', fields, 266, **kw)
>>> demo_get(
...    'rolf', 'choices/countries/Countries/actual_country', fields, 266, **kw)

>>> demo_get(
...    'rolf', 'choices/cv/Training/country', fields, 266, **kw)

The following fields have the full list, including fake countries)

>>> demo_get(
...    'rolf', 'choices/pcsw/Clients/nationality', fields, 270, **kw)

>>> demo_get(
...    'rolf', 'choices/countries/Places/country', fields, 270, **kw)

