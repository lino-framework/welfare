.. doctest docs/specs/reception/index.rst
.. _welfare.specs.reception:

===============================================
The :mod:`lino_welfare.modlib.reception` plugin
===============================================

The :mod:`lino_welfare.modlib.reception` plugin adds functionality for
receiving guests by an independent reception clerk.


.. contents::
   :depth: 2


.. include:: /../docs/shared/include/tested.rst

>>> from lino import startup
>>> startup('lino_welfare.projects.gerd.settings.doctests')
>>> from lino.api.doctest import *
>>> translation.activate('fr')

>>> dd.plugins.reception
lino_welfare.modlib.reception

.. _welfare.tour.reception:

Scenario
========

.. |fa-external-link| raw:: html

   <i class="fa fa-external-link"></i>


Imagine you are the reception clerk.
A visitor enters.

- Visitor: My name is xxx and I'd like to get social help.

    - Clerk: Can I have your id card please?
    - Search manually by name. Create manually a client record.
    - Read the id card.  If the person has a client record in our
      database, then Lino opens the the detail of this record. Otherwise
      it asks whether to create the client.


- Visitor: "My name is xxx, I have an appointment with Roger."
  (You know that Roger is one of the social agents.)

  - Open the clients table
    (:menuselection:`Reception --> Clients`) and find the client.

  - Click on "create visit" action.

  - Consult the *Waiting Visitors* table in your
    dasboard (if necessary, click on the |fa-external-link| icon).


  - Click on "Checkin"


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
============ ============ ================= =================== =========== =======================================================
 Start date   Start time   Managed by        Short description   State       Workflow
------------ ------------ ----------------- ------------------- ----------- -------------------------------------------------------
 15/05/2014   09:00:00     Caroline Carnol   Auswertung 2        Suggested   [Checkin] **Accepted** → [Absent] [Excused]
 15/05/2014   13:30:00     Hubert Huppertz   Abendessen          Cancelled   [Checkin] **Accepted** → [Absent] [Excused]
 22/05/2014                Mélanie Mélard    Urgent problem      Published   [Receive] [Checkout] **Waiting** → [Absent] [Excused]
 16/06/2014   09:00:00     Caroline Carnol   Auswertung 3        Suggested   [Checkin] **Accepted** → [Absent] [Excused]
 16/07/2014   09:00:00     Caroline Carnol   Auswertung 4        Suggested   [Checkin] **Accepted** → [Absent] [Excused]
 18/08/2014   09:00:00     Caroline Carnol   Auswertung 5        Suggested   [Checkin] **Accepted** → [Absent] [Excused]
 18/09/2014   09:00:00     Caroline Carnol   Auswertung 6        Suggested   [Checkin] **Accepted** → [Absent] [Excused]
 20/10/2014   09:00:00     Caroline Carnol   Auswertung 7        Suggested   [Checkin] **Accepted** → [Absent] [Excused]
 20/11/2014   09:00:00     Caroline Carnol   Auswertung 8        Suggested   [Checkin] **Accepted** → [Absent] [Excused]
 22/12/2014   09:00:00     Caroline Carnol   Auswertung 9        Suggested   [Checkin] **Accepted** → [Absent] [Excused]
============ ============ ================= =================== =========== =======================================================
<BLANKLINE>


Note that even Theresia who is a reception clerk and has no calendar
functionality can click on the dates to see their detail:

>>> rt.login('theresia').show(reception.AppointmentsByPartner, obj,
...     language="en")  #doctest: +REPORT_UDIFF
====================================== ================= =======================================================
 When                                   Managed by        Workflow
-------------------------------------- ----------------- -------------------------------------------------------
 `Thu 15/05/2014 at 09:00 <Detail>`__   Caroline Carnol   [Checkin] **Accepted** → [Absent] [Excused]
 `Thu 15/05/2014 at 13:30 <Detail>`__   Hubert Huppertz   [Checkin] **Accepted** → [Absent] [Excused]
 `Thu 22/05/2014 <Detail>`__            Mélanie Mélard    [Receive] [Checkout] **Waiting** → [Absent] [Excused]
 `Mon 16/06/2014 at 09:00 <Detail>`__   Caroline Carnol   [Checkin] **Accepted** → [Absent] [Excused]
 `Wed 16/07/2014 at 09:00 <Detail>`__   Caroline Carnol   [Checkin] **Accepted** → [Absent] [Excused]
 `Mon 18/08/2014 at 09:00 <Detail>`__   Caroline Carnol   [Checkin] **Accepted** → [Absent] [Excused]
 `Thu 18/09/2014 at 09:00 <Detail>`__   Caroline Carnol   [Checkin] **Accepted** → [Absent] [Excused]
 `Mon 20/10/2014 at 09:00 <Detail>`__   Caroline Carnol   [Checkin] **Accepted** → [Absent] [Excused]
 `Thu 20/11/2014 at 09:00 <Detail>`__   Caroline Carnol   [Checkin] **Accepted** → [Absent] [Excused]
 `Mon 22/12/2014 at 09:00 <Detail>`__   Caroline Carnol   [Checkin] **Accepted** → [Absent] [Excused]
====================================== ================= =======================================================
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
<clients.ClientStates.coached:30>

>>> rt.login('romain').show(reception.AgentsByClient, obj, language='en')
================= =============== =========================
 Agent             Coaching type   Actions
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
<clients.ClientStates.newcomer:10>

>>> rt.login('romain').show(reception.AgentsByClient, obj, language='en')
================= =============== =========================
 Agent             Coaching type   Actions
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

>>> list(d.keys()) #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE -REPORT_UDIFF +SKIP
[u'record_id', u'field_values', u'param_values', u'base_params']

>>> d.record_id
127
>>> d.base_params['mt'] #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE -REPORT_UDIFF +SKIP
5...
>>> d.base_params['mk']
127

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


.. _welfare.specs.20150715:

Reception clerk sees "Career" tab
=================================

>>> from lino.utils.jsgen import with_user_profile

The following helped us to understand and solve ticket :ticket:`340`
(discovered :blogref:`20150714`).

>>> translation.activate('en')

The problem: A reception clerk in Eupen
(:mod:`lino_welfare.projects.gerd`) should not see the career tab of
a client because the :attr:`required_roles
<lino.core.permissions.Permittable.required_roles>` of that panel
include :class:`IntegUser
<lino_welfare.modlib.integ.roles.IntegUser>`.  But they saw it
nevertheless:

.. image:: 20150715.png

A reception clerk is not an integration agent:

>>> from lino_welfare.modlib.welfare.user_types import *
>>> isinstance(ReceptionClerk, IntegUser)
False

>>> ia_user_type = users.UserTypes.get_by_value('100')
>>> print(ia_user_type)
100 (Integration agent)

>>> rc_user_type = users.UserTypes.get_by_value('210')
>>> print(rc_user_type)
210 (Reception clerk)


We are talking about the detail layout of a client, defined by
:class:`lino_weleup.lib.pcsw.models.ClientDetail`:

>>> dtl = rt.models.pcsw.Clients.detail_layout
>>> dtl  #doctest: +ELLIPSIS
<lino_weleup.lib.pcsw.models.ClientDetail object at ...>
>>> dtl.__class__
<class 'lino_weleup.lib.pcsw.models.ClientDetail'>

>>> lh = dtl.get_layout_handle(settings.SITE.kernel.default_ui)
>>> print(lh)
LayoutHandle for lino_weleup.lib.pcsw.models.ClientDetail on lino_welfare.modlib.pcsw.models.Clients

Let's get the `career` panel. It is a :class:`lino.core.elems.Panel`:

>>> # career_panel = lh.main.find_by_name('career')
>>> career_panel = with_user_profile(ia_user_type, lh.main.find_by_name, 'career')
>>> career_panel
<Panel career in lino_weleup.lib.pcsw.models.ClientDetail on lino_welfare.modlib.pcsw.models.Clients>
>>> career_panel.__class__
<class 'lino.core.elems.Panel'>

To see this panel, you need to be an integration agent:

>>> career_panel.required_roles == {IntegUser}
True

Theresia is a reception clerk
(:class:`lino_welfare.modlib.welfare.user_types.ReceptionClerk`):

>>> theresia = users.User.objects.get(username="theresia")
>>> theresia.user_type.role  #doctest: +ELLIPSIS
<lino_welfare.modlib.welfare.user_types.ReceptionClerk object at ...>

And that's not the role required to view this panel:

>>> theresia.user_type.has_required_roles(career_panel.required_roles)
False

And thus this panel is not visible for her:

>>> career_panel.get_view_permission(theresia.user_type)
False

Note that the Panel objects which are not visible continue to be in
`lh.main.elements`:

>>> print(' '.join([e.name for e in lh.main.elements]))
... #doctest: +NORMALIZE_WHITESPACE
general contact coaching aids_tab work_tab_1 career languages
competences contracts history calendar MovementsByProject misc cbss debts

Lino filters removes them only when generating the js files, IOW
during :func:`lino.utils.jsgen.py2js`:

>>> from lino.utils.jsgen import with_user_profile
>>> from lino.utils.jsgen import py2js, declare_vars
>>> def f():
...     print(py2js(lh.main.elements))
>>> with_user_profile(theresia.user_type, f)
... #doctest: +NORMALIZE_WHITESPACE +SKIP
[ general_panel1172, contact_panel1199, coaching_panel1428, aids_tab_panel1543, work_tab_1_panel1571, contracts_panel2318, history_panel2321, calendar_panel2401, misc_panel2442 ]

.. We skip above test because it is bothersome to adapt the names whenever a
   new actor is added, and because probably it doesn't actually doesn't cover
   anything.


I can even render the :file:`lino*.js` files (at least once):

>>> class W:
...     def write(self, s):
...         if "career" in s: print(s)
>>> w = W()
>>> def f():
...     dd.plugins.extjs.renderer.write_lino_js(w)
>>> with_user_profile(theresia.user_type, f)
... #doctest: +NORMALIZE_WHITESPACE

So until now everything looks okay.

The problem was that until :blogref:`20150716`, :meth:`write_lino_js`
left the requirements of our career panel modified (loosened) after
having run.  So the following was `False` only after the first time
and `True` all subsequent times:

>>> theresia.user_type.has_required_roles(career_panel.required_roles)
False
>>> theresia.user_type.has_required_roles(career_panel.required_roles)
False
