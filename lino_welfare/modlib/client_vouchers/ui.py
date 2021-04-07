# -*- coding: UTF-8 -*-
# Copyright 2015 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

"""Actors for `lino.modlib.client_vouchers`.



"""

from __future__ import unicode_literals

from lino.api import dd, rt, _

from lino_xl.lib.ledger.choicelists import VoucherTypes
from lino_xl.lib.ledger.ui import PartnerVouchers, ByJournal


class VoucherItems(dd.Table):
    model = 'client_vouchers.VoucherItem'
    auto_fit_column_widths = True
    order_by = ['voucher', "seqno"]


class ItemsByVoucher(VoucherItems):
    column_names = "partner due_date your_ref title amount"
    master_key = 'voucher'
    order_by = ["seqno"]


class ClientVoucherDetail(dd.DetailLayout):
    main = "general ledger"

    general = dd.Panel("""
    id date project user
    workflow_buttons amount
    ItemsByVoucher
    """, label=_("General"))

    ledger = dd.Panel("""
    journal year number narration state
    ledger.MovementsByVoucher
    """, label=_("Ledger"))


class ClientVouchers(PartnerVouchers):
    model = 'client_vouchers.ClientVoucher'
    order_by = ["-id"]
    column_names = "date id number project amount user *"
    detail_layout = ClientVoucherDetail()
    insert_layout = """
    journal project
    date amount
    """


class ClientVouchersByJournal(ByJournal, ClientVouchers):
    """Shows all simple invoices of a given journal (whose
    :attr:`Journal.voucher_type` must be
    :class:`lino_xl.lib.sales.models.ClientVoucher`).

    """
    params_layout = "project partner state year"
    column_names = "number date project amount user workflow_buttons *"
    insert_layout = """
    project
    date amount
    """
    # order_by = ["-number"]


VoucherTypes.add_item_lazy(ClientVouchersByJournal)
