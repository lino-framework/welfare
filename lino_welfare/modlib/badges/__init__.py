# Copyright 2014-2015 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

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


