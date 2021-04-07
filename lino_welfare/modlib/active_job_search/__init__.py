# -*- coding: UTF-8 -*-
# Copyright 2013-2015 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

"""Recherche active d'emploi.

.. autosummary::
   :toctree:

    fixtures.demo


"""

from lino.api import ad, _


class Plugin(ad.Plugin):
    verbose_name = _("Active Job Search")
    short_name = _("AJS")

    def setup_explorer_menu(self, site, user_type, m):
        menugroup = site.plugins.integ
        m = m.add_menu(menugroup.app_label, menugroup.verbose_name)
        m.add_action('active_job_search.Proofs')
