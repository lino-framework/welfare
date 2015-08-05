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

add = JournalGroups.add_item
add('50', _("Aids"), 'aids')

TradeTypes.add_item('A', _("Aids"), 'aids', dc=DEBIT)
TradeTypes.aids.update(
    partner_account_field_name='aids_account',
    partner_account_field_label=_("Aids account"))



# from lino_welfare.modlib.pcsw.mixins import ClientRelated


# class Movement(Movement, ClientRelated):
#     """In Lino Welfare, a *movement* can be *client-related*.

#     """
#     pass

# dd.update_field(Movement, 'client', blank=True, null=True)
