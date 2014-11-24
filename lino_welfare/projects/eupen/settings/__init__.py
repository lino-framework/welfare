# -*- coding: UTF-8 -*-
# Copyright 2014 Luc Saffre
# License: BSD (see file COPYING for details)

from __future__ import print_function
from __future__ import unicode_literals

from lino_welfare.projects.base import *

class Site(Site):

    title = "Lino für ÖSHZ"
    languages = 'de fr nl'  # tested docs rely on this distribution
    hidden_languages = None
    uppercase_last_name = True
    help_url = "http://de.welfare.lino-framework.org"

    demo_fixtures = """std few_languages props all_countries
    demo cbss mini demo2 local """.split()

    def get_default_language(self):
        return 'de'

    def get_apps_modifiers(self, **kw):
        kw = super(Site, self).get_apps_modifiers(**kw)
        kw.update(badges=None)  # remove the badges app
        kw.update(polls=None)
        kw.update(projects=None)
        kw.update(pcsw='lino_welfare.projects.eupen.modlib.pcsw')
        return kw

    def get_admin_main_items(self):
        yield self.modules.integ.UsersWithClients
        yield self.modules.reception.MyWaitingVisitors
        yield self.modules.cal.MyEvents
        yield self.modules.cal.MyTasks
        yield self.modules.reception.WaitingVisitors
        #~ yield self.modules.reception.ReceivedVisitors


# the following line should not be active in a checked-in version
#~ DATABASES['default']['NAME'] = ':memory:'
