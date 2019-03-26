# -*- coding: UTF-8 -*-
# Copyright 2009-2018 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

"""Defines default user profiles and shortcuts for Lino Welfare.

See :doc:`/specs/usertypes`.

"""

from lino.core.roles import Anonymous, SiteUser, SiteAdmin, Supervisor
from lino.modlib.users.roles import AuthorshipTaker
from lino.modlib.about.roles import SiteSearcher
from lino.modlib.office.roles import OfficeOperator, OfficeStaff, OfficeUser
from lino_xl.lib.notes.roles import NotesUser, NotesStaff
from lino_xl.lib.excerpts.roles import ExcerptsUser, ExcerptsStaff
from lino_xl.lib.contacts.roles import ContactsStaff, ContactsUser, SimpleContactsUser
from lino_xl.lib.ledger.roles import LedgerStaff, LedgerUser
from lino_xl.lib.cal.roles import GuestOperator
from lino_xl.lib.courses.roles import CoursesUser
from lino_xl.lib.cv.roles import CareerUser, CareerStaff
from lino_xl.lib.beid.roles import BeIdUser
from lino_welfare.modlib.cbss.roles import CBSSUser, SecurityAdvisor
from lino_welfare.modlib.pcsw.roles import SocialUser
from lino_welfare.modlib.pcsw.roles import SocialStaff
from lino_welfare.modlib.pcsw.roles import SocialCoordinator
from lino_welfare.modlib.aids.roles import AidsStaff,  AidsUser
from lino_welfare.modlib.xcourses.roles import CoursesUser as xCoursesUser
from lino_welfare.modlib.xcourses.roles import CoursesStaff as xCoursesStaff
from lino_welfare.modlib.integ.roles import IntegUser, IntegrationStaff
from lino_welfare.modlib.debts.roles import DebtsUser, DebtsStaff

from lino_welfare.modlib.newcomers.roles import (NewcomersUser,
                                                 NewcomersOperator)

from lino_xl.lib.polls.roles import PollsUser, PollsStaff
from lino.modlib.checkdata.roles import CheckdataUser
from lino_xl.lib.sepa.roles import SepaUser, SepaStaff
from lino_xl.lib.coachings.roles import CoachingsUser, CoachingsStaff

# class CoursesUser(CoursesUser, xCoursesUser):
#     pass


# 210
class ReceptionClerk(SiteUser, AuthorshipTaker,
                     OfficeOperator, NotesUser,
                     GuestOperator,
                     ContactsStaff, AidsStaff, CBSSUser, BeIdUser,
                     SepaUser, ExcerptsUser, CoursesUser,
                     SocialCoordinator, CoachingsStaff):
    pass


class ReceptionClerkFlexible(SiteUser, AuthorshipTaker,
                             SimpleContactsUser,
                             OfficeOperator, NotesUser,
                             GuestOperator, BeIdUser,
                             ExcerptsUser,
                             # AidsStaff,
                             # OfficeUser,
                             # SocialUser,
                             # CoursesUser,
                             NewcomersUser):
    pass

class IntegrationAgent(SiteUser, IntegUser, SocialUser, CareerUser,
                       CoursesUser, xCoursesUser, OfficeUser, CBSSUser,
                       CheckdataUser, AidsUser, PollsUser, SepaUser,
                       ExcerptsUser, CoachingsUser, BeIdUser,
                       GuestOperator, ContactsUser, NotesUser):
    pass


class IntegrationAgentManager(IntegrationAgent,
                              IntegrationStaff,
                              OfficeStaff, NotesStaff, CoachingsStaff, AidsStaff,
                              ContactsStaff, SocialStaff, CareerStaff,
                              NewcomersOperator, 
                              xCoursesStaff, SepaStaff, PollsStaff):
    pass
                              
class IntegrationAgentFlexible(NewcomersUser, IntegrationAgentManager,
                               BeIdUser, DebtsUser):
    pass

class SocialAgent(SiteUser, SocialUser,
                  OfficeUser, ContactsUser, CBSSUser, BeIdUser,
                  CheckdataUser, AidsUser, PollsUser, SepaUser,
                  CoursesUser, SocialCoordinator,
                  ExcerptsUser, CoachingsUser,
                  AuthorshipTaker, GuestOperator, NotesUser):
    pass

class SocialAgentManager(SocialAgent, SocialStaff, OfficeStaff,
                         ContactsStaff, AidsStaff, PollsStaff,
                         SepaStaff, CoachingsStaff):
    pass

class DebtsConsultant(SiteUser, DebtsUser, SocialUser, OfficeUser,
                      OfficeOperator, ContactsUser, CBSSUser,
                      CoursesUser,
                      PollsUser,
                      BeIdUser, NotesUser, CheckdataUser, AidsUser,
                      GuestOperator, CoachingsUser, SepaUser,
                      NewcomersUser):
    pass


class NewcomersConsultant(SiteUser, NewcomersUser, SocialUser,
                          OfficeUser, OfficeOperator, ContactsUser,
                          CBSSUser, BeIdUser, NotesUser, CoursesUser, 
                          CheckdataUser, AidsUser, CoachingsUser,
                          PollsUser,
                          GuestOperator, SepaUser):
    pass

class Accountant(SiteUser, LedgerUser, ContactsUser, OfficeUser,
                 NotesUser, ExcerptsUser, AidsStaff, SepaStaff):
    pass


class AccountantManager(SiteUser, LedgerStaff, ContactsUser, OfficeUser,
                        ExcerptsUser, AidsStaff, SepaStaff, NotesUser):
    pass


class SiteAdmin(
        SiteAdmin,
        AidsStaff,
        AuthorshipTaker,
        BeIdUser,
        CBSSUser,
        CareerStaff,
        CheckdataUser,
        CoachingsStaff,
        ContactsStaff,
        CoursesUser,
        xCoursesStaff,
        DebtsStaff,
        ExcerptsStaff,
        GuestOperator,
        IntegrationStaff,
        LedgerStaff,
        NewcomersUser,
        NotesStaff,
        OfficeStaff,
        PollsStaff,
        SepaStaff,
        SiteSearcher,
        SocialStaff):
    pass

class SecurityAdvisor(SiteAdmin, SecurityAdvisor):
    pass

class Supervisor(SiteUser, Supervisor, AuthorshipTaker,
                 OfficeOperator, BeIdUser,
                 GuestOperator, CoursesUser, NotesUser,
                 ContactsStaff, AidsStaff, NewcomersOperator,
                 ExcerptsUser, SepaUser):
    pass


from lino.modlib.users.choicelists import UserTypes
from lino.api import _

UserTypes.clear()
UserTypes.show_values = True

add = UserTypes.add_item

add('000', _("Anonymous"), Anonymous, name='anonymous',
    readonly=True, authenticated=False)
add('100', _("Integration agent"),             IntegrationAgent)
add('110', _("Integration agent (Manager)"),   IntegrationAgentManager)
add('120', _("Integration agent (Flexible)"),  IntegrationAgentFlexible)
add('200', _("Newcomers consultant"),          NewcomersConsultant)
add('210', _("Reception clerk"),               ReceptionClerk)
add('220', _("Reception clerk (Flexible)"),    ReceptionClerkFlexible)
add('300', _("Debts consultant"),              DebtsConsultant)
add('400', _("Social agent"),                  SocialAgent)
add('410', _("Social agent (Manager)"),        SocialAgentManager)
add('420', _("Social agent (Flexible)"),       IntegrationAgentFlexible)
add('500', _("Accountant"),                    Accountant)
add('510', _("Accountant (Manager)"),          AccountantManager)
add('800', _("Supervisor"),                    Supervisor)
add('900', _("Administrator"),                 SiteAdmin, name='admin')
add('910', _("Security advisor"),              SecurityAdvisor)

from lino.modlib.notify.choicelists import MessageTypes
UserTypes.get_by_value('420').mask_notifications(MessageTypes.change)

