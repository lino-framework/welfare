# -*- coding: UTF-8 -*-
# Copyright 2015-2019 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

"""Provides functionality for managing "immersion trainings" (stages
d'immersion).

Technical specs see :ref:`welcht`.

.. autosummary::
    :toctree:

    fixtures.std
    fixtures.demo

"""

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from lino.api import ad


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
