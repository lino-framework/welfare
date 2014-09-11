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

from lino.modlib.courses.models import *

CourseAreas.clear()
add = CourseAreas.add_item
add('S', _("Integration workshops"), 'integ')
add('B', _("Basic skills"), 'basic')
add('J', _("Job search modules"), 'job')

add = EnrolmentStates.add_item
add('40', _("Started"), 'started', uses_a_place=True)
add('50', _("Finished"), 'finished', uses_a_place=False)


@dd.receiver(dd.pre_analyze)
def my_enrolment_workflows(sender=None, **kw):

    EnrolmentStates.started.add_transition(
        states="confirmed requested")
    EnrolmentStates.finished.add_transition(
        states="started")


class Course(Course):
    class Meta:
        verbose_name = _("Workshop")
        verbose_name_plural = _('Workshops')
        abstract = dd.is_abstract_model(__name__, 'Course')


class Line(Line):
    class Meta:
        verbose_name = _("Workshop line")
        verbose_name_plural = _('Workshop lines')
        abstract = dd.is_abstract_model(__name__, 'Line')


EnrolmentsByPupil.column_names = 'request_date course workflow_buttons *'


class IntegEnrolmentsByPupil(EnrolmentsByPupil):
    _course_area = CourseAreas.integ


class BasicEnrolmentsByPupil(EnrolmentsByPupil):
    _course_area = CourseAreas.basic


class JobEnrolmentsByPupil(EnrolmentsByPupil):
    _course_area = CourseAreas.job


