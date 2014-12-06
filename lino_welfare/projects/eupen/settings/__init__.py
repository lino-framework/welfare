# -*- coding: UTF-8 -*-
# Copyright 2014 Luc Saffre
# License: BSD (see file COPYING for details)

from __future__ import print_function
from __future__ import unicode_literals

from lino_welfare.projects.base import *

configure_plugin('beid', read_only_simulate=True)


class Site(Site):

    title = "Lino für ÖSHZ"
    languages = 'de fr nl'  # tested docs rely on this distribution
    hidden_languages = None
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

    # def startup(self):
    def do_site_startup(self):
        # super(Site, self).startup()
        super(Site, self).do_site_startup()

        from lino.modlib.changes.models import watch_changes as wc

        wc(self.modules.contacts.Partner)
        wc(self.modules.contacts.Person, master_key='partner_ptr')
        wc(self.modules.contacts.Company, master_key='partner_ptr')
        wc(self.modules.pcsw.Client, master_key='partner_ptr')
        wc(self.modules.pcsw.Coaching, master_key='client__partner_ptr')
        wc(self.modules.pcsw.ClientContact, master_key='client__partner_ptr')
        wc(self.modules.jobs.Candidature, master_key='person__partner_ptr')

        #~ self.modules.notes.Note.watch_changes(master_key='project')
        #~ self.modules.outbox.Mail.watch_changes(master_key='project')
        #~ self.modules.cal.Event.watch_changes(master_key='project')
        #~ self.modules.debts.Budget.watch_changes(master_key='partner')

        # ContractBase is abstract, so it's not under self.modules
        from lino_welfare.modlib.isip.models import ContractBase
        wc(ContractBase, master_key='client__partner_ptr')

        from lino_welfare.modlib.cbss.models import CBSSRequest
        wc(CBSSRequest, master_key='person__partner_ptr')


# the following line should not be active in a checked-in version
#~ DATABASES['default']['NAME'] = ':memory:'
