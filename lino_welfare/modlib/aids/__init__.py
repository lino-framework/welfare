# Copyright 2014 Luc Saffre
# License: BSD (see file COPYING for details)


"""
See :mod:`welfare.aids`
"""

from lino import ad
from django.utils.translation import ugettext_lazy as _


class Plugin(ad.Plugin):

    verbose_name = _("Aids")

    def setup_main_menu(config, site, profile, m):
        menu_host = site.plugins.pcsw
        m = m.add_menu(menu_host.app_label, menu_host.verbose_name)
        m.add_action('aids.MyPendingGrantings')

    def setup_config_menu(config, site, profile, m):
        menu_host = site.plugins.pcsw
        m = m.add_menu(menu_host.app_label, menu_host.verbose_name)
        m.add_action('aids.AidTypes')
        m.add_action('aids.Categories')

    def setup_explorer_menu(config, site, profile, m):
        menu_host = site.plugins.pcsw
        m = m.add_menu(menu_host.app_label, menu_host.verbose_name)
        m.add_action('aids.Grantings')
        m.add_action('aids.IncomeConfirmations')
        m.add_action('aids.RefundConfirmations')
        m.add_action('aids.SimpleConfirmations')
