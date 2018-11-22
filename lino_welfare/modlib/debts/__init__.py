# Copyright 2014-2015 Rumma & Ko Ltd
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
"""Functionality for doing "debts mediation".

.. autosummary::
   :toctree:

   mixins
   fields
   fixtures.std
   fixtures.minimal
   fixtures.demo



"""

from builtins import str
from lino import ad

from django.utils.translation import ugettext_lazy as _


class Plugin(ad.Plugin):
    verbose_name = _("Debts mediation")

    ref_length = 20
    """The `max_length` of the `Reference` field of an account.
    """

    def setup_main_menu(self, site, user_type, m):
        m = m.add_menu(self.app_label, self.verbose_name)
        m.add_action('debts.Clients')
        m.add_action('debts.MyBudgets')

    def setup_config_menu(self, site, user_type, m):
        m = m.add_menu(self.app_label, self.verbose_name)

        m.add_action('debts.Groups')
        m.add_action('debts.Accounts')

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
                mb, label=str(fld.verbose_name),
                action=MyBudgets.detail_action)

    def setup_explorer_menu(self, site, user_type, m):
        m = m.add_menu(self.app_label, self.verbose_name)
        m.add_action('debts.Budgets')
        m.add_action('debts.Entries')
