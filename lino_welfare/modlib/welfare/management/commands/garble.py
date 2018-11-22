# -*- coding: UTF-8 -*-
# Copyright 2009-2014 Rumma & Ko Ltd
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
# along with Lino ; if not, see <http://www.gnu.org/licenses/>.

"""

Garbles person names in the database so that it may be used for a demo.

"""

from builtins import str
from optparse import make_option

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from lino.utils import dblogger
from lino.utils import Cycler, join_words

from lino import mixins
from lino.api import dd, rt


from lino.utils import confirm

from lino.utils import demonames as demo


def last_names():
    yield demo.LAST_NAMES_BELGIUM
    yield demo.LAST_NAMES_MUSLIM
    yield demo.LAST_NAMES_BELGIUM
    yield demo.LAST_NAMES_RUSSIA
    yield demo.LAST_NAMES_BELGIUM
    yield demo.LAST_NAMES_AFRICAN
LAST_NAMES = Cycler(last_names())


def male_first_names():
    yield demo.MALE_FIRST_NAMES_FRANCE
    yield demo.MALE_FIRST_NAMES_MUSLIM
    yield demo.MALE_FIRST_NAMES_FRANCE
    yield demo.MALE_FIRST_NAMES_RUSSIA
    yield demo.MALE_FIRST_NAMES_FRANCE
    yield demo.MALE_FIRST_NAMES_AFRICAN
MALES = Cycler(male_first_names())


def female_first_names():
    yield demo.FEMALE_FIRST_NAMES_FRANCE
    yield demo.FEMALE_FIRST_NAMES_MUSLIM
    yield demo.FEMALE_FIRST_NAMES_FRANCE
    yield demo.FEMALE_FIRST_NAMES_RUSSIA
    yield demo.FEMALE_FIRST_NAMES_FRANCE
    yield demo.FEMALE_FIRST_NAMES_AFRICAN
FEMALES = Cycler(female_first_names())

NATIONALITIES = Cycler('BE', 'MA', 'BE', 'RU', 'BE', 'CD')

#~ print 'Done'


class Command(BaseCommand):
    args = '(no arguments)'
    help = 'Garbles person names in the database so that it may be used for a demo.'

    option_list = BaseCommand.option_list + (
        make_option(
            '--noinput', action='store_false', dest='interactive', default=True,
            help='Do not prompt for input of any kind.'),
    )

    def handle(self, *args, **options):

        dbname = settings.DATABASES['default']['NAME']
        if options.get('interactive'):
            if not confirm("This is going to GARBLE your database (%s).\nAre you sure (y/n) ?" % dbname):
                raise CommandError("User abort.")

        contacts = dd.resolve_app('contacts')

        User = dd.resolve_model(settings.SITE.user_model)
        Person = dd.resolve_model('contacts.Person')
        Household = dd.resolve_model('households.Household')
        Member = dd.resolve_model('households.Member')
        Role = dd.resolve_model('households.Role')
        Country = dd.resolve_model('countries.Country')

        for p in Person.objects.order_by('id'):
            if User.objects.filter(partner=p).count() > 0:
                # users keep their original name
                pass
            else:
                p.nationality = Country.objects.get(
                    isocode=NATIONALITIES.pop())
                p.last_name = LAST_NAMES.pop()
                if p.gender == dd.Genders.male:
                    p.first_name = MALES.pop()
                    FEMALES.pop()
                else:
                    p.first_name = FEMALES.pop()
                    MALES.pop()
                #~ dblogger.log_changes(REQUEST,p)
                p.name = join_words(p.last_name, p.first_name)
                p.save()
                dblogger.info("%s from %s", str(p), str(p.nationality))

        MEN = Cycler(Person.objects.filter(gender=dd.Genders.male)
                     .order_by('id'))
        WOMEN = Cycler(
            Person.objects.filter(gender=dd.Genders.female).order_by('id'))
        for h in Household.objects.all():
            if h.member_set.all().count() == 0:
                he = MEN.pop()
                she = WOMEN.pop()
                h.name = he.last_name + "-" + she.last_name
                Member(household=h, person=he,
                       role=Role.objects.get(pk=1)).save()
                Member(household=h, person=she,
                       role=Role.objects.get(pk=2)).save()
            else:
                h.name = ''
                h.full_clean()
            h.save()
            dblogger.info(str(h))

        dblogger.info("GARBLE done on database %s." % dbname)
