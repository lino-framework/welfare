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
    
class Event(Event):
    
    def suggest_guests(self):
        for g in super(Event,self).suggest_guests(): 
            yield g
        if self.calendar is None: 
            return
        if self.calendar.invite_client:
            if self.project is not None:
                yield self.project
    

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
    id created:20 modified:20  
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
    
