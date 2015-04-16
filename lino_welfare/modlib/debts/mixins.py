# -*- coding: UTF-8 -*-
# Copyright 2012-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""
Database models for `lino_welfare.modlib.debts`.

"""

from __future__ import unicode_literals


from django.db import models

from lino import mixins


class SequencedBudgetComponent(mixins.Sequenced):
    
    class Meta:
        abstract = True

    budget = models.ForeignKey('debts.Budget')

    def get_siblings(self):
        "Overrides :meth:`lino.mixins.Sequenced.get_siblings`"
        return self.__class__.objects.filter(
            budget=self.budget).order_by('seqno')

    def get_row_permission(self, user, state, ba):
        if not self.budget.get_row_permission(user, state, ba):
            return False
        return super(
            SequencedBudgetComponent, self).get_row_permission(user, state, ba)

