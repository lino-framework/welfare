# Copyright 2014-2016 Luc Saffre
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

The :mod:`lino_welfare.modlib.pcsw` package provides data definitions
for PCSW specific objects.

.. autosummary::
   :toctree:

    roles
    actions
    choicelists
    models
    fixtures


"""


from lino.api import ad, _


class Plugin(ad.Plugin):
    "See :class:`lino.core.plugin.Plugin`."
    verbose_name = _("PCSW")
    needs_plugins = ['lino_xl.lib.coachings']

    def setup_main_menu(self, site, user_type, m):
        # mg = self.get_menu_group()
        mg = self
        m = m.add_menu(mg.app_label, mg.verbose_name)
        m.add_action('pcsw.CoachedClients')
        m.add_action('coachings.MyCoachings')

    def setup_config_menu(self, site, user_type, m):
        m = m.add_menu(self.app_label, self.verbose_name)
        m.add_action('pcsw.PersonGroups')
        m.add_action('pcsw.Activities')
        m.add_action('pcsw.ExclusionTypes')
        m.add_action('pcsw.DispenseReasons')
        if not site.is_installed('aids'):
            m.add_action('pcsw.AidTypes')

    def setup_explorer_menu(config, site, user_type, m):
        m = m.add_menu(config.app_label, config.verbose_name)
        m.add_action('pcsw.Exclusions')
        m.add_action('pcsw.Convictions')
        m.add_action('pcsw.AllClients')
        #~ m.add_action(PersonSearches)
        m.add_action('beid.CivilStates')
        m.add_action('clients.ClientStates')
        m.add_action('beid.BeIdCardTypes')

