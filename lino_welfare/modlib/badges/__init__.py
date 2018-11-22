# Copyright 2014-2015 Rumma & Ko Ltd
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

"""This module is internally named after the notion of
`Scout badges <http://en.wikipedia.org/wiki/Scout_badge>`.

It defines two models "Badge" and "Award".  Badges represent the
different achievement levels that can be awarded.  An Award is when a
given "holder" has the right to wear a given Badge.  The date of an
Award is the day when the holder passed a test or something equivalent.

**Settings**

"""

from lino.api import ad, _


class Plugin(ad.Plugin):

    """See :class:`lino.core.plugin.Plugin`.

    .. attribute:: holder_model

        A string referring to the model which represents the badge holder in
        your application.  Default value is ``'contacts.Person'``.

"""

    verbose_name = _("Badges")

    holder_model = 'contacts.Person'

    def setup_config_menu(self, site, user_type, m):
        mg = site.plugins.courses
        m = m.add_menu(mg.app_label, mg.verbose_name)
        m.add_action('badges.Badges')

    def setup_explorer_menu(self, site, user_type, m):
        mg = site.plugins.courses
        m = m.add_menu(mg.app_label, mg.verbose_name)
        m.add_action('badges.Awards')


