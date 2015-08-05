# -*- coding: UTF-8 -*-
# Copyright 2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""Actors for `lino.modlib.client_vouchers`.



"""

from __future__ import unicode_literals

from lino.api import dd, rt, _

from lino.modlib.ledger.choicelists import VoucherTypes
from lino.modlib.ledger.ui import PartnerVouchers, ByJournal

from .models import ClientVoucher


class VoucherItems(dd.Table):
    model = 'client_vouchers.VoucherItem'
    auto_fit_column_widths = True
    order_by = ['voucher', "seqno"]


class ItemsByVoucher(VoucherItems):
    column_names = "partner due_date your_ref title amount"
    master_key = 'voucher'
    order_by = ["seqno"]


class ClientVoucherDetail(dd.FormLayout):
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


class ClientVouchersByJournal(ClientVouchers, ByJournal):
    """Shows all simple invoices of a given journal (whose
    :attr:`Journal.voucher_type` must be
    :class:`lino.modlib.sales.models.ClientVoucher`).

    """
    params_layout = "project partner state year"
    column_names = "number date project amount user workflow_buttons *"
    insert_layout = """
    project
    date amount
    """
    order_by = ["-number"]

VoucherTypes.add_item(ClientVoucher, ClientVouchersByJournal)

