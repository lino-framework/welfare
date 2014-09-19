# -*- coding: UTF-8 -*-
# Copyright 2013-2014 Luc Saffre
# License: BSD (see file COPYING for details)

from lino import dd


class SectorFunction(dd.Model):

    """
    Abstract base for models that refer to a
    :class:`jobs.Sector` and a :class:`jobs.Function`.
    """
    class Meta:
        abstract = True

    sector = dd.ForeignKey("jobs.Sector", blank=True, null=True)
    function = dd.ForeignKey("jobs.Function", blank=True, null=True)

    @dd.chooser()
    def function_choices(cls, sector):
        if sector is None:
            return dd.modules.jobs.Function.objects.all()
        return sector.function_set.all()

