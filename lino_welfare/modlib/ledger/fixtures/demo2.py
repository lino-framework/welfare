# -*- coding: UTF-8 -*-
# Copyright 2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""
The demo fixture for :mod:`welfare.aids`.
"""

import datetime

from django.utils.translation import ugettext_lazy as _
from lino.utils import Cycler
from lino.utils import mti
from lino.api import dd, rt

current_group = None


def objects():
    Partner = rt.modules.contacts.Partner
    Client = rt.modules.pcsw.Client
    ClientContactType = rt.modules.pcsw.ClientContactType
    ClientStates = rt.modules.pcsw.ClientStates
    Journal = rt.modules.ledger.Journal
    BankStatement = rt.modules.finan.BankStatement
    AccountInvoice = rt.modules.ledger.AccountInvoice

    CLIENTS = Cycler(Client.objects.filter(client_state=ClientStates.coached))

    l = []
    qs = ClientContactType.objects.filter(can_refund=True)
    for cct in qs:
        qs2 = Partner.objects.filter(client_contact_type=cct)
        if qs2.count():
            i = (cct, Cycler(qs2))
            l.append(i)
    RECIPIENTS = Cycler(l)

    PRC = Journal.get_by_ref('PRC')
    for i in range(20):
        kw = dict()
        kw.update(partner=CLIENTS.pop())
        if i % 3:
            kw.update(recipient=RECIPIENTS.pop())
        kw.update(date=dd.today(-5*i))
        kw.update(journal=PRC)
        yield AccountInvoice(**kw)

