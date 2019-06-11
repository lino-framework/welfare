# -*- coding: UTF-8 -*-
# Copyright 2013-2018 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

"""
The :xfile:`models` module for the :mod:`lino_welfare.modlib.integ` app.

"""
from __future__ import unicode_literals

from builtins import str
import logging
logger = logging.getLogger(__name__)

import datetime

from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.db.utils import DatabaseError
from django.conf import settings

from etgen.html import E
from lino.utils.report import Report
from lino.mixins import ObservedDateRange
from lino.modlib.users.choicelists import UserTypes
from lino.modlib.system.choicelists import PeriodEvents

from lino.api import dd, rt, gettext
from .roles import IntegUser

config = dd.plugins.integ

contacts = dd.resolve_app('contacts')
pcsw = dd.resolve_app('pcsw')
isip = dd.resolve_app('isip')
jobs = dd.resolve_app('jobs')
courses = dd.resolve_app('courses')
cv = dd.resolve_app('cv')
# properties = dd.resolve_app('properties')

from lino_xl.lib.coachings.utils import has_contracts_filter
from lino_xl.lib.clients.choicelists import ClientEvents, ObservedEvent
from lino_xl.lib.clients.choicelists import ClientStates
from lino_xl.lib.coachings.desktop import CoachingEndings


class ClientIsAvailable(ObservedEvent):
    text = _("Available")

    def add_filter(self, qs, pv):
        period = (pv.start_date, pv.end_date)
        flt = has_contracts_filter('isip_contract_set_by_client', period)
        flt |= has_contracts_filter('job_contract_set_by_client', period)
        if dd.is_installed('immersion'):
            flt |= has_contracts_filter(
                'immersion_contract_set_by_client', period)
        qs = qs.exclude(flt)
        return qs

ClientEvents.add_item_instance(ClientIsAvailable("available"))


class Clients(pcsw.CoachedClients):
    # Black right-pointing triangle : U+25B6   &#9654;
    # Black right-pointing pointer : U+25BA    &#9658;
    help_text = """Wie Kontakte --> Klienten, aber mit \
    DSBE-spezifischen Kolonnen und Filterparametern."""
    #~ detail_layout = IntegClientDetail()
    required_roles = dd.login_required(IntegUser)
    params_panel_hidden = True
    title = _("Integration Clients")
    order_by = "last_name first_name id".split()
    allow_create = False  # see blog/2012/0922
    use_as_default_table = False
    column_names = "name_column:20 #active_contract:16 \
    applies_from applies_until contract_company:16 \
    national_id:10 gsm:10 address_column age:10 email phone:10 \
    id aid_type language:10"

    parameters = dict(
        group=dd.ForeignKey("pcsw.PersonGroup", blank=True, null=True,
                                verbose_name=_("Integration phase")),
        language=dd.ForeignKey('languages.Language',
                               verbose_name=_("Language knowledge"),
                               blank=True, null=True),
        wanted_property=dd.ForeignKey('properties.Property',
                                      verbose_name=_("Wanted skill"),
                                      blank=True, null=True),
        only_active=models.BooleanField(
            _("Only active clients"), default=False,
            help_text=_(
                "Show only clients in 'active' integration phases")),
        **pcsw.CoachedClients.parameters)

    params_layout = """
    client_state coached_by and_coached_by start_date end_date observed_event
    aged_from aged_to gender nationality also_obsolete
    language wanted_property group only_active only_primary
    """

    @classmethod
    def param_defaults(self, ar, **kw):
        kw = super(Clients, self).param_defaults(ar, **kw)
        kw.update(client_state=ClientStates.coached)
        kw.update(coached_by=ar.get_user())
        # kw.update(only_primary=True)
        return kw

    @classmethod
    def get_request_queryset(self, ar):
        #~ ar.param_values.update(client_state = ClientStates.coached)
        qs = super(Clients, self).get_request_queryset(ar)
        if ar.param_values.language:
            qs = qs.filter(languageknowledge__language=
                           ar.param_values.language).distinct()
        if ar.param_values.wanted_property:
            qs = qs.filter(personproperty__property=
                           ar.param_values.wanted_property).distinct()

        if ar.param_values.group:
            qs = qs.filter(group=ar.param_values.group)
        if ar.param_values.only_active:
            qs = qs.filter(group__active=True)
        return qs

    @classmethod
    def get_title_tags(self, ar):
        for t in super(Clients, self).get_title_tags(ar):
            yield t
        if ar.param_values.only_active:
            yield str(ar.actor.parameters['only_active'].verbose_name)
        if ar.param_values.language:
            yield str(
                ar.actor.parameters['language'].verbose_name) + \
                ' ' + str(ar.param_values.language)
        if ar.param_values.group:
            yield str(ar.param_values.group)


class UsersWithClients(dd.VirtualTable):
    """An overview table for agents of the integration service.


    """
    required_roles = dd.login_required(IntegUser)
    label = _("Users with their Clients")

    display_mode = 'html'

    @classmethod
    def get_data_rows(self, ar):
        """We only want the users who actually have at least one client.
        We store the corresponding request in the user object
        under the name `my_persons`.

        The list displays only integration agents, i.e. users with a
        nonempty `integ_level`.  With one subtility: system admins
        also have a nonempty `integ_level`, but normal users don't
        want to see them.  So we add the rule that only system admins
        see other system admins.

        """
        u = ar.get_user()
        if u is None or not u.user_type.has_required_roles([dd.SiteAdmin]):
            user_types = [p for p in UserTypes.items()
                        if p.has_required_roles([IntegUser])
                        and not p.has_required_roles([dd.SiteAdmin])]
        else:
            user_types = [
                p for p in UserTypes.items()
                if p.has_required_roles([IntegUser])]

        qs = rt.models.users.User.objects.filter(user_type__in=user_types)
        for user in qs.order_by('username'):
            r = Clients.request(param_values=dict(coached_by=user))
            if r.get_total_count():
                user.my_persons = r
                yield user

    @dd.virtualfield('coachings.Coaching.user')
    def user(self, obj, ar):
        return obj

    @dd.requestfield(_("Total"))
    def row_total(self, obj, ar):
        return obj.my_persons

    @dd.requestfield(_("Primary clients"))
    def primary_clients(self, obj, ar):
        t = dd.today()
        return Clients.request(param_values=dict(
            only_primary=True, coached_by=obj, start_date=t, end_date=t))

    @dd.requestfield(_("Active clients"))
    def active_clients(self, obj, ar):
        #~ return MyActiveClients.request(ar.ui,subst_user=obj)
        t = dd.today()
        return Clients.request(param_values=dict(
            only_active=True, only_primary=True,
            coached_by=obj, start_date=t, end_date=t))


@dd.receiver(dd.post_analyze)
def on_database_ready(sender, **kw):
    """
    Builds columns dynamically from the :class:`PersonGroup` database table.

    This must also be called before each test case.
    """
    self = UsersWithClients
    self.column_names = 'user:10'
    try:
        for pg in pcsw.PersonGroup.objects.exclude(
                ref_name='').order_by('ref_name'):
            def w(pg):
                # we must evaluate `today` for each request, not only
                # once on server startup
                today = dd.today()
                pv = dict(group=pg, start_date=today, end_date=today)
                if dd.plugins.integ.only_primary:
                    pv.update(only_primary=True)

                def func(self, obj, ar):
                    pv.update(coached_by=obj)
                    return Clients.request(param_values=pv)
                return func
            vf = dd.RequestField(w(pg), verbose_name=pg.name)
            self.add_virtual_field('G' + pg.ref_name, vf)
            self.column_names += ' ' + vf.name
    except DatabaseError:
        pass  # happens e.g. if database isn't yet initialized

    self.column_names += ' primary_clients active_clients row_total'
    self.clear_handle()  # avoid side effects when running multiple test cases
    settings.SITE.resolve_virtual_fields()


class CompareRequestsTable(dd.VirtualTable):
    """
    This is one of the tables of the :class:`ActivityReport`.

    """
    label = _("Evolution générale")
    auto_fit_column_widths = True
    column_names = "description old_value new_value"
    display_mode = 'html'
    hide_sums = True

    @dd.displayfield(_("Description"))
    def description(self, row, ar):
        return row[0]

    @dd.requestfield(_("Initial value"))
    def old_value(self, row, ar):
        return row[1]

    @dd.requestfield(_("Final value"))
    def new_value(self, row, ar):
        return row[2]

    @classmethod
    def get_data_rows(self, ar):
        #~ rows = []
        pv = ar.master_instance
        if pv is None:
            return
        #~ def add(A,oe=None,**kw):

        def add(A, **kw):
            pva = dict(**kw)
            ar = A.request(param_values=pva)
            cells = [ar.get_title()]
            for d in (pv.start_date, pv.end_date):
                ar = A.request(
                    param_values=dict(pva, start_date=d, end_date=d))
                #~ print 20130527, ar
                cells.append(ar)
            return cells

        yield add(
            pcsw.CoachedClients, observed_event=pcsw.ClientEvents.active)

        yield add(isip.Contracts, observed_event=isip.ContractEvents.active)
        #~ yield add(isip.Contracts,isip.ContractEvents.ended)
        yield add(jobs.Contracts, observed_event=isip.ContractEvents.active)
        #~ yield add(jobs.Contracts,isip.ContractEvents.ended)

        if hasattr(courses, 'PendingCourseRequests'):
            # chatelet uses `lino.modlib.courses` which doesn't have
            # this table.
            yield add(courses.PendingCourseRequests)

        all_contracts = isip.Contracts.request(
            param_values=dict(
                start_date=pv.start_date,
                end_date=pv.end_date)).get_data_iterator()
        # DISTINCT on fields doesn't work in sqlite
        study_types = set(all_contracts.values_list('study_type', flat=True))
        #~ print 20130527, study_types
        for st in study_types:
            if st is not None:
                yield add(isip.Contracts,
                          observed_event=isip.ContractEvents.active,
                          study_type=cv.StudyType.objects.get(pk=st))


class PeriodicNumbers(dd.VirtualTable):
    label = _("Indicateurs d'activité")
    auto_fit_column_widths = True
    column_names = "description number"
    display_mode = 'html'
    hide_sums = True

    @dd.displayfield(_("Description"))
    def description(self, row, ar):
        return row[0]

    @dd.requestfield(_("Number"))
    def number(self, row, ar):
        return row[1]

    @classmethod
    def get_data_rows(self, ar):

        mi = ar.master_instance
        if mi is None:
            return

        DSBE = rt.models.coachings.CoachingType.objects.get(
            pk=isip.COACHINGTYPE_DSBE)

        def add(A, **pva):
            #~ pva = dict(**kw)
            ar = A.request(param_values=pva)
            cells = [ar.get_title()]
            ar = A.request(
                param_values=dict(pva, start_date=mi.start_date, end_date=mi.end_date))
            cells.append(ar)
            return cells

        #~ def add(A,oe):
            #~ cells = ["%s %s" % (A.model._meta.verbose_name_plural,oe.text)]
            #~ pv = dict(start_date=mi.start_date,end_date=mi.end_date)
            #~ pv.update(observed_event=oe)
            #~ ar = A.request(param_values=pv)
            #~ cells.append(ar)
            #~ return cells
        yield add(
            rt.models.coachings.Coachings,
            observed_event=PeriodEvents.started, coaching_type=DSBE)
        yield add(
            rt.models.coachings.Coachings,
            observed_event=PeriodEvents.active, coaching_type=DSBE)
        yield add(
            rt.models.coachings.Coachings,
            observed_event=PeriodEvents.ended, coaching_type=DSBE)

        yield add(pcsw.Clients, observed_event=pcsw.ClientEvents.active)
        yield add(pcsw.Clients, observed_event=pcsw.ClientEvents.created)
        yield add(pcsw.Clients, observed_event=pcsw.ClientEvents.modified)

        for A in (isip.Contracts, jobs.Contracts):
            yield add(A, observed_event=isip.ContractEvents.started)
            yield add(A, observed_event=isip.ContractEvents.active)
            yield add(A, observed_event=isip.ContractEvents.ended)
            yield add(A, observed_event=isip.ContractEvents.decided)
            yield add(A, observed_event=isip.ContractEvents.issued)


class CoachingEndingsByUser(dd.VentilatingTable, CoachingEndings):
    label = _("Coaching endings by user")
    hide_zero_rows = True

    @classmethod
    def get_ventilated_columns(self):
        try:
            DSBE = rt.models.coachings.CoachingType.objects.get(
                pk=isip.COACHINGTYPE_DSBE)
        except rt.models.coachings.CoachingType.DoesNotExist:
            DSBE = None

        def w(user):
            def func(fld, obj, ar):
                mi = ar.master_instance
                if mi is None:
                    return None
                pv = dict(start_date=mi.start_date, end_date=mi.end_date)
                pv.update(observed_event=PeriodEvents.ended)
                pv.update(coaching_type=DSBE)
                if user is not None:
                    pv.update(coached_by=user)
                pv.update(ending=obj)
                return rt.models.coachings.Coachings.request(param_values=pv)
            return func

        user_types = [p for p in UserTypes.items()
                    if p.has_required_roles([IntegUser])]
        for u in settings.SITE.user_model.objects.filter(user_type__in=user_types):
            yield dd.RequestField(w(u), verbose_name=str(u.username))
        yield dd.RequestField(w(None), verbose_name=_("Total"))


# not currently used
class CoachingEndingsByType(dd.VentilatingTable, CoachingEndings):

    label = _("Coaching endings by type")

    @classmethod
    def get_ventilated_columns(self):
        def w(ct):
            def func(fld, obj, ar):
                mi = ar.master_instance
                if mi is None:
                    return None
                pv = dict(start_date=mi.start_date, end_date=mi.end_date)
                pv.update(observed_event=PeriodEvents.ended)
                if ct is not None:
                    pv.update(coaching_type=ct)
                pv.update(ending=obj)
                return rt.models.coachings.Coachings.request(
                    param_values=pv)
            return func
        for ct in rt.models.coachings.CoachingType.objects.all():
            yield dd.RequestField(w(ct), verbose_name=str(ct))
        yield dd.RequestField(w(None), verbose_name=_("Total"))


class ContractsByType(dd.VentilatingTable):
    contracts_table = isip.Contracts
    contract_type_model = isip.ContractType
    observed_event = isip.ContractEvents.ended
    selector_key = NotImplementedError
    hide_zero_rows = True

    @classmethod
    def get_observed_period(self, mi):
        return dict(start_date=mi.start_date, end_date=mi.end_date)

    @classmethod
    def get_ventilated_columns(self):
        def w(ct):
            def func(fld, obj, ar):
                mi = ar.master_instance
                if mi is None:
                    return None
                pv = self.get_observed_period(mi)
                pv.update(observed_event=self.observed_event)
                if ct is not None:
                    pv.update(type=ct)
                pv[self.selector_key] = obj
                return self.contracts_table.request(param_values=pv)
            return func
        for ct in self.contract_type_model.objects.all():
            yield dd.RequestField(w(ct), verbose_name=str(ct))
        yield dd.RequestField(w(None), verbose_name=_("Total"))


class ContractEndingsByType(ContractsByType, isip.ContractEndings):
    label = _("Contract endings by type")
    selector_key = 'ending'


class JobsContractEndingsByType(ContractEndingsByType):
    contracts_table = jobs.Contracts
    contract_type_model = jobs.ContractType

from lino_welfare.modlib.users.desktop import Users

class ContractsPerUserAndContractType(ContractsByType, Users):
    label = _("PIIS par agent et type")
    #~ filter = Q(coaching_type=isip.COACHINGTYPE_DSBE)
    contracts_table = isip.Contracts
    observed_event = isip.ContractEvents.active
    contract_type_model = isip.ContractType
    selector_key = 'user'

    @classmethod
    def get_observed_period(self, mi):
        return dict(start_date=mi.end_date, end_date=mi.end_date)


class JobsContractsPerUserAndContractType(ContractsPerUserAndContractType):
    label = _("Art60§7 par agent et type")
    contracts_table = jobs.Contracts
    contract_type_model = jobs.ContractType


class StudyTypesAndContracts(cv.StudyTypes, dd.VentilatingTable):
    label = _("PIIS et types de formation")
    help_text = _("""Nombre de PIIS actifs par 
    type de formation et type de contrat.""")
    contracts_table = isip.Contracts

    @classmethod
    def get_request_queryset(cls, ar):
        #~ logger.info("20120608.get_request_queryset param_values = %r",ar.param_values)
        qs = super(StudyTypesAndContracts, cls).get_request_queryset(ar)
        qs = qs.annotate(count=models.Count('contract'))
        return qs.filter(count__gte=1)
        #~ return qs

    @dd.virtualfield(dd.ForeignKey(
        'cv.StudyType'))  # , verbose_name=_("Description")))
    def description(self, obj, ar):
        return obj

    @classmethod
    def get_ventilated_columns(self):
        def w(ct):
            def func(fld, obj, ar):
                mi = ar.master_instance
                if mi is None:
                    return None
                pv = dict(start_date=mi.start_date, end_date=mi.end_date)
                pv.update(observed_event=isip.ContractEvents.active)
                if ct is not None:
                    pv.update(type=ct)
                pv.update(study_type=obj)
                return self.contracts_table.request(param_values=pv)
            return func
        for ct in isip.ContractType.objects.filter(needs_study_type=True):
            yield dd.RequestField(w(ct), verbose_name=str(ct))
        yield dd.RequestField(w(None), verbose_name=_("Total"))


class CompaniesAndContracts(contacts.Companies, dd.VentilatingTable):
    label = _("Organisations externes et contrats")
    help_text = _("""Nombre de PIIS actifs par 
    organisation externe et type de contrat.""")
    contracts_table = isip.Contracts
    contract_types = isip.ContractType
    hide_zero_rows = True

    @classmethod
    def get_request_queryset(cls, ar):
        qs = super(CompaniesAndContracts, cls).get_request_queryset(ar)
        qs = qs.annotate(count=models.Count(
            'isip_contractpartner_set_by_company'))
        return qs.filter(count__gte=1)

    @dd.virtualfield(dd.ForeignKey('contacts.Company'))
    def description(self, obj, ar):
        return obj

    @classmethod
    def get_ventilated_columns(self):
        def w(ct):
            def func(fld, obj, ar):
                mi = ar.master_instance
                if mi is None:
                    return None
                pv = dict(start_date=mi.start_date, end_date=mi.end_date)
                pv.update(observed_event=isip.ContractEvents.active)
                if ct is not None:
                    pv.update(type=ct)
                pv.update(company=obj)
                return self.contracts_table.request(param_values=pv)
            return func
        for ct in self.contract_types.objects.all():
            label = str(ct)
            yield dd.RequestField(w(ct), verbose_name=label)
        yield dd.RequestField(w(None), verbose_name=_("Total"))


class JobProvidersAndContracts(CompaniesAndContracts):
    """Ventilates number of job supplyments by provider and type."""
    label = _("Job providers and contrats")
    contracts_table = jobs.Contracts
    contract_types = jobs.ContractType

    @classmethod
    def get_request_queryset(cls, ar):
        #~ qs = super(CompaniesAndContracts,cls).get_request_queryset(ar)
        qs = jobs.JobProvider.objects.all()
        qs = qs.annotate(count=models.Count('jobs_contract_set_by_company'))
        return qs.filter(count__gte=1)


class ActivityReport(Report):
    """Gives an overview about the work of the Integration Service during
    a given period.

    """

    required_roles = dd.login_required(IntegUser)
    label = _("Activity Report")

    parameters = ObservedDateRange(
        # start_date=models.DateField(verbose_name=_("Period from")),
        # end_date=models.DateField(verbose_name=_("until")),
        include_jobs=models.BooleanField(
            verbose_name=dd.plugins.jobs.verbose_name),
        include_isip=models.BooleanField(verbose_name=_("ISIP")),
    )

    params_layout = "start_date end_date include_jobs include_isip"
    #~ params_panel_hidden = True

    @classmethod
    def param_defaults(self, ar, **kw):
        D = datetime.date
        kw.update(start_date=D(dd.today().year, 1, 1))
        kw.update(end_date=D(dd.today().year, 12, 31))
        return kw

    @classmethod
    def get_story(cls, self, ar):
        yield E.h2(gettext("Introduction"))
        yield E.p("Ceci est un ", E.b("rapport"), """,
càd un document complet généré par Lino, contenant des
sections, des tables et du texte libre.
Dans la version écran cliquer sur un chiffre pour voir d'où
il vient.
""")
        yield E.h2(str(UsersWithClients.label))
        yield UsersWithClients
        yield E.h2(gettext("Indicateurs généraux"))
        yield CompareRequestsTable
        yield E.p('.')
        yield PeriodicNumbers

        yield E.h2(gettext("Causes d'arrêt des interventions"))
        yield CoachingEndingsByUser
        #~ yield E.p('.')
        #~ yield CoachingEndingsByType

        yield E.h1(str(isip.Contract._meta.verbose_name_plural))
        #~ yield E.p("Voici quelques tables complètes:")
        for A in (ContractsPerUserAndContractType, CompaniesAndContracts,
                  ContractEndingsByType, StudyTypesAndContracts):
            yield E.h2(str(A.label))
            # if A.help_text:
            #     yield E.p(unicode(A.help_text))
            yield A

        yield E.h1(str(jobs.Contract._meta.verbose_name_plural))
        for A in (JobsContractsPerUserAndContractType,
                  JobProvidersAndContracts, JobsContractEndingsByType):
            yield E.h2(str(A.label))
            # if A.help_text:
            #     yield E.p(unicode(A.help_text))
            yield A
