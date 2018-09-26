.. doctest docs/specs/isip.rst
.. _welfare.specs.isip:

==============
ISIP contracts
==============

.. Doctest initialization:

    >>> import lino
    >>> lino.startup('lino_welfare.projects.eupen.settings.doctests')
    >>> from lino.api.doctest import *

    >>> ses = rt.login('robin')
    >>> translation.activate('en')

This describes  the :mod:`lino_welfare.modlib.isip` plugin.
See also :doc:`/tour/autoevents`.

.. contents::
   :local:

.. class:: ClientHasContract

    Whether the client has at least one ISIP contact during the
    observed date range.
    
    A filter criteria added to
    :class:`lino_xl.lib.clients.ClientEvents`.


.. class:: ContractsByClient

    To see this table you need either IntegrationAgent or
    SocialCoordinator.


Visibility
==========

ISIP contracts are created and managed by Integration agents, but they
are also available for consultation to social agents, newcomer
consultants and reception clerks.

>>> p100 = users.UserTypes.get_by_value('100') # integ agents
>>> p200 = users.UserTypes.get_by_value('200') # newcomer agents
>>> p210 = users.UserTypes.get_by_value('210') # reception clerks
>>> p400 = users.UserTypes.get_by_value('400') # social agents

>>> isip.MyContracts.get_view_permission(p100)
True
>>> isip.MyContracts.get_view_permission(p200)  #doctest: +SKIP
False
>>> isip.MyContracts.get_view_permission(p210)  #doctest: +SKIP
False
>>> isip.MyContracts.get_view_permission(p400)  #doctest: +SKIP
False

>>> isip.ContractsByClient.get_view_permission(p100)
True
>>> isip.ContractsByClient.get_view_permission(p200)
True
>>> isip.ContractsByClient.get_view_permission(p210)
True
>>> isip.ContractsByClient.get_view_permission(p400)
True


Configuration
=============

>>> ses.show(isip.ContractTypes)
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE -REPORT_UDIFF
===================== =========== ==================== ==================
 Designation           Reference   Examination Policy   needs Study type
--------------------- ----------- -------------------- ------------------
 VSE Ausbildung        vsea        Every month          Yes
 VSE Arbeitssuche      vseb        Every month          No
 VSE Lehre             vsec        Every month          No
 VSE Vollzeitstudium   vsed        Every month          Yes
 VSE Sprachkurs        vsee        Every month          No
===================== =========== ==================== ==================
<BLANKLINE>


>>> rt.show(isip.Contracts)
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
==== ============== ============ ============================ ================= =====================
 ID   applies from   date ended   Client                       Author            Contract Type
---- -------------- ------------ ---------------------------- ----------------- ---------------------
 1    29/09/2012     07/08/2013   AUSDEMWALD Alfons (116)      Hubert Huppertz   VSE Ausbildung
 2    08/08/2013     01/12/2014   AUSDEMWALD Alfons (116)      Mélanie Mélard    VSE Arbeitssuche
 3    09/10/2012     17/08/2013   DOBBELSTEIN Dorothée (124)   Alicia Allmanns   VSE Lehre
 4    19/10/2012     11/02/2014   EVERS Eberhart (127)         Alicia Allmanns   VSE Vollzeitstudium
 5    12/02/2014     14/03/2014   EVERS Eberhart (127)         Caroline Carnol   VSE Sprachkurs
 6    15/03/2014     21/01/2015   EVERS Eberhart (127)         Caroline Carnol   VSE Ausbildung
 7    29/10/2012     21/02/2014   ENGELS Edgar (129)           Alicia Allmanns   VSE Arbeitssuche
 8    22/02/2014     31/12/2014   ENGELS Edgar (129)           Mélanie Mélard    VSE Lehre
 9    08/11/2012     03/03/2014   GROTECLAES Gregory (132)     Alicia Allmanns   VSE Vollzeitstudium
 10   18/11/2012     18/12/2012   JACOBS Jacqueline (137)      Alicia Allmanns   VSE Sprachkurs
 11   28/11/2012     06/10/2013   KAIVERS Karl (141)           Alicia Allmanns   VSE Ausbildung
 12   08/12/2012     02/04/2014   LAZARUS Line (144)           Alicia Allmanns   VSE Arbeitssuche
 13   03/04/2014     09/02/2015   LAZARUS Line (144)           Mélanie Mélard    VSE Lehre
 14   18/12/2012     12/04/2014   MEESSEN Melissa (147)        Mélanie Mélard    VSE Vollzeitstudium
 15   13/04/2014     13/05/2014   MEESSEN Melissa (147)        Mélanie Mélard    VSE Sprachkurs
 16   14/05/2014     22/03/2015   MEESSEN Melissa (147)        Mélanie Mélard    VSE Ausbildung
 17   28/12/2012     22/04/2014   RADERMACHER Alfons (153)     Alicia Allmanns   VSE Arbeitssuche
 18   07/01/2013     15/11/2013   RADERMACHER Edgard (157)     Alicia Allmanns   VSE Lehre
 19   17/01/2013     12/05/2014   RADERMACHER Guido (159)      Caroline Carnol   VSE Vollzeitstudium
 20   13/05/2014     12/06/2014   RADERMACHER Guido (159)      Mélanie Mélard    VSE Sprachkurs
 21   13/06/2014     21/04/2015   RADERMACHER Guido (159)      Mélanie Mélard    VSE Ausbildung
 22   27/01/2013     22/05/2014   DA VINCI David (165)         Alicia Allmanns   VSE Arbeitssuche
 23   23/05/2014     31/03/2015   DA VINCI David (165)         Alicia Allmanns   VSE Lehre
 24   06/02/2013     01/06/2014   ÖSTGES Otto (168)            Alicia Allmanns   VSE Vollzeitstudium
 25   02/06/2014     02/07/2014   ÖSTGES Otto (168)            Mélanie Mélard    VSE Sprachkurs
 26   03/07/2014     11/05/2015   ÖSTGES Otto (168)            Mélanie Mélard    VSE Ausbildung
 27   16/02/2013     11/06/2014   BRECHT Bernd (177)           Alicia Allmanns   VSE Arbeitssuche
 28   12/06/2014     20/04/2015   BRECHT Bernd (177)           Hubert Huppertz   VSE Lehre
 29   26/02/2013     21/06/2014   DUBOIS Robin (179)           Alicia Allmanns   VSE Vollzeitstudium
 30   22/06/2014     22/07/2014   DUBOIS Robin (179)           Mélanie Mélard    VSE Sprachkurs
 31   23/07/2014     31/05/2015   DUBOIS Robin (179)           Mélanie Mélard    VSE Ausbildung
 32   08/03/2013     01/07/2014   JEANÉMART Jérôme (181)       Mélanie Mélard    VSE Arbeitssuche
 33   02/07/2014     10/05/2015   JEANÉMART Jérôme (181)       Hubert Huppertz   VSE Lehre
==== ============== ============ ============================ ================= =====================
<BLANKLINE>


Contracts and Grantings
=======================

(The following is not yet very useful:)

>>> for obj in isip.Contracts.request():
...    print ("{} {} {}".format(obj.id, obj.applies_from, repr(obj.get_granting())))
1 2012-09-29 Granting #1 ('EiEi/29/09/2012/116')
2 2013-08-08 None
3 2012-10-09 Granting #3 ('EiEi/09/10/2012/124')
4 2012-10-19 Granting #4 ('Ausl\xe4nderbeihilfe/19/10/2012/127')
5 2014-02-12 None
6 2014-03-15 None
7 2012-10-29 Granting #7 ('EiEi/29/10/2012/129')
8 2014-02-22 None
9 2012-11-08 Granting #9 ('EiEi/08/11/2012/132')
10 2012-11-18 Granting #10 ('Ausl\xe4nderbeihilfe/18/11/2012/137')
11 2012-11-28 Granting #11 ('EiEi/28/11/2012/141')
12 2012-12-08 Granting #12 ('Ausl\xe4nderbeihilfe/08/12/2012/144')
13 2014-04-03 None
14 2012-12-18 Granting #14 ('Ausl\xe4nderbeihilfe/18/12/2012/147')
15 2014-04-13 None
16 2014-05-14 None
17 2012-12-28 Granting #17 ('EiEi/28/12/2012/153')
18 2013-01-07 Granting #18 ('Ausl\xe4nderbeihilfe/07/01/2013/157')
19 2013-01-17 Granting #19 ('EiEi/17/01/2013/159')
20 2014-05-13 None
21 2014-06-13 None
22 2013-01-27 Granting #22 ('Ausl\xe4nderbeihilfe/27/01/2013/165')
23 2014-05-23 None
24 2013-02-06 Granting #24 ('Ausl\xe4nderbeihilfe/06/02/2013/168')
25 2014-06-02 None
26 2014-07-03 None
27 2013-02-16 Granting #27 ('EiEi/16/02/2013/177')
28 2014-06-12 None
29 2013-02-26 Granting #29 ('EiEi/26/02/2013/179')
30 2014-06-22 None
31 2014-07-23 None
32 2013-03-08 Granting #32 ('Ausl\xe4nderbeihilfe/08/03/2013/181')
33 2014-07-02 None

