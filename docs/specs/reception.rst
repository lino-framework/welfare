.. doctest docs/specs/reception.rst
.. _welfare.specs.reception:

===================
Reception
===================

..  doctest init:
   
    >>> from lino import startup
    >>> startup('lino_welfare.projects.eupen.settings.doctests')
    >>> from lino.api.doctest import *
    >>> translation.activate('fr')
    
A technical tour into the :mod:`lino_welfare.modlib.reception` module.

.. contents::
   :depth: 2


.. _welfare.specs.reception.AppointmentsByPartner:

AppointmentsByPartner
=====================

>>> obj = pcsw.Client.objects.get(pk=127)
>>> print(obj)
EVERS Eberhart (127)

This client has the following appointments. 

>>> rt.login('romain').show(reception.AppointmentsByPartner, obj,
...     column_names="event__start_date event__start_time event__user event__summary event__state workflow_buttons",
...     language="en")  #doctest: -REPORT_UDIFF
============ ============ ================== =================== ============ =======================================================
 Start date   Start time   Managed by         Short description   State        Workflow
------------ ------------ ------------------ ------------------- ------------ -------------------------------------------------------
 15/05/2014   09:00:00     Caroline Carnol    Auswertung 2        Suggested    [Checkin] **Accepted** → [Absent] [Excused]
 17/05/2014   10:20:00     Patrick Paraneau   Beratung            Took place   [Checkin] **Accepted** → [Present] [Absent] [Excused]
 22/05/2014                Mélanie Mélard     Urgent problem      Published    [Receive] [Checkout] **Waiting** → [Absent] [Excused]
 16/06/2014   09:00:00     Caroline Carnol    Auswertung 3        Suggested    [Checkin] **Accepted** → [Absent] [Excused]
 16/07/2014   09:00:00     Caroline Carnol    Auswertung 4        Suggested    [Checkin] **Accepted** → [Absent] [Excused]
 18/08/2014   09:00:00     Caroline Carnol    Auswertung 5        Suggested    [Checkin] **Accepted** → [Absent] [Excused]
 18/09/2014   09:00:00     Caroline Carnol    Auswertung 6        Suggested    [Checkin] **Accepted** → [Absent] [Excused]
 20/10/2014   09:00:00     Caroline Carnol    Auswertung 7        Suggested    [Checkin] **Accepted** → [Absent] [Excused]
 20/11/2014   09:00:00     Caroline Carnol    Auswertung 8        Suggested    [Checkin] **Accepted** → [Absent] [Excused]
 22/12/2014   09:00:00     Caroline Carnol    Auswertung 9        Suggested    [Checkin] **Accepted** → [Absent] [Excused]
============ ============ ================== =================== ============ =======================================================
<BLANKLINE>

Note that even Theresia who is a reception clerk and has no calendar
functionality can click on the dates to see their detail:

>>> rt.login('theresia').show(reception.AppointmentsByPartner, obj,
...     language="en")  #doctest: +REPORT_UDIFF
====================================== ================== =======================================================
 When                                   Managed by         Workflow
-------------------------------------- ------------------ -------------------------------------------------------
 `Thu 15/05/2014 at 09:00 <Detail>`__   Caroline Carnol    [Checkin] **Accepted** → [Absent] [Excused]
 `Sat 17/05/2014 at 10:20 <Detail>`__   Patrick Paraneau   [Checkin] **Accepted** → [Present] [Absent] [Excused]
 `Thu 22/05/2014 <Detail>`__            Mélanie Mélard     [Receive] [Checkout] **Waiting** → [Absent] [Excused]
 `Mon 16/06/2014 at 09:00 <Detail>`__   Caroline Carnol    [Checkin] **Accepted** → [Absent] [Excused]
 `Wed 16/07/2014 at 09:00 <Detail>`__   Caroline Carnol    [Checkin] **Accepted** → [Absent] [Excused]
 `Mon 18/08/2014 at 09:00 <Detail>`__   Caroline Carnol    [Checkin] **Accepted** → [Absent] [Excused]
 `Thu 18/09/2014 at 09:00 <Detail>`__   Caroline Carnol    [Checkin] **Accepted** → [Absent] [Excused]
 `Mon 20/10/2014 at 09:00 <Detail>`__   Caroline Carnol    [Checkin] **Accepted** → [Absent] [Excused]
 `Thu 20/11/2014 at 09:00 <Detail>`__   Caroline Carnol    [Checkin] **Accepted** → [Absent] [Excused]
 `Mon 22/12/2014 at 09:00 <Detail>`__   Caroline Carnol    [Checkin] **Accepted** → [Absent] [Excused]
====================================== ================== =======================================================
<BLANKLINE>




.. _welfare.specs.reception.AgentsByClient:

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
>>> obj.client_state
<ClientStates.coached:30>

>>> rt.login('romain').show(reception.AgentsByClient, obj, language='en')
================= =============== =========================
 Coach             Coaching type   Actions
----------------- --------------- -------------------------
 Hubert Huppertz   General         **Visit** **Find date**
 Caroline Carnol   Integ           **Visit** **Find date**
================= =============== =========================
<BLANKLINE>

Client 257 is a `ClientStates.newcomer` and *not* coached. In that
case Lino shows all social agents who care for newcomers (i.e. who
have a non-zero :attr:`newcomer_quota
<lino_welfare.modlib.users.User.newcomer_quota>`).


>>> obj = pcsw.Client.objects.get(first_name="Bruno", last_name="Braun")
>>> print(obj)
BRAUN Bruno (259)
>>> obj.client_state
<ClientStates.newcomer:10>

>>> rt.login('romain').show(reception.AgentsByClient, obj, language='en')
================= =============== =========================
 Coach             Coaching type   Actions
----------------- --------------- -------------------------
 Alicia Allmanns   Integ           **Visit** **Find date**
 Caroline Carnol   General         **Visit** **Find date**
 Hubert Huppertz   Integ           **Visit**
 Judith Jousten    General         **Visit** **Find date**
================= =============== =========================
<BLANKLINE>

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

The first button ("Visit") is here:

>>> btn = td.contents[0]
>>> print(btn.contents)
[<img alt="hourglass" src="/static/images/mjames/hourglass.png"/>]

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
>>> d.base_params['mt']
55
>>> d.base_params == {'mt': 55, 'mk': 127}
True

>>> d.field_values == {'userHidden': 5, 'user': 'Hubert Huppertz', 'summary': ''}
True

(This last line was right only since :blogref:`20150122`)

**Now the second action (Find date):**

The button is here:

>>> btn = td.contents[2]
>>> print(btn.contents)
[<img alt="calendar" src="/static/images/mjames/calendar.png"/>]

And also here, the `href` attribute is a javascript snippet:

>>> print(btn['href'])
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
javascript:Lino.extensible.CalendarPanel.grid.run(null,{ "base_params": { "prj": 127, "su": 5 }, "su": 5 })


This one is shorter, so we don't need to parse it for inspecting it.
Note that `su` (subst_user) is the id of the user whose calendar is to
be displayed.  And `prj` will become the value of the `project` field
if a new event would be created.



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
========================= ========== =======================================================
 Client                    Position   Workflow
------------------------- ---------- -------------------------------------------------------
 HILGERS Hildegard (133)   1          [Receive] [Checkout] **Waiting** → [Absent] [Excused]
 KAIVERS Karl (141)        2          [Receive] [Checkout] **Waiting** → [Absent] [Excused]
========================= ========== =======================================================
<BLANKLINE>

>>> rt.login('hubert').show(reception.MyWaitingVisitors, **kwargs)
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE -REPORT_UDIFF
===================== ========== =======================================================
 Client                Position   Workflow
--------------------- ---------- -------------------------------------------------------
 EMONTS Daniel (128)   1          [Receive] [Checkout] **Waiting** → [Absent] [Excused]
 JONAS Josef (139)     2          [Receive] [Checkout] **Waiting** → [Absent] [Excused]
 LAZARUS Line (144)    3          [Receive] [Checkout] **Waiting** → [Absent] [Excused]
===================== ========== =======================================================
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
========================= ================= =======================================================
 Client                    Managed by        Workflow
------------------------- ----------------- -------------------------------------------------------
 EMONTS Daniel (128)       Hubert Huppertz   [Receive] [Checkout] **Waiting** → [Absent] [Excused]
 EVERS Eberhart (127)      Mélanie Mélard    [Receive] [Checkout] **Waiting** → [Absent] [Excused]
 HILGERS Hildegard (133)   Alicia Allmanns   [Receive] [Checkout] **Waiting** → [Absent] [Excused]
 JACOBS Jacqueline (137)   Judith Jousten    [Receive] [Checkout] **Waiting** → [Absent] [Excused]
 JONAS Josef (139)         Hubert Huppertz   [Receive] [Checkout] **Waiting** → [Absent] [Excused]
 KAIVERS Karl (141)        Alicia Allmanns   [Receive] [Checkout] **Waiting** → [Absent] [Excused]
 LAMBERTZ Guido (142)      Mélanie Mélard    [Receive] [Checkout] **Waiting** → [Absent] [Excused]
 LAZARUS Line (144)        Hubert Huppertz   [Receive] [Checkout] **Waiting** → [Absent] [Excused]
========================= ================= =======================================================
<BLANKLINE>

>>> rt.login('theresia').show(reception.BusyVisitors, **kwargs)
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE -REPORT_UDIFF
========================= ================= ==========================================
 Client                    Managed by        Workflow
------------------------- ----------------- ------------------------------------------
 BRECHT Bernd (177)        Hubert Huppertz   [Checkout] **Busy** → [Absent] [Excused]
 COLLARD Charlotte (118)   Alicia Allmanns   [Checkout] **Busy** → [Absent] [Excused]
 DUBOIS Robin (179)        Mélanie Mélard    [Checkout] **Busy** → [Absent] [Excused]
 ENGELS Edgar (129)        Judith Jousten    [Checkout] **Busy** → [Absent] [Excused]
========================= ================= ==========================================
<BLANKLINE>


>>> rt.login('theresia').show(reception.GoneVisitors, **kwargs)
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE -REPORT_UDIFF
============================ ================= ===============================
 Client                       Managed by        Workflow
---------------------------- ----------------- -------------------------------
 MALMENDIER Marc (146)        Alicia Allmanns   **Gone** → [Absent] [Excused]
 KELLER Karl (178)            Judith Jousten    **Gone** → [Absent] [Excused]
 JEANÉMART Jérôme (181)       Mélanie Mélard    **Gone** → [Absent] [Excused]
 GROTECLAES Gregory (132)     Hubert Huppertz   **Gone** → [Absent] [Excused]
 EMONTS-GAST Erna (152)       Alicia Allmanns   **Gone** → [Absent] [Excused]
 DOBBELSTEIN Dorothée (124)   Judith Jousten    **Gone** → [Absent] [Excused]
 AUSDEMWALD Alfons (116)      Mélanie Mélard    **Gone** → [Absent] [Excused]
============================ ================= ===============================
<BLANKLINE>



Create a visit
==============

>>> print(py2rst(pcsw.Clients.create_visit))
Enregistrer consultation
(main) [visible for all]: **Utilisateur** (user), **Raison** (summary)

>>> show_fields(pcsw.Clients.create_visit, all=True)
=============== ============== ===========
 Internal name   Verbose name   Help text
--------------- -------------- -----------
 user            Utilisateur
 summary         Raison
=============== ============== ===========

>>> show_choices('romain', '/apchoices/pcsw/Clients/create_visit/user')
Alicia Allmanns
Caroline Carnol
Hubert Huppertz
Judith Jousten




Assign to me
============



Do not read
===========


When the primary key is a OneToOneField
---------------------------------------

Before :ticket:`2436`, a OneToOneField resulted in a StoreField giving
a single atomic value (the database object).

           
The primary key of a client is `id`:

>>> pk = pcsw.Client._meta.get_field('id')
>>> pk
<django.db.models.fields.AutoField: id>

>>> pk = pcsw.Client._meta.pk
>>> pk
<django.db.models.fields.related.OneToOneField: person_ptr>


>>> pk.primary_key
True

>>> ptr = pcsw.Client._meta.get_field('person_ptr')
>>> ptr
<django.db.models.fields.related.OneToOneField: person_ptr>
>>> ptr.primary_key
True

>>> ah = reception.Clients.get_handle()
>>> pprint(ah.store.list_fields)
((virtual)DisplayStoreField name_column,
 (virtual)DisplayStoreField address_column,
 StoreField 'national_id',
 (virtual)DisplayStoreField workflow_buttons,
 OneToOneStoreField 'person_ptr',
 DisabledFieldsStoreField 'disabled_fields',
 DisableEditingStoreField 'disable_editing',
 RowClassStoreField 'row_class')


>>> ah.store.pk
<django.db.models.fields.related.OneToOneField: person_ptr>

>>> ah.store.pk_index
4
>>> ah.store.list_fields[4]
OneToOneStoreField 'person_ptr'

>>> ses = rt.login("robin")
>>> ar = reception.Clients.request(user=ses.user)
>>> obj = pcsw.Client.objects.get(pk=116)
>>> lst = ah.store.row2list(ar, obj)
>>> #lst

>>> lst[ah.store.pk_index]
Person #116 ('M. Alfons AUSDEMWALD')


