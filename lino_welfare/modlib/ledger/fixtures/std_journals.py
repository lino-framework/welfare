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

"""Defines some default journals for social accounting.


"""

from __future__ import unicode_literals

from lino.api import dd, rt, _


def objects():

    Account = rt.modules.accounts.Account
    JournalGroups = rt.modules.ledger.JournalGroups
    BankStatement = rt.modules.finan.BankStatement
    PaymentOrder = rt.modules.finan.PaymentOrder
    DisbursementOrdersByJournal = rt.modules.finan.DisbursementOrdersByJournal
    InvoicesByJournal = rt.modules.vatless.InvoicesByJournal
    ProjectInvoicesByJournal = rt.modules.vatless.ProjectInvoicesByJournal
    MatchRule = rt.modules.ledger.MatchRule
    a4400 = Account.objects.get(ref="4400")
    a4450 = Account.objects.get(ref="4450")
    a5800 = Account.objects.get(ref="5800")

    kw = dict(journal_group=JournalGroups.reg)
    kw.update(trade_type='purchases', ref="REG")
    kw.update(dd.str2kw('name', _("Incoming invoices")))
    yield ProjectInvoicesByJournal.create_journal(**kw)

    kw.update(ref="SREG")
    kw.update(dd.str2kw('name', _("Collective purchase invoices")))
    yield InvoicesByJournal.create_journal(**kw)

    kw.update(dd.str2kw('name', _("Disbursement orders")))
    kw.update(account='4450', ref="AAW")
    kw.update(journal_group=JournalGroups.anw)
    jnl = DisbursementOrdersByJournal.create_journal(**kw)
    yield jnl
    yield MatchRule(journal=jnl, account=a4400)

    if dd.is_installed('client_vouchers'):
        ClientVoucher = rt.modules.client_vouchers.ClientVoucher
        kw = dict(journal_group=JournalGroups.aids)
        kw.update(trade_type='aids', ref="AIDS")
        kw.update(dd.str2kw('name', _("Aid allocations")))
        jnl = ClientVoucher.create_journal(**kw)
        yield jnl
        yield MatchRule(journal=jnl, account=a4400)

    kw = dict()
    kw.update(journal_group=JournalGroups.tre)
    kw.update(dd.str2kw('name', _("KBC")))
    kw.update(account='5500', ref="KBC")
    jnl = BankStatement.create_journal(**kw)
    yield jnl
    yield MatchRule(journal=jnl, account=a4450)
    yield MatchRule(journal=jnl, account=a5800)

    kw.update(journal_group=JournalGroups.zau)
    kw.update(dd.str2kw('name', _("KBC Payment Orders")))
    kw.update(account='5800', ref="ZKBC")
    jnl = PaymentOrder.create_journal(**kw)
    yield jnl
    yield MatchRule(journal=jnl, account=a4450)

    # kw.update(journal_group=JournalGroups.financial)
    # kw.update(trade_type='aids')
    # kw.update(ref="AAW")
    # kw.update(dd.str2kw('name', _("Aid allocations")))  # Zahlungsanweisungen
    # kw.update(account='5810')
    # jnl = PaymentOrder.create_journal(**kw)
    # yield jnl
    # yield MatchRule(journal=jnl, account=a4460)

