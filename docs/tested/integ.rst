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
>>> print(res.status_code)
200

We test whether a normal JSON response arrived:
>>> print(res.content)  #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE







