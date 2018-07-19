# -*- coding: UTF-8 -*-
# Copyright 2015-2018 Luc Saffre
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

from lino.core.roles import SiteUser, UserRole
from lino.modlib.users.roles import AuthorshipTaker
from lino.modlib.office.roles import OfficeUser, OfficeStaff
from lino_xl.lib.cal.roles import GuestOperator
from lino_xl.lib.polls.roles import PollsUser, PollsStaff
from lino_xl.lib.beid.roles import BeIdUser
from lino_xl.lib.notes.roles import NotesUser
from lino.modlib.checkdata.roles import CheckdataUser
from lino_welfare.modlib.cbss.roles import CBSSUser
from lino_welfare.modlib.aids.roles import AidsStaff, AidsUser
from lino_xl.lib.sepa.roles import SepaUser, SepaStaff
from lino_xl.lib.courses.roles import CoursesUser
from lino_xl.lib.excerpts.roles import ExcerptsUser
from lino_xl.lib.coachings.roles import CoachingsUser, CoachingsStaff
from lino_xl.lib.contacts.roles import ContactsStaff, ContactsUser


class SocialAgent(SiteUser, OfficeUser, ContactsUser, CBSSUser, BeIdUser,
                  CheckdataUser, AidsUser, PollsUser, SepaUser,
                  CoursesUser, ExcerptsUser, CoachingsUser,
                  AuthorshipTaker, GuestOperator, NotesUser):
    """
    A **social agent** is a user who does individual coaching of
    clients.  Certain privacy-relevant client data is visible only
    to social agents.

    """


class SocialStaff(SocialAgent, OfficeStaff, ContactsStaff, AidsStaff,
                  PollsStaff, SepaStaff, CoachingsStaff):
    """
    A **social staff member** is a social agent who has access to more
    technical information about welfare clients.  For example the
    `Miscellaneous` panel.

    """

class SocialCoordinator(UserRole):
    """
    Reception clerks (210) can see contracts.
    """
    pass
