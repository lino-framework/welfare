.. _welfare.tested.dupe_clients:

===========================
Avoiding duplicate clients
===========================

Lino Welfare offers some functionality for avoiding duplicate 
:class:`Client <lino_welfare.modlib.pcsw.models.Client>` records.


..  This document is part of the test suite.  To test only this
  document, run::

    $ python setup.py test -s tests.SpecsTests.test_dupable

    doctest init:

    >>> from __future__ import print_function, unicode_literals
    >>> import lino
    >>> lino.startup('lino_welfare.projects.std.settings.doctests')
    >>> from lino.api.doctest import *


In Lino Welfare, a :class:`Client
<lino_welfare.modlib.pcsw.models.Client>` inherits from
:class:`DupableClient
<lino_welfare.modlib.dupable_clients.mixins.DupableClient>`.


Phonetic words
--------------

See :class:`lino.mixins.dupable.PhoneticWordBase`.

>>> rt.show(pcsw.CoachedClients, column_names="id name dupable_words")
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
===== ======================= ======================
 ID    Name                    dupable_words
----- ----------------------- ----------------------
 116   Ausdemwald Alfons       *ASTM*, *ALFN*
 177   Brecht Bernd            *PRKT*, *PRNT*
 118   Collard Charlotte       *KLRT*, *XRLT*
 124   Dobbelstein Dorothée    *TPLS*, *TR0*
 179   Dubois Robin            *TP*, *RPN*
 128   Emonts Daniel           *AMNT*, *TNL*
 152   Emonts-Gast Erna        *AMNT*, *KST*, *ARN*
 129   Engels Edgar            *ANJL*, *ATKR*
 127   Evers Eberhart          *AFRS*, *APRR*
 132   Groteclaes Gregory      *KRTK*, *KRKR*
 133   Hilgers Hildegard       *HLKR*, *HLTK*
 137   Jacobs Jacqueline       *JKPS*, *JKLN*
 181   Jeanémart Jérôme        *JNMR*, *JRM*
 139   Jonas Josef             *JNS*, *JSF*
 141   Kaivers Karl            *KFRS*, *KRL*
 178   Keller Karl             *KLR*, *KRL*
 142   Lambertz Guido          *LMPR*, *KT*
 144   Lazarus Line            *LSRS*, *LN*
 146   Malmendier Marc         *MLMN*, *MRK*
 147   Meessen Melissa         *MSN*, *MLS*
 153   Radermacher Alfons      *RTRM*, *ALFN*
 155   Radermacher Christian   *RTRM*, *KRSX*
 157   Radermacher Edgard      *RTRM*, *ATKR*
 159   Radermacher Guido       *RTRM*, *KT*
 161   Radermacher Hedi        *RTRM*, *HT*
 173   Radermecker Rik         *RTRM*, *RK*
 165   da Vinci David          *T*, *FNK*, *TFT*
 166   van Veen Vincent        *FN*, *FNKN*
 168   Östges Otto             *STJS*, *AT*
===== ======================= ======================
<BLANKLINE>



Similar Clients
----------------

The test database contains a fictive person named Dorothée
Dobbelstein-Demeulenaere as an example of accidental duplicate data
entry.  Dorothée exists 3 times in our database:

>>> for p in pcsw.Client.objects.filter(name__contains="Dorothée"):
...     print(unicode(p))
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
DEMEULENAERE Dorothée (122)
DOBBELSTEIN Dorothée (124)
DOBBELSTEIN-DEMEULENAERE Dorothée (123)

The detail window of each of these records shows some of the other
records in the `SimilarClients` table:

>>> rt.show(dupable_clients.SimilarClients, pcsw.Client.objects.get(pk=122))
*DOBBELSTEIN-DEMEULENAERE Dorothée (123)* Phonetic words: TMLN, TR0

>>> rt.show(dupable_clients.SimilarClients, pcsw.Client.objects.get(pk=123))
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
*DEMEULENAERE Dorothée (122)* *DOBBELSTEIN Dorothée (124)* Phonetic words: TPLS, TMLN, TR0

>>> rt.show(dupable_clients.SimilarClients, pcsw.Client.objects.get(pk=124))
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
*DOBBELSTEIN-DEMEULENAERE Dorothée (123)* Phonetic words: TPLS, TR0

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

This is because :class:`lino.mixins.dupable.Dupable` replaces
the standard `submit_insert` action by the :class:`CheckedSubmitInsert
<lino.modlib.dedupe.mixins.CheckedSubmitInsert>` action.


The algorithm
-------------

The alarm bell rings when there are **two similar name components** in
both first and last name. Punctuation characters (like "-" or "&" or
",") are ignored, and also the ordering of elements does not matter.

The current implementation splits the :attr:`name
<lino.modlib.contacts.models.Partner.name>` of each client into its parts,
removing punctuation characters, computes a phonetic version using the
`NYSIIS algorithm
<https://en.wikipedia.org/wiki/New_York_State_Identification_and_Intelligence_System>`_
and stores them in a separate database table.

How good (how bad) is our algorithm? See the source code of
`lino.projects.min2.tests.test_min2`.
