# -*- coding: UTF-8 -*-
## Copyright 2009-2012 Luc Saffre
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
Default settings of a Lino/Welfare site.

"""

import os
#~ import lino

from lino.apps.std.settings import *

class Lino(Lino):
    """
    """
    source_dir = os.path.dirname(__file__)
    title = "Lino/PCSW"
    #~ domain = "pcsw.saffre-rumma.net"
    help_url = "http://packages.python.org/lino-welfare"
    migration_module = 'lino_welfare.migrate'
    
    #~ project_model = 'contacts.Person'
    project_model = 'pcsw.Client'
    user_model = 'users.User'
    
    languages = ('de', 'fr', 'nl', 'en')
    
    #~ index_view_action = "pcsw.Home"
    
    remote_user_header = "REMOTE_USER"
    
    override_modlib_models = [
        'contacts.Partner', 'contacts.Person', 'contacts.Company',
        'households.Household'
        ]
        
    def get_app_source_file(self):
        return __file__
        
    def get_main_action(self,user):
        return self.modules.lino.Home.default_action
        
    def get_application_info(self):
        from lino_welfare import __version__, __url__
        return ("Lino/Welfare",__version__,__url__)
        
        
    anonymous_user_profile = '400'
    
    #~ def setup_user_profiles(self):
    def setup_choicelists(self):
        """
        This defines default user profiles for :mod:`lino_welfare`.
        """
        from lino import dd
        from django.utils.translation import ugettext_lazy as _
        dd.UserProfiles.reset('* office integ cbss newcomers debts')
        add = dd.UserProfiles.add_item
        add('100', _("Integration Agent"),          'U U U U _ _')
        add('110', _("Integration Agent (Senior)"), 'U M M U _ _')
        add('200', _("Newcomers consultant"),       'U U _ U U _')
        add('300', _("Debts consultant"),           'U U _ _ _ U')
        #~ add('400', _("Readonly Manager"),           'M M M M M M', readonly=True)
        add('400', _("Readonly User"),              'U U U U U U', readonly=True)
        add('500', _("CBSS only"),                  'U _ _ U _ _')
        add('900', _("Administrator"),              'A A A A A A',name='admin')
        
        #~ for p in dd.UserProfiles.items():
            #~ print 20120715, repr(p)
            
        
    def on_site_startup(self):
        """
        A Lino/Welfare site by default watches the changes to certain Client fields
        and to all Contract fields.
        """
        
        #~ self.modules.pcsw.Client.watch_changes('first_name last_name national_id client_state')
        self.modules.pcsw.Client.watch_changes()
        
        # ContractBase is abstract, so it's not under self.modules
        from lino_welfare.modlib.isip.models import ContractBase
        ContractBase.watch_changes()
        
                
            

    def setup_quicklinks(self,ui,user,tb):
        #~ tb.add_action(self.modules.contacts.Persons().detail)
        #~ tb.add_action(self.modules.contacts.Persons,'detail')
        #~ tb.add_action(self.modules.contacts.Persons,'detail')
        tb.add_action(self.modules.pcsw.Clients.detail_action)
        self.on_each_app('setup_quicklinks',ui,user,tb)
        
        tb.add_action(self.modules.pcsw.MyClients)
        tb.add_action(self.modules.isip.MyContracts)
        tb.add_action(self.modules.jobs.MyContracts)
        #~ tb.add_action(self.modules.pcsw.Home)
        
        
    def setup_menu(self,ui,user,main):
        from django.utils.translation import ugettext_lazy as _
        from django.db import models
        from lino.modlib.users.models import UserLevels
        
        m = main.add_menu("master",_("Master"))
        
        #~ m = main.add_menu("contacts",_("Contacts"))

        if user.profile.level:
            #~ m.add_action(self.modules.contacts.Companies)
            #~ m.add_action(self.modules.contacts.Persons)
            m.add_action(self.modules.pcsw.Clients)
            #~ m.add_action(self.modules.contacts.AllPartners)
        if user.profile.integ_level:
            m.add_action(self.modules.pcsw.MyPersonSearches)
            
        self.on_each_app('setup_master_menu',ui,user,m)
        
            
        if user.profile.level and not user.profile.readonly:
          
            m = main.add_menu("my",_("My menu"))
            #~ m.add_action('projects.Projects')
            m.add_action(self.modules.notes.MyNotes)
            
            self.on_each_app('setup_my_menu',ui,user,m)
            m.add_action(self.modules.lino.MyTextFieldTemplates)

        
        self.on_each_app('setup_main_menu',ui,user,main)
        
        m = main.add_menu("lst",_("Listings"))
        m.add_action(self.modules.jobs.JobsOverview)
        m.add_action(self.modules.pcsw.UsersWithClients)
        m.add_action(self.modules.pcsw.ClientsTest)
        
        if user.profile.level >= UserLevels.manager: # is_staff:
            cfg = main.add_menu("config",_("Configure"))
            
            self.on_each_app('setup_config_menu',ui,user,cfg)
            
            
            
        if user.profile.level >= UserLevels.manager: # is_staff:
          
            m = main.add_menu("explorer",_("Explorer"))
            
            self.on_each_app('setup_explorer_menu',ui,user,m)
            
            m.add_action(self.modules.properties.Properties)

        
        m = main.add_menu("site",_("Site"))
        self.modules.lino.setup_site_menu(self,ui,user,m)
        
        return main
      
    def get_reminder_generators_by_user(self,user):
        """
        Yield a list of objects susceptible to generate 
        automatic reminders for the specified user.
        Used by :func:`lino.modlib.cal.update_reminders`.
        """
        from lino.core.modeltools import models_by_abc
        from django.db.models import Q
        from lino_welfare.modlib.isip import models as isip
        
        #~ for obj in self.modules.contacts.Person.objects.filter(
          #~ Q(coach2=user)|Q(coach2__isnull=True,coach1=user)):
            #~ yield obj
        for obj in self.modules.pcsw.Coaching.objects.filter(
            user=user,primary=True):
            yield obj.project
        for obj in self.modules.uploads.Upload.objects.filter(user=user):
            yield obj
        for model in models_by_abc(isip.ContractBase):
            for obj in model.objects.filter(user=user):
                yield obj
                
                

LINO = Lino(__file__,globals())

#~ TIME_ZONE = 'Europe/Brussels'
TIME_ZONE = None


INSTALLED_APPS = (
  #~ 'django.contrib.auth',
  'django.contrib.contenttypes',
  #~ 'django.contrib.sessions',
  #~ 'django.contrib.sites',
  #~ 'django.contrib.markup',
  #~ 'lino.modlib.system',
  'lino',
  'lino.modlib.users',
  #~ 'lino.modlib.workflows',
  'lino.modlib.countries',
  #~ 'lino.modlib.documents',
  'lino.modlib.properties',
  'lino.modlib.contacts',
  #~ 'lino.modlib.projects',
  #~ 'lino.modlib.notes',
  #~ 'lino.modlib.links',
  'lino.modlib.uploads',
  #~ 'lino.modlib.thirds',
  'lino.modlib.outbox',
  'lino.modlib.cal',
  'lino.modlib.postings',
  'lino.modlib.households',
  'lino.modlib.accounts',
  
  'lino_welfare.modlib.cv',
  'lino_welfare.modlib.isip',
  'lino_welfare.modlib.jobs',
  'lino_welfare.modlib.newcomers',
  'lino_welfare.modlib.debts',
  'lino_welfare.modlib.courses',
  'lino_welfare.modlib.pcsw', # pcsw.demo creates clients needed by cbss.demo
  'lino_welfare.modlib.cbss',
  'lino.modlib.notes', # because demo fixture creates notes for Clients 
)


