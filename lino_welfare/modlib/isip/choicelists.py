# -*- coding: UTF-8 -*-
# Copyright 2013-2017 Rumma & Ko Ltd
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


from lino.api import dd, _


class ContractEvents(dd.ChoiceList):
    verbose_name = _("Observed event")
    verbose_name_plural = _("Observed events")
add = ContractEvents.add_item
add('10', _("Active"), 'active')
add('20', _("Started"), 'started')
add('30', _("Ended"), 'ended')
add('40', _("Decided"), 'decided')
add('50', _("Issued"), 'issued')


class OverlapGroups(dd.ChoiceList):
    verbose_name = _("Overlap group")
    verbose_name_plural = _("Overlap groups")
add = OverlapGroups.add_item
add('10', _("Conventions"), 'contracts')
add('20', _("Trainings"), 'trainings')

