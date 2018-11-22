# coding: utf-8
# Copyright 2015 Rumma & Ko Ltd
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

"""Generates the objects in :mod:`lino_xl.lib.notes.fixtures.demo`
plus one :attr:`important
<lino_welfare.modlib.notes.models.Note.important>` note.

"""

from lino_xl.lib.notes.fixtures.demo import objects as lib_objects
from lino.utils import Cycler
from lino.api import dd, rt, _


def objects():
    Note = rt.models.notes.Note
    NTYPES = Cycler(rt.models.notes.NoteType.objects.all())
    USERS = Cycler(rt.models.users.User.objects.all())
    CLIENTS = Cycler(rt.models.pcsw.Client.objects.all())

    yield lib_objects()

    yield Note(user=USERS.pop(),
               date=dd.demo_date(days=-20),
               project=CLIENTS.pop(),
               subject=_("Do not offer coffee"),
               important=True,
               type=NTYPES.pop())

    


