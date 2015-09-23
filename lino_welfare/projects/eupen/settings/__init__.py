# -*- coding: UTF-8 -*-
# Copyright 2014-2015 Luc Saffre
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

from lino_welfare.projects.std.settings import *

# configure_plugin('beid', read_only_simulate=True)


class Site(Site):

    languages = 'de fr en'
    hidden_languages = None
    help_url = "http://de.welfare.lino-framework.org"

    demo_fixtures = """std welfare_std std2 few_languages props all_countries
    demo mini demo2 welfare_demo cbss checkdata local""".split()

    def get_default_language(self):
        return 'de'

    def get_apps_modifiers(self, **kw):
        kw = super(Site, self).get_apps_modifiers(**kw)
        kw.update(badges=None)  # remove the badges app
        kw.update(polls=None)
        # kw.update(projects=None)
        kw.update(immersion=None)
        # kw.update(ledger=None)
        # kw.update(finan=None)
        # kw.update(vatless=None)
        kw.update(active_job_search=None)
        kw.update(pcsw='lino_welfare.projects.eupen.modlib.pcsw')
        kw.update(cv='lino_welfare.modlib.cv')
        return kw

    def get_admin_main_items(self, ar):
        yield self.modules.integ.UsersWithClients
        yield self.modules.reception.MyWaitingVisitors
        yield self.modules.cal.MyEvents
        yield self.modules.cal.MyTasks
        yield self.modules.reception.WaitingVisitors
        #~ yield self.modules.reception.ReceivedVisitors

    def do_site_startup(self):
        super(Site, self).do_site_startup()

        from lino.modlib.changes.models import watch_changes as wc

        wc(self.modules.contacts.Partner)
        wc(self.modules.contacts.Person, master_key='partner_ptr')
        wc(self.modules.contacts.Company, master_key='partner_ptr')
        wc(self.modules.pcsw.Client, master_key='partner_ptr')

        wc(self.modules.pcsw.Coaching, master_key='client__partner_ptr')
        wc(self.modules.pcsw.ClientContact, master_key='client__partner_ptr')
        wc(self.modules.jobs.Candidature, master_key='person__partner_ptr')

        # ContractBase is abstract, so it's not under self.modules
        from lino_welfare.modlib.isip.models import ContractBase
        wc(ContractBase, master_key='client__partner_ptr')

        from lino_welfare.modlib.cbss.models import CBSSRequest
        wc(CBSSRequest, master_key='person__partner_ptr')


# the following line should not be active in a checked-in version
#~ DATABASES['default']['NAME'] = ':memory:'
