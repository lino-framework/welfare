# Copyright 2013-2015 Luc Saffre
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

