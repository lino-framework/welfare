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

"""
from __future__ import unicode_literals

import logging
logger = logging.getLogger(__name__)

import datetime

from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.conf import settings
from django.db.models import Q

from lino import dd
from lino.utils.xmlgen.html import E

contacts = dd.resolve_app('contacts')
pcsw = dd.resolve_app('pcsw')
isip = dd.resolve_app('isip')
jobs = dd.resolve_app('jobs')
courses = dd.resolve_app('courses')
users = dd.resolve_app('users')


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
        
        DSBE = pcsw.CoachingType.objects.get(pk=isip.COACHINGTYPE_DSBE)
        
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

        yield add(pcsw.Coachings,observed_event=pcsw.CoachingEvents.started,coaching_type=DSBE)
        yield add(pcsw.Coachings,observed_event=pcsw.CoachingEvents.active,coaching_type=DSBE)
        yield add(pcsw.Coachings,observed_event=pcsw.CoachingEvents.ended,coaching_type=DSBE)
        
        yield add(pcsw.Clients,observed_event=pcsw.ClientEvents.coached)
        yield add(pcsw.Clients,observed_event=pcsw.ClientEvents.created)
        yield add(pcsw.Clients,observed_event=pcsw.ClientEvents.modified)
        
        for A in (isip.Contracts,jobs.Contracts):
            yield add(A,observed_event=isip.ContractEvents.started)
            yield add(A,observed_event=isip.ContractEvents.active)
            yield add(A,observed_event=isip.ContractEvents.ended)
            yield add(A,observed_event=isip.ContractEvents.signed)
        

    
class CoachingEndingsByUser(dd.VentilatingTable,pcsw.CoachingEndings):
    label = _("Coaching endings by user")
    hide_zero_rows = True

    @classmethod
    def get_ventilated_columns(self):
        try:
            DSBE = pcsw.CoachingType.objects.get(pk=isip.COACHINGTYPE_DSBE)
        except pcsw.CoachingType.DoesNotExist:
            DSBE = None
        def w(user):
            def func(fld,obj,ar):
                mi = ar.master_instance
                if mi is None: return None
                pv = dict(start_date=mi.start_date,end_date=mi.end_date)
                pv.update(observed_event=pcsw.CoachingEvents.ended)
                pv.update(coaching_type=DSBE)
                if user is not None:
                    pv.update(coached_by=user)
                pv.update(ending=obj)
                return pcsw.Coachings.request(param_values=pv)
            return func
        #~ for u in settings.SITE.user_model.objects.exclude(profile=''):
        #~ for u in settings.SITE.user_model.objects.filter(coaching_type__id=isip.COACHINGTYPE_DSBE):
        for u in settings.SITE.user_model.objects.all():
            yield dd.RequestField(w(u),verbose_name=unicode(u.username))
        yield dd.RequestField(w(None),verbose_name=_("Total"))
    
   
class CoachingEndingsByType(dd.VentilatingTable,pcsw.CoachingEndings): # not currently used
    
    label = _("Coaching endings by type")
    
    @classmethod
    def get_ventilated_columns(self):
        def w(ct):
            def func(fld,obj,ar):
                mi = ar.master_instance
                if mi is None: return None
                pv = dict(start_date=mi.start_date,end_date=mi.end_date)
                pv.update(observed_event=pcsw.CoachingEvents.ended)
                if ct is not None:
                    pv.update(coaching_type=ct)
                pv.update(ending=obj)
                return pcsw.Coachings.request(param_values=pv)
            return func
        for ct in pcsw.CoachingType.objects.all():
            yield dd.RequestField(w(ct),verbose_name=unicode(ct))
        yield dd.RequestField(w(None),verbose_name=_("Total"))
    

class ContractsByType(dd.VentilatingTable):
    contracts_table = isip.Contracts
    contract_type_model = isip.ContractType
    observed_event = isip.ContractEvents.ended
    selector_key = NotImplementedError
    hide_zero_rows = True
    
    @classmethod
    def get_observed_period(self,mi):
        return dict(start_date=mi.start_date,end_date=mi.end_date)        
        
    @classmethod
    def get_ventilated_columns(self):
        def w(ct):
            def func(fld,obj,ar):
                mi = ar.master_instance
                if mi is None: return None
                pv = self.get_observed_period(mi)
                pv.update(observed_event=self.observed_event)
                if ct is not None:
                    pv.update(type=ct)
                pv[self.selector_key] = obj
                return self.contracts_table.request(param_values=pv)
            return func
        for ct in self.contract_type_model.objects.all():
            yield dd.RequestField(w(ct),verbose_name=unicode(ct))
        yield dd.RequestField(w(None),verbose_name=_("Total"))

class ContractEndingsByType(ContractsByType,isip.ContractEndings):
    label = _("Contract endings by type")
    selector_key = 'ending'
    
class JobsContractEndingsByType(ContractEndingsByType):
    contracts_table = jobs.Contracts
    contract_type_model = jobs.ContractType
    

class ContractsPerUserAndContractType(ContractsByType,users.Users):
    label = _("PIIS par agent et type")
    #~ filter = Q(coaching_type=isip.COACHINGTYPE_DSBE)
    contracts_table = isip.Contracts
    observed_event = isip.ContractEvents.active
    contract_type_model = isip.ContractType
    selector_key = 'user'
    
    @classmethod
    def get_observed_period(self,mi):
        return dict(start_date=mi.end_date,end_date=mi.end_date)
    
class JobsContractsPerUserAndContractType(ContractsPerUserAndContractType):
    label = _("Art60§7 par agent et type")
    contracts_table = jobs.Contracts
    contract_type_model = jobs.ContractType
    
    
    
    
class StudyTypesAndContracts(isip.StudyTypes,dd.VentilatingTable):
    label = _("PIIS et types de formation")
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
        def w(ct):
            def func(fld,obj,ar):
                mi = ar.master_instance
                if mi is None: return None
                pv = dict(start_date=mi.start_date,end_date=mi.end_date)
                pv.update(observed_event=isip.ContractEvents.active)
                if ct is not None:
                    pv.update(type=ct)
                pv.update(study_type=obj)
                return self.contracts_table.request(param_values=pv)
            return func
        for ct in isip.ContractType.objects.filter(needs_study_type=True):
            yield dd.RequestField(w(ct),verbose_name=unicode(ct))
        yield dd.RequestField(w(None),verbose_name=_("Total"))
    

class CompaniesAndContracts(contacts.Companies,dd.VentilatingTable):
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
        
    @dd.virtualfield(dd.ForeignKey('contacts.Company'))
    def description(self,obj,ar):
        return obj
        
    @classmethod
    def get_ventilated_columns(self):
        def w(ct):
            def func(fld,obj,ar):
                mi = ar.master_instance
                if mi is None: return None
                pv = dict(start_date=mi.start_date,end_date=mi.end_date)
                pv.update(observed_event=isip.ContractEvents.active)
                if ct is not None:
                    pv.update(type=ct)
                pv.update(company=obj)
                return self.contracts_table.request(param_values=pv)
            return func
        for ct in self.contract_types.objects.all():
            label = unicode(ct)
            yield dd.RequestField(w(ct),verbose_name=label)
        yield dd.RequestField(w(None),verbose_name=_("Total"))
    


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
        #~ yield E.p('.')
        #~ yield CoachingEndingsByType
        
        
        yield E.h1(isip.Contract._meta.verbose_name_plural)
        #~ yield E.p("Voici quelques tables complètes:")
        #~ for A in (pcsw.UsersWithClients,StudyTypesAndContracts,CompaniesAndContracts):
        for A in (ContractsPerUserAndContractType,CompaniesAndContracts,ContractEndingsByType,StudyTypesAndContracts):
            yield E.h2(A.label)
            if A.help_text:
                yield E.p(unicode(A.help_text))
            yield A

        yield E.h1(jobs.Contract._meta.verbose_name_plural)
        for A in (JobsContractsPerUserAndContractType,JobProvidersAndContracts,JobsContractEndingsByType):
            yield E.h2(A.label)
            if A.help_text:
                yield E.p(unicode(A.help_text))
            yield A



def setup_main_menu(site,ui,profile,m): 
    m  = m.add_menu("integ",pcsw.INTEG_MODULE_LABEL)
    m.add_action(ActivityReport)
