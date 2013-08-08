# -*- coding: UTF-8 -*-
## Copyright 2013 Luc Saffre
## This file is part of the Lino project.
## Lino is free software; you can redistribute it and/or modify 
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 3 of the License, or
## (at your option) any later version.
## Lino is distributed in the hope that it will be useful, 
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
## GNU General Public License for more details.
## You should have received a copy of the GNU General Public License
## along with Lino; if not, see <http://www.gnu.org/licenses/>.

"""
Defines models for :mod:`lino_welfare.modlib.reception`.
"""

import logging
logger = logging.getLogger(__name__)

import os
import sys
import cgi
import datetime
import base64


from django.db import models
from django.db.models import Q
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import pgettext_lazy
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.db import IntegrityError
from django.utils.encoding import force_unicode
from django.core.exceptions import ValidationError
from django.contrib.humanize.templatetags.humanize import naturaltime

from lino.utils.xmlgen.html import E
from lino.utils import ssin
from lino.utils import join_words
from lino.utils import join_elems
from lino.core.actions import InstanceAction

from lino import dd

from lino.modlib.reception.models import *


from lino.modlib.cal.models import GuestStates

from lino_welfare.modlib.reception import App
from lino.mixins import beid

cal = dd.resolve_app('cal')
pcsw = dd.resolve_app('pcsw')

#~ class CoachingsByClient(dd.Table):
    #~ model = 'pcsw.Coaching'
    #~ master_key = 'client'
    #~ column_names = "user info" 
    #~ auto_fit_column_widths = True
    #~ use_as_default_table = False
    #~ required = dd.Required(user_groups='reception')
    #~ 
    #~ @dd.virtualfield(dd.HtmlBox())
    #~ def info(cls,obj,ar):
        #~ sar = cal.CalendarPanel.request(subst_user=obj.user)
        #~ return ar.href_to_request(sar,unicode(obj.user))
    
class CreateNote(dd.RowAction): 
    label = _("Attestation")
    #~ show_in_workflow = True
    show_in_row_actions = True
    parameters = dict(
        #~ date=models.DateField(_("Date"),blank=True,null=True),
        note_type=dd.ForeignKey('notes.NoteType'),
        subject=models.CharField(verbose_name=_("Subject"),blank=True))
    params_layout = """
    note_type
    subject
    """
    #~ required = dict(states='coached')
    
    def run_from_ui(self,obj,ar,**kw):
        notes = dd.resolve_app('notes')
        ekw = dict(project=obj,user=ar.get_user()) 
        ekw.update(type=ar.action_param_values.note_type)
        ekw.update(date=datetime.date.today())
        if ar.action_param_values.subject:
            ekw.update(subject=ar.action_param_values.subject)
        note = notes.Note(**ekw)
        note.save()
        #~ kw.update(success=True)
        #~ kw.update(refresh=True)
        return ar.goto_instance(note,**kw)

    
class ClientDetail(dd.FormLayout):
    
    main = "general history"
    
    history = dd.Panel("""
    pcsw.NotesByPerson #:60 #pcsw.LinksByPerson:20
    # lino.ChangesByMaster
    """,label = _("History"))
    
    general = dd.Panel("""
    client_info:30 box1:30 AppointmentsByGuest:40 box2:30
    box4 image:15
    """,label = _("General"))
    
    box1 = """
    checkin_for
    find_appointment 
    workflow_buttons
    """
    
    #~ box1 = dd.Panel("""
    #~ last_name first_name:15 title:10
    #~ address_column
    #~ """,label = _("Address"))
    
    box2 = dd.Panel("""
    email
    phone
    gsm
    """,label = _("Contact"))
    
    box3 = dd.Panel("""
    gender:10 birth_date age:10 
    birth_country birth_place nationality:15 national_id:15 
    """,label = _("Birth"))
    
    eid_panel = dd.Panel("""
    card_number:12 card_valid_from:12 card_valid_until:12 card_issuer:10 card_type:12
    """,label = _("eID card"))

    box4 = """
    box3
    eid_panel
    """
    
    def override_labels(self):
        return dict(
            card_number = _("number"),
            card_valid_from = _("valid from"),
            card_valid_until = _("valid until"),
            card_issuer = _("issued by"),
            card_type = _("eID card type"))
    
def fld2html(fld,value) :
    if value:
        return ("%s: " % f.verbose_name,E.b(value))
    return []
    
#~ class Clients(pcsw.Clients): # we don't want filter defaults nor create_event action
class Clients(dd.Table):
    model = 'pcsw.Client'
    column_names = "name_column address_column national_id workflow_buttons" 
    auto_fit_column_widths = True
    use_as_default_table = False
    required = dd.Required(user_groups='reception')
    detail_layout = ClientDetail()
    #~ editable = False

    read_beid = beid.BeIdReadCardAction()
    #~ find_by_beid = beid.FindByBeIdAction()
    
    quick_event = CreateGuestEvent()
    create_note = CreateNote()
    
    #~ @dd.virtualfield(dd.HtmlBox())
    #~ def eid_card(cls,self,ar):
        #~ for fldname in 'card_number card_valid_from card_valid_until card_issuer card_type'
        #~ fld2html()
        
    #~ @dd.virtualfield(dd.HtmlBox())
    @dd.displayfield()
    def client_info(cls,self,ar):
        elems = [self.get_salutation(nominative=True),E.br()]
        elems += [self.first_name,' ',E.b(self.last_name),E.br()]
        #~ lines = list(self.address_person_lines()) + list(self.address_location_lines())
        #~ lines = 
        #~ logger.info("20130805 %s", lines)
        elems += join_elems(list(self.address_location_lines()),sep=E.br) 
        #~ logger.info("20130805 %s", elems)
        #~ elems = []
        #~ for ln in lines:
            #~ if ln:   
                #~ if len(elems): 
                    #~ elems.append(E.br())
                #~ elems.append(ln)
        return E.div(*elems,style="font-size:18px;font-weigth:bold;vertical-align:bottom;text-align:middle")
    
    @dd.displayfield(_("Find appointment"))
    def find_appointment(cls,self,ar):
        elems = []
        for obj in self.coachings_by_client.all():
            sar = cal.CalendarPanel.request(subst_user=obj.user,current_project=self.pk)
            elems += [ar.href_to_request(sar,obj.user.username),' ']
        return E.div(*elems)
        
    @dd.displayfield(_("Checkin"))
    def checkin_for(cls,obj,ar):
        """
        """
        elems = []
        ba = cls.get_action_by_name('quick_event')
        for coaching in obj.coachings_by_client.all():
            u = coaching.user
            sar = ba.request(obj,action_param_values=dict(user=u))
            #~ logger.info("20130809 %s",sar.action_param_values)
            #~ elems += [ar.action_button(ba,obj,unicode(u),param_values=dict(user=u)),' ']
            kw = dict()
            kw.update(title=_("Create a quick event for this client with this coach."))
            elems += [ar.href_to_request(sar,u.username,**kw),' ']
            #~ elems += [unicode(u),' ']
        return E.div(*elems)


inherited_setup_main_menu = setup_main_menu

def setup_main_menu(site,ui,profile,main):
    m  = main.add_menu("reception",_(App.verbose_name))
    #~ m.add_separator("-")
    #~ m.add_action('reception.Clients','find_by_beid')
    m.add_action('reception.Clients')
    inherited_setup_main_menu(site,ui,profile,main)
