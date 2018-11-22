# -*- coding: UTF-8 -*-
# Copyright 2013-2015 Rumma & Ko Ltd
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

"""Recherche active d'emploi.

.. autosummary::
   :toctree:

    fixtures.demo
    models


"""

from lino.api import ad, _


class Plugin(ad.Plugin):
    verbose_name = _("Active Job Search")
    short_name = _("AJS")

    def setup_explorer_menu(self, site, user_type, m):
        menugroup = site.plugins.integ
        m = m.add_menu(menugroup.app_label, menugroup.verbose_name)
        m.add_action('active_job_search.Proofs')
