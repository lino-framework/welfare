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

"""Runs some tests about :mod:`lino.modlib.plausibility` problems
specific to Lino Welfare.

You can run only these tests by issuing::

  $ go welfare
  $ cd lino_welfare/projects/std
  $ python manage.py test tests.test_plausibility


See also :mod:`lino.projects.min2.tests.test_addresses`.


"""


from __future__ import unicode_literals
from __future__ import print_function

from lino.core.utils import gfk2lookup
from lino.utils.djangotest import RemoteAuthTestCase
from lino.api import rt


def create(m, **kw):
    obj = m(**kw)
    obj.full_clean()
    obj.save()
    obj.after_ui_save(None, None)
    return obj


class TestCase(RemoteAuthTestCase):
    fixtures = ['few_countries', 'few_cities', 'demo_users']

    def test(self):
        Client = rt.modules.pcsw.Client
        Address = rt.modules.addresses.Address
        Place = rt.modules.countries.Place
        Problem = rt.modules.plausibility.Problem
        eupen = Place.objects.get(name="Eupen")

        def assert_check(obj, *expected):
            qs = Problem.objects.filter(**gfk2lookup(Problem.owner, obj))
            got = tuple(p.message for p in qs)
            self.assertEqual(got, expected)

        ar = rt.modules.pcsw.Clients.request()
        doe = create(
            Client, first_name="John", last_name="Doe", city=eupen)

        mow = create(
            Client, first_name="John", last_name="Mow", city=eupen)

        self.assertEqual(Client.objects.count(), 2)
        self.assertEqual(Address.objects.count(), 0)

        # "Owner with address, but no address record"
        # Detect problems for one client:
        doe.partner_ptr.check_plausibility(ar, fix=False)
        assert_check(
            doe.partner_ptr,
            "(\u2605) Owner with address, but no address record.")
        addr = doe.get_primary_address()
        self.assertEqual(addr, None)

        doe.check_plausibility(ar, fix=False)
        assert_check(
            doe,
            "Neither valid eId data nor alternative identifying document.")

        # Fix the problems for both:
        doe.partner_ptr.check_plausibility(ar, fix=True)
        mow.partner_ptr.check_plausibility(ar, fix=True)
        # problems have been fixed:
        assert_check(doe.partner_ptr)
        assert_check(mow.partner_ptr)

        # mow.merge_row.run_from_code(ar)

        # test case not finished. we should merge them now and get a
        # duplicate primary address.
