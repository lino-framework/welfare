# -*- coding: UTF-8 -*-
# Copyright 2014-2016 Rumma & Ko Ltd
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
"""Creates some workshops.
"""

from __future__ import unicode_literals
from __future__ import print_function


from builtins import range
from django.conf import settings
from lino.api import dd, rt, _
from lino.utils import Cycler


def objects():
    CourseAreas = rt.models.courses.CourseAreas
    Line = rt.models.courses.Line
    Course = rt.models.courses.Course
    EventType = rt.models.cal.EventType
    Pupil = rt.models.pcsw.Client
    Enrolment = rt.models.courses.Enrolment
    EnrolmentStates = rt.models.courses.EnrolmentStates

    ses = settings.SITE.login('hubert')
    
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
    role = rt.models.cal.GuestRole.objects.get(pk=2)
    # **dd.str2kw('name', _("Visitor")))
    kw.update(guest_role=role)
    obj = line(CourseAreas.default, _("Kitchen"), **kw)
    yield obj
    
    kitchen_course = Course(
        line=obj, start_date=dd.demo_date(-10),
        monday=True, start_time="8:00", end_time="12:00",
        user=ses.get_user(),
        max_events=5)
    yield kitchen_course
    
    kw.update(dd.str2kw('description', ""))
    obj = line(CourseAreas.default, _("Creativity"), **kw)
    yield obj
    yield Course(line=obj, start_date=dd.demo_date(-10))

    obj = line(CourseAreas.default, _("Our first baby"), **kw)
    yield obj
    yield Course(line=obj, start_date=dd.demo_date(-10))

    obj = line(CourseAreas.default, _("Mathematics"))
    yield obj
    yield Course(line=obj, start_date=dd.demo_date(-10))

    obj = line(CourseAreas.default, _("French"))
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

    # this will generate 5 events, and for each event one
    # guest.
    
    res = ses.run(kitchen_course.do_update_events)
    if not res['success']:
        raise Exception("oops")

#     expected = """\
# Générer les évènements for Cuisine (12/05/2014)...
# Generating events between 2014-05-12 and 2019-05-22 (max. 5).
# Générer les participants for Entrée calendrier #474  1 (12.05.2014 08:00)...
# 7 row(s) have been updated.
# Générer les participants for Entrée calendrier #475  2 (19.05.2014 08:00)...
# 7 row(s) have been updated.
# Générer les participants for Entrée calendrier #476  3 (26.05.2014 08:00)...
# 7 row(s) have been updated.
# Générer les participants for Entrée calendrier #477  4 (02.06.2014 08:00)...
# 7 row(s) have been updated.
# Générer les participants for Entrée calendrier #478  5 (16.06.2014 08:00)...
# 7 row(s) have been updated.
# 5 row(s) have been updated."""
#     # raise Exception("20161222 {} {}".format(type(res['info_message']), type(expected)))
#     if res['info_message'] != expected:
#         msg = "Expected:\n{0!r}\nGOT:\n{1!r}".format(
#             expected, res['info_message'])
#         print(res['info_message'])
#         raise Exception(msg)

