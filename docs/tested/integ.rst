.. _welfare.tested.integ:

Integration Service
===================

.. include:: /include/tested.rst

.. How to test only this document:
  $ python setup.py test -s tests.DocsTests.test_integ

..  
    >>> from __future__ import print_function
    >>> import os
    >>> os.environ['DJANGO_SETTINGS_MODULE'] = \
    ...    'lino_welfare.projects.docs.settings.test'
    >>> from lino.runtime import *
    >>> from django.utils import translation
    >>> from django.test import Client
    >>> import json
    >>> from bs4 import BeautifulSoup

>>> print(settings.SETTINGS_MODULE)
lino_welfare.projects.docs.settings.test

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

>>> print(pcsw.Client.objects.get(last_name="Keller", first_name="Karl"))
KELLER Karl (177)

>>> client = Client()
>>> url = '/api/integ/Clients/177?pv=30&pv=5&pv=&pv=29.04.2014&pv=29.04.2014&pv=&pv=&pv=&pv=&pv=&pv=false&pv=&pv=&pv=1&pv=false&pv=false&an=detail&rp=ext-comp-1351&fmt=json'
>>> res = client.get(url, REMOTE_USER='rolf')

This returns a huge JSON structure:

>>> print(res.status_code)
200
>>> d = json.loads(res.content)

We test the MembersByPerson panel. It contains a summary:

>>> print(d['data']['MembersByPerson'])
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +SKIP
<div>KELLER Karl (177) ist<ul><li>Vorstand in <a href="javascript:Lino.households.Households.detail.run(&quot;ext-comp-1351&quot;,{ &quot;record_id&quot;: 184 })">Legale Wohngemeinschaft Keller-&#213;unapuu</a></li></ul><br /><a href="javascript:Lino.contacts.Persons.create_household.run(&quot;ext-comp-1351&quot;,{ &quot;record_id&quot;: 177, &quot;field_values&quot;: { &quot;head&quot;: &quot;KELLER Karl (177)&quot;, &quot;headHidden&quot;: 177, &quot;typeHidden&quot;: null, &quot;partner&quot;: null, &quot;partnerHidden&quot;: null, &quot;type&quot;: null }, &quot;param_values&quot;: { &quot;observed_event&quot;: null, &quot;and_coached_by&quot;: null, &quot;end_date&quot;: null, &quot;genderHidden&quot;: null, &quot;also_obsolete&quot;: false, &quot;gender&quot;: null, &quot;nationalityHidden&quot;: null, &quot;aged_from&quot;: null, &quot;only_primary&quot;: false, &quot;client_stateHidden&quot;: &quot;30&quot;, &quot;and_coached_byHidden&quot;: null, &quot;coached_by&quot;: null, &quot;coached_byHidden&quot;: null, &quot;observed_eventHidden&quot;: null, &quot;nationality&quot;: null, &quot;client_state&quot;: &quot;Begleitet&quot;, &quot;start_date&quot;: null, &quot;aged_to&quot;: null }, &quot;base_params&quot;: {  } })">Haushalt erstellen</a></div>

Since this is not very human-readable, we are going to analyze it with
`BeautifulSoup <http://beautiful-soup-4.readthedocs.org/en/latest>`_.


>>> soup = BeautifulSoup(d['data']['MembersByPerson'])

>>> print(soup.get_text(' ', strip=True))
... #doctest: +NORMALIZE_WHITESPACE +REPORT_CDIFF

>>> links = soup.find_all('a')

It contains eight links:

>>> len(links)
6

The first link is the disabled checkbox for the :attr:`primary
<ml.households.Member.primary>` field:

>>> print(links[0].string)
... #doctest: +NORMALIZE_WHITESPACE
☐


>>> print(links[0].get('href'))
javascript:Lino.households.Members.set_primary("ext-comp-1351",7,{  })
>>> print(links[1].get('href'))
javascript:Lino.households.Households.detail.run("ext-comp-1351",{ "record_id": 230 })
>>> print(links[1].string)
Karl & Õie Keller-Õunapuu

>>> print(links[2].string)
Ehepartner

>>> print(links[2].get('href'))
... #doctest: +NORMALIZE_WHITESPACE +ELLIPSIS
javascript:Lino.pcsw.Clients.create_household.run("ext-comp-1351",{
"field_values": { 
  "head": "KELLER Karl (177)",
  "headHidden": 177, "typeHidden": 1, "partner": null,
  "partnerHidden": null, "type": "Ehepartner" }, 
"param_values": {
  "observed_event": null, "and_coached_by": null, "end_date": null,
  "genderHidden": null, "also_obsolete": false, "gender": null,
  "nationalityHidden": null, "aged_from": null, "only_primary": false,
  "client_stateHidden": "30", "and_coached_byHidden": null,
  "coached_by": null, "coached_byHidden": null, 
  "observed_eventHidden": null, "nationality": null, 
  "client_state": "Begleitet", "start_date": null, "aged_to": null }, 
"base_params": { } 
})

Let's automatize this trick:

>>> def check(uri, fieldname):
...     url = '/api/%s?fmt=json&an=detail' % uri
...     res = client.get(url, REMOTE_USER='rolf')
...     assert res.status_code == 200
...     d = json.loads(res.content)
...     return d['data'][fieldname]

>>> soup = BeautifulSoup(check('integ/Clients/177', 'MembersByPerson'))
>>> links = soup.find_all('a')
>>> len(links)
8

.. _paulfrisch:

Paul Frisch
-----------

Mr. Paul Frisch is a fictive client for which the demo database
contains fictive family links. His client id is 196.

>>> print(pcsw.Client.objects.get(first_name="Paul", last_name="Frisch"))
FRISCH Paul (235)

>>> soup = BeautifulSoup(check('integ/Clients/235', 'LinksByHuman'))
>>> links = soup.find_all('a')
>>> len(links)
14

>>> print(links[1].get('href'))
... #doctest: +NORMALIZE_WHITESPACE
javascript:Lino.pcsw.Clients.detail.run(null,{ "record_id": 243 })

These are the family relationships of Paul Frisch:

>>> print(soup.get_text(' ', strip=True))
... #doctest: +NORMALIZE_WHITESPACE +REPORT_CDIFF
Paul ist Vater von Dennis (12 Jahre) Vater von Clara (14 Jahre) Vater
von Philippe (16 Jahre) Vater von Peter (26 Jahre) Ehemann von Petra
ZWEITH (45 Jahre) Sohn von Gaby FROGEMUTH (79 Jahre) Sohn von Hubert
(80 Jahre) Beziehung erstellen als Vater / Sohn Adoptivvater /
Adoptivsohn Ehemann Verwandter Sonstiger

>>> url = '/api/newcomers/AvailableCoachesByClient?fmt=json&mt=58&mk=116'
>>> res = client.get(url, REMOTE_USER='rolf')
>>> assert res.status_code == 200
>>> d = json.loads(res.content)

The second cell of the first row contains one call to
`newcomers.AvailableCoachesByClient.assign_coach`:

>>> html = d['rows'][0][1]
>>> soup = BeautifulSoup(html)
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
Laurent (116) wird ab jetzt begleitet f\u00fcr Finanzielle Begleitung
durch Alicia Allmanns.", "notify_subject": "BASTIAENSEN Laurent (116)
zugewiesen zu Alicia Allmanns", "notify_silent": false },
"param_values": { "since": "22.04.2014", "for_clientHidden": null,
"for_client": null }, "base_params": { "mt": ..., "mk": 116 } })

This call is generated by :meth:`dd.Actor.workflow_buttons`, which
calls :meth:`rt.ActionRequest.action_button`. Which is where we had a
bug on :blogref:`20150515`.


>>> soup = BeautifulSoup(check('pcsw/Clients/176', 'UploadsByClient'))
>>> print(soup.get_text())
... #doctest: +NORMALIZE_WHITESPACE
Personalausweis: Aufenthaltserlaubnis: Arbeitserlaubnis: 3Führerschein: 4Diploma:

>>> links = soup.find_all('a')
>>> len(links)
5

>>> rt.modules.uploads.UploadsByClient._upload_area
<UploadAreas.general:90>

>>> print(links[0].get('href'))
... #doctest: +NORMALIZE_WHITESPACE +ELLIPSIS
javascript:Lino.uploads.UploadsByClient.insert.run(null,{ "data_record": { "phantom": true, "data": { "valid_until": null, "typeHidden": 1, "description": "", "disabled_actions": {  }, "userHidden": 3, "upload_area": "Uploads", "disable_editing": false, "upload_areaHidden": "90", "user": "Rolf Rompen", "file": "", "owner": "<a href=\"javascript:Lino.pcsw.Clients.detail.run(null,{ &quot;record_id&quot;: 176 })\">BRECHT Bernd (176)</a>", "disabled_fields": { "mimetype": true }, "type": "Personalausweis", "id": null }, "title": "Uploads von BRECHT Bernd (176)" }, "base_params": { "mt": ..., "mk": 176, "type_id": 1 } })

>>> print(links[2].get('href'))
... #doctest: +NORMALIZE_WHITESPACE +ELLIPSIS
javascript:Lino.uploads.Uploads.detail.run(null,{ "record_id": 3 })

>>> print(links[3].get('href'))
... #doctest: +NORMALIZE_WHITESPACE +ELLIPSIS
javascript:Lino.uploads.Uploads.detail.run(null,{ "record_id": 4 })
