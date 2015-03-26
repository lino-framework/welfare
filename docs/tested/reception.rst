.. _welfare.tested.reception:

===================
Reception
===================

.. How to test only this document:

  $ python setup.py test -s tests.DocsTests.test_reception

A technical tour into the :mod:`lino_welfare.modlib.reception` module.

.. contents::
   :depth: 2

A tested document
=================

This document is part of the Lino Welfare test suite and has been
tested using doctest with the following initialization code:

>>> from __future__ import print_function
>>> import os
>>> os.environ['DJANGO_SETTINGS_MODULE'] = \
...    'lino_welfare.projects.eupen.settings.doctests'
>>> from lino.api.doctest import *

>>> translation.activate('fr')

.. _welfare.tested.reception.AppointmentsByPartner:

AppointmentsByPartner
=====================

>>> obj = pcsw.Client.objects.get(pk=127)
>>> print(obj)
EVERS Eberhart (127)

This client has the following appointments. 

>>> rt.login('romain').show(reception.AppointmentsByPartner, obj,
...     column_names="event__start_date event__start_time event__user event__summary workflow_buttons",
...     language="en")
============ ============ ================ ================ =============================================
 Start date   Start time   Managed by       Summary          Workflow
------------ ------------ ---------------- ---------------- ---------------------------------------------
 5/22/14                   Mélanie Mélard   Urgent problem   **Waiting** → [Receive] [Checkout]
 5/23/14      09:40:00     Rolf Rompen      Erstgespräch     **Accepted** → [Excused] [Absent] [Checkin]
============ ============ ================ ================ =============================================
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

Client #127 is `ClientStates.coached` and has two coachings:

>>> obj = pcsw.Client.objects.get(pk=127)
>>> print(obj)
EVERS Eberhart (127)
>>> print(obj.client_state)
coached
>>> rt.login('romain').show(reception.AgentsByClient, obj, language='en')
================= =============== =========================
 Coach             Coaching type   Actions
----------------- --------------- -------------------------
 Hubert Huppertz   General         **Visit** **Find date**
 Caroline Carnol   Integ           **Visit** **Find date**
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
>>> rt.login('romain').show(reception.AgentsByClient, obj, language='en')
================= =============== =========================
 Coach             Coaching type   Actions
----------------- --------------- -------------------------
 Alicia Allmanns   Integ           **Visit** **Find date**
 Caroline Carnol   General         **Visit** **Find date**
 Hubert Huppertz   None            **Visit**
 Judith Jousten    General         **Visit** **Find date**
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


Some tables
===========

In the following tables we remove some columns which are not relevant
here. Here we define the keyword arguments we are going to pass to the
:meth:`show <lino.core.requests.BaseRequest.show>` method:

>>> kwargs = dict(language="en")
>>> kwargs.update(column_names="client position workflow_buttons")

Social workers can see on their computer who is waiting for them in
the lounge:

>>> rt.login('alicia').show(reception.MyWaitingVisitors, **kwargs)
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE -REPORT_UDIFF
========================= ========== ====================================
 Client                    Position   Workflow
------------------------- ---------- ------------------------------------
 HILGERS Hildegard (133)   1          **Waiting** → [Receive] [Checkout]
 KAIVERS Karl (141)        2          **Waiting** → [Receive] [Checkout]
========================= ========== ====================================
<BLANKLINE>

>>> rt.login('hubert').show(reception.MyWaitingVisitors, **kwargs)
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE -REPORT_UDIFF
===================== ========== ====================================
 Client                Position   Workflow
--------------------- ---------- ------------------------------------
 EMONTS Daniel (128)   1          **Waiting** → [Receive] [Checkout]
 JONAS Josef (139)     2          **Waiting** → [Receive] [Checkout]
 LAZARUS Line (144)    3          **Waiting** → [Receive] [Checkout]
===================== ========== ====================================
<BLANKLINE>

Theresia is the reception clerk. She has no visitors on her own.

>>> rt.login('theresia').show(reception.MyWaitingVisitors, **kwargs)
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE -REPORT_UDIFF
<BLANKLINE>
No data to display
<BLANKLINE>

Theresia is rather going to use the overview tables:

>>> kwargs.update(column_names="client event__user workflow_buttons")
>>> rt.login('theresia').show(reception.WaitingVisitors, **kwargs)
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE -REPORT_UDIFF
========================= ================= ====================================
 Client                    Managed by        Workflow
------------------------- ----------------- ------------------------------------
 EMONTS Daniel (128)       Hubert Huppertz   **Waiting** → [Receive] [Checkout]
 EVERS Eberhart (127)      Mélanie Mélard    **Waiting** → [Receive] [Checkout]
 HILGERS Hildegard (133)   Alicia Allmanns   **Waiting** → [Receive] [Checkout]
 JACOBS Jacqueline (137)   Judith Jousten    **Waiting** → [Receive] [Checkout]
 JONAS Josef (139)         Hubert Huppertz   **Waiting** → [Receive] [Checkout]
 KAIVERS Karl (141)        Alicia Allmanns   **Waiting** → [Receive] [Checkout]
 LAMBERTZ Guido (142)      Mélanie Mélard    **Waiting** → [Receive] [Checkout]
 LAZARUS Line (144)        Hubert Huppertz   **Waiting** → [Receive] [Checkout]
========================= ================= ====================================
<BLANKLINE>

>>> rt.login('theresia').show(reception.BusyVisitors, **kwargs)
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE -REPORT_UDIFF
========================= ================= =======================
 Client                    Managed by        Workflow
------------------------- ----------------- -----------------------
 BRECHT Bernd (177)        Hubert Huppertz   **Busy** → [Checkout]
 COLLARD Charlotte (118)   Alicia Allmanns   **Busy** → [Checkout]
 DUBOIS Robin (179)        Mélanie Mélard    **Busy** → [Checkout]
 ENGELS Edgar (129)        Judith Jousten    **Busy** → [Checkout]
========================= ================= =======================
<BLANKLINE>


>>> rt.login('theresia').show(reception.GoneVisitors, **kwargs)
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE -REPORT_UDIFF
============================ ================= ==========
 Client                       Managed by        Workflow
---------------------------- ----------------- ----------
 MALMENDIER Marc (146)        Alicia Allmanns   **Gone**
 KELLER Karl (178)            Judith Jousten    **Gone**
 JEANÉMART Jérôme (181)       Mélanie Mélard    **Gone**
 GROTECLAES Gregory (132)     Hubert Huppertz   **Gone**
 EMONTS-GAST Erna (152)       Alicia Allmanns   **Gone**
 DOBBELSTEIN Dorothée (124)   Judith Jousten    **Gone**
 AUSDEMWALD Alfons (116)      Mélanie Mélard    **Gone**
============================ ================= ==========
<BLANKLINE>



