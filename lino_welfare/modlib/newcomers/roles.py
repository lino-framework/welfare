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
"""Choicelists for `lino_welfare.modlib.newcomers`.




"""

from lino.modlib.beid.roles import BeIdUser
from lino.modlib.contacts.roles import ContactsUser
from lino_welfare.modlib.pcsw.roles import SocialAgent


class NewcomersAgent(SocialAgent):
    """A **newcomers agent** is a *social agent* who also manages
    newcomers.

    """
    pass


class NewcomersOperator(ContactsUser, BeIdUser):
    """A **newcomers operator** is a user who is not *social agent* but
    can e.g. register newcomers and assign them a coach.

    """
    pass

