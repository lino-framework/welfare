# -*- coding: UTF-8 -*-
# Copyright 2009-2015 Luc Saffre
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

Local administrators may define their own module, similar to this, and
have :attr:`lino.core.site.Site.user_profiles_module` point to it.

"""

from lino.core.roles import UserRole, SiteAdmin, Supervisor
from lino.modlib.office.roles import OfficeOperator
from lino.modlib.contacts.roles import ContactsStaff
from lino.modlib.office.roles import OfficeUser
from lino.modlib.ledger.roles import LedgerStaff
from lino.modlib.beid.roles import BeIdUser
from lino_welfare.modlib.cbss.roles import CBSSUser
from lino_welfare.modlib.pcsw.roles import SocialAgent
from lino_welfare.modlib.pcsw.roles import SocialStaff
from lino_welfare.modlib.aids.roles import AidsStaff
from lino_welfare.modlib.integ.roles import IntegrationAgent, IntegrationStaff
from lino_welfare.modlib.debts.roles import DebtsUser, DebtsStaff
from lino_welfare.modlib.newcomers.roles import (NewcomersAgent,
                                                 NewcomersOperator)


class SiteAdmin(
        SiteAdmin,
        IntegrationStaff,
        DebtsStaff, LedgerStaff,
        NewcomersAgent,
        OfficeOperator,
        AidsStaff):
    """The site adminstrator has permission for everything."""


class ReceptionClerk(OfficeOperator, ContactsStaff, AidsStaff,
                     CBSSUser, BeIdUser):
    """A **reception clerk** is a user who is not a *social agent* but
    receives clients and does certain administrative tasks (in Eupen
    they call them `back office
    <https://en.wikipedia.org/wiki/Back_office>`__).

    """
    pass


class ReceptionClerkNewcomers(ReceptionClerk, NewcomersOperator):
    """A **newcomers reception clerk** is a *reception clerk* who also
    can assign coaches to clients.

    """
    pass


class Supervisor(Supervisor, OfficeOperator, ContactsStaff, AidsStaff,
                 NewcomersOperator):
    """A backoffice user who can act as others."""
    pass


class IntegrationAgentNewcomers(IntegrationAgent, NewcomersOperator):
    """A **newcomers reception clerk** is a *reception clerk* who also
    can assign coaches to clients.

    """
    pass


class LedgerUser(LedgerStaff, OfficeUser, AidsStaff):
    """An **accountant** is a user who enters invoices, bank statements,
    payment orders and other ledger operations.

    """
    pass

from lino.modlib.users.choicelists import UserProfiles
from lino.api import _

UserProfiles.clear()

add = UserProfiles.add_item

add('000', _("Anonymous"), UserRole, name='anonymous',
    readonly=True, authenticated=False)
add('100', _("Integration agent"),             IntegrationAgent)
add('110', _("Integration agent (Manager)"),   IntegrationStaff)
add('120', _("Integration agent (Newcomers)"), IntegrationAgentNewcomers)
add('200', _("Newcomers consultant"),          NewcomersAgent)
add('210', _("Reception clerk"),               ReceptionClerk)
add('220', _("Newcomers reception clerk"),     ReceptionClerkNewcomers)
add('300', _("Debts consultant"),              DebtsUser)
add('400', _("Social agent"),                  SocialAgent)
add('410', _("Social agent (Manager)"),        SocialStaff)
add('500', _("Accountant"),                    LedgerUser)
add('800', _("Supervisor"),                    Supervisor)
add('900', _("Administrator"),                 SiteAdmin, name='admin')
