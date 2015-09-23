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

"""Defines a default accounts chart with account groups and accounts
for social accounting.


Purchase invoices go to 4400 (suppliers). Unlike default ledger, 4400
is to be matched by a payment *instruction* which moves them to 4450
(instructions to execute). And then we write a payment *order* which
satisfies the payment *instruction*.

Classic accounting:

#. Purchase invoice -> 4400
#. (4400 ->) Payment order -> 5800
#. Bank Statement -> 5500

Lino Welfare accounting:

#. Purchase invoice -> 4400
#. (4400 ->) Payment instruction -> 4450
#. (4450 ->) Payment order -> 5800
#. (5800 ->) Bank Statement -> 5500



"""

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from lino.api import dd, rt

current_group = None


def objects():
    # Chart = rt.modules.accounts.Chart
    Group = rt.modules.accounts.Group
    Account = rt.modules.accounts.Account
    AccountTypes = rt.modules.accounts.AccountTypes
    JournalGroups = rt.modules.ledger.JournalGroups
    BankStatement = rt.modules.finan.BankStatement
    PaymentOrder = rt.modules.finan.PaymentOrder
    AccountInvoice = rt.modules.vatless.AccountInvoice
    MatchRule = rt.modules.ledger.MatchRule

    # chart = Chart(**dd.str2kw('name',  _("Social Accounting")))
    # yield chart
    chart = rt.modules.accounts.AccountCharts.default

    def group(ref, type, name):
        global current_group
        current_group = Group(
            chart=chart,
            ref=ref,
            account_type=AccountTypes.get_by_name(type),
            **dd.str2kw('name', name))
        return current_group

    def account(ref, type, name, **kw):
        kw.update(dd.str2kw('name', name))
        return Account(
            chart=chart,
            group=current_group,
            ref=ref,
            type=AccountTypes.get_by_name(type), **kw)

    # yield group('10', 'capital', _("Capital"))
    yield group('40', 'assets', _("Receivables"))
    obj = account('4000', 'assets', _("Customers"), clearable=True)
    yield obj
    # if sales:
    #     settings.SITE.site_config.update(clients_account=obj)

    yield group('44', 'assets', _("Liabilities"))
    a4400 = account('4400', 'liabilities', _("Suppliers"), clearable=True)
    yield a4400
    settings.SITE.site_config.update(suppliers_account=a4400)

    a4450 = account('4450', 'liabilities',
                    _("Instructions to execute"), clearable=True)
    yield a4450
    # settings.SITE.site_config.update(suppliers_account=a4400)

    yield group('55', 'assets', _("Financial institutes"))
    yield account("5500", 'bank_accounts', "KBC")
    # a5600 = account("5600", 'bank_accounts', _("Payment instructions"))
    # yield a5600
    yield account("5700", 'bank_accounts', _("Cash"))

    yield group('58', 'assets', _("Current transactions"))
    a5800 = account("5800", 'bank_accounts', _("Payment Orders"),
                    clearable=True)
    yield a5800

    yield group('6', 'expenses', _("Expenses"))
    for ref, name in (
            ('832/3331/01', _("Eingliederungseinkommen")),
            ('832/330/01', _("Allgemeine Beihilfen")),
            ('832/330/03F', _("Fonds Gas und Elektrizität")),
            ('832/330/03', _("Heizkosten- u. Energiebeihilfe")),
            ('832/3343/21', _("Beihilfe für Ausländer")),
            ('832/334/27', _("Sozialhilfe")),
            ('832/333/22', _("Mietbeihilfe")),
            ('832/330/04', _("Mietkaution")),
            ('820/333/01', _("Vorschuss auf Vergütungen o.ä.")),
            ('821/333/01', _("Vorschuss auf Pensionen")),
            ('822/333/01', _("Vorsch. Entsch. Arbeitsunfälle")),
            ('823/333/01', _("Vor. Kranken- u. Invalidengeld")),
            ('825/333/01', _("Vorschuss auf Familienzulage")),
            ('826/333/01', _("Vorschuss auf Arbeitslosengeld")),
            ('827/333/01', _("Vorschuss auf Behindertenzulag")),
            ('P87/000/00', _("Abhebung von pers. Guthaben")),
            ('P82/000/00', _("Einn. Dritter: Weiterleitung")),
            ('P83/000/00', _("Unber. erh. Beträge + Erstatt.")),
            ('832/330/02', _("Gesundheitsbeihilfe")),
            ):
        yield account(ref, 'expenses', name, purchases_allowed=True)

    yield group('7', 'incomes', _("Revenues"))
    obj = account('7000', 'incomes', _("Sales"), sales_allowed=True)
    yield obj

    kw = dict(chart=chart, journal_group=JournalGroups.purchases)
    kw.update(trade_type='purchases', ref="REG")
    kw.update(dd.str2kw('name', _("Purchase invoices")))
    yield AccountInvoice.create_journal(**kw)

    kw = dict(chart=chart, journal_group=JournalGroups.aids)
    kw.update(dd.str2kw('name', _("Payment instructions")))
    kw.update(account='4450', ref="AAW")
    jnl = PaymentOrder.create_journal(**kw)
    yield jnl
    yield MatchRule(journal=jnl, account=a4400)

    if dd.is_installed('client_vouchers'):
        ClientVoucher = rt.modules.client_vouchers.ClientVoucher
        kw = dict(chart=chart, journal_group=JournalGroups.aids)
        kw.update(trade_type='aids', ref="AIDS")
        kw.update(dd.str2kw('name', _("Aids allocations")))
        jnl = ClientVoucher.create_journal(**kw)
        yield jnl
        yield MatchRule(journal=jnl, account=a4400)

    kw.update(journal_group=JournalGroups.financial)
    kw.update(dd.str2kw('name', _("KBC")))
    kw.update(account='5500', ref="KBC")
    jnl = BankStatement.create_journal(**kw)
    yield jnl
    yield MatchRule(journal=jnl, account=a4450)
    yield MatchRule(journal=jnl, account=a5800)

    kw.update(journal_group=JournalGroups.financial)
    kw.update(dd.str2kw('name', _("PO KBC")))
    kw.update(account='5800', ref="POKBC")
    jnl = PaymentOrder.create_journal(**kw)
    yield jnl
    yield MatchRule(journal=jnl, account=a4450)

