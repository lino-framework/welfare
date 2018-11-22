# -*- coding: UTF-8 -*-
# Copyright 2012-2014 Rumma & Ko Ltd
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


from builtins import range
from lino.api import dd, rt
from lino.utils import Cycler


def objects():
    Client = rt.models.pcsw.Client
    Property = rt.models.properties.Property
    PP = rt.models.cv.PersonProperty

    PERSONS = Cycler(Client.objects.all())
    for prop in Property.objects.order_by('id'):
        for n in range(10):
                #~ prop = PROPS.pop()
            VALUES = Cycler(prop.type.choices_for(prop))
            #~ print "20120409", repr(VALUES.items)
            #~ for n in range(3):
            if len(VALUES) == 0:
                yield PP(person=PERSONS.pop(), property=prop)
            else:
                for n in range(len(VALUES)):
                    yield PP(person=PERSONS.pop(),
                             property=prop, value=VALUES.pop()[0].value)

