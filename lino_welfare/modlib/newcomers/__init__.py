# -*- coding: UTF-8 -*-
# Copyright 2013-2015 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

"""The :mod:`lino_welfare.modlib.newcomers` package provides data
definitions for managing "newcomers".

.. autosummary::
   :toctree:

   fixtures

"""

from django.utils.translation import gettext_lazy as _

from lino import ad


class Plugin(ad.Plugin):
    verbose_name = _("Newcomers")

    def setup_main_menu(self, site, user_type, m):
        m = m.add_menu(self.app_label, self.verbose_name)
        m.add_action('newcomers.NewClients')
        m.add_action('newcomers.AvailableCoaches')

    def setup_config_menu(self, site, user_type, m):
        m = m.add_menu(self.app_label, self.verbose_name)
        m.add_action('newcomers.Brokers')
        m.add_action('newcomers.Faculties')

    def setup_explorer_menu(self, site, user_type, m):
        m = m.add_menu(self.app_label, self.verbose_name)
        m.add_action('newcomers.Competences')
