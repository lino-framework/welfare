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

    sector = dd.ForeignKey("jobs.Sector",
                           blank=True, null=True)
    function = dd.ForeignKey("jobs.Function",
                             blank=True, null=True)

    @dd.chooser()
    def function_choices(cls, sector):
        Function = dd.modules.jobs.Function
        if sector is not None:
            return sector.function_set.all()
        return Function.objects.all()


