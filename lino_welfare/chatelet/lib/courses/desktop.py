# -*- coding: UTF-8 -*-
# Copyright 2014-2017 Rumma & Ko Ltd
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

from lino.api import _
from lino_xl.lib.courses.desktop import *

Enrolments.detail_layout = """
request_date user
course pupil
remark workflow_buttons printed
motivation problems
"""


EnrolmentsByPupil.column_names = 'request_date course workflow_buttons *'
EnrolmentsByPupil.insert_layout = """
course_area
course
places option
remark
request_date user
"""

    
    


class BasicCourses(Activities):
    _course_area = CourseAreas.default


class JobCourses(Activities):
    _course_area = CourseAreas.job


# class IntegEnrolmentsByPupil(EnrolmentsByPupil):
#     _course_area = CourseAreas.integ


class BasicEnrolmentsByPupil(EnrolmentsByPupil):
    _course_area = CourseAreas.default


class JobEnrolmentsByPupil(EnrolmentsByPupil):
    _course_area = CourseAreas.job


class ActiveCourses(ActiveCourses):
    label = _("Active workshops")
    column_names = 'detail_link enrolments free_places room description *'
    hide_sums = True


class DraftCourses(DraftCourses):
    label = _("Draft workshops")
    column_names = 'detail_link room description *'


class InactiveCourses(InactiveCourses):
    label = _("Inactive workshops")


class ClosedCourses(ClosedCourses):
    label = _("Closed workshops")
    

