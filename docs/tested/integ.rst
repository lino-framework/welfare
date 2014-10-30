.. _welfare.tested.integ:

Integration Service
===================

.. include:: /include/tested.rst

.. How to test only this document:
  $ python setup.py test -s tests.DocsTests.test_integ


>>> from __future__ import print_function
>>> import os
>>> os.environ['DJANGO_SETTINGS_MODULE'] = \
...    'lino_welfare.projects.docs.settings.doctests'
>>> from lino.runtime import *
>>> from django.utils import translation
>>> from django.test import Client
>>> import json
>>> from bs4 import BeautifulSoup
>>> print(settings.SETTINGS_MODULE)
lino_welfare.projects.docs.settings.doctests
>>> ses = rt.login('robin')
>>> translation.activate('en')


UsersWithClients
----------------

>>> ses.show(integ.UsersWithClients)
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
==================== ============ =========== ======== ======= ========= ================= ================ ========
 Coach                Evaluation   Formation   Search   Work    Standby   Primary clients   Active clients   Total
-------------------- ------------ ----------- -------- ------- --------- ----------------- ---------------- --------
 Alicia Allmanns                   1           2        2       1         5                 6                6
 Hubert Huppertz      3            2           4        4       4         11                17               17
 Mélanie Mélard       4            3           3        2       2         10                14               14
 **Total (3 rows)**   **7**        **6**       **9**    **8**   **7**     **26**            **37**           **37**
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

The following verifies that :linoticket:`104` is solved.
Every contract potentially generates a series of calendar events for
evaluation meetings (according to the
:attr:`welfare.isip.ContractBase.exam_policy` field).

Let's pick up ISIP contract #1, written by Alicia for client Alfons

>>> obj = isip.Contract.objects.get(pk=1)
>>> print(obj)
ISIP#1 (Alfons Ausdemwald)
>>> print(obj.user.first_name)
Alicia

This contract was active in the following period:

>>> print(obj.applies_from)
2012-09-29
>>> print(obj.applies_until)
2013-08-07

This contract is an example of a special condition which in reality
arise quite often: the coach changes while the contract is still
active. In our example, Alicia handed this client over to Hubert on
March 8th, 2013:

>>> rt.show(pcsw.CoachingsByClient, obj.client)
==================== ========== ================= ========= ===================== ============================
 Coached from         until      Coach             Primary   Coaching type         Reason of termination
-------------------- ---------- ----------------- --------- --------------------- ----------------------------
 3/13/12              3/8/13     Alicia Allmanns   No        Integration service   Transfer to colleague
 3/8/13               10/24/13   Hubert Huppertz   No        Integration service   End of right on social aid
 10/24/13                        Mélanie Mélard    Yes       Integration service
 **Total (3 rows)**                                **1**
==================== ========== ================= ========= ===================== ============================
<BLANKLINE>

Lino nicely attributes the automatic evaluation events to the coach in
charge, depending on their date:

>>> ar = cal.EventsByController.request(master_instance=obj)
>>> events = ["%s (%s)" % (e.start_date, e.user.first_name) for e in ar]
>>> print(", ".join(events))
... #doctest: +NORMALIZE_WHITESPACE
2012-10-29 (Alicia), 2012-11-29 (Alicia), 2012-12-31 (Alicia),
2013-01-31 (Alicia), 2013-02-28 (Alicia), 2013-03-28 (Hubert),
2013-04-29 (Hubert), 2013-05-29 (Hubert), 2013-07-01 (Hubert),
2013-08-01 (Hubert)

The first 5 appointments are with Alicia, the next 5 with Hubert.
That's what we wanted.


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
javascript:Lino.households.Households.detail.run("ext-comp-1351",{ "record_id": 232 })


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

Let's automatize this trick:

>>> def check(uri, fieldname):
...     url = '/api/%s?fmt=json&an=detail' % uri
...     res = client.get(url, REMOTE_USER='rolf')
...     assert res.status_code == 200
...     d = json.loads(res.content)
...     return d['data'][fieldname]

>>> soup = BeautifulSoup(check('integ/Clients/179', 'MembersByPerson'))
>>> links = soup.find_all('a')
>>> len(links)
8

Assigning a coach to a newcomer
-------------------------------

Similar test for a newcomer


>>> obj = pcsw.Client.objects.get(pk=117)
>>> print(obj)
BASTIAENSEN Laurent (117)

>>> rt.show(newcomers.AvailableCoachesByClient, master_instance=obj)
====================== =============== ================= =============== ========== =========== =============== ===================
 Name                   Arbeitsablauf   Komplette Akten   Neue Klienten   Quote NZ   Belastung   Mehrbelastung   Mehrbelastung (%)
---------------------- --------------- ----------------- --------------- ---------- ----------- --------------- -------------------
 Alicia Allmanns                        10                1               100        10,         6,              100,00
 **Total (1 Zeilen)**                   **10**            **1**           **100**    **10,**     **6,**          **100,00**
====================== =============== ================= =============== ========== =========== =============== ===================
<BLANKLINE>

>>> url = '/api/newcomers/AvailableCoachesByClient?fmt=json&mt=58&mk=117'
>>> res = client.get(url, REMOTE_USER='rolf')
>>> assert res.status_code == 200
>>> d = json.loads(res.content)

The second cell of the first data row in the above table looks empty
here, but when rendered on screen it contains a call to
`newcomers.AvailableCoachesByClient.assign_coach`:

>>> html = d['rows'][0][1]
>>> soup = BeautifulSoup(html)
>>> print(soup.get_text(' ', strip=True))
... #doctest: +NORMALIZE_WHITESPACE +REPORT_CDIFF
Zuweisen

>>> links = soup.find_all('a')
>>> len(links)
1

The text of this action call is "Zuweisen":

>>> print(links[0].string)
Zuweisen

And the `status` of this call (the second argument to
:js:func:`Lino.WindowAction.run`) must include the `record_id` of the
user being assigned (6 in this case):

>>> print(links[0].get('href'))
... #doctest: +NORMALIZE_WHITESPACE +ELLIPSIS
javascript:Lino.newcomers.AvailableCoachesByClient.assign_coach.run(null,{
"record_id": 6, "field_values": { "notify_body": "BASTIAENSEN
Laurent (117) wird ab jetzt begleitet f\u00fcr Finanzielle Begleitung
durch Alicia Allmanns.", "notify_subject": "BASTIAENSEN Laurent (117)
zugewiesen zu Alicia Allmanns", "notify_silent": false },
"param_values": { "since": "22.04.2014", "for_clientHidden": null,
"for_client": null }, "base_params": { "mt": ..., "mk": 117 } })

This call is generated by :meth:`dd.Actor.workflow_buttons`, which
calls :meth:`rt.ActionRequest.action_button`. Which is where we had a
bug on :blogref:`20150515`.



Uploads by client
-----------------

The folowing example is for client # 177
>>> obj = pcsw.Client.objects.get(pk=177)
>>> print(obj)
BRECHT Bernd (177)

>>> soup = BeautifulSoup(check('pcsw/Clients/177', 'UploadsByClient'))
>>> print(soup.get_text())
... #doctest: +NORMALIZE_WHITESPACE
Personalausweis: Aufenthaltserlaubnis: Arbeitserlaubnis: 3Führerschein: 4Diplom: 

>>> links = soup.find_all('a')
>>> len(links)
5

>>> rt.modules.uploads.UploadsByClient._upload_area
<UploadAreas.general:90>

>>> print(links[0].get('href'))
... #doctest: +NORMALIZE_WHITESPACE +ELLIPSIS
javascript:Lino.uploads.UploadsByClient.insert.run(null,{ "data_record": { "phantom": true, "data": { "valid_until": null, "typeHidden": 1, "description": "", "disabled_actions": {  }, "userHidden": 3, "upload_area": "Uploads", "disable_editing": false, "upload_areaHidden": "90", "user": "Rolf Rompen", "file": "", "owner": "<a href=\"javascript:Lino.pcsw.Clients.detail.run(null,{ &quot;record_id&quot;: 177 })\">BRECHT Bernd (177)</a>", "disabled_fields": { "mimetype": true }, "type": "Personalausweis", "id": null }, "title": "Uploads von BRECHT Bernd (177)" }, "base_params": { "mt": ..., "mk": 177, "type_id": 1 } })

>>> print(links[2].get('href'))
... #doctest: +NORMALIZE_WHITESPACE +ELLIPSIS
javascript:Lino.uploads.Uploads.detail.run(null,{ "record_id": 3 })

>>> print(links[3].get('href'))
... #doctest: +NORMALIZE_WHITESPACE +ELLIPSIS
javascript:Lino.uploads.Uploads.detail.run(null,{ "record_id": 4 })
