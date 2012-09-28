# -*- coding: UTF-8 -*-
## Copyright 2012 Luc Saffre
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

import os
import sys
import cgi
import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db import IntegrityError
from django.utils.encoding import force_unicode


from lino import tools
from lino import dd
#~ from lino.utils.babel import default_language
#~ from lino import reports
#~ from lino import layouts
from lino.core.perms import UserProfiles
from lino.utils.restify import restify
#~ from lino.utils import printable
from lino.utils.choosers import chooser
from lino.utils import babel
from lino import mixins
from django.conf import settings
#~ from lino import choices_method, simple_choices_method
#~ from lino.modlib.contacts import models as contacts
from lino.modlib.users import models as users
from lino.modlib.cal.utils import amonthago


#~ from lino_welfare.models import Person
#~ from lino_welfare.modlib.pcsw import models as welfare
from lino_welfare.modlib.pcsw import models as pcsw

MODULE_LABEL = _("Newcomers")

class Broker(dd.Model):
    """
    A Broker (Vermittler) is an external institution 
    who suggests newcomers.
    """
    class Meta:
        verbose_name = _("Broker")
        verbose_name_plural = _("Brokers")
        
    name = models.CharField(max_length=200)
    
    def __unicode__(self):
        return self.name

class Brokers(dd.Table):
    """
    List of Brokers on this site.
    """
    required=dict(user_groups=['newcomers'],user_level='manager')
    #~ required_user_level = UserLevels.manager
    model = Broker
    column_names = 'name *'
    order_by = ["name"]



class Faculty(babel.BabelNamed):
    """
    A Faculty (Fachbereich) is a conceptual (not organizational)
    department of this PCSW. 
    Each Newcomer will be assigned to one and only one Faculty, 
    based on his/her needs.
    
    """
    class Meta:
        verbose_name = _("Faculty")
        verbose_name_plural = _("Faculties")
    #~ body = babel.BabelTextField(_("Body"),blank=True,format='html')
    

class Faculties(dd.Table):
    required=dict(user_groups=['newcomers'],user_level='manager')
    #~ required_user_groups = ['newcomers']
    #~ required_user_level = UserLevels.manager
    model = Faculty
    column_names = 'name *'
    order_by = ["name"]
    detail_template = """
    id name
    CompetencesByFaculty
    ClientsByFaculty
    """

class Competence(mixins.AutoUser,mixins.Sequenced):
    """
    Deserves more documentation.
    """
    class Meta:
        #~ abstract = True
        verbose_name = _("Competence") 
        verbose_name_plural = _("Competences")
        
    faculty = models.ForeignKey(Faculty)
    
    def __unicode__(self):
        return u'%s #%s' % (self._meta.verbose_name,self.pk)
        
class Competences(dd.Table):
    required = dict(user_groups=['newcomers'],user_level='manager')
    #~ required_user_groups = ['newcomers']
    #~ required_user_level = UserLevels.manager
    model = Competence
    column_names = 'id *'
    order_by = ["id"]

class CompetencesByUser(Competences):
    #~ required = dict(user_groups=['newcomers'])
    required = dict()
    #~ required_user_level = None
    master_key = 'user'
    column_names = 'seqno faculty *'
    order_by = ["seqno"]

class CompetencesByFaculty(Competences):
    master_key = 'faculty'
    column_names = 'user *'
    order_by = ["user"]


class MyCompetences(mixins.ByUser,CompetencesByUser):
    pass

    
#~ class Newcomers(pcsw.Clients):
    #~ """
    #~ Clients who have the "Newcomer" checkbox on.
    #~ """
    #~ required = dict(user_groups=['newcomers'])
    
    #~ use_as_default_table = False
    #~ column_names = "name_column broker faculty address_column *"
    
    #~ label = _("Newcomers")
    
    #~ @classmethod
    #~ def param_defaults(self,ar,**kw):
        #~ kw = super(Newcomers,self).param_defaults(ar,**kw)
        #~ kw.update(client_state=pcsw.ClientStates.newcomer)
        #~ kw.update(coached_on=None)
        #~ return kw
        
    
        
#~ class NewcomersByFaculty(Newcomers):
    #~ master_key = 'faculty'
    #~ column_names = "name_column broker address_column *"
        
class NewClientDetail(pcsw.ClientDetail):
    main = pcsw.ClientDetail.main + " newcomers"
    
    newcomers = dd.Panel("""
    broker:12 faculty:12  
    client_state workflow_buttons
    AvailableCoachesByClient
    """,label=_(MODULE_LABEL))
    

class NewClients(pcsw.Clients):
    required=dict(user_groups=['newcomers'])
    #~ required_user_groups = ['newcomers']
    label = _("New Clients")
    use_as_default_table = False
    
    detail_layout = NewClientDetail()
    
    column_names = "name_column:20 client_state broker faculty national_id:10 gsm:10 address_column age:10 email phone:10 id bank_account1 aid_type language:10 *"
    
    #~ @classmethod
    #~ def param_defaults(self,ar,**kw):
        #~ kw = super(NewClients,self).param_defaults(ar,**kw)
        #~ kw.update(new_since=amonthago())
        #~ return kw
        
        
    parameters = dict(
      also_refused = models.BooleanField(_("Also refused clients"),default=False),
      also_obsolete = models.BooleanField(_("Also obsolete clients"),default=False),
      #~ new_since = models.DateField(_("New clients since"),blank=True),
      new_since = models.DateField(_("Also newly coached clients since"),default=amonthago,blank=True,null=True),
      coached_by = models.ForeignKey(users.User,blank=True,null=True,
          verbose_name=_("Coached by")),
      )
    params_layout = 'also_refused also_obsolete new_since coached_by'
    
    @classmethod
    def get_request_queryset(self,ar):
        # Note that we skip pcsw.Clients mro parent
        qs = super(NewClients,self).get_request_queryset(ar)
        
        q = models.Q(client_state__in=(pcsw.ClientStates.new,pcsw.ClientStates.refused))
        if ar.param_values.new_since:
            q = q | models.Q(
                client_state=pcsw.ClientStates.coached,
                pcsw_coaching_set_by_project__start_date__gte=ar.param_values.new_since)
        qs = qs.filter(q)

        if ar.param_values.coached_by:
            qs = pcsw.only_coached_by(qs,ar.param_values.coached_by)
        if not ar.param_values.also_obsolete:
            qs = qs.filter(is_deprecated=False)
        #~ if not ar.param_values.also_refused:
            #~ qs = qs.filter(client_status=False)
        #~ logger.info('20120914 Clients.get_request_queryset --> %d',qs.count())
        return qs

    @classmethod
    def get_title(self,ar):
        #~ title = super(Clients,self).get_title(ar)
        title = pcsw.Client._meta.verbose_name_plural
        #~ if ar.param_values.new_since:
            #~ title = _("New clients since") + ' ' + str(ar.param_values.new_since)
            #~ title += _(" new since ") + str(ar.param_values.new_since)
        #~ if ar.param_values.coached_by:
            #~ title += _(" of ") + unicode(ar.param_values.coached_by)
        #~ if ar.param_values.coached_on:
            #~ title += _(" on ") + babel.dtos(ar.param_values.coached_on)
        tags = []
        #~ if ar.param_values.client_state:
            #~ tags.append(unicode(ar.param_values.client_state))
        if ar.param_values.also_refused:
            tags.append(unicode(_("refused")))
        if ar.param_values.also_obsolete:
            tags.append(unicode(_("obsolete")))
        if ar.param_values.new_since:
            tags.append(unicode(_("new since")) + ' ' + babel.dtos(ar.param_values.new_since))
        if len(tags):
            title += " (%s)" % (', '.join(tags))
        return title
        
        
class ClientsByFaculty(NewClients):
    master_key = 'faculty'
    column_names = "name_column broker address_column *"
    
    
        
#~ class UsersByNewcomer(dd.VirtualTable):
#~ class UsersByNewcomer(dd.Table):
#~ class UsersByNewcomer(users.Users):
class AvailableCoaches(users.Users):
    """
    A list of the Users that are susceptible to become responsible for a Newcomer.
    """
    use_as_default_table = False
    
    required = dict(user_groups=['newcomers'])
    #~ required_user_groups = ['newcomers']
    #~ model = users.User
    editable = False # even root should not edit here
    #~ filter = models.Q(profile__in=[p for p in UserProfiles.items() if p.integ_level])
    #~ label = _("Users by Newcomer")
    label = _("Available Coaches")
    column_names = 'name_column primary_clients active_clients new_clients newcomer_quota newcomer_score'
    parameters = dict(
        for_client = models.ForeignKey('contacts.Person',
            verbose_name=_("Show suggested agents for"),
            blank=True),
        since = models.DateField(_("Count Newcomers since"),
            blank=True,default=amonthago),
    )
    params_layout = "for_client since"
    
    @chooser()
    def for_client_choices(cls):
        return Newcomers.request().data_iterator
        
    @classmethod
    def get_request_queryset(self,ar):
        profiles = [p for p in UserProfiles.items() if p.integ_level]
        return super(AvailableCoaches,self,ar).filter(models.Q(profile__in=profiles))
        
        
    #~ @classmethod
    #~ def get_permission(self,action,user):
        #~ return isinstance(p.actors.ReadPermission)
        #~ return True
        
        
    @classmethod
    def get_data_rows(self,ar):
        """
        We only want the users who actually have at least one client.
        We store the corresponding request in the user object 
        under the name `my_persons`.
        """
        qs = super(AvailableCoaches,self).get_request_queryset(ar)
        for user in qs:
            if ar.param_values.for_client:
                r = Competence.objects.filter(user=user,faculty=ar.param_values.for_client.faculty)
                if r.count() == 0:
                    continue
            #~ else:
                #~ logger.info("20120928 AvailableCoaches.get_data_rows : no for_client")
            user.new_clients = NewClients.request(
              ar.ui,param_values=dict(
                coached_by=user,
                new_since=ar.param_values.since))
            yield user
                
    #~ @dd.virtualfield('contacts.Person.coach1')
    #~ def user(self,obj,ar):
        #~ return obj
        
    @dd.requestfield(_("Primary clients"))
    def primary_clients(self,obj,ar):
        #~ return pcsw.ClientsByCoach1.request(ar.ui,master_instance=obj)
        return pcsw.CoachingsByUser.request(ar.ui,master_instance=obj)
        
    @dd.requestfield(_("Active clients"))
    def active_clients(self,obj,ar):
        #~ return pcsw.MyActiveClients.request(ar.ui,subst_user=obj)
        return pcsw.IntegClients.request(ar.ui,param_values=dict(coached_by=obj,only_active=True))
        
    @dd.requestfield(_("New Clients"))
    def new_clients(self,obj,ar):
        return obj.new_clients
        
    @dd.virtualfield(models.IntegerField(_("Score")))
    def newcomer_score(self,obj,ar):
        if obj.new_clients.get_total_count():
            return 100 * obj.newcomer_quota / obj.new_clients.get_total_count()
        else:
            return None
        

class AvailableCoachesByClient(AvailableCoaches):
    #~ master_key = 'for_client'
    master = pcsw.Client

    @classmethod
    def get_data_rows(self,ar):
        ar.param_values.for_client = ar.master_instance
        return super(AvailableCoachesByClient,self).get_data_rows(ar)
        
    @dd.action(label=_("Attribute"))
    def attribute_coach(obj,ar):
        client = ar.master_instance
        pcsw.Coaching(project=client,user=obj,start_date=datetime.date.today()).save()
        client.client_state = pcsw.ClientStates.coached
        client.save()
        msg = _("Client %(client)s now coached by %(user)s") % dict(client=client,user=obj)
        return ar.success_response(refresh=True,message=msg,alert=True)
        
        








#~ settings.LINO.add_user_field('newcomers_level',UserLevels.field(MODULE_LABEL))
#~ settings.LINO.add_user_group('newcomers',MODULE_LABEL)
settings.LINO.add_user_field('newcomer_quota',models.IntegerField(
          _("Newcomers Quota"),
          default=0,
          help_text="""Relative number expressing 
          how many Newcomer requests this User is able to treat."""
        ))


dd.inject_field(pcsw.Client,
    'broker',
    models.ForeignKey(Broker,
        blank=True,null=True),
    """The Broker who sent this Newcomer.
    """)
dd.inject_field(pcsw.Client,
    'faculty',
    models.ForeignKey(Faculty,
        blank=True,null=True),
    """The Faculty this client has been attributed to.
    """)

def site_setup(site):
    site.modules.users.Users.add_detail_tab('newcomers.CompetencesByUser')
  
def setup_main_menu(site,ui,user,m):
    #~ if user.profile.newcomers_level < UserLevels.user:
        #~ return
    m  = m.add_menu("newcomers",MODULE_LABEL)
    #~ m.add_action(Newcomers)
    m.add_action(NewClients)
    m.add_action(AvailableCoaches)
            
  
def setup_master_menu(site,ui,user,m): pass
  
def setup_my_menu(site,ui,user,m): 
    pass
    
def setup_config_menu(site,ui,user,m): 
    #~ if user.profile.newcomers_level < UserLevels.manager:
        #~ return
    m  = m.add_menu("newcomers",MODULE_LABEL)
    m.add_action(Brokers)
    m.add_action(Faculties)
  
def setup_explorer_menu(site,ui,user,m):
    #~ if user.profile.newcomers_level < UserLevels.manager:
        #~ return
    m.add_action(Competences)
  
dd.add_user_group('newcomers',MODULE_LABEL)
  