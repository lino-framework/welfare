.. _welfare.specs.isip_chatelet:

=========================
ISIP contracts (Chatelet)
=========================

.. How to test only this document:

    $ python setup.py test -s tests.SpecsTests.test_isip_chatelet
    
    Doctest initialization:

    >>> from lino import startup
    >>> startup('lino_welfare.projects.chatelet.settings.doctests')
    >>> from lino.api.doctest import *

    >>> ses = rt.login('robin')
    >>> translation.activate('en')


.. contents::
   :local:

Contracts
=========

>>> rt.show(isip.Contracts)
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE -REPORT_UDIFF
==== ============== =============== ============================ ================= =====================
 ID   applies from   applies until   Client                       Author            Contract Type
---- -------------- --------------- ---------------------------- ----------------- ---------------------
 1    29/09/2012     07/08/2013      AUSDEMWALD Alfons (116)      Hubert Huppertz   VSE Ausbildung
 2    08/08/2013     01/12/2014      AUSDEMWALD Alfons (116)      Mélanie Mélard    VSE Arbeitssuche
 3    09/10/2012     17/08/2013      COLLARD Charlotte (118)      Alicia Allmanns   VSE Lehre
 4    19/10/2012     11/02/2014      DOBBELSTEIN Dorothée (124)   Alicia Allmanns   VSE Vollzeitstudium
 5    12/02/2014     14/03/2014      DOBBELSTEIN Dorothée (124)   Caroline Carnol   VSE Sprachkurs
 6    15/03/2014     21/01/2015      DOBBELSTEIN Dorothée (124)   Caroline Carnol   VSE Ausbildung
 7    03/11/2012     26/02/2014      EMONTS-GAST Erna (152)       Alicia Allmanns   VSE Arbeitssuche
 8    13/11/2012     13/12/2012      EVERS Eberhart (127)         Alicia Allmanns   VSE Lehre
 9    23/11/2012     01/10/2013      FAYMONVILLE Luc (130*)       Mélanie Mélard    VSE Vollzeitstudium
 10   02/10/2013     25/01/2015      FAYMONVILLE Luc (130*)       Hubert Huppertz   VSE Sprachkurs
 11   08/12/2012     02/04/2014      JACOBS Jacqueline (137)      Alicia Allmanns   VSE Ausbildung
 12   03/04/2014     03/05/2014      JACOBS Jacqueline (137)      Mélanie Mélard    VSE Arbeitssuche
 13   04/05/2014     12/03/2015      JACOBS Jacqueline (137)      Mélanie Mélard    VSE Lehre
 14   18/12/2012     12/04/2014      JONAS Josef (139)            Hubert Huppertz   VSE Vollzeitstudium
 15   13/04/2014     19/02/2015      JONAS Josef (139)            Hubert Huppertz   VSE Sprachkurs
 16   28/12/2012     22/04/2014      KELLER Karl (178)            Alicia Allmanns   VSE Ausbildung
 17   12/01/2013     20/11/2013      MALMENDIER Marc (146)        Mélanie Mélard    VSE Arbeitssuche
 18   21/11/2013     16/03/2015      MALMENDIER Marc (146)        Hubert Huppertz   VSE Lehre
 19   22/01/2013     30/11/2013      RADERMACHER Alfons (153)     Alicia Allmanns   VSE Vollzeitstudium
 20   01/02/2013     27/05/2014      RADERMACHER Edgard (157)     Alicia Allmanns   VSE Sprachkurs
 21   28/05/2014     27/06/2014      RADERMACHER Edgard (157)     Hubert Huppertz   VSE Ausbildung
 22   28/06/2014     06/05/2015      RADERMACHER Edgard (157)     Hubert Huppertz   VSE Arbeitssuche
 23   16/02/2013     11/06/2014      RADERMACHER Hedi (161)       Alicia Allmanns   VSE Lehre
 24   12/06/2014     12/07/2014      RADERMACHER Hedi (161)       Hubert Huppertz   VSE Vollzeitstudium
 25   13/07/2014     21/05/2015      RADERMACHER Hedi (161)       Hubert Huppertz   VSE Sprachkurs
 26   26/02/2013     21/06/2014      DA VINCI David (165)         Alicia Allmanns   VSE Ausbildung
 27   22/06/2014     30/04/2015      DA VINCI David (165)         Alicia Allmanns   VSE Arbeitssuche
 28   08/03/2013     01/07/2014      ÖSTGES Otto (168)            Mélanie Mélard    VSE Lehre
 29   02/07/2014     01/08/2014      ÖSTGES Otto (168)            Hubert Huppertz   VSE Vollzeitstudium
 30   02/08/2014     10/06/2015      ÖSTGES Otto (168)            Hubert Huppertz   VSE Sprachkurs
==== ============== =============== ============================ ================= =====================
<BLANKLINE>


This contract has a slave table 
:class:`EntriesByContract<lino_welfare.modlib.isip.models.EntriesByContract>`
which contains non-ascii characters:

>>> obj = isip.Contract.objects.get(id=1)
>>> rt.show(isip.EntriesByContract, obj)
=============== ============
 Summary         Date
--------------- ------------
 Évaluation 1    29/10/2012
 Évaluation 2    29/11/2012
 Évaluation 3    31/12/2012
 Évaluation 4    31/01/2013
 Évaluation 5    28/02/2013
 Évaluation 6    28/03/2013
 Évaluation 7    29/04/2013
 Évaluation 8    29/05/2013
 Évaluation 9    01/07/2013
 Évaluation 10   01/08/2013
=============== ============
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
