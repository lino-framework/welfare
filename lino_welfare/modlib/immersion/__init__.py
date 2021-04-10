# -*- coding: UTF-8 -*-
# Copyright 2015-2021 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

"""Provides functionality for managing "immersion trainings" (stages
d'immersion).

Technical specs see :ref:`welcht`.

.. autosummary::
    :toctree:

    fixtures.std

"""


from lino.api import ad, _


class Plugin(ad.Plugin):
    "See :class:`lino.core.plugin.Plugin`."
    verbose_name = _("Immersion trainings")

    needs_plugins = ['lino_welfare.modlib.jobs']

    def setup_main_menu(self, site, user_type, m):
        mg = site.plugins.integ
        m = m.add_menu(mg.app_label, mg.verbose_name)
        m.add_action('immersion.MyContracts')

    def setup_config_menu(self, site, user_type, m):
        mg = site.plugins.integ
        m = m.add_menu(mg.app_label, mg.verbose_name)
        m.add_action('immersion.ContractTypes')
        m.add_action('immersion.Goals')

    def setup_explorer_menu(self, site, user_type, m):
        mg = site.plugins.integ
        m = m.add_menu(mg.app_label, mg.verbose_name)
        m.add_action('immersion.Contracts')
