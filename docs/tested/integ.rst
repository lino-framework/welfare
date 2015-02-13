.. _welfare.tested.integ:

===================
Integration Service
===================

.. How to test only this document:
  $ python setup.py test -s tests.DocsTests.test_integ

A technical tour into the :mod:`lino_welfare.modlib.integ` module.

.. contents::
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

>>> ses.show(isip.ExamPolicies)
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE -REPORT_UDIFF
==================== ========================= ====================
 Designation          Designation (fr)          Designation (de)
-------------------- ------------------------- --------------------
 every month          mensuel                   monatlich
 every 2 months       bimensuel                 zweimonatlich
 every 3 months       tous les 3 mois           alle 3 Monate
 every 2 weeks        hebdomadaire              zweiwöchentlich
 Once after 10 days   Une fois après 10 jours   Once after 10 days
 Other                Autre                     Sonstige
==================== ========================= ====================
<BLANKLINE>

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
 Default       Default            Default
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
(and passed when it was fixed):

>>> url = 'http://127.0.0.1:8000/api/integ/UsersWithClients?an=as_pdf'
>>> res = client.get(url, REMOTE_USER='rolf')  #doctest: +SKIP
>>> print(res.status_code)  #doctest: +SKIP
200
>>> result = json.loads(res.content)  #doctest: +SKIP
>>> print(result)  #doctest: +SKIP
{u'open_url': u'/media/cache/appypdf/127.0.0.1/integ.UsersWithClients.pdf', u'success': True}




Coach changes while contract active
-----------------------------------

The following verifies that :linoticket:`104` is solved.  Every
contract potentially generates a series of calendar events for
evaluation meetings (according to the :attr:`exam_policy
<welfare.isip.ContractBase.exam_policy>` field).

But a special condition which in reality arises quite often is that
the coach changes while the contract is still active.  


TODO: we want to show that Lino attributes the automatic evaluation
events to the coach in charge, depending on their date.  But currently
there is no contract in our demo data which matches this specific
condition.


Display a list of demo contracts which meet this condition:

>>> print(settings.SITE.ignore_dates_before)
None
>>> print(str(settings.SITE.ignore_dates_after))
2019-05-22

List of coaches who ended at least one integration coaching:

>>> integ = pcsw.CoachingType.objects.filter(does_integ=True)
>>> l = []
>>> for u in users.User.objects.all():
...     qs = pcsw.Coaching.objects.filter(user=u,
...             type__in=integ, end_date__isnull=False)
...     if qs.count():
...         l.append("%s (%s)" % (u.username, qs[0].end_date))
>>> print(', '.join(l))
... #doctest: +ELLIPSIS -REPORT_UDIFF +NORMALIZE_WHITESPACE
alicia (2013-10-24), caroline (2014-03-23), hubert (2013-03-08), melanie (2013-10-24)

List of contracts (isip + jobs) whose client changed the coach during
application period:

>>> l = []
>>> qs1 = isip.Contract.objects.all()
>>> qs2 = jobs.Contract.objects.all()
>>> for obj in list(qs1) + list(qs2):
...     ar = cal.EventsByController.request(master_instance=obj)
...     names = set([e.user.username for e in ar])
...     if len(names) > 1:
...         l.append(unicode(obj))
>>> print(len(l))
4
>>> print(', '.join(l))
... #doctest: +ELLIPSIS -REPORT_UDIFF +NORMALIZE_WHITESPACE
ISIP#21 (Hedi RADERMACHER), Art60§7 job supplyment#9 (Karl KAIVERS), Art60§7 job supplyment#11 (Melissa MEESSEN), Art60§7 job supplyment#16 (Vincent VAN VEEN)

Let's pick up ISIP contract #21:

>>> obj = isip.Contract.objects.get(pk=21)

This contract was created by Alicia (without any coaching), and on
2013-11-10 Caroline started to coach this client:

>>> print(obj.user.username)
alicia
>>> rt.show(pcsw.CoachingsByClient, obj.client)
==================== ======= ================= ========= =============== =======================
 Coached from         until   Coach             Primary   Coaching type   Reason of termination
-------------------- ------- ----------------- --------- --------------- -----------------------
 10/11/13                     Caroline Carnol   Yes       General
 10/14/13                     Hubert Huppertz   No        Integ
 **Total (2 rows)**                             **1**
==================== ======= ================= ========= =============== =======================
<BLANKLINE>

Lino attributes the automatic evaluation events to the coach in
charge, depending on their date.

>>> ar = cal.EventsByController.request(master_instance=obj)
>>> events = ["%s (%s)" % (e.start_date, e.user.first_name) for e in ar]
>>> print(", ".join(events))
... #doctest: +NORMALIZE_WHITESPACE
2013-03-18 (Alicia), 2013-04-18 (Alicia), 2013-05-20 (Alicia),
2013-06-20 (Alicia), 2013-07-22 (Alicia), 2013-08-22 (Alicia),
2013-09-23 (Alicia), 2013-10-23 (Caroline), 2013-11-25 (Caroline),
2013-12-25 (Caroline), 2014-01-27 (Caroline), 2014-02-27 (Caroline),
2014-03-27 (Caroline), 2014-04-28 (Caroline), 2014-05-28 (Caroline)

Note that appointments before 2013-11-10 are with Alicia, later
appointments are with Caroline.  That's what we wanted.


Expects a list of 12 values but got 16
--------------------------------------

The following code caused an Exception "ParameterStore of LayoutHandle
for ParamsLayout on pcsw.Clients expects a list of 12 values but got
16" on :blogref:`20140429`.

>>> print(pcsw.Client.objects.get(pk=179))
DUBOIS Robin (179)

>>> client = Client()
>>> url = '/api/integ/Clients/179?pv=30&pv=5&pv=&pv=29.04.2014&pv=29.04.2014&pv=&pv=&pv=&pv=&pv=&pv=false&pv=&pv=&pv=1&pv=false&pv=false&an=detail&rp=ext-comp-1351&fmt=json'
>>> res = client.get(url, REMOTE_USER='rolf')
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

