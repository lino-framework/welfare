# Copyright 2016 Luc Saffre
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

"""Adds functionality to produce "fiches de stages" for the European
Social Fund. See :doc:`/specs/fse`.

"""

from lino.api import ad, _


class Plugin(ad.Plugin):

    """See :class:`lino.core.plugin.Plugin`. """

    verbose_name = _("FSE")

    needs_plugins = ['lino.modlib.summaries', 'lino.modlib.weasyprint']

    # def setup_config_menu(self, site, profile, m):
    #     mg = site.plugins.integ
    #     m = m.add_menu(mg.app_label, mg.verbose_name)
    #     m.add_action('badges.Badges')

    def setup_explorer_menu(self, site, profile, m):
        mg = site.plugins.integ
        m = m.add_menu(mg.app_label, mg.verbose_name)
        m.add_action('fse.AllSummaries')


