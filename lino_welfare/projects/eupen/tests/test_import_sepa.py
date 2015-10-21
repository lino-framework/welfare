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

"""Testing CODA import (defined in :class:`lino_cosi.lib.sepa`).

You can run only these tests by issuing::

  $ cd lino_welfare/projects/eupen
  $ python manage.py test tests.test_import_sepa
  
"""

from __future__ import unicode_literals

import os

from django.db import models
from django.conf import settings

from lino.api import dd, rt
from lino.utils.djangotest import TestCase

HERE = os.path.dirname(__file__)


class TestCase(TestCase):
    # fixtures = ['std']

    maxDiff = None

    def test01(self):
        """We simply read the file

        """

        dd.plugins.sepa.import_statements_path = HERE
        dd.plugins.sepa.delete_imported_xml_files = False

        rt.modules.users.User(username='robin').save()
        ses = rt.login('robin')
        settings.SITE.site_config.import_sepa(ses)

        Account = rt.modules.sepa.Account
        Movement = rt.modules.sepa.Movement
        self.assertEqual(Account.objects.count(), 193)
        self.assertEqual(Movement.objects.count(), 131)
