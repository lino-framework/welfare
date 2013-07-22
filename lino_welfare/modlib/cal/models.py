# -*- coding: UTF-8 -*-
## Copyright 2013 Luc Saffre
## This file is part of the Lino-Faggio project.
## Lino-Faggio is free software; you can redistribute it and/or modify 
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 3 of the License, or
## (at your option) any later version.
## Lino-Faggio is distributed in the hope that it will be useful, 
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
## GNU General Public License for more details.
## You should have received a copy of the GNU General Public License
## along with Lino-Faggio; if not, see <http://www.gnu.org/licenses/>.

"""
This module extends :mod:`lino.modlib.cal.models`
"""

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from lino import dd

#~ dd.extends_app('lino.modlib.cal',globals())

#~ PARENT_APP = 'lino.modlib.cal'
from lino.modlib.cal.models import *

from lino.modlib.cal.workflows import welfare


class Calendar(Calendar):
    
    #~ invite_team_members = models.BooleanField(
        #~ _("Invite team members"),default=False)
    invite_team_members = dd.ForeignKey('users.Team',blank=True,null=True)
    invite_client = models.BooleanField(_("Invite client"),default=False)
    
dd.inject_field('system.SiteConfig','client_guestrole',
    dd.ForeignKey('cal.GuestRole',
        verbose_name=_("Guest role for clients"),
        related_name='client_guestroles',
        blank=True,null=True))    
    
dd.inject_field('system.SiteConfig','client_calender',
    dd.ForeignKey('cal.Calendar',
        verbose_name=_("Default calendar for client events"),
        related_name='client_calendars',
        blank=True,null=True))    
    
dd.inject_field('system.SiteConfig','team_guestrole',
    dd.ForeignKey('cal.GuestRole',
        verbose_name=_("Guest role for team members"),
        related_name='team_guestroles',
        blank=True,null=True))    
    
class Event(Event):
    
    def suggest_guests(self):
        #~ print "20130722 suggest_guests"
        for g in super(Event,self).suggest_guests(): 
            yield g
        if self.calendar is None: 
            return
        Guest = settings.SITE.modules.cal.Guest
        if self.calendar.invite_team_members:
            ug = self.calendar.invite_team_members
            for obj in settings.SITE.modules.cal.Membership.objects.filter(group=ug).exclude(user=self.user):
                if obj.user.partner:
                    yield Guest(event=self,
                        partner=obj.user.partner,
                        role=settings.SITE.site_config.team_guestrole)
        
            
        if self.calendar.invite_client:
            if self.project is not None:
                yield Guest(event=self,
                    partner=self.project,
                    role=settings.SITE.site_config.client_guestrole)
    

@dd.receiver(dd.post_analyze)
def customize_cal(sender,**kw):
    site = sender
    
    site.modules.cal.Calendars.set_detail_layout("""
    type name id 
    # description
    url_template username password
    readonly invite_team_members invite_client color start_date
    build_method template email_template attach_to_email
    EventsByCalendar SubscriptionsByCalendar
    """)
    
    site.modules.cal.Calendars.set_insert_layout("""
    name 
    type invite_team_members color 
    invite_client 
    """,window_size=(60,'auto'))
    
    site.modules.cal.Events.set_detail_layout("general more")
    site.modules.cal.Events.add_detail_panel("general","""
    calendar summary project 
    start end user assigned_to
    room priority access_class transparent #rset 
    owner workflow_buttons
    description GuestsByEvent 
    """,_("General"))
    site.modules.cal.Events.add_detail_panel("more","""
    id created:20 modified:20 state
    outbox.MailsByController postings.PostingsByController
    """,_("More"))
    
    site.modules.cal.Events.set_insert_layout("""
    summary 
    start end 
    calendar project 
    """,
    start="start_date start_time",
    end="end_date end_time",
    window_size=(60,'auto'))
    

class CreateClientEvent(dd.RowAction):
    label = _("Appointment")
    show_in_workflow = True
    parameters = dict(
        date=models.DateField(_("Date"),blank=True,null=True),
        user=dd.ForeignKey(settings.SITE.user_model),
        summary=models.CharField(verbose_name=_("Summary"),blank=True))
    params_layout = """
    date user 
    summary
    """
    #~ required = dict(states='coached')
    
    #~ @classmethod
    def action_param_defaults(self,ar,obj,**kw):
        kw = super(CreateClientEvent,self).action_param_defaults(ar,obj,**kw)
        kw.update(user=ar.get_user())
        kw.update(date=datetime.date.today())
        return kw
        
    def get_notify_subject(self,ar,obj):
        return _("Created appointment for %(user)s with %(partner)s") % dict(
            event=obj,
            user=obj.event.user,
            partner=obj.partner)
     
    def run_from_ui(self,obj,ar,**kw):
        ekw = dict(project=obj,user=ar.get_user()) 
        ekw.update(state=EventStates.draft)
        #~ ekw.update(state=EventStates.scheduled)
        ekw.update(start_date=ar.action_param_values.date)
        ekw.update(end_date=ar.action_param_values.date)
        ekw.update(calendar=settings.SITE.site_config.client_calender)
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
        kw.update(eval_js=ar.renderer.instance_handler(ar,event))
        return kw


