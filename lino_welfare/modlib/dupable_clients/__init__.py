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

"""Adds functionality for avoiding duplicate client records.

Like :mod:`lino.modlib.dupable_partners`, but specialized for
`pcsw.Client`.

Examples and test cases in
:ref:`welfare.tested.dupe_clients`.
and
:mod:`lino_welfare.projects.std.tests.test_dupe_clients`.

.. autosummary::
   :toctree:

    models
    mixins
    fixtures.demo2


"""

from lino.api import ad, _


class Plugin(ad.Plugin):
    "See :class:`lino.core.plugin.Plugin`."
    verbose_name = _("Dupable clients")

    needs_plugins = ['lino_welfare.modlib.pcsw']

    def setup_explorer_menu(self, site, profile, main):
        mg = site.plugins.pcsw
        m = main.add_menu(mg.app_label, mg.verbose_name)
        m.add_action('dupable_clients.Words')
        
