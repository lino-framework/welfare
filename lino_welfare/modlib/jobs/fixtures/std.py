# -*- coding: UTF-8 -*-
# Copyright 2011-2014 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

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


