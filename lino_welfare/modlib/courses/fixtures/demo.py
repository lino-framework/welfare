# -*- coding: UTF-8 -*-
# Copyright 2008-2014 Luc Saffre
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

"""
Adds PCSW-specific demo data.
"""

from __future__ import unicode_literals

import datetime
ONE_DAY = datetime.timedelta(days=1)

from django.conf import settings
from django.utils.translation import ugettext as _


from lino import dd
from lino import mixins
from lino.utils import i2d, Cycler
from lino.modlib.beid.mixins import BeIdCardTypes
from lino.utils.instantiator import Instantiator
from lino.core.dbutils import resolve_model
from north.dbutils import babelkw
from lino.dd import field2kw
from lino.utils import mti
from lino.utils.ssin import generate_ssin

from lino.modlib.cal.utils import DurationUnits

# isip = dd.resolve_app('isip')
# jobs = dd.resolve_app('jobs')
# contacts = dd.resolve_app('contacts')
# users = dd.resolve_app('users')
# countries = dd.resolve_app('countries')
# reception = dd.resolve_app('reception')
# cal = dd.resolve_app('cal')

Company = dd.resolve_model('contacts.Company')


def objects():

    pcsw = dd.resolve_app('pcsw')

    Place = resolve_model('countries.Place')
    Client = resolve_model('pcsw.Client')
    CourseContent = resolve_model('courses.CourseContent')

    CLIENTS = Cycler(
        Client.objects.filter(client_state=pcsw.ClientStates.coached))

    eupen = Place.objects.get(name__exact='Eupen')

    courseprovider = Instantiator('courses.CourseProvider').build
    oikos = courseprovider(name=u"Oikos", city=eupen, country='BE')
    yield oikos

    #~ kap = company(name=u"KAP",city=eupen,country='BE',
      #~ is_courseprovider=True)
    kap = courseprovider(name=u"KAP", city=eupen, country='BE')
    yield kap

    yield CourseContent(id=1, name=u"Deutsch")
    yield CourseContent(id=2, name=u"Französisch")

    COURSECONTENTS = Cycler(CourseContent.objects.all())

    creq = Instantiator('courses.CourseRequest').build
    for i in range(20):
        yield creq(
            person=CLIENTS.pop(), content=COURSECONTENTS.pop(),
            date_submitted=settings.SITE.demo_date(-i * 2))
    #~ yield creq(person=ulrike,content=1,date_submitted=settings.SITE.demo_date(-30))
    #~ yield creq(person=tatjana,content=1,date_submitted=settings.SITE.demo_date(-30))
    #~ yield creq(person=erna,content=2,date_submitted=settings.SITE.demo_date(-30))

    offer = Instantiator('courses.CourseOffer').build
    course = Instantiator('courses.Course').build
    yield offer(provider=oikos, title=u"Deutsch für Anfänger", content=1)
    #~ yield course(offer=1,start_date=i2d(20110110))
    yield course(offer=1, start_date=settings.SITE.demo_date(+30))

    yield offer(provider=kap, title=u"Deutsch für Anfänger", content=1)
    #~ yield course(offer=2,start_date=i2d(20110117))
    yield course(offer=2, start_date=settings.SITE.demo_date(+16))

    yield offer(provider=kap, title=u"Français pour débutants", content=2)
    #~ yield course(offer=3,start_date=i2d(20110124))
    yield course(offer=3, start_date=settings.SITE.demo_date(+16))
