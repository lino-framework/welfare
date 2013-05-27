# -*- coding: UTF-8 -*-
## Copyright 2008-2013 Luc Saffre
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
Contains PCSW-specific models and tables that have not yet been 
moved into a separate module because they are really very PCSW specific.

"""
from __future__ import unicode_literals

import logging
logger = logging.getLogger(__name__)

import base64
import os
import cgi
import datetime

from django.db import models
from django.db.models import Q
from django.db.utils import DatabaseError
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.exceptions import MultipleObjectsReturned
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import string_concat
from django.utils.encoding import force_unicode 
from django.utils.functional import lazy

#~ import lino
#~ logger.debug(__file__+' : started')
#~ from django.utils import translation

#~ from django_sites.dbutils import range_filter

#~ from lino import reports
from lino import dd
#~ from lino import layouts
#~ from lino.core import perms
#~ from lino.utils import printable
from lino import mixins
#~ from lino import fields
#~ from lino.modlib.users.models import UserLevels
#~ from lino.modlib.uploads.models import UploadsByPerson
#~ from lino.models import get_site_config
from lino.core import dbutils
from lino.core.actors import Actor
from lino.core.dbutils import get_field
from lino.core.dbutils import resolve_field
#~ from north import babel
from lino.utils import join_words
from lino.utils.choosers import chooser
from lino.utils import mti
from lino.utils.ranges import isrange
from lino.utils.xmlgen import html as xghtml
from lino.utils.xmlgen.html import E
from lino.utils import IncompleteDate

from lino.mixins.printable import DirectPrintAction, Printable
#~ from lino.mixins.reminder import ReminderEntry
from lino.core import actions
#~ from lino.core import changes

from lino.modlib.contacts.utils import street2kw
from lino.modlib.contacts import models as contacts

#~ from lino.modlib.notes import models as notes
#~ from lino.modlib.links import models as links
#~ from lino.modlib.uploads import models as uploads
#~ from lino.modlib.cal import models as cal
#~ from lino.modlib.users import models as users
#~ from lino.modlib.countries.models import CountryCity
#~ from lino.modlib.cal.models import DurationUnits, update_reminder
#~ from lino.modlib.properties import models as properties
#~ from lino_welfare.modlib.cv import models as cv
#~ from lino.modlib.contacts.models import Contact
from lino.core.dbutils import resolve_model, UnresolvedModel

households = dd.resolve_app('households')
cal = dd.resolve_app('cal')
properties = dd.resolve_app('properties')
countries = dd.resolve_app('countries')
cv = dd.resolve_app('cv')
uploads = dd.resolve_app('uploads')
users = dd.resolve_app('users')
isip = dd.resolve_app('isip')
jobs = dd.resolve_app('jobs')
pcsw = dd.resolve_app('pcsw')
courses = dd.resolve_app('courses')
#~ from lino_welfare.modlib.isip import models as isip
#~ newcomers = dd.resolve_app('newcomers')


ui = dd.resolve_app('ui')

class SiteConfig(ui.SiteConfig,isip.Signers):
    """
    This adds the :class:`lino_welfare.modlib.isip.models.Signers` 
    mixin to Lino's standard SiteConfig.
    
    This trick having ``"ui.SiteConfig"`` in :attr:`lino.Lino.override_modlib_models`.
    
    """
    class Meta:
        app_label = 'ui'

dd.update_field(SiteConfig,'signer1', blank=True,null=True)
dd.update_field(SiteConfig,'signer2', blank=True,null=True)


def customize_users():
  
    dd.inject_field(settings.SITE.user_model,
        'coaching_type',
        dd.ForeignKey('pcsw.CoachingType',
            blank=True,null=True,
            help_text="""The default CoachingType used when creating Coachings."""))
    dd.inject_field(settings.SITE.user_model,
        'coaching_supervisor',
        models.BooleanField(_("Notify me when a coach has been assigned"),
            help_text=u"""\
Wenn ein Neuantrag einem Begleiter zugewiesen wurde, wird außer dem Begleiter auch dieser Benutzer benachrichtigt."""))
        
  
def customize_siteconfig():
    """
    Injects application-specific fields to :class:`SiteConfig <lino.models.SiteConfig>`.
    """
    
    dd.inject_field('ui.SiteConfig',
        'job_office',
        models.ForeignKey('contacts.Company',
            blank=True,null=True,
            verbose_name=_("Local job office"),
            related_name='job_office_sites',
            help_text="""The Company whose contact persons 
            will be choices for `Person.job_office_contact`."""))
        
    dd.inject_field('ui.SiteConfig',
        'residence_permit_upload_type',
        models.ForeignKey("uploads.UploadType",
            blank=True,null=True,
            verbose_name=_("Upload Type for residence permit"),
            related_name='residence_permit_sites'))
        
    dd.inject_field('ui.SiteConfig',
        'work_permit_upload_type',
        #~ UploadType.objects.get(pk=2)
        models.ForeignKey("uploads.UploadType",
            blank=True,null=True,
            verbose_name=_("Upload Type for work permit"),
            related_name='work_permit_sites'))

    dd.inject_field('ui.SiteConfig',
        'driving_licence_upload_type',
        models.ForeignKey("uploads.UploadType",
            blank=True,null=True,
            verbose_name=_("Upload Type for driving licence"),
            related_name='driving_licence_sites'))
    


def customize_contacts():
    """
    Injects application-specific fields to :mod:`contacts <lino.modlib.contacts>`.
    """
    dd.inject_field(contacts.RoleType,
        'use_in_contracts',
        models.BooleanField(
            verbose_name=_("usable in contracts"),
            default=True,
            help_text=_("Whether Links of this type can be used as contact person of a job contract.")))
        
        
if False:
  
    def customize_countries():
        """
        Injects application-specific fields to :mod:`countries <lino.modlib.countries>`.
        """
        dd.inject_field(countries.Country,
            'nationalities',
            models.CharField(
                verbose_name=_("Nationality texts (NL, FR, DE, EN)"),
                max_length=200,
                blank=True,
                help_text=_("Space separated list of case insensitive nationality designations in 4 languages.")))
            
            

        

def customize_notes():
    """
    Application-specific changes to :mod:`lino.modlib.notes`.
    """
    #~ from lino.modlib.notes.models import Note, Notes
    notes = dd.resolve_app('notes')

    dd.inject_field(notes.Note,'company',
        models.ForeignKey('contacts.Company',
            blank=True,null=True,
            help_text="""\
    An optional third-party Organization that is related to this Note.
    The note will then be visible in that company's history panel.
    """
        ))
        
    def get_person(self):
        return self.project
    notes.Note.person = property(get_person)
        
      


@dd.receiver(dd.auto_create)
def on_auto_create(sender,**kw):
    #~ raise Warning("auto_create is not permitted here")
    logger.info("auto_create %s %s",dd.obj2str(sender),kw)
    from django.core.mail import mail_admins
    body = 'Record %s has been automatically created using %s' % (dd.obj2str(sender),kw)
    mail_admins('auto_create', body, fail_silently=True)

#~ dd.auto_create.connect(on_auto_create)


def customize_sqlite():
    """
    Here is how we install case-insensitive sorting in sqlite3.
    Note that this caused noticeable performance degradation...

    Thanks to 
    - http://efreedom.com/Question/1-3763838/Sort-Order-SQLite3-Umlauts
    - http://docs.python.org/library/sqlite3.html#sqlite3.Connection.create_collation
    - http://www.sqlite.org/lang_createindex.html
    """
    from django.db.backends.signals import connection_created

    def belgian(s):
      
        s = s.decode('utf-8').lower()
        
        s = s.replace(u'ä',u'a')
        s = s.replace(u'à',u'a')
        s = s.replace(u'â',u'a')
        
        s = s.replace(u'ç',u'c')
        
        s = s.replace(u'é',u'e')
        s = s.replace(u'è',u'e')
        s = s.replace(u'ê',u'e')
        s = s.replace(u'ë',u'e')
        
        s = s.replace(u'ö',u'o')
        s = s.replace(u'õ',u'o')
        s = s.replace(u'ô',u'o')
        
        s = s.replace(u'ß',u'ss')
        
        s = s.replace(u'ù',u'u')
        s = s.replace(u'ü',u'u')
        s = s.replace(u'û',u'u')
        
        return s
        
    def stricmp(str1, str2):
        return cmp(belgian(str1),belgian(str2))
        
    def my_callback(sender,**kw):
        from django.db.backends.sqlite3.base import DatabaseWrapper
        if sender is DatabaseWrapper:
            db = kw['connection']
            db.connection.create_collation('BINARY', stricmp)

    connection_created.connect(my_callback)



#~ class Home(cal.Home):
    #~ label = cal.Home.label
    #~ app_label = 'lino'
    #~ detail_layout = """
    #~ quick_links:80x1
    #~ welcome
    #~ pcsw.UsersWithClients:80x8
    #~ coming_reminders:40x16 missed_reminders:40x16
    #~ """
    


#~ def setup_main_menu(site,ui,profile,m): 
def setup_reports_menu(site,ui,profile,m):
    m.add_action(site.modules.jobs.JobsOverview)
    m.add_action(site.modules.pcsw.UsersWithClients)
    m.add_action(site.modules.pcsw.ClientsTest)
    #~ m  = m.add_menu("pcsw",pcsw.MODULE_LABEL)
    m.add_action(ActivityReport)
    #~ m.add_action(ActivityReport1) # old version
        


@dd.receiver(dd.post_startup)
def register_change_watchers(sender,**kw):
    """
    A Lino/Welfare site by default watches the changes to certain Client fields
    and to all Contract fields.
    """
    
    self = sender
    
    #~ super(Site,self).on_site_startup()
    
    from lino.modlib.changes.models import watch_changes as wc
    
    #~ self.modules.pcsw.Client.watch_changes('first_name last_name national_id client_state')
    wc(self.modules.contacts.Partner)
    wc(self.modules.contacts.Person,master_key='partner_ptr')
    wc(self.modules.contacts.Company,master_key='partner_ptr')
    wc(self.modules.pcsw.Client,master_key='partner_ptr')
    wc(self.modules.pcsw.Coaching,master_key='client__partner_ptr')
    wc(self.modules.pcsw.ClientContact,master_key='client__partner_ptr')
    wc(self.modules.jobs.Candidature,master_key='person__partner_ptr')
    
    #~ self.modules.notes.Note.watch_changes(master_key='project')
    #~ self.modules.outbox.Mail.watch_changes(master_key='project')
    #~ self.modules.cal.Event.watch_changes(master_key='project')
    #~ self.modules.debts.Budget.watch_changes(master_key='partner')
    
    # ContractBase is abstract, so it's not under self.modules
    from lino_welfare.modlib.isip.models import ContractBase
    #~ ContractBase.watch_changes(master_key='client__partner_ptr')
    wc(ContractBase, master_key='client__partner_ptr')
    
    from lino_welfare.modlib.cbss.models import CBSSRequest
    wc(CBSSRequest,master_key='person__partner_ptr')
                
            
  

def site_setup(site):
    """
    This is the place where we can override or 
    define application-specific things.
    This includes especially those detail layouts 
    which depend on the *combination* of installed modules.
    """
   
    #~ class HouseholdDetail(households.HouseholdDetail):
        #~ box3 = """
        #~ country region
        #~ city zip_code:10
        #~ street_prefix street:25 street_no street_box
        #~ addr2:40
        #~ activity bank_account1:12 bank_account2:12
        #~ """

    #~ class Households(households.Households):
        #~ model = 'households.Household'
        #~ detail_layout = HouseholdDetail()
        

    site.modules.lino.Home.set_detail_layout("""
    quick_links:80x1
    welcome
    pcsw.UsersWithClients:80x8
    coming_reminders:40x16 missed_reminders:40x16
    """)
    
    site.modules.households.Households.set_detail_layout(box3="""
    country region
    city zip_code:10
    street_prefix street:25 street_no street_box
    addr2:40
    activity bank_account1:12 bank_account2:12
    """)
    
    
    site.modules.ui.SiteConfigs.set_detail_layout("""
    site_company system_note_type default_build_method 
    next_partner_id:20 job_office debts_bailiff_type master_budget
    signer1 signer2
    signer1_function signer2_function 
    constants
    # lino.ModelsBySite
    """,constants="""
    propgroup_skills propgroup_softskills propgroup_obstacles
    residence_permit_upload_type work_permit_upload_type driving_licence_upload_type
    """)
    
    site.modules.properties.Properties.set_detail_layout("""
    id group type 
    name
    cv.PersonPropsByProp
    """)
    
    site.modules.countries.Cities.set_detail_layout("""
    name country inscode 
    parent type id
    CitiesByCity
    contacts.PartnersByCity jobs.StudiesByCity
    """)
    
    #~ site.modules.countries.Cities.detail_layout.update(main="""
    #~ name country 
    #~ contacts.PartnersByCity jobs.StudiesByCity
    #~ """)
    
    site.modules.countries.Countries.set_detail_layout("""
    isocode name short_code inscode
    # nationalities
    countries.CitiesByCountry jobs.StudiesByCountry
    """)
    
    site.modules.uploads.Uploads.set_detail_layout("""
    file user
    type description valid_until
    # person company
    # reminder_date reminder_text delay_value delay_type reminder_done
    modified created owner
    cal.TasksByController
    # show_date show_time 
    # show_date time timestamp
    """)

    site.modules.uploads.Uploads.set_insert_layout("""
    file user
    type valid_until
    description 
    # owner
    """,window_size=(60,'auto'))


    site.modules.contacts.Partners.set_detail_layout(pcsw.PartnerDetail())
    site.modules.contacts.Companies.set_detail_layout(pcsw.CompanyDetail())
    #~ site.modules.contacts.Persons.set_detail_layout(PersonDetail())
    #~ for T in (site.modules.contacts.Partners,
            #~ site.modules.contacts.Persons,
            #~ site.modules.contacts.Companies,
            #~ site.modules.pcsw.Clients):
        #~ T.add_detail_tab('changes','lino.ChangesByMaster')
    site.modules.contacts.Partners.add_detail_tab('changes','changes.ChangesByMaster')

    
    site.modules.cal.Events.set_detail_layout("general more")
    site.modules.cal.Events.add_detail_panel("general","""
    calendar summary project 
    start end user assigned_to
    place priority access_class transparent #rset 
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
    
    #~ site.modules.users.Users.set_detail_layout(box2 = """
    #~ level
    #~ integ_level
    #~ cbss_level
    #~ newcomers_level newcomer_quota
    #~ debts_level
    #~ """)
    
    
    #~ site.modules.users.Users.set_detail_layout("""
    #~ box1:50 MembershipsByUser:25
    #~ remarks AuthoritiesGiven 
    #~ """,
    site.modules.users.Users.set_detail_layout(
    coaching_a="""
    newcomer_quota 
    coaching_type 
    coaching_supervisor
    newcomers.CompetencesByUser
    """)
    #~ box2="""
    #~ newcomer_quota 
    #~ """)
    
    site.modules.users.Users.add_detail_tab('coaching',"""
    coaching_a:20 pcsw.CoachingsByUser:40
    """,_("Coaching"),)
    
        
    site.modules.notes.Notes.set_detail_layout(
        left = """
        date:10 event_type:25 type:25
        subject 
        project company
        id user:10 language:8 build_time
        body
        """,
        
        right = """
        uploads.UploadsByController
        outbox.MailsByController
        postings.PostingsByController
        cal.TasksByController
        """,
        
        main = """
        left:60 right:30
        """
    )
    
    
    site.modules.notes.Notes.set_insert_layout("""
    event_type:25 type:25
    subject 
    project company
    """,window_size=(50,'auto'))
    
    #~ site.modules.outbox.Mails.set_detail_layout("""
    #~ subject project date 
    #~ user sent #build_time id owner
    #~ RecipientsByMail:50x5 AttachmentsByMail:20x5 uploads.UploadsByOwner:20x5
    #~ body:90x10
    #~ """)
        
    #~ site.modules.courses.CourseProviders.set_detail_layout(CourseProviderDetail())

#~ logger.info("20130409 %s declare set_merge_actions()",__name__)
#~ raise Exception("20130409 %s declare set_merge_actions()" % __name__)
    
@dd.receiver(dd.pre_analyze)
def set_merge_actions(sender,**kw):
    #~ logger.info("20130409 %s.set_merge_actions()",__name__)
    modules = sender.modules
    for m in (modules.pcsw.Client,modules.contacts.Company):
        #~ print repr(m)
        m.define_action(merge_row=dd.MergeAction(m))
        #~ m.merge_row = dd.MergeAction(m)
    
#~ dd.signals.pre_startup.connect()


customize_siteconfig()
#~ customize_countries()
customize_contacts()        
customize_notes()
customize_sqlite()
customize_users()

#~ customize_user_groups()
#~ customize_user_profiles()
#~ setup_user_profiles()
  



def setup_workflows(site):

    #~ ClientStates.newcomer.add_transition(states='refused coached invalid former',user_groups='newcomers')
    
    def allow_state_newcomer(action,user,obj,state):
        """
        A Client with at least one Coaching cannot become newcomer.
        """
        #~ if obj.client_state == ClientStates.coached:
        if obj.coachings_by_client.count() > 0:
            return False
        return True
    
    
    pcsw.ClientStates.newcomer.add_transition(states='refused coached former',
        user_groups='newcomers',allow=allow_state_newcomer)
    pcsw.ClientStates.refused.add_transition(pcsw.RefuseClient)
    #~ ClientStates.refused.add_transition(_("Refuse"),states='newcomer invalid',user_groups='newcomers',notify=True)
    #~ ClientStates.coached.add_transition(_("Coached"),states='new',user_groups='newcomers')
    pcsw.ClientStates.former.add_transition(_("Former"),
        #~ states='coached invalid',
        states='coached',
        user_groups='newcomers')
    #~ ClientStates.add_transition('new','refused',user_groups='newcomers')

#~ dd.register_screenshot('index','');
#~ dd.register_screenshot('cal.CalendarPanel','/api/cal/CalendarPanel',username='alicia');
#~ register_screenshot('/api/cal/CalendarPanel?su=8&ul='+LANGUAGE,'cal.CalendarPanel-su.png');
#~ //~ register_screenshot('/api/cal/PanelEvents/266?an=detail&ul='+LANGUAGE,'cal.Event.detail.png');
#~ register_screenshot('/api/cal/PanelEvents/105?an=detail&ul='+LANGUAGE,'cal.Event.detail.png');
#~ 
#~ register_screenshot('/api/pcsw/Clients?ul='+LANGUAGE,'pcsw.Clients.grid.png');
#~ register_screenshot('/api/pcsw/Clients/122?ul='+LANGUAGE,'pcsw.Client.detail.png');
#~ register_screenshot('/api/pcsw/Clients/122?tab=1&ul='+LANGUAGE,'pcsw.Client.detail.1.png');
#~ register_screenshot('/api/pcsw/Clients/122?tab=2&ul='+LANGUAGE,'pcsw.Client.detail.2.png');
#~ 
#~ register_screenshot('/api/debts/Budgets/2?ul='+LANGUAGE,'debts.Budget.detail.png');
#~ register_screenshot('/api/debts/Budgets/2?tab=1&ul='+LANGUAGE,'debts.Budget.detail.1.png');
#~ register_screenshot('/api/debts/Budgets/2?tab=2&ul='+LANGUAGE,'debts.Budget.detail.2.png');
#~ register_screenshot('/api/debts/Budgets/2?tab=3&ul='+LANGUAGE,'debts.Budget.detail.3.png');
#~ register_screenshot('/api/debts/Budgets/2?tab=4&ul='+LANGUAGE,'debts.Budget.detail.4.png');
#~ register_screenshot('/api/jobs/JobsOverview?ul='+LANGUAGE,'jobs.JobsOverview.png');
#~ 
#~ 

#~ """
    #~ quick_links:80x1
    #~ welcome
    #~ pcsw.UsersWithClients:80x8
    #~ coming_reminders:40x16 missed_reminders:40x16
#~ """

#~ from lino.ui.models import get_installed_todo_tables
            

def unused_dashboard(ar):
    #~ raise Exception("20130522 dashboard()")
    html = []
    #~ from lino.core import requests
    #~ ar = requests.BaseRequest(
        #~ renderer=settings.SITE.ui.ext_renderer,
        #~ request=request)
        #~ user=request.subst_user or request.user
    #~ quicklinks = settings.SITE.get_quicklinks(ar)
    #~ if quicklinks.items:
        #~ chunks = []
        #~ for mi in quicklinks.items:
            #~ chunks.append(' ')
            #~ chunks.append(settings.SITE.ui.ext_renderer.window_action_button(
              #~ ar,mi.bound_action))
        #~ html.append(E.p('Quick Links:',*chunks))
        
    #~ MAXITEMS = 2
    u = ar.get_user()
    
    if u.profile.authenticated:
      
        #~ intro = [_("Hi, "),u.first_name,'! ']
        #~ html.append(E.p(*intro))
        warnings = []
        for table,text in settings.SITE.get_todo_tables(ar):
            r = table.request(user=u)
            if r.get_total_count() != 0:
                
                warnings.append(E.li(
                    ar.href_to_request(r,text % r.get_total_count())))
        
        if len(warnings):
            html.append(E.h3(_("You have")))
            html.append(E.ul(*warnings))
        #~ else:
            #~ html.append(E.p(_("Congratulatons: you have no warnings.")))
    #~ html.append(E.div(*story,class_="htmlText",style="margin:5px"))
   
    sar = ar.spawn(pcsw.UsersWithClients)
    html.append(sar.table2xhtml())
   
        #~ return reminders_as_html(ar,days_forward=30,
            #~ max_items=10,before='<ul><li>',separator='</li><li>',after="</li></ul>")
    
    
    #~ for jobtype in self.jobtypes:
        #~ html.append(E.h2(unicode(jobtype)))
        #~ sar = ar.spawn(JobsOverviewByType,
            #~ master_instance=jobtype,
            #~ param_values=dict(date=self.today))
        #~ html.append(sar.table2xhtml())
        
    return E.tostring(E.div(*html,class_="htmlText",style="margin:5px"))


#~ settings.SITE.dashboard = dashboard


class CompareRequestsTable(dd.VirtualTable):
    label = _("Evolution générale")
    auto_fit_column_widths = True
    column_names = "description old_value new_value"
    slave_grid_format = 'html'
    hide_sums = True
    
    @dd.displayfield(_("Description"))
    def description(self,row,ar): return row[0]
        
    @dd.requestfield(_("Initial value"))
    def old_value(self,row,ar): return row[1]

    @dd.requestfield(_("Final value"))
    def new_value(self,row,ar): return row[2]

    @classmethod
    def get_data_rows(self,ar):
        #~ rows = []
        pv = ar.master_instance
        if pv is None: return
        #~ def add(A,oe=None,**kw):
        def add(A,**kw):
            pva = dict(**kw)
            ar = A.request(param_values=pva)
            cells = [ar.get_title()]
            for d in (pv.start_date,pv.end_date):
                ar = A.request(param_values=dict(pva,start_date=d,end_date=d))
                #~ print 20130527, ar
                cells.append(ar)
            return cells
            
        yield add(pcsw.Clients,observed_event=pcsw.ClientEvents.coached)
        
        yield add(isip.Contracts,observed_event=isip.ContractEvents.active)
        #~ yield add(isip.Contracts,isip.ContractEvents.ended)
        yield add(jobs.Contracts,observed_event=isip.ContractEvents.active)
        #~ yield add(jobs.Contracts,isip.ContractEvents.ended)
        yield add(courses.PendingCourseRequests)
        
        all_contracts = isip.Contracts.request(
            param_values=dict(
                start_date=pv.start_date,
                end_date=pv.end_date)).get_data_iterator()
        # DISTINCT on fields doesn't work in sqlite
        study_types = set(all_contracts.values_list('study_type',flat=True))
        #~ print 20130527, study_types
        for st in study_types:
            if st is not None:
                yield add(isip.Contracts,
                    observed_event=isip.ContractEvents.active,
                    study_type=isip.StudyType.objects.get(pk=st))


class PeriodicNumbers(dd.VirtualTable):
    label = _("Indicateurs d'activité")
    auto_fit_column_widths = True
    column_names = "description number"
    slave_grid_format = 'html'
    hide_sums = True
    
    @dd.displayfield(_("Description"))
    def description(self,row,ar): return row[0]
        
    @dd.requestfield(_("Number"))
    def number(self,row,ar): return row[1]

    @classmethod
    def get_data_rows(self,ar):
        mi = ar.master_instance
        if mi is None: return
        
        def add(A,**pva):
            #~ pva = dict(**kw)
            ar = A.request(param_values=pva)
            cells = [ar.get_title()]
            ar = A.request(param_values=dict(pva,start_date=mi.start_date,end_date=mi.end_date))
            cells.append(ar)
            return cells
            
        
        #~ def add(A,oe):
            #~ cells = ["%s %s" % (A.model._meta.verbose_name_plural,oe.text)]
            #~ pv = dict(start_date=mi.start_date,end_date=mi.end_date)
            #~ pv.update(observed_event=oe)
            #~ ar = A.request(param_values=pv)
            #~ cells.append(ar)
            #~ return cells

        yield add(pcsw.Coachings,observed_event=pcsw.CoachingEvents.started)
        yield add(pcsw.Coachings,observed_event=pcsw.CoachingEvents.active)
        yield add(pcsw.Coachings,observed_event=pcsw.CoachingEvents.ended)
        
        yield add(pcsw.Clients,observed_event=pcsw.ClientEvents.coached)
        yield add(pcsw.Clients,observed_event=pcsw.ClientEvents.created)
        yield add(pcsw.Clients,observed_event=pcsw.ClientEvents.modified)
        
        for A in (isip.Contracts,jobs.Contracts):
            yield add(A,observed_event=isip.ContractEvents.started)
            yield add(A,observed_event=isip.ContractEvents.active)
            yield add(A,observed_event=isip.ContractEvents.ended)
            yield add(A,observed_event=isip.ContractEvents.signed)
        

class VentilatingTable(dd.Table):
    
    ventilated_column_suffix = ':5'
    
    @dd.virtualfield(models.CharField(_("Description"),max_length=30))
    def description(self,obj,ar):
        return unicode(obj)
                
    @classmethod
    def setup_columns(self):
        self.column_names = 'description '
        for i,vf in enumerate(self.get_ventilated_columns()):
            self.add_virtual_field('vc'+str(i),vf)
            self.column_names += ' ' + vf.name+self.ventilated_column_suffix
            
    
    @classmethod
    def get_ventilated_columns(self):
        return []
        
        
    
class CoachingEndingsByUser(VentilatingTable,pcsw.CoachingEndings):
    
    label = _("Coaching endings by user")
    
    @classmethod
    def get_ventilated_columns(self):
        for u in settings.SITE.user_model.objects.exclude(profile=''):
            label = unicode(u.username)
            def w(user):
                def func(fld,obj,ar):
                    mi = ar.master_instance
                    if mi is None: return None
                    pv = dict(start_date=mi.start_date,end_date=mi.end_date)
                    pv.update(observed_event=pcsw.CoachingEvents.ended)
                    pv.update(coached_by=user)
                    pv.update(ending=obj)
                    return pcsw.Coachings.request(param_values=pv)
                return func
            yield dd.RequestField(w(u),verbose_name=label)
    
   
class CoachingEndingsByType(VentilatingTable,pcsw.CoachingEndings):
    
    label = _("Coaching endings by type")
    
    @classmethod
    def get_ventilated_columns(self):
        for ct in pcsw.CoachingType.objects.all():
            label = unicode(ct)
            def w(ct):
                def func(fld,obj,ar):
                    mi = ar.master_instance
                    if mi is None: return None
                    pv = dict(start_date=mi.start_date,end_date=mi.end_date)
                    pv.update(observed_event=pcsw.CoachingEvents.ended)
                    pv.update(coaching_type=ct)
                    pv.update(ending=obj)
                    return pcsw.Coachings.request(param_values=pv)
                return func
            yield dd.RequestField(w(ct),verbose_name=label)
    

class ContractEndingsByType(VentilatingTable,isip.ContractEndings):
    
    label = _("Contract endings by type")
    contracts_table = isip.Contracts
    
    @classmethod
    def get_ventilated_columns(self):
        for ct in jobs.ContractType.objects.all():
            label = unicode(ct)
            def w(ct):
                def func(fld,obj,ar):
                    mi = ar.master_instance
                    if mi is None: return None
                    pv = dict(start_date=mi.start_date,end_date=mi.end_date)
                    pv.update(observed_event=isip.ContractEvents.ended)
                    pv.update(type=ct)
                    pv.update(ending=obj)
                    return self.contracts_table.request(param_values=pv)
                return func
            yield dd.RequestField(w(ct),verbose_name=label)
    
class JobsContractEndingsByType(ContractEndingsByType):
    contracts_table = jobs.Contracts
    
class StudyTypesAndContracts(isip.StudyTypes,VentilatingTable):
    label = _("Types de formation et contrats")
    help_text = _("""Nombre de PIIS actifs par 
    type de formation et type de contrat.""")
    contracts_table = isip.Contracts
    
    @classmethod
    def get_request_queryset(cls,ar):
        #~ logger.info("20120608.get_request_queryset param_values = %r",ar.param_values)
        qs = super(StudyTypesAndContracts,cls).get_request_queryset(ar)
        qs = qs.annotate(count=models.Count('contract'))
        return qs.filter(count__gte=1)
        #~ return qs
        
    @dd.virtualfield(dd.ForeignKey(isip.StudyType,_("Description")))
    def description(self,obj,ar):
        return obj
        
    @classmethod
    def get_ventilated_columns(self):
        for ct in isip.ContractType.objects.filter(needs_study_type=True):
            label = unicode(ct)
            def w(ct):
                def func(fld,obj,ar):
                    mi = ar.master_instance
                    if mi is None: return None
                    pv = dict(start_date=mi.start_date,end_date=mi.end_date)
                    pv.update(observed_event=isip.ContractEvents.active)
                    pv.update(type=ct)
                    pv.update(study_type=obj)
                    return self.contracts_table.request(param_values=pv)
                return func
            yield dd.RequestField(w(ct),verbose_name=label)
    

class CompaniesAndContracts(contacts.Companies,VentilatingTable):
    label = _("Organisations externes et contrats")
    help_text = _("""Nombre de PIIS actifs par 
    organisation externe et type de contrat.""")
    contracts_table = isip.Contracts
    contract_types = isip.ContractType
    hide_zero_rows = True
    
    @classmethod
    def get_request_queryset(cls,ar):
        qs = super(CompaniesAndContracts,cls).get_request_queryset(ar)
        qs = qs.annotate(count=models.Count('isip_contract_set_by_company'))
        return qs.filter(count__gte=1)
        
    @dd.virtualfield(dd.ForeignKey(isip.StudyType,_("Description")))
    def description(self,obj,ar):
        return obj
        
    @classmethod
    def get_ventilated_columns(self):
        for ct in self.contract_types.objects.all():
            label = unicode(ct)
            def w(ct):
                def func(fld,obj,ar):
                    mi = ar.master_instance
                    if mi is None: return None
                    pv = dict(start_date=mi.start_date,end_date=mi.end_date)
                    pv.update(observed_event=isip.ContractEvents.active)
                    pv.update(type=ct)
                    pv.update(company=obj)
                    return self.contracts_table.request(param_values=pv)
                return func
            yield dd.RequestField(w(ct),verbose_name=label)
    
#~ class JobsCompaniesAndContracts(CompaniesAndContracts):
class JobProvidersAndContracts(CompaniesAndContracts):
    label = _("Employants et contrats Art 60§7")
    help_text = _("""Nombre de projets Art 60§7 actifs par 
    employants et type de contrat.""")
    contracts_table = jobs.Contracts
    contract_types = jobs.ContractType
    
    @classmethod
    def get_request_queryset(cls,ar):
        #~ qs = super(CompaniesAndContracts,cls).get_request_queryset(ar)
        qs = jobs.JobProvider.objects.all()
        qs = qs.annotate(count=models.Count('jobs_contract_set_by_company'))
        return qs.filter(count__gte=1)
    

class ActivityReport1(dd.EmptyTable):
    """
    Welche (Wieviele) Verträge
    
    - waren aktiv am X
    - wurden unterzeichnet / abgeschlossen / beendet
      in der Periode vom X bis Y
    - pro Kategorie (Sozialwirtschaft, Interne, Externe Öffentlich, Externe Privat,...)
    - pro Beendigungsgrund
    - pro Partnerorganisation
    - pro Ausbildungsart
    
    """
    required = dd.required(user_level='manager')
    label = _("Activity Report") 
    
    parameters = dict(
      start_date = models.DateField(verbose_name=_("Period from")),
      end_date = models.DateField(verbose_name=_("until")),
      include_jobs = models.BooleanField(verbose_name=pcsw.JOBS_MODULE_LABEL),
      include_isip = models.BooleanField(verbose_name=_("ISIP")),
      )
      
    params_layout = "start_date end_date include_jobs include_isip"
    #~ params_panel_hidden = True

    @classmethod
    def param_defaults(self,ar,**kw):
        D = datetime.date
        kw.update(start_date = D(D.today().year,1,1))
        kw.update(end_date = D(D.today().year,12,31))
        return kw

    detail_layout = "CompareRequestsTable PeriodicNumbers t2"
    
    @dd.virtualfield(dd.HtmlBox(_("Second tab")))
    def t2(cls,self,ar):
        html = []
        for A in (CoachingEndingsByUser,CoachingEndingsByType,ContractEndingsByType):
            html.append(E.h3(A.label))
            html.append(ar.show(A,master_instance=self))
        #~ html.append(E.p("Foo"))
        #~ html.append(E.p("Bar"))
        return E.div(*html)


class ActivityReport(dd.Report):
    
    required = dd.required(user_level='manager')
    label = _("Activity Report") 
    
    parameters = dict(
      start_date = models.DateField(verbose_name=_("Period from")),
      end_date = models.DateField(verbose_name=_("until")),
      include_jobs = models.BooleanField(verbose_name=pcsw.JOBS_MODULE_LABEL),
      include_isip = models.BooleanField(verbose_name=_("ISIP")),
      )
      
    params_layout = "start_date end_date include_jobs include_isip"
    #~ params_panel_hidden = True
    
    @classmethod
    def param_defaults(self,ar,**kw):
        D = datetime.date
        kw.update(start_date = D(D.today().year,1,1))
        kw.update(end_date = D(D.today().year,12,31))
        return kw
    
    @classmethod
    def get_story(cls,self,ar):
        yield E.h2(_("Introduction"))
        yield E.p("Ceci est un ",E.b("rapport"),""", 
            càd un document complet généré par Lino, contenant des 
            sections, des tables et du texte libre.
            Dans la version écran cliquer sur un chiffre pour voir d'où 
            il vient.
            """)
        yield E.h2(_("Indicateurs généraux"))
        yield CompareRequestsTable
        yield E.p('.')
        yield PeriodicNumbers
        yield E.h2(_("Causes d'arrêt des accompagnements"))
        yield CoachingEndingsByUser
        yield E.p('.')
        yield CoachingEndingsByType
        for A in (ContractEndingsByType,JobsContractEndingsByType):
            yield E.h2(_("Causes d'arrêt des %s") % A.contracts_table.label)
            yield A
        #~ yield E.p(pcsw.JOBS_MODULE_LABEL)
        #~ yield JobsContractEndingsByType
        
        #~ yield E.h2(_("Snapshot"))
        #~ yield E.p("Voici quelques tables complètes:")
        #~ for A in (pcsw.UsersWithClients,StudyTypesAndContracts,CompaniesAndContracts):
        for A in (StudyTypesAndContracts,CompaniesAndContracts,JobProvidersAndContracts):
            yield E.h2(A.label)
            if A.help_text:
                yield E.p(unicode(A.help_text))
            yield A
