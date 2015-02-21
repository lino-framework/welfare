# -*- coding: UTF-8 -*-
# Copyright 2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""Tests :class:`lino.modlib.contenttypes.models.StaleGenericRelateds`.

You can run only these tests by issuing::

  $ cd lino_welfare/projects/eupen
  $ python manage.py test tests.test_stale_gfk
  
"""

from __future__ import unicode_literals

from django.db import models

from lino.api import rt
from lino.utils.djangotest import TestCase


class TestCase(TestCase):

    fixtures = ['std']

    maxDiff = None

    def test01(self):
        """Test whether StaleGenericRelateds works as expected.

        We create a Client, some Excerpt and a Note whose owner field
        points to that client.  And then, when we have all these
        database objects (generically) related to our client, we
        delete that client. Django does not prevent us from doing it.

        """

        # User = rt.modules.users.User
        Client = rt.modules.pcsw.Client
        Note = rt.modules.notes.Note
        # ExcerptType = rt.modules.excerpts.ExcerptType
        # Excerpt = rt.modules.excerpts.Excerpt
        # ContentType = rt.modules.contenttypes.ContentType
        StaleGenericRelateds = rt.modules.contenttypes.StaleGenericRelateds

        # User(username='roger').save()

        ar = StaleGenericRelateds.request()
    
        def create_related_objects():
            cli = Client(first_name="John", last_name="Doe")
            cli.save()

            self.assertEqual(cli.first_name, "John")
            # similar to what CreateExcerpt action would do
            # ar.selected_rows = [cli]
            # ct = ContentType.objects.get_for_model(Client)
            # qs = ExcerptType.objects.filter(content_type=ct)
            # for et in qs:
            #     et.get_or_create_excerpt(ar)

            Note(owner=cli, subject="test").save()
            return cli
    
        cli = create_related_objects()
        # self.assertEqual(Excerpt.objects.all().count(), 0)
        self.assertEqual(Note.objects.all().count(), 1)
        cli.delete()
        # self.assertEqual(Excerpt.objects.all().count(), 0)
        self.assertEqual(Note.objects.all().count(), 0)
        rst = StaleGenericRelateds.to_rst(ar)
        self.assertEqual(rst, "\nKeine Daten anzuzeigen\n")

        cli = create_related_objects()
        # self.assertEqual(Excerpt.objects.all().count(), 123)
        self.assertEqual(Note.objects.all().count(), 1)
        models.Model.delete(cli)
        # self.assertEqual(Excerpt.objects.all().count(), 0)
        #  should be 1:
        self.assertEqual(Note.objects.all().count(), 0)
    
        rst = StaleGenericRelateds.to_rst(ar)
        self.assertEqual(rst, "")
