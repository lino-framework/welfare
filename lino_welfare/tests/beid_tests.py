# -*- coding: UTF-8 -*-
# Copyright 2014 Luc Saffre
# This file is part of the Lino project.
# Lino is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
# Lino is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with Lino; if not, see <http://www.gnu.org/licenses/>.

"""This module contains "quick" tests that are run on a demo database
without any fixture. You can run only these tests by issuing::

  python manage.py test lino_welfare.tests.beid_tests

"""

from __future__ import unicode_literals

import logging
logger = logging.getLogger(__name__)

import os

from lino import dd
from lino.runtime import *
from djangosite.utils.djangotest import RemoteAuthTestCase
from django.utils.datastructures import MultiValueDict

# from ..mixins import holder_model

Holder = pcsw.Client  #  holder_model()


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

    def test01(self):
        self.assertEqual(1+1, 2)
        u = users.User(username='root', profile=dd.UserProfiles.admin)
        u.save()
        be = countries.Country(name="Belgium", isocode="BE")
        be.save()
        kw = dict()
        kw.update(card_number="123456789")
        kw.update(first_name="Jean Jacques")
        kw.update(last_name="Jéffin")
        obj = Holder(**kw)
        obj.full_clean()
        obj.save()
        data = readfile('beid_tests_1.txt')
        url = '/api/pcsw/Clients'
        res = self.client.post(
            url,
            REMOTE_USER='root',
            HTTP_ACCEPT_LANGUAGE='en',
            an='read_beid', card_data=data)
        
        # request = WebRequest(u, dict(card_data=[data]))
        # ses = settings.SITE.login('test', request=request)
        # rv = obj.read_beid.run_from_code(ses)
        self.assertEqual(res, 42)

__all__ = ['BeIdTests']
