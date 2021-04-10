# -*- coding: UTF-8 -*-
# Copyright 2015-2021 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

"""Adds demo journals and some bookings for usage by Lino Welfare.

"""

from dateutil.relativedelta import relativedelta as delta
# from builtins import range
from lino_xl.lib.sepa.fixtures.demo import objects as lib_objects
from decimal import Decimal as D

from lino.utils import Cycler
from lino.api import dd, rt

from django.conf import settings
from lino_xl.lib.clients.choicelists import ClientStates


def objects():
    yield lib_objects()

    Client = rt.models.pcsw.Client
    Company = rt.models.contacts.Company
    Journal = rt.models.ledger.Journal
    AccountInvoice = rt.models.vatless.AccountInvoice
    InvoiceItem = rt.models.vatless.InvoiceItem
    Account = rt.models.ledger.Account
    PaymentOrder = rt.models.finan.PaymentOrder
    PaymentOrderItem = rt.models.finan.PaymentOrderItem

    CLIENTS = Cycler(Client.objects.filter(
        client_state=ClientStates.coached)[:5])
    if len(CLIENTS) == 0:
        raise Exception("Oops, no CLIENTS in %s" % CLIENTS)
    qs = Company.objects.filter(sepa_accounts__iban__gt='').distinct()
    # qs = Company.objects.exclude(sepa_accounts__iban='').distinct().order_by('id')
    # if qs.count() == 0:
    # qs = qs.order_by('name')
    # RECIPIENTS = Cycler(qs[:5])
    RECIPIENTS = Cycler(qs)
    if len(RECIPIENTS) == 0:
        raise Exception("Oops, no recipients in %s" % qs)
    ACCOUNTS = Cycler(Account.objects.filter(ref__startswith="8"))
    if len(ACCOUNTS) == 0:
        raise Exception("Oops, no ACCOUNTS in %s" % ACCOUNTS)
    AMOUNTS = Cycler(10, D('12.50'), 25, D('29.95'), 120, D('5.33'))
    ITEMNUMS = Cycler(1, 5, 1, 1, 7, 1)

    ses = rt.login('wilfried')
    REG = Journal.get_by_ref('REG')
    SREG = Journal.get_by_ref('SREG')
    for i in range(30):
        kw = dict()
        kw.update(partner=RECIPIENTS.pop())
        # if i % 9 != 0:
        #     kw.update(project=CLIENTS.pop())
        kw.update(entry_date=dd.today(-5*i))
        kw.update(voucher_date=dd.today(-5*i-1))
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
    ACCOUNTS = list(rt.models.ledger.Account.objects.filter(ref__in=refs))
    AMOUNTS = Cycler(D('648.91'), D('817.36'), D('544.91'), D('800.08'))
    jnl = Journal.get_by_ref('AAW')
    months = 2
    date = dd.today(-30*months)
    for i in range(months+1):
        kw = dict()
        kw.update(entry_date=date)
        kw.update(voucher_date=date)
        kw.update(journal=jnl)
        kw.update(user=ses.get_user())
        for acc in ACCOUNTS:
            kw.update(narration=acc.name)
            kw.update(item_account=acc)
            obj = jnl.create_voucher(**kw)
            # obj = PaymentOrder(**kw)
            yield obj
            for j in range(5):
                cli = CLIENTS.pop()
                yield PaymentOrderItem(
                    seqno=j+1,
                    voucher=obj,
                    amount=-AMOUNTS.pop(), project=cli)
            # this is especially slow in a sqlite :memory: databae
            # dd.logger.info(
            #     "20151211 Gonna register PaymentOrder %s %s %s",
            #     dd.fds(obj.entry_date), obj, obj.narration)
            obj.register(ses)
            obj.save()

        date += delta(months=1)
