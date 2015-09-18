# -*- coding: UTF-8 -*-
# Copyright 2014-2015 Luc Saffre
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

"""Runs some tests about the disable-delete handler and cascading deletes.

You can run only these tests by issuing::

  $ go welfare
  $ cd lino_welfare/projects/std
  $ python manage.py test tests.test_ddh

Or::

  $ python setup.py test -s tests.DemoTests.test_std

"""

from __future__ import unicode_literals
from __future__ import print_function

import logging
logger = logging.getLogger(__name__)

import os

from lino.utils.djangotest import RemoteAuthTestCase
from django.utils.datastructures import MultiValueDict
from lino.utils import ssin
from lino.api import rt


class DDHTests(RemoteAuthTestCase):
    maxDiff = None

    def test01(self):
        from lino.core import constants
        from django.conf import settings
        from lino.modlib.users.choicelists import UserProfiles
        
        from lino.api.shell import countries, addresses, pcsw, users

        # is it the right settings module?
        self.assertEqual(os.environ['DJANGO_SETTINGS_MODULE'],
                         'lino_welfare.projects.std.settings.demo')

        self.assertEqual(settings.MIDDLEWARE_CLASSES, (
            'django.middleware.common.CommonMiddleware',
            'django.middleware.locale.LocaleMiddleware',
            'lino.core.auth.RemoteUserMiddleware',
            'lino.utils.ajax.AjaxExceptionResponse'))

        u = users.User(username='robin',
                       profile=UserProfiles.admin,
                       language="en")
        u.save()
