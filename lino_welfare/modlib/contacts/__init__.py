# Copyright 2013-2017 Luc Saffre
# License: BSD (see file COPYING for details)

"""
Lino-Welfare extension of :mod:`lino_xl.lib.contacts`
"""

from lino_xl.lib.contacts import Plugin

from django.utils.text import format_lazy
from django.utils.translation import ugettext_lazy as _


class Plugin(Plugin):

    use_vcard_export = False
    
    extends_models = ['Partner', 'Person', 'Company']

    def setup_main_menu(self, site, user_type, main):
        m = main.add_menu(self.app_label, self.verbose_name)
        m.add_action('contacts.Persons')
        m.add_action(
            'pcsw.Clients',
            label=format_lazy(u"{}{}",
                u' \u25b6 ', site.modules.pcsw.Clients.label))
        m.add_action('contacts.Companies')
        m.add_separator('-')
        m.add_action('contacts.Partners', label=_("Partners (all)"))

