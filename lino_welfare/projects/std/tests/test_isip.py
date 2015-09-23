# -*- coding: utf-8 -*-
# Copyright 2014-2015 Luc Saffre
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

"""This module contains "quick" tests that are run on a demo database
without any fixture. You can run only these tests by issuing::

  $ cd lino_welfare/projects/std
  $ python manage.py test tests.test_isip

"""

from __future__ import unicode_literals
from __future__ import print_function

import logging
logger = logging.getLogger(__name__)

from django.conf import settings
from lino.utils.djangotest import RemoteAuthTestCase

from lino.utils import i2d
from lino.modlib.cal.utils import WORKDAYS
from lino.modlib.users.choicelists import UserProfiles
from lino.modlib.system.mixins import Genders


def create(model, **kwargs):
    obj = model(**kwargs)
    obj.full_clean()
    obj.save()
    return obj
    

class QuickTest(RemoteAuthTestCase):
    maxDiff = None

    def test01(self):
        from lino.api.shell import cal, pcsw, isip, users, contacts

        users.User(username="robin",
                   profile=UserProfiles.admin,
                   language="en").save()
        ses = settings.SITE.login('robin')

        # room = create(cal.Room, name="First Room")
        here = create(cal.EventType, name="Consultation here")

        sc = settings.SITE.site_config
        settings.SITE.ignore_dates_after = i2d(20161231)
        sc.signer1 = create(contacts.Person,
                            first_name="A",
                            last_name="Secretary")
        sc.signer2 = create(contacts.Person,
                            first_name="B",
                            last_name="President")
        sc.save()
        
        kw = dict()
        kw.update(first_name="Max")
        kw.update(last_name="Mustermann")
        kw.update(
            gender=Genders.male,
            client_state=pcsw.ClientStates.coached)
        client = create(pcsw.Client, **kw)

        kw = dict()
        for d in WORKDAYS:
            kw[d.name] = True
        kw.update(
            event_type=here,
            name="Every 3 months",
            every_unit=cal.Recurrencies.monthly,
            every=3,
            max_events=10)
        exam_policy = create(isip.ExamPolicy, **kw)

        ctype = create(
            isip.ContractType,
            exam_policy=exam_policy,
            name="Simple",
        )

        kw = dict()
        kw.update(
            client=client,
            type=ctype,
            applies_from=i2d(20140401),
            applies_until=i2d(20150331)
        )

        obj = create(isip.Contract, **kw)

        self.assertEqual(unicode(obj), "ISIP#1 (Max MUSTERMANN)")

        settings.SITE.verbose_client_info_message = True

        """Run do_update_events a first time

        """

        res = ses.run(obj.do_update_events)
        self.assertEqual(res['success'], True)

        # note how this will generate 3 events, and for each event one
        # guest.
        expected = """\
Update Events for ISIP#1 (Max MUSTERMANN)...
Generating events between 2014-07-01 and 2015-03-31.
Reached upper date limit 2015-03-31
Update Guests for Event #1 Evaluation 1 (01.07.2014)...
0 row(s) have been updated.
Update Guests for Event #2 Evaluation 2 (01.10.2014)...
0 row(s) have been updated.
Update Guests for Event #3 Evaluation 3 (01.01.2015)...
0 row(s) have been updated.
3 row(s) have been updated."""
        # print(expected)
        self.assertEqual(res['info_message'], expected)

        ar = ses.spawn(cal.EventsByController, master_instance=obj)
        s = ar.to_rst(column_names="start_date state")
        # print(s)
        self.assertEqual(s, """\
============ ===========
 Start date   State
------------ -----------
 7/1/14       Suggested
 10/1/14      Suggested
 1/1/15       Suggested
============ ===========

""")


# __all__ = ['QuickTest']
