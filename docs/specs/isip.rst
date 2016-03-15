.. _welfare.specs.isip:

==============
ISIP contracts
==============

.. How to test only this document:

    $ python setup.py test -s tests.SpecsTests.test_isip
    
    Doctest initialization:

    >>> from __future__ import print_function
    >>> import os
    >>> os.environ['DJANGO_SETTINGS_MODULE'] = \
    ...    'lino_welfare.projects.std.settings.doctests'
    >>> from lino.api.doctest import *

    >>> ses = rt.login('robin')
    >>> translation.activate('en')

A technical tour into the :mod:`lino_welfare.modlib.isip` module.
See also :doc:`/tour/autoevents`.

.. contents::
   :local:

Configuration
=============

>>> ses.show(isip.ContractTypes)
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE -REPORT_UDIFF
===================== ===================== ===================== =========== ==================== ==================
 Designation           Designation (fr)      Designation (de)      Reference   Examination Policy   needs Study type
--------------------- --------------------- --------------------- ----------- -------------------- ------------------
 VSE Ausbildung        VSE Ausbildung        VSE Ausbildung        vsea        Every month          Yes
 VSE Arbeitssuche      VSE Arbeitssuche      VSE Arbeitssuche      vseb        Every month          No
 VSE Lehre             VSE Lehre             VSE Lehre             vsec        Every month          No
 VSE Vollzeitstudium   VSE Vollzeitstudium   VSE Vollzeitstudium   vsed        Every month          Yes
 VSE Sprachkurs        VSE Sprachkurs        VSE Sprachkurs        vsee        Every month          No
 **Total (5 rows)**                                                                                 **2**
===================== ===================== ===================== =========== ==================== ==================
<BLANKLINE>


>>> rt.show(isip.Contracts)
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE -REPORT_UDIFF
==== ============== =============== ============================ =================== =====================
 ID   applies from   applies until   Client                       Integration agent   Contract Type
---- -------------- --------------- ---------------------------- ------------------- ---------------------
 1    9/29/12        8/7/13          AUSDEMWALD Alfons (116)      Hubert Huppertz     VSE Ausbildung
 2    8/8/13         12/1/14         AUSDEMWALD Alfons (116)      Mélanie Mélard      VSE Arbeitssuche
 3    10/9/12        8/17/13         COLLARD Charlotte (118)      Alicia Allmanns     VSE Lehre
 4    10/19/12       2/11/14         DOBBELSTEIN Dorothée (124)   Alicia Allmanns     VSE Vollzeitstudium
 5    2/12/14        3/14/14         DOBBELSTEIN Dorothée (124)   Caroline Carnol     VSE Sprachkurs
 6    3/15/14        1/21/15         DOBBELSTEIN Dorothée (124)   Caroline Carnol     VSE Ausbildung
 7    11/3/12        2/26/14         EMONTS-GAST Erna (152)       Alicia Allmanns     VSE Arbeitssuche
 8    11/13/12       12/13/12        EVERS Eberhart (127)         Alicia Allmanns     VSE Lehre
 9    11/23/12       10/1/13         FAYMONVILLE Luc (130*)       Mélanie Mélard      VSE Vollzeitstudium
 10   10/2/13        1/25/15         FAYMONVILLE Luc (130*)       Hubert Huppertz     VSE Sprachkurs
 11   12/8/12        4/2/14          JACOBS Jacqueline (137)      Alicia Allmanns     VSE Ausbildung
 12   4/3/14         5/3/14          JACOBS Jacqueline (137)      Mélanie Mélard      VSE Arbeitssuche
 13   5/4/14         3/12/15         JACOBS Jacqueline (137)      Mélanie Mélard      VSE Lehre
 14   12/18/12       4/12/14         JONAS Josef (139)            Hubert Huppertz     VSE Vollzeitstudium
 15   4/13/14        2/19/15         JONAS Josef (139)            Hubert Huppertz     VSE Sprachkurs
 16   12/28/12       4/22/14         KELLER Karl (178)            Alicia Allmanns     VSE Ausbildung
 17   1/12/13        11/20/13        MALMENDIER Marc (146)        Mélanie Mélard      VSE Arbeitssuche
 18   11/21/13       3/16/15         MALMENDIER Marc (146)        Hubert Huppertz     VSE Lehre
 19   1/22/13        11/30/13        RADERMACHER Alfons (153)     Alicia Allmanns     VSE Vollzeitstudium
 20   2/1/13         5/27/14         RADERMACHER Edgard (157)     Alicia Allmanns     VSE Sprachkurs
 21   5/28/14        6/27/14         RADERMACHER Edgard (157)     Hubert Huppertz     VSE Ausbildung
 22   6/28/14        5/6/15          RADERMACHER Edgard (157)     Hubert Huppertz     VSE Arbeitssuche
 23   2/16/13        6/11/14         RADERMACHER Hedi (161)       Alicia Allmanns     VSE Lehre
 24   6/12/14        7/12/14         RADERMACHER Hedi (161)       Hubert Huppertz     VSE Vollzeitstudium
 25   7/13/14        5/21/15         RADERMACHER Hedi (161)       Hubert Huppertz     VSE Sprachkurs
 26   2/26/13        6/21/14         DA VINCI David (165)         Alicia Allmanns     VSE Ausbildung
 27   6/22/14        4/30/15         DA VINCI David (165)         Alicia Allmanns     VSE Arbeitssuche
 28   3/8/13         7/1/14          ÖSTGES Otto (168)            Mélanie Mélard      VSE Lehre
 29   7/2/14         8/1/14          ÖSTGES Otto (168)            Hubert Huppertz     VSE Vollzeitstudium
 30   8/2/14         6/10/15         ÖSTGES Otto (168)            Hubert Huppertz     VSE Sprachkurs
==== ============== =============== ============================ =================== =====================
<BLANKLINE>


Contracts and Grantings
=======================

(The following is not yet very useful:)

>>> for obj in isip.Contracts.request():
...    print obj.id, obj.applies_from, repr(obj.get_granting())
1 2012-09-29 Granting #1 ('EiEi/9/29/12/116')
2 2013-08-08 None
3 2012-10-09 Granting #3 ('EiEi/10/9/12/118')
4 2012-10-19 Granting #4 ('Ausl\xe4nderbeihilfe/10/19/12/124')
5 2014-02-12 None
6 2014-03-15 None
7 2012-11-03 Granting #7 ('EiEi/11/3/12/152')
8 2012-11-13 Granting #8 ('Ausl\xe4nderbeihilfe/11/13/12/127')
9 2012-11-23 Granting #9 ('EiEi/11/23/12/130')
10 2013-10-02 None
11 2012-12-08 Granting #11 ('EiEi/12/8/12/137')
12 2014-04-03 None
13 2014-05-04 None
14 2012-12-18 Granting #14 ('Ausl\xe4nderbeihilfe/12/18/12/139')
15 2014-04-13 None
16 2012-12-28 Granting #16 ('Ausl\xe4nderbeihilfe/12/28/12/178')
17 2013-01-12 Granting #17 ('EiEi/1/12/13/146')
18 2013-11-21 None
19 2013-01-22 Granting #19 ('EiEi/1/22/13/153')
20 2013-02-01 Granting #20 ('Ausl\xe4nderbeihilfe/2/1/13/157')
21 2014-05-28 None
22 2014-06-28 None
23 2013-02-16 Granting #23 ('EiEi/2/16/13/161')
24 2014-06-12 None
25 2014-07-13 None
26 2013-02-26 Granting #26 ('Ausl\xe4nderbeihilfe/2/26/13/165')
27 2014-06-22 None
28 2013-03-08 Granting #28 ('Ausl\xe4nderbeihilfe/3/8/13/168')
29 2014-07-02 None
30 2014-08-02 None
