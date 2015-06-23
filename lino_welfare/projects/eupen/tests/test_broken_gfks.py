# -*- coding: UTF-8 -*-
# Copyright 2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""Tests :class:`lino.modlib.contenttypes.models.BrokenGFKs`.

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
        """Test whether BrokenGFKs works as expected.

        We create a Client, some Excerpt and a Note whose owner field
        points to that client.  And then, when we have all these
        database objects (generically) related to our client, we
        delete that client. Django does not prevent us from doing it.

        """

        Client = rt.modules.pcsw.Client
        Note = rt.modules.notes.Note
        # ContentType = rt.modules.contenttypes.ContentType
        BrokenGFKs = rt.modules.contenttypes.BrokenGFKs

        ar = BrokenGFKs.request()
    
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
        rst = BrokenGFKs.to_rst(ar)
        self.assertEqual(rst, "\nKeine Daten anzuzeigen\n")

        cli = create_related_objects()
        self.assertEqual(Note.objects.all().count(), 1)
        # Here is what i dont understand.  according to the Django
        # docs, deleting an object will delete generic related objects
        # only if they have a GenericRelation field. So when I call
        # Djangos original delete method, the Note objects should
        # remain in the database with a stale GFK. should be 1, but it
        # is 0:
        models.Model.delete(cli)
        self.assertEqual(Note.objects.all().count(), 0)
    
        rst = BrokenGFKs.to_rst(ar)
        self.assertEqual(rst, "\nKeine Daten anzuzeigen\n")
