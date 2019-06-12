# -*- coding: UTF-8 -*-
# Copyright 2012-2014 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)


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

