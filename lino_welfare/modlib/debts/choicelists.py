# -*- coding: UTF-8 -*-
# Copyright 2012-2015 Luc Saffre
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

"""
Database models for `lino_welfare.modlib.debts`.

"""

from __future__ import unicode_literals

from django.db import models

from lino.api import dd, _


class TableLayout(dd.Choice):
    columns_spec = None

    def __init__(self, value, verbose_name, columns_spec):
        self.columns_spec = columns_spec
        super(TableLayout, self).__init__(value, verbose_name, None)


class TableLayouts(dd.ChoiceList):
    item_class = TableLayout
    verbose_name = _("Table layout")
    verbose_name_plural = _("Table layouts")
    column_names = 'value text columns_spec'

    @dd.virtualfield(models.CharField(_("Columns"), max_length=20))
    def columns_spec(cls, choice, ar):
        return choice.columns_spec

add = TableLayouts.add_item
add('10',  # used by PrintExpensesByBudget
    _("Description, remarks, yearly amount, actor amounts"),
    "description remarks yearly_amount:12 dynamic_amounts")

add('11',
    _("Description, remarks, actor amounts"),
    "description remarks dynamic_amounts")

add('20',  # used by PrintLiabilitiesByBudget
    _("Partner, remarks, monthly rate, actor amounts"),
    "partner:20 remarks:20 monthly_rate dynamic_amounts")

add('30',  # used by PrintAssetsByBudget, PrintIncomesByBudget
    _("Full description, actor amounts"),
    "full_description dynamic_amounts")

add('40',  # used by Inkasso-Unternehmen and Gerichtsvollzieher
    _("Debt-collector, partner, remarks, monthly rate, amounts"),
    "bailiff:20 partner:20 remarks:20 monthly_rate dynamic_amounts")

# add('I', '10',  # used by PrintAssetsByBudget, PrintIncomesByBudget
#     _("Full description, actor amounts"),
#     "full_description dynamic_amounts")

