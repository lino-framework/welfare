# -*- coding: UTF-8 -*-
# Copyright 2012-2013 Luc Saffre
# License: BSD (see file COPYING for details)

"""
Loads all cbss specific default data.
"""

from lino_welfare.modlib.cbss.fixtures import sectors, purposes
from lino.modlib.statbel.fixtures import inscodes


def objects():
    yield sectors.objects()
    yield purposes.objects()
    yield inscodes.objects()
