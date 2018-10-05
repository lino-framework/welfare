.. doctest docs/specs/usertypes.rst
.. _welfare.usertypes:

====================================
The Lino Welfare Standard User Types
====================================

..  doctest init:

    >>> from lino import startup
    >>> startup('lino_welfare.projects.eupen.settings.doctests')
    >>> from lino.api.doctest import *


Defining user types and their respective permissions is a complex area
where it is difficult to get an overview and where it is easy to
forget some aspect when deciding about a change.  This document is an
attempt to fix this problem at least for Lino Welfare by developing a
standard set of user types.

The default set of user types for Lino Welfare is defined in the
:mod:`lino_welfare.modlib.welfare.user_types` module.  Individual
centers can define their own local :attr:`user_types_module
<lino.core.site.Site.user_types_module>`, Lino does not force you to
use the following.

But we recommend to use the standard set of user types and to join our
common effort.  If you discover a problem with what's described
hereafter, please contact the responsible author (currently Luc
Saffre).

The default set of user types for Lino Welfare lives in the
:class:`lino.modlib.users.UserTypes` choicelist:

>>> rt.show(users.UserTypes, language="en")
======= =========== ============================== =================================================================
 value   name        text                           User role
------- ----------- ------------------------------ -----------------------------------------------------------------
 000     anonymous   Anonymous                      lino.core.roles.Anonymous
 100                 Integration agent              lino_welfare.modlib.welfare.user_types.IntegrationAgent
 110                 Integration agent (Manager)    lino_welfare.modlib.welfare.user_types.IntegrationAgentManager
 120                 Integration agent (Flexible)   lino_welfare.modlib.welfare.user_types.IntegrationAgentFlexible
 200                 Newcomers consultant           lino_welfare.modlib.welfare.user_types.NewcomersConsultant
 210                 Reception clerk                lino_welfare.modlib.welfare.user_types.ReceptionClerk
 220                 Reception clerk (Flexible)     lino_welfare.modlib.welfare.user_types.ReceptionClerkFlexible
 300                 Debts consultant               lino_welfare.modlib.welfare.user_types.DebtsConsultant
 400                 Social agent                   lino_welfare.modlib.welfare.user_types.SocialAgent
 410                 Social agent (Manager)         lino_welfare.modlib.welfare.user_types.SocialAgentManager
 420                 Social agent (Flexible)        lino_welfare.modlib.welfare.user_types.IntegrationAgentFlexible
 500                 Accountant                     lino_welfare.modlib.welfare.user_types.Accountant
 510                 Accountant (Manager)           lino_welfare.modlib.welfare.user_types.AccountantManager
 800                 Supervisor                     lino_welfare.modlib.welfare.user_types.Supervisor
 900     admin       Administrator                  lino_welfare.modlib.welfare.user_types.SiteAdmin
 910                 Security advisor               lino_welfare.modlib.welfare.user_types.SecurityAdvisor
======= =========== ============================== =================================================================
<BLANKLINE>

A **social agent** is a user who does individual coaching of
clients.  Certain privacy-relevant client data is visible only
to social agents.

A **social staff member** is a social agent who has access to more
technical information about welfare clients.  For example the
`Miscellaneous` panel.


An **integration agent** is a specialized social agent who works with
immigrants who want to integrate into local society.  They can access
database content specific to integration work: CV, language courses,
workshops, ...

A *flexible* integration agent can also assign coaches to clients and
create budgets for debts mediation.


A **newcomers consultant** manages new client applications.

A **newcomers operator** is a user who is not *social agent* but
can e.g. register newcomers and assign them a coach.

A **reception clerk** is a user who is not a *social agent* but
receives clients and does certain administrative tasks (in Eupen they
call them `back office
<https://en.wikipedia.org/wiki/Back_office>`__).  A flexible
*reception clerk* can also  assign coaches to clients.


An **accountant** is a user who enters invoices, bank statements,
payment orders and other ledger operations.
The *manager* variant also has access to configuration.

A **site adminstrator** has permission for everything.

A **supervisor** is a backoffice user who can act as others.


The *Manager* variants of *Integration agent*, *Social agent* and
*Accountant* give some additional permissions like editing contracts
authored by other users, more configuration options, but they are not
a :class:`SiteStaff <lino.core.roles.SiteStaff>`.

The *Flexible* variants 120, 220 and 420 are designed to be used in
centers where they don't use 100, 200 and 400.

An *Integration agent (Manager)* has some staff permissions

>>> from lino.core.roles import SiteStaff
>>> from lino_xl.lib.contacts.roles import ContactsStaff

>>> p100 = users.UserTypes.get_by_value('100')
>>> p110 = users.UserTypes.get_by_value('110')
>>> p210 = users.UserTypes.get_by_value('210')

>>> p110.has_required_roles([SiteStaff])
False
>>> p210.has_required_roles([SiteStaff])
False

A reception clerk is a :class:`ContactsStaff
<lino_xl.lib.contacts.ContactsStaff>`:

>>> p100.has_required_roles([ContactsStaff])
False
>>> p110.has_required_roles([ContactsStaff])
True
>>> p210.has_required_roles([ContactsStaff])
True

A reception clerk is an :class:`OfficeOperator`:

>>> from lino_welfare.modlib.welfare.user_types import OfficeOperator
>>> p210.has_required_roles([OfficeOperator])
True

A reception clerk can see the :guilabel:`Calendar` tab because it
contains the :class:`EntriesByClient
<lino_welfare.modlib.cal.EntriesByClient>` panel.  Since 20180124 also
TasksByProject of that tab.

>>> cal.EntriesByClient.get_view_permission(p210)
True

>>> print(py2rst(pcsw.Clients.detail_layout['calendar']))
**Kalender** (calendar) [visible for 100 110 120 200 210 220 300 400 410 420 500 510 800 admin 910]:
- **Kalendereinträge** (cal.EntriesByClient)
- **Aufgaben** (cal.TasksByProject)
<BLANKLINE>


>>> rt.show(users.UserRoles)
+----------------------------------+----------------------------------------------------------------------------------+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
| Name                             | Beschreibung                                                                     | 000 | 100 | 110 | 120 | 200 | 210 | 220 | 300 | 400 | 410 | 420 | 500 | 510 | 800 | 900 | 910 |
+==================================+==================================================================================+=====+=====+=====+=====+=====+=====+=====+=====+=====+=====+=====+=====+=====+=====+=====+=====+
| about.SiteSearcher               |                                                                                  |     |     |     |     |     |     |     |     |     |     |     |     |     |     | ☑   | ☑   |
+----------------------------------+----------------------------------------------------------------------------------+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
| aids.AidsStaff                   | A user who can manage aids grantings and confirmations.                          |     |     | ☑   | ☑   |     | ☑   |     |     |     | ☑   | ☑   | ☑   | ☑   | ☑   | ☑   | ☑   |
+----------------------------------+----------------------------------------------------------------------------------+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
| aids.AidsUser                    | A user who can issue aids grantings and confirmations.                           |     | ☑   | ☑   | ☑   | ☑   | ☑   |     | ☑   | ☑   | ☑   | ☑   | ☑   | ☑   | ☑   | ☑   | ☑   |
+----------------------------------+----------------------------------------------------------------------------------+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
| beid.BeIdUser                    |                                                                                  |     | ☑   | ☑   | ☑   | ☑   | ☑   | ☑   | ☑   | ☑   | ☑   | ☑   |     |     | ☑   | ☑   | ☑   |
+----------------------------------+----------------------------------------------------------------------------------+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
| cal.GuestOperator                |                                                                                  |     | ☑   | ☑   | ☑   | ☑   | ☑   | ☑   | ☑   | ☑   | ☑   | ☑   |     |     | ☑   | ☑   | ☑   |
+----------------------------------+----------------------------------------------------------------------------------+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
| cbss.CBSSUser                    |                                                                                  |     | ☑   | ☑   | ☑   | ☑   | ☑   |     | ☑   | ☑   | ☑   | ☑   |     |     |     | ☑   | ☑   |
+----------------------------------+----------------------------------------------------------------------------------+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
| checkdata.CheckdataUser          | A user who can see data problems.                                                |     | ☑   | ☑   | ☑   | ☑   |     |     | ☑   | ☑   | ☑   | ☑   |     |     |     | ☑   | ☑   |
+----------------------------------+----------------------------------------------------------------------------------+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
| coachings.CoachingsStaff         |                                                                                  |     |     | ☑   | ☑   |     | ☑   |     |     |     | ☑   | ☑   |     |     |     | ☑   | ☑   |
+----------------------------------+----------------------------------------------------------------------------------+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
| coachings.CoachingsUser          |                                                                                  |     | ☑   | ☑   | ☑   | ☑   | ☑   |     | ☑   | ☑   | ☑   | ☑   |     |     |     | ☑   | ☑   |
+----------------------------------+----------------------------------------------------------------------------------+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
| contacts.ContactsStaff           |                                                                                  |     |     | ☑   | ☑   |     | ☑   |     |     |     | ☑   | ☑   |     |     | ☑   | ☑   | ☑   |
+----------------------------------+----------------------------------------------------------------------------------+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
| contacts.ContactsUser            |                                                                                  |     | ☑   | ☑   | ☑   | ☑   | ☑   |     | ☑   | ☑   | ☑   | ☑   | ☑   | ☑   | ☑   | ☑   | ☑   |
+----------------------------------+----------------------------------------------------------------------------------+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
| contacts.SimpleContactsUser      |                                                                                  |     | ☑   | ☑   | ☑   | ☑   | ☑   | ☑   | ☑   | ☑   | ☑   | ☑   | ☑   | ☑   | ☑   | ☑   | ☑   |
+----------------------------------+----------------------------------------------------------------------------------+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
| core.Anonymous                   | The role used by anonymous guest sessions.                                       | ☑   |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |
+----------------------------------+----------------------------------------------------------------------------------+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
| core.SiteUser                    | Every authenticated user has this role.                                          |     | ☑   | ☑   | ☑   | ☑   | ☑   | ☑   | ☑   | ☑   | ☑   | ☑   | ☑   | ☑   | ☑   | ☑   | ☑   |
+----------------------------------+----------------------------------------------------------------------------------+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
| courses.CoursesUser              | Can see and edit all courses.                                                    |     | ☑   | ☑   | ☑   | ☑   | ☑   |     | ☑   | ☑   | ☑   | ☑   |     |     | ☑   | ☑   | ☑   |
+----------------------------------+----------------------------------------------------------------------------------+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
| cv.CareerStaff                   |                                                                                  |     |     | ☑   | ☑   |     |     |     |     |     |     | ☑   |     |     |     | ☑   | ☑   |
+----------------------------------+----------------------------------------------------------------------------------+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
| cv.CareerUser                    |                                                                                  |     | ☑   | ☑   | ☑   |     |     |     |     |     |     | ☑   |     |     |     | ☑   | ☑   |
+----------------------------------+----------------------------------------------------------------------------------+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
| debts.DebtsStaff                 |                                                                                  |     |     |     |     |     |     |     |     |     |     |     |     |     |     | ☑   | ☑   |
+----------------------------------+----------------------------------------------------------------------------------+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
| debts.DebtsUser                  |                                                                                  |     |     |     | ☑   |     |     |     | ☑   |     |     | ☑   |     |     |     | ☑   | ☑   |
+----------------------------------+----------------------------------------------------------------------------------+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
| excerpts.ExcerptsStaff           |                                                                                  |     |     |     |     |     |     |     |     |     |     |     |     |     |     | ☑   | ☑   |
+----------------------------------+----------------------------------------------------------------------------------+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
| excerpts.ExcerptsUser            |                                                                                  |     | ☑   | ☑   | ☑   |     | ☑   | ☑   |     | ☑   | ☑   | ☑   | ☑   | ☑   | ☑   | ☑   | ☑   |
+----------------------------------+----------------------------------------------------------------------------------+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
| integ.IntegUser                  |                                                                                  |     | ☑   | ☑   | ☑   |     |     |     |     |     |     | ☑   |     |     |     | ☑   | ☑   |
+----------------------------------+----------------------------------------------------------------------------------+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
| integ.IntegrationStaff           |                                                                                  |     |     | ☑   | ☑   |     |     |     |     |     |     | ☑   |     |     |     | ☑   | ☑   |
+----------------------------------+----------------------------------------------------------------------------------+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
| ledger.LedgerStaff               |                                                                                  |     |     |     |     |     |     |     |     |     |     |     |     | ☑   |     | ☑   | ☑   |
+----------------------------------+----------------------------------------------------------------------------------+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
| ledger.LedgerUser                |                                                                                  |     |     |     |     |     |     |     |     |     |     |     | ☑   | ☑   |     | ☑   | ☑   |
+----------------------------------+----------------------------------------------------------------------------------+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
| newcomers.NewcomersOperator      |                                                                                  |     |     | ☑   | ☑   | ☑   |     | ☑   | ☑   |     |     | ☑   |     |     | ☑   | ☑   | ☑   |
+----------------------------------+----------------------------------------------------------------------------------+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
| newcomers.NewcomersUser          |                                                                                  |     |     |     | ☑   | ☑   |     | ☑   | ☑   |     |     | ☑   |     |     |     | ☑   | ☑   |
+----------------------------------+----------------------------------------------------------------------------------+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
| notes.NotesUser                  |                                                                                  |     | ☑   | ☑   | ☑   | ☑   | ☑   | ☑   | ☑   | ☑   | ☑   | ☑   | ☑   | ☑   | ☑   | ☑   | ☑   |
+----------------------------------+----------------------------------------------------------------------------------+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
| office.OfficeOperator            | A user who manages office functionality for other users (but not for himself).   |     |     | ☑   | ☑   | ☑   | ☑   | ☑   | ☑   |     | ☑   | ☑   |     |     | ☑   | ☑   | ☑   |
|                                  | Currently an office operator can create their own notes and uploads, but no      |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |
|                                  | calendar entries. For example the `lino_xl.lib.cal.ui.OverdueAppointments` table |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |
|                                  | requires :class:`OfficeStaff` and is *not* available for                         |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |
|                                  | :class:`OfficeOperator`.                                                         |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |
+----------------------------------+----------------------------------------------------------------------------------+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
| office.OfficeStaff               | A user who manages configuration of office functionality.                        |     |     | ☑   | ☑   |     |     |     |     |     | ☑   | ☑   |     |     |     | ☑   | ☑   |
+----------------------------------+----------------------------------------------------------------------------------+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
| office.OfficeUser                | A user who has access to office functionality like calendar, notes and uploads.  |     | ☑   | ☑   | ☑   | ☑   |     |     | ☑   | ☑   | ☑   | ☑   | ☑   | ☑   |     | ☑   | ☑   |
+----------------------------------+----------------------------------------------------------------------------------+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
| pcsw.SocialCoordinator           | Reception clerks (210) can see contracts.                                        |     |     |     |     |     | ☑   |     |     | ☑   | ☑   |     |     |     |     |     |     |
+----------------------------------+----------------------------------------------------------------------------------+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
| pcsw.SocialStaff                 |                                                                                  |     |     | ☑   | ☑   |     |     |     |     |     | ☑   | ☑   |     |     |     | ☑   | ☑   |
+----------------------------------+----------------------------------------------------------------------------------+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
| pcsw.SocialUser                  |                                                                                  |     | ☑   | ☑   | ☑   | ☑   |     |     | ☑   | ☑   | ☑   | ☑   |     |     |     | ☑   | ☑   |
+----------------------------------+----------------------------------------------------------------------------------+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
| polls.PollsStaff                 | Can create new polls.                                                            |     |     | ☑   | ☑   |     |     |     |     |     | ☑   | ☑   |     |     |     | ☑   | ☑   |
+----------------------------------+----------------------------------------------------------------------------------+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
| polls.PollsUser                  | Can see polls and create new responses.                                          |     | ☑   | ☑   | ☑   | ☑   |     |     | ☑   | ☑   | ☑   | ☑   |     |     |     | ☑   | ☑   |
+----------------------------------+----------------------------------------------------------------------------------+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
| sepa.SepaStaff                   | Can see imported statements and movements also globally in the                   |     |     | ☑   | ☑   |     |     |     |     |     | ☑   | ☑   | ☑   | ☑   |     | ☑   | ☑   |
|                                  | :menuselection`Explorer` menu.                                                   |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |
+----------------------------------+----------------------------------------------------------------------------------+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
| sepa.SepaUser                    | Can see imported statements and movements per partner.                           |     | ☑   | ☑   | ☑   | ☑   | ☑   |     | ☑   | ☑   | ☑   | ☑   | ☑   | ☑   | ☑   | ☑   | ☑   |
+----------------------------------+----------------------------------------------------------------------------------+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
| users.AuthorshipTaker            |                                                                                  |     |     |     |     |     | ☑   | ☑   |     | ☑   | ☑   |     |     |     | ☑   | ☑   | ☑   |
+----------------------------------+----------------------------------------------------------------------------------+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
| welfare.Accountant               |                                                                                  |     |     |     |     |     |     |     |     |     |     |     | ☑   |     |     |     |     |
+----------------------------------+----------------------------------------------------------------------------------+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
| welfare.AccountantManager        |                                                                                  |     |     |     |     |     |     |     |     |     |     |     |     | ☑   |     |     |     |
+----------------------------------+----------------------------------------------------------------------------------+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
| welfare.DebtsConsultant          |                                                                                  |     |     |     |     |     |     |     | ☑   |     |     |     |     |     |     |     |     |
+----------------------------------+----------------------------------------------------------------------------------+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
| welfare.IntegrationAgent         |                                                                                  |     | ☑   | ☑   | ☑   |     |     |     |     |     |     | ☑   |     |     |     |     |     |
+----------------------------------+----------------------------------------------------------------------------------+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
| welfare.IntegrationAgentFlexible |                                                                                  |     |     |     | ☑   |     |     |     |     |     |     | ☑   |     |     |     |     |     |
+----------------------------------+----------------------------------------------------------------------------------+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
| welfare.IntegrationAgentManager  |                                                                                  |     |     | ☑   | ☑   |     |     |     |     |     |     | ☑   |     |     |     |     |     |
+----------------------------------+----------------------------------------------------------------------------------+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
| welfare.NewcomersConsultant      |                                                                                  |     |     |     |     | ☑   |     |     |     |     |     |     |     |     |     |     |     |
+----------------------------------+----------------------------------------------------------------------------------+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
| welfare.ReceptionClerk           |                                                                                  |     |     |     |     |     | ☑   |     |     |     |     |     |     |     |     |     |     |
+----------------------------------+----------------------------------------------------------------------------------+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
| welfare.ReceptionClerkFlexible   |                                                                                  |     |     |     |     |     |     | ☑   |     |     |     |     |     |     |     |     |     |
+----------------------------------+----------------------------------------------------------------------------------+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
| welfare.SecurityAdvisor          |                                                                                  |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     | ☑   |
+----------------------------------+----------------------------------------------------------------------------------+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
| welfare.SiteAdmin                |                                                                                  |     |     |     |     |     |     |     |     |     |     |     |     |     |     | ☑   | ☑   |
+----------------------------------+----------------------------------------------------------------------------------+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
| welfare.SocialAgent              |                                                                                  |     |     |     |     |     |     |     |     | ☑   | ☑   |     |     |     |     |     |     |
+----------------------------------+----------------------------------------------------------------------------------+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
| welfare.SocialAgentManager       |                                                                                  |     |     |     |     |     |     |     |     |     | ☑   |     |     |     |     |     |     |
+----------------------------------+----------------------------------------------------------------------------------+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
| welfare.Supervisor               |                                                                                  |     |     |     |     |     |     |     |     |     |     |     |     |     | ☑   |     |     |
+----------------------------------+----------------------------------------------------------------------------------+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
| xcourses.CoursesStaff            |                                                                                  |     |     | ☑   | ☑   |     |     |     |     |     |     | ☑   |     |     |     | ☑   | ☑   |
+----------------------------------+----------------------------------------------------------------------------------+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
| xcourses.CoursesUser             |                                                                                  |     | ☑   | ☑   | ☑   |     |     |     |     |     |     | ☑   |     |     |     | ☑   | ☑   |
+----------------------------------+----------------------------------------------------------------------------------+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
<BLANKLINE>

The user types are only the tip of the iceberg.  A user type is an
arbitrary choice of user roles made available for a given application.
Lino defines a lot of user roles.  For example, the following diagram
visualizes the genealogy of a reception clerk:

For example the :class:`lino_welfare.modlib.isip.ContractsByClient`
table is visible for users having the IntegUser or SocialCoordinator
role:

>>> isip.ContractsByClient.required_roles
set([(<class 'lino_welfare.modlib.integ.roles.IntegUser'>, <class 'lino_welfare.modlib.pcsw.roles.SocialCoordinator'>)])
>>> print(visible_for(isip.ContractsByClient))
100 110 120 210 400 410 420 admin 910
