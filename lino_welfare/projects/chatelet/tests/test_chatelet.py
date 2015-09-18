# -*- coding: UTF-8 -*-
# Copyright 2015 Luc Saffre
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

"""Miscellaneous tests on an empty database.

You can run only these tests by issuing::

  $ python setup.py test -s tests.DemoTests.test_chatelet

Or::

  $ cd lino_welfare/projects/chatelet
  $ python manage.py test tests.test_chatelet

"""

from __future__ import unicode_literals

import logging
logger = logging.getLogger(__name__)

from django.conf import settings

from lino.api import rt
from lino.utils.djangotest import TestCase
from lino.utils import i2d
from lino.core import constants

from lino.modlib.users.choicelists import UserProfiles


class TestCase(TestCase):
    """Miscellaneous tests on an empty database."""
    maxDiff = None

    def test_cv_obstacle(self):
        """Test whether cv.Obstacle.user is correctly set to the requesting
        user.

        """
        ContentType = rt.modules.contenttypes.ContentType
        Obstacle = rt.modules.cv.Obstacle
        ObstacleType = rt.modules.cv.ObstacleType
        Client = rt.modules.pcsw.Client
        User = settings.SITE.user_model

        User(username='robin', profile=UserProfiles.admin).save()
        ObstacleType(name='Alcohol').save()

        obj = Client(first_name="First", last_name="Last")
        obj.save()

        self.assertEqual(obj.first_name, "First")

        self.assertEqual(
            rt.modules.cv.ObstaclesByPerson.column_names,
            "type user detected_date remark  *")

        url = "/api/cv/ObstaclesByPerson"
        post_data = dict()
        post_data.update(type='1')
        post_data.update(typeHidden='1')
        post_data[constants.URL_PARAM_MASTER_PK] = obj.pk
        ct = ContentType.objects.get_for_model(Client)
        post_data[constants.URL_PARAM_MASTER_TYPE] = ct.id
        post_data[constants.URL_PARAM_ACTION_NAME] = 'grid_post'
        response = self.client.post(
            url, post_data,
            REMOTE_USER='robin',
            HTTP_ACCEPT_LANGUAGE='en')
        result = self.check_json_result(response, 'rows success message')
        self.assertEqual(result['success'], True)
        self.assertEqual(
            result['message'],
            """Freins "Obstacle object" a \xe9t\xe9 cr\xe9\xe9""")
        self.assertEqual(result['rows'], [
            ['Alcohol', 1, 'robin', 1, '22.05.2014', '', 1,
             'First LAST', 100,
             {'id': True}, {}, False]])

        self.assertEqual(Obstacle.objects.get(pk=1).user.username, 'robin')

    def test_dupable_hidden(self):
        """Since `dupable_clients` is hidden, we can create duplicate partners
        without warning.

        """
        Client = rt.modules.pcsw.Client
        User = settings.SITE.user_model

        User(username='robin', profile=UserProfiles.admin).save()

        Client(first_name="First", last_name="Last").save()

        data = dict(an="submit_insert")
        data.update(first_name="First")
        data.update(last_name="Last")
        data.update(genderHidden="M")
        data.update(gender="Male")
        response = self.client.post(
            '/api/pcsw/Clients', data=data, REMOTE_USER="robin")
        result = self.check_json_result(
            response,
            "detail_handler_name data_record rows "
            "close_window success message")
        self.assertEqual(result['success'], True)
        self.assertEqual(
            result['message'],
            'B\xe9n\xe9ficiaire "LAST First (101)" a \xe9t\xe9 cr\xe9\xe9')

    def test_suggest_cal_guests(self):
        """Tests a bugfix in :meth:`suggest_cal_guests
        <lino.modlib.courses.Course.suggest_cal_guests>`.

        """
        User = settings.SITE.user_model
        Guest = rt.modules.cal.Guest
        Event = rt.modules.cal.Event
        EventType = rt.modules.cal.EventType
        GuestRole = rt.modules.cal.GuestRole
        Recurrencies = rt.modules.cal.Recurrencies
        Room = rt.modules.cal.Room
        Enrolment = rt.modules.courses.Enrolment
        Course = rt.modules.courses.Course
        Line = rt.modules.courses.Line
        EnrolmentStates = rt.modules.courses.EnrolmentStates
        Pupil = rt.modules.pcsw.Client

        robin = User(username='robin', profile=UserProfiles.admin)
        robin.save()
        ar = rt.login('robin')
        settings.SITE.verbose_client_info_message = False

        pupil = Pupil(first_name="First", last_name="Last")
        pupil.save()

        et = EventType(name="lesson")
        et.full_clean()
        et.save()

        gr = GuestRole(name="pupil")
        gr.save()

        room = Room(name="classroom")
        room.save()

        line = Line(
            name="Test", guest_role=gr,
            event_type=et,
            every_unit=Recurrencies.weekly)
        line.full_clean()
        line.save()
        course = Course(
            max_events=4,
            line=line, start_date=i2d(20150409), user=robin,
            monday=True, room=room)
        course.full_clean()
        course.save()
        wanted = course.get_wanted_auto_events(ar)
        # self.assertEqual(
        # ar.response['info_message'], 'Generating events between...')
        self.assertEqual(len(wanted), 4)
        enr = Enrolment(
            course=course, state=EnrolmentStates.requested, pupil=pupil)
        enr.save()

        course.do_update_events.run_from_ui(ar)
        self.assertEqual(ar.response['success'], True)
        self.assertEqual(Event.objects.all().count(), 4)
        self.assertEqual(Guest.objects.all().count(), 4)
        # self.assertEqual(ar.response['info_message'], '')

