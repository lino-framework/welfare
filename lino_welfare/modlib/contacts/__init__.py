# Copyright 2013-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""
Lino-Welfare extension of :mod:`lino.modlib.contacts`
"""

from lino.modlib.contacts import Plugin

from django.utils.translation import string_concat
from django.utils.translation import ugettext_lazy as _


class Plugin(Plugin):

    extends_models = ['Partner', 'Person', 'Company']

    def setup_main_menu(self, site, profile, main):
        m = main.add_menu(self.app_label, self.verbose_name)
        m.add_action('contacts.Persons')
        m.add_action(
            'pcsw.Clients',
            label=string_concat(
                u' \u25b6 ', site.modules.pcsw.Clients.label))
        m.add_action('contacts.Companies')
        m.add_separator('-')
        m.add_action('contacts.Partners', label=_("Partners (all)"))

