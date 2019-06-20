.. doctest docs/specs/checkdata.rst
.. _welfare.specs.checkdata:

==========================================
Checking for data problems in Lino Welfare
==========================================

..  doctest init:
   
    >>> from lino import startup
    >>> startup('lino_welfare.projects.gerd.settings.doctests')
    >>> from lino.api.doctest import *

Lino Welfare offers some functionality for managing data
problems.

See also :ref:`book.specs.checkdata`.


..  preliminary:
   
    >>> cal.Event.get_default_table()
    lino_xl.lib.cal.ui.OneEvent


Data checkers available in Lino Welfare
=======================================

In the web interface you can select :menuselection:`Explorer -->
System --> Data checkers` to see a table of all available
checkers.

.. 
    >>> show_menu_path(checkdata.Checkers, language="en")
    Explorer --> System --> Data checkers
    
>>> rt.show(checkdata.Checkers, language="en")
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
======================================= ===================================================
 value                                   text
--------------------------------------- ---------------------------------------------------
 addresses.AddressOwnerChecker           Check for missing or non-primary address records
 aids.ConfirmationChecker                Check for confirmations outside of granted period
 beid.SSINChecker                        Check for invalid SSINs
 cal.ConflictingEventsChecker            Check for conflicting calendar entries
 cal.EventGuestChecker                   Entries without participants
 cal.LongEntryChecker                    Too long-lasting calendar entries
 cal.ObsoleteEventTypeChecker            Obsolete generated calendar entries
 coachings.ClientCoachingsChecker        Check coachings
 countries.PlaceChecker                  Check data of geographical places.
 dupable_clients.SimilarClientsChecker   Check for similar clients
 finan.FinancialVoucherItemChecker       Check for invalid account/partner combination
 isip.OverlappingContractsChecker        Check for overlapping contracts
 ledger.VoucherChecker                   Check integrity of ledger vouchers
 mixins.DupableChecker                   Check for missing phonetic words
 pcsw.IdentityChecker                    Check for valid identification
 printing.CachedPrintableChecker         Check for missing target files
 sepa.BankAccountChecker                 Check for partner mismatches in bank accounts
======================================= ===================================================
<BLANKLINE>



Showing all problems
====================

The demo database deliberately contains some data problems.  In the
web interface you can select :menuselection:`Explorer --> System -->
Data problems` to see them.  Note that messages are in the language of
the responsible user.

..
    >>> show_menu_path(checkdata.AllProblems, language="en")
    Explorer --> System --> Data problems


>>> rt.show(checkdata.AllProblems, language="en")
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
================== ========================================================== ========================================================== ========================================
 Responsible        Database object                                            Message                                                    Checker
------------------ ---------------------------------------------------------- ---------------------------------------------------------- ----------------------------------------
 Robin Rood         *Christi Himmelfahrt (29.05.2014)*                         Event conflicts with 4 other events.                       Check for conflicting calendar entries
 Robin Rood         *Pfingsten (09.06.2014)*                                   Event conflicts with 2 other events.                       Check for conflicting calendar entries
 Patrick Paraneau   *Beratung (29.05.2014 08:30) with INGELS Irene (135)*      Event conflicts with Christi Himmelfahrt (29.05.2014).     Check for conflicting calendar entries
 Judith Jousten     *Frühstück (09.06.2014 09:40) with KAIVERS Karl (141)*     Event conflicts with Pfingsten (09.06.2014).               Check for conflicting calendar entries
 Mélanie Mélard     *Rencontre (09.06.2014 10:20) with LAMBERTZ Guido (142)*   Event conflicts with Pfingsten (09.06.2014).               Check for conflicting calendar entries
 Romain Raffault    *Absent for private reasons (29.05.2014)*                  Event conflicts with Christi Himmelfahrt (29.05.2014).     Check for conflicting calendar entries
 Caroline Carnol    *AUSDEMWALD Alfons (116)*                                  Weder gültige eID-Daten noch identifizierendes Dokument.   Check for valid identification
                    *BASTIAENSEN Laurent (117)*                                Weder gültige eID-Daten noch identifizierendes Dokument.   Check for valid identification
                    *CHANTRAINE Marc (120*)*                                   Weder gültige eID-Daten noch identifizierendes Dokument.   Check for valid identification
                    *DEMEULENAERE Dorothée (122)*                              Similar clients: DOBBELSTEIN-DEMEULENAERE Dorothée (123)   Check for similar clients
                    *DEMEULENAERE Dorothée (122)*                              Weder gültige eID-Daten noch identifizierendes Dokument.   Check for valid identification
 Hubert Huppertz    *DOBBELSTEIN-DEMEULENAERE Dorothée (123)*                  Similar clients: DEMEULENAERE Dorothée (122)               Check for similar clients
 Mélanie Mélard     *DOBBELSTEIN Dorothée (124)*                               Similar clients: DOBBELSTEIN-DEMEULENAERE Dorothée (123)   Check for similar clients
 ...
 Caroline Carnol    *DENON Denis (180*)*                                       Begleitet und veraltet zugleich.                           Check coachings
 Caroline Carnol    *DENON Denis (180*)*                                       Weder gültige eID-Daten noch identifizierendes Dokument.   Check for valid identification
 Hubert Huppertz    *JEANÉMART Jérôme (181)*                                   Weder gültige eID-Daten noch identifizierendes Dokument.   Check for valid identification
                    *KASENNOVA Tatjana (213)*                                  Weder gültige eID-Daten noch identifizierendes Dokument.   Check for valid identification
                    *FRISCH Paul (240)*                                        Weder gültige eID-Daten noch identifizierendes Dokument.   Check for valid identification
                    *BRAUN Bruno (259)*                                        Weder gültige eID-Daten noch identifizierendes Dokument.   Check for valid identification
================== ========================================================== ========================================================== ========================================
<BLANKLINE>




Filtering data problems
=======================

The user can set the table parameters e.g. to see only problems of a
given type ("checker"). The following snippet simulates the situation
of selecting the :class:`SimilarClientsChecker
<lino_welfare.modlib.dupable_clients.models.SimilarClientsChecker>`.

>>> Checkers = rt.models.checkdata.Checkers
>>> rt.show(checkdata.AllProblems, language="en",
...     param_values=dict(checker=Checkers.get_by_value(
...     'dupable_clients.SimilarClientsChecker')))
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE -REPORT_UDIFF
================= =========================================== ========================================================== ===========================
 Responsible       Database object                             Message                                                    Checker
----------------- ------------------------------------------- ---------------------------------------------------------- ---------------------------
                   *DEMEULENAERE Dorothée (122)*               Similar clients: DOBBELSTEIN-DEMEULENAERE Dorothée (123)   Check for similar clients
 Hubert Huppertz   *DOBBELSTEIN-DEMEULENAERE Dorothée (123)*   Similar clients: DEMEULENAERE Dorothée (122)               Check for similar clients
 Mélanie Mélard    *DOBBELSTEIN Dorothée (124)*                Similar clients: DOBBELSTEIN-DEMEULENAERE Dorothée (123)   Check for similar clients
================= =========================================== ========================================================== ===========================
<BLANKLINE>


My problems
===========

In the web interface you can select :menuselection:`Office -->
Data problems assigned to me` to see a list of all problems
assigned to you.

..
    >>> show_menu_path(checkdata.MyProblems, language="en")
    Office --> Data problems assigned to me

>>> print(rt.login('melanie').user.language)
fr
>>> rt.login('melanie').show(checkdata.MyProblems, language="en")
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
================ ===================================================================== ========================================================== ========================================
 Responsible      Database object                                                       Message                                                    Checker
---------------- --------------------------------------------------------------------- ---------------------------------------------------------- ----------------------------------------
 Mélanie Mélard   `Rencontre (09.06.2014 10:20) with LAMBERTZ Guido (142) <Detail>`__   Event conflicts with Pfingsten (09.06.2014).               Check for conflicting calendar entries
 Mélanie Mélard   `DOBBELSTEIN Dorothée (124) <Detail>`__                               Similar clients: DOBBELSTEIN-DEMEULENAERE Dorothée (123)   Check for similar clients
 Mélanie Mélard   `DOBBELSTEIN Dorothée (124) <Detail>`__                               Sans données eID ou document identifiant alternatif.       Check for valid identification
 Mélanie Mélard   `ENGELS Edgar (129) <Detail>`__                                       Sans données eID ou document identifiant alternatif.       Check for valid identification
 Mélanie Mélard   `GROTECLAES Gregory (132) <Detail>`__                                 Sans données eID ou document identifiant alternatif.       Check for valid identification
 Mélanie Mélard   `KAIVERS Karl (141) <Detail>`__                                       Sans données eID ou document identifiant alternatif.       Check for valid identification
 Mélanie Mélard   `LAZARUS Line (144) <Detail>`__                                       Sans données eID ou document identifiant alternatif.       Check for valid identification
 Mélanie Mélard   `MEESSEN Melissa (147) <Detail>`__                                    Sans données eID ou document identifiant alternatif.       Check for valid identification
 Mélanie Mélard   `RADERMACHER Alfons (153) <Detail>`__                                 Sans données eID ou document identifiant alternatif.       Check for valid identification
 Mélanie Mélard   `RADERMACHER Guido (159) <Detail>`__                                  Sans données eID ou document identifiant alternatif.       Check for valid identification
 Mélanie Mélard   `KELLER Karl (178) <Detail>`__                                        Sans données eID ou document identifiant alternatif.       Check for valid identification
================ ===================================================================== ========================================================== ========================================
<BLANKLINE>

