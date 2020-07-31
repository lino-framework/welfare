# -*- coding: UTF-8 -*-
# Copyright 2008-2018 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

"""Database models for `lino_welfare.modlib.isip`.

"""

from builtins import str

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from lino import mixins
from lino_xl.lib.cal.mixins import RecurrenceSet
from .choicelists import *
from .mixins import (ContractTypeBase,
                     ContractPartnerBase, ContractBase,
                     ContractBaseTable)

config = dd.plugins.isip

from lino_xl.lib.coachings.utils import has_contracts_filter
from lino_xl.lib.clients.choicelists import ClientEvents, ObservedEvent

from lino_welfare.modlib.pcsw.roles import SocialStaff, SocialUser
from lino_welfare.modlib.integ.roles import IntegUser
from lino_welfare.modlib.pcsw.roles import SocialCoordinator


class ClientHasContract(ObservedEvent):
    text = config.verbose_name

    def add_filter(self, qs, pv):
        period = (pv.start_date, pv.end_date)
        flt = has_contracts_filter('isip_contract_set_by_client', period)
        qs = qs.filter(flt).distinct()
        return qs

ClientEvents.add_item_instance(ClientHasContract("isip"))


COACHINGTYPE_ASD = 1
COACHINGTYPE_DSBE = 2


class ContractType(ContractTypeBase):
    preferred_foreignkey_width = 20

    templates_group = 'isip/Contract'

    class Meta:
        app_label = 'isip'
        verbose_name = _("ISIP Type")
        verbose_name_plural = _('ISIP Types')

    ref = models.CharField(_("Reference"), max_length=20, blank=True)
    needs_study_type = models.BooleanField(
        _("needs Study type"), default=False)


class ContractTypes(dd.Table):
    required_roles = dd.login_required(SocialStaff)
    model = 'isip.ContractType'
    column_names = 'name ref exam_policy needs_study_type *'
    detail_layout = """
    id ref exam_policy overlap_group needs_study_type
    name
    full_name
    ContractsByType
    """


#
# EXAMINATION POLICIES
#
class ExamPolicy(mixins.BabelNamed, RecurrenceSet):
    class Meta:
        app_label = 'isip'
        verbose_name = _("Examination Policy")
        verbose_name_plural = _('Examination Policies')

    # hidden_columns = 'start_date start_time end_date end_time'
    event_type = dd.ForeignKey(
        'cal.EventType', null=True, blank=True,
        help_text=_("""Generated events will receive this type."""))


class ExamPolicies(dd.Table):
    required_roles = dd.login_required(SocialStaff)
    model = 'isip.ExamPolicy'
    column_names = 'name *'
    detail_layout = """
    id name
    # summary start_date end_date
    # description
    max_events every every_unit event_type
    monday tuesday wednesday thursday friday saturday sunday
    isip.ContractsByPolicy
    jobs.ContractsByPolicy
    """


JOBS_MODULE_NAME = settings.SITE.plugins.jobs.verbose_name



class ContractEnding(dd.Model):
    class Meta:
        app_label = 'isip'
        verbose_name = _("Reason of termination")
        verbose_name_plural = _('Contract termination reasons')

    name = models.CharField(_("Designation"), max_length=200)
    use_in_isip = models.BooleanField(config.verbose_name, default=True)
    use_in_jobs = models.BooleanField(JOBS_MODULE_NAME, default=True)
    is_success = models.BooleanField(_("Success"), default=False)
    needs_date_ended = models.BooleanField(
        _("Require date ended"), default=False)

    def __str__(self):
        return str(self.name)


class ContractEndings(dd.Table):
    required_roles = dd.login_required(SocialStaff)
    model = 'isip.ContractEnding'
    column_names = 'name use_in_isip use_in_jobs is_success needs_date_ended *'
    order_by = ['name']
    detail_layout = """
    name
    use_in_isip use_in_jobs is_success needs_date_ended
    isip.ContractsByEnding
    jobs.ContractsByEnding
    """


class ContractPartner(ContractPartnerBase):

    class Meta:
        app_label = 'isip'
        verbose_name = _("Contract partner")
        verbose_name_plural = _("Contract partners")

    allow_cascaded_delete = ['contract']

    contract = dd.ForeignKey('isip.Contract')

    duties_company = dd.RichTextField(
        _("duties company"),
        blank=True, null=True, format='html')


class ContractPartners(dd.Table):
    required_roles = dd.login_required(SocialStaff)
    model = 'isip.ContractPartner'
    columns = 'contract company contact_person contact_role'
    detail_layout = """
    company contact_person contact_role
    duties_company
    """
    insert_layout = """
    company 
    contact_person
    contact_role
    """


class PartnersByContract(ContractPartners):
    required_roles = dd.login_required(SocialUser)
    master_key = 'contract'
    columns = 'company contact_person contact_role duties_company'


class Contract(ContractBase):
    class Meta:
        app_label = 'isip'
        verbose_name = _("ISIP")
        verbose_name_plural = _("ISIPs")

    type = dd.ForeignKey(
        "isip.ContractType",
        related_name="%(app_label)s_%(class)s_set_by_type",
        verbose_name=_("Contract Type"), blank=True)

    study_type = dd.ForeignKey('cv.StudyType', blank=True, null=True)

    stages = dd.RichTextField(
        _("stages"),
        blank=True, null=True, format='html')
    goals = dd.RichTextField(
        _("goals"),
        blank=True, null=True, format='html')
    duties_asd = dd.RichTextField(
        _("duties ASD"),
        blank=True, null=True, format='html')
    duties_dsbe = dd.RichTextField(
        _("duties DSBE"),
        blank=True, null=True, format='html')
    duties_pcsw = dd.RichTextField(
        _("duties PCSW"),
        blank=True, null=True, format='html')
    duties_person = dd.RichTextField(
        _("duties person"),
        blank=True, null=True, format='html')

    user_dsbe = dd.ForeignKey(
        "users.User",
        verbose_name=_("responsible (IS)"),
        related_name="%(app_label)s_%(class)s_set_by_user_dsbe",
        blank=True, null=True)

    def before_dumpy_save(self, loader=None):
        # removes the need of writing a custom database migrator
        if loader and loader.source_version == '2017.1.0':
            if self.user_dsbe is None:
                self.user_dsbe = self.user 

    @classmethod
    def get_certifiable_fields(cls):
        return """client type
        applies_from applies_until
        language
        stages goals duties_dsbe
        duties_asd duties_pcsw duties_person 
        user user_asd user_dsbe exam_policy
        date_decided date_issued"""

    def before_printable_build(self, bm):
        super(Contract, self).before_printable_build(bm)
        if not self.duties_pcsw and not self.get_aid_confirmation():
            raise Warning(
                _("Cannot print {} because there is no active "
                  "aid confirmation and Duties (PCSW) is empty.").format(self))

# dd.update_field(
#     Contract, 'user',
#     verbose_name=_("Integration agent"))


class ContractDetail(dd.DetailLayout):
    general = dd.Panel("""
    id:8 client:25 type user:15 user_dsbe:15 user_asd:15
    study_type applies_from applies_until exam_policy language:8
    date_decided date_issued printed date_ended ending:20
    PartnersByContract
    cal.TasksByController cal.EntriesByController
    """, label=_("General"))

    isip = dd.Panel("""
    stages  goals duties_person
    duties_asd duties_dsbe duties_pcsw
    """, label=_("ISIP"))

    main = "general isip"

    #~ def setup_handle(self,dh):
        #~ dh.general.label = _("General")
        #~ dh.isip.label = _("ISIP")


class Contracts(ContractBaseTable):
    required_roles = dd.login_required(SocialUser)
    model = 'isip.Contract'
    column_names = 'id applies_from date_ended client user type *'
    order_by = ['id']
    detail_layout = ContractDetail()
    insert_layout = dd.InsertLayout("""
    client
    type
    """, window_size=(60, 'auto'))

    parameters = dict(
        type=dd.ForeignKey(ContractType, blank=True),
        study_type=dd.ForeignKey('cv.StudyType', blank=True),
        **ContractBaseTable.parameters)

    params_layout = """
    user type start_date end_date observed_event
    company:20 study_type:15 ending_success:20 ending
    """

    @classmethod
    def get_request_queryset(cls, ar):
        #~ logger.info("20120608.get_request_queryset param_values = %r",ar.param_values)
        qs = super(Contracts, cls).get_request_queryset(ar)
        pv = ar.param_values
        if pv.company:
            qs = qs.filter(contractpartner__company=pv.company)
        if pv.study_type:
            qs = qs.filter(study_type=pv.study_type)
        return qs

    @classmethod
    def get_title_tags(self, ar):
        for t in super(Contracts, self).get_title_tags(ar):
            yield t

        if ar.param_values.study_type:
            yield str(ar.param_values.study_type)


class MyContracts(Contracts):

    required_roles = dd.login_required(IntegUser)
    
    @classmethod
    def param_defaults(self, ar, **kw):
        kw = super(MyContracts, self).param_defaults(ar, **kw)
        kw.update(user=ar.get_user())
        return kw


class ContractsByClient(Contracts):
    required_roles = dd.login_required((IntegUser, SocialCoordinator))
    master_key = 'client'
    column_names = ('applies_from applies_until type '
                    'user study_type date_ended ending *')


class ContractsByPolicy(Contracts):
    master_key = 'exam_policy'


class ContractsByType(Contracts):
    master_key = 'type'
    column_names = "applies_from client user id applies_until *"
    order_by = ["applies_from"]


class ContractsByEnding(Contracts):
    master_key = 'ending'


class ContractsByStudyType(Contracts):
    master_key = 'study_type'


class DelegatedTasksByContract(dd.Table):
    model = "cal.Task"
    master_key = "owner"
    column_names = "summary due_date"
    filter = models.Q(delegated=True)

    @classmethod
    def override_column_headers(self, ar, **kwargs):
        kwargs.update(summary=str(_("Proceedings")))
        return kwargs


class EntriesByContract(dd.Table):
    model = "cal.Event"
    master_key = "owner"
    column_names = "summary start_date"

    @classmethod
    def override_column_headers(self, ar, **kwargs):
        kwargs.update(start_date=_("Date"))
        return kwargs

# from lino_xl.lib.uploads.models import UploadsByProject

# class UploadsByContract(UploadsByProject):
#     @classmethod
#     def create_instance(self, ar, **kw):
#         obj = super(UploadsByContract, self).create_instance(ar, **kw)
#         obj.owner = obj.project
#         return obj


@dd.receiver(dd.post_analyze)
def customize_cv(sender, **kw):
    site = sender

    site.modules.cv.StudyTypes.set_detail_layout("""
    name id
    education_level is_study is_training
    cv.StudiesByType
    cv.TrainingsByType
    isip.ContractsByStudyType
    """)

# def site_setup(site):
#     site.modules.cv.StudyTypes.set_detail_layout("""
#     name education_level id
#     isip.ContractsByStudyType
#     cv.StudiesByType
#     """)
