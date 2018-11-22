# -*- coding: UTF-8 -*-
# Copyright 2011-2014 Rumma & Ko Ltd
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

"""Adds default data to `jobs.Schedule`, `cv.Regime` and `cv.Status`.

"""

from lino.utils.instantiator import Instantiator
from lino.api.dd import babel_values


def objects():

    schedule = Instantiator('jobs.Schedule').build
    yield schedule(**babel_values('name',
                                  de=u"5-Tage-Woche",              fr=u"5 jours/semaine",         en=u"5 days/week"))
    yield schedule(**babel_values('name',
                                  de=u"Individuell",               fr=u"individuel",              en=u"Individual"))
    yield schedule(**babel_values('name',
                                  de=u"Montag, Mittwoch, Freitag",
                                  fr=u"lundi,mercredi,vendredi",
                                  en=u"Monday, Wednesday, Friday"))


