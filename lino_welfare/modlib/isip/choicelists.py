# -*- coding: UTF-8 -*-
# Copyright 2013-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""Choicelists for `lino_welfare.modlib.isip`.

"""

from lino.api import dd, _


class ContractEvents(dd.ChoiceList):
    verbose_name = _("Observed event")
    verbose_name_plural = _("Observed events")
add = ContractEvents.add_item
add('10', _("Started"), 'started')
add('20', _("Active"), 'active')
add('30', _("Ended"), 'ended')
add('40', _("Signed"), 'signed')


class OverlapGroups(dd.ChoiceList):
    """The list of all known overlap groups to be selected for the
    :attr:`overlap_group
    <lino_welfare.modlib.isip.mixins.ContractTypeBase.overlap_group>`
    of a contract type.

    """

    verbose_name = _("Overlap group")
    verbose_name_plural = _("Overlap groups")
add = OverlapGroups.add_item
add('10', _("Conventions"), 'contracts')
add('20', _("Trainings"), 'trainings')

