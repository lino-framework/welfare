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

from lino.modlib.office.roles import OfficeUser, OfficeStaff
from lino.modlib.polls.roles import PollsUser, PollsStaff
from lino.modlib.beid.roles import BeIdUser
from lino.modlib.plausibility.roles import PlausibilityUser
from lino_welfare.modlib.cbss.roles import CBSSUser
from lino_welfare.modlib.aids.roles import AidsStaff, AidsUser


class SocialAgent(OfficeUser, CBSSUser, BeIdUser, PlausibilityUser,
                  AidsUser, PollsUser):
    """A **social agent** is a user who does individual coaching of
    clients.  Certain privacy-relevant client data is visible only
    to social agents.

    """


class SocialStaff(SocialAgent, OfficeStaff, AidsStaff, PollsStaff):
    """A **social staff member** is a social agent who has access to more
    technical information about welfare clients.  For example the
    `Miscellaneous` panel.

    """
