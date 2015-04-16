# Copyright 2014-2015 Luc Saffre
# License: BSD (see file COPYING for details)
"""Functionality for doing "debts mediation".

.. autosummary::
   :toctree:

   mixins
   fields
   models
   ui
   fixtures.std
   fixtures.demo



"""

from lino import ad

from django.utils.translation import ugettext_lazy as _


class Plugin(ad.Plugin):
    verbose_name = _("Debts mediation")

    def setup_main_menu(self, site, profile, m):
        m = m.add_menu(self.app_label, self.verbose_name)
        m.add_action('debts.Clients')
        m.add_action('debts.MyBudgets')

    def setup_config_menu(self, site, profile, m):
        m = m.add_menu(self.app_label, self.verbose_name)
        mb = site.site_config.master_budget
        if mb is not None:
            """
            the following line is to specify user permissions: non-manager 
            debts agents users should have this command.
            """
            #~ mb._detail_action = MyBudgets.get_url_action('detail_action')
            # (TODO: find a more elegant solution)

            fld = site.modules.system.SiteConfig._meta.get_field(
                'master_budget')
    
            MyBudgets = site.modules.debts.MyBudgets
            m.add_instance_action(
                mb, label=unicode(fld.verbose_name),
                action=MyBudgets.detail_action)

    def setup_explorer_menu(self, site, profile, m):
        m = m.add_menu(self.app_label, self.verbose_name)
        m.add_action('debts.Budgets')
        m.add_action('debts.Entries')
