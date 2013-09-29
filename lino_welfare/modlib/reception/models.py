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
The :xfile:`models.py` for :mod:`lino_welfare.modlib.reception`.
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
dd.inject_field('system.SiteConfig','attestation_note_nature',
    dd.ForeignKey('notes.EventType',
        verbose_name=_("Event type of attestations"),
        null=True,blank=True,
        related_name="attestation_siteconfig_set"))

        
    
class CreateClientVisit(dd.Action): 
    sort_index = 91
    icon_name = 'hourglass'
    #~ icon_file = 'hourglass.png'
    label = _("Create visit")
    #~ show_in_workflow = True
    #~ show_in_row_actions = True
    parameters = dict(
        #~ date=models.DateField(_("Date"),blank=True,null=True),
        user=dd.ForeignKey(settings.SITE.user_model),
        summary=models.CharField(verbose_name=_("Reason"),blank=True))
    params_layout = """
    user 
    summary
    """
    def run_from_ui(self,ar,**kw):
        obj = ar.selected_rows[0]
        event = create_prompt_event(obj,obj,
            ar.action_param_values.user,
            ar.action_param_values.summary,
            settings.SITE.site_config.client_guestrole)
        #~ kw = super(CreateVisit,self).run_from_ui(obj,ar,**kw)
        kw.update(success=True)
        #~ kw.update(eval_js=ar.renderer.instance_handler(ar,event))
        kw.update(refresh=True)
        return kw
        
class CreateCoachingVisit(CreateClientVisit): 
    
    help_text = _("Create a prompt event for this client with this coach.")
    
    def action_param_defaults(self,ar,obj,**kw):
        kw = super(CreateCoachingVisit,self).action_param_defaults(ar,obj,**kw)
        if obj is not None:
            kw.update(user=obj.user)
        return kw
        
    def run_from_ui(self,ar,**kw):
        obj = ar.selected_rows[0]
        event = create_prompt_event(obj.client,obj.client,
            ar.action_param_values.user,
            ar.action_param_values.summary,
            settings.SITE.site_config.client_guestrole)
        #~ kw = super(CreateVisit,self).run_from_ui(obj,ar,**kw)
        kw.update(success=True)
        #~ kw.update(eval_js=ar.renderer.instance_handler(ar,event))
        kw.update(refresh=True)
        return kw
        

        
    
class CreateNote(dd.Action): 
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
    
    def run_from_ui(self,ar,**kw):
        obj = ar.selected_rows[0]
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
            
            
class ButtonsTable(dd.VirtualTable):
    column_names = 'button'
    auto_fit_column_widths = True
    window_size = (60,20)
    hide_top_toolbar = True
    
    @dd.displayfield(_("Button"))
    def button(self,obj,ar):
        return obj
        
class CreateNoteActionsByClient(ButtonsTable):
    sort_index = 94
    master = 'pcsw.Client'
    label = _("Issue attestation")
    icon_name = 'script'
    #~ icon_file = 'script.png'
    
    @classmethod
    def get_title(self,ar):
        s = super(CreateNoteActionsByClient,self).get_title(ar)
        if ar.master_instance is not None:
            s += _(" for %s") % ar.master_instance
        return s
        
    @classmethod
    def get_data_rows(self,ar=None):
        if ar.master_instance is None: return
        sar = ar.spawn(notes.NotesByProject,master_instance=ar.master_instance)
        for nt in notes.NoteType.objects.filter(is_attestation=True):
            btn = sar.insert_button(unicode(nt),
                dict(type=nt,event_type=settings.SITE.site_config.attestation_note_nature),
                title=_("Create a %s for this client.") % nt,
                icon_name=None)
            if btn is not None:
                yield btn

        
class CreateEventActionsByClient(ButtonsTable):
    sort_index = 93
    master = 'pcsw.Client'
    label = _("Find date with...")
    icon_name = 'calendar'
    #~ icon_file = 'calendar.png'
    
    @classmethod
    def get_title(self,ar):
        s = super(CreateEventActionsByClient,self).get_title(ar)
        if ar.master_instance is not None:
            s += _(" for %s") % ar.master_instance
        return s
        
    @classmethod
    def get_data_rows(self,ar=None):
        if ar.master_instance is None: return
        for user in settings.SITE.user_model.objects.exclude(profile__isnull=True):
            #~ sar = cal.CalendarPanel.request(
                #~ renderer=settings.SITE.ui.ext_renderer,
                #~ subst_user=user,
                #~ current_project=ar.master_instance.pk)
            
            sar = ar.spawn(cal.CalendarPanel.default_action,
                current_project=ar.master_instance.pk,subst_user=user)
            btn = sar.as_button(unicode(user))
            
            if btn is not None:
                yield btn
            

    
class ClientDetail(dd.FormLayout):
    
    main = "general contact history"
    
    general = dd.Panel("""
    client_info:30 image:15 box3:20 box3c
    AppointmentsByPartner:30 reception.CoachingsByClient:40
    """,label = _("General"))
    
    history = dd.Panel("""
    # create_note_actions:30 pcsw.NotesByPerson:60
    CreateNoteActionsByClient:30 pcsw.NotesByPerson:60
    """,label = _("History"))
    
    contact = dd.Panel("""
    contact1 box2:20 
    pcsw.ContactsByClient
    """,label = _("Contact"))
    
    #~ box1 = """
    #~ create_visit_actions
    #~ find_appointment
    #~ workflow_buttons
    #~ """
    
    #~ box1 = dd.Panel("""
    #~ last_name first_name:15 title:10
    #~ address_column
    #~ """,label = _("Address"))
    
    contact1 = """
    country city zip_code
    street street_no street_box
    addr2
    """
    
    box2 = """
    email
    phone
    gsm
    """
    
    box3 = """
    birth_date 
    age
    gender
    birth_country 
    birth_place 
    """
    box3c = """
    national_id
    gesdos_id
    nationality
    # eid_info
    """
    
    #~ eid_panel = dd.Panel("""
    #~ card_number:12 card_valid_from:12 card_valid_until:12 card_issuer:10 card_type:12
    #~ """,label = _("eID card"))

    
    #~ def override_labels(self):
        #~ return dict(
            #~ card_number = _("number"),
            #~ card_valid_from = _("valid from"),
            #~ card_valid_until = _("valid until"),
            #~ card_issuer = _("issued by"),
            #~ card_type = _("eID card type"))
    
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
    print_eid_content = None

    #~ read_beid = beid.BeIdReadCardAction()
    #~ find_by_beid = beid.FindByBeIdAction()
    
    create_note_actions = dd.ShowSlaveTable(CreateNoteActionsByClient)
    create_event_actions = dd.ShowSlaveTable(CreateEventActionsByClient)
    
    create_visit = CreateClientVisit()
    #~ create_note = CreateNote()
    
    @classmethod
    def param_defaults(self,ar,**kw):
        kw = super(Clients,self).param_defaults(ar,**kw)
        kw.update(client_state=None)
        kw.update(observed_event=pcsw.ClientEvents.active)
        return kw
        
        
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
                
        elems = [E.div(*elems,style="font-size:18px;font-weigth:bold;vertical-align:bottom;text-align:middle")]
        
        elems.append(E.br())
        elems.append(self.eid_info(ar))
        elems = [E.div(*elems)]
                
        #~ if not self.has_valid_card_data():
            #~ ba = cls.get_action_by_name('read_beid')
            #~ elems.append(E.br())
            #~ elems.append(ar.action_button(ba,self,_("Must read eID card!")))
            #~ elems.append(E.br())
            #~ elems = [E.div(*elems)]
                
        return elems
    

#~ pcsw.Coaching.define_action(create_visit=CreateCoachingVisit())
dd.inject_action('pcsw.Coaching',create_visit=CreateCoachingVisit())

class CoachingsByClient(pcsw.CoachingsByClient):
    label = _("Coaches")
    filter = models.Q(end_date__isnull=True)
    column_names = "user primary type actions"
    
    #~ @classmethod
    #~ def get_data_rows(self,ar=None):
        #~ for obj in self.get_request_queryset(ar): 
            #~ yield obj
        #~ if ar.master_instance:
            #~ yield pcsw.Coaching(client=ar.master_instance)
    
    @dd.displayfield(_("Actions"))
    def actions(cls,obj,ar):
        elems = []
        elems += [ar.instance_action_button(obj.create_visit,_("Visit"),icon_name=CreateClientVisit.icon_name),' ']
        
        #~ ba = cls.get_action_by_name('create_visit')
        #~ u = obj.user
        #~ sar = ba.request(obj) # ,action_param_values=dict(user=u))
        #~ kw = dict()
        #~ kw.update(title=)
        #~ elems += [ar.href_to_request(sar,**kw),' ']
        
        if obj.user.profile is not None:
            sar = cal.CalendarPanel.request(
                subst_user=obj.user,
                current_project=obj.client.pk)
            elems += [ar.href_to_request(sar,_("Find date"),
                title=_("Find date"),
                icon_name=CreateEventActionsByClient.icon_name),' ']
            #~ icon_name = 'x-tbar-calendar'
            #~ icon_file = 'calendar.png'

        
        return E.div(*elems)


"""
Override library :mod:`WaitingVisitors <lino.modlib.reception.WaitingVisitors>` 
table to change one behaviour:  when clicking in that table 
on the partner, Lino-Welfare should show the *Client's* and not 
the *Partner's*  detail.    
"""
        
if False: # doesn't work
    
    def partner2client(self,obj,ar):
        return pcsw.Client.objects.get(pk=obj.partner.pk)
    WaitingVisitors.virtual_fields['partner'].override_getter(partner2client)

if False: # doesn't work
    WaitingVisitors.partner = dd.VirtualField(dd.ForeignKey('pcsw.Client'),partner2client)
    MyWaitingVisitors.partner = dd.VirtualField(dd.ForeignKey('pcsw.Client'),partner2client)

if True: # works, though is very hackerish
    
    def func(obj,ar):
        return pcsw.Client.objects.get(pk=obj.partner.pk)
    dd.inject_field('cal.Guest','client',dd.VirtualField(dd.ForeignKey('pcsw.Client'),func))
    for T in WaitingVisitors, MyWaitingVisitors:
        T.column_names = T.column_names.replace('partner','client')
        T.detail_layout = T.detail_layout.replace('partner','client')
    
    #~ class WaitingVisitors(WaitingVisitors): 
        #~ label = WaitingVisitors.label
    
if False: # works, but is very stupid
    
  class WaitingVisitors(WaitingVisitors): 
    # labels are not automatically inherited. Must inherit manually
    label = WaitingVisitors.label 
    
    @dd.virtualfield(dd.ForeignKey('pcsw.Client'))
    def partner(self,obj,ar):
        return pcsw.Client.objects.get(pk=obj.partner.pk)


  #~ The same for MyWaitingVisitors. See :blogref:`20130817`
  class MyWaitingVisitors(MyWaitingVisitors): 
    # labels are not automatically inherited. Must inherit manually
    label = MyWaitingVisitors.label 
    
    @dd.virtualfield(dd.ForeignKey('pcsw.Client'))
    def partner(self,obj,ar):
        return pcsw.Client.objects.get(pk=obj.partner.pk)
        

inherited_setup_main_menu = setup_main_menu

def setup_main_menu(site,ui,profile,main):
    m  = main.add_menu("reception",App.verbose_name)
    #~ m.add_separator("-")
    #~ m.add_action('reception.Clients','find_by_beid')
    m.add_action('reception.Clients')
    inherited_setup_main_menu(site,ui,profile,main)
