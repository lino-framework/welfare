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
The :xfile:`models.py` module for the :mod:`lino_welfare` app.

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

from lino.core.dbutils import resolve_model, UnresolvedModel

households = dd.resolve_app('households')
#~ cal = dd.resolve_app('cal')
properties = dd.resolve_app('properties')
countries = dd.resolve_app('countries')
contacts = dd.resolve_app('contacts')
cv = dd.resolve_app('cv')
uploads = dd.resolve_app('uploads')
users = dd.resolve_app('users')
isip = dd.resolve_app('isip')
jobs = dd.resolve_app('jobs')
pcsw = dd.resolve_app('pcsw')
courses = dd.resolve_app('courses')
#~ from lino_welfare.modlib.isip import models as isip
#~ newcomers = dd.resolve_app('newcomers')



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
    
    dd.inject_field('system.SiteConfig',
        'job_office',
        models.ForeignKey('contacts.Company',
            blank=True,null=True,
            verbose_name=_("Local job office"),
            related_name='job_office_sites',
            help_text="""The Company whose contact persons 
            will be choices for `Person.job_office_contact`."""))
        
    dd.inject_field('system.SiteConfig',
        'residence_permit_upload_type',
        models.ForeignKey("uploads.UploadType",
            blank=True,null=True,
            verbose_name=_("Upload Type for residence permit"),
            related_name='residence_permit_sites'))
        
    dd.inject_field('system.SiteConfig',
        'work_permit_upload_type',
        #~ UploadType.objects.get(pk=2)
        models.ForeignKey("uploads.UploadType",
            blank=True,null=True,
            verbose_name=_("Upload Type for work permit"),
            related_name='work_permit_sites'))

    dd.inject_field('system.SiteConfig',
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
        

    #~ site.modules.lino.Home.set_detail_layout("""
    #~ quick_links:80x1
    #~ welcome
    #~ pcsw.UsersWithClients:80x8
    #~ coming_reminders:40x16 missed_reminders:40x16
    #~ """)
    
    site.modules.households.Households.set_detail_layout(box3="""
    country region
    city zip_code:10
    street_prefix street:25 street_no street_box
    addr2:40
    activity bank_account1:12 bank_account2:12
    """)
    
    site.modules.system.SiteConfigs.set_detail_layout(
        "general constants",
        general=dd.Panel("""
        site_company next_partner_id:10 
        job_office debts_bailiff_type master_budget
        signer1 signer2
        signer1_function signer2_function 
        """,label=_("General")),constants=dd.Panel("""
        system_note_type default_build_method 
        propgroup_skills propgroup_softskills propgroup_obstacles
        residence_permit_upload_type work_permit_upload_type driving_licence_upload_type
        client_calendar prompt_calendar 
        client_guestrole team_guestrole 
        attestation_note_nature
        """,label=_("Constants")))
    
    site.modules.properties.Properties.set_detail_layout("""
    id group type 
    name
    cv.PersonPropsByProp
    """)
    
    site.modules.countries.Cities.set_detail_layout("""
    name country inscode zip_code
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


    site.modules.contacts.Partners.set_detail_layout(contacts.PartnerDetail())
    site.modules.contacts.Companies.set_detail_layout(contacts.CompanyDetail())
    #~ site.modules.contacts.Persons.set_detail_layout(PersonDetail())
    #~ for T in (site.modules.contacts.Partners,
            #~ site.modules.contacts.Persons,
            #~ site.modules.contacts.Companies,
            #~ site.modules.pcsw.Clients):
        #~ T.add_detail_tab('changes','lino.ChangesByMaster')
    site.modules.contacts.Partners.add_detail_tab('changes','changes.ChangesByMaster')

    
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
#~ customize_notes()
customize_sqlite()
customize_users()

#~ customize_user_groups()
#~ customize_user_profiles()
#~ setup_user_profiles()
  


