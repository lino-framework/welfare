# -*- coding: UTF-8 -*-
# Copyright 2015 Luc Saffre
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

"""Runs some tests about dupe clients.

You can run only these tests by issuing::

  $ go welfare
  $ cd lino_welfare/projects/std
  $ python manage.py test tests.test_dupe_clients

"""

from __future__ import unicode_literals
from __future__ import print_function

from lino.utils.djangotest import RemoteAuthTestCase
from lino.api import rt


class TestCase(RemoteAuthTestCase):
    fixtures = ['few_countries', 'few_cities', 'demo_users']

    def test(self):
        Client = rt.modules.pcsw.Client
        Word = rt.modules.dupable_clients.Word

        argnames = "first_name last_name birth_date national_id".split()

        def C(*args):
            kw = dict()
            for i, v in enumerate(args):
                kw[argnames[i]] = v
            obj = Client(**kw)
            obj.full_clean()
            obj.save()
            obj.update_dupable_words(True)  # update phonetic words
            return obj

        jj1 = C("Nemard", "Jean", "1948-04-27", "480427 001-29")
        jj2 = C("Nemard", "Jean", "1968-06-01", "680601 053-29")

        # The `dupable_matches_required` feature is currently not
        # used, we always check for two matching words:
        self.assertEqual(jj1.dupable_matches_required(), 2)
        self.assertEqual(jj2.dupable_matches_required(), 2)

        # Verify that the phonetic words have been updated:
        s = ' '.join(map(unicode, Word.objects.all()))
        self.assertEqual(s, "JN NMRT JN NMRT")
        self.assertEqual(Word.objects.all().count(), 4)

        def jjcheck(*expected):
            s1 = [o.pk for o in jj1.find_similar_instances()]
            s2 = [o.pk for o in jj2.find_similar_instances()]
            for i in s1:
                if i in s2:
                    self.fail("Oops")
            s = set(s1 + s2)
            self.assertEqual(s, set(expected))

        # Initial situation: both national_id and birth_date are given
        # and different
        jjcheck()   # no similar clients detected

        # one client's national_id is missing
        jj1.national_id = ""
        jj1.save()
        jjcheck()

        # one client's birth_date is missing
        jj1.national_id = "480427 001-29"
        jj1.birth_date = ""
        jj1.save()
        jjcheck()

        # both national_id and birth_date are missing for one client
        jj1.national_id = ""
        jj1.birth_date = ""
        jj1.save()
        jjcheck(100, 101)

        # both national_id and birth_date are missing for both clients
        jj2.national_id = ""
        jj2.birth_date = ""
        jj2.save()
        jjcheck(100, 101)

        # Now some checks just on names
        def check2(fn1, ln1, fn2, ln2, similar):
            Client.objects.all().delete()
            Word.objects.all().delete()
            o1 = C(fn1, ln1)
            o2 = C(fn2, ln2)
            s1 = o1.find_similar_instances()
            s2 = o2.find_similar_instances()
            self.assertEqual(o1 in s2, similar)
            self.assertEqual(o2 in s1, similar)
            
        check2("Jean", "Nemard", "Jacques", "Nemard", False)
        check2("Jean", "Nemard", "Jean-Jacques", "Nemard", True)
        check2("Jean-Jacques", "Nemard", "Jean-Jacques", "Vandenberg", False)
        check2("Jean-Jacques", "Nemard", "Jean-Jacques", "Namard", True)
        check2("Jean-Jacques", "Nemard", "Jean-Jacques", "Nomard", True)
        check2("Jean-Jacques", "Nemard", "Jean-Jacques", "Homard", False)

        # common family name prefixes make no difference:

        check2("Norbert", "Berg", "Norbert", "van Berg", True)
        check2("Norbert", "Berg", "Norbert", "van den Berg", True)
        check2("Norbert", "Berg", "Lydia", "van Berg", False)
        check2("Norbert", "Berg", "Lydia", "van den Berg", False)
        check2("Norbert", "van Berg", "Lydia", "van Berg", False)
        check2("Norbert", "van den Berg", "Lydia", "van den Berg", False)

