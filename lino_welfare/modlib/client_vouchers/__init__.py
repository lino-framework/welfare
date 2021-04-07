# Copyright 2015-2019 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)


"""Adds functionality to work with **client vouchers**.

A **client voucher** is a PCSW specific accounting document which is
related to *one client* and contains transactions with *several
partners*.


"""


from lino.api import ad, _


class Plugin(ad.Plugin):
    "See :class:`lino.core.plugin.Plugin`."
    verbose_name = _("Client vouchers")

    def setup_explorer_menu(self, site, user_type, m):
        mg = site.plugins.ledger
        m = m.add_menu(mg.app_label, mg.verbose_name)
        m.add_action('client_vouchers.Voucher')
