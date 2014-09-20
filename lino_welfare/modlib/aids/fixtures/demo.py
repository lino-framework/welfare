# -*- coding: UTF-8 -*-
# Copyright 2014 Luc Saffre
# This file is part of the Lino-Welfare project.
# Lino-Welfare is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
# Lino-Welfare is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with Lino-Welfare; if not, see <http://www.gnu.org/licenses/>.

"""
"""

from django.conf import settings
from lino.dd import resolve_model
from lino.utils import Cycler
from lino import dd, rt


def objects():
    Granting = rt.modules.aids.Granting
    AidType = rt.modules.aids.AidType
    Person = rt.modules.contacts.Person
    ClientStates = rt.modules.pcsw.ClientStates
    ClientContactType = rt.modules.pcsw.ClientContactType
    Board = rt.modules.boards.Board

    Project = resolve_model('pcsw.Client')
    qs = Project.objects.filter(client_state=ClientStates.coached)
    # if qs.count() > 10:
    #     qs = qs[:10]
    PROJECTS = Cycler(qs)

    l = []
    qs = ClientContactType.objects.filter(can_refund=True)
    for cct in qs:
        qs2 = Person.objects.filter(client_contact_type=cct)
        if qs2.count():
            i = (cct, Cycler(qs2))
            l.append(i)
    PARTNERS = Cycler(l)

    BOARDS = Cycler(Board.objects.all())

    for i, at in enumerate(AidType.objects.all()):
        kw = dict(start_date=dd.demo_date(days=i),
                  board=BOARDS.pop(),
                  decision_date=dd.demo_date(days=i-1),
                  aid_type=at)
        kw.update(client=PROJECTS.pop())
        yield Granting(**kw)

    # ConfirmationTypes = rt.modules.aids.ConfirmationTypes
    RefundConfirmation = rt.modules.aids.RefundConfirmation
    # for i in range(5):
    #     for ct in ConfirmationTypes.items():
    #         for at in AidType.objects.filter(confirmation_type=ct):
    #             for g in Granting.objects.filter(aid_type=at):
    #                 kw = dict(granting=g, client=g.client)
    #                 if ct.model == RefundConfirmation:
    #                     type, cycler = PARTNERS.pop()
    #                     kw.update(partner_type=type)
    #                     kw.update(partner=cycler.pop())
    #                 yield ct.model(**kw)

    for i in range(2):
        for g in Granting.objects.all():
            ct = g.aid_type.confirmation_type
            kw = dict(granting=g, client=g.client)
            if ct.model == RefundConfirmation:
                type, cycler = PARTNERS.pop()
                kw.update(doctor_type=type)
                kw.update(doctor=cycler.pop())
            yield ct.model(**kw)
