.. _welfare.tested.dupable_partners:

===========================
Avoiding duplicate partners
===========================

Lino Welfare offers some functionality for avoiding duplicate records
on all partners (including :class:`Client
<lino_welfare.modlib.pcsw.models.Client>`).


..  This document is part of the test suite.  To test only this
  document, run::

    $ python setup.py test -s tests.DocsTests.test_dupable

This is a tested document:

>>> from __future__ import print_function, unicode_literals
>>> import os
>>> os.environ['DJANGO_SETTINGS_MODULE'] = \
...    'lino_welfare.projects.std.settings.doctests'
>>> from lino.api.doctest import *


In Lino Welfare, a :class:`Partner
<lino_welfare.modlib.contacts.models.Partner>` inherits from
:class:`DupablePartner
<lino.modlib.dupable_partners.mixins.DupablePartner>`.


Phonetic words
--------------

>>> rt.show(contacts.Partners, column_names="id name dupable_words")
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
===== ======================================================================= ===========================================
 ID    Name                                                                    dupable_words
----- ----------------------------------------------------------------------- -------------------------------------------
...
 260   Adam Ilja                                                               *ATM*, *AL*
 265   Adam Noémie                                                             *ATM*, *NM*
 266   Adam Odette                                                             *ATM*, *ATT*
 267   Adam Pascale                                                            *ATM*, *PSKL*
 268   Adam-Evrard                                                             *ATM*, *AFRR*
 269   Adam-Freisen                                                            *ATM*, *FRSN*
 203   Alliance Nationale des Mutualités Chrétiennes                           *ALNK*, *NXNL*, *TS*, *MTLT*, *KRTN*, ...
 192   Allmanns Alicia                                                         *ALMN*, *ALK*
 115   Altenberg Hans                                                          *ALTN*, *HNS*
 208   Apotheke Reul                                                           *AP0K*, *RL*
 209   Apotheke Schunck                                                        *AP0K*, *XNK*
 222   Arbeitsamt der D.G.                                                     *ARPT*, *TR*, *TK*
 113   Arens Andreas                                                           *ARNS*, *ANTR*
 114   Arens Annette                                                           *ARNS*, *ANT*
...
 124   Dobbelstein Dorothée                                                    *TPLS*, *TR0*
 123   Dobbelstein-Demeulenaere Dorothée                                       *TPLS*, *TMLN*, *TR0*
...
 167   Õunapuu Õie                                                             *NP*,
 195   ÖSHZ Kettenis                                                           *XS*, *KTNS*
 168   Östges Otto                                                             *STJS*, *AT*
===== ======================================================================= ===========================================
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

>>> rt.show(dupable_partners.SimilarPartners, pcsw.Client.objects.get(pk=122))
===========================================
 Other
-------------------------------------------
 *DOBBELSTEIN-DEMEULENAERE Dorothée (123)*
===========================================
<BLANKLINE>

>>> rt.show(dupable_partners.SimilarPartners, pcsw.Client.objects.get(pk=123))
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
===============================
 Other
-------------------------------
 *DEMEULENAERE Dorothée (122)*
 *DOBBELSTEIN Dorothée (124)*
===============================
<BLANKLINE>

>>> rt.show(dupable_partners.SimilarPartners, pcsw.Client.objects.get(pk=124))
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
===========================================
 Other
-------------------------------------------
 *DOBBELSTEIN-DEMEULENAERE Dorothée (123)*
===========================================
<BLANKLINE>

Note how the result can differ depending on the partner.  Our
algorithm is not perfect and does not detect all duplicates. 

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
and stores them in a separate database table.

How good (how bad) is our algorithm? See the source code of
`lino.projects.min2.tests.test_min2`.
