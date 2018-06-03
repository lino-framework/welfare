# -*- coding: UTF-8 -*-
# Copyright 2015-2018 Rumma & Ko Ltd
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

"""Tests :class:`lino.modlib.gfks.models.BrokenGFKs`.

You can run only these tests by issuing::

  $ cd lino_welfare/projects/eupen
  $ python manage.py test tests.test_broken_gfks
  
"""

from __future__ import unicode_literals

from django.db import models

from lino.api import rt
from lino.utils.djangotest import TestCase


class TestCase(TestCase):

    fixtures = ['std']

    maxDiff = None

    def test01(self):
        """
        Test whether BrokenGFKs works as expected.

        We create a Client and a Note whose owner field points to that
        client.  And then, when we have all these database objects
        (generically) related to our client, we delete that
        client. Django does not prevent us from doing it.
        """
        # print("20180502 test_broken_gfks.test_01()")

        from django.db.models.deletion import ProtectedError

        Client = rt.models.pcsw.Client
        Note = rt.models.notes.Note
        # ContentType = rt.models.contenttypes.ContentType
        BrokenGFKs = rt.models.gfks.BrokenGFKs

        def create_related_objects():
            cli = Client(first_name="John", last_name="Doe")
            cli.save()

            self.assertEqual(cli.first_name, "John")
            Note(owner=cli, subject="test").save()
            return cli
    
        cli = create_related_objects()
        self.assertEqual(Note.objects.all().count(), 1)
        Note.objects.all().delete()
        cli.delete()
        self.assertEqual(Note.objects.all().count(), 0)
        ar = BrokenGFKs.request()
        rst = ar.to_rst()
        self.assertEqual(rst, "Keine Daten anzuzeigen\n")

        cli = create_related_objects()
        self.assertEqual(Note.objects.all().count(), 1)
        # Here is what i dont understand.  according to the Django
        # docs, deleting an object will delete generic related objects
        # only if they have a GenericRelation field. So when I call
        # Djangos original delete method, the Note objects should
        # remain in the database with a stale GFK. should be 1, but it
        # is 0:
        try:
            models.Model.delete(cli)
            self.fail("Failed to raise ProtectedError")
        except ProtectedError:
            # ProtectedError: ("Cannot delete some instances of model
            # 'Client' because they are referenced through a protected
            # foreign key: 'Note.project'", [Note #1 (u'Ereignis/Notiz
            # #1')])
            pass

        self.assertEqual(Note.objects.all().count(), 1)
    
        rst = ar.to_rst()
        self.assertEqual(rst, "Keine Daten anzuzeigen\n")
