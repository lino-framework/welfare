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

"""Adds demo journals and some bookings for usage by Lino Welfare.

"""

from lino.utils import Cycler
from lino.api import dd, rt

current_group = None


def objects():
    User = rt.modules.users.User
    Company = rt.modules.contacts.Company
    Client = rt.modules.pcsw.Client
    ClientStates = rt.modules.pcsw.ClientStates
    Journal = rt.modules.ledger.Journal
    AccountInvoice = rt.modules.vatless.AccountInvoice
    InvoiceItem = rt.modules.vatless.InvoiceItem
    Account = rt.modules.accounts.Account
    AccountCharts = rt.modules.accounts.AccountCharts
    AccountTypes = rt.modules.accounts.AccountTypes
    PaymentOrder = rt.modules.finan.PaymentOrder

    CLIENTS = Cycler(Client.objects.filter(
        client_state=ClientStates.coached)[:5])

    wilfried = User(username="wilfried",
                    first_name="Wilfried", last_name="Willems",
                    profile='500')
    yield wilfried

    qs = Company.objects.filter(sepa_accounts__iban__gt='').distinct()
    # RECIPIENTS = Cycler(qs[:5])
    RECIPIENTS = Cycler(qs)
    ACCOUNTS = Cycler(Account.objects.filter(
        chart=AccountCharts.default, type=AccountTypes.expenses))
    AMOUNTS = Cycler(10, '12.50', 25, '29.95', 120, '5.33')

    ses = rt.login('wilfried')
    jnl = Journal.get_by_ref('REG')
    for i in range(30):
        kw = dict()
        kw.update(partner=RECIPIENTS.pop())
        # if i % 9 != 0:
        #     kw.update(project=CLIENTS.pop())
        kw.update(date=dd.today(-5*i))
        kw.update(due_date=dd.today(30-5*i))
        kw.update(journal=jnl)
        kw.update(user=ses.get_user())
        obj = AccountInvoice(**kw)
        yield obj

        for j in range(i % 5 + 1):
            yield InvoiceItem(
                voucher=obj, amount=AMOUNTS.pop(),
                project=CLIENTS.pop(),
                account=ACCOUNTS.pop())
        # if i % 5 == 0:
        #     yield InvoiceItem(
        #         voucher=obj, amount=AMOUNTS.pop(), account=ACCOUNTS.pop())
        obj.register(ses)
        obj.save()

    jnl = Journal.get_by_ref('AAW')
    for i in range(30):
        kw = dict()
        kw.update(date=dd.today(-5*i))
        kw.update(journal=jnl)
        kw.update(user=ses.get_user())
        obj = PaymentOrder(**kw)
        yield obj

    if dd.is_installed('client_vouchers'):
        ClientVoucher = rt.modules.client_vouchers.ClientVoucher
        ClientVoucherItem = rt.modules.client_vouchers.VoucherItem
        jnl = Journal.get_by_ref('AIDS')
        for i in range(20):
            kw = dict()
            # kw.update(partner=RECIPIENTS.pop())
            # if i % 9 != 0:
            #     kw.update(project=CLIENTS.pop())
            kw.update(date=dd.today(-5*i))
            kw.update(journal=jnl)
            kw.update(project=CLIENTS.pop())
            kw.update(user=ses.get_user())
            obj = ClientVoucher(**kw)
            yield obj
            kw = dict(voucher=obj)
            for j in range(10):
                kw.update(amount=AMOUNTS.pop(), account=ACCOUNTS.pop())
                kw.update(partner=RECIPIENTS.pop())
                kw.update(seqno=j+1)
                yield ClientVoucherItem(**kw)
                obj.register(ses)
                obj.save()
