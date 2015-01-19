.. _welfare.tested.reception:

===================
Reception
===================

.. include:: /include/tested.rst

.. How to test only this document:
  $ python setup.py test -s tests.DocsTests.test_reception


>>> from __future__ import print_function
>>> import os
>>> os.environ['DJANGO_SETTINGS_MODULE'] = \
...    'lino_welfare.projects.eupen.settings.doctests'
>>> from lino.runtime import *
>>> from django.utils import translation
>>> from django.test import Client
>>> import json
>>> from bs4 import BeautifulSoup
>>> print(settings.SETTINGS_MODULE)
lino_welfare.projects.eupen.settings.doctests

>>> ses = rt.login('romain')
>>> translation.activate('fr')


AppointmentsByPartner
=====================

>>> obj = pcsw.Client.objects.get(pk=127)
>>> print(obj)
EVERS Eberhart (127)
>>> print(obj.client_state)
coached

TODO: The following says "aucun enregistrement" ("no data to display")
because the permission is denied. It would be better to either write
"no permission".

>>> reception.AppointmentsByPartner.show(obj)
<BLANKLINE>
Aucun enregistrement
<BLANKLINE>

>>> ses = rt.login('romain')
>>> ses.show(reception.AppointmentsByPartner, obj)
================== ================ =====================================================
 Quand              Traité par       État
------------------ ---------------- -----------------------------------------------------
 **mai 22, 2014**   Mélanie Mélard   **Attend** → [Excusé] [Absent] [Reçevoir] [Quitter]
================== ================ =====================================================
<BLANKLINE>



AgentsByClient
==============

>>> ses.show(reception.AgentsByClient, obj)
================= ============================== ==========================
 Intervenant       Service                        Actions
----------------- ------------------------------ --------------------------
 Hubert Huppertz   SSG (Service social général)   **Visite** **Find date**
 Caroline Carnol   Service intégration            **Visite** **Find date**
================= ============================== ==========================
<BLANKLINE>

>>> client = Client()
>>> url = "/api/pcsw/Clients/{0}?_dc=1421645352616&pv=&pv=&pv=&pv=&pv=false&pv=30&pv=&pv=&pv=&pv=&pv=&pv=false&an=detail&rp=ext-comp-1268&fmt=json"
>>> url = url.format(obj.pk)

>>> res = client.get(url, REMOTE_USER='romain')
>>> print(res.status_code)
200

The response to this AJAX request is in JSON:

>>> d = json.loads(res.content)

We test the AgentsByClient panel. 

>>> chunk = d['data']['AgentsByClient']

It contains a table:

>>> print(chunk)
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
<table bgcolor="#ffffff" ...
src="/media/lino/extjs/images/mjames/calendar.png" /></a> </div></td></tr></tbody></table>

