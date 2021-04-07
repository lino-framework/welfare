# -*- coding: UTF-8 -*-
# Copyright 2015-2020 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

"""Defines some default journals for social accounting.

"""

from lino.api import dd, rt, _
from lino_xl.lib.ledger.utils import DC
from lino_xl.lib.ledger.choicelists import CommonAccounts

def objects():

    Account = rt.models.ledger.Account
    JournalGroups = rt.models.ledger.JournalGroups
    BankStatement = rt.models.finan.BankStatement
    PaymentOrdersByJournal = rt.models.finan.PaymentOrdersByJournal
    DisbursementOrdersByJournal = rt.models.finan.DisbursementOrdersByJournal
    InvoicesByJournal = rt.models.vatless.InvoicesByJournal
    ProjectInvoicesByJournal = rt.models.vatless.ProjectInvoicesByJournal
    MatchRule = rt.models.ledger.MatchRule
    a4400 = CommonAccounts.suppliers.get_object()
    a4450 = CommonAccounts.disbursement_orders.get_object()
    a5800 = CommonAccounts.pending_po.get_object()

    kw = dict(journal_group=JournalGroups.reg)
    kw.update(trade_type='purchases', ref="REG")
    kw.update(dd.str2kw('name', _("Incoming invoices")))
    kw.update(dc=DC.debit)
    yield ProjectInvoicesByJournal.create_journal(**kw)

    kw.update(ref="SREG")
    kw.update(dd.str2kw('name', _("Collective purchase invoices")))
    yield InvoicesByJournal.create_journal(**kw)

    kw.update(dd.str2kw('name', _("Disbursement orders")))
    kw.update(account='4450', ref="AAW")
    kw.update(journal_group=JournalGroups.anw)
    kw.update(dc=DC.credit)  # 20201219  AAW Journal.dc
    # kw.update(invert_due_dc=False)
    jnl = DisbursementOrdersByJournal.create_journal(**kw)
    yield jnl
    yield MatchRule(journal=jnl, account=a4400)

    if dd.is_installed('client_vouchers'):
        ClientVoucher = rt.models.client_vouchers.ClientVoucher
        kw = dict(journal_group=JournalGroups.aids)
        kw.update(trade_type='aids', ref="AIDS")
        kw.update(dd.str2kw('name', _("Aid allocations")))
        jnl = ClientVoucher.create_journal(**kw)
        yield jnl
        yield MatchRule(journal=jnl, account=a4400)

    kw = dict()
    # kw.update(journal_group=JournalGroups.tre)
    # kw.update(dd.str2kw('name', _("KBC")))
    # kw.update(account='5500', ref="KBC")
    # jnl = BankStatement.create_journal(**kw)
    # yield jnl
    # yield MatchRule(journal=jnl, account=a4450)
    # yield MatchRule(journal=jnl, account=a5800)

    kw.update(journal_group=JournalGroups.zau)
    kw.update(dd.str2kw('name', _("KBC Payment Orders")))
    kw.update(account=a5800, ref="ZKBC")
    kw.update(dc=DC.credit)  # 20201219  ZKBC Journal.dc
    jnl = PaymentOrdersByJournal.create_journal(**kw)
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
