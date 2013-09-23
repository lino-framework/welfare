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
The :xfile:`models.py` module for the 
:mod:`lino_welfare.modlib.isip` app
(eee :ddref:`isip`)

"""

import os
import cgi
import datetime

from django.db import models
from django.db.models import Q
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from django.utils import translation
#~ from django.utils.encoding import force_unicode


from lino import dd
from lino.utils import dblogger as logger
#~ from lino.utils import printable
from lino import mixins
#~ from lino.modlib.contacts import models as contacts
#~ from lino.modlib.notes import models as notes
notes = dd.resolve_app('notes')
contacts = dd.resolve_app('contacts')
#~ pcsw = dd.resolve_app('pcsw')
#~ integ = dd.resolve_app('integ')

#~ from lino.modlib.links import models as links
from lino.modlib.uploads import models as uploads
#~ from lino.utils.choicelists import HowWell
#~ from lino.modlib.properties.utils import KnowledgeField #, StrengthField
#~ from lino.modlib.uploads.models import UploadsByPerson
from lino.core.dbutils import get_field
from lino.core.dbutils import resolve_field
from lino.utils.htmlgen import UL
from lino.utils.choosers import chooser
from lino.utils import mti
from lino.utils.ranges import isrange, overlap, overlap2, encompass
from lino.mixins.printable import DirectPrintAction
#~ from lino.mixins.reminder import ReminderEntry

from lino_welfare.modlib.system.models import Signers

from lino_welfare.modlib.isip import App

def rangefmt(r):
    return dd.dtos(r[0]) + '...' + dd.dtos(r[1])
    


#~ from lino.modlib.cal.models import update_auto_task

#~ from lino.modlib.cal import models as cal

cal = dd.resolve_app('cal')

COACHINGTYPE_ASD = 1
COACHINGTYPE_DSBE = 2


#~ class IntegTable(dd.Table):
  
    #~ @classmethod
    #~ def get_permission(self,action,user,obj):
        #~ if not user.integ_level:
            #~ return False
        #~ return super(IntegTable,self).get_permission(action,user,obj)
        

#
# CONTRACT TYPES 
#
class ContractType(mixins.PrintableType,dd.BabelNamed):
  
    """
    The contract type determines the print template to be used. 
    Print templates may use the `ref` field to conditionally 
    hide or show certain parts.
    `exam_policy` is the default ExamPolicy for new Contracts.
    """
    
    #~ _lino_preferred_width = 20 
    preferred_foreignkey_width = 20 
    
    templates_group = 'isip/Contract'
    
    class Meta:
        verbose_name = _("ISIP Type")
        verbose_name_plural = _('ISIP Types')
        
    ref = models.CharField(_("Reference"),max_length=20,blank=True)
    exam_policy = models.ForeignKey("isip.ExamPolicy",
        related_name="%(app_label)s_%(class)s_set",
        blank=True,null=True)
    needs_study_type = models.BooleanField(_("needs Study type"),default=False)
        

class ContractTypes(dd.Table):
    required=dict(user_groups = ['integ'],user_level='manager')
    model = ContractType
    column_names = 'name ref build_method template *'
    detail_layout = """
    id name 
    ref build_method template exam_policy needs_study_type
    ContractsByType
    """



#
# EXAMINATION POLICIES
#
class ExamPolicy(dd.BabelNamed,cal.RecurrenceSet):
#~ class ExamPolicy(dd.BabelNamed,mixins.ProjectRelated,cal.RecurrenceSet):
    """
    Examination policy. 
    This also decides about automatic tasks to be created.
    """
    class Meta:
        verbose_name = _("Examination Policy")
        verbose_name_plural = _('Examination Policies')
        
    #~ hidden_columns = 'summary description start_date start_time end_date end_time'
    hidden_columns = 'start_date start_time end_date end_time'
    
        

class ExamPolicies(dd.Table):
    required=dict(user_groups = ['integ'],user_level='manager')
    model = ExamPolicy
    column_names = 'name *'
    detail_layout = """
    id name
    # summary start_date end_date
    # description
    max_events every every_unit calendar
    isip.ContractsByPolicy    
    jobs.ContractsByPolicy    
    """


from lino_welfare.modlib.jobs import App as JobsApp
JOBS_MODULE_NAME = JobsApp.verbose_name
    
class ContractEnding(dd.Model):
    class Meta:
        verbose_name = _("Reason of termination")
        verbose_name_plural = _('Contract termination reasons')
        
    name = models.CharField(_("designation"),max_length=200)
    use_in_isip = models.BooleanField(App.verbose_name,default=True)
    use_in_jobs = models.BooleanField(JOBS_MODULE_NAME,default=True)
    is_success = models.BooleanField(_("Success"),default=False)
    needs_date_ended = models.BooleanField(_("Require date ended"),default=False)
    
    def __unicode__(self):
        return unicode(self.name)
        
class ContractEndings(dd.Table):
    required=dict(user_groups = ['integ'],user_level='manager')
    model = ContractEnding
    column_names = 'name *'
    order_by = ['name']
    detail_layout = """
    name
    use_in_isip use_in_jobs is_success needs_date_ended
    isip.ContractsByEnding 
    jobs.ContractsByEnding
    """

#~ FUNCTION_ID_SECRETARY = 3
#~ FUNCTION_ID_PRESIDENT = 16
#~ FUNCTION_ID_PRESIDENT = 5

def default_signer1():
    return settings.SITE.site_config.signer1
    #~ return SecretaryPresident.secretary_choices()[0]

def default_signer2(): 
    return settings.SITE.site_config.signer2
    #~ return SecretaryPresident.president_choices()[0]

  
class StudyType(dd.BabelNamed):
    #~ text = models.TextField(_("Description"),blank=True,null=True)
    class Meta:
        verbose_name = _("study type")
        verbose_name_plural = _("study types")

class StudyTypes(dd.Table):
    required = dd.required(user_groups='integ',user_level='admin')
    #~ label = _('Study types')
    model = StudyType
    order_by = ["name"]
    detail_layout = """
    name id
    ContractsByStudyType
    """



#~ class ContractBase(contacts.CompanyContact,mixins.DiffingMixin,mixins.TypedPrintable,cal.EventGenerator):
class ContractBase(
    #~ contacts.CompanyContact,
    Signers,
    contacts.ContactRelated,
    mixins.TypedPrintable,
    cal.EventGenerator):
    """
    Abstract base class for 
    :ddref:`jobs.Contract`
    and
    :ddref:`isip.Contract`.
    """
    
    manager_level_field = 'integ_level'
    
    TASKTYPE_CONTRACT_APPLIES_UNTIL = 1
    
    class Meta:
        abstract = True
        
    #~ eventgenerator = models.OneToOneField(cal.EventGenerator,
        #~ related_name="%(app_label)s_%(class)s_ptr",
        #~ parent_link=True)
  
    #~ person = models.ForeignKey(settings.SITE.person_model,
    client = models.ForeignKey('pcsw.Client',
        related_name="%(app_label)s_%(class)s_set_by_client")
        
    language = dd.LanguageField()
    
    applies_from = models.DateField(_("applies from"),blank=True,null=True)
    applies_until = models.DateField(_("applies until"),blank=True,null=True)
    date_decided = models.DateField(blank=True,null=True,verbose_name=_("date decided"))
    date_issued = models.DateField(blank=True,null=True,verbose_name=_("date issued"))
    
    user_asd = models.ForeignKey("users.User",
        verbose_name=_("responsible (ASD)"),
        related_name="%(app_label)s_%(class)s_set_by_user_asd",
        #~ related_name='contracts_asd',
        blank=True,null=True) 
    
    exam_policy = models.ForeignKey("isip.ExamPolicy",
        related_name="%(app_label)s_%(class)s_set",
        blank=True,null=True)
        
    ending = models.ForeignKey("isip.ContractEnding",
        related_name="%(app_label)s_%(class)s_set",
        blank=True,null=True)
    date_ended = models.DateField(blank=True,null=True,verbose_name=_("date ended"))
    
    hidden_columns = 'date_decided date_issued exam_policy user_asd ending date_ended signer1 signer2'
    
    
            
    def __unicode__(self):
        #~ return u'%s # %s' % (self._meta.verbose_name,self.pk)
        #~ return u'%s#%s (%s)' % (self.job.name,self.pk,
            #~ self.person.get_full_name(salutation=False))
        return u'%s#%s (%s)' % (self._meta.verbose_name,self.pk,
            self.client.get_full_name(salutation=False))
    
    #~ def __unicode__(self):
        #~ msg = _("Contract # %s")
        #~ # msg = _("Contract # %(pk)d (%(person)s/%(company)s)")
        #~ # return msg % dict(pk=self.pk, person=self.person, company=self.company)
        #~ return msg % self.pk
        
    def get_recipient(self):
        contact = self.get_contact()
        #~ if self.contact_person:
        if contact is not None:
            #~ contacts = self.get_contact_set()
            return contact
        if self.company:
            return self.company
        return self.client
    recipient = property(get_recipient)
    
    # backwards compat for document templates
    def get_person(self): 
        return self.client
    person = property(get_person)
        
        
    #~ @classmethod
    #~ def contact_choices_queryset(cls,company):
        #~ return contacts.Role.objects.filter(
            #~ type__use_in_contracts=True,
            #~ company=company)

    @classmethod
    def contact_person_choices_queryset(cls,company):
        return settings.SITE.modules.contacts.Person.objects.filter(
            rolesbyperson__company=company,
            rolesbyperson__type__use_in_contracts=True)
            
    @dd.chooser()
    def contact_role_choices(cls):
        return contacts.RoleType.objects.filter(use_in_contracts=True)
        
    @dd.chooser()
    def ending_choices(cls):
        return ContractEnding.objects.filter(use_in_isip=True)
        
        

    #~ def dsbe_person(self): removed 20120921 because no longer used
        #~ """Used in document templates."""
        #~ if self.person_id is not None:
            #~ if self.person.coach2_id is not None:
                #~ return self.person.coach2_id
            #~ return self.person.coach1 or self.user
            
    def client_changed(self,request):
        """
        If the contract's author is the client's primary coach, 
        then set user_asd to None,
        otherwise set user_asd to the primary coach.
        We suppose that only integration agents write contracts.
        """
        if self.client_id is not None:
            #~ pc = self.person.get_primary_coach()
            #~ qs = self.person.get_coachings(self.applies_from,active=True)
            qs = self.client.get_coachings(self.applies_from,type__id=COACHINGTYPE_ASD)
            if qs.count() == 1:
                user_asd = qs[0].user
                if user_asd is None or user_asd == self.user:
                #~ if self.person.coach1_id is None or self.person.coach1_id == self.user_id:
                    self.user_asd = None
                else:
                    self.user_asd = user_asd
                
    def on_create(self,ar):
        super(ContractBase,self).on_create(ar)
        self.client_changed(ar)
      
                    
    def full_clean(self,*args,**kw):
        r = self.active_period()
        if not isrange(*r):
            raise ValidationError(_('Contract ends before it started.'))
        
        if self.type_id and self.type.exam_policy_id:
            if not self.exam_policy_id:
                self.exam_policy_id = self.type.exam_policy_id
                
        if self.client_id is not None:
            msg = OverlappingContractsTest(self.client).check(self)
            if msg:
                #~ print 20130225, translation._trans, translation.get_language()
                raise ValidationError(msg)
        #~ print 20130320, get_field(self.__class__,'signer1').default
        super(ContractBase,self).full_clean(*args,**kw)
        
        if self.type_id is None:
            raise ValidationError(dict(type=_("You must specify a contract type.")))
        

    def update_owned_instance(self,other):
        #~ mixins.Reminder.update_owned_task(self,task)
        #~ contacts.PartnerDocument.update_owned_task(self,task)
        #~ task.company = self.company
        if isinstance(other,mixins.ProjectRelated):
            other.project = self.client
        super(ContractBase,self).update_owned_instance(other)
        
    def after_update_owned_instance(self,other):
        if other.is_user_modified():
            self.update_reminders()
        
        
    def update_cal_rset(self):
        return self.exam_policy
        
    def update_cal_from(self):
        return self.applies_from
        
    def update_cal_calendar(self):
        if self.exam_policy is not None:
            return self.exam_policy.calendar
        
    def update_cal_until(self):
        return self.date_ended or self.applies_until
        
    def update_cal_subject(self,i):
        return _("Evaluation %d") % i
        
    def update_reminders(self):
        super(ContractBase,self).update_reminders()
        au = self.update_cal_until()
        if au:
            au = cal.DurationUnits.months.add_duration(au,-1)
        cal.update_auto_task(
          self.TASKTYPE_CONTRACT_APPLIES_UNTIL,
          self.user,
          au,
          _("Contract ends in a month"),
          self)
          #~ alarm_value=1,alarm_unit=DurationUnit.months)
        
                        
              
    #~ def overlaps_with(self,b):
        #~ if b == self: 
            #~ return False
        #~ a1 = self.applies_from
        #~ a2 = self.date_ended or self.applies_until
        #~ b1 = b.applies_from
        #~ b2 = b.date_ended or b.applies_until
        #~ return overlap(a1,a2,b1,b2)
        
    def active_period(self):
        return (self.applies_from, self.date_ended or self.applies_until)
        #~ r = (self.applies_from, self.date_ended or self.applies_until)
        #~ if isrange(r): return r
        #~ return None
        
        
    #~ def data_control(self):
        #~ msgs = []
        #~ for model in models_by_abc(ContractBase):
            #~ for con in model.objects.filter(person=self.person):
                #~ if self.overlaps_with(con):
                    #~ msgs.append(_("Dates overlap with %s") % con)
        #~ return msgs

#~ dd.update_field(ContractBase,'contact_person',verbose_name=_("represented by"))
dd.update_field(ContractBase,'signer1', default=default_signer1)
dd.update_field(ContractBase,'signer2', default=default_signer2)


class ContractEvents(dd.ChoiceList):
    verbose_name = _("Observed event")
    verbose_name_plural = _("Observed events")
add = ContractEvents.add_item
add('10', _("Started"),'started')
add('20', _("Active"),'active')
add('30', _("Ended"),'ended')
add('40', _("Signed"),'signed')

class ContractBaseTable(dd.Table):
    parameters = dd.ObservedPeriod(
        user = dd.ForeignKey(settings.SITE.user_model,blank=True),
        #~ show_past = models.BooleanField(_("past contracts"),default=True),
        #~ show_active = models.BooleanField(_("active contracts"),default=True),
        #~ show_coming = models.BooleanField(_("coming contracts"),default=True),
        #~ today = models.DateField(_("on"),blank=True,default=datetime.date.today),
      
        observed_event = ContractEvents.field(blank=True,default=ContractEvents.active),
      
        ending_success = dd.YesNo.field(_("Successfully ended"),
            blank=True,help_text="""Contrats terminés avec succès."""),
        ending = models.ForeignKey(ContractEnding,
            blank=True,null=True,
            help_text="""Nur Konventionen mit diesem Beendigungsgrund."""),
        company = models.ForeignKey('contacts.Company',
            blank=True,null=True,
            help_text="""Nur Konventionen mit dieser Organisation als Drittpartner."""),
      
    )
    
    params_layout = """
    user type start_date end_date observed_event
    company ending_success ending
    """
    params_panel_hidden = True
    
    #~ @classmethod
    #~ def param_defaults(self,ar,**kw):
        #~ kw = super(ContractBaseTable,self).param_defaults(ar,**kw)
        #~ D = datetime.date
        #~ kw.update(start_date = D.today())
        #~ kw.update(end_date = D.today())
        #~ return kw
        
    @classmethod
    def get_request_queryset(cls,ar):
        #~ logger.info("20120608.get_request_queryset param_values = %r",ar.param_values)
        qs = super(ContractBaseTable,cls).get_request_queryset(ar)
        #~ user = ar.param_values.get('user',None)
        if ar.param_values.user:
            qs = qs.filter(user=ar.param_values.user)
        if ar.param_values.type:
            qs = qs.filter(type=ar.param_values.type)
        if ar.param_values.company:
            qs = qs.filter(company=ar.param_values.company)
            
        ce = ar.param_values.observed_event
        if ar.param_values.start_date is None or ar.param_values.end_date is None:
            period = None
        else:
            period = (ar.param_values.start_date, ar.param_values.end_date)
        if ce and period is not None:
            if ce == ContractEvents.ended:
                #~ qs = qs.filter(Q(applies_until__lte=period[1]) | Q(date_ended__isnull=False,date_ended__lte=period[1]))
                qs = qs.filter(dd.inrange_filter('applies_until',period)|dd.inrange_filter('date_ended',period))
            elif ce == ContractEvents.started:
                qs = qs.filter(dd.inrange_filter('applies_from',period))
            elif ce == ContractEvents.signed:
                qs = qs.filter(dd.inrange_filter('date_decided',period))
            elif ce == ContractEvents.active:
                f1 = Q(applies_until__isnull=True) | Q(applies_until__gte=period[0])
                flt = f1 & (Q(date_ended__isnull=True) | Q(date_ended__gte=period[0]))
                flt &= Q(applies_from__lte=period[1])
                qs = qs.filter(flt)
                #~ print 20130527, qs.query
            else:
                raise Exception(repr(ce))
        #~ today = ar.param_values.today or datetime.date.today()
        #~ if today:
            #~ if not ar.param_values.show_active:
                #~ flt = range_filter(today,'applies_from','applies_until')
                #~ qs = qs.exclude(flt)
            #~ if not ar.param_values.show_past:
                #~ qs = qs.exclude(applies_until__isnull=False,applies_until__lt=today)
            #~ if not ar.param_values.show_coming:
                #~ qs = qs.exclude(applies_from__isnull=False,applies_from__gt=today)
                
        if ar.param_values.ending_success == dd.YesNo.yes:
            qs = qs.filter(ending__isnull=False,ending__success=True)
        elif ar.param_values.ending_success == dd.YesNo.no:
            qs = qs.filter(ending__isnull=False,ending__success=False)
            
        if ar.param_values.ending is not None:
            qs = qs.filter(ending=ar.param_values.ending)
        #~ logger.info("20130524 %s",qs.query)
        return qs
    
    
    @classmethod
    def get_title_tags(self,ar):
        for t in super(ContractBaseTable,self).get_title_tags(ar):
            yield t
            
        pv = ar.param_values
        if pv.start_date is None or pv.end_date is None:
            period = None
        else:
            oe = pv.observed_event
            if oe is not None:
                yield "%s %s-%s" % (unicode(oe.text),dd.dtos(pv.start_date), dd.dtos(pv.end_date))
            
        if ar.param_values.company:
            yield unicode(ar.param_values.company)
            



class OverlappingContractsTest:
    """
    Volatile object used to test for overlapping contracts.
    """
    def __init__(self,client):
        """
        Test whether this client has overlapping contracts.
        """
        #~ from lino_welfare.modlib.isip.models import ContractBase
        self.client = client
        self.actives = []
        for model in dd.models_by_base(ContractBase):
            for con1 in model.objects.filter(client=client):
                ap = con1.active_period()
                if ap[0] is None and ap[1] is None: continue
                self.actives.append((ap,con1))
        
    def check(self,con1):
        ap = con1.active_period()
        if ap[0] is None and ap[1] is None:
            return
        if False:
            cp = (self.client.coached_from,self.client.coached_until)
            if not encompass(cp,ap):
                return _("Date range %(p1)s lies outside of coached period %(p2)s.") \
                    % dict(p2=rangefmt(cp),p1=rangefmt(ap))
        for (p2,con2) in self.actives:
            if con1 != con2 and overlap2(ap,p2):
                return _("Date range overlaps with %(ctype)s #%(id)s") % dict(
                  ctype=con2.__class__._meta.verbose_name,
                  id=con2.pk
                )
        return None
        
    def check_all(self):
        messages = []
        for (p1,con1) in self.actives:
            msg = self.check(con1)
            if msg:
                messages.append(
                  _("%(ctype)s #%(id)s : %(msg)s") % dict(
                    msg=msg,
                    ctype=con1.__class__._meta.verbose_name,
                    id=con1.pk))
        return messages
        

            
    
class Contract(ContractBase):
    """
    ISIP = Individual Social Integration Project (VSE)
    """
    class Meta:
        verbose_name = _("ISIP")
        verbose_name_plural = _("ISIPs")
        
    type = models.ForeignKey("isip.ContractType",
        related_name="%(app_label)s_%(class)s_set_by_type",
        verbose_name=_("Contract Type"),blank=True)
    
    stages = dd.RichTextField(_("stages"),
        blank=True,null=True,format='html')
    goals = dd.RichTextField(_("goals"),
        blank=True,null=True,format='html')
    duties_asd = dd.RichTextField(_("duties ASD"),
        blank=True,null=True,format='html')
    duties_dsbe = dd.RichTextField(_("duties DSBE"),
        blank=True,null=True,format='html')
    duties_company = dd.RichTextField(_("duties company"),
        blank=True,null=True,format='html')
    duties_person = dd.RichTextField(_("duties person"),
        blank=True,null=True,format='html')
        
    hidden_columns = (ContractBase.hidden_columns 
        + " stages goals duties_asd duties_dsbe duties_company duties_person")
        
    study_type = models.ForeignKey('isip.StudyType',blank=True,null=True)
      
        
    
    @classmethod
    def on_analyze(cls,lino):
        """
        Here's how to override the default verbose_name of a field.
        """
        #~ resolve_field('dsbe.Contract.user').verbose_name=_("responsible (DSBE)")
        Contract.user.verbose_name=_("responsible (DSBE)")
        #~ lino.CONTRACT_PRINTABLE_FIELDS = dd.fields_list(cls,
        cls.PRINTABLE_FIELDS = dd.fields_list(cls,
            'client company contact_person contact_role type '
            'applies_from applies_until '
            'language '
            'stages goals duties_dsbe duties_company '
            'duties_asd duties_person '
            'user user_asd exam_policy '
            'date_decided date_issued ')
        super(Contract,cls).on_analyze(lino)
        
    def disabled_fields(self,ar):
        #~ if self.must_build:
        if not self.build_time:
            return []
        #~ return df + settings.SITE.CONTRACT_PRINTABLE_FIELDS
        return self.PRINTABLE_FIELDS


class ContractDetail(dd.FormLayout):
    general = dd.Panel("""
    id:8 client:25 type user:15 user_asd:15
    study_type  company contact_person contact_role
    applies_from applies_until exam_policy language:8
    
    date_decided date_issued date_ended ending:20
    # signer1 signer2
    cal.TasksByController cal.EventsByController
    """,label = _("General"))
    
    isip = dd.Panel("""
    stages        goals
    duties_asd    duties_dsbe
    duties_company duties_person
    """,label = _("ISIP"))
    
    main = "general isip"
    
    #~ def setup_handle(self,dh):
        #~ dh.general.label = _("General")
        #~ dh.isip.label = _("ISIP")


class Contracts(ContractBaseTable):
    required = dd.required(user_groups='integ')
    model = Contract
    column_names = 'id applies_from applies_until client user type *'
    order_by = ['id']
    #~ active_fields = ('company','contact')
    active_fields = ['company']
    detail_layout = ContractDetail()
    insert_layout = dd.FormLayout("""
    client
    type company
    """,window_size=(60,'auto'))    
    
    parameters = dict(
      type = models.ForeignKey(ContractType,blank=True),
      study_type = models.ForeignKey('isip.StudyType',blank=True),
      **ContractBaseTable.parameters)
      
    params_layout = """
    user type start_date end_date observed_event
    company:20 study_type:15 ending_success:20 ending
    """
    
    @classmethod
    def get_request_queryset(cls,ar):
        #~ logger.info("20120608.get_request_queryset param_values = %r",ar.param_values)
        qs = super(Contracts,cls).get_request_queryset(ar)
        if ar.param_values.study_type:
            qs = qs.filter(study_type=ar.param_values.study_type)
        return qs
            
    @classmethod
    def get_title_tags(self,ar):
        for t in super(Contracts,self).get_title_tags(ar):
            yield t
            
        if ar.param_values.study_type:
            yield unicode(ar.param_values.study_type)
            
      
    
class MyContracts(Contracts):
#~ class MyContracts(Contracts,mixins.ByUser):
    #~ column_names = "applies_from client *"
    #~ label = _("My ISIP contracts")
    #~ label = _("My PIIS contracts")
    #~ order_by = "reminder_date"
    #~ column_names = "reminder_date client company *"
    #~ order_by = ["applies_from"]
    #~ filter = dict(reminder_date__isnull=False)
    
    #~ debug_permissions = 20121127

      
    @classmethod
    def param_defaults(self,ar,**kw):
        kw = super(MyContracts,self).param_defaults(ar,**kw)
        kw.update(user=ar.get_user())
        return kw
      


    
class ContractsByPerson(Contracts):
    master_key = 'client'
    column_names = 'applies_from applies_until user type *'

class ContractsByPolicy(Contracts):
    master_key = 'exam_policy'
    #~ column_names = 'applies_from applies_until user type *'

       
class ContractsByType(Contracts):
    master_key = 'type'
    column_names = "applies_from client user *"
    order_by = ["applies_from"]

class ContractsByEnding(Contracts):
    master_key = 'ending'
    
class ContractsByStudyType(Contracts):
    master_key = 'study_type'
    
#~ def customize_siteconfig():
    #~ from lino.ui.models import SiteConfig
    #~ dd.inject_field(SiteConfig,
        #~ 'signer1_function',
        #~ models.ForeignKey("contacts.RoleType",
            #~ blank=True,null=True,
            #~ verbose_name=_("First signer function"),
            #~ help_text=_("""Contact function to designate the secretary."""),
            #~ related_name="%(app_label)s_%(class)s_set_by_signer1"))
    #~ dd.inject_field(SiteConfig,
        #~ 'signer2_function',
        #~ models.ForeignKey("contacts.RoleType",
            #~ blank=True,null=True,
            #~ verbose_name=_("Second signer function"),
            #~ help_text=_("Contact function to designate the president."),
            #~ related_name="%(app_label)s_%(class)s_set_by_signer2"))
        #~ 
#~ customize_siteconfig()


#~ from lino_welfare.modlib.integ import App

#~ def setup_main_menu(site,ui,profile,m): 
    #~ m  = m.add_menu("integ",App.verbose_name)
    #~ m.add_action(MyContracts)
    
#~ def setup_config_menu(site,ui,profile,m): 
    #~ m  = m.add_menu("integ",App.verbose_name)
    #~ m.add_action(ContractTypes)
    #~ m.add_action(ContractEndings)
    #~ m.add_action(ExamPolicies)
    #~ m.add_action(StudyTypes)
  #~ 
#~ def setup_explorer_menu(site,ui,profile,m):
    #~ m  = m.add_menu("integ",App.verbose_name)
    #~ m.add_action(Contracts)
#~ 
