# -*- coding: UTF-8 -*-
# Copyright 2015-2018 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)


"""Table definitions for `lino_welfare.modlib.immersion`.

"""
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _

from lino.api import dd

from lino_welfare.modlib.isip.mixins import ContractBaseTable

from lino_welfare.modlib.integ.roles import IntegUser, IntegrationStaff
from lino_welfare.modlib.pcsw.roles import SocialCoordinator


class Goals(dd.Table):
    """
    """
    required_roles = dd.login_required(IntegrationStaff)
    model = 'immersion.Goal'
    column_names = 'name *'
    detail_layout = """
    id name
    ContractsByGoal
    """


class ContractTypes(dd.Table):
    """The default table for :class:`ContractType` instances.
    """
    required_roles = dd.login_required(IntegrationStaff)
    model = 'immersion.ContractType'
    column_names = 'name exam_policy template *'
    detail_layout = """
    id name
    exam_policy template overlap_group
    full_name
    ContractsByType
    """
    insert_layout = """
    name
    exam_policy
    """


class ContractDetail(dd.DetailLayout):
    box1 = """
    id:8 client:25 user:15 language:8
    type goal company contact_person contact_role
    applies_from applies_until exam_policy
    # sector_function:30 remark:30 person_printed 
    sector function
    reference_person printed
    date_decided date_issued date_ended ending:20
    remark #responsibilities
    """

    right = """
    cal.EntriesByController
    cal.TasksByController
    """

    sector_function = """
    sector
    function
    """
    person_printed = """
    reference_person
    printed
    """

    main = """
    box1:70 right:30
    """


class Contracts(ContractBaseTable):

    required_roles = dd.login_required(IntegUser)
    model = 'immersion.Contract'
    column_names = 'id client company applies_from applies_until user type *'
    order_by = ['id']
    detail_layout = 'immersion.ContractDetail'
    insert_layout = """
    client
    company
    type goal
    """

    parameters = dict(
        type=dd.ForeignKey(
            'immersion.ContractType', blank=True,
            verbose_name=_("Only immersion trainings of type")),
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
    required_roles = dd.login_required((IntegUser, SocialCoordinator))
    master_key = 'client'
    auto_fit_column_widths = True
    column_names = ('applies_from '
                    'date_ended type goal company sector function '
                    'remark:20 *')


class ContractsByProvider(Contracts):
    master_key = 'company'
    column_names = 'client applies_from applies_until user type *'


class ContractsByPolicy(Contracts):
    master_key = 'exam_policy'


class ContractsByType(Contracts):
    master_key = 'type'
    column_names = "applies_from client user *"
    order_by = ["applies_from"]


class ContractsByGoal(Contracts):
    master_key = 'goal'
    column_names = "applies_from client user *"
    order_by = ["applies_from"]


class ContractsByEnding(Contracts):
    master_key = 'ending'



class MyContracts(Contracts):
    column_names = "applies_from client type company applies_until date_ended ending *"

    @classmethod
    def param_defaults(self, ar, **kw):
        kw = super(MyContracts, self).param_defaults(ar, **kw)
        kw.update(user=ar.get_user())
        return kw


