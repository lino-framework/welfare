# -*- coding: UTF-8 -*-
# Copyright 2014-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""Runs some tests about reading eID cards.

You can run only these tests by issuing::

  $ go welfare
  $ cd lino_welfare/projects/std
  $ python manage.py test tests.test_beid

"""

from __future__ import unicode_literals
from __future__ import print_function

import logging
logger = logging.getLogger(__name__)

import os

from lino.utils.djangotest import RemoteAuthTestCase
from django.utils.datastructures import MultiValueDict
from lino.mixins.repairable import repairdata
from lino.utils import ssin


def readfile(name):
    fn = os.path.join(os.path.dirname(__file__), name)
    return open(fn).read()


class WebRequest:
    method = "POST"
    subst_user = None
    requesting_panel = None

    def __init__(self, user, data):
        self.POST = self.REQUEST = MultiValueDict(data)
        self.user = user


class BeIdTests(RemoteAuthTestCase):
    maxDiff = None
    override_djangosite_settings = dict(use_java=True)

    def test01(self):
        from lino.core import constants
        from django.conf import settings
        from lino.modlib.users.choicelists import UserProfiles
        from lino.modlib.beid.mixins import holder_model
        Holder = holder_model()
        
        from lino.api.shell import countries, addresses, pcsw, users

        # is it the right settings module?
        self.assertEqual(os.environ['DJANGO_SETTINGS_MODULE'],
                         'lino_welfare.projects.std.settings.demo')

        self.assertEqual(settings.MIDDLEWARE_CLASSES, (
            'django.middleware.common.CommonMiddleware',
            'django.middleware.locale.LocaleMiddleware',
            'lino.core.auth.RemoteUserMiddleware',
            'lino.utils.ajax.AjaxExceptionResponse'))

        u = users.User(username='root',
                       profile=UserProfiles.admin,
                       language="en")
        u.save()
        be = countries.Country(name="Belgium", isocode="BE")
        be.save()
        kw = dict()
        # kw.update(card_number="123456789")
        # kw.update(national_id="680601 053-29")
        kw.update(first_name="Jean")
        kw.update(middle_name="Jacques")
        kw.update(last_name="Jeffin")
        obj = Holder(**kw)
        obj.full_clean()
        obj.save()

        url = '/api/pcsw/Clients'
        post_data = dict()
        post_data.update(
            card_data=readfile('beid_tests_1.txt'))
        post_data[constants.URL_PARAM_ACTION_NAME] = 'find_by_beid'

        # First attempt fails because a person with exactly the same
        # name already exists.
        response = self.client.post(
            url, post_data,
            REMOTE_USER='root',
            HTTP_ACCEPT_LANGUAGE='en')
        result = self.check_json_result(response, 'alert success message')
        self.assertEqual(result['success'], False)
        expected = ("Sorry, I cannot handle that case: Cannot create "
                    "new client because there is already a person named "
                    "Jean Jacques Jeffin in our database.")
        self.assertEqual(result['message'], expected)

        # Second attempt. We are reading the same card, but this time
        # there is a person with this `national_id`.
        obj.national_id = "680601 053-29"
        # obj.first_name = "Jean-Claude"
        obj.full_clean()
        obj.save()
        response = self.client.post(
            url, post_data,
            REMOTE_USER='root',
            HTTP_ACCEPT_LANGUAGE='en')
        # self.assertEqual(response.content, '')
        result = self.check_json_result(
            response,
            'xcallback success message')
        self.assertEqual(result['success'], True)
        expected = """\
Click OK to apply the following changes for JEFFIN Jean (100) :\
<br/>City : None -> Place #1 (u'Tallinn')
<br/>Gender : None -> <Genders.male:M>
<br/>until : None -> 2016-08-19
<br/>Street : '' -> 'Estland'
<br/>ID card valid from : None -> 2011-08-19
<br/>eID card type : None -> <BeIdCardTypes.belgian_citizen:1>
<br/>eID card issuer : '' -> 'Tallinn'
<br/>Birth place : '' -> 'Mons'
<br/>Country : None -> Country #BE (u'Belgium')
<br/>Birth date : '' -> 1968-06-01
<br/>eID card number : '' -> '592345678901'
<br/>Zip code : '' -> '1418'"""
        # print(result['message'])
        self.assertEqual(result['message'], expected)

        # ... and we answer yes:

        cb = result['xcallback']
        self.assertEqual(cb['title'], "Confirmation")
        self.assertEqual(cb['buttons'], {'yes': 'Yes', 'no': 'No'})
        url = '/callbacks/%d/yes' % cb['id']
        response = self.client.get(
            url,
            REMOTE_USER='root',
            HTTP_ACCEPT_LANGUAGE='en')
        result = self.check_json_result(
            response,
            'detail_handler_name data_record alert success message')
        self.assertEqual(result['success'], True)
        self.assertEqual(
            result['message'],
            'Client "JEFFIN Jean (100)" has been saved.')
        obj = pcsw.Client.objects.get(id=100)
        addr = addresses.Address.objects.get(partner=obj)
        self.assertEqual(addr.city.name, "Tallinn")
        self.assertEqual(addr.primary, True)

        # Third attempt. A person with almost same name and same
        # national_id.

        url = '/api/pcsw/Clients'
        obj.national_id = "680601 053-29"
        obj.first_name = "Jean-Jacques"
        obj.middle_name = ""
        obj.full_clean()
        obj.save()
        response = self.client.post(
            url, post_data,
            REMOTE_USER='root',
            HTTP_ACCEPT_LANGUAGE='en')
        # self.assertEqual(response.content, '')
        result = self.check_json_result(
            response,
            'xcallback success message')
        self.assertEqual(result['success'], True)
        expected = """\
Click OK to apply the following changes for JEFFIN Jean (100) :<br/>First name : 'Jean-Jacques' -> 'Jean'
<br/>Middle name : '' -> 'Jacques'"""
        # print(result['message'])
        self.assertEqual(result['message'], expected)

        # Fourth attempt. A person with slightly different name and
        # equivalent but wrongly formatted national_id exists.  Lino
        # does not recognize this duplicate here. To avoid this case,
        # the StrangeClients table warns about wrongly formatted
        # national_id fields.

        ssin.parse_ssin('68060105329')
        url = '/api/pcsw/Clients'
        obj.national_id = "68060105329"
        obj.first_name = "Jean-Jacques"
        obj.middle_name = ""
        # obj.client_state = pcsw.ClientStates.coached
        obj.full_clean()
        obj.save()
        response = self.client.post(
            url, post_data,
            REMOTE_USER='root',
            HTTP_ACCEPT_LANGUAGE='en')
        # self.assertEqual(response.content, '')
        result = self.check_json_result(
            response,
            'xcallback success message')
        self.assertEqual(result['success'], True)
        expected = "Create new client Jean Jacques Jeffin : Are you sure?"
        # print(result['message'])
        self.assertEqual(result['message'], expected)

        # two methods to test whether the StrangeClients table
        # actually would have warned:

        ar = pcsw.StrangeClients.request()
        self.assertEqual(ar.get_total_count(), 1)
        self.assertEqual(
            ar[0].error_message,
            "Invalid SSIN 68060105329 : "
            "A formatted SSIN must have 13 positions")

        # second method to test the same result:

        s = pcsw.StrangeClients.request().to_rst()
        self.assertEqual(s, """\
=========================== ==================================================================== ===============
 Name                        Error message                                                        Primary coach
--------------------------- -------------------------------------------------------------------- ---------------
 JEFFIN Jean-Jacques (100)   Invalid SSIN 68060105329 : A formatted SSIN must have 13 positions
=========================== ==================================================================== ===============
""")

        g = '\n'.join(repairdata(really=False))
        e = """\
JEFFIN Jean-Jacques (100) : Malformed SSIN '68060105329' must be '680601 053-29'."""
        # print(g)
        self.assertEqual(g, e)

        g = '\n'.join(repairdata(really=True))
        # print(g)
        self.assertEqual(g, e)

        g = '\n'.join(repairdata(really=False))
        # print(g)
        self.assertEqual(g, '')
        
        # Last attempt for this card. No similar person exists. Create
        # new client from eid.

        obj.first_name = "Jean-Claude"
        obj.national_id = ""
        obj.full_clean()
        obj.save()
        url = '/api/pcsw/Clients'
        response = self.client.post(
            url, post_data,
            REMOTE_USER='root',
            HTTP_ACCEPT_LANGUAGE='en')
        # self.assertEqual(response.content, '')
        result = self.check_json_result(
            response,
            'xcallback success message')
        self.assertEqual(result['success'], True)
        expected = "Create new client Jean Jacques Jeffin : Are you sure?"
        self.assertEqual(result['message'], expected)

        # next card. a foreigner card with incomplete birth date

        post_data.update(card_data=readfile('beid_tests_2.txt'))
        url = '/api/pcsw/Clients'
        response = self.client.post(
            url, post_data,
            REMOTE_USER='root',
            HTTP_ACCEPT_LANGUAGE='en')
        # self.assertEqual(response.content, '')
        result = self.check_json_result(
            response,
            'xcallback success message')
        self.assertEqual(result['success'], True)
        expected = "Create new client Marc Petitjean : Are you sure?"
        self.assertEqual(result['message'], expected)
