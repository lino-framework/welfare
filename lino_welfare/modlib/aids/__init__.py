# Copyright 2014-2018 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

"""Specs for this plugin are in :ref:`weleup`.


"""

from lino.api import ad, _


class Plugin(ad.Plugin):
    """The plugin."""
    verbose_name = _("Aids")

    no_date_range_veto_until = 0
    """

    Optionally specify the primary key (an integer) of the last granting for
    which you want to deactivate date range validation in confirmations.  This
    is useful for keeping legacy confirmations that have been issued before the
    rule was activated.

    The default value **0** means that date range validation is always active, the
    special value **-1** means that it is never active.

    """

    def setup_main_menu(config, site, user_type, m):
        menu_host = site.plugins.pcsw
        m = m.add_menu(menu_host.app_label, menu_host.verbose_name)
        m.add_action('aids.MyPendingGrantings')

    def setup_config_menu(config, site, user_type, m):
        menu_host = site.plugins.pcsw
        m = m.add_menu(menu_host.app_label, menu_host.verbose_name)
        m.add_action('aids.AidTypes')
        m.add_action('aids.Categories')

    def setup_explorer_menu(config, site, user_type, m):
        menu_host = site.plugins.pcsw
        m = m.add_menu(menu_host.app_label, menu_host.verbose_name)
        m.add_action('aids.AllGrantings')
        m.add_action('aids.AllIncomeConfirmations')
        m.add_action('aids.AllRefundConfirmations')
        m.add_action('aids.AllSimpleConfirmations')
