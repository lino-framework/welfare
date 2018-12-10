# Copyright 2014-2016 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)


"""

The :mod:`lino_welfare.modlib.pcsw` package provides data definitions
for PCSW specific objects.

.. autosummary::
   :toctree:

    roles
    actions
    choicelists
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
        m.add_action('contacts.CivilStates')
        m.add_action('clients.ClientStates')
        m.add_action('beid.BeIdCardTypes')

