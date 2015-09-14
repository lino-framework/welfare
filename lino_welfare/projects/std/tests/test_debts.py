# -*- coding: UTF-8 -*-
# Copyright 2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""Some test cases for :mod:`lino_welfare.modlib.debts`.

How to run only this test::

  $ go welfare
  $ cd lino_welfare/projects/std
  $ python manage.py test tests.test_debts

"""

from __future__ import unicode_literals
from __future__ import print_function

import logging
logger = logging.getLogger(__name__)

import os
import json
from bs4 import BeautifulSoup


from lino.utils.djangotest import RemoteAuthTestCase
from lino.utils import AttrDict
from django.utils.datastructures import MultiValueDict

from django.conf import settings
from lino.modlib.users.choicelists import UserProfiles
from lino.api.shell import countries, pcsw, users
from lino.api import rt


def readfile(name):
    fn = os.path.join(os.path.dirname(__file__), name)
    return open(fn).read()


class DebtsTests(RemoteAuthTestCase):
    maxDiff = None
    # override_djangosite_settings = dict(use_java=True)

    def test01(self):

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
        # be = countries.Country(name="Belgium", isocode="BE")
        # be.save()
        # kw = dict()
        # # kw.update(card_number="123456789")
        # # kw.update(national_id="680601 053-29")
        # kw.update(id=116)
        # kw.update(first_name="Jean")
        # kw.update(middle_name="Jacques")
        # kw.update(last_name="Jeffin")
        # obj = pcsw.Client(**kw)
        # obj.full_clean()
        # obj.save()

        # from lino.modlib.households.fixtures.std import objects
        # for o in objects():
        #     o.save()

        # Reproduce ticket #521
        ar = rt.login('root')
        # Member = rt.modules.households.Member
        Household = rt.modules.households.Household
        Person = rt.modules.contacts.Person
        Genders = rt.modules.system.Genders
        Budget = rt.modules.debts.Budget
        
        p1 = Person(first_name="A", last_name="A", gender=Genders.male)
        p1.save()
        p2 = Person(first_name="B", last_name="B", gender=Genders.female)
        p2.save()
        h = Household.create_household(ar, p1, p2, None)

        # The household has for whatever reason an empty member
        # entry. Lino should ignore this entry.
        h.add_member(None)

        b = Budget(partner=h)
        b.save()
        b.fill_defaults()
        # from django.utils.encoding import force_unicode
        # s = ' & '.join([force_unicode(a) for a in b.get_actors()])
        # s = '{0} & {1}'.format(*b.get_actors())
        # self.assertEqual(s, "Mr. & Mrs.")
        
