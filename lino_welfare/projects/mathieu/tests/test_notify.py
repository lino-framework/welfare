# -*- coding: UTF-8 -*-
# Copyright 2016-2018 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

"""
Miscellaneous tests about the notification framework
(:mod:`lino.modlib.notify` and :mod:`lino_xl.lib.notes`). Consult the
source code of this module.

You can run these tests individually by issuing::

  $ cd lino_welfare/projects/chatelet
  $ python manage.py test tests.test_notify
"""

from __future__ import unicode_literals
from __future__ import print_function

from builtins import str
import json
from six.moves.urllib.parse import urlencode
import six
from django.conf import settings
from django.utils import translation

from lino.utils.djangotest import TestCase
from lino.utils import i2d, AttrDict

from lino.api import rt

from lino.modlib.users.choicelists import UserTypes


class TestCase(TestCase):
    maxDiff = None

    def check_notifications(self, expected=''):
        """
        Check whether the database contains notification messages as
        expected.

        Hint: when `expected` is empty, then the found result is being
        printed to stdout so you can copy it into your code.
        """
        ar = rt.models.notify.Messages.request()
        rst = ar.to_rst(column_names="subject owner user")
        if expected:
            self.assertEquivalent(expected, rst)
        else:
            print(rst)
        # print rst  # handy when something fails

    def check_notes(self, expected=''):
        ar = rt.models.notes.Notes.request()
        rst = ar.to_rst(column_names="id user project subject")
        if expected:
            self.assertEquivalent(expected, rst)
        else:
            print(rst)

    def check_coachings(self, expected=''):
        ar = rt.models.coachings.Coachings.request()
        rst = ar.to_rst(
            column_names="id client start_date end_date user primary")
        if expected:
            self.assertEquivalent(expected, rst)
        else:
            print(rst)

    def test_checkin_guest(self):
        """Test whether notifications are being emitted.

        - when a visitor checks in
        - when a client is modified
        - when a coaching is created or modified
        - when a note is created or modified

        """
        User = settings.SITE.user_model
        Message = rt.models.notify.Message
        Note = rt.models.notes.Note
        NoteType = rt.models.notes.EventType
        Guest = rt.models.cal.Guest
        Event = rt.models.cal.Event
        EventType = rt.models.cal.EventType
        Client = rt.models.pcsw.Client
        ClientStates = rt.models.pcsw.ClientStates
        Coaching = rt.models.coachings.Coaching
        ContentType = rt.models.contenttypes.ContentType

        self.assertEqual(settings.SITE.use_websockets, False)

        robin = self.create_obj(
            User, username='robin',
            user_type=UserTypes.admin, language="en")
        caroline = self.create_obj(
            User, username='caróline',
            user_type='200', language="fr")
        alicia = self.create_obj(
            User, username='alícia', first_name="Alicia",
            user_type='120', language="fr")
        roger = self.create_obj(
            User, username='róger', user_type='420',
            language="en")

        ses = rt.login('robin')
        translation.activate('fr')

        first = self.create_obj(
            Client, first_name="First", last_name="Gérard",
            client_state=ClientStates.coached)

        second = self.create_obj(
            Client, first_name="Second", last_name="Gérard",
            client_state=ClientStates.coached)
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
        settings.SITE.site_config.update(system_note_type=nt)

        consultation = self.create_obj(EventType, name="consultation")

        # gr = self.create_obj(GuestRole, name="client")

        event = self.create_obj(
            Event, event_type=consultation, user=caroline)
        guest = self.create_obj(Guest, event=event, partner=first)

        self.assertEqual(str(guest), 'Présence #1 (22.05.2014)')

        # Checkin a guest

        res = ses.run(guest.checkin)
        # 'GÉRARD First (100) has started waiting for caroline'
        self.assertEqual(res, {
            'message': "GÉRARD First (100) a commencé d'attendre caróline",
            'success': True, 'refresh': True})

        # it has caused a notification message:
        self.assertEqual(Message.objects.count(), 1)
        msg = Message.objects.all()[0]
        self.assertEqual(msg.user.username, 'caróline')

        self.assertEqual(
            msg.subject,
            "GÉRARD First (100) a commencé d'attendre caróline")

        # it does *not* cause a system note:
        self.assertEqual(Note.objects.count(), 0)
        
        

        # When a client is modified, all active coaches get a
        # notification.
        # Note that Caroline doesn't get a notification because her
        # coaching is not active.
        # Alicia doesn't get a notification because she did it herself.
        # Roger doesn't get notified because he is user_type 420

        data = dict(first_name="Seconda", an="submit_detail")
        kwargs = dict(data=urlencode(data))
        kwargs['REMOTE_USER'] = 'alícia'
        url = '/api/pcsw/Clients/{}'.format(second.pk)
        self.client.force_login(alicia)
        res = self.client.put(url, **kwargs)
        self.assertEqual(res.status_code, 200)

        # self.assertEqual(Message.objects.count(), 2)
        # self.check_notifications()
        self.check_notifications("""
=================================================== ======= ==============
 Sujet                                               Lié à   Destinataire
--------------------------------------------------- ------- --------------
 GÉRARD First (100) a commencé d'attendre caróline           caróline
=================================================== ======= ==============
""")

        # When a coaching is modified, all active coaches of that
        # client get a notification.

        Message.objects.all().delete()
        data = dict(start_date="02.05.2014", an="grid_put")
        data.update(mt=51)
        data.update(mk=second.pk)
        kwargs = dict(data=urlencode(data))
        kwargs['REMOTE_USER'] = 'robin'
        self.client.force_login(robin)
        url = '/api/coachings/CoachingsByClient/{}'.format(second_roger.pk)
        res = self.client.put(url, **kwargs)
        self.assertEqual(res.status_code, 200)

        # self.check_notifications()
        self.check_notifications("""
================================== ==================== ===========
 Subject                            Controlled by        Recipient
---------------------------------- -------------------- -----------
 robin a modifié róger / Gérard S   *róger / Gérard S*   Alicia
================================== ==================== ===========
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
        # self.check_coachings()
        self.check_coachings("""
==== ====================== ============== ============ ========== =========
 ID   Client                 Coached from   until        Coach      Primary
---- ---------------------- -------------- ------------ ---------- ---------
 1    GÉRARD Seconda (101)   01/05/2013     01/05/2014   caróline   No
 2    GÉRARD Seconda (101)   02/05/2014                  róger      No
 3    GÉRARD Seconda (101)   20/05/2014                  Alicia     No
==== ====================== ============== ============ ========== =========
""")

        self.assertEqual(Note.objects.count(), 0)

        data = dict(
            fv=["First GÉRARD assigned to caróline", "Body", 'false'],
            an="assign_coach")
        data.update(mt=ContentType.objects.get_for_model(Client).pk)
        data.update(mk=first.pk)
        kwargs = dict(data=data)
        # kwargs = dict(data=urlencode(data))
        kwargs['REMOTE_USER'] = 'alícia'
        self.client.force_login(alicia)
        url = '/api/newcomers/AvailableCoachesByClient/{}'.format(
            caroline.pk)
        res = self.client.get(url, **kwargs)
        self.assertEqual(res.status_code, 200)

        self.check_notifications("""
=================================== ======= ==============
 Sujet                               Lié à   Destinataire
----------------------------------- ------- --------------
 First GÉRARD assigned to caróline           caróline
=================================== ======= ==============
""")

        # self.check_coachings("")
        self.check_coachings("""
==== ====================== ======================== ============ ============= ==========
 ID   Bénéficiaire           En intervention depuis   au           Intervenant   Primaire
---- ---------------------- ------------------------ ------------ ------------- ----------
 1    GÉRARD Seconda (101)   01/05/2013               01/05/2014   caróline      Non
 2    GÉRARD Seconda (101)   02/05/2014                            róger         Non
 3    GÉRARD Seconda (101)   20/05/2014                            Alicia        Non
 4    GÉRARD First (100)     22/05/2014                            caróline      Oui
==== ====================== ======================== ============ ============= ==========
""")

        self.check_notes("""
==== ======== ==================== ===================================
 ID   Auteur   Bénéficiaire         Sujet
---- -------- -------------------- -----------------------------------
 1    Alicia   GÉRARD First (100)   First GÉRARD assigned to caróline
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
        kwargs['REMOTE_USER'] = 'alícia'
        self.client.force_login(alicia)
        url = '/api/pcsw/Clients/{}'.format(second.pk)
        res = self.client.get(url, **kwargs)
        self.assertEqual(res.status_code, 200)
        res = AttrDict(json.loads(res.content))
        self.assertEqual(
            res.message, 'This will end 2 coachings of GÉRARD Seconda (101).')

        self.assertEqual(res.xcallback['title'], "Confirmation")
        kwargs = dict()
        kwargs['REMOTE_USER'] = 'alícia'
        self.client.force_login(alicia)
        url = '/callbacks/{}/yes'.format(res.xcallback['id'])
        res = self.client.get(url, **kwargs)
        self.assertEqual(res.status_code, 200)
        res = AttrDict(json.loads(res.content))
        self.assertEqual(
            res.message,
            'Alicia a classé GÉRARD Seconda (101) comme <b>Ancien</b>.')
        self.assertTrue(res.success)

        self.check_notifications("""
=========================================================== ======================== ==============
 Sujet                                                       Lié à                    Destinataire
----------------------------------------------------------- ------------------------ --------------
 Alicia a classé GÉRARD Seconda (101) comme <b>Ancien</b>.   *GÉRARD Seconda (101)*   róger
=========================================================== ======================== ==============
""")

        # check two coachings have now an end_date set:
        # self.check_coachings()
        self.check_coachings("""
==== ====================== ======================== ============ ============= ==========
 ID   Bénéficiaire           En intervention depuis   au           Intervenant   Primaire
---- ---------------------- ------------------------ ------------ ------------- ----------
 1    GÉRARD Seconda (101)   01/05/2013               01/05/2014   caróline      Non
 2    GÉRARD Seconda (101)   02/05/2014               22/05/2014   róger         Non
 3    GÉRARD Seconda (101)   20/05/2014               22/05/2014   Alicia        Non
 4    GÉRARD First (100)     22/05/2014                            caróline      Oui
==== ====================== ======================== ============ ============= ==========
""")
        # self.check_notes()
        self.check_notes("""
==== ======== ====================== ===========================================================
 ID   Auteur   Bénéficiaire           Sujet
---- -------- ---------------------- -----------------------------------------------------------
 2    Alicia   GÉRARD Seconda (101)   Alicia a classé GÉRARD Seconda (101) comme <b>Ancien</b>.
==== ======== ====================== ===========================================================
""")

        #
        # RefuseClient
        #

        Message.objects.all().delete()
        Note.objects.all().delete()

        self.create_obj(
            Coaching, client=first, start_date=i2d(20130501), user=roger)
        
        first.client_state = ClientStates.newcomer
        first.save()

        data = dict(fv=["20", ""], an="refuse_client")
        kwargs = dict(data=data)
        # kwargs = dict(data=urlencode(data))
        kwargs['REMOTE_USER'] = 'alícia'
        self.client.force_login(alicia)
        url = '/api/pcsw/Clients/{}'.format(first.pk)
        res = self.client.get(url, **kwargs)
        self.assertEqual(res.status_code, 200)
        # self.check_notifications("")
        #if six.PY2:
        self.check_notifications("""
========================================================= ====================== ==============
Sujet                                                     Lié à                  Destinataire
--------------------------------------------------------- ---------------------- --------------
Alicia a classé GÉRARD First (100) comme <b>Refusé</b>.   *GÉRARD First (100)*   caróline
Alicia a classé GÉRARD First (100) comme <b>Refusé</b>.   *GÉRARD First (100)*   róger
========================================================= ====================== ==============
""")
        # self.check_notes()
        self.check_notes("""
==== ======== ==================== =========================================================
 ID   Auteur   Bénéficiaire         Sujet
---- -------- -------------------- ---------------------------------------------------------
 3    Alicia   GÉRARD First (100)   Alicia a classé GÉRARD First (100) comme <b>Refusé</b>.
==== ======== ==================== =========================================================
""")

        # When a note is created, all active coaches of that
        # client get a notification.

        Message.objects.all().delete()
        data = dict()
        data.update(mt=51)
        data.update(mk=second.pk)
        data.update(an='submit_insert')
        data.update(
            subject="test",
            projectHidden=second.pk)
        
        kwargs = dict(data=data)
        kwargs['REMOTE_USER'] = 'alícia'
        self.client.force_login(alicia)
        url = '/api/notes/NotesByProject/{}'.format(second.pk)
        res = self.client.post(url, **kwargs)
        self.assertEqual(res.status_code, 200)
        res = AttrDict(json.loads(res.content))
        self.assertEqual(res.data_record['id'], 4)
        new_note_pk = res.data_record['id']
        

        # self.check_notifications()
        self.check_notifications("""
============================== ================== ==============
 Sujet                          Lié à              Destinataire
------------------------------ ------------------ --------------
 Alicia created Event/Note #4   *Observation #4*   róger
============================== ================== ==============
""")


        Message.objects.all().delete()
        data = dict()
        data.update(mt=51)
        data.update(mk=second.pk)
        data.update(an='submit_detail')
        data.update(
            subject="test 2",
            body="<p>Bla bla bla</p>",
            projectHidden=second.pk)
        
        kwargs = dict(data=urlencode(data))
        # kwargs = dict(data=data)
        kwargs['REMOTE_USER'] = 'alícia'
        self.client.force_login(alicia)
        url = '/api/notes/NotesByProject/{}'.format(new_note_pk)
        res = self.client.put(url, **kwargs)
        self.assertEqual(res.status_code, 200)
        # self.check_notifications()
        # self.check_notifications("Aucun enregistrement")
        self.check_notifications("""
=============================== ================== ==============
 Sujet                           Lié à              Destinataire
------------------------------- ------------------ --------------
 Alicia modified Event/Note #4   *Observation #4*   róger
=============================== ================== ==============
""")

        
        self.assertEqual(Message.objects.count(), 1)
        msg = Message.objects.all()[0]
        # print msg.body
        self.assertEquivalent(msg.body, """
<div><p>Subject: test 2<br/>Client: [client 101] (Seconda GÉRARD)</p><p>Alicia modified [note 4] (test 2):</p><ul><li><b>Body</b> : 1 lines added</li><li><b>Subject</b> : test --&gt; test 2</li></ul></div>
""")

