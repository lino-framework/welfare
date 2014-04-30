.. _welfare.tested.integ:

Integration Service
===================

.. include:: /include/tested.rst

Some tests:
  
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
<div>KELLER Karl (177) ist<ul><li>Oberhaupt in <a href="javascript:Lino.households.Households.detail.run(&quot;ext-comp-1351&quot;,{ &quot;record_id&quot;: 184 })">Legale Wohngemeinschaft Keller-&#213;unapuu</a></li></ul><br /><a href="javascript:Lino.contacts.Persons.create_household.run(&quot;ext-comp-1351&quot;,{ &quot;record_id&quot;: 177, &quot;field_values&quot;: { &quot;head&quot;: &quot;KELLER Karl (177)&quot;, &quot;headHidden&quot;: 177, &quot;typeHidden&quot;: null, &quot;partner&quot;: null, &quot;partnerHidden&quot;: null, &quot;type&quot;: null }, &quot;param_values&quot;: { &quot;observed_event&quot;: null, &quot;and_coached_by&quot;: null, &quot;end_date&quot;: null, &quot;genderHidden&quot;: null, &quot;also_obsolete&quot;: false, &quot;gender&quot;: null, &quot;nationalityHidden&quot;: null, &quot;aged_from&quot;: null, &quot;only_primary&quot;: false, &quot;client_stateHidden&quot;: &quot;30&quot;, &quot;and_coached_byHidden&quot;: null, &quot;coached_by&quot;: null, &quot;coached_byHidden&quot;: null, &quot;observed_eventHidden&quot;: null, &quot;nationality&quot;: null, &quot;client_state&quot;: &quot;Begleitet&quot;, &quot;start_date&quot;: null, &quot;aged_to&quot;: null }, &quot;base_params&quot;: {  } })">Haushalt erstellen</a></div>

Since this is not very human-readable, we are going to parse it using
BeautifulSoup:

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


