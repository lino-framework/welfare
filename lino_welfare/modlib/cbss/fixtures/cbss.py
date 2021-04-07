# -*- coding: UTF-8 -*-
# Copyright 2012-2015 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

"""
Loads all cbss specific default data.
"""

from lino_welfare.modlib.cbss.fixtures import sectors, purposes
from lino_welfare.modlib.cbss.fixtures import cbss_demo, democfg
from lino_xl.lib.statbel.countries.fixtures import inscodes


def objects():
    yield sectors.objects()
    yield purposes.objects()
    yield inscodes.objects()
    yield democfg.objects()
    yield cbss_demo.objects()
