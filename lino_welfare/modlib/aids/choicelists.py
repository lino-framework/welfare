# -*- coding: UTF-8 -*-
# Copyright 2014-2015 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
"""
Choicelists for `lino_welfare.modlib.aids`.

.. autosummary::


"""

from __future__ import unicode_literals

import logging
logger = logging.getLogger(__name__)

from django.db import models
from django.utils.text import format_lazy

from lino.api import dd, rt, _


class ConfirmationType(dd.Choice):

    def __init__(self, model, table_class):
        self.table_class = table_class
        model = dd.resolve_model(model)
        self.model = model
        value = dd.full_model_name(model)
        # text = model._meta.verbose_name + ' (%s)' % dd.full_model_name(model)
        text = format_lazy(u"{} ({})",model._meta.verbose_name,value)
        name = None
        super(ConfirmationType, self).__init__(value, text, name)

    def get_aidtypes(self):
        return rt.models.aids.AidType.objects.filter(confirmation_type=self)


class ConfirmationTypes(dd.ChoiceList):
    """A list of the models that may be used as confirmation.

    .. attribute:: et_template

        The `template` defined for the `ExcerptType` defined for this
        confirmation type.

    """
    item_class = ConfirmationType
    max_length = 100
    verbose_name = _("Aid confirmation type")
    verbose_name_plural = _("Aid confirmation types")

    @classmethod
    def get_column_names(self, ar):
        return 'name value text et_template *'

    @dd.virtualfield(models.CharField(_("Template"), max_length=20))
    def et_template(cls, choice, ar):
        et = rt.models.excerpts.ExcerptType.get_for_model(choice.model)
        if et:
            return et.template

    @classmethod
    def get_for_model(self, model):
        for o in self.objects():
            if o.model is model:
                return o

    @classmethod
    def add_item(cls, model, table_class):
        return cls.add_item_instance(ConfirmationType(model, table_class))


class AidRegimes(dd.ChoiceList):
    verbose_name = _("Aid Regime")
add = AidRegimes.add_item
add('10', _("Financial aids"), 'financial')
add('20', _("Medical aids"), 'medical')
add('30', _("Other aids"), 'other')


class ConfirmationStates(dd.Workflow):
    verbose_name_plural = _("Aid confirmation states")

add = ConfirmationStates.add_item
add('01', _("Unconfirmed"), 'requested')
add('02', _("Confirmed"), 'confirmed')
# add('03', _("Cancelled"), 'cancelled')


