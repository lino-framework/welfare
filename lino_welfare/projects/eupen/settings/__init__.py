# -*- coding: UTF-8 -*-
# Copyright 2014 Luc Saffre
# License: BSD (see file COPYING for details)

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
        kw.update(pcsw='lino_welfare.projects.eupen.modlib.pcsw')
        return kw

# the following line should not be active in a checked-in version
#~ DATABASES['default']['NAME'] = ':memory:'
