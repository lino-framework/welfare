# -*- coding: UTF-8 -*-
# Copyright 2013-2015 Luc Saffre
# This file is part of Lino Welfare.
#
# Lino Welfare is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# Lino Welfare is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License along with Lino Welfare.  If not, see
# <http://www.gnu.org/licenses/>.

"""
Database models for :mod:`lino_welfare.modlib.reception`.

.. autosummary::

"""

import logging
logger = logging.getLogger(__name__)

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from lino.utils.xmlgen.html import E

from lino.api import dd

from lino.core.tables import ButtonsTable

#from lino.modlib.contacts.roles import ContactsUser

from lino.modlib.reception.models import *

pcsw = dd.resolve_app('pcsw')
extensible = dd.resolve_app('extensible')
from lino_welfare.modlib.pcsw.models import ClientStates

# Make EventsByDay available also for reception agents who are not in
# office group.
# cal = dd.resolve_app('cal')
# cal.EventsByDay.required_roles.add(OfficeUser)
# cal.EventsByDay.required_roles = dd.required(OfficeUser)

# Visitors.required.update(user_groups='coaching reception')
# WaitingVisitors.required.update(user_groups='coaching reception')
# MyWaitingVisitors.required.update(user_groups='coaching')
# MyBusyVisitors.required.update(user_groups='coaching')
# MyGoneVisitors.required.update(user_groups='coaching')


def appointable_users(*args, **kw):
    """Return a queryset of the users for whom reception clerks can create
    appointments. Candidates must have a :attr:`profile
    <lino.modlib.users.models.User.profile>` and a :attr:`calendar
    <lino_welfare.modlib.users.models.User.calendar>`.
    Additional arguments are forwarded to the query filter.

    """
    qs = settings.SITE.user_model.objects.exclude(profile='')
    kw.update(calendar__isnull=False)
    qs = qs.filter(*args, **kw)
    return qs


class FindDateByClientTable(ButtonsTable):
    """A :class:`ButtonsTable <lino.core.tables.ButtonsTable>` which shows
    all users who are candidates responsible of new client
    appointment. Clicking on one of them will open the
    `extensible.CalendarPanel` with appropriate parameters
    (`subst_user` and `current_project`).

    """
    master = 'pcsw.Client'

    # forwarded to ShowSlaveTable:
    sort_index = 103
    label = _("Find date with...")
    icon_name = 'calendar'

    @classmethod
    def get_title(self, ar):
        s = super(FindDateByClientTable, self).get_title(ar)
        if ar.master_instance is not None:
            s += _(" for %s") % ar.master_instance
        return s

    @classmethod
    def get_data_rows(self, ar=None):
        mi = ar.master_instance  # a Client
        if mi is None:
            return
        # for user in appointable_users(newcomer_quota__gt=0):
        for user in appointable_users(newcomer_appointments=True):
        # for user in appointable_users():
            sar = extensible.CalendarPanel.request(
                subst_user=user,
                current_project=mi.pk)
            yield ar.href_to_request(sar, unicode(user), icon_name=None)


class FindDateByClientDlg(dd.Action):
    """Create an appointment from a client for this client with a user to
be selected manually."""
    show_in_bbar = True
    sort_index = 101
    icon_name = FindDateByClientTable.icon_name
    label = _("Create appointment")
    parameters = dict(
        user=dd.ForeignKey(settings.SITE.user_model),
        summary=models.CharField(verbose_name=_("Reason"), blank=True))
    params_layout = """
    user
    summary
    """

    @dd.chooser()
    def user_choices(self):
        return appointable_users(newcomer_appointments=True)
        # return appointable_users()

    def run_from_ui(self, ar, **kw):
        obj = ar.selected_rows[0]  # a Client
        kw.update(
            subst_user=ar.action_param_values.user,
            current_project=obj.pk)
        return extensible.CalendarPanel.default_action.run_from_ui(ar, **kw)


class CreateClientVisit(dd.Action):
    """Create a prompt event from a client."""
    readonly = False
    show_in_bbar = True
    sort_index = 101
    icon_name = 'hourglass'
    label = _("Create visit")
    parameters = dict(
        user=dd.ForeignKey(settings.SITE.user_model),
        summary=models.CharField(verbose_name=_("Reason"), blank=True))
    params_layout = """
    user
    summary
    """

    @dd.chooser()
    def user_choices(self):
        return appointable_users(newcomer_consultations=True)

    def run_from_ui(self, ar, **kw):
        obj = ar.selected_rows[0]
        pv = ar.action_param_values
        if not pv.user:
            raise Warning(_("Please select a user!"))
        create_prompt_event(obj, obj, pv.user, pv.summary,
                            settings.SITE.site_config.client_guestrole)
        ar.success(refresh=True)


class CreateCoachingVisit(CreateClientVisit):
    """Call a prompt event from a :class:`Coaching`.  See also
:func:`lino.modlib.reception.models.create_prompt_event`.

    """
    help_text = _("Create a prompt event for this client with this coach.")

    def action_param_defaults(self, ar, obj, **kw):
        kw = super(CreateCoachingVisit,
                   self).action_param_defaults(ar, obj, **kw)
        if obj is not None:
            kw.update(user=obj.user)
        return kw

    def run_from_ui(self, ar, **kw):
        obj = ar.selected_rows[0]
        create_prompt_event(
            obj.client, obj.client,
            ar.action_param_values.user,
            ar.action_param_values.summary,
            settings.SITE.site_config.client_guestrole)
        #~ kw = super(CreateVisit,self).run_from_ui(obj,ar,**kw)
        #~ kw.update(success=True)
        #~ kw.update(eval_js=ar.renderer.instance_handler(ar,event))
        ar.success(refresh=True)
        #~ return kw


class CreateNote(dd.Action):
    label = _("Attestation")
    show_in_bbar = False
    custom_handler = True
    parameters = dict(
        #~ date=models.DateField(_("Date"),blank=True,null=True),
        note_type=dd.ForeignKey('notes.NoteType'),
        subject=models.CharField(verbose_name=_("Subject"), blank=True))
    params_layout = """
    note_type
    subject
    """
    #~ required = dict(states='coached')

    def run_from_ui(self, ar, **kw):
        obj = ar.selected_rows[0]
        notes = dd.resolve_app('notes')

        def ok(ar):
            ekw = dict(project=obj, user=ar.get_user())
            ekw.update(type=ar.action_param_values.note_type)
            ekw.update(date=settings.SITE.today())
            if ar.action_param_values.subject:
                ekw.update(subject=ar.action_param_values.subject)
            note = notes.Note(**ekw)
            note.save()
            #~ kw.update(success=True)
            #~ kw.update(refresh=True)
            ar.goto_instance(note)

        if obj.has_valid_card_data():
            ok(ar)
            return
        ar.confirm(ok, _("Client has no valid eID data!",
                         _("Do you still want to issue an excerpt?")))


# def fld2html(fld, value):
#     if value:
#         return ("%s: " % f.verbose_name, E.b(value))
#     return []

#~ class Clients(dd.Table):


class Clients(pcsw.CoachedClients):  # see blog 2013/0817
    """The list that opens by :menuselection:`Reception --> Clients`.

    Visible to user profiles in group "reception".
    It differs from :class:`pcsw.CoachedClients
    <lino_welfare.modlib.pcsw.models.CoachedClients>` by the visible columns.

    """
    required_roles = dd.required((OfficeUser, OfficeOperator))
    # required_roles = dd.required((ContactsUser, OfficeOperator))
    column_names = "name_column address_column national_id workflow_buttons"
    auto_fit_column_widths = True
    use_as_default_table = False
    create_event = None  # don't inherit this action
    print_eid_content = None

    #~ read_beid = beid.BeIdReadCardAction()
    #~ find_by_beid = beid.FindByBeIdAction()

    # @classmethod
    # def param_defaults(self, ar, **kw):
    #     kw = super(Clients, self).param_defaults(ar, **kw)
    #     kw.update(client_state=None)
    #     kw.update(observed_event=pcsw.ClientEvents.active)
    #     return kw


dd.inject_action('pcsw.Coaching', create_visit=CreateCoachingVisit())
dd.inject_action('pcsw.Client', create_visit=CreateClientVisit())
if False:
    # doesn't work because the combination (dialog action with JS
    # instead of AJAX call) is not yet possible. But helps to imagine
    # how it would look
    dd.inject_action(
        'pcsw.Client', find_date_dlg=FindDateByClientDlg())
dd.inject_action(
    'pcsw.Client', find_date=dd.ShowSlaveTable(FindDateByClientTable))


class AgentsByClient(pcsw.CoachingsByClient):
    """Shows the users for whom an appointment can be made with this
client. Per user you have two possible buttons: (1) a prompt
consultation (client will wait in the lounge until the user receives
them) or (2) a scheduled appointment in the user's calendar.

Tested document about :ref:`welfare.tested.reception.AgentsByClient`

    """
    label = _("Create appointment with")
    filter = models.Q(end_date__isnull=True)
    column_names = "user coaching_type actions"
    # master = 'pcsw.Client'
    master_key = 'client'
    slave_grid_format = 'html'
    # auto_fit_column_widths = True

    @classmethod
    def get_data_rows(self, ar=None):
        mi = ar.master_instance
        if mi is None:
            return
        if mi.client_state == ClientStates.coached:
            for obj in pcsw.Coaching.objects.filter(
                    client=mi, end_date__isnull=True).order_by('start_date'):
                yield obj
        else:
            # yield agents available for open consultation
            cnd = Q(newcomer_appointments=True) \
                | Q(newcomer_consultations=True)
            for u in appointable_users(cnd):
            # for u in appointable_users(newcomer_quota__gt=0):
                # Create a temporary coaching. needed for generating
                # the action buttons below.
                yield pcsw.Coaching(
                    client=mi, user=u, type=u.coaching_type,
                    start_date=dd.today())

    @dd.displayfield(_("Agent"))
    def user(self, obj, ar):
        return unicode(obj.user)

    @dd.displayfield(_("Coaching type"))
    def coaching_type(self, obj, ar):
        return unicode(obj.type)

    @dd.displayfield(_("Actions"))
    def actions(cls, obj, ar):
        
        client = ar.master_instance
        if client is None:
            return ''
        elems = []

        user = obj.user

        # client.create_visit is the instance action for
        # CreateClientVisit
        if client.client_state == ClientStates.coached \
           or user.newcomer_consultations:
           # or user.newcomer_quota > 0:
            apv = dict(user=user)
            if False:  # apv are ignored, and it's ugly
                ba = pcsw.CoachedClients.get_action_by_name('create_visit')
                sar = ba.request(action_param_values=apv)
                sar.setup_from(ar)
                btn = sar.row_action_button_ar(client, _("Visit"))
            else:
                btn = ar.instance_action_button(
                    client.create_visit,
                    _("Visit"),
                    request_kwargs=dict(action_param_values=apv),
                    icon_name=CreateClientVisit.icon_name)
            elems += [btn, ' ']

        if client.client_state == ClientStates.coached \
           or user.newcomer_appointments:
           # or user.newcomer_quota > 0:
            sar = extensible.CalendarPanel.request(
                subst_user=user,
                current_project=client.pk)
            elems += [ar.href_to_request(
                sar, _("Find date"),
                title=_("Find date"),
                icon_name=FindDateByClientTable.icon_name), ' ']
            #~ icon_name = 'x-tbar-calendar'
            #~ icon_file = 'calendar.png'

        return E.div(*elems)


class CoachingsByClient(pcsw.CoachingsByClient):
    # obsolete. replaced by AgentsByClient
    label = _("Create appointment with")
    filter = models.Q(end_date__isnull=True)
    column_names = "user type actions"

    #~ @classmethod
    #~ def get_data_rows(self,ar=None):
        #~ for obj in self.get_request_queryset(ar):
            #~ yield obj
        #~ if ar.master_instance:
            #~ yield pcsw.Coaching(client=ar.master_instance)

    @dd.displayfield(_("Actions"))
    def actions(cls, obj, ar):
        client = ar.master_instance
        if client is None:
            return ''
        elems = []
        elems += [ar.instance_action_button(
            obj.create_visit,
            _("Visit"), icon_name=CreateClientVisit.icon_name), ' ']

        if obj.user.profile is not None:
            sar = extensible.CalendarPanel.request(
                subst_user=obj.user,
                current_project=client.pk)
            elems += [ar.href_to_request(
                sar, _("Find date"),
                title=_("Find date"),
                icon_name=FindDateByClientTable.icon_name), ' ']
            #~ icon_name = 'x-tbar-calendar'
            #~ icon_file = 'calendar.png'

        return E.div(*elems)


# Override library :mod:`WaitingVisitors
# <lino.modlib.reception.models.WaitingVisitors>` table to change one
# behaviour: when clicking in that table on the partner, :ref:`welfare`
# should show the *Client's* and not the *Partner's* detail.

if True:  # works, though is very hackerish

    def func(obj, ar):
        return pcsw.Client.objects.get(pk=obj.partner.pk)
    dd.inject_field('cal.Guest', 'client',
                    dd.VirtualField(dd.ForeignKey('pcsw.Client'), func))
    for T in WaitingVisitors, MyWaitingVisitors, GoneVisitors, BusyVisitors:
        T.column_names = T.column_names.replace('partner', 'client')
        T.detail_layout = T.detail_layout.replace('partner', 'client')

if False:  # works, but is very stupid

    class WaitingVisitors(WaitingVisitors):
        # labels are not automatically inherited. Must inherit manually
        label = WaitingVisitors.label

        @dd.virtualfield(dd.ForeignKey('pcsw.Client'))
        def partner(self, obj, ar):
            return pcsw.Client.objects.get(pk=obj.partner.pk)

    #~ The same for MyWaitingVisitors. See :blogref:`20130817`
    class MyWaitingVisitors(MyWaitingVisitors):
        # labels are not automatically inherited. Must inherit manually
        label = MyWaitingVisitors.label

    @dd.virtualfield(dd.ForeignKey('pcsw.Client'))
    def partner(self, obj, ar):
        return pcsw.Client.objects.get(pk=obj.partner.pk)


