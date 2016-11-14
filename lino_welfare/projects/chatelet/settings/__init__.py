# -*- coding: UTF-8 -*-
# Copyright 2008-2016 Luc Saffre
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

"""
The settings.py used for building both `/docs` and `/userdocs`
"""

from lino_welfare.projects.std.settings import *


class Site(Site):

    # verbose_name = "Lino pour CPAS"
    languages = "fr nl de en"
    # hidden_languages = None

    # strict_choicelist_values = False

    demo_fixtures = """std std2 few_languages all_countries
    demo cbss demo2 checksummaries""".split()

    migration_class = 'lino_welfare.projects.chatelet.migrate.Migrator'

    def get_apps_modifiers(self, **kw):
        kw = super(Site, self).get_apps_modifiers(**kw)
        # remove whole plugin:
        kw.update(finan=None)
        kw.update(ledger=None)
        kw.update(vatless=None)
        # kw.update(debts=None)
        # kw.update(aids=None)
        kw.update(sepa=None)
        kw.update(b2c=None)
        # kw.update(badges=None)
        kw.update(properties=None)
        kw.update(dupable_clients=None)
        # alternative implementations:
        kw.update(courses='lino_welfare.projects.chatelet.modlib.courses')
        kw.update(pcsw='lino_welfare.projects.chatelet.modlib.pcsw')
        kw.update(isip='lino_welfare.projects.chatelet.modlib.isip')
        return kw

    def setup_plugins(self):
        """
        Change the default value of certain plugin settings.

        """
        super(Site, self).setup_plugins()
        self.plugins.integ.configure(only_primary=True)

    # def get_default_language(self):
    #     return 'fr'

    def get_admin_main_items(self, ar):
        """Defines the items to show in :xfile:`admin_main.html`.
        See :meth:`lino.core.site.Site.get_admin_main_items`.
        """

        # "Visiteurs qui m'attendent" est intéressant pour les
        # travailleurs sociaux qui attendent leurs rdv ou qui tiennent
        # des permanences.

        if ar.get_user().authenticated:
            yield self.actors.notify.MyMessages
            
        yield self.modules.reception.MyWaitingVisitors
        yield self.modules.cal.MyEventsToday
        yield self.modules.cal.MyTasks
        
        yield self.modules.reception.WaitingVisitors
        # yield self.modules.integ.UsersWithClients
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


# the following line should not be active in a checked-in version
#~ DATABASES['default']['NAME'] = ':memory:'
