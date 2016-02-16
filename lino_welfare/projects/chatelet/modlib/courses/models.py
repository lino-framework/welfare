# -*- coding: UTF-8 -*-
# Copyright 2014-2016 Luc Saffre
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

"""
Does some adaptions.
"""

from __future__ import unicode_literals
from __future__ import print_function

import logging
logger = logging.getLogger(__name__)

from django.utils.translation import ugettext_lazy as _

from lino.api import dd, rt

from lino_cosi.lib.courses.models import *

CourseAreas.clear()
add = CourseAreas.add_item
add('S', _("Integration workshops"), 'integ')  # no longer used
add('B', _("General integration workshops"), 'basic')  # requested #564
add('J', _("Job search workshops"), 'job')  # requested #564

# Dans l'onglet O.I., remplacer "Ateliers" par "Ateliers d'Insertion
# sociale" et "Module de détermination d'un projet socioprofessionnel"
# par "Ateliers d'Insertion socioprofessionnelle".

add = EnrolmentStates.add_item
add('40', _("Started"), 'started', invoiceable=False, uses_a_place=True)
add('50', _("Finished"), 'finished', invoiceable=False, uses_a_place=False)


@dd.receiver(dd.pre_analyze)
def my_enrolment_workflows(sender=None, **kw):

    EnrolmentStates.started.add_transition(
        required_states="confirmed requested")
    EnrolmentStates.finished.add_transition(
        required_states="started")

    CourseStates.registered.add_transition(required_states="draft")
    CourseStates.draft.add_transition(required_states="registered")


class Course(Course):
    class Meta:
        verbose_name = _("Workshop")
        verbose_name_plural = _('Workshops')
        abstract = dd.is_abstract_model(__name__, 'Course')


# GUEST_ENROLMENT_STATES = set([
#     EnrolmentStates.confirmed,
#     EnrolmentStates.started])


class Enrolment(Enrolment):
    """Adds two text fields :attr:`motivation` and :attr:`problems`.

    """
    motivation = dd.RichTextField(
        _("Motif de l'orientation"),
        blank=True, format="html")
    problems = dd.RichTextField(
        _("Difficultés à l'origine de la demande / "
          "Problématiques repérées"),
        blank=True, format="html")

    # def suggest_guest_for(self, event):
    #     return self.state in GUEST_ENROLMENT_STATES

Enrolments.detail_layout = """
request_date user
course pupil
remark workflow_buttons printed
motivation problems
"""


class Line(Line):
    class Meta:
        verbose_name = _("Workshop series")
        verbose_name_plural = _('Workshop lines')
        abstract = dd.is_abstract_model(__name__, 'Line')


EnrolmentsByPupil.column_names = 'request_date course workflow_buttons *'


class IntegEnrolmentsByPupil(EnrolmentsByPupil):
    _course_area = CourseAreas.integ


class BasicEnrolmentsByPupil(EnrolmentsByPupil):
    _course_area = CourseAreas.basic


class JobEnrolmentsByPupil(EnrolmentsByPupil):
    _course_area = CourseAreas.job


ActiveCourses._label = _("Active workshops")
DraftCourses._label = _("Draft workshops")
