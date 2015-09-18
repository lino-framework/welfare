# -*- coding: UTF-8 -*-
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

