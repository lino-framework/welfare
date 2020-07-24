.. doctest docs/specs/main.rst
.. _welfare.specs.main:

===================
The admin main page
===================

This describes the main page of :ref:`welfare`.

.. contents::
   :depth: 1

.. include:: /../docs/shared/include/tested.rst

>>> from lino import startup
>>> startup('lino_welfare.projects.gerd.settings.doctests')
>>> from lino.api.doctest import *

Some tests
==========

Test the content of the admin main page.

>>> test_client.force_login(rt.login('rolf').user)
>>> res = test_client.get('/api/main_html', REMOTE_USER='rolf')
>>> print(res.status_code)
200
>>> result = json.loads(res.content)
>>> result['success']
True
>>> # print(html2text(result['html']))
>>> soup = BeautifulSoup(result['html'], 'lxml')

We might test the complete content here, but currently we skip this as
it is much work to maintain.

>>> print(soup.get_text(' ', strip=True))
... #doctest: +NORMALIZE_WHITESPACE +REPORT_CDIFF +SKIP

>>> links = soup.find_all('a')
>>> len(links)
125

>>> print(links[0].text)
Suchen

>>> tables = soup.find_all('table')
>>> len(tables)
4

>>> for h in soup.find_all('h2'):
...     print(h.text.strip())
Benutzer und ihre Klienten ⏏
Wartende Besucher ⏏
Meine Termine  ⏏
Meine überfälligen Termine  ⏏
Meine Benachrichtigungen ✓ ⏏


>>> test_client.force_login(rt.login('robin').user)
>>> res = test_client.get('/api/main_html', REMOTE_USER='robin')
>>> print(res.status_code)
200
>>> result = json.loads(res.content)
>>> soup = BeautifulSoup(result['html'], 'lxml')
>>> for h in soup.find_all('h2'):
...     print(h.text.strip())
Users with their Clients ⏏
Waiting visitors ⏏
My appointments  ⏏
My overdue appointments  ⏏
My Notification messages ✓ ⏏


Here is a text variant of Hubert's dashboard.
Not tested because some details are changing in the demo database.

>>> rt.login('hubert').show_dashboard()
... #doctest: +NORMALIZE_WHITESPACE +REPORT_CDIFF +ELLIPSIS +SKIP
---------------------------------------------------------
Users with their Clients `⏏ <Users with their Clients>`__
---------------------------------------------------------
<BLANKLINE>
==================== ============ ============ ======== ======== ========= ================= ================ ========
 Coach                Auswertung   Ausbildung   Suchen   Arbeit   Standby   Primary clients   Active clients   Total
-------------------- ------------ ------------ -------- -------- --------- ----------------- ---------------- --------
 Alicia Allmanns      **4**        **1**                 **1**    **1**     **3**             **3**            **7**
 Hubert Huppertz      **5**        **4**        **6**    **1**    **1**     **14**            **14**           **17**
 Mélanie Mélard       **2**        **4**        **6**    **4**    **3**     **10**            **10**           **19**
 **Total (3 rows)**   **11**       **9**        **12**   **6**    **5**     **27**            **27**           **43**
==================== ============ ============ ======== ======== ========= ================= ================ ========
<BLANKLINE>
-------------------------------------------------------
Visitors waiting for me `⏏ <Visitors waiting for me>`__
-------------------------------------------------------
<BLANKLINE>
========================== ===================== ========== =================== =======================================================
 Since                      Client                Position   Short description   Workflow
-------------------------- --------------------- ---------- ------------------- -------------------------------------------------------
 `5 years ago <Detail>`__   EMONTS Daniel (128)   1                              [Receive] [Checkout] **Waiting** → [Absent] [Excused]
 `5 years ago <Detail>`__   JONAS Josef (139)     2                              [Receive] [Checkout] **Waiting** → [Absent] [Excused]
 `5 years ago <Detail>`__   LAZARUS Line (144)    3                              [Receive] [Checkout] **Waiting** → [Absent] [Excused]
========================== ===================== ========== =================== =======================================================
<BLANKLINE>
-----------------------------------------
Waiting visitors `⏏ <Waiting visitors>`__
-----------------------------------------
<BLANKLINE>
========================== ========================= ================= ========== =================== =======================================================
 Since                      Client                    Managed by        Position   Short description   Workflow
-------------------------- ------------------------- ----------------- ---------- ------------------- -------------------------------------------------------
 `5 years ago <Detail>`__   EMONTS Daniel (128)       Hubert Huppertz   1                              [Receive] [Checkout] **Waiting** → [Absent] [Excused]
 `5 years ago <Detail>`__   EVERS Eberhart (127)      Mélanie Mélard    1          Urgent problem      **Waiting** → [Absent] [Excused]
 `5 years ago <Detail>`__   HILGERS Hildegard (133)   Alicia Allmanns   1          Beschwerde          **Waiting** → [Absent] [Excused]
 `5 years ago <Detail>`__   JACOBS Jacqueline (137)   Judith Jousten    1          Information         **Waiting** → [Absent] [Excused]
 `5 years ago <Detail>`__   JONAS Josef (139)         Hubert Huppertz   2                              [Receive] [Checkout] **Waiting** → [Absent] [Excused]
 `5 years ago <Detail>`__   KAIVERS Karl (141)        Alicia Allmanns   2          Beschwerde          **Waiting** → [Absent] [Excused]
 `5 years ago <Detail>`__   LAMBERTZ Guido (142)      Mélanie Mélard    2          Urgent problem      **Waiting** → [Absent] [Excused]
 `5 years ago <Detail>`__   LAZARUS Line (144)        Hubert Huppertz   3                              [Receive] [Checkout] **Waiting** → [Absent] [Excused]
========================== ========================= ================= ========== =================== =======================================================
<BLANKLINE>
-----------------------------------------------
My appointments **New** `⏏ <My appointments>`__
-----------------------------------------------
<BLANKLINE>
====================================== ======================== ===================== =================== ===============================
 When                                   Client                   Calendar entry type   Short description   Workflow
-------------------------------------- ------------------------ --------------------- ------------------- -------------------------------
 `Tue 27/05/2014 at 10:20 <Detail>`__                            Internal              Abendessen          **☼ Published** → [☒] [☐]
 `Wed 28/05/2014 at 09:00 <Detail>`__   BRECHT Bernd (177)       Evaluation            Évaluation 15       [▽] **? Suggested** → [☼] [☒]
 `Mon 02/06/2014 at 09:40 <Detail>`__                            Internal              Abendessen          **☐ Draft** → [☼] [☒]
 `Tue 03/06/2014 <Detail>`__            DENON Denis (180*)       Evaluation            Auswertung 1        [▽] **? Suggested** → [☼] [☒]
 `Wed 04/06/2014 <Detail>`__            LAMBERTZ Guido (142)     Evaluation            Évaluation 6        [▽] **? Suggested** → [☼] [☒]
 `Sun 08/06/2014 at 08:30 <Detail>`__                            Internal              Abendessen          **? Suggested** → [☼] [☒]
 `Thu 19/06/2014 at 09:00 <Detail>`__   JEANÉMART Jérôme (181)   Evaluation            Évaluation 15       [▽] **? Suggested** → [☼] [☒]
 `Mon 14/07/2014 at 09:00 <Detail>`__   BRECHT Bernd (177)       Evaluation            Auswertung 1        [▽] **? Suggested** → [☼] [☒]
 `Mon 04/08/2014 at 09:00 <Detail>`__   JEANÉMART Jérôme (181)   Evaluation            Auswertung 1        [▽] **? Suggested** → [☼] [☒]
 `Tue 05/08/2014 <Detail>`__            FAYMONVILLE Luc (130*)   Evaluation            Auswertung 3        [▽] **? Suggested** → [☼] [☒]
 `Tue 12/08/2014 <Detail>`__            RADERMECKER Rik (173)    Evaluation            Auswertung 2        [▽] **? Suggested** → [☼] [☒]
 `Thu 14/08/2014 at 09:00 <Detail>`__   BRECHT Bernd (177)       Evaluation            Auswertung 2        [▽] **? Suggested** → [☼] [☒]
 `Wed 03/09/2014 <Detail>`__            DENON Denis (180*)       Evaluation            Auswertung 2        [▽] **? Suggested** → [☼] [☒]
 `Thu 04/09/2014 <Detail>`__            LAMBERTZ Guido (142)     Evaluation            Évaluation 7        [▽] **? Suggested** → [☼] [☒]
 `Thu 04/09/2014 at 09:00 <Detail>`__   JEANÉMART Jérôme (181)   Evaluation            Auswertung 2        [▽] **? Suggested** → [☼] [☒]
====================================== ======================== ===================== =================== ===============================
<BLANKLINE>
---------------------------------------------------------------
My overdue appointments **New** `⏏ <My overdue appointments>`__
---------------------------------------------------------------
<BLANKLINE>
=========================================================================== ========================================================== ===================== ===================================
 Calendar entry                                                              Controlled by                                              Calendar entry type   Workflow
--------------------------------------------------------------------------- ---------------------------------------------------------- --------------------- -----------------------------------
 `Évaluation 10 (16.01.2014 09:00) with JEANÉMART Jérôme (181) <Detail>`__   `ISIP#32 (Jérôme JEANÉMART) <Detail>`__                    Evaluation            [▽] **? Suggested** → [☼] [☑] [☒]
 `Évaluation 11 (27.01.2014 09:00) with BRECHT Bernd (177) <Detail>`__       `ISIP#27 (Bernd BRECHT) <Detail>`__                        Evaluation            [▽] **? Suggested** → [☼] [☑] [☒]
 `Auswertung 1 (03.02.2014) with FAYMONVILLE Luc (130*) <Detail>`__          `Art60§7 job supplyment#4 (Luc FAYMONVILLE) <Detail>`__    Evaluation            [▽] **? Suggested** → [☼] [☑] [☒]
 `Évaluation 11 (17.02.2014 09:00) with JEANÉMART Jérôme (181) <Detail>`__   `ISIP#32 (Jérôme JEANÉMART) <Detail>`__                    Evaluation            [▽] **? Suggested** → [☼] [☑] [☒]
 `Évaluation 12 (27.02.2014 09:00) with BRECHT Bernd (177) <Detail>`__       `ISIP#27 (Bernd BRECHT) <Detail>`__                        Evaluation            [▽] **? Suggested** → [☼] [☑] [☒]
 `Évaluation 12 (17.03.2014 09:00) with JEANÉMART Jérôme (181) <Detail>`__   `ISIP#32 (Jérôme JEANÉMART) <Detail>`__                    Evaluation            [▽] **? Suggested** → [☼] [☑] [☒]
 `Évaluation 13 (27.03.2014 09:00) with BRECHT Bernd (177) <Detail>`__       `ISIP#27 (Bernd BRECHT) <Detail>`__                        Evaluation            [▽] **? Suggested** → [☼] [☑] [☒]
 `Évaluation 13 (17.04.2014 09:00) with JEANÉMART Jérôme (181) <Detail>`__   `ISIP#32 (Jérôme JEANÉMART) <Detail>`__                    Evaluation            [▽] **? Suggested** → [☼] [☑] [☒]
 `Évaluation 14 (28.04.2014 09:00) with BRECHT Bernd (177) <Detail>`__       `ISIP#27 (Bernd BRECHT) <Detail>`__                        Evaluation            [▽] **? Suggested** → [☼] [☑] [☒]
 `Abendessen (03.05.2014 09:40) <Detail>`__                                                                                             Internal              **☐ Draft** → [☼] [☑] [☒]
 `Auswertung 2 (05.05.2014) with FAYMONVILLE Luc (130*) <Detail>`__          `Art60§7 job supplyment#4 (Luc FAYMONVILLE) <Detail>`__    Evaluation            [▽] **? Suggested** → [☼] [☑] [☒]
 `Abendessen (09.05.2014 08:30) <Detail>`__                                                                                             Internal              **? Suggested** → [☼] [☑] [☒]
 `Auswertung 1 (12.05.2014) with RADERMECKER Rik (173) <Detail>`__           `Art60§7 job supplyment#14 (Rik RADERMECKER) <Detail>`__   Evaluation            [▽] **? Suggested** → [☼] [☑] [☒]
 `Évaluation 14 (19.05.2014 09:00) with JEANÉMART Jérôme (181) <Detail>`__   `ISIP#32 (Jérôme JEANÉMART) <Detail>`__                    Evaluation            [▽] **? Suggested** → [☼] [☑] [☒]
=========================================================================== ========================================================== ===================== ===================================
<BLANKLINE>
---------------------------------------------------------------
My Notification messages **✓** `⏏ <My Notification messages>`__
---------------------------------------------------------------
<BLANKLINE>
===================== ==================================== ============== ==========
 Created               Subject                              Message Type   Workflow
--------------------- ------------------------------------ -------------- ----------
 2014-05-22 05:48:00   Die Datenbank wurde initialisiert.   System event   [✓]
===================== ==================================== ============== ==========
<BLANKLINE>
