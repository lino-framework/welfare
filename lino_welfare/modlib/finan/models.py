# -*- coding: UTF-8 -*-
# Copyright 2013-2016 Rumma & Ko Ltd
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

from lino_xl.lib.finan.models import *
from lino.api import _


class DisbursementOrderDetail(JournalEntryDetail):
    general = dd.Panel("""
    journal number voucher_date entry_date accounting_period
    item_account total workflow_buttons
    narration item_remark
    finan.ItemsByDisbursementOrder
    """, label=_("General"))

    more = dd.Panel("""
    state user id
    ledger.MovementsByVoucher
    """, label=_("More"))


class DisbursementOrders(PaymentOrders):
    """The table of all :class:`PaymentOrder` vouchers seen as payment
    instructions."""
    detail_layout = DisbursementOrderDetail()
    suggestions_table = 'finan.SuggestionsByPaymentOrder'


class ItemsByPaymentOrder(ItemsByPaymentOrder):
    column_names = "seqno project partner workflow_buttons bank_account match "\
                   "amount remark *"


class ItemsByDisbursementOrder(ItemsByPaymentOrder):
    column_names = "seqno project partner bank_account workflow_buttons match "\
                   "amount *"


class DisbursementOrdersByJournal(ledger.ByJournal, DisbursementOrders):
    insert_layout = """
    item_account
    voucher_date
    """


VoucherTypes.add_item_lazy(
    DisbursementOrdersByJournal, _("Disbursement orders"))


@dd.receiver(dd.pre_analyze)
def override_field_names(sender=None, **kwargs):
    for m in rt.models_by_base(FinancialVoucher):
        dd.update_field(
            m, 'narration', verbose_name=_("Internal reference"))
        dd.update_field(
            m, 'item_remark', verbose_name=_("External reference"))
    for m in rt.models_by_base(FinancialVoucherItem):
        # dd.update_field(
        #     m, 'narration', verbose_name=_("Internal reference"))
        dd.update_field(
            m, 'remark', verbose_name=_("External reference"))
