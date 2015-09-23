# -*- coding: UTF-8 -*-
# Copyright 2008-2015 Luc Saffre
# This file is part of Lino Welfare.
#
# Lino Welfare is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# Lino Welfare is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License along with Lino Welfare.  If not, see
# <http://www.gnu.org/licenses/>.

"""Database models for `lino_welfare.modlib.isip`.

"""

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from lino.api import dd
from lino import mixins

from lino.modlib.cal.mixins import RecurrenceSet

from .mixins import (ContractEvents, ContractTypeBase,
                     ContractPartnerBase, ContractBase,
                     ContractBaseTable)

config = dd.plugins.isip

from lino_welfare.modlib.pcsw.choicelists import (
    ClientEvents, ObservedEvent, has_contracts_filter)

from lino_welfare.modlib.pcsw.roles import SocialStaff
from lino_welfare.modlib.integ.roles import IntegrationAgent, IntegrationStaff


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
    """The type of an :class:`isip.Contract <Class>`.

    .. attribute:: needs_study_type

        Whether contracts of this type need their :attr:`study_type`
        field filled in.

    """
    preferred_foreignkey_width = 20

    templates_group = 'isip/Contract'

    class Meta:
        verbose_name = _("ISIP Type")
        verbose_name_plural = _('ISIP Types')

    ref = models.CharField(_("Reference"), max_length=20, blank=True)
    needs_study_type = models.BooleanField(
        _("needs Study type"), default=False)


class ContractTypes(dd.Table):
    required_roles = dd.required(SocialStaff)
    model = 'isip.ContractType'
    column_names = 'name ref exam_policy needs_study_type *'
    detail_layout = """
    id ref exam_policy needs_study_type
    name
    full_name
    ContractsByType
    """


#
# EXAMINATION POLICIES
#
class ExamPolicy(mixins.BabelNamed, RecurrenceSet):
    """An **examination policy** is mostly a :class:`RecurrenceSet
    <lino.modlib.cal.mixins.RecurrenceSet>` used for generating
    "evaluation meetings".  That is, Lino automatically suggests dates
    where the agent invites the client.

    TODO: move this to :mod:`lino_welfare.modlib.integ.modules`.

    """
    class Meta:
        verbose_name = _("Examination Policy")
        verbose_name_plural = _('Examination Policies')

    # hidden_columns = 'start_date start_time end_date end_time'
    event_type = dd.ForeignKey(
        'cal.EventType', null=True, blank=True,
        help_text=_("""Generated events will receive this type."""))


class ExamPolicies(dd.Table):
    required_roles = dd.required(SocialStaff)
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
    """A possible reason for premature termination of a contract.

    TODO: move this to :mod:`lino_welfare.modlib.integ.modules`.

    """
    class Meta:
        verbose_name = _("Reason of termination")
        verbose_name_plural = _('Contract termination reasons')

    name = models.CharField(_("designation"), max_length=200)
    use_in_isip = models.BooleanField(config.verbose_name, default=True)
    use_in_jobs = models.BooleanField(JOBS_MODULE_NAME, default=True)
    is_success = models.BooleanField(_("Success"), default=False)
    needs_date_ended = models.BooleanField(
        _("Require date ended"), default=False)

    def __unicode__(self):
        return unicode(self.name)


class ContractEndings(dd.Table):
    required_roles = dd.required(SocialStaff)
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
        verbose_name = _("Contract partner")
        verbose_name_plural = _("Contract partners")

    contract = dd.ForeignKey('isip.Contract')

    duties_company = dd.RichTextField(
        _("duties company"),
        blank=True, null=True, format='html')


class ContractPartners(dd.Table):
    required_roles = dd.login_required(IntegrationStaff)
    model = 'isip.ContractPartner'
    columns = 'contract company contact_person contact_role'
    detail_layout = """
    company contact_person contact_role
    duties_company
    """


class PartnersByContract(ContractPartners):
    required_roles = dd.login_required(IntegrationAgent)
    master_key = 'contract'
    columns = 'company contact_person contact_role duties_company'


class Contract(ContractBase):
    """An **ISIP** (called "PIIS" in French and "VSE" in German) is a
    convention or contract between the PCSW and a young client that
    leads to an individual coaching of the person, mostly concerning
    the client's scholar education.

    .. attribute:: type

        The type of this contract.
        Pointer to :class:`ContractType`.

    .. attribute:: study_type

        The type of study that is going to be followed during this
        contract.

        Pointer to :class:`lino.modlib.cv.models.StudyType`.

    """
    class Meta:
        verbose_name = _("ISIP")
        verbose_name_plural = _("ISIPs")

    type = models.ForeignKey(
        "isip.ContractType",
        related_name="%(app_label)s_%(class)s_set_by_type",
        verbose_name=_("Contract Type"), blank=True)

    study_type = models.ForeignKey('cv.StudyType', blank=True, null=True)

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
    duties_person = dd.RichTextField(
        _("duties person"),
        blank=True, null=True, format='html')

    @classmethod
    def get_certifiable_fields(cls):
        return """client type
        applies_from applies_until
        language
        stages goals duties_dsbe
        duties_asd duties_person
        user user_asd exam_policy
        date_decided date_issued"""


dd.update_field(
    Contract, 'user',
    verbose_name=_("Integration agent"))


class ContractDetail(dd.FormLayout):
    general = dd.Panel("""
    id:8 client:25 type user:15 user_asd:15
    study_type applies_from applies_until exam_policy language:8
    date_decided date_issued printed date_ended ending:20
    PartnersByContract
    cal.TasksByController cal.EventsByController
    """, label=_("General"))

    isip = dd.Panel("""
    stages  goals
    duties_asd  duties_dsbe  duties_person
    """, label=_("ISIP"))

    main = "general isip"

    #~ def setup_handle(self,dh):
        #~ dh.general.label = _("General")
        #~ dh.isip.label = _("ISIP")


class Contracts(ContractBaseTable):
    required_roles = dd.login_required(IntegrationAgent)
    model = 'isip.Contract'
    column_names = 'id applies_from applies_until client user type *'
    order_by = ['id']
    detail_layout = ContractDetail()
    insert_layout = dd.FormLayout("""
    client
    type
    """, window_size=(60, 'auto'))

    parameters = dict(
        type=models.ForeignKey(ContractType, blank=True),
        study_type=models.ForeignKey('cv.StudyType', blank=True),
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
            yield unicode(ar.param_values.study_type)


class MyContracts(Contracts):

    @classmethod
    def param_defaults(self, ar, **kw):
        kw = super(MyContracts, self).param_defaults(ar, **kw)
        kw.update(user=ar.get_user())
        return kw


class ContractsByClient(Contracts):
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
        kwargs.update(summary=unicode(_("Proceedings")))
        return kwargs


class EventsByContract(dd.Table):
    model = "cal.Event"
    master_key = "owner"
    column_names = "summary start_date"

    @classmethod
    def override_column_headers(self, ar, **kwargs):
        kwargs.update(start_date=_("Date"))
        return kwargs


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
