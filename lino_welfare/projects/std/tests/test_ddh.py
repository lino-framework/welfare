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

Reproduces :ticket:`503`.

You can run only these tests by issuing::

  $ go welfare
  $ cd lino_welfare/projects/std
  $ python manage.py test tests.test_ddh

Or::

  $ python setup.py test -s tests.DemoTests.test_std

"""

from __future__ import unicode_literals
from __future__ import print_function

from builtins import str
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
        from lino.modlib.users.choicelists import UserTypes
        Client = rt.models.pcsw.Client
        User = rt.models.users.User
        Person = rt.models.contacts.Person
        Partner = rt.models.contacts.Partner
        Country = rt.models.countries.Country
        Address = rt.models.addresses.Address
        Note = rt.models.notes.Note

        u = User(username='robin',
                 user_type=UserTypes.admin,
                 language="en")
        u.save()

        def createit():
            obj = Client(first_name="John", last_name="Doe")
            obj.full_clean()
            obj.save()
            pk = obj.pk
            return (obj, Person.objects.get(pk=pk), Partner.objects.get(pk=pk))

        #
        # If there are no vetos, user can ask to delete from any MTI form
        #
        cl, pe, pa = createit()
        cl.delete()

        cl, pe, pa = createit()
        pe.delete()

        cl, pe, pa = createit()
        pa.delete()

        #
        # Cascade-related objects (e.g. addresses) are deleted
        # independently of the polymorphic form which initiated
        # deletion.
        #

        BE = Country(name="Belgium")
        BE.save()

        def check_cascade(model):
            cl, pe, pa = createit()
            obj = model.objects.get(pk=cl.pk)
            addr = Address(partner=pa, country=BE)
            addr.full_clean()
            addr.save()
            obj.delete()
            self.assertEqual(Address.objects.count(), 0)

        check_cascade(Partner)
        check_cascade(Person)
        check_cascade(Client)

        #
        # Vetos of one form are deteced by all other forms.
        #
        def check_veto(obj, expected):
            try:
                obj.delete()
                self.fail("Failed to raise Warning({0})".format(expected))
            except Warning as e:
                self.assertEqual(str(e), expected)

        def check_vetos(obj, msg):
            m = obj.__class__
            obj.full_clean()
            obj.save()
            check_veto(pa, msg)
            check_veto(pe, msg)
            check_veto(cl, msg)
            self.assertEqual(m.objects.count(), 1)
            obj.delete()
            self.assertEqual(m.objects.count(), 0)

        cl, pe, pa = createit()

        msg = "Cannot delete Client DOE John (106) because " \
              "1 Events/Notes refer to it."
        check_vetos(Note(project=cl), msg)

        ct = rt.models.contenttypes.ContentType.objects.get_for_model(Client)
        check_vetos(Note(owner_type=ct, owner_id=pa.pk), msg)

        msg = "Cannot delete Person John DOE because " \
              "1 Events/Notes refer to it."
        check_vetos(Note(contact_person=pe), msg)

