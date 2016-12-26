.. _welfare.specs.checkdata:
.. _welfare.tested.plausibility:

==========================================
Checking for data problems in Lino Welfare
==========================================

.. to test only this doc:

    $ python setup.py test -s tests.SpecsTests.test_checkdata

    >>> from lino import startup
    >>> startup('lino_welfare.projects.std.settings.doctests')
    >>> from lino.api.doctest import *

Lino Welfare offers some functionality for managing plausibility
problems.

See also :ref:`book.specs.checkdata`.


Data checkers available in Lino Welfare
=======================================

In the web interface you can select :menuselection:`Explorer -->
System --> Plausibility checkers` to see a table of all available
checkers.

.. 
    >>> show_menu_path(plausibility.Checkers)
    Explorer --> System --> Plausibility checkers
    
>>> rt.show(plausibility.Checkers)
======================================= ==================================================
 value                                   text
--------------------------------------- --------------------------------------------------
 printing.CachedPrintableChecker         Check for missing target files
 countries.PlaceChecker                  Check plausibility of geographical places.
 addresses.AddressOwnerChecker           Check for missing or non-primary address records
 cal.EventGuestChecker                   Events without participants
 cal.ConflictingEventsChecker            Check for conflicting events
 cal.ObsoleteEventTypeChecker            Obsolete event type of generated events
 cal.LongEventChecker                    Too long-lasting events
 mixins.DupableChecker                   Check for missing phonetic words
 beid.BeIdCardHolderChecker              Check for invalid SSINs
 pcsw.SSINChecker                        Check for valid identification
 pcsw.ClientCoachingsChecker             Check coachings
 isip.OverlappingContractsChecker        Check for overlapping contracts
 ledger.VoucherChecker                   Check integrity of ledger movements
 sepa.BankAccountChecker                 Check for partner mismatches in bank accounts
 dupable_clients.SimilarClientsChecker   Check for similar clients
======================================= ==================================================
<BLANKLINE>



Showing all problems
====================
The demo database deliberately contains some data problems.
In the web interface you can select :menuselection:`Explorer -->
System --> Plausibility problems` to see them.

..
    >>> show_menu_path(plausibility.AllProblems)
    Explorer --> System --> Plausibility problems


>>> rt.show(plausibility.AllProblems)
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
================= ============================================================= ========================================================================== ================================
 Responsible       Controlled by                                                 Message                                                                    Plausibility checker
----------------- ------------------------------------------------------------- -------------------------------------------------------------------------- --------------------------------
 Robin Rood        *Calendar entry #66 Ascension of Jesus (29.05.2014)*          Event conflicts with 8 other events.                                       Check for conflicting events
 Alicia Allmanns   *Calendar entry #484 Souper (29.05.2014 08:30)*               Event conflicts with Calendar entry #66 Ascension of Jesus (29.05.2014).   Check for conflicting events
 Hubert Huppertz   *Calendar entry #496 Consultation (29.05.2014 10:20)*         Event conflicts with Calendar entry #66 Ascension of Jesus (29.05.2014).   Check for conflicting events
 Judith Jousten    *Calendar entry #508 First meeting (29.05.2014 13:30)*        Event conflicts with Calendar entry #66 Ascension of Jesus (29.05.2014).   Check for conflicting events
 Mélanie Mélard    *Calendar entry #520 Souper (29.05.2014 09:40)*               Event conflicts with Calendar entry #66 Ascension of Jesus (29.05.2014).   Check for conflicting events
 Romain Raffault   *Calendar entry #544 Première rencontre (29.05.2014 08:30)*   Event conflicts with Calendar entry #66 Ascension of Jesus (29.05.2014).   Check for conflicting events
 Rolf Rompen       *Calendar entry #556 Abendessen (29.05.2014 10:20)*           Event conflicts with Calendar entry #66 Ascension of Jesus (29.05.2014).   Check for conflicting events
 Robin Rood        *Calendar entry #568 Consultation (29.05.2014 13:30)*         Event conflicts with Calendar entry #66 Ascension of Jesus (29.05.2014).   Check for conflicting events
 Theresia Thelen   *Calendar entry #580 First meeting (29.05.2014 09:40)*        Event conflicts with Calendar entry #66 Ascension of Jesus (29.05.2014).   Check for conflicting events
 Caroline Carnol   *AUSDEMWALD Alfons (116)*                                     Neither valid eId data nor alternative identifying document.               Check for valid identification
                   *BASTIAENSEN Laurent (117)*                                   Neither valid eId data nor alternative identifying document.               Check for valid identification
 Hubert Huppertz   *COLLARD Charlotte (118)*                                     Neither valid eId data nor alternative identifying document.               Check for valid identification
                   *CHANTRAINE Marc (120*)*                                      Neither valid eId data nor alternative identifying document.               Check for valid identification
                   *DEMEULENAERE Dorothée (122)*                                 Similar clients: DOBBELSTEIN-DEMEULENAERE Dorothée (123)                   Check for similar clients
                   *DEMEULENAERE Dorothée (122)*                                 Neither valid eId data nor alternative identifying document.               Check for valid identification
 Mélanie Mélard    *DOBBELSTEIN-DEMEULENAERE Dorothée (123)*                     Similar clients: DEMEULENAERE Dorothée (122)                               Check for similar clients
 Mélanie Mélard    *DOBBELSTEIN Dorothée (124)*                                  Similar clients: DOBBELSTEIN-DEMEULENAERE Dorothée (123)                   Check for similar clients
 Mélanie Mélard    *DOBBELSTEIN Dorothée (124)*                                  Neither valid eId data nor alternative identifying document.               Check for valid identification
                   *ERNST Berta (125)*                                           Neither valid eId data nor alternative identifying document.               Check for valid identification
 Alicia Allmanns   *EVERS Eberhart (127)*                                        Neither valid eId data nor alternative identifying document.               Check for valid identification
 Mélanie Mélard    *EMONTS Daniel (128)*                                         Neither valid eId data nor alternative identifying document.               Check for valid identification
 Mélanie Mélard    *ENGELS Edgar (129)*                                          Neither valid eId data nor alternative identifying document.               Check for valid identification
 Mélanie Mélard    *FAYMONVILLE Luc (130*)*                                      Both coached and obsolete.                                                 Check coachings
 Mélanie Mélard    *FAYMONVILLE Luc (130*)*                                      Neither valid eId data nor alternative identifying document.               Check for valid identification
                   *GERNEGROß Germaine (131)*                                    Neither valid eId data nor alternative identifying document.               Check for valid identification
 Alicia Allmanns   *GROTECLAES Gregory (132)*                                    Neither valid eId data nor alternative identifying document.               Check for valid identification
 Mélanie Mélard    *HILGERS Hildegard (133)*                                     Neither valid eId data nor alternative identifying document.               Check for valid identification
                   *HILGERS Henri (134)*                                         Neither valid eId data nor alternative identifying document.               Check for valid identification
                   *INGELS Irene (135)*                                          Neither valid eId data nor alternative identifying document.               Check for valid identification
                   *JANSEN Jérémy (136)*                                         Neither valid eId data nor alternative identifying document.               Check for valid identification
 Caroline Carnol   *JACOBS Jacqueline (137)*                                     Neither valid eId data nor alternative identifying document.               Check for valid identification
 Hubert Huppertz   *JONAS Josef (139)*                                           Neither valid eId data nor alternative identifying document.               Check for valid identification
                   *JOUSTEN Jan (140*)*                                          Neither valid eId data nor alternative identifying document.               Check for valid identification
 Mélanie Mélard    *KAIVERS Karl (141)*                                          Neither valid eId data nor alternative identifying document.               Check for valid identification
 Mélanie Mélard    *LAMBERTZ Guido (142)*                                        Neither valid eId data nor alternative identifying document.               Check for valid identification
                   *LASCHET Laura (143)*                                         Neither valid eId data nor alternative identifying document.               Check for valid identification
 Mélanie Mélard    *LAZARUS Line (144)*                                          Neither valid eId data nor alternative identifying document.               Check for valid identification
 Hubert Huppertz   *MALMENDIER Marc (146)*                                       Neither valid eId data nor alternative identifying document.               Check for valid identification
 Mélanie Mélard    *MEESSEN Melissa (147)*                                       Neither valid eId data nor alternative identifying document.               Check for valid identification
                   *MEIER Marie-Louise (149)*                                    Neither valid eId data nor alternative identifying document.               Check for valid identification
                   *EMONTS Erich (150*)*                                         Neither valid eId data nor alternative identifying document.               Check for valid identification
                   *EMONTSPOOL Erwin (151)*                                      Neither valid eId data nor alternative identifying document.               Check for valid identification
 Hubert Huppertz   *EMONTS-GAST Erna (152)*                                      Neither valid eId data nor alternative identifying document.               Check for valid identification
 Mélanie Mélard    *RADERMACHER Alfons (153)*                                    Neither valid eId data nor alternative identifying document.               Check for valid identification
                   *RADERMACHER Berta (154)*                                     Neither valid eId data nor alternative identifying document.               Check for valid identification
 Alicia Allmanns   *RADERMACHER Christian (155)*                                 Neither valid eId data nor alternative identifying document.               Check for valid identification
                   *RADERMACHER Daniela (156)*                                   Neither valid eId data nor alternative identifying document.               Check for valid identification
 Caroline Carnol   *RADERMACHER Edgard (157)*                                    Neither valid eId data nor alternative identifying document.               Check for valid identification
 Mélanie Mélard    *RADERMACHER Guido (159)*                                     Neither valid eId data nor alternative identifying document.               Check for valid identification
                   *RADERMACHER Hans (160*)*                                     Neither valid eId data nor alternative identifying document.               Check for valid identification
 Caroline Carnol   *RADERMACHER Hedi (161)*                                      Neither valid eId data nor alternative identifying document.               Check for valid identification
                   *RADERMACHER Inge (162)*                                      Neither valid eId data nor alternative identifying document.               Check for valid identification
                   *DI RUPO Didier (164)*                                        Neither valid eId data nor alternative identifying document.               Check for valid identification
 Hubert Huppertz   *DA VINCI David (165)*                                        Neither valid eId data nor alternative identifying document.               Check for valid identification
 Hubert Huppertz   *VAN VEEN Vincent (166)*                                      Neither valid eId data nor alternative identifying document.               Check for valid identification
 Hubert Huppertz   *ÖSTGES Otto (168)*                                           Neither valid eId data nor alternative identifying document.               Check for valid identification
                   *MARTELAER Mark (172)*                                        Neither valid eId data nor alternative identifying document.               Check for valid identification
 Mélanie Mélard    *RADERMECKER Rik (173)*                                       Neither valid eId data nor alternative identifying document.               Check for valid identification
                   *VANDENMEULENBOS Marie-Louise (174)*                          Neither valid eId data nor alternative identifying document.               Check for valid identification
                   *EIERSCHAL Emil (175)*                                        Neither valid eId data nor alternative identifying document.               Check for valid identification
                   *LAHM Lisa (176)*                                             Neither valid eId data nor alternative identifying document.               Check for valid identification
 Hubert Huppertz   *KELLER Karl (178)*                                           Neither valid eId data nor alternative identifying document.               Check for valid identification
 Hubert Huppertz   *DUBOIS Robin (179)*                                          Neither valid eId data nor alternative identifying document.               Check for valid identification
 Mélanie Mélard    *DENON Denis (180*)*                                          Both coached and obsolete.                                                 Check coachings
 Mélanie Mélard    *DENON Denis (180*)*                                          Neither valid eId data nor alternative identifying document.               Check for valid identification
 Hubert Huppertz   *JEANÉMART Jérôme (181)*                                      Neither valid eId data nor alternative identifying document.               Check for valid identification
                   *KASENNOVA Tatjana (213)*                                     Neither valid eId data nor alternative identifying document.               Check for valid identification
                   *FRISCH Paul (240)*                                           Neither valid eId data nor alternative identifying document.               Check for valid identification
                   *BRAUN Bruno (259)*                                           Neither valid eId data nor alternative identifying document.               Check for valid identification
================= ============================================================= ========================================================================== ================================
<BLANKLINE>


Filtering data problems
=======================

The user can set the table parameters e.g. to see only problems of a
given type ("checker"). The following snippet simulates the situation
of selecting the :class:`SimilarClientsChecker
<lino_welfare.modlib.dupable_clients.models.SimilarClientsChecker>`.

>>> Checkers = rt.modules.plausibility.Checkers
>>> rt.show(plausibility.AllProblems,
...     param_values=dict(checker=Checkers.get_by_value(
...     'dupable_clients.SimilarClientsChecker')))
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE -REPORT_UDIFF
================ =========================================== ========================================================== ===========================
 Responsible      Controlled by                               Message                                                    Plausibility checker
---------------- ------------------------------------------- ---------------------------------------------------------- ---------------------------
                  *DEMEULENAERE Dorothée (122)*               Similar clients: DOBBELSTEIN-DEMEULENAERE Dorothée (123)   Check for similar clients
 Mélanie Mélard   *DOBBELSTEIN-DEMEULENAERE Dorothée (123)*   Similar clients: DEMEULENAERE Dorothée (122)               Check for similar clients
 Mélanie Mélard   *DOBBELSTEIN Dorothée (124)*                Similar clients: DOBBELSTEIN-DEMEULENAERE Dorothée (123)   Check for similar clients
================ =========================================== ========================================================== ===========================
<BLANKLINE>


My problems
===========

In the web interface you can select :menuselection:`Office -->
Plausibility problems assigned to me` to see a list of all problems
assigned to you.

..
    >>> show_menu_path(plausibility.MyProblems)
    Office --> Plausibility problems assigned to me

>>> rt.login('melanie').show(plausibility.MyProblems)
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
================ ============================================================ ========================================================================== ================================
 Responsible      Controlled by                                                Message                                                                    Plausibility checker
---------------- ------------------------------------------------------------ -------------------------------------------------------------------------- --------------------------------
 Mélanie Mélard   `Calendar entry #520 Souper (29.05.2014 09:40) <Detail>`__   Event conflicts with Calendar entry #66 Ascension of Jesus (29.05.2014).   Check for conflicting events
 Mélanie Mélard   `DOBBELSTEIN-DEMEULENAERE Dorothée (123) <Detail>`__         Similar clients: DEMEULENAERE Dorothée (122)                               Check for similar clients
 Mélanie Mélard   `DOBBELSTEIN Dorothée (124) <Detail>`__                      Similar clients: DOBBELSTEIN-DEMEULENAERE Dorothée (123)                   Check for similar clients
 Mélanie Mélard   `DOBBELSTEIN Dorothée (124) <Detail>`__                      Neither valid eId data nor alternative identifying document.               Check for valid identification
 Mélanie Mélard   `EMONTS Daniel (128) <Detail>`__                             Neither valid eId data nor alternative identifying document.               Check for valid identification
 Mélanie Mélard   `ENGELS Edgar (129) <Detail>`__                              Neither valid eId data nor alternative identifying document.               Check for valid identification
 Mélanie Mélard   `FAYMONVILLE Luc (130*) <Detail>`__                          Both coached and obsolete.                                                 Check coachings
 Mélanie Mélard   `FAYMONVILLE Luc (130*) <Detail>`__                          Neither valid eId data nor alternative identifying document.               Check for valid identification
 Mélanie Mélard   `HILGERS Hildegard (133) <Detail>`__                         Neither valid eId data nor alternative identifying document.               Check for valid identification
 Mélanie Mélard   `KAIVERS Karl (141) <Detail>`__                              Neither valid eId data nor alternative identifying document.               Check for valid identification
 Mélanie Mélard   `LAMBERTZ Guido (142) <Detail>`__                            Neither valid eId data nor alternative identifying document.               Check for valid identification
 Mélanie Mélard   `LAZARUS Line (144) <Detail>`__                              Neither valid eId data nor alternative identifying document.               Check for valid identification
 Mélanie Mélard   `MEESSEN Melissa (147) <Detail>`__                           Neither valid eId data nor alternative identifying document.               Check for valid identification
 Mélanie Mélard   `RADERMACHER Alfons (153) <Detail>`__                        Neither valid eId data nor alternative identifying document.               Check for valid identification
 Mélanie Mélard   `RADERMACHER Guido (159) <Detail>`__                         Neither valid eId data nor alternative identifying document.               Check for valid identification
 Mélanie Mélard   `RADERMECKER Rik (173) <Detail>`__                           Neither valid eId data nor alternative identifying document.               Check for valid identification
 Mélanie Mélard   `DENON Denis (180*) <Detail>`__                              Both coached and obsolete.                                                 Check coachings
 Mélanie Mélard   `DENON Denis (180*) <Detail>`__                              Neither valid eId data nor alternative identifying document.               Check for valid identification
================ ============================================================ ========================================================================== ================================
<BLANKLINE>
