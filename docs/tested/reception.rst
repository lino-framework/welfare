.. _welfare.tested.reception:

===================
Reception
===================

.. include:: /include/tested.rst

.. How to test only this document:

  $ python setup.py test -s tests.DocsTests.test_reception

.. 
    >>> from __future__ import print_function
    >>> import os
    >>> os.environ['DJANGO_SETTINGS_MODULE'] = \
    ...    'lino_welfare.projects.eupen.settings.doctests'
    >>> from lino.runtime import *
    >>> from django.utils import translation
    >>> from django.test import Client
    >>> import json
    >>> from bs4 import BeautifulSoup

This documents uses the :mod:`lino_welfare.projects.eupen` test
database:

>>> print(settings.SETTINGS_MODULE)
lino_welfare.projects.eupen.settings.doctests

>>> ses = rt.login('romain')
>>> translation.activate('fr')


AppointmentsByPartner
=====================

>>> obj = pcsw.Client.objects.get(pk=127)
>>> print(obj)
EVERS Eberhart (127)

This client has 3 appointments. The second and third are evaluations
led by Hubert with a client for whom she also has a coaching.

>>> ses = rt.login('romain')
>>> ses.show(reception.AppointmentsByPartner, obj)
=========================== ================= =====================================================
 Quand                       Traité par        État
--------------------------- ----------------- -----------------------------------------------------
 **mai 22, 2014**            Mélanie Mélard    **Attend** → [Excusé] [Absent] [Recevoir] [Quitter]
 **mai 5, 2014 at 09:00**    Hubert Huppertz   **Accepté** → [Excusé] [Absent] [Arriver]
 **juin 5, 2014 at 09:00**   Hubert Huppertz   **Accepté** → [Excusé] [Absent] [Arriver]
=========================== ================= =====================================================
<BLANKLINE>


TODO: Note that we had to log in to show the above table.  Not yet
sure whether this is correct. A simple show() says "aucun
enregistrement" ("no data to display") because the permission is
denied. It might be better to write "no permission" in that case. Or
to ignore any permission requirements here (since console scripts are
supposed to be run only by users who have root permissions).

>>> reception.AppointmentsByPartner.show(obj)
<BLANKLINE>
Aucun enregistrement
<BLANKLINE>



AgentsByClient
==============

>>> ses = rt.login('romain')

Client #127 is `ClientStates.coached` and has two coachings:

>>> obj = pcsw.Client.objects.get(pk=127)
>>> print(obj)
EVERS Eberhart (127)
>>> print(obj.client_state)
coached
>>> ses.show(reception.AgentsByClient, obj)
================= ============================== ==========================
 Intervenant       Service                        Actions
----------------- ------------------------------ --------------------------
 Hubert Huppertz   SSG (Service social général)   **Visite** **Find date**
 Caroline Carnol   Service intégration            **Visite** **Find date**
================= ============================== ==========================
<BLANKLINE>

Client 257 is not coached but a `ClientStates.newcomer`. So
AgentsByClient shows all users who care for newcomers (i.e. who have
:attr:`newcomer_consultations
<lino_welfare.modlib.users.User.newcomer_consultations>` set).

>>> obj = pcsw.Client.objects.get(pk=257)
>>> print(obj)
BRAUN Bruno (257)
>>> print(obj.client_state)
newcomer
>>> ses.show(reception.AgentsByClient, obj)
================= ============================== ==========================
 Intervenant       Service                        Actions
----------------- ------------------------------ --------------------------
 Alicia Allmanns   Service intégration            **Visite** **Find date**
 Caroline Carnol   SSG (Service social général)   **Visite** **Find date**
 Hubert Huppertz   None                           **Visite** **Find date**
 Judith Jousten    SSG (Service social général)   **Visite** **Find date**
 Mélanie Mélard    None                           **Visite** **Find date**
================= ============================== ==========================
<BLANKLINE>

(TODO: why do Hubert and Mélanie have no service defined?)



Now let's have a closer look at these action buttons.


>>> obj = pcsw.Client.objects.get(pk=127)
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

