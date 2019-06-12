# Copyright 2014-2015 Luc Saffre
# License: BSD (see file COPYING for details)
"""
This module is not actively used.
"""

from lino.api import ad

from django.utils.translation import ugettext_lazy as _


class Plugin(ad.Plugin):

    verbose_name = _("Client projects")

    def setup_config_menu(self, site, user_type, m):
        m = m.add_menu(self.app_label, self.verbose_name)
        m.add_action('projects.ProjectTypes')

    def setup_explorer_menu(self, site, user_type, m):
        m = m.add_menu(self.app_label, self.verbose_name)
        m.add_action('projects.Projects')


