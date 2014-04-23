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

temporary script used to import humanlinks from TIM


"""

import sys

from lino.utils import dbfreader
from lino.utils import dblogger

# PLPTYPES.DBC:
# 01 |Vater/Mutter   |01R|Vater        |Mutter        ||
# 01R|Kind           |01 |Sohn         |Tochter       ||
# 02 |Onkel/Tante    |02R|Onkel        |Tante         ||
# 02R|Nichte/Neffe   |02 |Neffe        |Nichte        ||
# 03 |Stiefelternteil|03R|Stiefvater   |Stiefmutter   ||
# 03R|Stiefkind      |03 |Stiefsohn    |Stieftochter  ||


from lino.modlib.humanlinks.models import LinkTypes, Link

# from django.conf import settings
from lino.runtime import pcsw


def tim2lino(plptype):
    if plptype == '01':
        return LinkTypes.natural
    if plptype == '03':
        return LinkTypes.adoptive
    if plptype == '02':
        return LinkTypes.other
    if plptype in ('01R', '02R', '03R'):
        return
    raise Exception("Invalid link type %r" % plptype)


def main():
    fn = sys.argv[1]
    f = dbfreader.DBFFile(fn, codepage="cp850")
    dblogger.info("Loading %d records from %s...", len(f), fn)
    f.open()
    for dbfrow in f:
        p = pcsw.Client.objects.get(pk=int(dbfrow.idpar1))
        c = pcsw.Client.objects.get(pk=int(dbfrow.idpar2))
        t = tim2lino(dbfrow.type)
        if t:
            obj = Link(parent=p, child=c, type=t)
            obj.full_clean()
            print obj.child

    f.close()

if __name__ == '__main__':
    main()
