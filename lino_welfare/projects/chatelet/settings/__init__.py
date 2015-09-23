# -*- coding: UTF-8 -*-
# Copyright 2008-2015 Luc Saffre
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

    demo_fixtures = """std std2 few_languages props all_countries
    demo cbss mini demo2 local""".split()

    migration_class = 'lino_welfare.projects.chatelet.migrate.Migrator'

    def get_apps_modifiers(self, **kw):
        kw = super(Site, self).get_apps_modifiers(**kw)
        # remove whole plugin:
        kw.update(finan=None)
        kw.update(ledger=None)
        kw.update(vatless=None)
        kw.update(debts=None)
        # kw.update(aids=None)
        kw.update(sepa=None)
        # kw.update(badges=None)
        kw.update(properties=None)
        kw.update(dupable_clients=None)
        # alternative implementations:
        kw.update(courses='lino_welfare.projects.chatelet.modlib.courses')
        kw.update(pcsw='lino_welfare.projects.chatelet.modlib.pcsw')
        kw.update(isip='lino_welfare.projects.chatelet.modlib.isip')
        return kw

    # def setup_plugins(self):
    #     """
    #     Change the default value of certain plugin settings.

    #     """
    #     self.plugins.courses.configure(pupil_model='pcsw.Client')
    #     # self.plugins.courses.configure(teacher_model='users.User')
    #     super(Site, self).setup_plugins()

    # def get_default_language(self):
    #     return 'fr'

    def get_admin_main_items(self, ar):

        # Mathieu: je remarque que le module "Visiteurs qui
        # m'attendent" ne fonctionne plus. Hors, c'est surtout ce
        # système qui est intéressant pour les travailleurs sociaux
        # qui attendent leurs rdv ou qui tiennent des permanences.

        yield self.modules.reception.MyWaitingVisitors
        yield self.modules.cal.MyEvents
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

        # from lino.utils.sendchanges import register, subscribe
        # e = register('notes.Note', 'subject body',
        #              update_tpl='note_updated.eml')
        # e.updated_subject = "Changement dans {obj}"
        # subscribe('john.doe@example.org')

        # from lino.core.signals import receiver, on_ui_updated

        # def immersion_template(obj, bm):
        #     # Use a custom template for immersion trainings with
        #     # external partner.

        #     if bm.template_ext != '.odt':
        #         raise Exception("Not supported")
        #     if obj.company is None:
        #         return "Default.odt"
        #     return "StageForem.odt"

        # self.plugins.excerpts.register_default_template_handler(
        #     self.modules.immersion.Contract, immersion_template)


# the following line should not be active in a checked-in version
#~ DATABASES['default']['NAME'] = ':memory:'
