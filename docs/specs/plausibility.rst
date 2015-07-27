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
================= =========================================== ============================================================== ================================
 Responsible       Controlled by                               Message                                                        Plausibility checker
----------------- ------------------------------------------- -------------------------------------------------------------- --------------------------------
 Caroline Carnol   *AUSDEMWALD Alfons (116)*                   Neither valid eId data nor alternative identifying document.   Check for valid identification
                   *BASTIAENSEN Laurent (117)*                 Neither valid eId data nor alternative identifying document.   Check for valid identification
 Hubert Huppertz   *COLLARD Charlotte (118)*                   Neither valid eId data nor alternative identifying document.   Check for valid identification
                   *CHANTRAINE Marc (120*)*                    Neither valid eId data nor alternative identifying document.   Check for valid identification
                   *DEMEULENAERE Dorothée (122)*               Similar clients: DOBBELSTEIN-DEMEULENAERE Dorothée (123)       Check for similar clients
                   *DEMEULENAERE Dorothée (122)*               Neither valid eId data nor alternative identifying document.   Check for valid identification
 Mélanie Mélard    *DOBBELSTEIN-DEMEULENAERE Dorothée (123)*   Similar clients: DEMEULENAERE Dorothée (122)                   Check for similar clients
 Mélanie Mélard    *DOBBELSTEIN Dorothée (124)*                Similar clients: DOBBELSTEIN-DEMEULENAERE Dorothée (123)       Check for similar clients
 Mélanie Mélard    *DOBBELSTEIN Dorothée (124)*                Neither valid eId data nor alternative identifying document.   Check for valid identification
                   *ERNST Berta (125)*                         Neither valid eId data nor alternative identifying document.   Check for valid identification
 Alicia Allmanns   *EVERS Eberhart (127)*                      Neither valid eId data nor alternative identifying document.   Check for valid identification
 Mélanie Mélard    *EMONTS Daniel (128)*                       Neither valid eId data nor alternative identifying document.   Check for valid identification
 Mélanie Mélard    *ENGELS Edgar (129)*                        Neither valid eId data nor alternative identifying document.   Check for valid identification
 Mélanie Mélard    *FAYMONVILLE Luc (130*)*                    Both coached and obsolete.                                     Check coachings
 Mélanie Mélard    *FAYMONVILLE Luc (130*)*                    Neither valid eId data nor alternative identifying document.   Check for valid identification
                   *GERNEGROß Germaine (131)*                  Neither valid eId data nor alternative identifying document.   Check for valid identification
 Alicia Allmanns   *GROTECLAES Gregory (132)*                  Neither valid eId data nor alternative identifying document.   Check for valid identification
 Mélanie Mélard    *HILGERS Hildegard (133)*                   Neither valid eId data nor alternative identifying document.   Check for valid identification
                   *HILGERS Henri (134)*                       Neither valid eId data nor alternative identifying document.   Check for valid identification
                   *INGELS Irene (135)*                        Neither valid eId data nor alternative identifying document.   Check for valid identification
                   *JANSEN Jérémy (136)*                       Neither valid eId data nor alternative identifying document.   Check for valid identification
 Caroline Carnol   *JACOBS Jacqueline (137)*                   Neither valid eId data nor alternative identifying document.   Check for valid identification
 Hubert Huppertz   *JONAS Josef (139)*                         Neither valid eId data nor alternative identifying document.   Check for valid identification
                   *JOUSTEN Jan (140*)*                        Neither valid eId data nor alternative identifying document.   Check for valid identification
 Mélanie Mélard    *KAIVERS Karl (141)*                        Neither valid eId data nor alternative identifying document.   Check for valid identification
 Mélanie Mélard    *LAMBERTZ Guido (142)*                      Neither valid eId data nor alternative identifying document.   Check for valid identification
                   *LASCHET Laura (143)*                       Neither valid eId data nor alternative identifying document.   Check for valid identification
 Mélanie Mélard    *LAZARUS Line (144)*                        Neither valid eId data nor alternative identifying document.   Check for valid identification
 Hubert Huppertz   *MALMENDIER Marc (146)*                     Neither valid eId data nor alternative identifying document.   Check for valid identification
 Mélanie Mélard    *MEESSEN Melissa (147)*                     Neither valid eId data nor alternative identifying document.   Check for valid identification
                   *MEIER Marie-Louise (149)*                  Neither valid eId data nor alternative identifying document.   Check for valid identification
                   *EMONTS Erich (150*)*                       Neither valid eId data nor alternative identifying document.   Check for valid identification
                   *EMONTSPOOL Erwin (151)*                    Neither valid eId data nor alternative identifying document.   Check for valid identification
 Hubert Huppertz   *EMONTS-GAST Erna (152)*                    Neither valid eId data nor alternative identifying document.   Check for valid identification
 Mélanie Mélard    *RADERMACHER Alfons (153)*                  Neither valid eId data nor alternative identifying document.   Check for valid identification
                   *RADERMACHER Berta (154)*                   Neither valid eId data nor alternative identifying document.   Check for valid identification
 Alicia Allmanns   *RADERMACHER Christian (155)*               Neither valid eId data nor alternative identifying document.   Check for valid identification
                   *RADERMACHER Daniela (156)*                 Neither valid eId data nor alternative identifying document.   Check for valid identification
 Caroline Carnol   *RADERMACHER Edgard (157)*                  Neither valid eId data nor alternative identifying document.   Check for valid identification
 Mélanie Mélard    *RADERMACHER Guido (159)*                   Neither valid eId data nor alternative identifying document.   Check for valid identification
                   *RADERMACHER Hans (160*)*                   Neither valid eId data nor alternative identifying document.   Check for valid identification
 Caroline Carnol   *RADERMACHER Hedi (161)*                    Neither valid eId data nor alternative identifying document.   Check for valid identification
                   *RADERMACHER Inge (162)*                    Neither valid eId data nor alternative identifying document.   Check for valid identification
                   *DI RUPO Didier (164)*                      Neither valid eId data nor alternative identifying document.   Check for valid identification
 Hubert Huppertz   *DA VINCI David (165)*                      Neither valid eId data nor alternative identifying document.   Check for valid identification
 Hubert Huppertz   *VAN VEEN Vincent (166)*                    Neither valid eId data nor alternative identifying document.   Check for valid identification
 Hubert Huppertz   *ÖSTGES Otto (168)*                         Neither valid eId data nor alternative identifying document.   Check for valid identification
                   *MARTELAER Mark (172)*                      Neither valid eId data nor alternative identifying document.   Check for valid identification
 Mélanie Mélard    *RADERMECKER Rik (173)*                     Neither valid eId data nor alternative identifying document.   Check for valid identification
                   *VANDENMEULENBOS Marie-Louise (174)*        Neither valid eId data nor alternative identifying document.   Check for valid identification
                   *EIERSCHAL Emil (175)*                      Neither valid eId data nor alternative identifying document.   Check for valid identification
                   *LAHM Lisa (176)*                           Neither valid eId data nor alternative identifying document.   Check for valid identification
 Hubert Huppertz   *KELLER Karl (178)*                         Neither valid eId data nor alternative identifying document.   Check for valid identification
 Hubert Huppertz   *DUBOIS Robin (179)*                        Neither valid eId data nor alternative identifying document.   Check for valid identification
 Mélanie Mélard    *DENON Denis (180*)*                        Both coached and obsolete.                                     Check coachings
 Mélanie Mélard    *DENON Denis (180*)*                        Neither valid eId data nor alternative identifying document.   Check for valid identification
 Hubert Huppertz   *JEANÉMART Jérôme (181)*                    Neither valid eId data nor alternative identifying document.   Check for valid identification
                   *KASENNOVA Tatjana (221)*                   Neither valid eId data nor alternative identifying document.   Check for valid identification
                   *FRISCH Paul (238)*                         Neither valid eId data nor alternative identifying document.   Check for valid identification
                   *BRAUN Bruno (257)*                         Neither valid eId data nor alternative identifying document.   Check for valid identification
================= =========================================== ============================================================== ================================
<BLANKLINE>

The user can set the table parameters e.g. to see only problems of a
given type ("checker"):

>>> Checkers = rt.modules.plausibility.Checkers
>>> rt.show(plausibility.AllProblems,
...     param_values=dict(checker=Checkers.get_by_value(
...     'lino_welfare.modlib.dupable_clients.models.SimilarClientsChecker')))
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE -REPORT_UDIFF
================ =========================================== ========================================================== ===========================
 Responsible      Controlled by                               Message                                                    Plausibility checker
---------------- ------------------------------------------- ---------------------------------------------------------- ---------------------------
                  *DEMEULENAERE Dorothée (122)*               Similar clients: DOBBELSTEIN-DEMEULENAERE Dorothée (123)   Check for similar clients
 Mélanie Mélard   *DOBBELSTEIN-DEMEULENAERE Dorothée (123)*   Similar clients: DEMEULENAERE Dorothée (122)               Check for similar clients
 Mélanie Mélard   *DOBBELSTEIN Dorothée (124)*                Similar clients: DOBBELSTEIN-DEMEULENAERE Dorothée (123)   Check for similar clients
================ =========================================== ========================================================== ===========================
<BLANKLINE>


>>> rt.login('melanie').show(plausibility.MyProblems)
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
================ =========================================== ============================================================== ================================
 Responsible      Controlled by                               Message                                                        Plausibility checker
---------------- ------------------------------------------- -------------------------------------------------------------- --------------------------------
 Mélanie Mélard   *DOBBELSTEIN-DEMEULENAERE Dorothée (123)*   Similar clients: DEMEULENAERE Dorothée (122)                   Check for similar clients
 Mélanie Mélard   *DOBBELSTEIN Dorothée (124)*                Similar clients: DOBBELSTEIN-DEMEULENAERE Dorothée (123)       Check for similar clients
 Mélanie Mélard   *DOBBELSTEIN Dorothée (124)*                Neither valid eId data nor alternative identifying document.   Check for valid identification
 Mélanie Mélard   *EMONTS Daniel (128)*                       Neither valid eId data nor alternative identifying document.   Check for valid identification
 Mélanie Mélard   *ENGELS Edgar (129)*                        Neither valid eId data nor alternative identifying document.   Check for valid identification
 Mélanie Mélard   *FAYMONVILLE Luc (130*)*                    Both coached and obsolete.                                     Check coachings
 Mélanie Mélard   *FAYMONVILLE Luc (130*)*                    Neither valid eId data nor alternative identifying document.   Check for valid identification
 Mélanie Mélard   *HILGERS Hildegard (133)*                   Neither valid eId data nor alternative identifying document.   Check for valid identification
 Mélanie Mélard   *KAIVERS Karl (141)*                        Neither valid eId data nor alternative identifying document.   Check for valid identification
 Mélanie Mélard   *LAMBERTZ Guido (142)*                      Neither valid eId data nor alternative identifying document.   Check for valid identification
 Mélanie Mélard   *LAZARUS Line (144)*                        Neither valid eId data nor alternative identifying document.   Check for valid identification
 Mélanie Mélard   *MEESSEN Melissa (147)*                     Neither valid eId data nor alternative identifying document.   Check for valid identification
 Mélanie Mélard   *RADERMACHER Alfons (153)*                  Neither valid eId data nor alternative identifying document.   Check for valid identification
 Mélanie Mélard   *RADERMACHER Guido (159)*                   Neither valid eId data nor alternative identifying document.   Check for valid identification
 Mélanie Mélard   *RADERMECKER Rik (173)*                     Neither valid eId data nor alternative identifying document.   Check for valid identification
 Mélanie Mélard   *DENON Denis (180*)*                        Both coached and obsolete.                                     Check coachings
 Mélanie Mélard   *DENON Denis (180*)*                        Neither valid eId data nor alternative identifying document.   Check for valid identification
================ =========================================== ============================================================== ================================
<BLANKLINE>
