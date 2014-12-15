# -*- coding: UTF-8 -*-
# Copyright 2009-2014 Luc Saffre
# License: BSD (see file COPYING for details)

"""
Default settings of a :ref:`welfare` site.

"""
import datetime

from lino.projects.std.settings import *
from lino_welfare import SETUP_INFO


class Site(Site):

    """
    The base class for all Lino Welfare sites.
    """
    version = SETUP_INFO['version']  # lino_welfare.__version__
    url = SETUP_INFO['url']  # "http://code.google.com/p/lino-welfare/"
    uppercase_last_name = True

    # use_java = False  # temporarily

    verbose_name = "Lino Welfare"

    demo_fixtures = """std few_languages props demo cbss
    democfg cbss_demo demo2 demo_events""".split()

    # ~ catch_layout_exceptions = False # 20130804

    migration_class = 'lino_welfare.migrate.Migrator'

    userdocs_prefix = 'welfare.'
    auto_configure_logger_names = 'djangosite lino lino_welfare'

    project_model = 'pcsw.Client'
    user_model = 'users.User'

    # verbose_client_info_message = True

    languages = 'en fr de nl'  # tested docs rely on this distribution
    hidden_languages = 'nl'

    # def get_default_language(self):
    #     """The default returns German which is statistically not correct, but
    #     Lino Welfare was born in the German-speaking region, and quite
    #     some test cases rely on this default setting.

    #     """
    #     return 'de'

    #~ index_view_action = "pcsw.Home"

    #~ remote_user_header = "REMOTE_USER"

    #~ admin_url = '/admin'

    def setup_plugins(self):
        """
        Change the default value of certain plugin settings.

        - :setting:`accounts.ref_length` = 5
        - (no longer) :setting:`humanlinks.human_model` = 'pcsw.Client'
        
        """
        self.plugins.accounts.configure(ref_length=5)
        # self.plugins.humanlinks.configure(person_model='pcsw.Client')
        # self.plugins.households.configure(person_model='pcsw.Client')
        super(Site, self).setup_plugins()

    def setup_choicelists(self):
        """
        This defines default user profiles for :ref:`welfare`.
        """
        from django.utils.translation import ugettext_lazy as _
        from lino.modlib.users.mixins import UserProfiles

        UserProfiles.reset(
            '* office coaching integ courses cbss newcomers debts '
            'reception beid')
        add = UserProfiles.add_item
        add('000', _("Anonymous"),                   '_ _ _ _ _ _ _ _ _ _',
            name='anonymous',
            readonly=True,
            authenticated=False)
        add('100', _("Integration Agent"),           'U U U U U U _ _ _ U')
        add('110', _("Integration Agent (Manager)"), 'U M M M M U _ _ _ U')
        add('200', _("Newcomers consultant"),        'U U U _ _ U U _ _ U')
        add('210', _("Reception clerk"),             'U U _ _ _ _ _ _ U U')
        add('300', _("Debts consultant"),            'U U U _ _ _ _ U _ U')
        add('400', _("Social agent"),                'U U U _ U U _ _ _ U')
        add('410', _("Social agent (Manager)"),      'U M M _ M U _ _ _ U')
        add('900', _("Administrator"),               'A A A A A A A A A U',
            name='admin')

    def setup_quicklinks(self, ar, tb):
        #~ tb.add_action(self.modules.contacts.Persons().detail)
        #~ tb.add_action(self.modules.contacts.Persons,'detail')
        #~ tb.add_action(self.modules.contacts.Persons,'detail')
        #~ tb.add_action(self.modules.pcsw.Clients.detail_action)
        tb.add_action('pcsw.Clients', 'detail')
        self.on_each_app('setup_quicklinks', ar, tb)

        tb.add_action(self.modules.integ.Clients)
        tb.add_action(self.modules.isip.MyContracts)
        tb.add_action(self.modules.jobs.MyContracts)
        tb.add_action(self.modules.cal.EventsByDay)

    def setup_menu(self, ui, profile, main):
        from django.utils.translation import ugettext_lazy as _
        from django.utils.translation import string_concat
        from django.db import models
        from lino import dd, rt
        contacts = dd.resolve_app("contacts")

        #~ m = main.add_menu("contacts",_("Contacts"))
        #~ m = main.add_menu("contacts",contacts.MODULE_LABEL)
        #~ m.add_action(self.modules.pcsw.Clients)

        #~ if user.profile.level:
            #~ m.add_action(self.modules.contacts.Companies)
            #~ m.add_action(self.modules.contacts.Persons)
            #~ m.add_action(self.modules.contacts.AllPartners)

        m = main.add_menu("master", _("Master"))
        self.on_each_app('setup_master_menu', ui, profile, m)

        self.on_each_app('setup_main_menu', ui, profile, main)

        m = main.add_menu("reports", _("Listings"))
        self.on_each_app('setup_reports_menu', ui, profile, m)

        # ~ if profile.level >= dd.UserLevels.manager: # is_staff:
        m = main.add_menu("config", _("Configure"))
        self.on_each_app('setup_config_menu', ui, profile, m)

        # ~ if profile.level >= dd.UserLevels.manager: # is_staff:

        m = main.add_menu("explorer", _("Explorer"))
        self.on_each_app('setup_explorer_menu', ui, profile, m)

        m = main.add_menu("site", _("Site"))
        #~ self.modules.lino.setup_site_menu(self,ui,user,m)
        self.on_each_app('setup_site_menu', ui, profile, m)

        return main

    def get_installed_apps(self):
        yield super(Site, self).get_installed_apps()

        yield 'lino_welfare.modlib.system'
        yield 'lino.modlib.contenttypes'
        yield 'django.contrib.humanize'  # translations for
        yield 'lino_welfare.modlib.users'
        yield 'lino.modlib.changes'
        yield 'lino.modlib.countries'
        yield 'lino.modlib.properties'
        yield 'lino_welfare.modlib.contacts'
        yield 'lino.modlib.addresses'
        #~ 'lino.modlib.projects'
        #~ 'lino.modlib.notes',
        #~ 'lino.modlib.links',
        yield 'lino_welfare.modlib.uploads'
        #~ 'lino.modlib.thirds'
        yield 'lino.modlib.outbox'
        yield 'lino.modlib.extensible'
        yield 'lino_welfare.modlib.cal'
        #~ yield 'lino.modlib.postings'
        yield 'lino_welfare.modlib.reception'
        yield 'lino.modlib.languages'
        yield 'lino.modlib.accounts'
        yield 'lino_welfare.modlib.badges'
        yield 'lino.modlib.iban'
        yield 'lino_welfare.modlib.sepa'

        yield 'lino.modlib.excerpts'
        yield 'lino.modlib.dedupe'
        yield 'lino.modlib.boards'

        if False:  # not yet ready
            yield 'lino.modlib.families'

        yield 'lino_welfare'

        yield 'lino.modlib.statbel'
        # NOTE: ordering influences (1) main menu (2) fixtures loading
        # e.g. pcsw.demo creates clients needed by cbss.demo
        yield 'lino_welfare.modlib.sales'
        yield 'lino_welfare.modlib.pcsw'
        yield 'lino_welfare.modlib.cv'
        yield 'lino_welfare.modlib.isip'
        yield 'lino_welfare.modlib.jobs'
        yield 'lino_welfare.modlib.integ'
        yield 'lino_welfare.modlib.active_job_search'
        yield 'lino_welfare.modlib.courses'
        yield 'lino_welfare.modlib.newcomers'
        yield 'lino_welfare.modlib.cbss'  # must come after pcsw
        yield 'lino_welfare.modlib.households'  # must come after pcsw
        yield 'lino.modlib.humanlinks'  # must come after households
        yield 'lino_welfare.modlib.debts'  # must come after households
        # The `notes` demo fixture creates Notes for Clients.
        yield 'lino_welfare.modlib.notes'
        yield 'lino_welfare.modlib.aids'
        yield 'lino_welfare.modlib.projects'
        yield 'lino_welfare.modlib.polls'

        yield 'lino.modlib.beid'
        yield 'lino.modlib.davlink'

        yield 'lino.modlib.appypod'
        yield 'lino.modlib.export_excel'

    def get_admin_main_items(self):
        yield self.modules.integ.UsersWithClients
        yield self.modules.reception.MyWaitingVisitors
        yield self.modules.cal.MyEvents
        yield self.modules.cal.MyTasks
        yield self.modules.reception.WaitingVisitors
        #~ yield self.modules.reception.ReceivedVisitors




