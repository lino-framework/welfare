# -*- coding: utf-8 -*-
# Copyright 2017 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

"""

  $ cd lino_welfare/projects/eupen
  $ python manage.py test tests.test_clients

"""

from __future__ import unicode_literals
from __future__ import print_function

import logging
logger = logging.getLogger(__name__)

from django.conf import settings
from lino.utils.djangotest import RemoteAuthTestCase

from lino.utils import i2d
from lino_xl.lib.cal.choicelists import WORKDAYS
from lino_xl.lib.clients.choicelists import ClientStates
from lino.modlib.users.choicelists import UserTypes
from lino.modlib.system.choicelists import Genders
from lino.utils.instantiator import create_row as create
from lino.api import rt


# def create(model, **kwargs):
#     obj = model(**kwargs)
#     obj.full_clean()
#     obj.save()
#     return obj
    

class QuickTest(RemoteAuthTestCase):
    maxDiff = None

    def test01(self):
        # print("20180503 test_clients.test01()")
        from lino.api.shell import pcsw, users
        # NoteType = rt.models.notes.NoteType
        EventType = rt.models.notes.EventType
        Note = rt.models.notes.Note
        Coaching = rt.models.coachings.Coaching
        Message = rt.models.notify.Message

        robin = create(
            users.User, username="robin",
            user_type=UserTypes.admin,
            language="fr")
        
        self.client.force_login(robin)
        aline = create(
            users.User,
            username="aline",
            user_type=UserTypes.admin,
            language="fr")
        

        nt = create(EventType, name="System note")
        settings.SITE.site_config.update(system_note_type=nt)

        kw = dict()
        kw.update(first_name="Max")
        kw.update(last_name="Mustermann")
        kw.update(
            gender=Genders.male,
            client_state=ClientStates.newcomer)
        obj = create(pcsw.Client, **kw)
        create(Coaching, client=obj, user=aline)

        # settings.SITE.verbose_client_info_message = True

        """Run do_update_events a first time

        """

        url = "/api/pcsw/Clients/{0}?sr={0}".format(obj.pk)
        reason = "Wohnt%20noch%20in%20L%C3%BCttich.%20Wollte%20nach%20Eupen%20ziehen.%20Noch%20nicht%20zust%C3%A4ndig"
        url += "&fv=20&fv={}g&an=refuse_client".format(reason)

        response = self.client.get(url, REMOTE_USER='robin')
        result = self.check_json_result(
            response, 'message close_window success alert')

        self.assertEqual(result['success'], True)

        expected = """\
robin a class\xe9 MUSTERMANN Max (100) comme <b>Refus\xe9</b>."""
        # print(expected)
        self.assertEqual(expected, result['message'])
        self.assertEqual(Note.objects.count(), 1)
        self.assertEqual(Message.objects.count(), 1)
        msg = Message.objects.all()[0]
        expected = """\
robin a classé [client 100] (M. Max MUSTERMANN) comme <b>Refusé</b>.
Raison de refus: CPAS n'est pas compétent
Wohnt noch in Lüttich. Wollte nach Eupen ziehen. Noch nicht zuständigg"""
        self.assertEqual(expected, msg.body)
        
        # print("20180503 test_clients.test01() done")
