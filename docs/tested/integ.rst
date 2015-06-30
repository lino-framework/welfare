.. _welfare.tested.integ:

===================
Integration Service
===================

.. How to test only this document:

  $ python setup.py test -s tests.DocsTests.test_integ

A technical tour into the :mod:`lino_welfare.modlib.integ` module.
See also :doc:`/tour/autoevents`.

.. contents::
   :local:
   :depth: 2

.. include:: /include/tested.rst


>>> from __future__ import print_function
>>> import os
>>> os.environ['DJANGO_SETTINGS_MODULE'] = \
...    'lino_welfare.projects.std.settings.doctests'
>>> from lino.api.doctest import *

>>> ses = rt.login('robin')
>>> translation.activate('en')


Configuration
=============

>>> ses.show(isip.ContractTypes)
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE -REPORT_UDIFF
===================== ===================== ===================== =========== ==================== ==================
 Designation           Designation (fr)      Designation (de)      Reference   Examination Policy   needs Study type
--------------------- --------------------- --------------------- ----------- -------------------- ------------------
 VSE Ausbildung        VSE Ausbildung        VSE Ausbildung        vsea        every month          Yes
 VSE Arbeitssuche      VSE Arbeitssuche      VSE Arbeitssuche      vseb        every month          No
 VSE Lehre             VSE Lehre             VSE Lehre             vsec        every month          No
 VSE Vollzeitstudium   VSE Vollzeitstudium   VSE Vollzeitstudium   vsed        every month          Yes
 VSE Sprachkurs        VSE Sprachkurs        VSE Sprachkurs        vsee        every month          No
 **Total (5 rows)**                                                                                 **2**
===================== ===================== ===================== =========== ==================== ==================
<BLANKLINE>


>>> ses.show(isip.ContractEndings)
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE -REPORT_UDIFF
==================== ======= =============== ========= ====================
 designation          ISIP    Job supplying   Success   Require date ended
-------------------- ------- --------------- --------- --------------------
 Alcohol              Yes     Yes             No        Yes
 Force majeure        Yes     Yes             No        Yes
 Health               Yes     Yes             No        Yes
 Normal               Yes     Yes             No        No
 **Total (4 rows)**   **4**   **4**           **0**     **3**
==================== ======= =============== ========= ====================
<BLANKLINE>


>>> ses.show(jobs.Schedules)
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE -REPORT_UDIFF
==== =========================== ========================= ===========================
 ID   Designation                 Designation (fr)          Designation (de)
---- --------------------------- ------------------------- ---------------------------
 1    5 days/week                 5 jours/semaine           5-Tage-Woche
 2    Individual                  individuel                Individuell
 3    Monday, Wednesday, Friday   lundi,mercredi,vendredi   Montag, Mittwoch, Freitag
==== =========================== ========================= ===========================
<BLANKLINE>

>>> ses.show(jobs.ContractTypes)
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE -REPORT_UDIFF
============================ =========================== =========================== ===========
 Designation                  Designation (fr)            Designation (de)            Reference
---------------------------- --------------------------- --------------------------- -----------
 social economy               économie sociale            Sozialökonomie              art60-7a
 social economy - increased   économie sociale - majoré   Sozialökonomie - majoré     art60-7b
 social economy school        avec remboursement école    mit Rückerstattung Schule   art60-7d
 social economy with refund   avec remboursement          mit Rückerstattung          art60-7c
 town                         ville d'Eupen               Stadt Eupen                 art60-7e
============================ =========================== =========================== ===========
<BLANKLINE>

>>> ses.show(art61.ContractTypes)
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE -REPORT_UDIFF
============= ================== ================== ===========
 Designation   Designation (fr)   Designation (de)   Reference
------------- ------------------ ------------------ -----------
 Default       Default            Standardwert
============= ================== ================== ===========
<BLANKLINE>

>>> ses.show(immersion.ContractTypes)
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE -REPORT_UDIFF
===================== =========================== =====================
 Designation           Designation (fr)            Designation (de)
--------------------- --------------------------- ---------------------
 Immersion training    Stage d'immersion           Immersion training
 Internal engagement   Mise en situation interne   Internal engagement
 MISIP                 MISIP                       MISIP
===================== =========================== =====================
<BLANKLINE>

>>> ses.show(jobs.JobTypes)
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE -REPORT_UDIFF
======= ========= ================================================ ======== ================
 ID      Seq.No.   Designation                                      Remark   Social economy
------- --------- ------------------------------------------------ -------- ----------------
 4       4         Extern (Privat Kostenrückerstattung)                      No
 3       3         Extern (Öffentl. VoE mit Kostenrückerstattung)            No
 2       2         Intern                                                    No
 5       5         Sonstige                                                  No
 1       1         Sozialwirtschaft = "majorés"                              No
 **0**   **15**                                                              **0**
======= ========= ================================================ ======== ================
<BLANKLINE>



UsersWithClients
----------------

>>> ses.show(integ.UsersWithClients)
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE -REPORT_UDIFF
==================== ============ =========== ======== ======= ========= ================= ================ ========
 Coach                Evaluation   Formation   Search   Work    Standby   Primary clients   Active clients   Total
-------------------- ------------ ----------- -------- ------- --------- ----------------- ---------------- --------
 Alicia Allmanns      **2**        **2**       **1**    **1**   **1**     **3**             **7**            **7**
 Hubert Huppertz      **3**        **5**       **6**    **3**   **2**     **11**            **19**           **19**
 Mélanie Mélard       **4**        **1**       **4**    **5**   **4**     **11**            **18**           **18**
 **Total (3 rows)**   **9**        **8**       **11**   **9**   **7**     **25**            **44**           **44**
==================== ============ =========== ======== ======= ========= ================= ================ ========
<BLANKLINE>


Printing UsersWithClients to pdf
--------------------------------

User problem report:

  | pdf-Dokument aus Startseite erstellen:
  | kommt leider nur ein leeres Dok-pdf bei raus auf den 30/09/2011 datiert

The following lines reproduced this problem 
and passed when it was fixed:

>>> url = 'http://127.0.0.1:8000/api/integ/UsersWithClients?an=as_pdf'
>>> res = test_client.get(url, REMOTE_USER='rolf')  #doctest: +SKIP
>>> print(res.status_code)  #doctest: +SKIP
200
>>> result = json.loads(res.content)  #doctest: +SKIP
>>> print(result)  #doctest: +SKIP
{u'open_url': u'/media/cache/appypdf/127.0.0.1/integ.UsersWithClients.pdf', u'success': True}



Expects a list of 12 values but got 16
--------------------------------------

The following code caused an Exception "ParameterStore of LayoutHandle
for ParamsLayout on pcsw.Clients expects a list of 12 values but got
16" on :blogref:`20140429`.

>>> print(pcsw.Client.objects.get(pk=179))
DUBOIS Robin (179)

>>> client = Client()
>>> url = '/api/integ/Clients/179?pv=30&pv=5&pv=&pv=29.04.2014&pv=29.04.2014&pv=&pv=&pv=&pv=&pv=&pv=false&pv=&pv=&pv=1&pv=false&pv=false&an=detail&rp=ext-comp-1351&fmt=json'
>>> res = test_client.get(url, REMOTE_USER='rolf')
>>> print(res.status_code)
200

The response to this AJAX request is in JSON:

>>> d = json.loads(res.content)

We test the MembersByPerson panel. It contains a summary:

>>> print(d['data']['MembersByPerson'])
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
<div>DUBOIS Robin (179) ist<ul><li><a href="javascript:Lino.households.Members.set_primary(...)...</div>

Since this is not very human-readable, we are going to analyze it with
`BeautifulSoup <http://beautiful-soup-4.readthedocs.org/en/latest>`_.

>>> soup = BeautifulSoup(d['data']['MembersByPerson'])

>>> print(soup.get_text(' ', strip=True))
... #doctest: +NORMALIZE_WHITESPACE +REPORT_CDIFF
DUBOIS Robin (179) ist ☐ Vorstand in Robin & Mélanie Dubois-Mélard Haushalt erstellen : Ehepartner / Geschieden / Faktischer Haushalt / Legale Wohngemeinschaft / Getrennt / Sonstige

>>> links = soup.find_all('a')

It contains eight links:

>>> len(links)
8

The first link is the disabled checkbox for the :attr:`primary
<ml.households.Member.primary>` field:

>>> print(links[0].string)
... #doctest: +NORMALIZE_WHITESPACE
☐

Clicking on this would run the following JavaScript:

>>> print(links[0].get('href'))
javascript:Lino.households.Members.set_primary("ext-comp-1351",9,{  })

The next link is the name of the household, and clicking on it would
equally execute some Javascript code:

>>> print(links[1].string)
Robin & Mélanie Dubois-Mélard
>>> print(links[1].get('href'))
javascript:Lino.households.Households.detail.run("ext-comp-1351",{ "record_id": 234 })


The third link is:

>>> print(links[2].string)
Ehepartner
>>> print(links[2].get('href'))
... #doctest: +NORMALIZE_WHITESPACE +ELLIPSIS
javascript:Lino.contacts.Persons.create_household.run("ext-comp-1351",{
"field_values": { 
  "head": "DUBOIS Robin (179)", "headHidden": 179, 
  "typeHidden": 1, 
  "partner": null, "partnerHidden": null, 
  "type": "Ehepartner" 
}, "param_values": { 
  "also_obsolete": false, "gender": null, "genderHidden": null 
}, "base_params": {  } })


The :func:`lino.api.doctest.get_json_soup` automates this trick:

>>> soup = get_json_soup('rolf', 'integ/Clients/179', 'MembersByPerson')
>>> links = soup.find_all('a')
>>> len(links)
8

