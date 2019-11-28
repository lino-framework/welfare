# -*- coding: UTF-8 -*-
# Copyright 2012-2016 Rumma & Ko Ltd
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

from lino import mixins
from lino.api import dd, _
from lino_xl.lib.notes.choicelists import SpecialTypes


class SequencedBudgetComponent(mixins.Sequenced):
    
    class Meta:
        abstract = True

    budget = dd.ForeignKey('debts.Budget')

    def get_siblings(self):
        "Overrides :meth:`lino.mixins.Sequenced.get_siblings`"
        return self.__class__.objects.filter(budget=self.budget)

    def get_row_permission(self, user, state, ba):
        if not self.budget.get_row_permission(user, state, ba):
            # print("20160531 veto for", ba)
            return False
        return super(
            SequencedBudgetComponent, self).get_row_permission(user, state, ba)



class ActorBase:
    """Base class for both the volatile :class:`MainActor` and the
    :class:`Actor <lino_welfare.modlib.debts.models.Actor>` model.


    """

    def get_first_meeting(self):
        obj = self.client
        if obj:
            return obj.get_first_meeting(self.budget.date)

    def get_first_meeting_text(self, *args):
        note = self.get_first_meeting(*args)
        if note is not None:
            return _("{meeting} on {date} with {user}").format(
                meeting=SpecialTypes.first_meeting.text,
                date=dd.fdl(note.date), user=note.user)

    @property
    def person(self):
        return self.partner.get_mti_child('person')

    @property
    def client(self):
        person = self.partner.get_mti_child('person')
        if person is not None:
            return person.get_mti_child('client')

    @property
    def household(self):
        return self.partner.get_mti_child('household')

    def __str__(self):
        return self.header


class MainActor(ActorBase):

    "A volatile object that represents the budget partner as actor"

    def __init__(self, budget, header):
        self.budget = budget
        self.header = header
        self.remark = ''
        if budget.partner_id:
            self.partner = budget.partner


