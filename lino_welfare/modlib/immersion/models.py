# -*- coding: UTF-8 -*-
# Copyright 2015-2017 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)


"""Database models for `lino_welfare.modlib.immersion`.

"""
from __future__ import unicode_literals

import logging
logger = logging.getLogger(__name__)

from django.db import models
from django.utils.translation import ugettext_lazy as _

from lino.api import dd
from lino import mixins

from lino_xl.lib.cv.mixins import SectorFunction
from lino_welfare.modlib.isip.mixins import (
    ContractTypeBase, ContractBase, ContractPartnerBase)

from lino_xl.lib.clients.choicelists import ClientEvents, ObservedEvent
from lino_xl.lib.coachings.utils import has_contracts_filter


class ClientHasContract(ObservedEvent):
    text = _("Immersion training")

    def add_filter(self, qs, pv):
        period = (pv.start_date, pv.end_date)
        flt = has_contracts_filter('immersion_contract_set_by_client', period)
        qs = qs.filter(flt).distinct()
        return qs

ClientEvents.add_item_instance(ClientHasContract("immersion"))


class ContractType(ContractTypeBase):
    """Every *immersion training* has a mandatory field
    :attr:`Contract.type` which points to this.  The **immersion
    training type** defines certain properties of the immersion
    trainings that use it.

    .. attribute:: name

        Translatable description.

    .. attribute:: template

        See :attr:`lino_welfare.modlib.isip.mixins.ContractTypeBase.template`

    """

    templates_group = 'immersion/Contract'

    class Meta:
        app_label = 'immersion'
        verbose_name = _("Immersion training type")
        verbose_name_plural = _('Immersion training types')
        ordering = ['name']


class Goal(mixins.BabelNamed):

    preferred_foreignkey_width = 20

    class Meta:
        app_label = 'immersion'
        verbose_name = _("Immersion training goal")
        verbose_name_plural = _('Immersion training goals')
        ordering = ['name']


class Contract(ContractBase, ContractPartnerBase, SectorFunction):
    """An immersion training.

    """

    class Meta:
        app_label = 'immersion'
        verbose_name = _("Immersion training")
        verbose_name_plural = _('Immersion trainings')

    type = dd.ForeignKey(
        "immersion.ContractType",
        related_name="%(app_label)s_%(class)s_set_by_type")

    goal = dd.ForeignKey("immersion.Goal", related_name="trainings")

    reference_person = models.CharField(
        _("reference person"), max_length=200, blank=True)
    responsibilities = dd.RichTextField(
        _("responsibilities"), blank=True, null=True, format='html')
    remark = models.TextField(_("Remark"), blank=True)

    # @dd.chooser()
    # def company_choices(cls):
    #     return rt.models.jobs.JobProvider.objects.all()

    @classmethod
    def get_certifiable_fields(cls):
        return (
            'client company contact_person contact_role type '
            'applies_from applies_until '
            'language  '
            'reference_person responsibilities '
            'user user_asd exam_policy '
            'date_decided date_issued ')


dd.update_field(Contract, 'user', verbose_name=_("responsible (IS)"))
dd.update_field(Contract, 'company', blank=False, null=False)


from .ui import *
