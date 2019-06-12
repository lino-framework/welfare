# -*- coding: UTF-8 -*-
# Copyright 2015-2018 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)


from __future__ import unicode_literals

import logging

logger = logging.getLogger(__name__)

from django.db import models
from django.utils.translation import ugettext_lazy as _

from lino.api import dd
from lino import mixins

from lino_welfare.modlib.integ.roles import IntegUser, IntegrationStaff

from lino_welfare.modlib.isip.mixins import (ContractBaseTable,
                                             ContractTypeBase)
from lino_welfare.modlib.jobs.mixins import JobSupplyment

from .choicelists import Subsidizations

from lino_xl.lib.coachings.utils import has_contracts_filter
from lino_xl.lib.clients.choicelists import ClientEvents, ObservedEvent
from lino_welfare.modlib.pcsw.roles import SocialCoordinator


class ClientHasContract(ObservedEvent):
    text = _("Art61 job supplyment")

    def add_filter(self, qs, pv):
        period = (pv.start_date, pv.end_date)
        flt = has_contracts_filter('art61_contract_set_by_client', period)
        qs = qs.filter(flt).distinct()
        return qs

ClientEvents.add_item_instance(ClientHasContract("art61"))


class ContractType(ContractTypeBase, mixins.Referrable):

    preferred_foreignkey_width = 20

    templates_group = 'art61/Contract'

    class Meta:
        verbose_name = _("Art61 job supplyment type")
        verbose_name_plural = _('Art61 job supplyment types')
        ordering = ['name']


class ContractTypes(dd.Table):
    required_roles = dd.login_required(IntegrationStaff)
    model = ContractType
    column_names = 'name ref *'
    detail_layout = """
    id name ref overlap_group:20
    ContractsByType
    """


class Contract(JobSupplyment):

    class Meta:
        verbose_name = _("Art61 job supplyment")
        verbose_name_plural = _('Art61 job supplyments')

    type = dd.ForeignKey(
        "art61.ContractType",
        verbose_name=_("Type"),
        related_name="%(app_label)s_%(class)s_set_by_type")

    # The following four fields are the same as in `cv.Experience`
    # except that `duration` is `cv_duration` because we have already
    # another field `duration` (number of days) from `JobSupplyment`
    job_title = models.CharField(
        max_length=200, verbose_name=_("Job title"), blank=True)
    status = dd.ForeignKey('cv.Status', blank=True, null=True)
    cv_duration = dd.ForeignKey('cv.Duration', blank=True, null=True)
    regime = dd.ForeignKey(
        'cv.Regime', blank=True, null=True,
        related_name="art61_contracts")

    @classmethod
    def get_certifiable_fields(cls):
        return (
            'client type company contact_person contact_role '
            'applies_from applies_until duration '
            'language job_title status cv_duration regime '
            'reference_person responsibilities '
            'user user_asd exam_policy '
            'date_decided date_issued ')

    def get_subsidizations(self):
        for sub in Subsidizations.items():
            if getattr(self, sub.contract_field_name()):
                yield sub

    def get_excerpt_options(self, ar, **kw):
        # Implements :meth:`lino.printing.Printable.get_excerpt_options`.

        # When printing a contract, there is no recipient.

        kw = super(Contract, self).get_excerpt_options(ar, **kw)
        del kw['company']
        del kw['contact_person']
        del kw['contact_role']
        return kw

# dd.update_field(Contract, 'user', verbose_name=_("responsible (IS)"))
dd.update_field(Contract, 'company', blank=False, null=False)


class ContractDetail(dd.DetailLayout):
    box1 = """
    id:8 client:25 user:15 language:8
    type company contact_person contact_role
    applies_from duration applies_until exam_policy
    job_title status cv_duration regime
    reference_person remark printed
    date_decided date_issued date_ended ending:20
    subsidize_10 subsidize_20 subsidize_30 subsidize_40 subsidize_50
    # signer1 signer2
    responsibilities
    """

    right = """
    cal.EntriesByController
    cal.TasksByController
    """

    main = """
    box1:70 right:30
    """


class Contracts(ContractBaseTable):
    #~ debug_permissions = "20130222"
    required_roles = dd.login_required(IntegUser)
    model = 'art61.Contract'
    column_names = 'id client client__national_id ' \
                   'applies_from date_ended user type *'
    order_by = ['id']
    detail_layout = ContractDetail()
    insert_layout = """
    client
    company
    type
    """

    parameters = dict(
        type=dd.ForeignKey(
            'art61.ContractType', blank=True,
            verbose_name=_("Only job supplies of type")),
        **ContractBaseTable.parameters)

    params_layout = """
    user type start_date end_date observed_event
    company ending_success ending
    """

    @classmethod
    def get_request_queryset(cls, ar):
        qs = super(Contracts, cls).get_request_queryset(ar)
        pv = ar.param_values
        if pv.company:
            qs = qs.filter(company=pv.company)
        return qs


class ContractsByClient(Contracts):
    required_roles = dd.login_required((IntegUser, SocialCoordinator))
    label = _("Art61 job supplyments and activations")
    master_key = 'client'
    auto_fit_column_widths = True
    column_names = 'applies_from applies_until date_ended duration type '\
                   'company contact_person user remark:20 '\
                   'subsidize_10 subsidize_20 subsidize_30 subsidize_40 subsidize_50 *'


class ContractsByProvider(Contracts):
    master_key = 'company'
    column_names = 'client applies_from applies_until user type *'


class ContractsByPolicy(Contracts):
    master_key = 'exam_policy'


class ContractsByType(Contracts):
    master_key = 'type'
    column_names = "applies_from client user *"
    order_by = ["applies_from"]


class ContractsByEnding(Contracts):
    master_key = 'ending'


class MyContracts(Contracts):
    column_names = ("applies_from client type company applies_until "
                    "date_ended ending *")

    @classmethod
    def param_defaults(self, ar, **kw):
        kw = super(MyContracts, self).param_defaults(ar, **kw)
        kw.update(user=ar.get_user())
        return kw


@dd.receiver(dd.pre_analyze)
def inject_subsidization_fields(sender, **kw):
    for sub in Subsidizations.items():
        dd.inject_field(
            'art61.Contract', sub.contract_field_name(),
            models.BooleanField(verbose_name=sub.text, default=False))
