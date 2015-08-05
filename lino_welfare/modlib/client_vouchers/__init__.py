# Copyright 2015 Luc Saffre
# License: BSD (see file COPYING for details)


"""Adds functionality to work with **client vouchers**.

A **client voucher** is a PCSW specific accounting document which is
related to *one client* and contains transactions with *several
partners*.


.. autosummary::
   :toctree:

    models
    ui

"""


from lino.api import ad, _


class Plugin(ad.Plugin):
    "See :class:`lino.core.plugin.Plugin`."
    verbose_name = _("Client vouchers")

    def setup_explorer_menu(self, site, profile, m):
        mg = site.plugins.accounts
        m = m.add_menu(mg.app_label, mg.verbose_name)
        m.add_action('client_vouchers.Voucher')
