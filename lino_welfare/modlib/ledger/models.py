# -*- coding: UTF-8 -*-
# Copyright 2015-2020 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

"""
Database models for :mod:`lino_welfare.modlib.ledger`.
"""

from lino_xl.lib.ledger.models import *
from lino.api import _
from lino_xl.lib.ledger.utils import DC
from lino_xl.lib.ledger.choicelists import CommonAccounts
from lino_xl.lib.ledger.choicelists import TradeTypes


add = CommonAccounts.add_item
add('4450', _("Disbursement orders to execute"),
    "disbursement_orders", True)
add('4810', _("Granted aids"), "granted_aids", True)

# class DisbursementOrders(Liabilities):
#     value = '4450'
#     text = _("Disbursement orders to execute")
#     name = "disbursement_orders"
#     clearable = True
#     needs_partner = True
# CommonAccounts.add_item_instance(DisbursementOrders())

# class Aids(Liabilities):
#     value = '4800'
#     text = _("Aids")
#     name = "aids"
#     clearable = True
#     needs_partner = True
# CommonAccounts.add_item_instance(Aids())


JournalGroups.clear()
add = JournalGroups.add_item
add('10', _("Purchase orders"), 'bst')
add('20', _("Incoming invoices"), 'reg')
add('30', _("Claimings"), 'ffo')
add('40', _("Disbursement orders"), 'anw')
add('50', _("Payment orders"), 'zau')
# add('60', _("Financial"), 'tre')
# add('70', _("Budgetary"), 'hhh')
# add('80', _("Domiciliations"), 'dom')
# add('90', _("Closing entries"), 'clo')


TradeTypes.clear()
add = TradeTypes.add_item
add('P', _("Purchases"), 'purchases', dc=DC.debit)
add('A', _("Aids"), 'aids', dc=DC.debit)
add('C', _("Clearings"), 'clearings', dc=DC.debit)


TradeTypes.purchases.update(main_account=CommonAccounts.suppliers)
TradeTypes.aids.update(main_account=CommonAccounts.granted_aids)


from lino_xl.lib.ledger.models import Account
Account._meta.verbose_name = _("Budgetary article")
Account._meta.verbose_name_plural = _("Budgetary articles")

from lino_xl.lib.ledger.models import Voucher
fld = Voucher._meta.get_field('entry_date')
fld.verbose_name = _("Booking date")

def set_partner_verbose_name(m):
    fld = m._meta.get_field('partner')
    fld.verbose_name = _("Payment recipient")

from lino_xl.lib.ledger.models import Movement
set_partner_verbose_name(Movement)
from lino_xl.lib.finan.mixins import FinancialVoucherItem
set_partner_verbose_name(FinancialVoucherItem)
from lino_xl.lib.vatless.models import AccountInvoice
set_partner_verbose_name(AccountInvoice)
