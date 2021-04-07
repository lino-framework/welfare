# -*- coding: UTF-8 -*-
# Copyright 2013-2018 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
"""Adds functionality for managing *external* courses.

.. autosummary::
   :toctree:

   roles
   fixtures

"""

from lino.api import ad, _


class Plugin(ad.Plugin):
    verbose_name = _("Courses")
    short_name = _("Courses")

    def setup_main_menu(self, site, user_type, m):
        if True:  # user_type.courses_level:
            m = m.add_menu(self.app_label, self.verbose_name)
            m.add_action('xcourses.CourseProviders')
            m.add_action('xcourses.CourseOffers')
            m.add_action('xcourses.PendingCourseRequests')

    def setup_config_menu(self, site, user_type, m):
        m = m.add_menu(self.app_label, self.verbose_name)
        m.add_action('xcourses.CourseContents')

    def setup_explorer_menu(self, site, user_type, m):
        m = m.add_menu(self.app_label, self.verbose_name)
        m.add_action('xcourses.Courses')
        m.add_action('xcourses.CourseRequests')

