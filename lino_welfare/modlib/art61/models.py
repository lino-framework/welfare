# -*- coding: UTF-8 -*-
# Copyright 2015 Luc Saffre
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


"""Database models for the `lino_welfare.modlib.art61`.


"""
from __future__ import unicode_literals

import logging
logger = logging.getLogger(__name__)

from django.db import models
from django.utils.translation import ugettext_lazy as _

from lino.api import dd
from lino import mixins

from lino_welfare.modlib.integ.roles import IntegrationAgent, IntegrationStaff

from lino_welfare.modlib.isip.mixins import (ContractBaseTable,
                                             ContractTypeBase)
from lino_welfare.modlib.jobs.mixins import JobSupplyment

from .choicelists import Subsidizations

from lino_welfare.modlib.pcsw.choicelists import (
    ClientEvents, ObservedEvent, has_contracts_filter)


class ClientHasContract(ObservedEvent):
    text = _("Art61 job supplyment")

    def add_filter(self, qs, pv):
        period = (pv.start_date, pv.end_date)
        flt = has_contracts_filter('art61_contract_set_by_client', period)
        qs = qs.filter(flt).distinct()
        return qs

ClientEvents.add_item_instance(ClientHasContract("art61"))


class ContractType(ContractTypeBase, mixins.Referrable):

    """This is the homologue of :class:`isip.ContractType
    <lino_welfare.modlib.isip.models.ContractType>` (see there for
    general documentation).
    
    The demo database comes with these contract types:

    .. django2rst::

        rt.show('art61.ContractTypes')

    """

    preferred_foreignkey_width = 20

    templates_group = 'art61/Contract'

    class Meta:
        verbose_name = _("Art61 job supplyment type")
        verbose_name_plural = _('Art61 job supplyment types')
        ordering = ['name']


class ContractTypes(dd.Table):
    """
    """
    required_roles = dd.required(IntegrationStaff)
    model = ContractType
    column_names = 'name ref *'
    detail_layout = """
    id name ref
    ContractsByType
    """


class Contract(JobSupplyment):

    """An "Art61 job supplyment" is an agreement between the PCSW and a
    private company...

    """

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
        """Yield a list of all subsidizations activated for this contract.
        """
        for sub in Subsidizations.items():
            if getattr(self, sub.contract_field_name()):
                yield sub

    def get_excerpt_options(self, ar, **kw):
        """Implements :meth:`lino.core.model.Model.get_excerpt_options`.

        When printing a contract, there is no recipient.

        """
        kw = super(Contract, self).get_excerpt_options(ar, **kw)
        del kw['company']
        del kw['contact_person']
        del kw['contact_role']
        return kw

dd.update_field(Contract, 'user', verbose_name=_("responsible (IS)"))
dd.update_field(Contract, 'company', blank=False, null=False)


class ContractDetail(dd.FormLayout):
    box1 = """
    id:8 client:25 user:15 language:8
    type company contact_person contact_role
    applies_from duration applies_until exam_policy
    job_title status cv_duration regime
    reference_person printed
    date_decided date_issued date_ended ending:20
    subsidize_10 subsidize_20 subsidize_30
    # signer1 signer2
    responsibilities
    """

    right = """
    cal.EventsByController
    cal.TasksByController
    """

    main = """
    box1:70 right:30
    """


class Contracts(ContractBaseTable):
    #~ debug_permissions = "20130222"
    required_roles = dd.required(IntegrationAgent)
    model = Contract
    column_names = 'id applies_from applies_until user type *'
    order_by = ['id']
    detail_layout = ContractDetail()
    insert_layout = """
    client
    company
    type
    """

    parameters = dict(
        type=models.ForeignKey(
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
    """
    """
    master_key = 'client'
    auto_fit_column_widths = True
    column_names = ('applies_from applies_until duration type '
                    'company contact_person user remark:20 *')


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
