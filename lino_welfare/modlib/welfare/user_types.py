# -*- coding: UTF-8 -*-
# Copyright 2009-2017 Luc Saffre
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

"""Defines default user profiles and shortcuts for Lino Welfare.

See :ref:`welfare.specs.users`

"""

from lino.core.roles import UserRole, SiteUser, SiteAdmin, Supervisor, login_required
from lino.modlib.users.roles import AuthorshipTaker
from lino.modlib.about.roles import SiteSearcher
from lino.modlib.office.roles import OfficeOperator, OfficeStaff, OfficeUser
from lino_xl.lib.excerpts.roles import ExcerptsUser, ExcerptsStaff
from lino_xl.lib.contacts.roles import ContactsStaff, ContactsUser, SimpleContactsUser
from lino_xl.lib.ledger.roles import LedgerStaff, LedgerUser
from lino_xl.lib.sepa.roles import SepaStaff
from lino_xl.lib.cal.roles import GuestOperator
from lino_xl.lib.sepa.roles import SepaUser
from lino_xl.lib.courses.roles import CoursesUser
from lino_xl.lib.beid.roles import BeIdUser
from lino_welfare.modlib.cbss.roles import CBSSUser, SecurityAdvisor
from lino_xl.lib.coachings.roles import CoachingsStaff
from lino_welfare.modlib.pcsw.roles import SocialAgent
from lino_welfare.modlib.pcsw.roles import SocialStaff
from lino_welfare.modlib.aids.roles import AidsStaff
from lino_welfare.modlib.integ.roles import IntegrationAgent, IntegrationStaff
from lino_welfare.modlib.debts.roles import DebtsUser, DebtsStaff
from lino_welfare.modlib.newcomers.roles import (NewcomersAgent,
                                                 NewcomersOperator)


class AccountantManager(SiteUser, LedgerStaff, ContactsUser, OfficeUser,
                        ExcerptsUser, AidsStaff, SepaStaff):
    """Like an **accountant**, but also has access to configuration.

    """
    pass


class SiteAdmin(
        SiteAdmin,
        SiteSearcher,
        IntegrationStaff,
        DebtsStaff,
        LedgerStaff,
        # ContactsStaff,
        OfficeStaff,
        NewcomersAgent,
        ExcerptsStaff,
        #SocialAgent,
        AidsStaff, SepaStaff):
    """The site adminstrator has permission for everything."""


class ReceptionClerk(SiteUser, AuthorshipTaker, OfficeOperator,
                     GuestOperator,
                     ContactsStaff, AidsStaff, CBSSUser, BeIdUser,
                     SepaUser, CoursesUser, ExcerptsUser,
                     CoachingsStaff):
    """A **reception clerk** is a user who is not a *social agent* but
    receives clients and does certain administrative tasks (in Eupen
    they call them `back office
    <https://en.wikipedia.org/wiki/Back_office>`__).

    """
    pass


class ReceptionClerkNewcomers(SiteUser, AuthorshipTaker, SimpleContactsUser,
                              OfficeOperator,
                              GuestOperator,
                              ExcerptsUser,
                              # OfficeUser,
                              # SocialAgent,
                              # CoursesUser,
                              NewcomersAgent,
                              BeIdUser):
                              # ContactsUser,
                              # ContactsStaff,
                              # AidsStaff, CBSSUser, BeIdUser, SepaUser,
                              # ):
    """A **newcomers reception clerk** is a *reception clerk* who also
    can assign coaches to clients.

    """
    pass


class IntegrationAgentNewcomers(IntegrationAgent, NewcomersOperator,
                                DebtsUser):
    """A **newcomers integration agent** is an *integration agent* who
    also can assign coaches to clients and create budgets for debts
    mediation.

    """
    pass


class LedgerUser(SiteUser, LedgerUser, ContactsUser, OfficeUser, ExcerptsUser,
                 AidsStaff, SepaStaff):
    """An **accountant** is a user who enters invoices, bank statements,
    payment orders and other ledger operations.

    """
    pass


class SecurityAdvisor(SiteAdmin, SecurityAdvisor):
    pass

class NewcomersConsultant(NewcomersAgent, SocialAgent):
    pass

class Supervisor(SiteUser, Supervisor, AuthorshipTaker, OfficeOperator,
                 GuestOperator,
                 ContactsStaff, AidsStaff, NewcomersOperator,
                 ExcerptsUser, SepaUser, CoursesUser):
    """A backoffice user who can act as others."""
    pass


from lino.modlib.users.choicelists import UserTypes
from lino.api import _

UserTypes.clear()

add = UserTypes.add_item

add('000', _("Anonymous"), UserRole, name='anonymous',
    readonly=True, authenticated=False)
add('100', _("Integration agent"),             IntegrationAgent)
add('110', _("Integration agent (Manager)"),   IntegrationStaff)
add('120', _("Integration agent (Newcomers)"), IntegrationAgentNewcomers)
add('200', _("Newcomers consultant"),          NewcomersConsultant)
add('210', _("Reception clerk"),               ReceptionClerk)
add('220', _("Newcomers reception clerk"),     ReceptionClerkNewcomers)
add('300', _("Debts consultant"),              DebtsUser)
add('400', _("Social agent"),                  SocialAgent)
add('410', _("Social agent (Manager)"),        SocialStaff)
add('500', _("Accountant"),                    LedgerUser)
add('510', _("Accountant (Manager)"),          AccountantManager)
add('800', _("Supervisor"),                    Supervisor)
add('900', _("Administrator"),                 SiteAdmin, name='admin')
add('910', _("Security advisor"),              SecurityAdvisor)


