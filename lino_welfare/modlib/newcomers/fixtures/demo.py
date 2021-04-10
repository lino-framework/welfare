# -*- coding: UTF-8 -*-
# Copyright 2012-2015 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

"""
Adds demo data for :mod:`lino_welfare.modlib.newcomers`.
"""


from builtins import range
from lino.utils.instantiator import Instantiator
from lino.utils import Cycler

from lino.api.dd import babel_values

from lino.api import dd, rt
from lino.modlib.users.choicelists import UserTypes
from lino_welfare.modlib.integ.roles import IntegUser
from lino_xl.lib.clients.choicelists import ClientStates


def objects():

    from lino_welfare.modlib.newcomers.models import Broker, Faculty, Competence
    pcsw = dd.resolve_app('pcsw')
    Person = dd.resolve_model('contacts.Person')
    User = rt.models.users.User

    I = Instantiator(Broker).build
    #~ yield I(**babel_values('name',
        #~ de=u"Polizei", fr=u"Police",en=u"Police"))
    #~ yield I(**babel_values('name',
        #~ de=u"Jugendgericht", fr=u"Jugendgericht",en=u"Jugendgericht"))
    yield I(name="Police")
    yield I(name="Other PCSW")

    I = Instantiator(Faculty).build
    yield I(weight=10, **babel_values('name', de=u"Eingliederungseinkommen (EiEi)", fr=u"Revenu d'intégration sociale (RIS)",  en=u"EiEi"))
    yield I(weight=5, **babel_values('name', de=u"DSBE",                    fr=u"Service d'insertion socio-professionnelle",   en=u"DSBE"))
    yield I(weight=4, **babel_values('name', de=u"Ausländerbeihilfe",       fr=u"Aide sociale équivalente (pour étrangers)", en=u"Ausländerbeihilfe"))
    yield I(weight=6, **babel_values('name', de=u"Finanzielle Begleitung",  fr=u"Accompagnement budgétaire",     en=u"Finanzielle Begleitung"))
    yield I(weight=2, **babel_values('name', de=u"Laufende Beihilfe",       fr=u"Aide complémenataire",       en=u"Laufende Beihilfe"))

    #~ User = resolve_model('users.User')
    #~ yield User(username="caroline",
        #~ first_name="Caroline",last_name="Carnol",
        # ~ user_type='200') # UserTypes.caroline)
    #~ FACULTIES = Cycler(Faculty.objects.all())
    #~ user_types = [p for p in UserTypes.items() if p.integ_level]
    #~ USERS = Cycler(User.objects.filter(user_type__in=user_types))
    #~ for i in range(7):
        #~ yield Competence(user=USERS.pop(),faculty=FACULTIES.pop())
    #~ for p in pcsw.Client.objects.filter(client_state=ClientStates.new):
        #~ p.faculty = FACULTIES.pop()
        #~ p.save()
    newcomers = dd.resolve_app('newcomers')

    QUOTAS = Cycler(100, 60, 50, 20)
    FACULTIES = Cycler(newcomers.Faculty.objects.all())

    user_types = [
        p for p in UserTypes.items()
        if p.has_required_roles([IntegUser])
        and not p.has_required_roles([dd.SiteStaff])]
    qs = User.objects.filter(user_type__in=user_types)
    # qs = qs.order_by('last_name', 'first_name', 'username')
    for u in qs:
        u.newcomer_quota = QUOTAS.pop()
        yield u

    USERS = Cycler(qs)
    for i in range(7):
        yield newcomers.Competence(user=USERS.pop(), faculty=FACULTIES.pop())

        for p in pcsw.Client.objects.exclude(
                client_state=ClientStates.former):
            p.faculty = FACULTIES.pop()
            p.save()
