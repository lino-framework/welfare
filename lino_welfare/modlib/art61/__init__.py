# -*- coding: UTF-8 -*-
# Copyright 2015-2019 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

"""Provides functionality for managing so-called "article 61 job
supplyments".  Technical specs see :ref:`welcht`.


.. autosummary::
   :toctree:

   fixtures.std

"""

from __future__ import unicode_literals

from lino import ad

from django.utils.translation import ugettext_lazy as _


class Plugin(ad.Plugin):
    "See :class:`lino.core.plugin.Plugin`."
    verbose_name = _("Art61 job supplying")  # Mises à l'emploi art.61
    needs_plugins = ['lino_welfare.modlib.jobs', 'lino_xl.lib.cv']

    def setup_main_menu(self, site, user_type, m):
        mg = site.plugins.integ
        m = m.add_menu(mg.app_label, mg.verbose_name)
        m.add_action('art61.MyContracts')

    def setup_config_menu(self, site, user_type, m):
        mg = site.plugins.integ
        m = m.add_menu(mg.app_label, mg.verbose_name)
        m.add_action('art61.ContractTypes')

    def setup_explorer_menu(self, site, user_type, m):
        mg = site.plugins.integ
        m = m.add_menu(mg.app_label, mg.verbose_name)
        m.add_action('art61.Contracts')
