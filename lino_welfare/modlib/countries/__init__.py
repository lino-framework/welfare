# -*- coding: UTF-8 -*-
# Copyright 2015 Luc Saffre
# License: BSD (see file COPYING for details)
"""Inherits from :mod:`lino.modlib.countries`, adding 
:mod:`lino.modlib.statbel`.
"""

from lino.modlib.countries import *


class Plugin(Plugin):
    needs_plugins = ['lino.modlib.statbel']
