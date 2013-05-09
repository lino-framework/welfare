# -*- coding: UTF-8 -*-
## Copyright 2009-2013 Luc Saffre
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

from lino.projects.std.settings import *
#~ from lino_welfare import __version__, __url__, __name__
#~ from lino_welfare.version import *
import lino_welfare
from lino_welfare.modlib import cbss
from lino.modlib import cal
from lino_welfare import SETUP_INFO

#~ class Site(Site,cal.SiteMixin,cbss.SiteMixin):
class Site(Site,cbss.SiteMixin):
  
    version = SETUP_INFO['version'] # lino_welfare.__version__
    url = SETUP_INFO['url'] # "http://code.google.com/p/lino-welfare/"
    #~ verbose_name = SETUP_INFO['name'] # "Lino Welfare"
    verbose_name = "Lino Welfare"
    #~ description = "a Lino application for Belgian Public Welfare Centres."
    #~ author = 'Luc Saffre'
    #~ author_email = 'luc.saffre@gmail.com'
    
    demo_fixtures = 'std few_countries few_cities few_languages props cbss democfg demo demo2 demo_events'.split()
    
    #~ title = label # __name__
    #~ domain = "pcsw.saffre-rumma.net"
    #~ help_url = "http://packages.python.org/lino-welfare"
    migration_module = 'lino_welfare.migrate'
    
    userdocs_prefix = 'welfare.'
    
    #~ project_model = 'contacts.Person'
    project_model = 'pcsw.Client'
    user_model = 'users.User'
    
    accounts_ref_length = 5
    
    #~ languages = ('de', 'fr', 'nl', 'en')
    languages = "de fr nl en"
    
    #~ index_view_action = "pcsw.Home"
    
    #~ remote_user_header = "REMOTE_USER"
    
    use_eid_jslib = True
    
    #~ admin_url = '/admin'
    
    #~ mergeable_models = [
        #~ 'pcsw.Client', 
        #~ 'contacts.Company',
        #~ 'households.Household'
        #~ ]
        
    override_modlib_models = [
        'contacts.Partner', 
        'contacts.Person', 
        'contacts.Company',
        'households.Household',
        'ui.SiteConfig'
        ]
        
        
    #~ def get_application_description(self):
        #~ import lino
        #~ s = """
        #~ %s is a customizable <a href="%s">Lino</a> application 
        #~ to be used in Belgian Public Centres for Social Welfare.
        #~ """ % (self.label,lino.__url__)
        #~ return s
        
    def get_main_action(self,user):
        return self.modules.lino.Home.default_action
        #~ a = self.modules.lino.Home.default_action
        #~ if a is None:
            #~ raise Exception("20121004 self.modules.lino.Home.get_url_action('default_action') returned None")
        #~ return a
        
    #~ def get_application_info(self):
        #~ return (__name__,__version__,__url__)
        
        
    
    #~ def setup_user_profiles(self):
    def setup_choicelists(self):
        """
        This defines default user profiles for :mod:`lino_welfare`.
        """
        from lino import dd
        from django.utils.translation import ugettext_lazy as _
        dd.UserProfiles.reset('* office integ cbss newcomers debts')
        add = dd.UserProfiles.add_item
        add('000', _("Anonymous"),                  '_ _ _ _ _ _', 
            name='anonymous', readonly=True,authenticated=False)
        add('100', _("Integration Agent"),          'U U U U _ _')
        add('110', _("Integration Agent (Senior)"), 'U M M U _ _')
        add('200', _("Newcomers consultant"),       'U U _ U U _')
        add('300', _("Debts consultant"),           'U U _ _ _ U')
        #~ add('400', _("Readonly Manager"),           'M M M M M M', readonly=True)
        #~ add('400', _("Readonly User"),              'U U U U U U', readonly=True)
        add('500', _("CBSS only"),                  'U _ _ U _ _')
        add('900', _("Administrator"),              'A A A A A A',name='admin')
        
        #~ for p in dd.UserProfiles.items():
            #~ print 20120715, repr(p)
            
        

    def setup_quicklinks(self,ar,tb):
        #~ tb.add_action(self.modules.contacts.Persons().detail)
        #~ tb.add_action(self.modules.contacts.Persons,'detail')
        #~ tb.add_action(self.modules.contacts.Persons,'detail')
        #~ tb.add_action(self.modules.pcsw.Clients.detail_action)
        tb.add_action('pcsw.Clients','detail')
        self.on_each_app('setup_quicklinks',ar,tb)
        
        tb.add_action(self.modules.pcsw.IntegClients)
        tb.add_action(self.modules.isip.MyContracts)
        tb.add_action(self.modules.jobs.MyContracts)
        #~ tb.add_action(self.modules.pcsw.Home)
        
        tb.add_action(self.modules.pcsw.Clients,'find_by_beid')
        
    def setup_menu(self,ui,profile,main):
        from django.utils.translation import ugettext_lazy as _
        from django.utils.translation import string_concat
        from django.db import models
        from lino import dd
        contacts = dd.resolve_app("contacts")
        
        #~ m = main.add_menu("contacts",_("Contacts"))
        #~ m = main.add_menu("contacts",contacts.MODULE_LABEL)
        #~ m.add_action(self.modules.pcsw.Clients)

        #~ if user.profile.level:
            #~ m.add_action(self.modules.contacts.Companies)
            #~ m.add_action(self.modules.contacts.Persons)
            #~ m.add_action(self.modules.contacts.AllPartners)
            
        m = main.add_menu("master",_("Master"))
        self.on_each_app('setup_master_menu',ui,profile,m)
        
        #~ if user.profile.integ_level:
            #~ m = main.get_item("contacts")
            #~ m.add_action(self.modules.pcsw.MyPersonSearches)
            
            
        if profile.level and not profile.readonly:
          
            m = main.add_menu("my",_("My menu"))
            #~ m.add_action('projects.Projects')
            #~ m.add_action(self.modules.notes.MyNotes)
            
            self.on_each_app('setup_my_menu',ui,profile,m)
            #~ m.add_action(self.modules.lino.MyTextFieldTemplates)

        
        self.on_each_app('setup_main_menu',ui,profile,main)
        
        m = main.get_item("contacts")
        m.clear()
        m.add_action(self.modules.contacts.Persons)
        m.add_action(self.modules.pcsw.Clients,label=string_concat(u' \u25b6 ',self.modules.pcsw.Clients.label))
        m.add_action(self.modules.pcsw.Clients,'find_by_beid')
        m.add_action(self.modules.contacts.Companies)
        m.add_action(self.modules.households.Households)
        m.add_separator('-')
        m.add_action(self.modules.contacts.Partners,label=_("Partners (all)"))
        
        m = main.add_menu("reports",_("Listings"))
        self.on_each_app('setup_reports_menu',ui,profile,m)
        
        #~ if profile.level >= dd.UserLevels.manager: # is_staff:
        cfg = main.add_menu("config",_("Configure"))
        self.on_each_app('setup_config_menu',ui,profile,cfg)
            
            
            
        #~ if profile.level >= dd.UserLevels.manager: # is_staff:
          
        m = main.add_menu("explorer",_("Explorer"))
        self.on_each_app('setup_explorer_menu',ui,profile,m)
        m.add_action(self.modules.properties.Properties)

        
        m = main.add_menu("site",_("Site"))
        #~ self.modules.lino.setup_site_menu(self,ui,user,m)
        self.on_each_app('setup_site_menu',ui,profile,m)
        
        return main
      
    #~ def get_reminder_generators_by_user(self,user):
        #~ """
        #~ Yield a list of objects susceptible to generate 
        #~ automatic reminders for the specified user.
        #~ Used by :func:`lino.modlib.cal.update_reminders`.
        #~ """
        #~ from lino.core.dbutils import models_by_base
        #~ from django.db.models import Q
        #~ from lino_welfare.modlib.isip import models as isip
        
        #~ for obj in self.modules.pcsw.Coaching.objects.filter(
            #~ user=user,primary=True):
            #~ yield obj.project
        #~ for obj in self.modules.uploads.Upload.objects.filter(user=user):
            #~ yield obj
        #~ for model in models_by_base(isip.ContractBase):
            #~ for obj in model.objects.filter(user=user):
                #~ yield obj
                
    def get_installed_apps(self):
        for a in super(Site,self).get_installed_apps():
            yield a
            
        yield 'django.contrib.contenttypes'
        yield 'lino.modlib.users'
        yield 'lino.modlib.changes'
        #~ yield 'lino.modlib.codechanges'
        #~ yield 'lino.modlib.pages'
        #~ 'lino.modlib.workflows'
        yield 'lino.modlib.countries'
        #~ 'lino.modlib.documents'
        yield 'lino.modlib.properties'
        yield 'lino.modlib.contacts'
        #~ 'lino.modlib.projects'
        #~ 'lino.modlib.notes',
        #~ 'lino.modlib.links',
        yield 'lino.modlib.uploads'
        #~ 'lino.modlib.thirds'
        yield 'lino.modlib.outbox'
        yield 'lino.modlib.cal'
        yield 'lino.modlib.postings'
        yield 'lino.modlib.households'
        yield 'lino.modlib.accounts'
        
        yield 'lino_welfare'
        yield 'lino_welfare.modlib.statbel'
        # NOTE: ordering influences (1) main menu (2) fixtures loading
        yield 'lino_welfare.modlib.pcsw' # pcsw.demo creates clients needed by cbss.demo
        yield 'lino_welfare.modlib.cv'
        yield 'lino_welfare.modlib.isip'
        yield 'lino_welfare.modlib.jobs'
        yield 'lino_welfare.modlib.courses'
        yield 'lino_welfare.modlib.newcomers'
        yield 'lino_welfare.modlib.debts'
        yield 'lino_welfare.modlib.cbss'
        yield 'lino.modlib.notes' # notes demo fixture creates notes for Clients 
      
    #~ def get_urls(self):
        #~ from django.conf.urls.defaults import patterns
        #~ rx = '^'
        #~ urlpatterns = patterns('')
        #~ if self.use_eid_jslib:
            #~ from lino_welfare import beid
            #~ urlpatterns += patterns('',
                #~ (rx+r'eid-jslib$', beid.EidJSlib.as_view()),
            #~ )
        #~ return urlpatterns
        

SITE = Site(globals())

LOGGING['logger_names'] = 'djangosite north lino lino_welfare'
#~ LOGGING.update(loggers='djangosite north lino lino_welfare')
#~ print 20130409, __file__, LOGGING

#~ TIME_ZONE = 'Europe/Brussels'
#~ TIME_ZONE = None
