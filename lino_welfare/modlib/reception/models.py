# -*- coding: UTF-8 -*-
# Copyright 2013-2014 Luc Saffre
# License: BSD (see file COPYING for details)

"""
The :xfile:`models.py` for :mod:`lino_welfare.modlib.reception`.
"""

import logging
logger = logging.getLogger(__name__)

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from lino.utils.xmlgen.html import E

from lino import dd

from lino.modlib.reception.models import *

pcsw = dd.resolve_app('pcsw')
extensible = dd.resolve_app('extensible')

# Make EventsByDay available also for reception agents who are not in
# office group.
cal = dd.resolve_app('cal')
cal.EventsByDay.required.update(user_groups='office reception')

MyWaitingVisitors.required.update(user_groups='coaching')
MyBusyVisitors.required.update(user_groups='coaching')
MyGoneVisitors.required.update(user_groups='coaching')


class CreateClientVisit(dd.Action):
    show_in_bbar = True
    sort_index = 91
    icon_name = 'hourglass'
    label = _("Create visit")
    parameters = dict(
        #~ date=models.DateField(_("Date"),blank=True,null=True),
        user=dd.ForeignKey(settings.SITE.user_model),
        summary=models.CharField(verbose_name=_("Reason"), blank=True))
    params_layout = """
    user
    summary
    """

    def run_from_ui(self, ar, **kw):
        obj = ar.selected_rows[0]
        create_prompt_event(obj, obj,
                            ar.action_param_values.user,
                            ar.action_param_values.summary,
                            settings.SITE.site_config.client_guestrole)
        #~ kw = super(CreateVisit,self).run_from_ui(obj,ar,**kw)
        #~ kw.update(success=True)
        #~ kw.update(eval_js=ar.renderer.instance_handler(ar,event))
        ar.success(refresh=True)


class CreateCoachingVisit(CreateClientVisit):

    help_text = _("Create a prompt event for this client with this coach.")

    def action_param_defaults(self, ar, obj, **kw):
        kw = super(CreateCoachingVisit,
                   self).action_param_defaults(ar, obj, **kw)
        if obj is not None:
            kw.update(user=obj.user)
        return kw

    def run_from_ui(self, ar, **kw):
        obj = ar.selected_rows[0]
        event = create_prompt_event(obj.client, obj.client,
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


class ButtonsTable(dd.VirtualTable):
    column_names = 'button'
    auto_fit_column_widths = True
    window_size = (60, 20)
    hide_top_toolbar = True

    @dd.displayfield(_("Button"))
    def button(self, obj, ar):
        return obj


class CreateEventActionsByClient(ButtonsTable):
    sort_index = 93
    master = 'pcsw.Client'
    label = _("Find date with...")
    icon_name = 'calendar'
    #~ icon_file = 'calendar.png'

    @classmethod
    def get_title(self, ar):
        s = super(CreateEventActionsByClient, self).get_title(ar)
        if ar.master_instance is not None:
            s += _(" for %s") % ar.master_instance
        return s

    @classmethod
    def get_data_rows(self, ar=None):
        if ar.master_instance is None:
            return
        for user in settings.SITE.user_model.objects.exclude(
                profile__isnull=True):
            sar = ar.spawn(
                extensible.CalendarPanel.default_action,
                current_project=ar.master_instance.pk,
                subst_user=user)
            btn = sar.as_button(unicode(user), icon_name=None)

            if btn is not None:
                yield btn


# def fld2html(fld, value):
#     if value:
#         return ("%s: " % f.verbose_name, E.b(value))
#     return []

#~ class Clients(dd.Table):


class Clients(pcsw.Clients):  # see blog 2013/0817
    #~ model = 'pcsw.Client'
    column_names = "name_column address_column national_id workflow_buttons"
    auto_fit_column_widths = True
    use_as_default_table = False
    required = dd.Required(user_groups='reception')
    # detail_layout = ClientDetail()
    # ~ insert_layout = pcsw.Clients.insert_layout.main # manually inherited
    #~ editable = False
    # ~ parameters = None # don't inherit filter parameters
    # ~ params_layout = None # don't inherit filter parameters
    #~ params_panel_hidden = True
    create_event = None  # don't inherit this action
    print_eid_content = None

    #~ read_beid = beid.BeIdReadCardAction()
    #~ find_by_beid = beid.FindByBeIdAction()

    create_event_actions = dd.ShowSlaveTable(CreateEventActionsByClient)

    create_visit = CreateClientVisit()
    #~ create_note = CreateNote()

    @classmethod
    def param_defaults(self, ar, **kw):
        kw = super(Clients, self).param_defaults(ar, **kw)
        kw.update(client_state=None)
        kw.update(observed_event=pcsw.ClientEvents.active)
        return kw


dd.inject_action('pcsw.Coaching', create_visit=CreateCoachingVisit())


class CoachingsByClient(pcsw.CoachingsByClient):
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
        elems = []
        elems += [ar.instance_action_button(
            obj.create_visit,
            _("Visit"), icon_name=CreateClientVisit.icon_name), ' ']

        #~ ba = cls.get_action_by_name('create_visit')
        #~ u = obj.user
        # ~ sar = ba.request(obj) # ,action_param_values=dict(user=u))
        #~ kw = dict()
        #~ kw.update(title=)
        #~ elems += [ar.href_to_request(sar,**kw),' ']

        if obj.user.profile is not None:
            sar = extensible.CalendarPanel.request(
                subst_user=obj.user,
                current_project=obj.client.pk)
            elems += [ar.href_to_request(
                sar, _("Find date"),
                title=_("Find date"),
                icon_name=CreateEventActionsByClient.icon_name), ' ']
            #~ icon_name = 'x-tbar-calendar'
            #~ icon_file = 'calendar.png'

        return E.div(*elems)


"""
Override library :mod:`WaitingVisitors
<ml.reception.WaitingVisitors>` table to change one
behaviour: when clicking in that table on the partner, :ref:`welfare`
should show the *Client's* and not the *Partner's* detail.

"""

if False:  # doesn't work

    def partner2client(self, obj, ar):
        return pcsw.Client.objects.get(pk=obj.partner.pk)
    WaitingVisitors.virtual_fields['partner'].override_getter(partner2client)

if False:  # doesn't work
    WaitingVisitors.partner = dd.VirtualField(
        dd.ForeignKey('pcsw.Client'), partner2client)
    MyWaitingVisitors.partner = dd.VirtualField(
        dd.ForeignKey('pcsw.Client'), partner2client)

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


inherited_setup_main_menu = setup_main_menu


def setup_main_menu(site, ui, profile, main):
    app = dd.apps.reception
    m = main.add_menu(app.app_name, app.verbose_name)
    m.add_action('reception.Clients')
    inherited_setup_main_menu(site, ui, profile, main)
