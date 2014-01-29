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
from django.utils.translation import ugettext as _
from lino.utils.instantiator import Instantiator
from lino.dd import resolve_model
from lino.utils import Cycler


def objects():
    Aid = resolve_model('aids.Aid')
    Decider = resolve_model('aids.Decider')
    Category = resolve_model('aids.Category')
    AidType = resolve_model('aids.AidType')

    if settings.SITE.project_model is not None:
        Project = resolve_model(settings.SITE.project_model)
        qs = Project.objects.all()
        if qs.count() > 10:
            qs = qs[:10]
        PROJECTS = Cycler(qs)
    
    NTYPES = Cycler(AidType.objects.all())
    DECIDERS = Cycler(Decider.objects.all())
    CATS = Cycler(Category.objects.all())

    for i in range(12):
        kw = dict(decider=DECIDERS.pop(),
                  category=CATS.pop(),
                  decided_date=settings.SITE.demo_date(days=i),
                  type=NTYPES.pop())
        if settings.SITE.project_model is not None:
            kw.update(project=PROJECTS.pop())
        yield Aid(**kw)
