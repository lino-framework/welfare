.. _welfare.tested.integ:

Integration Service
===================

.. include:: /include/tested.rst

.. How to test only this document:
  $ python setup.py test -s tests.DocsTests.test_integ

..  
    >>> from __future__ import print_function
    >>> from lino.runtime import *
    >>> from django.utils import translation
    >>> from django.test import Client
    >>> import json
    >>> from lino import dd


The following code caused an Exception "ParameterStore of LayoutHandle
for ParamsLayout on pcsw.Clients expects a list of 12 values but got
16" on :blogref:`20140429`.

>>> client = Client()
>>> url = '/api/integ/Clients/177?pv=30&pv=5&pv=&pv=29.04.2014&pv=29.04.2014&pv=&pv=&pv=&pv=&pv=&pv=false&pv=&pv=&pv=1&pv=false&pv=false&an=detail&rp=ext-comp-1351&fmt=json'
>>> res = client.get(url, REMOTE_USER='rolf')

This returns a huge JSON structure:

>>> print(res.status_code)
200
>>> d = json.loads(res.content)

We test the MembersByPerson panel. It contains a summary:

>>> print(d['data']['MembersByPerson'])
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
<div>KELLER Karl (177) ist<ul><li>Vorstand in <a href="javascript:Lino.households.Households.detail.run(&quot;ext-comp-1351&quot;,{ &quot;record_id&quot;: 184 })">Legale Wohngemeinschaft Keller-&#213;unapuu</a></li></ul><br /><a href="javascript:Lino.contacts.Persons.create_household.run(&quot;ext-comp-1351&quot;,{ &quot;record_id&quot;: 177, &quot;field_values&quot;: { &quot;head&quot;: &quot;KELLER Karl (177)&quot;, &quot;headHidden&quot;: 177, &quot;typeHidden&quot;: null, &quot;partner&quot;: null, &quot;partnerHidden&quot;: null, &quot;type&quot;: null }, &quot;param_values&quot;: { &quot;observed_event&quot;: null, &quot;and_coached_by&quot;: null, &quot;end_date&quot;: null, &quot;genderHidden&quot;: null, &quot;also_obsolete&quot;: false, &quot;gender&quot;: null, &quot;nationalityHidden&quot;: null, &quot;aged_from&quot;: null, &quot;only_primary&quot;: false, &quot;client_stateHidden&quot;: &quot;30&quot;, &quot;and_coached_byHidden&quot;: null, &quot;coached_by&quot;: null, &quot;coached_byHidden&quot;: null, &quot;observed_eventHidden&quot;: null, &quot;nationality&quot;: null, &quot;client_state&quot;: &quot;Begleitet&quot;, &quot;start_date&quot;: null, &quot;aged_to&quot;: null }, &quot;base_params&quot;: {  } })">Haushalt erstellen</a></div>

Since this is not very human-readable, we are going to analyze it with
`BeautifulSoup <http://beautiful-soup-4.readthedocs.org/en/latest>`_.


>>> from bs4 import BeautifulSoup
>>> soup = BeautifulSoup(d['data']['MembersByPerson'])
>>> links = soup.find_all('a')

It contains two links:

>>> len(links)
2
>>> print(links[0].get('href'))
javascript:Lino.households.Households.detail.run("ext-comp-1351",{ "record_id": 184 })
>>> print(links[0].string)
Legale Wohngemeinschaft Keller-Õunapuu

>>> print(links[1].string)
Haushalt erstellen

>>> print(links[1].get('href'))
... #doctest: +NORMALIZE_WHITESPACE
javascript:Lino.contacts.Persons.create_household.run("ext-comp-1351",{
"record_id": 177, 
"field_values": { 
  "head": "KELLER Karl (177)",
  "headHidden": 177, "typeHidden": null, "partner": null,
  "partnerHidden": null, "type": null }, 
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
2

>>> soup = BeautifulSoup(check('integ/Clients/195', 'LinksByHuman'))
>>> links = soup.find_all('a')
>>> len(links)
14

>>> print(links[1].get('href'))
... #doctest: +NORMALIZE_WHITESPACE
javascript:Lino.contacts.Persons.detail.run(null,{ "record_id": 203 })


>>> print(soup.get_text())
... #doctest: +NORMALIZE_WHITESPACE +SKIP
Paul istVater von Dennis Frisch (12 Jahre)Vater von Frau Clara Frisch (14 Jahre)Vater von Herr Philippe Frisch (16 Jahre)Vater von Herr Peter Frisch (26 Jahre)Ehemann von Frau Petra Zweith (45 Jahre)Sohn von Frau Gaby Frogemuth (79 Jahre)Sohn von Herr Hubert Frisch (80 Jahre)Beziehung erstellen als Vater/Sohn Adoptivvater/Adoptivsohn Verwandter Sonstige



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
"param_values": { "since": "...", "for_clientHidden": null,
"for_client": null }, "base_params": { "mt": 58, "mk": 116 } })

This call is generated by :meth:`dd.Actor.workflow_buttons`, which
calls :meth:`rt.ActionRequest.action_button`. Which is where we had a
bug on :blogref:`20150515`.

