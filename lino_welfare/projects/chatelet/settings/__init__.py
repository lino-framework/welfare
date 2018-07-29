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

from lino_welfare.modlib.welfare.settings import *
from lino.api import _


class Site(Site):

    # verbose_name = "Lino pour CPAS"
    languages = "fr nl de en"
    # hidden_languages = None

    # strict_choicelist_values = False

    demo_fixtures = """std std2 few_languages all_countries
    demo cbss demo2 checksummaries""".split()

    migration_class = 'lino_welfare.projects.chatelet.migrate.Migrator'
    
    # custom_layouts_module = 'lino_welfare.projects.chatelet.layouts'

    def get_apps_modifiers(self, **kw):
        kw = super(Site, self).get_apps_modifiers(**kw)
        # remove whole plugin:
        kw.update(finan=None)
        kw.update(ledger=None)
        kw.update(vatless=None)
        # kw.update(tinymce=None)
        # kw.update(debts=None)
        # kw.update(aids=None)
        kw.update(sepa=None)
        kw.update(b2c=None)
        kw.update(xcourses=None)
        kw.update(courses='lino_welfare.projects.chatelet.modlib.courses')
        # kw.update(badges=None)
        kw.update(properties=None)
        kw.update(dupable_clients=None)
        # alternative implementations:
        kw.update(pcsw='lino_welfare.projects.chatelet.modlib.pcsw')
        kw.update(isip='lino_welfare.projects.chatelet.modlib.isip')
        return kw

    # def get_installed_apps(self):
    #     yield super(Site, self).get_installed_apps()
    #     yield 'lino_welfare.projects.chatelet.modlib.courses'
        
    def setup_plugins(self):
        """
        Change the default value of certain plugin settings.

        """
        super(Site, self).setup_plugins()
        self.plugins.integ.configure(only_primary=True)

    # def get_default_language(self):
    #     return 'fr'

    def get_dashboard_items(self, user):
        """Defines the items to show in :xfile:`admin_main.html`.
        See :meth:`lino.core.site.Site.get_dashboard_items`.
        """

        # "Visiteurs qui m'attendent" est intéressant pour les
        # travailleurs sociaux qui attendent leurs rdv ou qui tiennent
        # des permanences.

        yield self.models.reception.MyWaitingVisitors
        yield self.models.cal.MyUnconfirmedAppointments
        yield self.models.cal.MyEntriesToday
        yield self.models.cal.MyTasks
        yield self.models.cal.DailyPlanner
        
        yield self.models.reception.WaitingVisitors
        # yield self.models.integ.UsersWithClients
        #~ yield self.models.reception.ReceivedVisitors
        yield self.models.cal.MyOverdueAppointments
        
        if user.authenticated:
            yield self.models.notify.MyMessages
            

    def do_site_startup(self):
        super(Site, self).do_site_startup()

        from lino.core.inject import update_field
        # ctt = self.models.clients.ClientContactTypes
        ct = self.models.clients.ClientContact
        ct.column_names = "company contact_person remark"
        update_field(ct, 'remark', verbose_name=_("Contact details"))

        from lino.utils.watch import watch_changes as wc

        wc(self.models.contacts.Partner)
        wc(self.models.contacts.Person, master_key='partner_ptr')
        wc(self.models.contacts.Company, master_key='partner_ptr')
        wc(self.models.pcsw.Client, master_key='partner_ptr')

        wc(self.models.coachings.Coaching, master_key='client__partner_ptr')
        wc(self.models.clients.ClientContact, master_key='client__partner_ptr')


# the following line should not be active in a checked-in version
#~ DATABASES['default']['NAME'] = ':memory:'
