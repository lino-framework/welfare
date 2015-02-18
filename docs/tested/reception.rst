.. _welfare.tested.reception:

===================
Reception
===================

.. How to test only this document:

  $ python setup.py test -s tests.DocsTests.test_reception


A technical tour into the :mod:`lino_welfare.modlib.reception` module.

.. include:: /include/tested.rst

.. contents::
   :depth: 2

About this document
===================

.. 
    >>> from __future__ import print_function
    >>> import os
    >>> os.environ['DJANGO_SETTINGS_MODULE'] = \
    ...    'lino_welfare.projects.eupen.settings.doctests'
    >>> from lino.api.doctest import *

This document uses the :mod:`lino_welfare.projects.eupen` test
database:

>>> print(settings.SETTINGS_MODULE)
lino_welfare.projects.eupen.settings.doctests

>>> ses = rt.login('romain')
>>> translation.activate('fr')

.. _welfare.tested.reception.AppointmentsByPartner:

AppointmentsByPartner
=====================

>>> obj = pcsw.Client.objects.get(pk=127)
>>> print(obj)
EVERS Eberhart (127)

This client has 3 appointments. The second and third are evaluations
led by Hubert with a client for whom she also has a coaching.

>>> ses = rt.login('romain')
>>> ses.show(reception.AppointmentsByPartner, obj)
============================ ================= ===========================================
 Quand                        Traité par        État
---------------------------- ----------------- -------------------------------------------
 **mai 5, 2014 at 09:00**     Hubert Huppertz   **Accepté** → [Excusé] [Absent] [Arriver]
 **mai 22, 2014**             Mélanie Mélard    **Attend** → [Recevoir] [Quitter]
 **juin 5, 2014 at 09:00**    Hubert Huppertz   **Accepté** → [Excusé] [Absent] [Arriver]
 **juil. 7, 2014 at 09:00**   Hubert Huppertz   **Accepté** → [Excusé] [Absent] [Arriver]
 **août 7, 2014 at 09:00**    Hubert Huppertz   **Accepté** → [Excusé] [Absent] [Arriver]
 **sep. 29, 2014 at 09:00**   Hubert Huppertz   **Accepté** → [Excusé] [Absent] [Arriver]
 **oct. 29, 2014 at 09:00**   Hubert Huppertz   **Accepté** → [Excusé] [Absent] [Arriver]
 **déc. 1, 2014 at 09:00**    Hubert Huppertz   **Accepté** → [Excusé] [Absent] [Arriver]
 **jan. 1, 2015 at 09:00**    Hubert Huppertz   **Accepté** → [Excusé] [Absent] [Arriver]
 **fév. 2, 2015 at 09:00**    Hubert Huppertz   **Accepté** → [Excusé] [Absent] [Arriver]
 **mars 2, 2015 at 09:00**    Hubert Huppertz   **Accepté** → [Excusé] [Absent] [Arriver]
 **avr. 2, 2015 at 09:00**    Hubert Huppertz   **Accepté** → [Excusé] [Absent] [Arriver]
 **mai 4, 2015 at 09:00**     Hubert Huppertz   **Accepté** → [Excusé] [Absent] [Arriver]
 **juin 4, 2015 at 09:00**    Hubert Huppertz   **Accepté** → [Excusé] [Absent] [Arriver]
 **juil. 6, 2015 at 09:00**   Hubert Huppertz   **Accepté** → [Excusé] [Absent] [Arriver]
 **août 6, 2015 at 09:00**    Hubert Huppertz   **Accepté** → [Excusé] [Absent] [Arriver]
============================ ================= ===========================================
<BLANKLINE>


TODO: Note that we had to log in to show the above table.  Not yet
sure whether this is correct. A simple show() says "aucun
enregistrement" ("no data to display") because the permission is
denied. It might be better to write "no permission" in that case. Or
to ignore any permission requirements here (since console scripts are
supposed to be run only by users who have root permissions).

>>> reception.AppointmentsByPartner.show(obj)  #doctest: +SKIP
<BLANKLINE>
Aucun enregistrement
<BLANKLINE>

.. _welfare.tested.reception.AgentsByClient:

AgentsByClient
==============

The :class:`AgentsByClient
<lino_welfare.modlib.reception.models.AgentsByClient>` table shows the
users for whom a reception clerk can make an appointment with a given
client. Per user you have two possible buttons: (1) a prompt
consultation (client will wait in the lounge until the user receives
them) or (2) a scheduled appointment in the user's calendar.

>>> ses = rt.login('romain')

Client #127 is `ClientStates.coached` and has two coachings:

>>> obj = pcsw.Client.objects.get(pk=127)
>>> print(obj)
EVERS Eberhart (127)
>>> print(obj.client_state)
coached
>>> ses.show(reception.AgentsByClient, obj, language='en')
================= =============== =========================
 Coach             Coaching type   Actions
----------------- --------------- -------------------------
 Hubert Huppertz   ASD             **Visit** **Find date**
 Caroline Carnol   DSBE            **Visit** **Find date**
================= =============== =========================
<BLANKLINE>

Client 257 is not coached but a `ClientStates.newcomer`. So
AgentsByClient shows all users who care for newcomers (i.e. who have a
non-zero :attr:`newcomer_quota
<lino_welfare.modlib.users.User.newcomer_quota>`).

>>> obj = pcsw.Client.objects.get(pk=257)
>>> print(obj)
BRAUN Bruno (257)
>>> print(obj.client_state)
newcomer
>>> ses.show(reception.AgentsByClient, obj, language='en')
================= =============== =========================
 Coach             Coaching type   Actions
----------------- --------------- -------------------------
 Alicia Allmanns   DSBE            **Visit** **Find date**
 Hubert Huppertz   None            **Visit** **Find date**
 Mélanie Mélard    None            **Visit** **Find date**
================= =============== =========================
<BLANKLINE>

TODO: For Hubert and Mélanie the "Service" column says "None" because
their `User.coaching_type` field are empty.  Why was this?


Now let's have a closer look at the action buttons in the third column
of above table.  This column is defined by a
:func:`lino.core.fields.displayfield`.

It has up to two actions (labeled `Create prompt event` and `Find
date`)

We are going to inspect the AgentsByClient panel.

>>> soup = get_json_soup('romain', 'pcsw/Clients/127', 'AgentsByClient')

It contains a table, and we want the cell at the first data row and
third column:

>>> td = soup.table.tbody.tr.contents[2]
>>> #print(td.div)
>>> #len(td.div.contents)

The first button ("Visit") is here:

>>> btn = td.div.contents[0]
>>> print(btn.contents)
[<img alt="hourglass" src="/media/lino/extjs/images/mjames/hourglass.png"/>]

And yes, the `href` attribute is a javascript snippet:

>>> print(btn['href'])
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
javascript:Lino.pcsw.Clients.create_visit.run(null,...)

Now let's inspect the three dots (`...`). 

>>> dots = btn['href'][51:-1]
>>> print(dots)  #doctest: +ELLIPSIS 
{ ... }

They are a big "object" (in Python we call it a `dict`):

>>> d = AttrDict(json.loads(dots))

It has 4 keys:

>>> d.keys()
[u'record_id', u'field_values', u'param_values', u'base_params']

>>> d.record_id
127
>>> d.base_params
{u'mk': 127}
>>> d.field_values
{u'userHidden': 5, u'user': u'Hubert Huppertz', u'summary': u''}

(This last line was right only since :blogref:`20150122`)

**Now the second action (Find date):**

The button is here:

>>> btn = td.div.contents[2]
>>> print(btn.contents)
[<img alt="calendar" src="/media/lino/extjs/images/mjames/calendar.png"/>]

And also here, the `href` attribute is a javascript snippet:

>>> print(btn['href'])
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
javascript:Lino.extensible.CalendarPanel.grid.run(null,{ "su": 5, "base_params": { "su": 5, "prj": 127 } })

This one is shorter, so we don't need to parse it for inspecting it.
Note that `su` (subst_user) is the id of the user whose calendar is to be displayed.
And `prj` will become the value of the `project` field if a new event would be created.
