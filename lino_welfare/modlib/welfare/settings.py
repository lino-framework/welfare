# -*- coding: UTF-8 -*-
# Copyright 2009-2018 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

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

    demo_fixtures = """std std2 few_languages demo
    demo2 cbss checkdata""".split()

    languages = 'en fr de nl'
    hidden_languages = 'nl'

    migration_class = 'lino_welfare.migrate.Migrator'
    project_model = 'pcsw.Client'

    # ~ catch_layout_exceptions = False # 20130804

    userdocs_prefix = 'welfare.'
    auto_configure_logger_names = 'atelier schedule django lino lino_xl lino_cosi lino_welfare'
    # use_java = False  # temporarily
    # verbose_client_info_message = True


    # default_ui = "lino_react.react" # does not yet work because "Tried to get
    # static handle for debts.PrintEntriesByBudget"

    # default_build_method = "appyodt"
    default_build_method = "appypdf"
    uppercase_last_name = True

    user_types_module = 'lino_welfare.modlib.welfare.user_types'
    # workflows_module = 'lino_xl.lib.reception.workflows'
    workflows_module = 'lino_welfare.modlib.welfare.workflows'

    # def setup_plugins(self):
    #     """
    #     Change the default value of certain plugin settings.
    #
    #     - :attr:`lino_xl.lib.ledger.Plugin.ref_length` = 5
    #
    #     - :attr:`excerpts.responsible_user
    #       <lino_xl.lib.excerpts.Plugin.responsible_user>` is set to
    #       ``'melanie'``.
    #
    #     """
    #     super(Site, self).setup_plugins()
    #     self.plugins.clients.configure(client_model='pcsw.Client')
    #     self.plugins.addresses.configure(partner_model='contacts.Partner')
    #     self.plugins.excerpts.configure(responsible_user='melanie')
    #     # self.plugins.extjs.configure(enter_submits_form=True)
    #
    #     if 'ledger' in self.plugins:
    #         self.plugins.ledger.configure(ref_length=16)
    #         self.plugins.ledger.configure(project_model='pcsw.Client')
    #     # self.plugins.humanlinks.configure(person_model='pcsw.Client')
    #     # self.plugins.households.configure(person_model='pcsw.Client')

    def get_plugin_configs(self):
        yield super(Site, self).get_plugin_configs()
        yield ('clients', 'client_model', 'pcsw.Client')
        yield ('clients', 'demo_coach', 'hubert')
        yield ('addresses', 'partner_model', 'contacts.Partner')
        yield ('excerpts', 'responsible_user', 'melanie')
        # if 'ledger' in self.plugins:
        yield ('ledger', 'ref_length', 16)
        yield ('ledger', 'project_model', 'pcsw.Client')
        yield ('cal', 'mytasks_start_date', -30)

    def setup_quicklinks(self, user, tb):
        # tb.add_action(self.modules.pcsw.Clients.detail_action)

        super(Site, self).setup_quicklinks(user, tb)

        tb.add_action(self.modules.pcsw.Clients, 'find_by_beid')
        tb.add_action(self.modules.integ.Clients)
        tb.add_action(self.modules.isip.MyContracts)
        tb.add_action(self.modules.jobs.MyContracts)
        tb.add_action(self.modules.cal.EntriesByDay)

    def get_installed_apps(self):
        yield super(Site, self).get_installed_apps()

        yield 'lino_welfare.modlib.system'
        yield 'lino_xl.lib.statbel.countries'
        yield 'lino_welfare.modlib.contacts'

        # yield 'lino.modlib.gfks'
        yield 'lino_xl.lib.appypod'
        yield 'django.contrib.humanize'  # translations for
        yield 'lino_welfare.modlib.users'
        yield 'lino.modlib.notify'
        yield 'lino.modlib.changes'

        yield 'lino_xl.lib.properties'
        yield 'lino_xl.lib.addresses'

        yield 'lino_xl.lib.excerpts'

        yield 'lino_xl.lib.uploads'
        yield 'lino_xl.lib.outbox'

        if self.default_ui == "lino.modlib.extjs":
            yield 'lino_xl.lib.extensible'
            yield 'lino_welfare.modlib.cal'
        else:
            yield 'lino_welfare.modlib.cal'
            yield 'lino_xl.lib.calview'

        yield 'lino_welfare.modlib.reception'
        yield 'lino_welfare.modlib.badges'
        yield 'lino_xl.lib.boards'

        yield 'lino_welfare.modlib.pcsw'
        # yield 'lino_xl.lib.clients'
        # yield 'lino_xl.lib.coachings'
        yield 'lino_welfare.modlib.welfare'

        # NOTE: ordering influences (1) main menu (2) fixtures loading
        # e.g. pcsw.demo creates clients needed by cbss.demo
        yield 'lino_welfare.modlib.sales'
        # yield 'lino_welfare.modlib.pcsw'
        yield 'lino_welfare.modlib.ledger'
        yield 'lino_welfare.modlib.sepa'
        yield 'lino_xl.lib.b2c'
        yield 'lino_welfare.modlib.finan'
        # yield 'lino_xl.lib.bevats'

        # yield 'lino_xl.lib.ledger'
        yield 'lino_xl.lib.vatless'
        if False:  # not sure whether they make sense
            yield 'lino_welfare.modlib.client_vouchers'
        # yield 'lino_xl.lib.finan'

        yield 'lino_welfare.chatelet.lib.cv'
        yield 'lino_welfare.modlib.integ'
        yield 'lino_welfare.modlib.isip'
        yield 'lino_welfare.modlib.jobs'
        yield 'lino_welfare.modlib.art61'
        yield 'lino_welfare.modlib.immersion'
        yield 'lino_welfare.modlib.active_job_search'
        yield 'lino_welfare.chatelet.lib.courses'
        yield 'lino_welfare.modlib.xcourses'
        yield 'lino_welfare.modlib.newcomers'
        yield 'lino_welfare.modlib.cbss'  # must come after pcsw
        yield 'lino_welfare.modlib.households'  # must come after pcsw
        yield 'lino_xl.lib.humanlinks'  # must come after households
        yield 'lino_welfare.modlib.debts'  # must come after households
        # The `notes` demo fixture creates Notes for Clients.
        yield 'lino_welfare.modlib.notes'
        yield 'lino_welfare.modlib.aids'
        # yield 'lino_welfare.modlib.projects'
        yield 'lino_welfare.modlib.polls'
        yield 'lino_welfare.modlib.esf'

        yield 'lino_xl.lib.beid'
        # yield 'lino.modlib.davlink'
        yield 'lino.modlib.dashboard'

        yield 'lino.modlib.export_excel'
        yield 'lino_welfare.modlib.dupable_clients'
        yield 'lino.modlib.checkdata'
        if self.default_ui == "lino.modlib.extjs":
            yield 'lino.modlib.tinymce'

    def get_dashboard_items(self, user):
        """Returns the items of the admin index page:

        - :class:`lino_welfare.modlib.integ.models.UsersWithClients`
        - :class:`lino_welfare.modlib.reception.models.MyWaitingVisitors`
        - :class:`lino_xl.lib.cal.MyEntries`
        - :class:`lino_xl.lib.cal.MyTasks`
        - ...


        """
        if user.is_authenticated:
            yield self.modules.integ.UsersWithClients
            yield self.modules.reception.MyWaitingVisitors
            yield self.modules.reception.WaitingVisitors
            yield self.modules.cal.MyEntries
            yield self.modules.cal.MyTasks
            yield self.models.cal.MyOverdueAppointments
            #~ yield self.modules.reception.ReceivedVisitors
            yield self.models.notify.MyMessages
