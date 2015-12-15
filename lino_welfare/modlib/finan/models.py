# -*- coding: UTF-8 -*-
# Copyright 2013-2015 Luc Saffre
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
Database models for :mod:`lino_welfare.modlib.cal`.
"""

from __future__ import unicode_literals

from lino_cosi.lib.finan.models import *
from lino.api import _


class PaymentInstructionDetail(JournalEntryDetail):
    general = dd.Panel("""
    date user narration total workflow_buttons
    finan.ItemsByPaymentInstruction
    """, label=_("General"))


class PaymentInstructions(PaymentOrders):
    """The table of all :class:`PaymentOrder` vouchers seen as payment
    instructions."""
    detail_layout = PaymentInstructionDetail()
    suggestions_table = 'finan.SuggestionsByPaymentOrder'


class ItemsByPaymentOrder(ItemsByPaymentOrder):
    column_names = "seqno project partner workflow_buttons bank_account match "\
                   "amount remark *"


class ItemsByPaymentInstruction(ItemsByPaymentOrder):
    column_names = "seqno project partner account workflow_buttons match "\
                   "amount remark *"


class PaymentInstructionsByJournal(ledger.ByJournal, PaymentInstructions):
    pass


VoucherTypes.add_item(PaymentOrder, PaymentInstructionsByJournal)
