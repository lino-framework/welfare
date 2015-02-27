# -*- coding: UTF-8 -*-
# Copyright 2013-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""Lino-Welfare extension of :mod:`lino.modlib.reception`.

See also the tested document about :doc:`/tested/reception`.

.. autosummary::
   :toctree:

   models

"""

from lino.modlib.reception import Plugin


class Plugin(Plugin):

    required_user_groups = 'reception coaching'

    def setup_main_menu(self, site, profile, main):
        m = main.add_menu(self.app_name, self.verbose_name)
        m.add_action('reception.Clients')
        super(Plugin, self).setup_main_menu(site, profile, main)
