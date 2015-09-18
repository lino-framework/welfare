# -*- coding: UTF-8 -*-
# Copyright 2009-2015 Luc Saffre
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

"""Default settings of a :ref:`welfare` project.

"""

from lino.projects.std.settings import *
from django.utils.translation import ugettext_lazy as _
import lino_welfare


class Site(Site):
    """
    The base class for all Lino Welfare applications.
    """

    verbose_name = _("Lino Welfare")

    version = lino_welfare.SETUP_INFO['version']
    url = lino_welfare.SETUP_INFO['url']

    demo_fixtures = """std std2 few_languages props demo
    demo2 cbss demo_events checkdata""".split()

    languages = 'en fr de nl'
    hidden_languages = 'nl'

    migration_class = 'lino_welfare.migrate.Migrator'
    project_model = 'pcsw.Client'

    # ~ catch_layout_exceptions = False # 20130804

    userdocs_prefix = 'welfare.'
    auto_configure_logger_names = 'lino lino_welfare'
    # use_java = False  # temporarily
    # verbose_client_info_message = True
    # default_build_method = "appyodt"
    uppercase_last_name = True

    user_profiles_module = 'lino_welfare.modlib.welfare.roles'

    def setup_plugins(self):
        """
        Change the default value of certain plugin settings.

        - :attr:`lino.modlib.accounts.Plugin.ref_length` = 5
        
        - :attr:`excerpts.responsible_user
          <lino.modlib.excerpts.Plugin.responsible_user>` is set to
          ``'melanie'``.

        """
        super(Site, self).setup_plugins()
        self.plugins.accounts.configure(ref_length=16)
        self.plugins.excerpts.configure(responsible_user='melanie')

        if 'ledger' in self.plugins:
            self.plugins.ledger.configure(project_model='pcsw.Client')
        # self.plugins.humanlinks.configure(person_model='pcsw.Client')
        # self.plugins.households.configure(person_model='pcsw.Client')

    def setup_choicelists(self):
        """Adds two shortcut fields and a special note type."""

        super(Site, self).setup_choicelists()

        from django.utils.translation import ugettext_lazy as _
        from lino.modlib.excerpts.choicelists import Shortcuts
        Shortcuts.add_item('pcsw.Client', 'cvs_emitted', _("CVs emitted"))

        from lino.modlib.uploads.choicelists import add_shortcut as add
        add('pcsw.Client', 'id_document', _("Identifying document"),
            target='uploads.UploadsByClient')
        # from lino.modlib.uploads.choicelists import Shortcuts
        # Shortcuts.add_item(
        #     'pcsw.Client', 'id_document', _("Identifying document"),
        #     target='uploads.UploadsByClient')

        from lino.modlib.notes.choicelists import SpecialTypes
        add = SpecialTypes.add_item
        add('100', _("First meeting"), 'first_meeting')

    def setup_quicklinks(self, ar, tb):
        # tb.add_action(self.modules.pcsw.Clients.detail_action)

        super(Site, self).setup_quicklinks(ar, tb)

        tb.add_action(self.modules.pcsw.Clients, 'find_by_beid')
        tb.add_action(self.modules.integ.Clients)
        tb.add_action(self.modules.isip.MyContracts)
        tb.add_action(self.modules.jobs.MyContracts)
        tb.add_action(self.modules.cal.EventsByDay)

    def get_installed_apps(self):
        yield super(Site, self).get_installed_apps()

        yield 'lino_welfare.modlib.system'
        yield 'lino.modlib.gfks'
        yield 'django.contrib.humanize'  # translations for
        yield 'lino_welfare.modlib.users'
        yield 'lino.modlib.changes'
        yield 'lino.modlib.statbel.countries'

        yield 'lino.modlib.properties'
        yield 'lino_welfare.modlib.contacts'
        yield 'lino.modlib.addresses'

        yield 'lino_welfare.modlib.uploads'
        yield 'lino.modlib.outbox'
        yield 'lino.modlib.excerpts'

        yield 'lino.modlib.extensible'
        yield 'lino_welfare.modlib.cal'
        yield 'lino_welfare.modlib.reception'
        yield 'lino.modlib.accounts'
        yield 'lino_welfare.modlib.badges'
        yield 'lino_welfare.modlib.sepa'

        yield 'lino.modlib.boards'

        if False:  # not yet ready
            yield 'lino.modlib.families'

        yield 'lino_welfare.modlib.welfare'

        # NOTE: ordering influences (1) main menu (2) fixtures loading
        # e.g. pcsw.demo creates clients needed by cbss.demo
        yield 'lino_welfare.modlib.sales'
        yield 'lino_welfare.modlib.pcsw'

        yield 'lino_welfare.modlib.ledger'
        # yield 'lino_welfare.modlib.finan'
        # yield 'lino.modlib.ledger'
        yield 'lino.modlib.vatless'
        if False:  # not sure whether they make sense
            yield 'lino_welfare.modlib.client_vouchers'
        yield 'lino.modlib.finan'

        yield 'lino_welfare.projects.chatelet.modlib.cv'
        yield 'lino_welfare.modlib.integ'
        yield 'lino_welfare.modlib.isip'
        yield 'lino_welfare.modlib.jobs'
        yield 'lino_welfare.modlib.art61'
        yield 'lino_welfare.modlib.immersion'
        yield 'lino_welfare.modlib.active_job_search'
        # chatelet replaces courses by
        yield 'lino_welfare.modlib.courses'
        yield 'lino_welfare.modlib.newcomers'
        yield 'lino_welfare.modlib.cbss'  # must come after pcsw
        yield 'lino_welfare.modlib.households'  # must come after pcsw
        yield 'lino.modlib.humanlinks'  # must come after households
        yield 'lino_welfare.modlib.debts'  # must come after households
        # The `notes` demo fixture creates Notes for Clients.
        yield 'lino_welfare.modlib.notes'
        yield 'lino_welfare.modlib.aids'
        # yield 'lino_welfare.modlib.projects'
        yield 'lino_welfare.modlib.polls'

        yield 'lino.modlib.beid'
        yield 'lino.modlib.davlink'

        yield 'lino.modlib.export_excel'
        yield 'lino_welfare.modlib.dupable_clients'
        yield 'lino.modlib.plausibility'
        yield 'lino.modlib.tinymce'

    def get_admin_main_items(self, ar):
        """Returns the items of the admin index page:

        - :class:`lino_welfare.modlib.integ.models.UsersWithClients`
        - :class:`lino_welfare.modlib.reception.models.MyWaitingVisitors`
        - :class:`lino.modlib.cal.models.MyEvents`
        - :class:`lino.modlib.cal.models.MyTasks`
        - ...


        """
        yield self.modules.integ.UsersWithClients
        yield self.modules.reception.MyWaitingVisitors
        yield self.modules.cal.MyEvents
        yield self.modules.cal.MyTasks
        yield self.modules.reception.WaitingVisitors
        #~ yield self.modules.reception.ReceivedVisitors
