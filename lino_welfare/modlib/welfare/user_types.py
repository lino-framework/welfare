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

from lino.core.roles import Anonymous, SiteUser, SiteAdmin, Supervisor, login_required
from lino.modlib.users.roles import AuthorshipTaker
from lino.modlib.about.roles import SiteSearcher
from lino.modlib.office.roles import OfficeOperator, OfficeStaff, OfficeUser
from lino_xl.lib.notes.roles import NotesUser
from lino_xl.lib.excerpts.roles import ExcerptsUser, ExcerptsStaff
from lino_xl.lib.contacts.roles import ContactsStaff, ContactsUser, SimpleContactsUser
from lino_xl.lib.ledger.roles import LedgerStaff, LedgerUser
from lino_xl.lib.sepa.roles import SepaStaff
from lino_xl.lib.cal.roles import GuestOperator
from lino_xl.lib.sepa.roles import SepaUser
from lino_xl.lib.courses.roles import CoursesUser
from lino_xl.lib.cv.roles import CareerUser
from lino_xl.lib.beid.roles import BeIdUser
from lino_welfare.modlib.cbss.roles import CBSSUser, SecurityAdvisor
from lino_xl.lib.coachings.roles import CoachingsStaff
from lino_welfare.modlib.pcsw.roles import SocialAgent
from lino_welfare.modlib.pcsw.roles import SocialStaff
from lino_welfare.modlib.pcsw.roles import SocialCoordinator
from lino_welfare.modlib.aids.roles import AidsStaff
from lino_welfare.modlib.integ.roles import IntegrationAgent, IntegrationStaff
from lino_welfare.modlib.debts.roles import DebtsUser, DebtsStaff
from lino_welfare.modlib.newcomers.roles import (NewcomersAgent,
                                                 NewcomersOperator)


class ReceptionClerk(SiteUser, AuthorshipTaker, OfficeOperator,
                     GuestOperator, NotesUser,
                     ContactsStaff, AidsStaff, CBSSUser, BeIdUser,
                     SepaUser, CoursesUser, ExcerptsUser,
                     SocialCoordinator, CoachingsStaff):
    """
    A **reception clerk** is a user who is not a *social agent* but
    receives clients and does certain administrative tasks (in Eupen
    they call them `back office
    <https://en.wikipedia.org/wiki/Back_office>`__).

    """
    pass


class ReceptionClerkFlexible(SiteUser, AuthorshipTaker, SimpleContactsUser,
                             OfficeOperator, NotesUser,
                             GuestOperator,
                             ExcerptsUser,
                             # OfficeUser,
                             # SocialAgent,
                             # CoursesUser,
                             NewcomersAgent,
                             BeIdUser):
    """
    A **newcomers reception clerk** is a *reception clerk* who also
    can assign coaches to clients.

    """
    pass


class IntegrationAgentFlexible(IntegrationStaff, DebtsUser):
    """
    A **flexible integration agent** is an *integration agent* who
    also can assign coaches to clients and create budgets for debts
    mediation.

    """
    pass

# class SocialAgentFlexible(SocialAgent, SocialCoordinator, CareerUser):
#     """
#     A **flexible social agent** is an *social agent* who also can see
#     PARCOURS – COMPÉTENCES – FREINS - STAGES D’IMMERSION - MÉDIATION
#     DE DETTES.
#     """
#     pass


class Accountant(SiteUser, LedgerUser, ContactsUser, OfficeUser,
                 NotesUser, ExcerptsUser, AidsStaff, SepaStaff):
    """
    An **accountant** is a user who enters invoices, bank statements,
    payment orders and other ledger operations.

    """
    pass


class AccountantManager(SiteUser, LedgerStaff, ContactsUser, OfficeUser,
                        ExcerptsUser, AidsStaff, SepaStaff, NotesUser):
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


class SecurityAdvisor(SiteAdmin, SecurityAdvisor):
    pass

class NewcomersConsultant(NewcomersAgent, SocialAgent, NotesUser):
    pass

class Supervisor(SiteUser, Supervisor, AuthorshipTaker, OfficeOperator,
                 GuestOperator, NotesUser,
                 ContactsStaff, AidsStaff, NewcomersOperator,
                 ExcerptsUser, SepaUser, CoursesUser):
    """A backoffice user who can act as others."""
    pass


from lino.modlib.users.choicelists import UserTypes
from lino.api import _

UserTypes.clear()
UserTypes.show_values = True

add = UserTypes.add_item

add('000', _("Anonymous"), Anonymous, name='anonymous',
    readonly=True, authenticated=False)
add('100', _("Integration agent"),             IntegrationAgent)
add('110', _("Integration agent (Manager)"),   IntegrationStaff)
add('120', _("Integration agent (Flexible)"),  IntegrationAgentFlexible)
add('200', _("Newcomers consultant"),          NewcomersConsultant)
add('210', _("Reception clerk"),               ReceptionClerk)
add('220', _("Reception clerk (Flexible)"),    ReceptionClerkFlexible)
add('300', _("Debts consultant"),              DebtsUser)
add('400', _("Social agent"),                  SocialAgent)
add('410', _("Social agent (Manager)"),        SocialStaff)
add('420', _("Social agent (Flexible)"),       IntegrationAgentFlexible)
add('500', _("Accountant"),                    Accountant)
add('510', _("Accountant (Manager)"),          AccountantManager)
add('800', _("Supervisor"),                    Supervisor)
add('900', _("Administrator"),                 SiteAdmin, name='admin')
add('910', _("Security advisor"),              SecurityAdvisor)

from lino.modlib.notify.choicelists import MessageTypes
UserTypes.get_by_value('420').mask_notifications(MessageTypes.change)
