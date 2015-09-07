# -*- coding: UTF-8 -*-
# Copyright 2015 Luc Saffre
# License: BSD (see file COPYING for details)

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

            
            



