# -*- coding: UTF-8 -*-
# Copyright 2014-2018 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

from lino.projects.std.settings import *
# from lino_welfare.modlib.welfare.settings import *
from lino.api import _
import lino_welfare


class Site(Site):

    verbose_name = _("Lino Welfare")

    version = lino_welfare.SETUP_INFO['version']
    url = lino_welfare.SETUP_INFO['url']

    hidden_languages = 'nl'
    project_model = 'pcsw.Client'
    # catch_layout_exceptions = False # 20130804

    userdocs_prefix = 'welfare.'
    auto_configure_logger_names = 'atelier schedule django lino lino_xl lino_cosi lino_welfare'
    # use_java = False  # temporarily
    # verbose_client_info_message = True
    # default_build_method = "appyodt"
    default_build_method = "appypdf"
    uppercase_last_name = True
    user_types_module = 'lino_welfare.modlib.welfare.user_types'
    # workflows_module = 'lino_xl.lib.reception.workflows'
    workflows_module = 'lino_welfare.chatelet.workflows'

    # verbose_name = "Lino pour CPAS"
    languages = "fr nl de en"
    # hidden_languages = None

    # strict_choicelist_values = False

    demo_fixtures = """std std2 few_languages all_countries
    demo cbss demo2 checksummaries""".split()

    migration_class = 'lino_welfare.chatelet.migrate.Migrator'
    custom_layouts_module = 'lino_welfare.chatelet.layouts'

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
        yield 'lino_xl.lib.addresses'
        yield 'lino_xl.lib.excerpts'
        yield 'lino_xl.lib.uploads'
        yield 'lino_xl.lib.outbox'
        yield 'lino_xl.lib.extensible'
        yield 'lino_welfare.modlib.cal'
        yield 'lino_welfare.modlib.reception'
        yield 'lino_welfare.modlib.badges'
        yield 'lino_xl.lib.boards'

        yield 'lino_welfare.chatelet.lib.pcsw'
        # yield 'lino_xl.lib.clients'
        # yield 'lino_xl.lib.coachings'
        yield 'lino_welfare.modlib.welfare'

        # NOTE: ordering influences (1) main menu (2) fixtures loading
        # e.g. pcsw.demo creates clients needed by cbss.demo
        yield 'lino_welfare.modlib.sales'
        # yield 'lino_welfare.modlib.pcsw'
        # yield 'lino_welfare.modlib.ledger'

        yield 'lino_welfare.chatelet.lib.cv'
        yield 'lino_welfare.modlib.integ'
        yield 'lino_welfare.chatelet.lib.isip'
        yield 'lino_welfare.modlib.jobs'
        yield 'lino_welfare.modlib.art61'
        yield 'lino_welfare.modlib.immersion'
        yield 'lino_welfare.modlib.active_job_search'
        yield 'lino_welfare.chatelet.lib.courses'
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
        # yield 'lino_welfare.modlib.dupable_clients'
        yield 'lino.modlib.checkdata'
        yield 'lino.modlib.tinymce'

    def setup_plugins(self):
        """
        Change the default value of certain plugin settings.

        - :attr:`lino_xl.lib.ledger.Plugin.ref_length` = 5

        - :attr:`excerpts.responsible_user
          <lino_xl.lib.excerpts.Plugin.responsible_user>` is set to
          ``'melanie'``.

        """
        super(Site, self).setup_plugins()
        self.plugins.clients.configure(client_model='pcsw.Client')
        self.plugins.addresses.configure(partner_model='contacts.Partner')
        self.plugins.excerpts.configure(responsible_user='melanie')
        # self.plugins.extjs.configure(enter_submits_form=True)
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


    def setup_quicklinks(self, user, tb):
        # tb.add_action(self.modules.pcsw.Clients.detail_action)

        super(Site, self).setup_quicklinks(user, tb)

        tb.add_action(self.modules.pcsw.Clients, 'find_by_beid')
        tb.add_action(self.modules.integ.Clients)
        tb.add_action(self.modules.isip.MyContracts)
        tb.add_action(self.modules.jobs.MyContracts)
        tb.add_action(self.modules.cal.EntriesByDay)

