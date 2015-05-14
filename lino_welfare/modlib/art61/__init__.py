# -*- coding: UTF-8 -*-
# Copyright 2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""Provides functionality for managing so-called "art61 job supply" projects.


.. autosummary::
   :toctree:

   models
   fixtures.std

Document templates:

.. xfile:: art61/Contract/contract.body.html

  This file is used as :attr:`body_template
  <lino.modlib.excerpts.models.Excerpt.body_template>` on the excerpt
  type used to print a
  :class:`lino_welfare.modlib.art61.models.Contract`.

  Source code: :srcref:`art61/Contract/contract.body.html
  <lino_welfare/modlib/art61/config/art61/Contract/contract.body.html>`.

"""

from __future__ import unicode_literals

from lino import ad

from django.utils.translation import ugettext_lazy as _


class Plugin(ad.Plugin):
    "See :class:`lino.core.plugin.Plugin`."
    verbose_name = _("Art61 job supplying")  # Mises à l'emploi art.61
    needs_plugins = ['lino_welfare.modlib.jobs', 'lino.modlib.cv']

    def setup_main_menu(self, site, profile, m):
        mg = site.plugins.integ
        m = m.add_menu(mg.app_label, mg.verbose_name)
        m.add_action('art61.MyContracts')

    def setup_config_menu(self, site, profile, m):
        mg = site.plugins.integ
        m = m.add_menu(mg.app_label, mg.verbose_name)
        m.add_action('art61.ContractTypes')

    def setup_explorer_menu(self, site, profile, m):
        mg = site.plugins.integ
        m = m.add_menu(mg.app_label, mg.verbose_name)
        m.add_action('art61.Contracts')
