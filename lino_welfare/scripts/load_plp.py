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
# along with Lino ; if not, see <http://www.gnu.org/licenses/>.

"""

Temporary script used to import PLP.DBF from TIM.

PLP ("Person Link to Person")

# PLPTYPES.DBC:
# 01 |Vater/Mutter   |01R|Vater        |Mutter        ||
# 01R|Kind           |01 |Sohn         |Tochter       ||
# 02 |Onkel/Tante    |02R|Onkel        |Tante         ||
# 02R|Nichte/Neffe   |02 |Neffe        |Nichte        ||
# 03 |Stiefelternteil|03R|Stiefvater   |Stiefmutter   ||
# 03R|Stiefkind      |03 |Stiefsohn    |Stieftochter  ||
# 04 |Großelternteil |04R|Großvater    |Großmutter    ||
# 04R|Enkel          |04 |Enkel        |Enkelin       ||
# 10 |Partner        |10 |Partner      |Partnerin     ||
# 11 |Freund         |11 |Freund       |Freundin      ||

$ python manage.py show --username rolf households.Roles

======= =================== ================== =============
 ID      Designation         Designation (fr)   name-giving
------- ------------------- ------------------ -------------
 1       Haushaltsvorstand   Chef de ménage     Yes
 2       Ehepartner          Conjoint           Yes
 3       Partner             Partenaire         Yes
 4       Mitbewohner         Cohabitant         No
 5       Kind                Enfant             No
 6       Adoptivkind         Enfant adopté      No
 7       Verwandter          Membre de famille  No
 **0**                                          **3**
======= =================== ================== =============

$ python manage.py show --username rolf households.Types

==== ========================= =====================
 ID   Designation               Designation (fr)    
---- ------------------------- ---------------------
 1    Ehepaar                   Couple marié
 2    Familie                   Famille
 3    Faktischer Haushalt       Ménage de fait
 4    Legale Wohngemeinschaft   Cohabitation légale
==== ========================= =====================



"""

import sys

from lino import dd

from lino.utils import dbfreader
from lino.utils import dblogger

from lino.modlib.humanlinks.models import LinkTypes, Link
from lino_welfare.modlib.households.models import Role, Member, Household

from lino.runtime import pcsw, households


# def tim2lino(plptype):
#     if plptype.endswith('R'):
#         return
#     if plptype == '01':
#         return LinkTypes.natural
#     if plptype == '03':
#         return LinkTypes.adoptive
#     if plptype == '10':
#         return LinkTypes.partner
#     if plptype == '11':
#         return LinkTypes.friend
#     if plptype == '02':
#         return LinkTypes.other
#     if plptype == '04':
#         return LinkTypes.grandparent
#     raise Exception("Invalid link type %r" % plptype)


R_CHEF = households.Role.objects.get(id=1)
R_MARRIED = households.Role.objects.get(id=2)
R_PARTNER = households.Role.objects.get(id=3)
R_CHILD = households.Role.objects.get(id=5)

R_ADOPTED = households.Role.objects.get(id=6)
R_COHABITANT = households.Role.objects.get(id=4)
try:
    R_RELATIVE = households.Role.objects.get(id=7)  # grandparent
except households.Role.DoesNotExist:
    kw = dd.babel_values('name',
                         de=u"Verwandter",
                         fr=u"Membre de famille",
                         en=u"Relative")
    R_RELATIVE = Role(**kw)
    R_RELATIVE.save()


HOUSEHOLDS_MAP = {}

parent_roles = households.Role.objects.filter(name_giving=True)
child_roles = households.Role.objects.filter(name_giving=False)

T_COUPLE = households.Type.objects.get(id=1)
T_FAMILY = households.Type.objects.get(id=2)
T_HOUSEHOLD = households.Type.objects.get(id=3)
T_COMMUNITY = households.Type.objects.get(id=4)


def plp2member(plptype, p, c):
    if plptype.endswith('R'):
        return
    if plptype == '01':
        role = R_CHILD
    elif plptype == '02':
        role = R_COHABITANT
    elif plptype == '03':
        role = R_ADOPTED
    elif plptype == '04':
        role = R_RELATIVE
    elif plptype == '10':
        role = R_MARRIED
    elif plptype == '11':
        role = R_PARTNER
    else:
        raise Exception("Invalid link type %r" % plptype)
    
    if not role.name_giving:  # i.e. CHILD, ADOPTED, RELATIVE
        # find household of parent
        members = households.Member.objects.filter(
            person=p.person, role__name_giving=True)
        if members.count() == 0:
            hh = households.Household(type=T_FAMILY)
            hh.full_clean()
            hh.save()
            dblogger.debug("Created household %s from parent %s", hh, p)
            obj = households.Member(
                household=hh, role=R_CHEF, person=p.person)
            obj.save()
        elif members.count() == 1:
            hh = members[0].household
        else:
            msg = "Found more than 1 household for parent %r" % p
            # raise Exception(msg)
            dblogger.warning(msg)
            return
        obj = households.Member(household=hh, role=role, person=c.person)
    else:
        members = households.Member.objects.filter(
            person=c.person, role__name_giving=False)
        if members.count() == 0:
            hh = households.Household(type=T_FAMILY)
            hh.full_clean()
            hh.save()
            dblogger.warning("Created household %s from child %s", hh, c)
            obj = households.Member(
                household=hh, role=R_CHILD, person=c.person)
            obj.save()
        elif members.count() == 1:
            hh = members[0].household
        else:
            msg = "Found more than 1 household for child %r" % c
            # raise Exception(msg)
            dblogger.warning(msg)
            return
        
        obj = households.Member(household=hh, role=role, person=p.person)

    obj.save()
    dblogger.info("Created %s as %s", obj.person, obj.role)
        

def get_or_warn(idpar):
    try:
        return pcsw.Client.objects.get(pk=int(idpar))
    except pcsw.Client.DoesNotExist:
        dblogger.warning("No client %s", idpar)


def main():
    fn = sys.argv[1]
    f = dbfreader.DBFFile(fn, codepage="cp850")
    dblogger.info("Loading %d records from %s...", len(f), fn)
    f.open()
    for dbfrow in f:
        # t = tim2lino(dbfrow.type)
        # if not t:
        #     continue

        c = get_or_warn(dbfrow.idpar1)
        p = get_or_warn(dbfrow.idpar2)
        if not c or not p:
            continue

        plp2member(dbfrow.type, p, c)

        # obj = Link(parent=p, child=c, type=t)
        # obj.full_clean()
        # obj.save()
        # dblogger.info("%s is %s of %s", obj.parent, obj.type, obj.child)

    f.close()

if __name__ == '__main__':
    main()
