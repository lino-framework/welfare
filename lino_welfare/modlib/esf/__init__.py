# Copyright 2016-2019 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

"""Adds functionality to produce "fiches de stages" for the European
Social Fund.

See :doc:`/specs/esf`.

"""

from lino.api import ad, _


class Plugin(ad.Plugin):

    """See :class:`lino.core.plugin.Plugin`. """

    verbose_name = _("ESF")

    needs_plugins = ['lino.modlib.summaries', 'lino.modlib.weasyprint']

    # def setup_config_menu(self, site, user_type, m):
    #     mg = site.plugins.integ
    #     m = m.add_menu(mg.app_label, mg.verbose_name)
    #     m.add_action('badges.Badges')

    def setup_explorer_menu(self, site, user_type, m):
        mg = site.plugins.integ
        m = m.add_menu(mg.app_label, mg.verbose_name)
        m.add_action('esf.AllSummaries')
        m.add_action('esf.StatisticalFields')


