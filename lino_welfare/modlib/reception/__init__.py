# -*- coding: UTF-8 -*-
# Copyright 2013-2015 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

"""Lino Welfare extension of :mod:`lino_xl.lib.reception`.

Technical specs see :ref:`weleup`.


"""

from lino_xl.lib.reception import Plugin


class Plugin(Plugin):

    def setup_main_menu(self, site, user_type, main):
        m = main.add_menu(self.app_name, self.verbose_name)
        m.add_action('reception.Clients')
        super(Plugin, self).setup_main_menu(site, user_type, main)
