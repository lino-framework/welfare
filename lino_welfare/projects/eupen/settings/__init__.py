# -*- coding: UTF-8 -*-
# Copyright 2014 Luc Saffre
# This file is part of the Lino project.
# Lino is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
# Lino is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with Lino; if not, see <http://www.gnu.org/licenses/>.

"""
The settings.py used for building both `/docs` and `/userdocs`
"""

from __future__ import print_function
from __future__ import unicode_literals

from lino_welfare.projects.base import *

class Site(Site):

    title = "Lino für ÖSHZ"
    languages = 'de fr nl'  # tested docs rely on this distribution
    hidden_languages = None
    uppercase_last_name = True

    demo_fixtures = """std few_languages props all_countries
    demo cbss mini demo2 local """.split()

    def get_default_language(self):
        return 'de'

    def get_apps_modifiers(self, **kw):
        kw = super(Site, self).get_apps_modifiers(**kw)
        kw.update(badges=None)  # remove the badges app
        return kw

# the following line should not be active in a checked-in version
#~ DATABASES['default']['NAME'] = ':memory:'
