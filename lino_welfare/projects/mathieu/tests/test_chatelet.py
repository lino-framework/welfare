# -*- coding: UTF-8 -*-
# Copyright 2015-2019 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

"""Miscellaneous tests on an empty database.

You can run just these tests by issuing::

  $ cd lino_welcht/demo
  $ python manage.py test tests.test_chatelet

"""

from __future__ import unicode_literals, print_function

from builtins import str

from django.conf import settings
from django.core.exceptions import ValidationError
import six

from lino.api import rt
from lino.core import constants
from lino.modlib.users.choicelists import UserTypes
from lino.utils import i2d
from lino.utils.djangotest import TestCase
from lino.utils.instantiator import create_row
from lino_welfare.modlib.integ.roles import IntegUser


class TestCase(TestCase):
    """Miscellaneous tests on an empty database."""
    maxDiff = None

    def test_cv_obstacle(self):
        """Test whether cv.Obstacle.user is correctly set to the requesting
        user.

        """
        ContentType = rt.models.contenttypes.ContentType
        Obstacle = rt.models.cv.Obstacle
        ObstacleType = rt.models.cv.ObstacleType
        Client = rt.models.pcsw.Client
        User = settings.SITE.user_model

        robin = create_row(
            User, username='robin', user_type=UserTypes.admin,
            language='en')
        self.assertTrue(robin.user_type.has_required_roles([IntegUser]))
        self.client.force_login(robin)

        ObstacleType(name='Alcohol').save()

        obj = Client(first_name="First", last_name="Last")
        obj.save()

        self.assertEqual(obj.first_name, "First")

        self.assertEqual(
            rt.models.cv.ObstaclesByPerson.column_names,
            "type user detected_date remark  *")

        rh = rt.models.cv.ObstaclesByPerson.get_handle()
        colnames = [col.name for col in rh.get_columns()]
        colnames.sort()
        self.assertEqual(
            'detected_date id overview person remark type user workflow_buttons',
            ' '.join(colnames))

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
            REMOTE_USER='robin')
        result = self.check_json_result(response, 'rows success message navinfo')
        self.assertEqual(result['success'], True)
        if six.PY2:
            self.assertEqual(
                # result['message'],
                # """Freins "Obstacle object" a \xe9t\xe9 cr\xe9\xe9""")
                result['message'],
                """Obstacle "Obstacle object" has been created.""")
            self.assertEqual(result['rows'], [
                ['Alcohol', 1, 'robin', 1, '22.05.2014', '', 1,
                 '<span />',
                 '<div><em>Obstacle object</em></div>',
                 '<div><em>Obstacle object</em></div>',
                 'First LAST', 100,
                 {'id': True}, False]])
        else:
            self.assertEqual(
                # result['message'],
                # """Freins "Obstacle object" a \xe9t\xe9 cr\xe9\xe9""")
                result['message'],
                """Obstacle "Obstacle object (1)" has been created.""")
            # print(result['rows'])
            self.assertEqual(result['rows'], [
                ['Alcohol', 1, 'robin', 1, '22.05.2014', '', 1,
                 '<div><em>Obstacle object (1)</em></div>',
                 '<div><em>Obstacle object (1)</em></div>',
                 '<span />', 'First LAST', 100,
                 {'id': True}, False]])

        self.assertEqual(Obstacle.objects.get(pk=1).user.username, 'robin')

    def test_dupable_hidden(self):
        """Since `dupable_clients` is hidden, we can create duplicate partners
        without warning.

        """
        Client = rt.models.pcsw.Client
        User = settings.SITE.user_model

        User(username='robin', user_type=UserTypes.admin).save()

        Client(first_name="First", last_name="Last").save()

        data = dict(an="submit_insert")
        data.update(first_name="First")
        data.update(last_name="Last")
        data.update(genderHidden="M")
        data.update(gender="Male")
        self.client.force_login(rt.login("robin").user)
        response = self.client.post(
            '/api/pcsw/Clients', data=data, REMOTE_USER="robin")
        result = self.check_json_result(
            response,
            "detail_handler_name data_record rows "
            "close_window success message navinfo")
        self.assertEqual(result['success'], True)
        self.assertEqual(
            result['message'],
            'B\xe9n\xe9ficiaire "LAST First (101)" a \xe9t\xe9 cr\xe9\xe9')

    def test_suggest_cal_guests(self):
        """Tests a bugfix in :meth:`suggest_cal_guests
        <lino_xl.lib.courses.Course.suggest_cal_guests>`.

        """
        User = settings.SITE.user_model
        Guest = rt.models.cal.Guest
        Event = rt.models.cal.Event
        EventType = rt.models.cal.EventType
        GuestRole = rt.models.cal.GuestRole
        Recurrencies = rt.models.cal.Recurrencies
        Room = rt.models.cal.Room
        Enrolment = rt.models.courses.Enrolment
        Course = rt.models.courses.Course
        Line = rt.models.courses.Line
        EnrolmentStates = rt.models.courses.EnrolmentStates
        Pupil = rt.models.pcsw.Client

        robin = User(username='robin', user_type=UserTypes.admin)
        robin.save()
        ar = rt.login('robin')
        settings.SITE.verbose_client_info_message = False

        pupil = Pupil(first_name="First", last_name="Pupil")
        pupil.save()

        pupil2 = Pupil(first_name="Second", last_name="Pupil")
        pupil2.save()

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

        # Two enrolments, one is requested, the other confirmed. Only
        # the confirmed enrolments will be inserted as guests.

        self.create_obj(Enrolment, course=course,
                        state=EnrolmentStates.requested, pupil=pupil2)

        self.create_obj(Enrolment, course=course,
                        state=EnrolmentStates.confirmed,
                        pupil=pupil)

        wanted, unwanted = course.get_wanted_auto_events(ar)
        self.assertEqual(
            ar.response['info_message'],
            'Generating events between 2015-04-13 and 2019-05-22 (max. 4).')
        self.assertEqual(len(wanted), 4)

        course.do_update_events.run_from_ui(ar)
        self.assertEqual(ar.response['success'], True)
        self.assertEqual(Event.objects.all().count(), 4)
        self.assertEqual(Guest.objects.all().count(), 4)
        # self.assertEqual(ar.response['info_message'], '')

        try:
            self.create_obj(Enrolment, course=course,
                            state=EnrolmentStates.confirmed, pupil=pupil)
            self.fail("Expected ValidationError")
        except ValidationError as e:
            if six.PY2:
                expected = "{'__all__': [u'Un object Inscription avec ces " \
                           "champs Atelier et B\\xe9n\\xe9ficiaire existe " \
                           "d\\xe9j\\xe0.']}"
            else:
                expected = "{'__all__': ['Un object Inscription avec ces champs Atelier et Bénéficiaire existe déjà.']}"
            self.assertEqual(str(e), expected)
