.. _welfare.tested.dedupe:

============
dedupe
============

..
  This document is part of the test suite.
  To test only this document, run::
    $ python setup.py test -s tests.DocsTests.test_dedupe

A technical tour into the :mod:`lino.modlib.dedupe` module.

.. include:: /include/tested.rst

.. contents::
   :depth: 2


..
    >>> from __future__ import print_function
    >>> import os
    >>> os.environ['DJANGO_SETTINGS_MODULE'] = \
    ...    'lino_welfare.projects.std.settings.doctests'
    >>> from lino.api.doctest import *


>>> ses = rt.login('robin')
>>> translation.activate('en')


Similar Persons
---------------

The test database contains some examples of accidental duplicate data
entry.

One fictive person exists 3 times:

- Dorothée Dobbelstein-Demeulenaere
- Dorothée Demeulenaere
- Dorothée Dobbelstein

Here we try to create a fourth one:

>>> obj = pcsw.Client(first_name=u"Dorothée", last_name="Dobbelstein")
>>> dedupe.SimilarPersons.get_words(obj)
set([u'Dobbelstein', u'Doroth\xe9e'])
>>> ses.show(dedupe.SimilarPersons, obj)
=================================================
 Other
-------------------------------------------------
 **Mrs Dorothée DOBBELSTEIN (124)**
 **Mrs Dorothée DOBBELSTEIN-DEMEULENAERE (123)**
=================================================
<BLANKLINE>

Note that *Mrs Dorothée Demeulenaere (122)* is missing. Our algorithm
detects only two of the existing three duplicates.


For the following tests we write a utility function:

>>> def check(first_name, last_name):
...     obj = pcsw.Client(first_name=first_name, last_name=last_name)
...     qs = ses.spawn(dedupe.SimilarPersons, master_instance=obj)
...     return [unicode(r) for r in qs.data_iterator]

This function returns the names of the persons that Lino would detect
as duplicates, depending on the given first_name and last_name.

>>> check("Bernard", "Bodard")
[u'Bernard BODARD (170*)']

Without our utility function the above test would be less readable:

>>> obj = pcsw.Client(first_name="Bernard", last_name="Bodard")
>>> ses.show(dedupe.SimilarPersons, obj)
===========================
 Other
---------------------------
 **Bernard BODARD (170*)**
===========================
<BLANKLINE>

Some users tend to mix up first and last name. Lino would detect that:

>>> check("Bodard", "Bernard")
[u'Bernard BODARD (170*)']

>>> check("Erna", "Odar")
[u'Bernard BODARD (170*)']

The following duplicates are **not yet** detected though they obviously
should. We are still experimenting...

>>> check("Bernard-Marie", "Bodard")
[]

>>> check("Marie", "Bernard-Bodard")
[]

The following duplicate is not detected because Lino doesn't yet use
phonetic algorithms:

>>> check("Bernhard", "Bodard")
[]


