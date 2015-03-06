.. _welfare.tested.dedupe:

==========================
Avoiding duplicate records
==========================

..  This document is part of the test suite.  To test only this
  document, run::

    $ python setup.py test -s tests.DocsTests.test_dedupe

A tested tour into the :mod:`lino.modlib.dedupe` module.

In Lino Welfare, a :class:`Partner
<lino_welfare.modlib.contacts.models.Partner>` inherits from
:class:`lino.modlib.dedupe.mixins.Dupable`, which means that Lino
offers some functionality for avoiding duplicate records on all
partners (including :class:`Client
<lino_welfare.modlib.pcsw.models.Client>`).

..
    >>> from __future__ import print_function, unicode_literals
    >>> import os
    >>> os.environ['DJANGO_SETTINGS_MODULE'] = \
    ...    'lino_welfare.projects.std.settings.doctests'
    >>> from lino.api.doctest import *


Phonetic words

>>> rt.show(contacts.Partners, column_names="id name phonetic_words")
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
===== ======================================================================= ===================================================================
 ID    Name                                                                    phonetic_words
----- ----------------------------------------------------------------------- -------------------------------------------------------------------
 182   AS Express Post                                                         , **EXPR**, **PAST**
 183   AS Matsalu Veevärk                                                      , **MATSAL**, **VAFRC**
 256   Adam Albert                                                             **ADAN**, **ALBAD**
 260   Adam Ilja                                                               **ADAN**, **ILJ**
...
 169   Ärgerlich Erna                                                          **RGARLACH**, **ERN**
 167   Õunapuu Õie                                                             **UNAP**,
 195   ÖSHZ Kettenis                                                           **S**, **CATAN**
 168   Östges Otto                                                             **STG**, **OT**
===== ======================================================================= ===================================================================
<BLANKLINE>


Similar Partners
----------------

The test database contains a fictive person named Dorothée
Dobbelstein-Demeulenaere as an example of accidental duplicate data
entry.  Dorothée exists 3 times in our database:

>>> for p in contacts.Partner.objects.filter(name__contains=u"Dorothée"):
...     print(unicode(p))
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
Demeulenaere Dorothée (122)
Dobbelstein-Demeulenaere Dorothée (123)
Dobbelstein Dorothée (124)

The detail window of each of these records shows some of the other
records in the `SimilarPartners` table:

>>> rt.show(dedupe.SimilarPartners, pcsw.Client.objects.get(pk=122))
=============================================
 Other
---------------------------------------------
 **DOBBELSTEIN-DEMEULENAERE Dorothée (123)**
=============================================
<BLANKLINE>

>>> rt.show(dedupe.SimilarPartners, pcsw.Client.objects.get(pk=123))
=================================
 Other
---------------------------------
 **DEMEULENAERE Dorothée (122)**
 **DOBBELSTEIN Dorothée (124)**
=================================
<BLANKLINE>

>>> rt.show(dedupe.SimilarPartners, pcsw.Client.objects.get(pk=124))
=============================================
 Other
---------------------------------------------
 **DOBBELSTEIN-DEMEULENAERE Dorothée (123)**
=============================================
<BLANKLINE>

Note how the result can differ depending on the partner.  Our
algorithm is not perfect and does not detect all duplicates. 

The algorithm
-------------

The alarm bell rings when there are **two similar name components** in
both first and last name. Punctuation characters (like "-" or "&" or
",") are ignored, and also the ordering of elements does not matter.

The current implementation splits the :attr:`name
<lino.modlib.contacts.Partners.name>` of each partner into its parts,
removing punctuation characters, computes a phonetic version using the
`NYSIIS algorithm
<https://en.wikipedia.org/wiki/New_York_State_Identification_and_Intelligence_System>`_
and stores them in a separate database field :attr:`phonetic_name
<lino.modlib.dedupe.mixins.Dupable.phonetic_name>`.

>>> obj = pcsw.Client(first_name="First", last_name="Last")
>>> obj.full_clean()
>>> obj.get_dupable_words()
[u'Last', u'First']
>>> obj.phonetic_words
u'LAST FARST'


Checked at input
----------------

If a user tries to create a fourth record of that person, then Lino
will ask a confirmation first:

>>> data = dict(an="submit_insert")
>>> data.update(first_name="Dorothée")
>>> data.update(last_name="Dobbelstein")
>>> data.update(genderHidden="F")
>>> data.update(gender="Weiblich")
>>> res = test_client.post('/api/pcsw/Clients', data=data, REMOTE_USER="robin")
>>> res.status_code
200
>>> r = json.loads(res.content)
>>> print(r['message'])
There are 2 similar Clients:<br/>
DOBBELSTEIN Dorothée (124)<br/>
DOBBELSTEIN-DEMEULENAERE Dorothée (123)<br/>
Are you sure you want to create a new Client named Mrs Dorothée DOBBELSTEIN?

This is because :class:`lino.modlib.dedupe.mixins.Dupable` replaces
the standard `submit_insert` action by the :class:`CheckedSubmitInsert
<lino.modlib.dedupe.mixins.CheckedSubmitInsert>` action.


Testing the algorithm
---------------------

How good (how bad) is our algorithm? Here are some examples.  For the
following tests we write a utility function:

>>> def check(first, last):
...     obj = contacts.Person(first_name=first, last_name=last)
...     obj.full_clean()
...     return map(unicode, dedupe.SimilarPartners.request(obj))

This function returns the names of the persons that Lino would detect
as duplicates, depending on the given first_name and last_name.

>>> check("Bernard", "Bodard")
[u'Bernard BODARD (170*)']

Lino detects if a user mixes up first and last name:

>>> check("Bodard", "Bernard")
[u'Bernard BODARD (170*)']

Until 20150304, a person named "Erna Odar" would have been detected as
similar to "Bernard Bodard". Which was of course nonsense.

>>> check("Erna", "Odar")
[]

And also the following duplicates are now detected because Lino now
uses "phonetic algorithms":

>>> check("Bernhard", "Bodard")
[u'Bernard BODARD (170*)']

>>> check("Bernard-Marie", "Bodard")
[u'Bernard BODARD (170*)']


>>> check("Marie", "Bernard-Bodard")
[u'Bernard BODARD (170*)']

(That last one is actually not a duplicate, but we should expect Lino to
make a false positive.)

