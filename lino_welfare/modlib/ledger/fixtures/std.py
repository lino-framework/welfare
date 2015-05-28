# -*- coding: UTF-8 -*-
# Copyright 2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""Defines a default accounts chart with account groups and accounts
for social accounting.

"""

from django.utils.translation import ugettext_lazy as _

from lino.api import dd, rt

current_group = None


def objects():
    AccountInvoice = rt.modules.ledger.AccountInvoice
    JournalGroups = rt.modules.ledger.JournalGroups
    BankStatement = rt.modules.finan.BankStatement
    # Chart = rt.modules.accounts.Chart
    Group = rt.modules.accounts.Group
    Account = rt.modules.accounts.Account
    AccountTypes = rt.modules.accounts.AccountTypes

    # chart = Chart(**dd.str2kw('name',  _("Social Accounting")))
    # yield chart
    chart = rt.modules.accounts.AccountCharts.welfare

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

    yield group('44', 'assets', _("Suppliers"))
    obj = account('4400', 'liabilities', _("Suppliers"), clearable=True)
    yield obj
    # if vat:
    #     settings.SITE.site_config.update(suppliers_account=obj)

    yield group('55', 'assets', _("Financial institutes"))
    yield account("5500", 'bank_accounts', "Bestbank")
    yield account("5700", 'bank_accounts', _("Cash"))

    yield group('58', 'assets', _("Current transactions"))
    yield account("5810", 'bank_accounts', _("Payment Orders"),
                  clearable=True)

    yield group('6', 'expenses', _("Expenses"))
    yield account('6040', 'expenses', _("Purchase of miscellaneous services"),
                  purchases_allowed=True)

    yield group('7', 'incomes', _("Revenues"))
    obj = account('7000', 'incomes', _("Sales"), sales_allowed=True)
    yield obj

    kw = dict(chart=chart, journal_group=JournalGroups.purchases)
    kw.update(trade_type='purchases', ref="PRC")
    kw.update(dd.str2kw('name', _("Purchase invoices")))
    yield AccountInvoice.create_journal(**kw)

    kw.update(journal_group=JournalGroups.financial)
    kw.update(dd.str2kw('name', _("Bestbank")))
    kw.update(account='5500', ref="BNK")
    yield BankStatement.create_journal(**kw)

