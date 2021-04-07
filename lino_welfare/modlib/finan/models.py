# -*- coding: UTF-8 -*-
# Copyright 2013-2020 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

"""
Database models for this plugin.
"""

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
                   "to_pay remark *"


class ItemsByDisbursementOrder(ItemsByPaymentOrder):
    column_names = "seqno project partner bank_account workflow_buttons match "\
                   "to_pay *"


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
