# -*- coding: UTF-8 -*-
# Copyright 2013-2014 Luc Saffre
# License: BSD (see file COPYING for details)

"""
The :xfile:`models.py` module for the :mod:`lino_welfare.modlib.cal` app.
"""

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _
from django.utils.translation import pgettext_lazy
from django.utils.translation import ugettext
from django.contrib.humanize.templatetags.humanize import naturaltime, naturalday

from django.db.models import Q

from lino import dd, rt

from lino.modlib.cal.models import *

#~ add = EventEvents.add_item
#~ add('30', _("Visit"),'visit')


from lino.modlib.cal.workflows import take, feedback

EventStates.published.text = _("Notified")


class EventType(EventType):

    #~ invite_team_members = models.BooleanField(
        #~ _("Invite team members"),default=False)
    # invite_team_members = dd.ForeignKey('users.Team', blank=True, null=True)
    invite_client = models.BooleanField(_("Invite client"), default=False)

dd.inject_field(
    'users.User', 'calendar',
    dd.ForeignKey(
        'cal.Calendar',
        verbose_name=_("Calendar where your events are published."),
        related_name='user_calendars',
        blank=True, null=True))

dd.inject_field(
    'system.SiteConfig', 'client_calendar',
    dd.ForeignKey(
        'cal.EventType',
        verbose_name=_("Default type for client events"),
        related_name='client_calendars',
        blank=True, null=True))

dd.inject_field('system.SiteConfig', 'client_guestrole',
                dd.ForeignKey('cal.GuestRole',
                              verbose_name=_(
                                  "Default guest role of client in events."),
                              related_name='client_guestroles',
                              blank=True, null=True))

dd.inject_field('system.SiteConfig', 'team_guestrole',
                dd.ForeignKey('cal.GuestRole',
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
        assert ar is not None
        #~ print 20130802, ar.renderer
        #~ raise foo
        #~ txt = naturaltime(datetime.datetime.combine(self.start_date,self.start_time or datetime.datetime.now().time()))
        txt = naturalday(self.start_date)
        if self.start_time is not None:
            txt = "%s %s %s" % (
                txt, pgettext_lazy("(time)", "at"),
                self.start_time.strftime(settings.SITE.time_format_strftime))

        #~ logger.info("20130802a when_text %r",txt)
        return ar.obj2html(self, txt)

dd.update_field(Event, 'user', verbose_name=_("Managed by"))

#~ class MyEvents(MyEvents):
    #~ exclude = dict(state=EventStates.visit)


class EventsByClient(Events):
    """Events where project is this OR one participant is this.
    """
    required = dd.required(user_groups='office')
    # master_key = 'project'
    # master = 'cal.Event'
    master = 'pcsw.Client'
    auto_fit_column_widths = True
    column_names = 'linked_date user summary workflow_buttons'
    # column_names = 'when_text user summary workflow_buttons'

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
        return kw  # tricky


class TasksByClient(Tasks):
    required = dd.required(user_groups='coaching')
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
        #~ required = dict(states='coached')

        #~ @classmethod
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
assigned_to room workflow_buttons *'

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
