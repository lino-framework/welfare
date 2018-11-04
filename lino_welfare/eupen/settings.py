# -*- coding: UTF-8 -*-
# Copyright 2014-2018 rumma & Ko Ltd

from lino_welfare.modlib.welfare.settings import *

class Site(Site):
    languages = 'de fr en'
    hidden_languages = None
    # use_websockets = True

    help_url = "http://de.welfare.lino-framework.org"
    demo_fixtures = """std std2 few_languages props all_countries
    demo payments demo2 cbss checkdata checksummaries""".split()

    def get_default_language(self):
        return 'de'
    
    def get_apps_modifiers(self, **kw):
        kw = super(Site, self).get_apps_modifiers(**kw)
        kw.update(badges=None)  # remove the badges app
        kw.update(polls=None)
        # kw.update(esf=None)
        # kw.update(projects=None)
        kw.update(immersion=None)
        kw.update(courses=None)
        # kw.update(ledger=None)
        # kw.update(finan=None)
        # kw.update(vatless=None)
        kw.update(active_job_search=None)
        kw.update(pcsw='lino_welfare.eupen.lib.pcsw')
        kw.update(cv='lino_welfare.modlib.cv')
        return kw

    # def get_dashboard_items(self, user):
    #     yield self.modules.integ.UsersWithClients
    #     yield self.modules.reception.MyWaitingVisitors
    #     yield self.modules.cal.MyEntries
    #     yield self.modules.cal.MyTasks
    #     yield self.modules.reception.WaitingVisitors
    #     #~ yield self.modules.reception.ReceivedVisitors
        
    #     if user.authenticated:
    #         yield self.models.notify.MyMessages

    def do_site_startup(self):
        ctt = self.models.clients.ClientContactTypes
        ctt.set_detail_layout("""
        id name can_refund is_bailiff
        clients.PartnersByClientContactType
        clients.ClientContactsByType
        """)
        ctt.column_names = "id name can_refund is_bailiff"
            
        super(Site, self).do_site_startup()

        from lino.utils.watch import watch_changes as wc

        wc(self.modules.contacts.Partner)
        wc(self.modules.contacts.Person, master_key='partner_ptr')
        wc(self.modules.contacts.Company, master_key='partner_ptr')
        wc(self.modules.pcsw.Client, master_key='partner_ptr')

        wc(self.modules.coachings.Coaching, master_key='client__partner_ptr')
        wc(self.modules.clients.ClientContact, master_key='client__partner_ptr')
        wc(self.modules.jobs.Candidature, master_key='person__partner_ptr')

        # ContractBase is abstract, so it's not under self.modules
        from lino_welfare.modlib.isip.models import ContractBase
        wc(ContractBase, master_key='client__partner_ptr')

        from lino_welfare.modlib.cbss.mixins import CBSSRequest
        wc(CBSSRequest, master_key='person__partner_ptr')


