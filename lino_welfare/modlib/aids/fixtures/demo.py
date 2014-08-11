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
from lino import dd


def objects():
    Aid = resolve_model('aids.IncomeConfirmation')
    NTYPES = Cycler(Aid.get_aid_types())
    Category = resolve_model('aids.Category')
    ClientStates = dd.modules.pcsw.ClientStates

    Project = resolve_model('pcsw.Client')
    qs = Project.objects.filter(client_state=ClientStates.coached)
    if qs.count() > 10:
        qs = qs[:10]
    PROJECTS = Cycler(qs)

    CATS = Cycler(Category.objects.all())

    for i in range(12):
        client = PROJECTS.pop()
        author = settings.SITE.user_model.objects.get(username='theresia')
        atype = NTYPES.pop()
        kw = dict(category=CATS.pop(),
                  start_date=settings.SITE.demo_date(days=i),
                  user=author,
                  aid_type=atype)
        kw.update(client=client)
        yield Aid(**kw)
