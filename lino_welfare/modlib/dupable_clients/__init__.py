# Copyright 2015 Luc Saffre
# License: BSD (see file COPYING for details)

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
        
