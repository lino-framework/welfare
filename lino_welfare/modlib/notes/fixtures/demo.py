# coding: utf-8
# Copyright 2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""Generates the objects in :mod:`lino.modlib.notes.fixtures.demo`
plus one :attr:`important
<lino_welfare.modlib.notes.models.Note.important>` note.

"""

from lino.modlib.notes.fixtures.demo import objects as lib_objects
from lino.utils import Cycler
from lino.api import dd, rt, _


def objects():
    Note = rt.modules.notes.Note
    NTYPES = Cycler(rt.modules.notes.NoteType.objects.all())
    USERS = Cycler(rt.modules.users.User.objects.all())
    CLIENTS = Cycler(rt.modules.pcsw.Client.objects.all())

    yield lib_objects()

    yield Note(user=USERS.pop(),
               date=dd.demo_date(days=-20),
               project=CLIENTS.pop(),
               subject=_("Do not offer coffee"),
               important=True,
               type=NTYPES.pop())

    


