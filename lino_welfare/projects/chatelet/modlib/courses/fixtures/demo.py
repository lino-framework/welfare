# -*- coding: UTF-8 -*-
# Copyright 2014 Luc Saffre
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

from __future__ import unicode_literals
from __future__ import print_function

import logging
logger = logging.getLogger(__name__)

from django.conf import settings
from lino.api import dd, rt, _
from lino.utils import Cycler


def objects():
    CourseAreas = rt.modules.courses.CourseAreas
    Line = rt.modules.courses.Line
    Course = rt.modules.courses.Course
    EventType = rt.modules.cal.EventType
    Pupil = rt.modules.pcsw.Client
    Enrolment = rt.modules.courses.Enrolment
    EnrolmentStates = rt.modules.courses.EnrolmentStates

    kw = dd.str2kw('name', _("Workshop"))
    event_type = EventType(**kw)
    yield event_type

    def line(course_area, name, **kw):
        kw.update(course_area=course_area)
        kw.update(event_type=event_type)
        kw.update(dd.str2kw('name', name))
        return Line(**kw)

    # Introduction aux techniques de cuisine élémentaires
    kw = dd.str2kw(
        'description',
        _("Introduction to basic kitchen technologies."))
    kw.update(body_template="enrolment.body.html")
    kw.update(dd.str2kw(
        'excerpt_title', _("Request for enrolment")))
    obj = line(CourseAreas.basic, _("Kitchen"), **kw)
    yield obj
    yield Course(line=obj, start_date=dd.demo_date(-10))
    
    kw.update(dd.str2kw('description', ""))
    obj = line(CourseAreas.basic, _("Creativity"), **kw)
    yield obj
    yield Course(line=obj, start_date=dd.demo_date(-10))

    obj = line(CourseAreas.basic, _("Our first baby"), **kw)
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
    yield Course(line=obj, start_date=dd.demo_date(-10), max_places=3)

    kw = dict()
    kw.update(dd.str2kw('excerpt_title',
                        _("Request for intervention")))
    kw.update(body_template="intervention.body.html")
    obj = line(CourseAreas.job, _("Psycho-social intervention"), **kw)
    yield obj
    yield Course(line=obj, start_date=dd.demo_date(-200), max_places=1)

    PUPILS = Cycler(Pupil.objects.all())
    #~ print 20130712, Pupil.objects.all()
    COURSES = Cycler(Course.objects.all())
    STATES = Cycler(EnrolmentStates.objects())
    USERS = Cycler(settings.SITE.user_model.objects.all())

    def fits(course, pupil):
        if course.max_places and course.get_free_places() == 0:
            return False
        if Enrolment.objects.filter(course=course, pupil=pupil).count():
            return False
        return True
    for i in range(100):
        course = COURSES.pop()
        pupil = PUPILS.pop()
        while not fits(course, pupil):
            course = COURSES.pop()
        kw = dict(user=USERS.pop(), course=course, pupil=pupil)
        kw.update(request_date=dd.demo_date(-i))
        kw.update(state=STATES.pop())
        yield Enrolment(**kw)
