# -*- coding: UTF-8 -*-
# Copyright 2013-2014 Luc Saffre
# This file is part of the Lino-Welfare project.
# Lino-Welfare is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
# Lino-Welfare is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with Lino-Welfare; if not, see <http://www.gnu.org/licenses/>.

from lino.modlib.cal.fixtures.demo2 import objects as lino_objects
from lino import dd
from lino.utils import Cycler


def objects():
    Client = dd.resolve_model('pcsw.Client')
    CLIENTS = Cycler(Client.objects.all())
    for obj in lino_objects():
        if obj.__class__.__name__ == 'Event':
            if obj.event_type.invite_client:
                obj.project = CLIENTS.pop()
        yield obj
