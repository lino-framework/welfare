# -*- coding: UTF-8 -*-
# Copyright 2011-2014 Luc Saffre
# License: BSD (see file COPYING for details)

"""Adds default data to `jobs.Schedule`, `cv.Regime` and `cv.Status`.

TODO: move data for `cv.Regime` and `cv.Status` to :mod:`lino.modlib.cv`.

"""

from django.utils.translation import ugettext_lazy as _

from lino.utils.instantiator import Instantiator
from lino.dd import babel_values

from lino import dd


def objects():

    regime = Instantiator('cv.Regime').build
    yield regime(**babel_values('name',
                                de=u"20 Stunden/Woche", fr=u"20 heures/semaine", en=u"20 hours/week"))
    yield regime(**babel_values('name',
                                de=u"35 Stunden/Woche", fr=u"35 heures/semaine", en=u"35 hours/week"))
    yield regime(**babel_values('name',
                                de=u"38 Stunden/Woche", fr=u"38 heures/semaine", en=u"38 hours/week"))

    schedule = Instantiator('jobs.Schedule').build
    yield schedule(**babel_values('name',
                                  de=u"5-Tage-Woche",              fr=u"5 jours/semaine",         en=u"5 days/week"))
    yield schedule(**babel_values('name',
                                  de=u"Individuell",               fr=u"individuel",              en=u"Individual"))
    yield schedule(**babel_values('name',
                                  de=u"Montag, Mittwoch, Freitag",
                                  fr=u"lundi,mercredi,vendredi",
                                  en=u"Monday, Wednesday, Friday"))

    status = Instantiator('cv.Status').build
    yield status(**dd.str2kw('name', _("Worker")))
    yield status(**dd.str2kw('name', _("Employee")))
    yield status(**dd.str2kw('name', _("Freelancer")))
    yield status(**dd.str2kw('name', _("Voluntary")))
    yield status(**dd.str2kw('name', _("Student")))
    yield status(**dd.str2kw('name', _("Laboratory")))  # fr=Stage,
                                                        # de=Praktikum
    yield status(**dd.str2kw('name', _("Interim")))

