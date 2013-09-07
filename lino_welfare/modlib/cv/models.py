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
The :xfile:`models.py` file for :mod:`lino_welfare.modlib.cv`.
"""

import logging
logger = logging.getLogger(__name__)

import os
import cgi
import datetime

from django.db import models
from django.db.models import Q
from django.db.utils import DatabaseError
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import string_concat
from django.utils.encoding import force_unicode 
from django.utils.functional import lazy
    

#~ import lino
#~ logger.debug(__file__+' : started')
#~ from django.utils import translation


#~ from lino import reports
from lino import dd
#~ from lino import layouts
#~ from lino.utils import printable
from lino import mixins
#~ from lino import actions
#~ from lino import fields
#~ from lino.modlib.contacts import models as contacts
#~ from lino.modlib.notes import models as notes
#~ from lino.modlib.links import models as links
#~ from lino.modlib.uploads import models as uploads
#~ from lino.modlib.cal import models as cal
cal = dd.resolve_app('cal')
uploads = dd.resolve_app('uploads')
notes = dd.resolve_app('notes')
contacts = dd.resolve_app('contacts')
#~ from lino.modlib.users import models as users
#~ from lino.modlib.properties.utils import KnowledgeField #, StrengthField
#~ from lino.modlib.uploads.models import UploadsByPerson
from lino.core.dbutils import get_field
from lino.core.dbutils import resolve_field
from north.dbutils import babelattr
from lino.utils.choosers import chooser
from lino.utils import mti
from lino.mixins.printable import DirectPrintAction, Printable
#~ from lino.mixins.reminder import ReminderEntry
#~ from lino.core.dbutils import obj2str

from lino.modlib.countries.models import CountryCity
from lino.modlib.properties import models as properties
from lino.modlib.cal.models import update_reminder
#~ from lino.modlib.contacts.models import Contact
from lino.core.dbutils import resolve_model, UnresolvedModel



class CefLevel(dd.ChoiceList):
    """
    Levels of the Common European Framework (CEF).
    
    | http://www.coe.int/t/dg4/linguistic/CADRE_EN.asp
    | http://www.coe.int/t/dg4/linguistic/Source/ManualRevision-proofread-FINAL_en.pdf
    | http://www.telc.net/en/what-telc-offers/cef-levels/a2/
    
    """
    verbose_name = _("CEF level")
    verbose_name_plural = _("CEF levels")
    show_values = True
    
    #~ @classmethod
    #~ def display_text(cls,bc):
        #~ def fn(bc):
            #~ return u"%s (%s)" % (bc.value,unicode(bc))
        #~ return lazy(fn,unicode)(bc)
    
add = CefLevel.add_item
add('A1', _("basic language skills"))
add('A2', _("basic language skills"))
add('A2+', _("basic language skills"))
add('B1', _("independent use of language"))
add('B2', _("independent use of language"))
add('B2+', _("independent use of language"))
add('C1', _("proficient use of language"))
add('C2', _("proficient use of language"))
add('C2+', _("proficient use of language"))





#
# LanguageKnowledge
#

class LanguageKnowledge(dd.Model):
    """Specifies how well a certain Person knows a certain Language.
    Deserves more documentation."""
    class Meta:
        verbose_name = _("language knowledge")
        verbose_name_plural = _("language knowledges")
        
    allow_cascaded_delete = ['person']
    
    #~ person = models.ForeignKey("contacts.Person")
    #~ person = models.ForeignKey(settings.SITE.person_model)
    person = models.ForeignKey('pcsw.Client')
    language = dd.ForeignKey("languages.Language")
    #~ language = models.ForeignKey("countries.Language")
    #~ language = fields.LanguageField()
    spoken = properties.HowWell.field(blank=True,verbose_name=_("spoken"))
    written = properties.HowWell.field(blank=True,verbose_name=_("written"))
    native = models.BooleanField(verbose_name=_("native language"))
    cef_level = CefLevel.field(blank=True) # ,null=True)
    
    def __unicode__(self):
        if self.language_id is None:
            return ''
        if self.cef_level:
            return u"%s (%s)" % (self.language,self.cef_level)
        if self.spoken > '1' and self.written > '1':
            return _(u"%s (s/w)") % self.language
        elif self.spoken > '1':
            return _(u"%s (s)") % self.language
        elif self.written > '1':
            return _(u"%s (w)") % self.language
        else:
            return unicode(self.language)
      
    
class LanguageKnowledges(dd.Table):
    model = LanguageKnowledge
    required = dd.required(user_groups='integ',user_level='manager')

class LanguageKnowledgesByPerson(LanguageKnowledges):
    master_key = 'person'
    #~ label = _("Language knowledge")
    #~ button_label = _("Languages")
    column_names = "language native spoken written cef_level"
    required = dd.required(user_groups='integ')
    
class KnowledgesByLanguage(LanguageKnowledges):
    master_key = 'language'
    column_names = "person native spoken written cef_level"
    required = dd.required(user_groups='integ')

# 
# PROPERTIES
# 


class PersonProperty(properties.PropertyOccurence):
    """
    The occurence of a given 
    :mod:`Property <lino.modlib.properties.models.Property>` 
    on a given 
    :class:`Client <lino_welfare.modlib.newcomers.models.Client>`.
    """
    
    allow_cascaded_delete = ['person']
    
    class Meta:
        app_label = 'properties'
        verbose_name = _("Property")
        verbose_name_plural = _("Properties")
        
    #~ person = models.ForeignKey("contacts.Person")
    #~ person = models.ForeignKey(settings.SITE.person_model)
    person = models.ForeignKey('pcsw.Client')
    remark = models.CharField(max_length=200,
        blank=True,# null=True,
        verbose_name=_("Remark"))


class PersonProperties(dd.Table):
    model = PersonProperty
    #~ hidden_columns = frozenset(['group'])
    hidden_columns = 'group id'
    required = dd.required(user_groups='integ',user_level='manager')
    
class PropsByPerson(PersonProperties):
    """
    Shows the :class:`PersonProperty` instances of a 
    :class:`Client <lino_welfare.modlib.newcomers.models.Client>`.
    """
    master_key = 'person'
    column_names = "property value remark *"
    required = dd.required(user_groups='integ')
    #~ hidden_columns = 'id'
    auto_fit_column_widths = True
    
    
class PersonPropsByProp(PersonProperties):
    model = PersonProperty
    #~ app_label = 'properties'
    master_key = 'property'
    column_names = "person value remark *"
    
#~ class PersonPropsByType(dd.Table):
    #~ model = PersonProperty
    #~ master_key = 'type'
    #~ column_names = "person property value remark *"
    #~ hidden_columns = frozenset(['group'])
    
class ConfiguredPropsByPerson(PropsByPerson):
    """
    Base class for 
    :class`SkillsByPerson`, 
    :class`SoftSkillsByPerson` and
    :class`ObstaclesByPerson`.
    """
    
    propgroup_config_name = None
    
    typo_check = False # to avoid warning "ConfiguredPropsByPerson 
                       # defines new attribute(s) propgroup_config_name"
                       
    @classmethod
    def get_known_values(self):
        pg = getattr(settings.SITE.site_config,self.propgroup_config_name)
        return dict(group=pg)
        
    @classmethod
    def get_actor_label(self):
        if self.propgroup_config_name is None:
            return self.__name__
        pg = getattr(settings.SITE.site_config,self.propgroup_config_name)
        if pg is None:
            return _("(SiteConfig %s is empty)" % self.propgroup_config_name)
        return babelattr(pg,'name')
        

    @classmethod
    def unused_on_analyze(self,site):
        """
        This is being called once for each subclass.
        """
        #~ print "20130220 after_site_setup %s" % self
        super(ConfiguredPropsByPerson,self).on_analyze(site)
        if self.propgroup_config_name:
            def adapt():
                try:
                    sc = site.site_config
                    pg = getattr(sc,self.propgroup_config_name)
                    self.known_values = dict(group=pg)
                    if pg is None:
                        self.label = _("(SiteConfig %s is empty)" % self.propgroup_config_name)
                    else:
                        self.label = lazy(babelattr,unicode)(pg,'name')
                    #~ print ("20130228 adapted %s to site config %r",self.propgroup_config_name,pg)
                except DatabaseError as e:
                    pass # database not initialized
            
            @dd.receiver(dd.connection_created,weak=False)
            def my_connection_created(sender,**kw):
                adapt()
            
            SiteConfig = site.modules.system.SiteConfig
            @dd.receiver(dd.post_save, sender=SiteConfig,weak=False)
            def my_post_save(sender, instance=None,**kwargs):
                adapt()
        
class SkillsByPerson(ConfiguredPropsByPerson):
    propgroup_config_name = 'propgroup_skills'
        
class SoftSkillsByPerson(ConfiguredPropsByPerson):
    propgroup_config_name = 'propgroup_softskills'
        
class ObstaclesByPerson(ConfiguredPropsByPerson):
    propgroup_config_name = 'propgroup_obstacles'
    
#~ @dd.receiver(dd.connection_created)
#~ def my_callback(sender,**kw):
    #~ raise Exception("20130302 connection_created")
    
    

def site_setup(site):
    site.modules.languages.Languages.set_detail_layout("""
    id iso2 name
    cv.KnowledgesByLanguage
    """)



def customize_siteconfig():

        
    dd.inject_field('system.SiteConfig',
        'propgroup_skills',
        models.ForeignKey('properties.PropGroup',
            blank=True,null=True,
            verbose_name=_("Skills Property Group"),
            related_name='skills_sites'),
        """The property group to be used as master 
        for the SkillsByPerson table.""")
    dd.inject_field('system.SiteConfig',
        'propgroup_softskills',
        models.ForeignKey('properties.PropGroup',
            blank=True,null=True,
            verbose_name=_("Soft Skills Property Group"),
            related_name='softskills_sites',
            ),
        """The property group to be used as master 
        for the SoftSkillsByPerson table."""
        )
    dd.inject_field('system.SiteConfig',
        'propgroup_obstacles',
        models.ForeignKey('properties.PropGroup',
            blank=True,null=True,
            verbose_name=_("Obstacles Property Group"),
            related_name='obstacles_sites',
            ),
        """The property group to be used as master 
        for the ObstaclesByPerson table."""
        )


customize_siteconfig()

def setup_explorer_menu(site,ui,profile,m):
    m = m.add_menu("cv",_("CV"))
    m.add_action(LanguageKnowledges)
