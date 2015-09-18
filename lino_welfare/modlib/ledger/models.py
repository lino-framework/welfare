# -*- coding: UTF-8 -*-
# Copyright 2015 Luc Saffre
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
Database models for :mod:`lino_welfare.modlib.ledger`.
"""

from __future__ import unicode_literals

from lino.modlib.ledger.models import *
from lino.api import _
from lino.modlib.accounts.utils import DEBIT
from lino.modlib.ledger.choicelists import TradeTypes

JournalGroups.clear()
add = JournalGroups.add_item
add('10', _("Purchases"), 'purchases')
add('20', _("Aids"), 'aids')
add('40', _("Financial"), 'financial')


TradeTypes.clear()
add = TradeTypes.add_item
add('P', _("Purchases"), 'purchases', dc=DEBIT)
add('A', _("Aids"), 'aids', dc=DEBIT)
add('C', _("Clearings"), 'clearings', dc=DEBIT)

TradeTypes.aids.update(
    partner_account_field_name='aids_account',
    partner_account_field_label=_("Aids account"))


