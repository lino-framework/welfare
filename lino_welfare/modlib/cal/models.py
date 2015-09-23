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
Database models for :mod:`lino_welfare.modlib.cal`.
"""

from __future__ import unicode_literals

import datetime


from django.utils.translation import ugettext_lazy as _
from django.utils.translation import pgettext_lazy
from django.contrib.humanize.templatetags.humanize import naturalday

from django.db.models import Q

from lino.api import dd, rt

from lino.utils.xmlgen.html import E

from lino.modlib.cal.models import *

from lino.modlib.cal.utils import format_date
from lino.modlib.cal.workflows import take, feedback
from lino.modlib.reception.models import checkout_guest
from lino.modlib.office.roles import OfficeUser
from lino_welfare.modlib.pcsw.roles import SocialAgent


EventStates.published.text = _("Notified")


class CloseMeeting(feedback.CloseMeeting):
    """Close the meeting (mark it as "took place") and check out all
guests. Ask confirmation naming the guests who need to check out.

    """
    def execute(self, ar, obj):

        def yes(ar):
            if not obj.end_time:
                obj.end_time = datetime.datetime.now()
                ar.info("event.end_time has been set by CloseMeeting")
            return super(CloseMeeting, self).execute(ar, obj)

        guests = obj.guest_set.filter(gone_since__isnull=True,
                                      waiting_since__isnull=False)
        num = len(guests)
        if num == 0:
            return yes(ar)  # no confirmation
        msg = _("This will checkout {num} guests: {guests}".format(
            num=num,
            guests=', '.join([unicode(g.partner) for g in guests])))
        rv = ar.confirm(yes, msg)
        for g in guests:
            checkout_guest(g, ar)

        return rv


@dd.receiver(dd.pre_analyze)
def my_event_workflows(sender=None, **kw):

    EventStates.override_transition(close_meeting=CloseMeeting)


def you_are_busy_messages(ar):
    """Yield :message:`You are busy in XXX` messages for the welcome
page."""

    events = rt.modules.cal.Event.objects.filter(
        user=ar.get_user(), guest__state=GuestStates.busy).distinct()
    if events.count() > 0:
        chunks = [unicode(_("You are busy in "))]
        sep = None
        for evt in events:
            if sep:
                chunks.append(sep)
            ctx = dict(id=evt.id)
            if evt.event_type is None:
                ctx.update(label=unicode(evt))
            else:
                ctx.update(label=evt.event_type.event_label)

            if evt.project is None:
                txt = _("{label} #{id}").format(**ctx)
            else:
                ctx.update(project=unicode(evt.project))
                txt = _("{label} with {project}").format(**ctx)
            chunks.append(ar.obj2html(evt, txt))
            chunks += [
                ' (',
                ar.instance_action_button(evt.close_meeting),
                ')']
            sep = ', '
        chunks.append('. ')
        yield E.span(*chunks)
            

dd.add_welcome_handler(you_are_busy_messages)


class EventType(EventType):

    #~ invite_team_members = models.BooleanField(
        #~ _("Invite team members"),default=False)
    # invite_team_members = dd.ForeignKey('users.Team', blank=True, null=True)
    invite_client = models.BooleanField(_("Invite client"), default=False)

dd.inject_field(
    'users.User', 'calendar',
    dd.ForeignKey(
        'cal.Calendar',
        verbose_name=_("User Calendar"),
        help_text=_("Calendar where your events are published."),
        related_name='user_calendars',
        blank=True, null=True))

dd.inject_field(
    'system.SiteConfig', 'client_calendar',
    dd.ForeignKey(
        'cal.EventType',
        verbose_name=_("Default type for client calendar events"),
        related_name='client_calendars',
        blank=True, null=True))

dd.inject_field(
    'system.SiteConfig', 'client_guestrole',
    dd.ForeignKey(
        'cal.GuestRole',
        verbose_name=_("Client guest role"),
        help_text=_("Default guest role of client in calendar events."),
        related_name='client_guestroles',
        blank=True, null=True))

dd.inject_field(
    'system.SiteConfig', 'team_guestrole',
    dd.ForeignKey(
        'cal.GuestRole',
        verbose_name=_("Guest role for team members"),
        related_name='team_guestroles',
        blank=True, null=True))


class Event(Event):

    # course = models.ForeignKey(
    #     "courses.Course", blank=True, null=True,
    #     help_text=_("Fill in only if this event is a session of a course."))

    def get_calendar(self):
        if self.assigned_to is not None:
            return self.assigned_to.calendar
        if self.user is not None:
            return self.user.calendar

    @dd.chooser()
    def assigned_to_choices(self):
        return settings.SITE.user_model.objects.filter(calendar__isnull=False)

    @dd.chooser()
    def user_choices(self):
        return settings.SITE.user_model.objects.filter(calendar__isnull=False)

    def full_clean(self):
        if not self.event_type:
            self.event_type = settings.SITE.site_config.client_calendar
        super(Event, self).full_clean()

    @dd.displayfield(_("When"))
    def when_text(self, ar):
        # Overrides `lino.modlib.cal.models_event.Event.when_text`.
        # It is a bit of redundant code, but making it configurable
        # would be nitpicky.
        assert ar is not None
        # txt = naturalday(self.start_date)
        txt = format_date(self.start_date, 'EE ')
        txt += dd.fds(self.start_date)
        if self.start_time is not None:
            txt = "%s %s %s" % (
                txt, pgettext_lazy("(time)", "at"),
                self.start_time.strftime(settings.SITE.time_format_strftime))

        #~ logger.info("20130802a when_text %r",txt)
        return ar.obj2html(self, txt)

    def suggest_guests(self):
        """Yields the guest suggested by `super`, but if Client field is
        filled and if `event_type` is marked `invite_client`, add the
        client as Guest.

        """
        for g in super(Event, self).suggest_guests():
            yield g
        client = self.project
        if client is None:
            return
        if self.event_type and self.event_type.invite_client:
            Guest = rt.modules.cal.Guest
            GuestStates = rt.modules.cal.GuestStates
            st = GuestStates.accepted
            yield Guest(event=self,
                        partner=client,
                        state=st,
                        role=settings.SITE.site_config.client_guestrole)


dd.update_field(Event, 'user', verbose_name=_("Managed by"))


class EventsByClient(Events):
    """Events where :attr:`Event.project` **or** one guest is this client.

    """
    required_roles = dd.required(OfficeUser)
    # master_key = 'project'
    # master = 'cal.Event'
    master = 'pcsw.Client'
    auto_fit_column_widths = True
    column_names = 'linked_date user summary workflow_buttons'
    # column_names = 'when_text user summary workflow_buttons'
    insert_layout = """
    event_type
    summary
    start_date start_time end_date end_time
    """

    @classmethod
    def get_queryset(self, ar):
        mi = ar.master_instance
        if mi is None:
            return None
        flt = Q(project=mi) | Q(guest__partner=mi)
        qs = self.model.objects.filter(flt).distinct()
        # logger.info("20140314 %s", qs.query)
        return qs

    @classmethod
    def get_filter_kw(self, ar, **kw):
        # cannot call super() since we don't have a master_key
        mi = ar.master_instance
        if mi is None:
            return None
        kw.update(project=mi)
        return kw


class TasksByClient(Tasks):
    required_roles = dd.required(SocialAgent)
    master_key = 'project'
    column_names = 'start_date due_date summary description notes'

    @dd.displayfield(_("Notes"))
    def notes(self, obj, ar):
        return '.' * 20


class Guest(Guest):

    def get_excerpt_options(self, ar, **kw):
        kw.update(project=self.event.project)
        return super(Guest, self).get_excerpt_options(ar, **kw)


@dd.receiver(dd.post_analyze)
def customize_cal(sender, **kw):
    site = sender

    site.modules.cal.EventTypes.set_detail_layout("""
    name
    event_label
    max_conflicting all_rooms locks_user
    id invite_client is_appointment email_template attach_to_email
    EventsByType
    """)

    site.modules.cal.EventTypes.set_insert_layout("""
    name
    # invite_team_members
    invite_client
    """, window_size=(60, 'auto'))

    rt.modules.cal.Guests.set_detail_layout("""
    event partner role
    state remark workflow_buttons
    waiting_since busy_since gone_since
    outbox.MailsByController
    """)
    site.modules.cal.Events.set_detail_layout("general more")
    site.modules.cal.Events.add_detail_panel("general", """
    event_type summary project
    start end user assigned_to
    room priority access_class transparent #rset
    owner workflow_buttons
    description GuestsByEvent
    """, _("General"))
    site.modules.cal.Events.add_detail_panel("more", """
    id created:20 modified:20 state
    outbox.MailsByController #postings.PostingsByController
    """, _("More"))

    site.modules.cal.Events.set_insert_layout(
        """
        summary
        start end
        event_type project
        """,
        start="start_date start_time",
        end="end_date end_time",
        window_size=(60, 'auto'))


if False:

    class CreateClientEvent(dd.Action):
        label = _("Appointment")
        custom_handler = True
        parameters = dict(
            date=models.DateField(_("Date"), blank=True, null=True),
            user=dd.ForeignKey(settings.SITE.user_model),
            summary=models.CharField(verbose_name=_("Summary"), blank=True))
        params_layout = """
    date user 
    summary
    """

        def action_param_defaults(self, ar, obj, **kw):
            kw = super(CreateClientEvent,
                       self).action_param_defaults(ar, obj, **kw)
            kw.update(user=ar.get_user())
            kw.update(date=settings.SITE.today())
            return kw

        def get_notify_subject(self, ar, obj):
            return _("Created appointment for %(user)s with %(partner)s") % dict(
                event=obj,
                user=obj.event.user,
                partner=obj.partner)

        def run_from_ui(self, ar, **kw):
            obj = ar.selected_rows[0]
            ekw = dict(project=obj, user=ar.get_user())
            ekw.update(state=EventStates.draft)
            #~ ekw.update(state=EventStates.published)
            ekw.update(start_date=ar.action_param_values.date)
            ekw.update(end_date=ar.action_param_values.date)
            ekw.update(event_type=settings.SITE.site_config.client_calendar)
            if ar.action_param_values.summary:
                ekw.update(summary=ar.action_param_values.summary)
            if ar.action_param_values.user != ar.get_user():
                ekw.update(assigned_to=ar.action_param_values.user)
            event = Event(**ekw)
            event.full_clean()
            event.save()
            #~ print 20130722, ekw, ar.action_param_values.user, ar.get_user()
            #~ kw = super(CreateClientEvent,self).run_from_ui(obj,ar,**kw)
            #~ kw.update(success=True)
            kw.update(eval_js=ar.renderer.instance_handler(ar, event))
            ar.success(**kw)

EventsByDay.column_names = 'start_time project summary user \
assigned_to event_type room workflow_buttons *'

EventsByController.column_names = 'when_text summary user \
assigned_to workflow_buttons *'


class Task(Task):

    class Meta:
        verbose_name = _("Task")
        verbose_name_plural = _("Tasks")
        abstract = dd.is_abstract_model(__name__, 'Task')

    delegated = models.BooleanField(
        _("Delegated to client"), default=False)

Tasks.detail_layout = """
    start_date due_date id workflow_buttons
    summary
    project user delegated
    owner created:20 modified:20
    description #notes.NotesByTask
    """



class TasksByController(TasksByController):
    column_names = 'start_date due_date summary user delegated workflow_buttons id'
    insert_layout = """
    summary
    start_date due_date
    user delegated
    """



# add = TaskStates.add_item
# add('40', _("Client"), 'client')

# @dd.receiver(dd.pre_analyze)
# def setup_task_workflows(sender=None, **kw):

#     TaskStates.client.add_transition(_("Delegated to client"), 
#                                      states='done started cancelled')
