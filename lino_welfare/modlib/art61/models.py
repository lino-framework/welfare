# -*- coding: UTF-8 -*-
# Copyright 2015 Luc Saffre
# License: BSD (see file COPYING for details)


"""The :xfile:`models.py` module for the
:mod:`lino_welfare.modlib.art61` app.


"""
from __future__ import unicode_literals

import logging
logger = logging.getLogger(__name__)

from django.db import models
from django.utils.translation import ugettext_lazy as _

from lino.api import dd
from lino import mixins

from lino_welfare.modlib.isip.mixins import (ContractBaseTable,
                                             ContractTypeBase)

from lino_welfare.modlib.jobs.mixins import JobSupplyment


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
    required = dd.required(user_groups='integ', user_level='manager')
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
        related_name="%(app_label)s_%(class)s_set_by_type")

    @classmethod
    def get_certifiable_fields(cls):
        return (
            'client company contact_person contact_role type '
            'applies_from applies_until duration '
            'language  '
            'reference_person responsibilities '
            'user user_asd exam_policy '
            'date_decided date_issued ')


dd.update_field(Contract, 'user', verbose_name=_("responsible (IS)"))
dd.update_field(Contract, 'company', blank=False, null=False)


class ContractDetail(dd.FormLayout):
    box1 = """
    id:8 client:25 user:15 user_asd:15 language:8
    type company contact_person contact_role
    applies_from duration applies_until exam_policy
    reference_person printed
    date_decided date_issued date_ended ending:20
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
    required = dd.required(user_groups='integ')
    #~ required_user_groups = ['integ']
    #~ required_user_level = UserLevels.manager
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
    column_names = 'applies_from applies_until user type *'


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

