# -*- coding: UTF-8 -*-
# Copyright 2016 Luc Saffre
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

"""Miscellaneous tests on an empty database.

You can run only these tests by issuing::

  $ python setup.py test -s tests.DemoTests.test_eupen

Or::

  $ cd lino_welfare/projects/eupen
  $ python manage.py test tests.test_notify

"""

from __future__ import unicode_literals

from django.conf import settings

from lino.api import rt
from lino.utils.djangotest import TestCase

from lino.modlib.users.choicelists import UserProfiles


class TestCase(TestCase):
    """"""
    maxDiff = None

    def test_checkin_guest(self):
        """Test whether a notification is emitted when a visitor checks in.

        """
        User = settings.SITE.user_model
        Notification = rt.models.notify.Notification
        Note = rt.models.notes.Note
        NoteType = rt.models.notes.EventType
        Guest = rt.models.cal.Guest
        Event = rt.models.cal.Event
        EventType = rt.models.cal.EventType
        GuestRole = rt.models.cal.GuestRole
        Client = rt.models.pcsw.Client

        self.create_obj(
            User, username='robin', profile=UserProfiles.admin)
        aurelie = self.create_obj(
            User, username='aurelie', profile=UserProfiles.admin)

        ses = rt.login('robin')

        first = Client(first_name="First", last_name="Client")
        first.save()

        nt = NoteType(name="System note")
        nt.full_clean()
        nt.save()
        sc = settings.SITE.site_config
        sc.system_note_type = nt
        sc.save()

        et = EventType(name="consultation")
        et.full_clean()
        et.save()

        gr = GuestRole(name="client")
        gr.save()

        event = self.create_obj(Event, event_type=et, user=aurelie)
        guest = self.create_obj(Guest, event=event, partner=first)

        self.assertEqual(str(guest), 'Anwesenheit #1 (22.05.2014)')

        res = ses.run(guest.checkin)
        self.assertEqual(res, {
            'message': '', 'success': True, 'refresh': True})
        
        self.assertEqual(Notification.objects.count(), 1)

        # don't write a system note for checking
        self.assertEqual(Note.objects.count(), 0)
