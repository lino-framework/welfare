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
    >>> from __future__ import print_function, unicode_literals
    >>> import os
    >>> os.environ['DJANGO_SETTINGS_MODULE'] = \
    ...    'lino_welfare.projects.std.settings.doctests'
    >>> from lino.api.doctest import *


>>> ses = rt.login('robin')
>>> translation.activate('en')


Similar Partners
---------------

The test database contains some examples of accidental duplicate data
entry.

One fictive person exists 3 times:

>>> for p in contacts.Partner.objects.filter(name__contains=u"Dorothée"):
...     print(unicode(p))
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
Demeulenaere Dorothée (122)
Dobbelstein-Demeulenaere Dorothée (123)
Dobbelstein Dorothée (124)

Here we try to create a fourth one:

>>> obj = pcsw.Client(first_name=u"Dorothée", last_name="Dobbelstein")
>>> obj.full_clean()  # 
>>> obj.get_words()
[u'Dobbelstein', u'Doroth\xe9e']
>>> ses.show(dedupe.SimilarPartners, obj)
=============================================
 Other
---------------------------------------------
 **Dobbelstein-Demeulenaere Dorothée (123)**
 **Dobbelstein Dorothée (124)**
=============================================
<BLANKLINE>

Note that *Mrs Dorothée Demeulenaere (122)* is missing. Our algorithm
detects only two of the existing three duplicates.


For the following tests we write a utility function:

>>> def check(first_name, last_name):
...     obj = pcsw.Client(first_name=first_name, last_name=last_name)
...     obj.full_clean()
...     qs = ses.spawn(dedupe.SimilarPartners, master_instance=obj)
...     return [unicode(r) for r in qs.data_iterator]

This function returns the names of the persons that Lino would detect
as duplicates, depending on the given first_name and last_name.

>>> check("Bernard", "Bodard")
[u'Bodard Bernard (170*)']

Without our utility function the above test would be less readable:

>>> obj = pcsw.Client(first_name="Bernard", last_name="Bodard")
>>> obj.full_clean()
>>> ses.show(dedupe.SimilarPartners, obj)
===========================
 Other
---------------------------
 **Bodard Bernard (170*)**
===========================
<BLANKLINE>

Some users tend to mix up first and last name. Lino would detect that:

>>> check("Bodard", "Bernard")
[u'Bodard Bernard (170*)']

Until 20150304, a person named "Erna Odar" would have been detected as
similar to "Bernard Bodard". Which was of course nonsense.

>>> check("Erna", "Odar")
[]

And also the following duplicates are now detected because Lino now
uses "phonetic algorithms":

>>> check("Bernhard", "Bodard")
[u'Bodard Bernard (170*)']

>>> check("Bernard-Marie", "Bodard")
[u'Bodard Bernard (170*)']


>>> check("Marie", "Bernard-Bodard")
[u'Bodard Bernard (170*)']

(That last one is actually not a duplicate, but we should expect Lino to
make a false positive.)

