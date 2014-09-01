# -*- coding: UTF-8 -*-
# Copyright 2014 Luc Saffre
# This file is part of the Lino Welfare project.
# Lino Welfare is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
# Lino Welfare is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with Lino Welfare; if not, see <http://www.gnu.org/licenses/>.

from __future__ import unicode_literals
from __future__ import print_function

import logging
logger = logging.getLogger(__name__)

from django.utils.translation import ugettext_lazy as _

from lino import dd


def objects():
    CourseAreas = dd.modules.courses.CourseAreas
    Line = dd.modules.courses.Line
    Course = dd.modules.courses.Course

    def line(course_area, name, **kw):
        kw.update(course_area=course_area)
        kw.update(dd.str2kw('name', name))
        return Line(**kw)

    obj = line(CourseAreas.integ, _("Kitchen"))
    yield obj
    yield Course(line=obj, start_date=dd.demo_date(-10))

    obj = line(CourseAreas.integ, _("Creativity"))
    yield obj
    yield Course(line=obj, start_date=dd.demo_date(-10))

    obj = line(CourseAreas.integ, _("Our first baby"))
    yield obj
    yield Course(line=obj, start_date=dd.demo_date(-10))

    obj = line(CourseAreas.basic, _("Mathematics"))
    yield obj
    yield Course(line=obj, start_date=dd.demo_date(-10))

    obj = line(CourseAreas.basic, _("French"))
    yield obj
    yield Course(line=obj, start_date=dd.demo_date(-10))

    obj = line(CourseAreas.job, _("Get active!"))
    yield obj
    yield Course(line=obj, start_date=dd.demo_date(-10))
