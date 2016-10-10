.. _welfare.tested.cal:
.. _welfare.specs.cal:

========
Calendar
========

.. How to test only this document:

    $ python setup.py test -s tests.SpecsTests.test_cal
    
    doctest init:

    >>> from lino import startup
    >>> startup('lino_welfare.projects.eupen.settings.doctests')
    >>> from lino.api.doctest import *

A technical tour into the :mod:`lino_welfare.modlib.cal` module.

.. contents::
   :local:


Not for everybody
=================

Only users with the :class:`OfficeUser
<lino.modlib.office.roles.OfficeUser>` role can see the calendar
functionality.  All users with one of the following profiles can see
each other's calendars:

>>> from lino.modlib.office.roles import OfficeUser
>>> for p in users.UserProfiles.items():
...     if isinstance(p.role, OfficeUser):
...         print repr(p), unicode(p)
... #doctest: +NORMALIZE_WHITESPACE +REPORT_UDIFF
users.UserProfiles:100 Begleiter im DSBE
users.UserProfiles:110 Begleiter im DSBE (Manager)
users.UserProfiles:120 Begleiter im DSBE (+Erstempfang)
users.UserProfiles:200 Berater Erstempfang
users.UserProfiles:300 Schuldenberater
users.UserProfiles:400 Sozi
users.UserProfiles:410 Sozi (Manager)
users.UserProfiles:500 Buchhalter
users.UserProfiles:510 Accountant (Manager)
users.UserProfiles.admin:900 Verwalter
users.UserProfiles:910 Security advisor




Events today
============

Here is what the :class:`lino.modlib.cal.ui.EventsByDay` table gives:

>>> rt.login('theresia').show(cal.EventsByDay, language='en', header_level=1)
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
===========================
Thu 22/05/2014 (22.05.2014)
===========================
============ ============================ ============= ================== ============= ======================= ====== ============================
 Start time   Client                       Summary       Managed by         Assigned to   Calendar Event Type     Room   Workflow
------------ ---------------------------- ------------- ------------------ ------------- ----------------------- ------ ----------------------------
 08:30:00                                  Diner         Alicia Allmanns                  Meeting                        **Suggested**
 08:30:00     MEIER Marie-Louise (149)     Evaluation    Romain Raffault                  Informational meeting          **Suggested**
 09:40:00     JANSEN Jérémy (136)          Diner         Mélanie Mélard                   Informational meeting          **Suggested**
 09:40:00                                  Auswertung    Theresia Thelen                  Meeting                        **Suggested** → [Notified]
 10:20:00     DOBBELSTEIN Dorothée (124)   Treffen       Hubert Huppertz                  Informational meeting          **Suggested**
 10:20:00                                  Mittagessen   Rolf Rompen                      Meeting                        **Suggested**
 11:10:00                                  Treffen       Patrick Paraneau                 Meeting                        **Suggested**
 13:30:00                                  Auswertung    Judith Jousten                   Meeting                        **Suggested**
 13:30:00     RADERMACHER Hedi (161)       Meeting       Robin Rood                       Informational meeting          **Suggested**
============ ============================ ============= ================== ============= ======================= ====== ============================
<BLANKLINE>


.. until 20160814 Note how Theresia cannot [Take] her own event
   (because she has it already), and how she can set only her own
   event to [Notified].

Note how Theresia can set only her own event to [Notified].

Users looking at their events
=============================

The **My events** table (:class:`lino_xl.lib.cal.ui.MyEvents`) shows
shows today's and all future appointments :attr:`show_appointments
<lino_xl.lib.cal.ui.Events.show_appointments>` of the user who
requests it.

Here is what it says for Alicia.

>>> rt.login('alicia').show(cal.MyEvents, language='en')
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE -REPORT_UDIFF
====================================== ========================================= ======================= ==================== =================================
 When                                   Client                                    Calendar Event Type     Summary              Workflow
-------------------------------------- ----------------------------------------- ----------------------- -------------------- ---------------------------------
 `Thu 22/05/2014 at 08:30 <Detail>`__                                             Meeting                 Diner                **Suggested** → [Notified]
 `Fri 23/05/2014 at 09:40 <Detail>`__   AUSDEMWALD Alfons (116)                   Appointment             Souper               **Draft** → [Notified] [Cancel]
 `Sat 24/05/2014 at 10:20 <Detail>`__   BASTIAENSEN Laurent (117)                 Evaluation              Petit-déjeuner       **Took place** → [Reset]
 `Sat 24/05/2014 at 11:10 <Detail>`__   COLLARD Charlotte (118)                   External meeting        Rencontre            **Cancelled**
 `Sun 25/05/2014 at 13:30 <Detail>`__   CHANTRAINE Marc (120*)                    Informational meeting   Consultation         **Omitted**
 `Mon 26/05/2014 at 08:30 <Detail>`__                                             Internal meeting        Séminaire            **Notified** → [Cancel] [Reset]
 `Mon 26/05/2014 at 09:40 <Detail>`__                                             External meeting        Evaluation           **Suggested** → [Notified]
 `Tue 27/05/2014 at 10:20 <Detail>`__                                             Private                 Première rencontre   **Draft** → [Notified] [Cancel]
 `Wed 28/05/2014 at 11:10 <Detail>`__                                             Meeting                 Interview            **Took place** → [Reset]
 `Wed 28/05/2014 at 13:30 <Detail>`__   DERICUM Daniel (121)                      Appointment             Diner                **Cancelled**
 `Thu 29/05/2014 at 08:30 <Detail>`__   DEMEULENAERE Dorothée (122)               Evaluation              Souper               **Omitted**
 `Fri 30/05/2014 at 09:40 <Detail>`__   DOBBELSTEIN-DEMEULENAERE Dorothée (123)   External meeting        Petit-déjeuner       **Notified** → [Cancel] [Reset]
 `Mon 23/06/2014 at 09:00 <Detail>`__   DA VINCI David (165)                      Evaluation              Évaluation 1         [▽] **Suggested** → [Notified]
 `Mon 14/07/2014 <Detail>`__            RADERMACHER Fritz (158)                   Evaluation              Évaluation 6         [▽] **Suggested** → [Notified]
 `Wed 23/07/2014 at 09:00 <Detail>`__   DA VINCI David (165)                      Evaluation              Évaluation 2         [▽] **Suggested** → [Notified]
 `Thu 14/08/2014 <Detail>`__            HILGERS Hildegard (133)                   Evaluation              Évaluation 7         [▽] **Suggested** → [Notified]
 `Mon 25/08/2014 at 09:00 <Detail>`__   DA VINCI David (165)                      Evaluation              Évaluation 3         [▽] **Suggested** → [Notified]
 `Thu 25/09/2014 at 09:00 <Detail>`__   DA VINCI David (165)                      Evaluation              Évaluation 4         [▽] **Suggested** → [Notified]
 `Tue 14/10/2014 <Detail>`__            RADERMACHER Fritz (158)                   Evaluation              Évaluation 7         [▽] **Suggested** → [Notified]
 `Mon 27/10/2014 at 09:00 <Detail>`__   DA VINCI David (165)                      Evaluation              Évaluation 5         [▽] **Suggested** → [Notified]
 `Thu 27/11/2014 at 09:00 <Detail>`__   DA VINCI David (165)                      Evaluation              Évaluation 6         [▽] **Suggested** → [Notified]
 `Mon 29/12/2014 at 09:00 <Detail>`__   DA VINCI David (165)                      Evaluation              Évaluation 7         [▽] **Suggested** → [Notified]
 `Thu 29/01/2015 at 09:00 <Detail>`__   DA VINCI David (165)                      Evaluation              Évaluation 8         [▽] **Suggested** → [Notified]
 `Mon 02/03/2015 at 09:00 <Detail>`__   DA VINCI David (165)                      Evaluation              Évaluation 9         [▽] **Suggested** → [Notified]
====================================== ========================================= ======================= ==================== =================================
<BLANKLINE>



These are for Hubert:

>>> rt.login('hubert').show(cal.MyEvents, language='en')
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE -REPORT_UDIFF
====================================== ============================ ======================= =============== =================================
 When                                   Client                       Calendar Event Type     Summary         Workflow
-------------------------------------- ---------------------------- ----------------------- --------------- ---------------------------------
 `Thu 22/05/2014 at 10:20 <Detail>`__   DOBBELSTEIN Dorothée (124)   Informational meeting   Treffen         **Suggested** → [Notified]
 `Fri 23/05/2014 at 11:10 <Detail>`__                                Internal meeting        Beratung        **Draft** → [Notified] [Cancel]
 `Sat 24/05/2014 at 08:30 <Detail>`__                                Private                 Auswertung      **Cancelled**
 `Sat 24/05/2014 at 13:30 <Detail>`__                                External meeting        Seminar         **Took place** → [Reset]
 `Sun 25/05/2014 at 09:40 <Detail>`__                                Meeting                 Erstgespräch    **Omitted**
 `Mon 26/05/2014 at 10:20 <Detail>`__   ERNST Berta (125)            Appointment             Interview       **Notified** → [Cancel] [Reset]
 `Mon 26/05/2014 at 11:10 <Detail>`__   EVERTZ Bernd (126)           Evaluation              Mittagessen     **Suggested** → [Notified]
 `Tue 27/05/2014 at 13:30 <Detail>`__   EVERS Eberhart (127)         External meeting        Abendessen      **Draft** → [Notified] [Cancel]
 `Wed 28/05/2014 at 08:30 <Detail>`__   EMONTS Daniel (128)          Informational meeting   Frühstück       **Took place** → [Reset]
 `Wed 28/05/2014 at 09:00 <Detail>`__   BRECHT Bernd (177)           Evaluation              Évaluation 15   [▽] **Suggested** → [Notified]
 `Wed 28/05/2014 at 09:40 <Detail>`__                                Internal meeting        Treffen         **Cancelled**
 `Thu 29/05/2014 at 10:20 <Detail>`__                                External meeting        Beratung        **Omitted**
 `Fri 30/05/2014 at 11:10 <Detail>`__                                Private                 Seminar         **Notified** → [Cancel] [Reset]
 `Tue 03/06/2014 <Detail>`__            DENON Denis (180*)           Evaluation              Auswertung 1    [▽] **Suggested** → [Notified]
 `Wed 04/06/2014 <Detail>`__            LAMBERTZ Guido (142)         Evaluation              Évaluation 6    [▽] **Suggested** → [Notified]
 `Thu 19/06/2014 at 09:00 <Detail>`__   JEANÉMART Jérôme (181)       Evaluation              Évaluation 15   [▽] **Suggested** → [Notified]
 `Mon 14/07/2014 at 09:00 <Detail>`__   BRECHT Bernd (177)           Evaluation              Auswertung 1    [▽] **Suggested** → [Notified]
 `Mon 04/08/2014 at 09:00 <Detail>`__   JEANÉMART Jérôme (181)       Evaluation              Auswertung 1    [▽] **Suggested** → [Notified]
 `Tue 05/08/2014 <Detail>`__            FAYMONVILLE Luc (130*)       Evaluation              Auswertung 3    [▽] **Suggested** → [Notified]
 `Tue 12/08/2014 <Detail>`__            RADERMECKER Rik (173)        Evaluation              Auswertung 2    [▽] **Suggested** → [Notified]
 `Thu 14/08/2014 at 09:00 <Detail>`__   BRECHT Bernd (177)           Evaluation              Auswertung 2    [▽] **Suggested** → [Notified]
 `Wed 03/09/2014 <Detail>`__            DENON Denis (180*)           Evaluation              Auswertung 2    [▽] **Suggested** → [Notified]
 `Thu 04/09/2014 <Detail>`__            LAMBERTZ Guido (142)         Evaluation              Évaluation 7    [▽] **Suggested** → [Notified]
 `Thu 04/09/2014 at 09:00 <Detail>`__   JEANÉMART Jérôme (181)       Evaluation              Auswertung 2    [▽] **Suggested** → [Notified]
 `Mon 15/09/2014 at 09:00 <Detail>`__   BRECHT Bernd (177)           Evaluation              Auswertung 3    [▽] **Suggested** → [Notified]
 `Mon 06/10/2014 at 09:00 <Detail>`__   JEANÉMART Jérôme (181)       Evaluation              Auswertung 3    [▽] **Suggested** → [Notified]
 `Wed 15/10/2014 at 09:00 <Detail>`__   BRECHT Bernd (177)           Evaluation              Auswertung 4    [▽] **Suggested** → [Notified]
 `Thu 06/11/2014 at 09:00 <Detail>`__   JEANÉMART Jérôme (181)       Evaluation              Auswertung 4    [▽] **Suggested** → [Notified]
 `Wed 12/11/2014 <Detail>`__            RADERMECKER Rik (173)        Evaluation              Auswertung 3    [▽] **Suggested** → [Notified]
 `Mon 17/11/2014 at 09:00 <Detail>`__   BRECHT Bernd (177)           Evaluation              Auswertung 5    [▽] **Suggested** → [Notified]
 `Wed 03/12/2014 <Detail>`__            DENON Denis (180*)           Evaluation              Auswertung 3    [▽] **Suggested** → [Notified]
 `Mon 08/12/2014 at 09:00 <Detail>`__   JEANÉMART Jérôme (181)       Evaluation              Auswertung 5    [▽] **Suggested** → [Notified]
 `Wed 17/12/2014 at 09:00 <Detail>`__   BRECHT Bernd (177)           Evaluation              Auswertung 6    [▽] **Suggested** → [Notified]
 `Thu 08/01/2015 at 09:00 <Detail>`__   JEANÉMART Jérôme (181)       Evaluation              Auswertung 6    [▽] **Suggested** → [Notified]
 `Mon 19/01/2015 at 09:00 <Detail>`__   BRECHT Bernd (177)           Evaluation              Auswertung 7    [▽] **Suggested** → [Notified]
 `Mon 09/02/2015 at 09:00 <Detail>`__   JEANÉMART Jérôme (181)       Evaluation              Auswertung 7    [▽] **Suggested** → [Notified]
 `Thu 19/02/2015 at 09:00 <Detail>`__   BRECHT Bernd (177)           Evaluation              Auswertung 8    [▽] **Suggested** → [Notified]
 `Tue 03/03/2015 <Detail>`__            DENON Denis (180*)           Evaluation              Auswertung 4    [▽] **Suggested** → [Notified]
 `Mon 09/03/2015 at 09:00 <Detail>`__   JEANÉMART Jérôme (181)       Evaluation              Auswertung 8    [▽] **Suggested** → [Notified]
 `Thu 19/03/2015 at 09:00 <Detail>`__   BRECHT Bernd (177)           Evaluation              Auswertung 9    [▽] **Suggested** → [Notified]
 `Thu 09/04/2015 at 09:00 <Detail>`__   JEANÉMART Jérôme (181)       Evaluation              Auswertung 9    [▽] **Suggested** → [Notified]
 `Mon 20/04/2015 at 09:00 <Detail>`__   BRECHT Bernd (177)           Evaluation              Auswertung 10   [▽] **Suggested** → [Notified]
====================================== ============================ ======================= =============== =================================
<BLANKLINE>



And these for Mélanie:

>>> rt.login('melanie').show(cal.MyEvents, language='en')
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE -REPORT_UDIFF
====================================== ============================= ======================= ==================== =================================
 When                                   Client                        Calendar Event Type     Summary              Workflow
-------------------------------------- ----------------------------- ----------------------- -------------------- ---------------------------------
 `Thu 22/05/2014 at 09:40 <Detail>`__   JANSEN Jérémy (136)           Informational meeting   Diner                **Suggested** → [Notified]
 `Fri 23/05/2014 at 10:20 <Detail>`__                                 Internal meeting        Souper               **Draft** → [Notified] [Cancel]
 `Sat 24/05/2014 at 11:10 <Detail>`__                                 External meeting        Petit-déjeuner       **Took place** → [Reset]
 `Sat 24/05/2014 at 13:30 <Detail>`__                                 Private                 Rencontre            **Cancelled**
 `Sun 25/05/2014 at 08:30 <Detail>`__                                 Meeting                 Consultation         **Omitted**
 `Mon 26/05/2014 at 09:00 <Detail>`__   ENGELS Edgar (129)            Evaluation              Évaluation 3         [▽] **Suggested** → [Notified]
 `Mon 26/05/2014 at 09:40 <Detail>`__   JACOBS Jacqueline (137)       Appointment             Séminaire            **Notified** → [Cancel] [Reset]
 `Mon 26/05/2014 at 10:20 <Detail>`__   JOHNEN Johann (138)           Evaluation              Evaluation           **Suggested** → [Notified]
 `Tue 27/05/2014 at 11:10 <Detail>`__   JONAS Josef (139)             External meeting        Première rencontre   **Draft** → [Notified] [Cancel]
 `Wed 28/05/2014 at 08:30 <Detail>`__                                 Internal meeting        Diner                **Cancelled**
 `Wed 28/05/2014 at 13:30 <Detail>`__   JOUSTEN Jan (140*)            Informational meeting   Interview            **Took place** → [Reset]
 `Thu 29/05/2014 at 09:40 <Detail>`__                                 External meeting        Souper               **Omitted**
 `Fri 30/05/2014 at 10:20 <Detail>`__                                 Private                 Petit-déjeuner       **Notified** → [Cancel] [Reset]
 `Thu 05/06/2014 at 09:00 <Detail>`__   LAZARUS Line (144)            Evaluation              Évaluation 2         [▽] **Suggested** → [Notified]
 `Thu 05/06/2014 at 09:00 <Detail>`__   DUBOIS Robin (179)            Evaluation              Évaluation 15        [▽] **Suggested** → [Notified]
 `Fri 13/06/2014 <Detail>`__            MALMENDIER Marc (146)         Evaluation              Évaluation 2         [▽] **Suggested** → [Notified]
 `Mon 16/06/2014 at 09:00 <Detail>`__   MEESSEN Melissa (147)         Evaluation              Évaluation 1         [▽] **Suggested** → [Notified]
 `Thu 26/06/2014 at 09:00 <Detail>`__   ENGELS Edgar (129)            Evaluation              Évaluation 4         [▽] **Suggested** → [Notified]
 `Wed 02/07/2014 <Detail>`__            RADERMACHER Christian (155)   Evaluation              Évaluation 2         [▽] **Suggested** → [Notified]
 `Wed 02/07/2014 at 09:00 <Detail>`__   ÖSTGES Otto (168)             Evaluation              Évaluation 1         [▽] **Suggested** → [Notified]
 `Mon 07/07/2014 at 09:00 <Detail>`__   LAZARUS Line (144)            Evaluation              Évaluation 3         [▽] **Suggested** → [Notified]
 `Mon 14/07/2014 at 09:00 <Detail>`__   RADERMACHER Guido (159)       Evaluation              Évaluation 1         [▽] **Suggested** → [Notified]
 `Wed 16/07/2014 at 09:00 <Detail>`__   MEESSEN Melissa (147)         Evaluation              Évaluation 2         [▽] **Suggested** → [Notified]
 `Tue 22/07/2014 at 09:00 <Detail>`__   DUBOIS Robin (179)            Evaluation              Évaluation 1         [▽] **Suggested** → [Notified]
 `Mon 28/07/2014 at 09:00 <Detail>`__   ENGELS Edgar (129)            Evaluation              Évaluation 5         [▽] **Suggested** → [Notified]
 `Mon 04/08/2014 at 09:00 <Detail>`__   ÖSTGES Otto (168)             Evaluation              Évaluation 1         [▽] **Suggested** → [Notified]
 `Thu 07/08/2014 at 09:00 <Detail>`__   LAZARUS Line (144)            Evaluation              Évaluation 4         [▽] **Suggested** → [Notified]
 `Thu 14/08/2014 at 09:00 <Detail>`__   RADERMACHER Guido (159)       Evaluation              Évaluation 2         [▽] **Suggested** → [Notified]
 `Mon 18/08/2014 at 09:00 <Detail>`__   MEESSEN Melissa (147)         Evaluation              Évaluation 3         [▽] **Suggested** → [Notified]
 `Mon 25/08/2014 at 09:00 <Detail>`__   DUBOIS Robin (179)            Evaluation              Évaluation 1         [▽] **Suggested** → [Notified]
 `Thu 28/08/2014 at 09:00 <Detail>`__   ENGELS Edgar (129)            Evaluation              Évaluation 6         [▽] **Suggested** → [Notified]
 `Thu 04/09/2014 at 09:00 <Detail>`__   ÖSTGES Otto (168)             Evaluation              Évaluation 2         [▽] **Suggested** → [Notified]
 `Mon 08/09/2014 at 09:00 <Detail>`__   LAZARUS Line (144)            Evaluation              Évaluation 5         [▽] **Suggested** → [Notified]
 `Mon 15/09/2014 <Detail>`__            MALMENDIER Marc (146)         Evaluation              Évaluation 3         [▽] **Suggested** → [Notified]
 `Mon 15/09/2014 at 09:00 <Detail>`__   RADERMACHER Guido (159)       Evaluation              Évaluation 3         [▽] **Suggested** → [Notified]
 `Thu 18/09/2014 at 09:00 <Detail>`__   MEESSEN Melissa (147)         Evaluation              Évaluation 4         [▽] **Suggested** → [Notified]
 `Thu 25/09/2014 at 09:00 <Detail>`__   DUBOIS Robin (179)            Evaluation              Évaluation 2         [▽] **Suggested** → [Notified]
 `Mon 29/09/2014 at 09:00 <Detail>`__   ENGELS Edgar (129)            Evaluation              Évaluation 7         [▽] **Suggested** → [Notified]
 `Thu 02/10/2014 <Detail>`__            RADERMACHER Christian (155)   Evaluation              Évaluation 3         [▽] **Suggested** → [Notified]
 `Mon 06/10/2014 at 09:00 <Detail>`__   ÖSTGES Otto (168)             Evaluation              Évaluation 3         [▽] **Suggested** → [Notified]
 `Wed 08/10/2014 at 09:00 <Detail>`__   LAZARUS Line (144)            Evaluation              Évaluation 6         [▽] **Suggested** → [Notified]
 `Wed 15/10/2014 at 09:00 <Detail>`__   RADERMACHER Guido (159)       Evaluation              Évaluation 4         [▽] **Suggested** → [Notified]
 `Mon 20/10/2014 at 09:00 <Detail>`__   MEESSEN Melissa (147)         Evaluation              Évaluation 5         [▽] **Suggested** → [Notified]
 `Mon 27/10/2014 at 09:00 <Detail>`__   DUBOIS Robin (179)            Evaluation              Évaluation 3         [▽] **Suggested** → [Notified]
 `Wed 29/10/2014 at 09:00 <Detail>`__   ENGELS Edgar (129)            Evaluation              Évaluation 8         [▽] **Suggested** → [Notified]
 `Thu 06/11/2014 at 09:00 <Detail>`__   ÖSTGES Otto (168)             Evaluation              Évaluation 4         [▽] **Suggested** → [Notified]
 `Mon 10/11/2014 at 09:00 <Detail>`__   LAZARUS Line (144)            Evaluation              Évaluation 7         [▽] **Suggested** → [Notified]
 `Mon 17/11/2014 at 09:00 <Detail>`__   RADERMACHER Guido (159)       Evaluation              Évaluation 5         [▽] **Suggested** → [Notified]
 `Thu 20/11/2014 at 09:00 <Detail>`__   MEESSEN Melissa (147)         Evaluation              Évaluation 6         [▽] **Suggested** → [Notified]
 `Thu 27/11/2014 at 09:00 <Detail>`__   DUBOIS Robin (179)            Evaluation              Évaluation 4         [▽] **Suggested** → [Notified]
 `Mon 01/12/2014 at 09:00 <Detail>`__   ENGELS Edgar (129)            Evaluation              Évaluation 9         [▽] **Suggested** → [Notified]
 `Mon 08/12/2014 at 09:00 <Detail>`__   ÖSTGES Otto (168)             Evaluation              Évaluation 5         [▽] **Suggested** → [Notified]
 `Wed 10/12/2014 at 09:00 <Detail>`__   LAZARUS Line (144)            Evaluation              Évaluation 8         [▽] **Suggested** → [Notified]
 `Wed 17/12/2014 at 09:00 <Detail>`__   RADERMACHER Guido (159)       Evaluation              Évaluation 6         [▽] **Suggested** → [Notified]
 `Mon 22/12/2014 at 09:00 <Detail>`__   MEESSEN Melissa (147)         Evaluation              Évaluation 7         [▽] **Suggested** → [Notified]
 `Mon 29/12/2014 at 09:00 <Detail>`__   DUBOIS Robin (179)            Evaluation              Évaluation 5         [▽] **Suggested** → [Notified]
 `Fri 02/01/2015 <Detail>`__            RADERMACHER Christian (155)   Evaluation              Évaluation 4         [▽] **Suggested** → [Notified]
 `Thu 08/01/2015 at 09:00 <Detail>`__   ÖSTGES Otto (168)             Evaluation              Évaluation 6         [▽] **Suggested** → [Notified]
 `Mon 12/01/2015 at 09:00 <Detail>`__   LAZARUS Line (144)            Evaluation              Évaluation 9         [▽] **Suggested** → [Notified]
 `Mon 19/01/2015 at 09:00 <Detail>`__   RADERMACHER Guido (159)       Evaluation              Évaluation 7         [▽] **Suggested** → [Notified]
 `Thu 22/01/2015 at 09:00 <Detail>`__   MEESSEN Melissa (147)         Evaluation              Évaluation 8         [▽] **Suggested** → [Notified]
 `Thu 29/01/2015 at 09:00 <Detail>`__   DUBOIS Robin (179)            Evaluation              Évaluation 6         [▽] **Suggested** → [Notified]
 `Mon 09/02/2015 at 09:00 <Detail>`__   ÖSTGES Otto (168)             Evaluation              Évaluation 7         [▽] **Suggested** → [Notified]
 `Thu 19/02/2015 at 09:00 <Detail>`__   RADERMACHER Guido (159)       Evaluation              Évaluation 8         [▽] **Suggested** → [Notified]
 `Mon 23/02/2015 at 09:00 <Detail>`__   MEESSEN Melissa (147)         Evaluation              Évaluation 9         [▽] **Suggested** → [Notified]
 `Mon 02/03/2015 at 09:00 <Detail>`__   DUBOIS Robin (179)            Evaluation              Évaluation 7         [▽] **Suggested** → [Notified]
 `Mon 09/03/2015 at 09:00 <Detail>`__   ÖSTGES Otto (168)             Evaluation              Évaluation 8         [▽] **Suggested** → [Notified]
 `Thu 19/03/2015 at 09:00 <Detail>`__   RADERMACHER Guido (159)       Evaluation              Évaluation 9         [▽] **Suggested** → [Notified]
 `Thu 02/04/2015 at 09:00 <Detail>`__   DUBOIS Robin (179)            Evaluation              Évaluation 8         [▽] **Suggested** → [Notified]
 `Thu 09/04/2015 at 09:00 <Detail>`__   ÖSTGES Otto (168)             Evaluation              Évaluation 9         [▽] **Suggested** → [Notified]
 `Mon 20/04/2015 at 09:00 <Detail>`__   RADERMACHER Guido (159)       Evaluation              Évaluation 10        [▽] **Suggested** → [Notified]
 `Mon 04/05/2015 at 09:00 <Detail>`__   DUBOIS Robin (179)            Evaluation              Évaluation 9         [▽] **Suggested** → [Notified]
 `Mon 11/05/2015 at 09:00 <Detail>`__   ÖSTGES Otto (168)             Evaluation              Évaluation 10        [▽] **Suggested** → [Notified]
====================================== ============================= ======================= ==================== =================================
<BLANKLINE>


These are Alicia's calendar appointments of the last two months:

>>> last_week = dict(start_date=dd.today(-30), end_date=dd.today(-1))
>>> rt.login('alicia').show(cal.MyEvents, language='en',
...     param_values=last_week)
====================================== ========================= ===================== =============== ================================
 When                                   Client                    Calendar Event Type   Summary         Workflow
-------------------------------------- ------------------------- --------------------- --------------- --------------------------------
 `Wed 07/05/2014 at 09:00 <Detail>`__   DA VINCI David (165)      Evaluation            Évaluation 15   [▽] **Suggested** → [Notified]
 `Wed 14/05/2014 <Detail>`__            HILGERS Hildegard (133)   Evaluation            Évaluation 6    [▽] **Suggested** → [Notified]
====================================== ========================= ===================== =============== ================================
<BLANKLINE>


Calendars and Subscriptions
===========================

A Calendar is a set of events that can be shown or hidden in the
Calendar Panel.

In Lino Welfare, we have one Calendar per User.  Or to be more
precise: 

- The :ddref:`users.User` model has a :ddref:`users.User.calendar`
  field.

- The calendar of an :ddref:`cal.Event` is indirectly defined by the
  Event's :ddref:`cal.Event.user` field.

Two users can share a common calendar.  This is possible when two
colleagues really work together when receiving visitors.

A Subscription is when a given user decides that she wants to see the
calendar of another user.

Every user is, by default, subscribed to her own calendar.
For example, demo user `rolf` is automatically subscribed to the
following calendars:

>>> ses = rt.login('rolf')
>>> with translation.override('de'):
...    ses.show(cal.SubscriptionsByUser, ses.get_user()) #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
==== ========== ===========
 ID   Kalender   versteckt
---- ---------- -----------
 8    rolf       Nein
==== ========== ===========
<BLANKLINE>


Events by client
================

This table is special in that it shows not only events directly
related to the client (i.e. :attr:`Event.project` pointing to it) but
also those where this client is among the guests.

>>> candidates = set()
>>> for obj in cal.Guest.objects.all():
...     if obj.partner and obj.partner_id != obj.event.project_id:
...         #print obj, obj.event.project_id, obj.partner_id
...         candidates.add(obj.event.project_id)
>>> print sorted(candidates)
[116, 127, 129, 133, 144, 146, 147, 157, 159, 166, 168, 173, 177, 179, 181]

>>> settings.SITE.site_config.hide_events_before
datetime.date(2014, 4, 1)


>>> obj = pcsw.Client.objects.get(pk=127)
>>> rt.show(cal.EventsByClient, obj, header_level=1, language="en")
========================================================
Events of EVERS Eberhart (127) (Dates 01.04.2014 to ...)
========================================================
============================ ================= ================ ===============
 When                         Managed by        Summary          Workflow
---------------------------- ----------------- ---------------- ---------------
 **Tue 15/04/2014 (09:00)**   Caroline Carnol   Auswertung 1     **Suggested**
 **Thu 15/05/2014 (09:00)**   Caroline Carnol   Auswertung 2     **Suggested**
 **Thu 22/05/2014**           Mélanie Mélard    Urgent problem   **Notified**
 **Tue 27/05/2014 (13:30)**   Hubert Huppertz   Abendessen       **Draft**
 **Mon 16/06/2014 (09:00)**   Caroline Carnol   Auswertung 3     **Suggested**
 **Wed 16/07/2014 (09:00)**   Caroline Carnol   Auswertung 4     **Suggested**
 **Mon 18/08/2014 (09:00)**   Caroline Carnol   Auswertung 5     **Suggested**
 **Thu 18/09/2014 (09:00)**   Caroline Carnol   Auswertung 6     **Suggested**
 **Mon 20/10/2014 (09:00)**   Caroline Carnol   Auswertung 7     **Suggested**
 **Thu 20/11/2014 (09:00)**   Caroline Carnol   Auswertung 8     **Suggested**
 **Mon 22/12/2014 (09:00)**   Caroline Carnol   Auswertung 9     **Suggested**
============================ ================= ================ ===============
<BLANKLINE>


Events generated by a contract
==============================

>>> settings.SITE.site_config.hide_events_before = None
>>> obj = isip.Contract.objects.get(id=18)
>>> rt.show(cal.EventsByController, obj, header_level=1, language="en")
======================================
Events of ISIP#18 (Edgard RADERMACHER)
======================================
============================ =============== ================= ============= ===============
 When                         Summary         Managed by        Assigned to   Workflow
---------------------------- --------------- ----------------- ------------- ---------------
 **Thu 07/02/2013 (09:00)**   Évaluation 1    Alicia Allmanns                 **Suggested**
 **Thu 07/03/2013 (09:00)**   Évaluation 2    Alicia Allmanns                 **Suggested**
 **Mon 08/04/2013 (09:00)**   Évaluation 3    Alicia Allmanns                 **Suggested**
 **Wed 08/05/2013 (09:00)**   Évaluation 4    Alicia Allmanns                 **Suggested**
 **Mon 10/06/2013 (09:00)**   Évaluation 5    Alicia Allmanns                 **Suggested**
 **Wed 10/07/2013 (09:00)**   Évaluation 6    Alicia Allmanns                 **Suggested**
 **Mon 12/08/2013 (09:00)**   Évaluation 7    Alicia Allmanns                 **Suggested**
 **Thu 12/09/2013 (09:00)**   Évaluation 8    Alicia Allmanns                 **Suggested**
 **Mon 14/10/2013 (09:00)**   Évaluation 9    Alicia Allmanns                 **Suggested**
 **Thu 14/11/2013 (09:00)**   Évaluation 10   Alicia Allmanns                 **Suggested**
============================ =============== ================= ============= ===============
<BLANKLINE>

