# -*- coding: UTF-8 -*-
# Copyright 2014 Rumma & Ko Ltd
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

"""Temporary script used to import PLP.DBF from TIM.

PLP ("Person Link to Person")
IdPar1
IdPar2
PlpType

Content of `PLPTYPES.DBC`::

    01 |Vater/Mutter   |01R|Vater        |Mutter        ||
    01R|Kind           |01 |Sohn         |Tochter       ||
    02 |Onkel/Tante    |02R|Onkel        |Tante         ||
    02R|Nichte/Neffe   |02 |Neffe        |Nichte        ||
    03 |Stiefelternteil|03R|Stiefvater   |Stiefmutter   ||
    03R|Stiefkind      |03 |Stiefsohn    |Stieftochter  ||
    04 |Großelternteil |04R|Großvater    |Großmutter    ||
    04R|Enkel          |04 |Enkel        |Enkelin       ||
    10 |Partner        |10 |Partner      |Partnerin     ||
    11 |Freund         |11 |Freund       |Freundin      ||

$ python manage.py show --username rolf households.MemberRoles

======= ============ ===================
 value   name         text
------- ------------ -------------------
 01      head         Head of household
 02      spouse       Spouse
 03      partner      Partner
 04      cohabitant   Cohabitant
 05      child        Child
 07      adopted      Adopted child
 06      relative     Relative
======= ============ ===================

$ python manage.py show --username rolf households.Types

==== ==================== ===================== =========================
 ID   Designation          Designation (fr)      Designation (de)
---- -------------------- --------------------- -------------------------
 1    Married couple       Couple marié          Ehepaar
 2    Family               Famille               Familie
 3    Factual household    Ménage de fait        Faktischer Haushalt
 4    Legal cohabitation   Cohabitation légale   Legale Wohngemeinschaft
==== ==================== ===================== =========================


Example sequence: A and B are married. A has a child B from previous
marriage, B has a child D from previous marriage, and they have two
common children E and F. From PLP.DBF we'll get (in a random sort
order):

A C child
B D child
A E child
A F child
B E child
B E child
A B spouse



"""

import sys

from lino.api import dd, rt

from lino.utils import dbfreader
from lino.utils import dblogger

from lino_welfare.modlib.households.models import (
    Member, MemberRoles, Household)

from lino.api.shell import households, contacts

LinkTypes = rt.models.humanlinks.LinkTypes
Link = rt.models.humanlinks.Link


def tim2lino(plptype):
    if plptype.endswith('R'):
        return
    if plptype == '01':
        return LinkTypes.parent
    if plptype == '03':
        return LinkTypes.adoptive
    if plptype == '10':
        return LinkTypes.spouse
    if plptype == '11':
        return LinkTypes.partner
    if plptype == '02':
        return LinkTypes.other
    if plptype == '04':
        return LinkTypes.grandparent
    raise Exception("Invalid link type %r" % plptype)


# R_CHEF = households.Role.objects.get(id=1)
# R_MARRIED = households.Role.objects.get(id=2)
# R_PARTNER = households.Role.objects.get(id=3)
# R_CHILD = households.Role.objects.get(id=5)
# R_ADOPTED = households.Role.objects.get(id=6)
# R_COHABITANT = households.Role.objects.get(id=4)
# try:
#     R_RELATIVE = households.Role.objects.get(id=7)  # grandparent
# except households.Role.DoesNotExist:
#     kw = dd.babel_values('name',
#                          de=u"Verwandter",
#                          fr=u"Membre de famille",
#                          en=u"Relative")
#     R_RELATIVE = Role(**kw)
#     R_RELATIVE.save()

R_CHEF = MemberRoles.head
R_MARRIED = MemberRoles.spouse
R_PARTNER = MemberRoles.partner
R_CHILD = MemberRoles.child
R_ADOPTED = MemberRoles.adopted
R_COHABITANT = MemberRoles.cohabitant
R_RELATIVE = MemberRoles.relative

HOUSEHOLDS_MAP = {}

# parent_roles = households.Role.objects.filter(name_giving=True)
# child_roles = households.Role.objects.filter(name_giving=False)

# if not role.name_giving:  # i.e. CHILD, ADOPTED, RELATIVE
child_roles = (R_CHILD, R_ADOPTED)  # , R_RELATIVE)

T_COUPLE = households.Type.objects.get(id=1)
T_FAMILY = households.Type.objects.get(id=2)
T_HOUSEHOLD = households.Type.objects.get(id=3)
T_COMMUNITY = households.Type.objects.get(id=4)


def plp2lino(plptype, p, c):
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
    
    # Is there a household where the parent of this relation is no a
    # child?
    members = Member.objects.filter(
        person=p.person).exclude(role__in=child_roles)
    if members.count() == 0:
        hh = Household(type=T_FAMILY, name=p.person.last_name)
        hh.full_clean()
        hh.save()
        dblogger.debug(
            "Created household %s from PLP `%s is %s of %s`",
            hh, p, role, c)
        obj = Member(household=hh, role=R_CHEF, person=p.person)
        obj.full_clean()
        obj.save()
    elif members.count() == 1:
        hh = members[0].household
    else:
        msg = "Found more than 1 household for parent %r" % p
        # raise Exception(msg)
        dblogger.warning(msg)
        return
        
    obj = Member(household=hh, role=role, person=c.person)
    obj.full_clean()
    obj.save()
    dblogger.info("Created %s as %s", obj.person, obj.role)


def get_or_warn(idpar):
    try:
        return contacts.Person.objects.get(pk=int(idpar))
    except contacts.Person.DoesNotExist:
        dblogger.warning("No client %s", idpar)


def main():
    fn = sys.argv[1]
    f = dbfreader.DBFFile(fn, codepage="cp850")
    dblogger.info("Loading %d records from %s...", len(f), fn)
    f.open()
    for dbfrow in f:
        if dbfrow.deleted():
            continue
        c = get_or_warn(dbfrow.idpar1)
        p = get_or_warn(dbfrow.idpar2)
        if not c or not p:
            continue  # invalid idpar
        t = tim2lino(dbfrow.type)
        if t is not None:
            # 10 and 11 are symmetric: don't duplicate them. if the
            # opposite record exists, ignore the other one.
            if dbfrow.type in ('10', '11'):
                qs = Link.objects.filter(parent=c, child=p, type=t)
                if qs.count() > 0:
                    continue
            obj = Link(parent=p, child=c, type=t)
            obj.full_clean()
            obj.save()

        # plp2lino(dbfrow.type, p, c)

    f.close()

if __name__ == '__main__':
    main()
