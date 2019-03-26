.. doctest docs/specs/coachings.rst
.. _welfare.specs.coachings:

===============
Coachings
===============

.. doctest init:

    >>> from lino import startup
    >>> startup('lino_welfare.projects.gerd.settings.doctests')
    >>> from lino.api.doctest import *

.. contents::
   :depth: 2
   :local:



What is a coaching?
===================

A coaching without client is not valid:

>>> cli = rt.models.pcsw.Client.objects.get(id=120)
>>> Coaching = rt.models.coachings.Coaching
>>> Coaching().full_clean()  #doctest: +NORMALIZE_WHITESPACE +IGNORE_EXCEPTION_DETAIL +ELLIPSIS
Traceback (most recent call last):
...
ValidationError: {'client': [u'Dieses Feld darf nicht null sein.']}

A coaching without user is not very useful but theoretically possible:

>>> obj = Coaching(client=cli)
>>> print(obj)
Begleitung CHANTRAINE Marc (120*)

>>> obj.full_clean()  #doctest: +ELLIPSIS



      
ClientStates
============

The list of possible choices for the :attr:`Client.client_state` field.
Default configuration is as follows:

>>> rt.show('clients.ClientStates', language="de")
====== ========== =========== =============
 Wert   name       Text        Button text
------ ---------- ----------- -------------
 10     newcomer   Neuantrag
 20     refused    Abgelehnt
 30     coached    Begleitet
 50     former     Ehemalig
====== ========== =========== =============
<BLANKLINE>

>>> rt.show('clients.ClientStates', language="fr")
====== ========== ============ =============
 Wert   name       Text         Button text
------ ---------- ------------ -------------
 10     newcomer   Nouveau
 20     refused    Refusé
 30     coached    Accompagné
 50     former     Ancien
====== ========== ============ =============
<BLANKLINE>


Any person who asks to meet with an agent for consultation will be
registered into the database.  At the beginning the client is a
**newcomer**. When the client introduces an application for a specific
help, they can become **refused** or **coached**. When a coached
client has no more active coaching, or when a newcomer does not come
back after their first visit, then somebody with appropriate rights
should mark the client as **former**.


>>> from lino_xl.lib.coachings.roles import CoachingsStaff
>>> username = 'rolf'
>>> rt.login(username).user.user_type.has_required_roles([CoachingsStaff])
True

>>> from lino_xl.lib.clients.choicelists import ClientStates

>>> list(ClientStates.required_roles)
[<class 'lino_xl.lib.contacts.roles.ContactsStaff'>]

>>> url = 'api/clients/ClientStates'
>>> url = settings.SITE.buildurl(url, fmt='json')
>>> test_client.force_login(rt.login(username).user)
>>> response = test_client.get(url, REMOTE_USER=username)
>>> result = check_json_result(response, None, "GET %s for user %s" % (url, username))
>>> result['count']
4


