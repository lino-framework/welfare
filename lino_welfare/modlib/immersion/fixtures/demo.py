# -*- coding: UTF-8 -*-
# Copyright 2015 Luc Saffre
# License: BSD (see file COPYING for details)
"""Adds some demo trainings for an arbitrary selection of clients.

Now done by :mod:`lino_welfare.modlib.integ.fixtures.demo`

"""

# from django.utils.translation import ugettext_lazy as _

from lino.api import rt, dd
from lino.utils.cycler import Cycler


def objects():
    
    yield rt.login('alicia').get_user()

    if False:  # done in lino_welfare/modlib/integ/fixtures/

        TT = Cycler(rt.models.immersion.ContractType.objects.all())
        TG = Cycler(rt.models.immersion.Goal.objects.all())
        Training = rt.models.immersion.Contract

        alicia = rt.login('alicia').get_user()
        selected_clients = (131, 149, 161)
        for i, pk in enumerate(selected_clients):
            kw = dict(client_id=pk)
            kw.update(type=TT.pop())
            kw.update(user=alicia)
            kw.update(goal=TG.pop())
            kw.update(applies_from=dd.demo_date(i*30))
            kw.update(applies_until=dd.demo_date(i*30+60*(i+1)))
            yield Training(**kw)

