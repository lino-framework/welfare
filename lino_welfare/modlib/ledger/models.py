# -*- coding: UTF-8 -*-
# Copyright 2015 Luc Saffre
# License: BSD (see file COPYING for details)

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


