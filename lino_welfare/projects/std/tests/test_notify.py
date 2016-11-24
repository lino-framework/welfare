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
(:mod:`lino.modlib.notify` and :mod:`lino_xl.lib.notes`). Consult the
source code of this module.

You can run these tests individually by issuing::

  $ python setup.py test -s tests.DemoTests.test_std

Or::

  $ cd lino_welfare/projects/std
  $ python manage.py test tests.test_notify

"""

from __future__ import unicode_literals

import json
from urllib import urlencode
from django.conf import settings

from lino.utils.djangotest import TestCase
from lino.utils import i2d, AttrDict

from lino.api import rt

from lino.modlib.users.choicelists import UserTypes


class TestCase(TestCase):
    maxDiff = None

    def check_notifications(self, expected=None):
        """Hint: when `expected` is empty, then the found result is being
        printed to stdout so you can copy it into your code.

        """
        ar = rt.actors.notify.Messages.request()
        rst = ar.to_rst(column_names="body owner user")
        if not expected:
            print rst
        # print rst  # handy when something fails
        self.assertEquivalent(expected, rst)

    def check_notes(self, expected):
        ar = rt.actors.notes.Notes.request()
        rst = ar.to_rst(column_names="id user project subject")
        if not expected:
            print rst
        self.assertEquivalent(expected, rst)

    def check_coachings(self, expected):
        ar = rt.actors.pcsw.Coachings.request()
        rst = ar.to_rst(
            column_names="id client start_date end_date user primary")
        if not expected:
            print rst
        self.assertEquivalent(expected, rst)

    def test_checkin_guest(self):
        """Test whether notifications are being emitted.

        - when a visitor checks in
        - when a client is modified
        - when a coaching is modified

        """
        User = settings.SITE.user_model
        Message = rt.models.notify.Message
        Note = rt.models.notes.Note
        NoteType = rt.models.notes.EventType
        Guest = rt.models.cal.Guest
        Event = rt.models.cal.Event
        EventType = rt.models.cal.EventType
        Client = rt.models.pcsw.Client
        Coaching = rt.models.pcsw.Coaching
        ContentType = rt.models.contenttypes.ContentType

        self.create_obj(
            User, username='robin', profile=UserTypes.admin)
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

        # Checkin a guest

        res = ses.run(guest.checkin)
        self.assertEqual(res, {
            'message': '', 'success': True, 'refresh': True})

        # it has caused a notification message:
        self.assertEqual(Message.objects.count(), 1)

        # id does *not* cause a system note:
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

        self.assertEqual(Message.objects.count(), 2)

        # self.check_notifications()
        self.check_notifications("""
+------------------------------------------------------------------------+------------------------+-----------+
| Body                                                                   | Controlled by          | Recipient |
+========================================================================+========================+===========+
|                                                                        |                        | caroline  |
+------------------------------------------------------------------------+------------------------+-----------+
| [CLIENT Seconda (101)](javascript:Lino.pcsw.Clients.detail.run\(null,{ | *CLIENT Seconda (101)* | roger     |
| "record_id": 101 }\)) has been modified by Alicia:                     |                        |           |
|                                                                        |                        |           |
|   * **Name** : 'Client Second' --&gt; 'Client Seconda'                 |                        |           |
|   * **First name** : 'Second' --&gt; 'Seconda'                         |                        |           |
+------------------------------------------------------------------------+------------------------+-----------+
""")

        # When a coaching is modified, all active coaches of that
        # client get a notification.

        Message.objects.all().delete()
        data = dict(start_date="02.05.2014", an="grid_put")
        data.update(mt=51)
        data.update(mk=second.pk)
        kwargs = dict(data=urlencode(data))
        kwargs['REMOTE_USER'] = 'alicia'
        url = '/api/pcsw/CoachingsByClient/{}'.format(second_roger.pk)
        res = self.client.put(url, **kwargs)
        self.assertEqual(res.status_code, 200)

        self.check_notifications("""
+-----------------------------------------------------+------------------------+-----------+
| Body                                                | Controlled by          | Recipient |
+=====================================================+========================+===========+
| **roger / Client S** has been modified by Alicia:   | *CLIENT Seconda (101)* | roger     |
|                                                     |                        |           |
|   * **Coached from** : 2014-05-01 --&gt; 2014-05-02 |                        |           |
+-----------------------------------------------------+------------------------+-----------+
""")

        # AssignCoach. we are going to Assign caroline as coach for
        # first client.

        # Request URL:http://127.0.0.1:8000/api/newcomers/AvailableCoachesByClient/5?_dc=1469707129689&fv=EVERS%20Eberhart%20(127)%20assigned%20to%20Hubert%20Huppertz%20&fv=EVERS%20Eberhart%20(127)%20is%20now%20coached%20by%20Hubert%20Huppertz%20for%20Laufende%20Beihilfe.&fv=false&mt=48&mk=127&an=assign_coach&sr=5
        # Request Method:GET

        # fv:EVERS Eberhart (127) assigned to Hubert Huppertz
        # fv:EVERS Eberhart (127) is now coached by Hubert Huppertz for Laufende Beihilfe.
        # fv:false
        # mt:48
        # mk:127
        # an:assign_coach
        # sr:5

        Message.objects.all().delete()
        # self.assertEqual(Coaching.objects.count(), 1)
        self.check_coachings("""
==== ====================== ============== ============ ========== =========
 ID   Client                 Coached from   until        Coach      Primary
---- ---------------------- -------------- ------------ ---------- ---------
 1    CLIENT Seconda (101)   01/05/2013     01/05/2014   caroline   No
 2    CLIENT Seconda (101)   02/05/2014                  roger      No
 3    CLIENT Seconda (101)   20/05/2014                  Alicia     No
==== ====================== ============== ============ ========== =========
""")

        self.assertEqual(Note.objects.count(), 0)

        data = dict(
            fv=["First CLIENT assigned to caroline", "Body", 'false'],
            an="assign_coach")
        data.update(mt=ContentType.objects.get_for_model(Client).pk)
        data.update(mk=first.pk)
        kwargs = dict(data=data)
        # kwargs = dict(data=urlencode(data))
        kwargs['REMOTE_USER'] = 'alicia'
        url = '/api/newcomers/AvailableCoachesByClient/{}'.format(
            caroline.pk)
        res = self.client.get(url, **kwargs)
        self.assertEqual(res.status_code, 200)

        # self.check_notifications()
        self.check_notifications("""
======================================== =============== ===========
 Body                                     Controlled by   Recipient
---------------------------------------- --------------- -----------
 First CLIENT assigned to caroline Body                   caroline
======================================== =============== ===========
""")

        self.check_coachings("""
==== ====================== ============== ============ ========== =========
 ID   Client                 Coached from   until        Coach      Primary
---- ---------------------- -------------- ------------ ---------- ---------
 1    CLIENT Seconda (101)   01/05/2013     01/05/2014   caroline   No
 2    CLIENT Seconda (101)   02/05/2014                  roger      No
 3    CLIENT Seconda (101)   20/05/2014                  Alicia     No
 4    CLIENT First (100)     22/05/2014                  caroline   No
==== ====================== ============== ============ ========== =========
""")

        self.check_notes("""
==== ======== ==================== ===================================
 ID   Author   Client               Subject
---- -------- -------------------- -----------------------------------
 1    Alicia   CLIENT First (100)   First CLIENT assigned to caroline
==== ======== ==================== ===================================
""")

        # Mark client as former

        # Request URL:http://127.0.0.1:8000/api/pcsw/Clients/181?_dc=1469714189945&an=mark_former&sr=181
        # Request Method:GET
        # an:mark_former

        Message.objects.all().delete()
        Note.objects.all().delete()

        data = dict(an="mark_former")
        kwargs = dict(data=data)
        # kwargs = dict(data=urlencode(data))
        kwargs['REMOTE_USER'] = 'alicia'
        url = '/api/pcsw/Clients/{}'.format(second.pk)
        res = self.client.get(url, **kwargs)
        self.assertEqual(res.status_code, 200)
        res = AttrDict(json.loads(res.content))
        self.assertEqual(
            res.message, 'This will end 2 coachings of CLIENT Seconda (101).')

        self.assertEqual(res.xcallback['title'], "Confirmation")
        kwargs = dict()
        kwargs['REMOTE_USER'] = 'alicia'
        url = '/callbacks/{}/yes'.format(res.xcallback['id'])
        res = self.client.get(url, **kwargs)
        self.assertEqual(res.status_code, 200)
        res = AttrDict(json.loads(res.content))
        self.assertEqual(
            res.message,
            'Alicia marked CLIENT Seconda (101) as <b>Former</b>.')
        self.assertTrue(res.success)

        self.check_notifications("""
=================================================== ======================== ===========
 Body                                                Controlled by            Recipient
--------------------------------------------------- ------------------------ -----------
 Alicia marked CLIENT Seconda (101) as **Former**.   *CLIENT Seconda (101)*   roger
=================================================== ======================== ===========
""")

        # check two coachings have now an end_date set:
        self.check_coachings("""
==== ====================== ============== ============ ========== =========
 ID   Client                 Coached from   until        Coach      Primary
---- ---------------------- -------------- ------------ ---------- ---------
 1    CLIENT Seconda (101)   01/05/2013     01/05/2014   caroline   No
 2    CLIENT Seconda (101)   02/05/2014     22/05/2014   roger      No
 3    CLIENT Seconda (101)   20/05/2014     22/05/2014   Alicia     No
 4    CLIENT First (100)     22/05/2014                  caroline   No
==== ====================== ============== ============ ========== =========
""")
        self.check_notes("""
==== ======== ====================== ======================================================
 ID   Author   Client                 Subject
---- -------- ---------------------- ------------------------------------------------------
 2    Alicia   CLIENT Seconda (101)   Alicia marked CLIENT Seconda (101) as <b>Former</b>.
==== ======== ====================== ======================================================
""")

        #
        # RefuseClient
        #

        Message.objects.all().delete()
        Note.objects.all().delete()

        data = dict(fv=["20", ""], an="refuse_client")
        kwargs = dict(data=data)
        # kwargs = dict(data=urlencode(data))
        kwargs['REMOTE_USER'] = 'alicia'
        url = '/api/pcsw/Clients/{}'.format(first.pk)
        res = self.client.get(url, **kwargs)
        self.assertEqual(res.status_code, 200)
        self.check_notifications("""
======================================================================== ====================== ===========
 Body                                                                     Controlled by          Recipient
------------------------------------------------------------------------ ---------------------- -----------
 Alicia marked CLIENT First (100) as **Refused**. PCSW is not competent   *CLIENT First (100)*   caroline
======================================================================== ====================== ===========
""")
        self.check_notes("""
==== ======== ==================== =====================================================
 ID   Author   Client               Subject
---- -------- -------------------- -----------------------------------------------------
 3    Alicia   CLIENT First (100)   Alicia marked CLIENT First (100) as <b>Refused</b>.
==== ======== ==================== =====================================================
""")

