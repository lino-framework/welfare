# -*- coding: UTF-8 -*-
# Copyright 2015 Rumma & Ko Ltd
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


class ClientVouchersByJournal(ClientVouchers, ByJournal):
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
    order_by = ["-number"]


VoucherTypes.add_item_lazy(ClientVouchersByJournal)

