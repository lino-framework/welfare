# -*- coding: UTF-8 -*-
# Copyright 2016 Luc Saffre
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
"""Main settings module for `lino_welfare.projects.eupen`.
"""

from __future__ import print_function
from __future__ import unicode_literals

from lino_welfare.projects.eupen.settings import *


class Site(Site):

    languages = 'de fr'
    hidden_languages = None
    help_url = "http://de.welfare.lino-framework.org"

    demo_fixtures = ["std"]

    def setup_plugins(self):
        super(Site, self).setup_plugins()
        self.plugins.tim2lino.languages = "de fr"
        self.plugins.ledger.fix_y2k = True
        self.plugins.ledger.start_year = 1994

    def get_installed_apps(self):
        yield super(Site, self).get_installed_apps()
        yield 'lino_xl.lib.tim2lino'


# the following line should not be active in a checked-in version
#~ DATABASES['default']['NAME'] = ':memory:'
