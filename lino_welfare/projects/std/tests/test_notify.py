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

"""Miscellaneous tests about the notification framework
(:mod:`lino.modlib.notify` and :mod:`lino_xl.lib.notes`).

You can run these tests individually by issuing::

  $ python setup.py test -s tests.DemoTests.test_std

Or::

  $ cd lino_welfare/projects/std
  $ python manage.py test tests.test_notify

"""

from __future__ import unicode_literals

from urllib import urlencode
from django.conf import settings

from lino.api import rt
from lino.utils.djangotest import TestCase
from lino.utils import i2d

from lino.modlib.users.choicelists import UserProfiles


class TestCase(TestCase):
    maxDiff = None

    def test_checkin_guest(self):
        """Test whether notifications are being emitted.

        - when a visitor checks in
        - when a client is modified
        - when a coaching is modified

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
        Coaching = rt.models.pcsw.Coaching

        self.create_obj(
            User, username='robin', profile=UserProfiles.admin)
        caroline = self.create_obj(
            User, username='caroline', profile='200')
        alicia = self.create_obj(
            User, username='alicia', first_name="Alicia", profile='100')
        roger = self.create_obj(
            User, username='roger', profile='400')

        ses = rt.login('robin')

        first = self.create_obj(
            Client, first_name="First", last_name="Client")

        second = self.create_obj(
            Client, first_name="Second", last_name="Client")
        self.create_obj(
            Coaching, client=second,
            start_date=i2d(20130501),
            end_date=i2d(20140501),
            user=caroline)
        second_roger = self.create_obj(
            Coaching, client=second, start_date=i2d(20140501),
            user=roger)
        self.create_obj(
            Coaching, client=second, start_date=i2d(20140520),
            user=alicia)

        nt = self.create_obj(NoteType, name="System note")
        sc = settings.SITE.site_config
        sc.system_note_type = nt
        sc.save()

        consultation = self.create_obj(EventType, name="consultation")

        # gr = self.create_obj(GuestRole, name="client")

        event = self.create_obj(
            Event, event_type=consultation, user=caroline)
        guest = self.create_obj(Guest, event=event, partner=first)

        self.assertEqual(str(guest), 'Presence #1 (22.05.2014)')

        res = ses.run(guest.checkin)
        self.assertEqual(res, {
            'message': '', 'success': True, 'refresh': True})
        
        self.assertEqual(Notification.objects.count(), 1)

        # checkin doesn't cause a system note
        self.assertEqual(Note.objects.count(), 0)

        # When a client is modified, all active coaches get a
        # notification.
        # Note that Caroline doesn't get a notification because this
        # coaching is not active.
        # Alicia doesn't get a notification because she did it herself.

        data = dict(first_name="Seconda", an="submit_detail")
        kwargs = dict(data=urlencode(data))
        kwargs['REMOTE_USER'] = 'alicia'
        url = '/api/pcsw/Clients/{}'.format(second.pk)
        res = self.client.put(url, **kwargs)
        self.assertEqual(res.status_code, 200)

        self.assertEqual(Notification.objects.count(), 2)

        def check_notifications(expected):
            ar = rt.actors.notify.Notifications.request()
            rst = ar.to_rst(column_names="subject owner user")
            # print rst
            self.assertEquivalent(rst, expected)

        check_notifications("""
====================================== ============================ ===========
 Subject                                About                        Recipient
-------------------------------------- ---------------------------- -----------
                                        *Presence #1 (22.05.2014)*   caroline
 Alicia modified CLIENT Seconda (101)   *CLIENT Seconda (101)*       roger
====================================== ============================ ===========
""")

        # When a coaching is modified, all active coaches of that
        # client get a notification.

        Notification.objects.all().delete()
        data = dict(start_date="02.05.2014", an="grid_put")
        data.update(mt=51)
        data.update(mk=second.pk)
        kwargs = dict(data=urlencode(data))
        kwargs['REMOTE_USER'] = 'alicia'
        url = '/api/pcsw/CoachingsByClient/{}'.format(second_roger.pk)
        res = self.client.put(url, **kwargs)
        self.assertEqual(res.status_code, 200)

        check_notifications("""
================================== ==================== ===========
 Subject                            About                Recipient
---------------------------------- -------------------- -----------
 Alicia modified roger / Client S   *roger / Client S*   roger
================================== ==================== ===========
""")
