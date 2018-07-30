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

The default set of user types for Lino Welfare is defined in the
:mod:`lino_welfare.modlib.welfare.user_types` module:

>>> rt.show(users.UserTypes, language="en")
======= =========== ============================== =================================================================
 value   name        text                           User role
------- ----------- ------------------------------ -----------------------------------------------------------------
 000     anonymous   Anonymous                      lino.core.roles.Anonymous
 100                 Integration agent              lino_welfare.modlib.integ.roles.IntegrationAgent
 110                 Integration agent (Manager)    lino_welfare.modlib.integ.roles.IntegrationStaff
 120                 Integration agent (Flexible)   lino_welfare.modlib.welfare.user_types.IntegrationAgentFlexible
 200                 Newcomers consultant           lino_welfare.modlib.welfare.user_types.NewcomersConsultant
 210                 Reception clerk                lino_welfare.modlib.welfare.user_types.ReceptionClerk
 220                 Reception clerk (Flexible)     lino_welfare.modlib.welfare.user_types.ReceptionClerkFlexible
 300                 Debts consultant               lino_welfare.modlib.debts.roles.DebtsUser
 400                 Social agent                   lino_welfare.modlib.pcsw.roles.SocialAgent
 410                 Social agent (Manager)         lino_welfare.modlib.pcsw.roles.SocialStaff
 420                 Social agent (Flexible)        lino_welfare.modlib.welfare.user_types.IntegrationAgentFlexible
 500                 Accountant                     lino_welfare.modlib.welfare.user_types.Accountant
 510                 Accountant (Manager)           lino_welfare.modlib.welfare.user_types.AccountantManager
 800                 Supervisor                     lino_welfare.modlib.welfare.user_types.Supervisor
 900     admin       Administrator                  lino_welfare.modlib.welfare.user_types.SiteAdmin
 910                 Security advisor               lino_welfare.modlib.welfare.user_types.SecurityAdvisor
======= =========== ============================== =================================================================
<BLANKLINE>


The *Manager* variants of *Integration agent*, *Social agent* and
*Accountant* give some additional permissions like editing contracts
authored by other users, more configuration options, but they are not
a :class:`SiteStaff <lino.core.roles.SiteStaff>`.

The *Flexible* variants 120, 220 and 420 are designed to be used in
centers where they don't use 100, 200 and 400.

An integration agent (manager) has some staff permissions

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

The user types are only the tip of the iceberg.  A user type is an
arbitrary choice of user roles made available for a given application.
Lino defines a lot of user roles.  For example, the following diagram
visualizes the genealogy of a reception clerk:

.. inheritance-diagram:: lino_welfare.modlib.welfare.user_types.ReceptionClerk



