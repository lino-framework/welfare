# -*- coding: UTF-8 -*-
# Copyright 2013-2015 Luc Saffre
# License: BSD (see file COPYING for details)
"""Adds functionality for managing *external* courses.
"""

from lino.api import ad, _


class Plugin(ad.Plugin):
    verbose_name = _("Courses")
    short_name = _("Courses")

    def setup_main_menu(self, site, profile, m):
        if True:  # profile.courses_level:
            m = m.add_menu(self.app_label, self.verbose_name)
            m.add_action('courses.CourseProviders')
            m.add_action('courses.CourseOffers')
            m.add_action('courses.PendingCourseRequests')

    def setup_config_menu(self, site, profile, m):
        m = m.add_menu(self.app_label, self.verbose_name)
        m.add_action('courses.CourseContents')

    def setup_explorer_menu(self, site, profile, m):
        m = m.add_menu(self.app_label, self.verbose_name)
        m.add_action('courses.Courses')
        m.add_action('courses.CourseRequests')

