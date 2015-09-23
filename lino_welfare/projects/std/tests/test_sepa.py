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

"""Runs some tests about SEPA accounts.

You can run only these tests by issuing::

  $ go welfare
  $ cd lino_welfare/projects/std
  $ python manage.py test tests.test_sepa

"""

from __future__ import unicode_literals
from __future__ import print_function

from django.core.exceptions import ValidationError
from lino.utils.djangotest import RemoteAuthTestCase
from lino.api import rt


class TestCase(RemoteAuthTestCase):
    # fixtures = ['few_countries', 'few_cities', 'demo_users']

    def test(self):
        Client = rt.modules.pcsw.Client
        Account = rt.modules.sepa.Account

        cli = Client(first_name="Ott", last_name="Karu")
        cli.full_clean()
        cli.save()

        acc = Account(partner=cli, iban="EE252200001100817338")
        acc.full_clean()

        self.assertEqual(acc.iban, "EE252200001100817338")

        expected = "{'iban': [u'EE IBANs must contain 20 characters.']}"
        acc = Account(partner=cli, iban="EE")
        try:
            acc.full_clean()
            self.fail("Expected {0}".format(expected))
        except ValidationError as e:
            self.assertEqual(str(e), expected)

        expected = "{'iban': [u'BE IBANs must contain 16 characters.']}"
        acc = Account(partner=cli, iban="BE")
        try:
            acc.full_clean()
            self.fail("Expected {0}".format(expected))
        except ValidationError as e:
            self.assertEqual(str(e), expected)

            
            



