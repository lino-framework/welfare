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

import os
HERE = os.path.dirname(__file__)

from lino_cosi.lib.sepa.fixtures.demo import objects as lib_objects

from lino.utils import Cycler
from lino.api import dd, rt

from django.conf import settings


def objects():
    yield lib_objects()

    Client = rt.modules.pcsw.Client
    ClientStates = rt.modules.pcsw.ClientStates
    Company = rt.modules.contacts.Company
    Journal = rt.modules.ledger.Journal
    AccountInvoice = rt.modules.vatless.AccountInvoice
    InvoiceItem = rt.modules.vatless.InvoiceItem
    Account = rt.modules.accounts.Account
    AccountCharts = rt.modules.accounts.AccountCharts
    AccountTypes = rt.modules.accounts.AccountTypes
    PaymentOrder = rt.modules.finan.PaymentOrder
    PaymentOrderItem = rt.modules.finan.PaymentOrderItem

    CLIENTS = Cycler(Client.objects.filter(
        client_state=ClientStates.coached)[:5])
    if len(CLIENTS) == 0:
        raise Exception("Oops, no CLIENTS in %s" % CLIENTS)
    qs = Company.objects.filter(sepa_accounts__iban__gt='').distinct()
    # RECIPIENTS = Cycler(qs[:5])
    RECIPIENTS = Cycler(qs)
    if len(RECIPIENTS) == 0:
        raise Exception("Oops, no recipients in %s" % qs)
    ACCOUNTS = Cycler(Account.objects.filter(
        chart=AccountCharts.default, type=AccountTypes.expenses))
    if len(ACCOUNTS) == 0:
        raise Exception("Oops, no ACCOUNTS in %s" % ACCOUNTS)
    AMOUNTS = Cycler(10, '12.50', 25, '29.95', 120, '5.33')
    ITEMNUMS = Cycler(1, 5, 1, 1, 7, 1)

    ses = rt.login('wilfried')
    REG = Journal.get_by_ref('REG')
    SREG = Journal.get_by_ref('SREG')
    for i in range(30):
        kw = dict()
        kw.update(partner=RECIPIENTS.pop())
        # if i % 9 != 0:
        #     kw.update(project=CLIENTS.pop())
        kw.update(date=dd.today(-5*i))
        kw.update(due_date=dd.today(30-5*i))
        kw.update(user=ses.get_user())
        itemnum = ITEMNUMS.pop()
        acc = ACCOUNTS.pop()
        prj = CLIENTS.pop()
        if itemnum == 1:
            kw.update(journal=REG)
            kw.update(project=prj)
        else:
            kw.update(journal=SREG)
        obj = AccountInvoice(**kw)
        yield obj
        for j in range(itemnum):
            yield InvoiceItem(
                voucher=obj, amount=AMOUNTS.pop(),
                project=prj, account=acc)
            prj = CLIENTS.pop()
        obj.register(ses)
        obj.save()

    refs = ('832/3331/01', '832/330/01', '832/330/03F',
            '832/330/03', '832/3343/21', '832/334/27')
    ACCOUNTS = list(rt.modules.accounts.Account.objects.filter(ref__in=refs))
    AMOUNTS = Cycler('648.91', '817.36', '544.91', '800.08')
    jnl = Journal.get_by_ref('AAW')
    for i in range(3):
        kw = dict()
        kw.update(date=dd.today(-30*i))
        kw.update(journal=jnl)
        kw.update(user=ses.get_user())
        for acc in ACCOUNTS:
            kw.update(narration=acc.name)
            obj = PaymentOrder(**kw)
            yield obj
            for j in range(5):
                cli = CLIENTS.pop()
                yield PaymentOrderItem(
                    seqno=j+1,
                    voucher=obj,
                    account=acc,
                    amount=AMOUNTS.pop(),
                    project=cli, partner=cli)
            # this is especially slow in a sqlite :memory: databae
            dd.logger.info(
                "20151211 Gonna register PaymentOrder %s %s %s",
                dd.fds(obj.date), obj, obj.narration)
            obj.register(ses)
            obj.save()
