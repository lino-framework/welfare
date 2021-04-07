# Copyright 2015-2019 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

"""Adds functionality for avoiding duplicate client records.

Like :mod:`lino_xl.lib.dupable_partners`, but specialized for
`pcsw.Client`.

Technical specs see :ref:`weleup`.

Test cases in
:mod:`lino_welfare.projects.std.tests.test_dupe_clients`.

.. autosummary::
   :toctree:

    mixins
    fixtures.demo2


"""

from lino.api import ad, _


class Plugin(ad.Plugin):
    "See :class:`lino.core.plugin.Plugin`."
    verbose_name = _("Dupable clients")

    needs_plugins = ['lino_welfare.modlib.pcsw']

    def setup_explorer_menu(self, site, user_type, main):
        mg = site.plugins.pcsw
        m = main.add_menu(mg.app_label, mg.verbose_name)
        m.add_action('dupable_clients.Words')
        
