# -*- coding: UTF-8 -*-
# Copyright 2014 Luc Saffre
# License: BSD (see file COPYING for details)

"""
Adds demo data for :mod:`lino_welfare.modlib.active_job_search`.
"""

from lino import dd
from lino.utils import Cycler
from lino.utils.instantiator import Instantiator

pcsw = dd.resolve_app('pcsw')
contacts = dd.resolve_app('contacts')
active_job_search = dd.resolve_app('active_job_search')


def create(client, company, date, spontaneous):
    return active_job_search.Proof(
        date=date, client=client, company=company,
        spontaneous=spontaneous)


def objects():
    CLIENTS = Cycler(pcsw.Client.objects.filter(
        client_state=pcsw.ClientStates.coached))
    COMPANIES = Cycler(contacts.Company.objects.all())
    for i in range(10):
        yield create(CLIENTS.pop(), COMPANIES.pop(),
                     dd.demo_date(i), i % 2)
