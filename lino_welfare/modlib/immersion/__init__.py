# -*- coding: UTF-8 -*-
# Copyright 2015 Luc Saffre
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

"""Provides functionality for managing "immersion trainings" (stages
d'immersion).

Technical specs and overview see :doc:`/specs/immersion`.

.. autosummary::
    :toctree:

    models
    ui
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

    def setup_main_menu(self, site, profile, m):
        mg = site.plugins.integ
        m = m.add_menu(mg.app_label, mg.verbose_name)
        m.add_action('immersion.MyContracts')

    def setup_config_menu(self, site, profile, m):
        mg = site.plugins.integ
        m = m.add_menu(mg.app_label, mg.verbose_name)
        m.add_action('immersion.ContractTypes')
        m.add_action('immersion.Goals')

    def setup_explorer_menu(self, site, profile, m):
        mg = site.plugins.integ
        m = m.add_menu(mg.app_label, mg.verbose_name)
        m.add_action('immersion.Contracts')
