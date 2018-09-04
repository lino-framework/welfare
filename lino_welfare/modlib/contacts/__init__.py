# Copyright 2013-2017 Luc Saffre
# This file is part of Lino Welfare.
#
# Lino Welfare is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# Lino Welfare is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License along with Lino Welfare.  If not, see
# <http://www.gnu.org/licenses/>.

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

