.. _welfare.tested.plausibility:

==============================
Managing plausibility problems
==============================

Lino Welfare offers some functionality for managing 
plausibility problems.
See :mod:`<lino.modlib.plausibility`.


..  This document is part of the test suite.  To test only this
  document, run::

    $ python setup.py test -s tests.DocsTests.test_plausibility

This is a tested document:

>>> from __future__ import print_function, unicode_literals
>>> import os
>>> os.environ['DJANGO_SETTINGS_MODULE'] = \
...    'lino_welfare.projects.std.settings.doctests'
>>> from lino.api.doctest import *


Showing all problems
====================

>>> rt.show(plausibility.AllProblems)
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE -REPORT_UDIFF
================= =========================================== ============================================================================ ========= ===========================
 Responsible       Controlled by                               Message                                                                      Fixable   Plausibility checker
----------------- ------------------------------------------- ---------------------------------------------------------------------------- --------- ---------------------------
 Caroline Carnol   *AUSDEMWALD Alfons (116)*                   Neither valid eId data nor alternative identifying document.                 No        Check SSIN validity
                   *BASTIAENSEN Laurent (117)*                 Neither valid eId data nor alternative identifying document.                 No        Check SSIN validity
                   *BRAUN Bruno (257)*                         Neither valid eId data nor alternative identifying document.                 No        Check SSIN validity
                   *CHANTRAINE Marc (120*)*                    Neither valid eId data nor alternative identifying document.                 No        Check SSIN validity
 Hubert Huppertz   *COLLARD Charlotte (118)*                   Neither valid eId data nor alternative identifying document.                 No        Check SSIN validity
                   *DEMEULENAERE Dorothée (122)*               Neither valid eId data nor alternative identifying document.                 No        Check SSIN validity
                   *DEMEULENAERE Dorothée (122)*               1 similar clients: DOBBELSTEIN-DEMEULENAERE Dorothée (123)                   No        Check for similar clients
 Mélanie Mélard    *DENON Denis (180*)*                        Neither valid eId data nor alternative identifying document.                 No        Check SSIN validity
 Mélanie Mélard    *DENON Denis (180*)*                        Both coached and obsolete.                                                   No        Check coachings
 Mélanie Mélard    *DOBBELSTEIN Dorothée (124)*                Neither valid eId data nor alternative identifying document.                 No        Check SSIN validity
 Mélanie Mélard    *DOBBELSTEIN Dorothée (124)*                1 similar clients: DOBBELSTEIN-DEMEULENAERE Dorothée (123)                   No        Check for similar clients
 Mélanie Mélard    *DOBBELSTEIN-DEMEULENAERE Dorothée (123)*   2 similar clients: DEMEULENAERE Dorothée (122), DOBBELSTEIN Dorothée (124)   No        Check for similar clients
 Hubert Huppertz   *DUBOIS Robin (179)*                        Neither valid eId data nor alternative identifying document.                 No        Check SSIN validity
                   *EIERSCHAL Emil (175)*                      Neither valid eId data nor alternative identifying document.                 No        Check SSIN validity
 Mélanie Mélard    *EMONTS Daniel (128)*                       Neither valid eId data nor alternative identifying document.                 No        Check SSIN validity
                   *EMONTS Erich (150*)*                       Neither valid eId data nor alternative identifying document.                 No        Check SSIN validity
 Hubert Huppertz   *EMONTS-GAST Erna (152)*                    Neither valid eId data nor alternative identifying document.                 No        Check SSIN validity
                   *EMONTSPOOL Erwin (151)*                    Neither valid eId data nor alternative identifying document.                 No        Check SSIN validity
 Mélanie Mélard    *ENGELS Edgar (129)*                        Neither valid eId data nor alternative identifying document.                 No        Check SSIN validity
                   *ERNST Berta (125)*                         Neither valid eId data nor alternative identifying document.                 No        Check SSIN validity
 Alicia Allmanns   *EVERS Eberhart (127)*                      Neither valid eId data nor alternative identifying document.                 No        Check SSIN validity
 Mélanie Mélard    *FAYMONVILLE Luc (130*)*                    Neither valid eId data nor alternative identifying document.                 No        Check SSIN validity
 Mélanie Mélard    *FAYMONVILLE Luc (130*)*                    Both coached and obsolete.                                                   No        Check coachings
                   *FRISCH Paul (238)*                         Neither valid eId data nor alternative identifying document.                 No        Check SSIN validity
                   *GERNEGROß Germaine (131)*                  Neither valid eId data nor alternative identifying document.                 No        Check SSIN validity
 Alicia Allmanns   *GROTECLAES Gregory (132)*                  Neither valid eId data nor alternative identifying document.                 No        Check SSIN validity
                   *HILGERS Henri (134)*                       Neither valid eId data nor alternative identifying document.                 No        Check SSIN validity
 Mélanie Mélard    *HILGERS Hildegard (133)*                   Neither valid eId data nor alternative identifying document.                 No        Check SSIN validity
                   *INGELS Irene (135)*                        Neither valid eId data nor alternative identifying document.                 No        Check SSIN validity
 Caroline Carnol   *JACOBS Jacqueline (137)*                   Neither valid eId data nor alternative identifying document.                 No        Check SSIN validity
                   *JANSEN Jérémy (136)*                       Neither valid eId data nor alternative identifying document.                 No        Check SSIN validity
 Hubert Huppertz   *JEANÉMART Jérôme (181)*                    Neither valid eId data nor alternative identifying document.                 No        Check SSIN validity
 Hubert Huppertz   *JONAS Josef (139)*                         Neither valid eId data nor alternative identifying document.                 No        Check SSIN validity
                   *JOUSTEN Jan (140*)*                        Neither valid eId data nor alternative identifying document.                 No        Check SSIN validity
 Mélanie Mélard    *KAIVERS Karl (141)*                        Neither valid eId data nor alternative identifying document.                 No        Check SSIN validity
                   *KASENNOVA Tatjana (221)*                   Neither valid eId data nor alternative identifying document.                 No        Check SSIN validity
 Hubert Huppertz   *KELLER Karl (178)*                         Neither valid eId data nor alternative identifying document.                 No        Check SSIN validity
                   *LAHM Lisa (176)*                           Neither valid eId data nor alternative identifying document.                 No        Check SSIN validity
 Mélanie Mélard    *LAMBERTZ Guido (142)*                      Neither valid eId data nor alternative identifying document.                 No        Check SSIN validity
                   *LASCHET Laura (143)*                       Neither valid eId data nor alternative identifying document.                 No        Check SSIN validity
 Mélanie Mélard    *LAZARUS Line (144)*                        Neither valid eId data nor alternative identifying document.                 No        Check SSIN validity
 Hubert Huppertz   *MALMENDIER Marc (146)*                     Neither valid eId data nor alternative identifying document.                 No        Check SSIN validity
                   *MARTELAER Mark (172)*                      Neither valid eId data nor alternative identifying document.                 No        Check SSIN validity
 Mélanie Mélard    *MEESSEN Melissa (147)*                     Neither valid eId data nor alternative identifying document.                 No        Check SSIN validity
                   *MEIER Marie-Louise (149)*                  Neither valid eId data nor alternative identifying document.                 No        Check SSIN validity
 Mélanie Mélard    *RADERMACHER Alfons (153)*                  Neither valid eId data nor alternative identifying document.                 No        Check SSIN validity
                   *RADERMACHER Berta (154)*                   Neither valid eId data nor alternative identifying document.                 No        Check SSIN validity
 Alicia Allmanns   *RADERMACHER Christian (155)*               Neither valid eId data nor alternative identifying document.                 No        Check SSIN validity
                   *RADERMACHER Daniela (156)*                 Neither valid eId data nor alternative identifying document.                 No        Check SSIN validity
 Caroline Carnol   *RADERMACHER Edgard (157)*                  Neither valid eId data nor alternative identifying document.                 No        Check SSIN validity
 Mélanie Mélard    *RADERMACHER Guido (159)*                   Neither valid eId data nor alternative identifying document.                 No        Check SSIN validity
                   *RADERMACHER Hans (160*)*                   Neither valid eId data nor alternative identifying document.                 No        Check SSIN validity
 Caroline Carnol   *RADERMACHER Hedi (161)*                    Neither valid eId data nor alternative identifying document.                 No        Check SSIN validity
                   *RADERMACHER Inge (162)*                    Neither valid eId data nor alternative identifying document.                 No        Check SSIN validity
 Mélanie Mélard    *RADERMECKER Rik (173)*                     Neither valid eId data nor alternative identifying document.                 No        Check SSIN validity
                   *VANDENMEULENBOS Marie-Louise (174)*        Neither valid eId data nor alternative identifying document.                 No        Check SSIN validity
 Hubert Huppertz   *DA VINCI David (165)*                      Neither valid eId data nor alternative identifying document.                 No        Check SSIN validity
                   *DI RUPO Didier (164)*                      Neither valid eId data nor alternative identifying document.                 No        Check SSIN validity
 Hubert Huppertz   *VAN VEEN Vincent (166)*                    Neither valid eId data nor alternative identifying document.                 No        Check SSIN validity
 Hubert Huppertz   *ÖSTGES Otto (168)*                         Neither valid eId data nor alternative identifying document.                 No        Check SSIN validity
================= =========================================== ============================================================================ ========= ===========================
<BLANKLINE>

The user can set the table parameters e.g. to see only problems of a
given type ("checker"):

>>> Checkers = rt.modules.plausibility.Checkers
>>> rt.show(plausibility.AllProblems, param_values=dict(checker=Checkers.get_by_value('pcsw.Client.SimilarClientsChecker')))
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE -REPORT_UDIFF
================ =========================================== ============================================================================ ========= ===========================
 Responsible      Controlled by                               Message                                                                      Fixable   Plausibility checker
---------------- ------------------------------------------- ---------------------------------------------------------------------------- --------- ---------------------------
                  *DEMEULENAERE Dorothée (122)*               1 similar clients: DOBBELSTEIN-DEMEULENAERE Dorothée (123)                   No        Check for similar clients
 Mélanie Mélard   *DOBBELSTEIN Dorothée (124)*                1 similar clients: DOBBELSTEIN-DEMEULENAERE Dorothée (123)                   No        Check for similar clients
 Mélanie Mélard   *DOBBELSTEIN-DEMEULENAERE Dorothée (123)*   2 similar clients: DEMEULENAERE Dorothée (122), DOBBELSTEIN Dorothée (124)   No        Check for similar clients
================ =========================================== ============================================================================ ========= ===========================
<BLANKLINE>


>>> rt.login('melanie').show(plausibility.MyProblems)
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
================ =========================================== ============================================================================ ========= ===========================
 Responsible      Controlled by                               Message                                                                      Fixable   Plausibility checker
---------------- ------------------------------------------- ---------------------------------------------------------------------------- --------- ---------------------------
 Mélanie Mélard   *DENON Denis (180*)*                        Neither valid eId data nor alternative identifying document.                 No        Check SSIN validity
 Mélanie Mélard   *DENON Denis (180*)*                        Both coached and obsolete.                                                   No        Check coachings
 Mélanie Mélard   *DOBBELSTEIN Dorothée (124)*                Neither valid eId data nor alternative identifying document.                 No        Check SSIN validity
 Mélanie Mélard   *DOBBELSTEIN Dorothée (124)*                1 similar clients: DOBBELSTEIN-DEMEULENAERE Dorothée (123)                   No        Check for similar clients
 Mélanie Mélard   *DOBBELSTEIN-DEMEULENAERE Dorothée (123)*   2 similar clients: DEMEULENAERE Dorothée (122), DOBBELSTEIN Dorothée (124)   No        Check for similar clients
 Mélanie Mélard   *EMONTS Daniel (128)*                       Neither valid eId data nor alternative identifying document.                 No        Check SSIN validity
 Mélanie Mélard   *ENGELS Edgar (129)*                        Neither valid eId data nor alternative identifying document.                 No        Check SSIN validity
 Mélanie Mélard   *FAYMONVILLE Luc (130*)*                    Neither valid eId data nor alternative identifying document.                 No        Check SSIN validity
 Mélanie Mélard   *FAYMONVILLE Luc (130*)*                    Both coached and obsolete.                                                   No        Check coachings
 Mélanie Mélard   *HILGERS Hildegard (133)*                   Neither valid eId data nor alternative identifying document.                 No        Check SSIN validity
 Mélanie Mélard   *KAIVERS Karl (141)*                        Neither valid eId data nor alternative identifying document.                 No        Check SSIN validity
 Mélanie Mélard   *LAMBERTZ Guido (142)*                      Neither valid eId data nor alternative identifying document.                 No        Check SSIN validity
 Mélanie Mélard   *LAZARUS Line (144)*                        Neither valid eId data nor alternative identifying document.                 No        Check SSIN validity
 Mélanie Mélard   *MEESSEN Melissa (147)*                     Neither valid eId data nor alternative identifying document.                 No        Check SSIN validity
 Mélanie Mélard   *RADERMACHER Alfons (153)*                  Neither valid eId data nor alternative identifying document.                 No        Check SSIN validity
 Mélanie Mélard   *RADERMACHER Guido (159)*                   Neither valid eId data nor alternative identifying document.                 No        Check SSIN validity
 Mélanie Mélard   *RADERMECKER Rik (173)*                     Neither valid eId data nor alternative identifying document.                 No        Check SSIN validity
================ =========================================== ============================================================================ ========= ===========================
<BLANKLINE>
