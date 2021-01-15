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
113

>>> print(links[0].text)
Suchen

>>> tables = soup.find_all('table')
>>> len(tables)
3

>>> for h in soup.find_all('h2'):
...     print(h.text.strip())
Benutzer und ihre Klienten ⏏
Wartende Besucher ⏏
Meine Termine  ⏏
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
My Notification messages ✓ ⏏


Here is a text variant of Hubert's dashboard.

.. Not tested because some details are changing in the demo database.

>>> show_dashboard('hubert', ignore_links=True)
... #doctest: +NORMALIZE_WHITESPACE +REPORT_CDIFF +ELLIPSIS -SKIP
Quick links: [Calendar] [Read eID card] [Clients] [ISIPs] [Art60§7 job
supplyments] [Appointments today] autorefresh [Refresh]
<BLANKLINE>
Hi, Hubert Huppertz! You are busy in Consultations with client (22.05.2014)
with BRECHT Bernd (177) (☑).  There are 2 data problems assigned to you. You
have 16 items in Grantings to confirm.
<BLANKLINE>
This is a Lino demo site. Try also the other demo sites. Your feedback is
welcome to users@lino-framework.org or directly to the person who invited you.
**We are running with simulated date set to Thursday, 22 May 2014.**
<BLANKLINE>
## Users with their Clients ⏏
<BLANKLINE>
Coach| Auswertung| Ausbildung| Suchen| Arbeit| Standby| Primary clients|
Active clients| Total
---|---|---|---|---|---|---|---|---
 _Alicia Allmanns_| 4| 1| | 1| 1| 3| 3| 7
 _Hubert Huppertz_| 5| 4| 6| 1| 1| 14| 14| 17
 _Mélanie Mélard_| 2| 4| 6| 4| 3| 10| 10| 19
 **Total (3 rows)**|  **11**|  **9**|  **12**|  **6**|  **5**|  **27**|
**27**|  **43**
<BLANKLINE>
## Visitors waiting for me ⏏
<BLANKLINE>
Since| Client| Position| Short description| Workflow
---|---|---|---|---
6 years, 7 months ago| EMONTS Daniel (128)| 1| | Receive Checkout **Waiting**
→ Absent Excused
6 years, 7 months ago| JONAS Josef (139)| 2| | Receive Checkout **Waiting** →
Absent Excused
6 years, 7 months ago| LAZARUS Line (144)| 3| | Receive Checkout **Waiting** →
Absent Excused
<BLANKLINE>
## Waiting visitors ⏏
<BLANKLINE>
Since| Client| Managed by| Position| Short description| Workflow
---|---|---|---|---|---
6 years, 7 months ago| EMONTS Daniel (128)| Hubert Huppertz| 1| | Receive
Checkout **Waiting** → Absent Excused
6 years, 7 months ago| EVERS Eberhart (127)| Mélanie Mélard| 1| Urgent
problem|  **Waiting** → Absent Excused
6 years, 7 months ago| HILGERS Hildegard (133)| Alicia Allmanns| 1|
Beschwerde|  **Waiting** → Absent Excused
6 years, 7 months ago| JACOBS Jacqueline (137)| Judith Jousten| 1|
Information|  **Waiting** → Absent Excused
6 years, 7 months ago| JONAS Josef (139)| Hubert Huppertz| 2| | Receive
Checkout **Waiting** → Absent Excused
6 years, 7 months ago| KAIVERS Karl (141)| Alicia Allmanns| 2| Beschwerde|
**Waiting** → Absent Excused
6 years, 7 months ago| LAMBERTZ Guido (142)| Mélanie Mélard| 2| Urgent
problem|  **Waiting** → Absent Excused
6 years, 7 months ago| LAZARUS Line (144)| Hubert Huppertz| 3| | Receive
Checkout **Waiting** → Absent Excused
<BLANKLINE>
## My appointments ![add](/static/images/mjames/add.png) ⏏
<BLANKLINE>
When| Client| Calendar entry type| Short description| Workflow
---|---|---|---|---
Sat 24/05/2014 at 11:10| HILGERS Hildegard (133)|  _Internal meetings with
client_|  Auswertung|  **? Suggested** →  ☼  ☒
Mon 26/05/2014| |  _Absences_|  Absent for private reasons|  **? Suggested** →
☼  ☒
Wed 28/05/2014 at 09:00| BRECHT Bernd (177)|  _Evaluation_|  Évaluation 15|  ▽
**? Suggested** →  ☼  ☒
Fri 30/05/2014 at 09:40| JACOBS Jacqueline (137)|  _Internal meetings with
client_|  Seminar|  **? Suggested** →  ☼  ☒
Tue 03/06/2014| DENON Denis (180*)|  _Evaluation_|  Auswertung 1|  ▽  **?
Suggested** →  ☼  ☒
Wed 04/06/2014| LAMBERTZ Guido (142)|  _Evaluation_|  Évaluation 6|  ▽  **?
Suggested** →  ☼  ☒
Wed 04/06/2014 at 13:30| KAIVERS Karl (141)|  _Internal meetings with client_|
Beratung|  **? Suggested** →  ☼  ☒
Mon 09/06/2014 at 10:20| LEFFIN Josefine (145)|  _Internal meetings with
client_|  Treffen|  **? Suggested** →  ☼  ☒
Thu 19/06/2014 at 09:00| JEANÉMART Jérôme (181)|  _Evaluation_|  Évaluation
15|  ▽  **? Suggested** →  ☼  ☒
Mon 14/07/2014 at 09:00| BRECHT Bernd (177)|  _Evaluation_|  Auswertung 1|  ▽
**? Suggested** →  ☼  ☒
Mon 04/08/2014 at 09:00| JEANÉMART Jérôme (181)|  _Evaluation_|  Auswertung 1|
▽  **? Suggested** →  ☼  ☒
Tue 05/08/2014| FAYMONVILLE Luc (130*)|  _Evaluation_|  Auswertung 3|  ▽  **?
Suggested** →  ☼  ☒
Tue 12/08/2014| RADERMECKER Rik (173)|  _Evaluation_|  Auswertung 2|  ▽  **?
Suggested** →  ☼  ☒
Thu 14/08/2014 at 09:00| BRECHT Bernd (177)|  _Evaluation_|  Auswertung 2|  ▽
**? Suggested** →  ☼  ☒
Wed 03/09/2014| DENON Denis (180*)|  _Evaluation_|  Auswertung 2|  ▽  **?
Suggested** →  ☼  ☒
<BLANKLINE>
## My overdue appointments ![add](/static/images/mjames/add.png) ⏏
<BLANKLINE>
Calendar entry| Controlled by| Calendar entry type| Workflow
---|---|---|---
Évaluation 13 (17.04.2014 09:00) with JEANÉMART Jérôme (181)| ISIP#32 (Jérôme
JEANÉMART)|  _Evaluation_|  ▽  **? Suggested** →  ☼  ☑  ☒
Évaluation 14 (28.04.2014 09:00) with BRECHT Bernd (177)| ISIP#27 (Bernd
BRECHT)|  _Evaluation_|  ▽  **? Suggested** →  ☼  ☑  ☒
Auswertung 2 (05.05.2014) with FAYMONVILLE Luc (130*)| Art60§7 job
supplyment#4 (Luc FAYMONVILLE)|  _Evaluation_|  ▽  **? Suggested** →  ☼  ☑  ☒
Auswertung 1 (12.05.2014) with RADERMECKER Rik (173)| Art60§7 job
supplyment#14 (Rik RADERMECKER)|  _Evaluation_|  ▽  **? Suggested** →  ☼  ☑  ☒
Évaluation 14 (19.05.2014 09:00) with JEANÉMART Jérôme (181)| ISIP#32 (Jérôme
JEANÉMART)|  _Evaluation_|  ▽  **? Suggested** →  ☼  ☑  ☒
<BLANKLINE>
## My Notification messages ✓ ⏏
<BLANKLINE>
  * ✓ 22/05/2014 05:48 Die Datenbank wurde initialisiert.
<BLANKLINE>
<BLANKLINE>
