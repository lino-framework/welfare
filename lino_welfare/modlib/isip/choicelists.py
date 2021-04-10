# -*- coding: UTF-8 -*-
# Copyright 2013-2021 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)


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
