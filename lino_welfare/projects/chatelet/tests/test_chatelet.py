# -*- coding: UTF-8 -*-
# Copyright 2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""Test whether cv.Obstacle.user is correctly set to the requesting
user.

You can run only these tests by issuing::

  $ python setup.py test -s tests.DemoTests.test_chatelet

Or::

  $ cd lino_welfare/projects/chatelet
  $ python manage.py test

"""

from __future__ import unicode_literals

import logging
logger = logging.getLogger(__name__)

from django.conf import settings

from lino.api import rt
from lino.utils.djangotest import TestCase
from lino.core import constants

from lino.modlib.users.choicelists import UserProfiles


class TestCase(TestCase):

    maxDiff = None

    def test00(self):
        
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
        self.assertEqual(result['message'],
                         """Obstacle "Obstacle object" has been created.""")
        self.assertEqual(result['rows'], [
            [u'Alcohol', 1, u'robin', 1, u'', 1, {}, {}, False]])

        self.assertEqual(Obstacle.objects.get(pk=1).user.username, 'robin')

