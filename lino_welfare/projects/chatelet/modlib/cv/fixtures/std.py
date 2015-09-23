# -*- coding: UTF-8 -*-
# Copyright 2015 Luc Saffre
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
"""Standard fixture for :mod:`lino_modlib.projects.chatelet.modlib.cv`.

"""

from __future__ import unicode_literals
from __future__ import print_function

import logging
logger = logging.getLogger(__name__)


from lino.modlib.cv.fixtures.std import objects as stdobjects

from lino.api import dd, rt, _


def objects():
    yield stdobjects()

    def proof(name):
        return rt.modules.cv.Proof(**dd.str2kw('name', name))

    def obstacle_type(name):
        return rt.modules.cv.ObstacleType(**dd.str2kw('name', name))

    yield proof(_("Declarative"))
    yield proof(_("Certificate"))
    yield proof(_("Attestation"))
    yield proof(_("Diploma"))

    yield obstacle_type(_("Alcohol"))
    yield obstacle_type(_("Health"))
    yield obstacle_type(_("Debts"))
    yield obstacle_type(_("Family problems"))
