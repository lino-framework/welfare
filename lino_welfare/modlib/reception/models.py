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
notes = dd.resolve_app('notes')

dd.inject_field('notes.NoteType','is_attestation',models.BooleanField(_("attestation"),default=False))

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
        def ok():
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
        if obj.has_valid_card_data():
            return ok()
        return ar.confirm(ok,_("Client has no valid eID data!",
            _("Do you still want to issue an attestation?")))

    
class ClientDetail(dd.FormLayout):
    
    main = "general history pcsw.ContactsByClient"
    
    history = dd.Panel("""
    create_note_actions:30 pcsw.NotesByPerson:60
    """,label = _("History"))
    
    general = dd.Panel("""
    client_info:30 box1:30 AppointmentsByGuest:40 box2:30
    box4 image:15
    """,label = _("General"))
    
    box1 = """
    create_visit_actions
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
    
#~ class Clients(dd.Table):
class Clients(pcsw.Clients): # see blog 2013/0817
    #~ model = 'pcsw.Client'
    column_names = "name_column address_column national_id workflow_buttons" 
    auto_fit_column_widths = True
    use_as_default_table = False
    required = dd.Required(user_groups='reception')
    detail_layout = ClientDetail()
    #~ insert_layout = pcsw.Clients.insert_layout.main # manually inherited
    #~ editable = False
    #~ parameters = None # don't inherit filter parameters
    #~ params_layout = None # don't inherit filter parameters
    #~ params_panel_hidden = True
    create_event = None # don't inherit this action

    read_beid = beid.BeIdReadCardAction()
    #~ find_by_beid = beid.FindByBeIdAction()
    
    create_visit = CreateVisit()
    #~ create_note = CreateNote()
    
    #~ @dd.virtualfield(dd.HtmlBox())
    #~ def eid_card(cls,self,ar):
        #~ for fldname in 'card_number card_valid_from card_valid_until card_issuer card_type'
        #~ fld2html()
        
    #~ @classmethod
    #~ def get_title_tags(self,ar):
        #~ return []
        #~ 
    #~ @classmethod
    #~ def get_request_queryset(self,ar):
        #~ return super(pcsw.Clients,self).get_request_queryset(ar) # skip one parent
        #~ return dd.Table.get_request_queryset(ar)
        
        
    #~ @dd.virtualfield(dd.HtmlBox())
    @dd.displayfield()
    def client_info(cls,self,ar):
        elems = [self.get_salutation(nominative=True),E.br()]
        #~ elems += [self.first_name,' ',E.b(self.last_name),E.br()]
        elems += [self.first_name,' ',ar.obj2html(self,self.last_name),E.br()]
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
    
    @dd.displayfield(create_visit.label)
    def create_visit_actions(cls,obj,ar):
        elems = []
        ba = cls.get_action_by_name('create_visit')
        for coaching in obj.coachings_by_client.all():
            u = coaching.user
            sar = ba.request(obj,action_param_values=dict(user=u))
            #~ logger.info("20130809 %s",sar.action_param_values)
            kw = dict()
            kw.update(title=_("Create a spot visit for this client with this coach."))
            elems += [ar.href_to_request(sar,u.username,**kw),' ']
        return E.div(*elems)

    @dd.virtualfield(dd.HtmlBox(_("Issue attestation")))
    def create_note_actions(cls,obj,ar):
        elems = []
        if not obj.has_valid_card_data():
            elems.append(E.b(_("Must read eID card!"),E.br()))
            ba = cls.get_action_by_name('read_beid')
            elems.append(E.br())
            elems.append(ar.action_button(ba,obj))
            elems.append(E.br())
        sar = ar.spawn(notes.NotesByProject,master_instance=obj)
        for nt in notes.NoteType.objects.filter(is_attestation=True):
            btn = sar.insert_button(unicode(nt),dict(type=nt),
                title=_("Create a %s for this client.") % nt,
                icon_file=None)
            if btn is not None:
                elems += [btn,E.br()]
            
        return E.div(*elems,style="background-color:red !important;height:auto !important")
        #~ return E.div(*elems)
        
        
        
class WaitingGuests(WaitingGuests): 
    """
    Overrides the library `reception.WaitingGuests` to change one behaviour:    
    when clicking in that table 
    on the partner, Lino-Welfare should show the *Client's* and not 
    the *Partner's*  detail.    
    """
    # labels are not automatically inherited. Must inherit manually
    label = WaitingGuests.label 
    
    @dd.virtualfield(dd.ForeignKey('pcsw.Client'))
    def partner(self,obj,ar):
        return pcsw.Client.objects.get(pk=obj.partner.pk)
        
    
        
#~ class ExpectedGuests(ExpectedGuests): 
    #~ 
    #~ @dd.virtualfield(dd.ForeignKey('pcsw.Client'))
    #~ def partner(self,obj,ar):
        #~ return obj.partner
    
        


inherited_setup_main_menu = setup_main_menu

def setup_main_menu(site,ui,profile,main):
    m  = main.add_menu("reception",_(App.verbose_name))
    #~ m.add_separator("-")
    #~ m.add_action('reception.Clients','find_by_beid')
    m.add_action('reception.Clients')
    inherited_setup_main_menu(site,ui,profile,main)
