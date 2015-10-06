.. _welfare.specs.isip_chatelet:

=========================
ISIP contracts (Chatelet)
=========================

.. How to test only this document:

    $ python setup.py test -s tests.SpecsTests.test_isip_chatelet
    
    Doctest initialization:

    >>> from __future__ import print_function
    >>> import os
    >>> os.environ['DJANGO_SETTINGS_MODULE'] = \
    ...    'lino_welfare.projects.chatelet.settings.doctests'
    >>> from lino.api.doctest import *

    >>> ses = rt.login('robin')
    >>> translation.activate('en')


.. contents::
   :local:

Contracts
=========

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

This contract has a slave table 
:class:`EventsByContract<lino_welfare.modlib.isip.models.EventsByContract>`
which contains non-ascii characters:

>>> obj = isip.Contract.objects.get(id=1)
>>> rt.show(isip.EventsByContract, obj)
=============== ==========
 Summary         Date
--------------- ----------
 Évaluation 1    10/29/12
 Évaluation 2    11/29/12
 Évaluation 3    12/31/12
 Évaluation 4    1/31/13
 Évaluation 5    2/28/13
 Évaluation 6    3/28/13
 Évaluation 7    4/29/13
 Évaluation 8    5/29/13
 Évaluation 9    7/1/13
 Évaluation 10   8/1/13
=============== ==========
<BLANKLINE>


.. 20151005 tried to reproduce a unicode error
    >> context = obj.get_printable_context(ar)
    >> context.update(self=obj)
    >> context.update(self=obj)
    >> target = "tmp.odt"
    >> #bm = rt.modules.printing.BuildMethods.appyodt
    >> #action = obj.do_print.bound_action.action
    >> #action = rt.modules.excerpts.Excerpt.do_print
    >> # tplfile = bm.get_template_file(ar, action, obj)
    >> tplfile = settings.SITE.find_config_file('Default.odt', 'isip/Contract')

    >> from lino.modlib.appypod.appy_renderer import AppyRenderer
    >> r = AppyRenderer(ar, tplfile, context, target, **settings.SITE.appy_params).run()
