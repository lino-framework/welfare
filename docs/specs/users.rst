.. doctest docs/specs/users.rst
.. _welfare.specs.users:

=============
Users
=============

..  doctest init:

    >>> from lino import startup
    >>> startup('lino_welfare.projects.eupen.settings.doctests')
    >>> from lino.api.doctest import *

This document describes how Lino Welfare uses the
:mod:`lino.modlib.users` plugin.

.. contents::
   :depth: 2

User types
=============

The default set of user types for Lino Welfare is defined in
:mod:`lino_welfare.modlib.welfare.user_types` and leads to the
following list:

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
 500                 Accountant                     lino_welfare.modlib.welfare.user_types.LedgerUser
 510                 Accountant (Manager)           lino_welfare.modlib.welfare.user_types.AccountantManager
 800                 Supervisor                     lino_welfare.modlib.welfare.user_types.Supervisor
 900     admin       Administrator                  lino_welfare.modlib.welfare.user_types.SiteAdmin
 910                 Security advisor               lino_welfare.modlib.welfare.user_types.SecurityAdvisor
======= =========== ============================== =================================================================
<BLANKLINE>


**Remarks:**

The *Manager* variants of *Integration agent*, *Social agent* and
*Accountant* give some additional permissions like editing contracts
authored by other users, more configuration options, but they are not
a :class:`SiteStaff <lino.core.roles.SiteStaff>`.

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



Demo users
==========

>>> rt.show('users.Users', language="en")
========== ============================= ============ ===========
 Username   User type                     First name   Last name
---------- ----------------------------- ------------ -----------
 alicia     Integration agent             Alicia       Allmanns
 caroline   Newcomers consultant          Caroline     Carnol
 hubert     Integration agent             Hubert       Huppertz
 judith     Social agent                  Judith       Jousten
 kerstin    Debts consultant              Kerstin      Kerres
 melanie    Integration agent (Manager)   Mélanie      Mélard
 nicolas
 patrick    Security advisor              Patrick      Paraneau
 robin      Administrator                 Robin        Rood
 rolf       Administrator                 Rolf         Rompen
 romain     Administrator                 Romain       Raffault
 theresia   Reception clerk               Theresia     Thelen
 wilfried   Accountant                    Wilfried     Willems
========== ============================= ============ ===========
<BLANKLINE>



Authorities
===========

Alicia, Hubert and Mélanie give "authority" to Theresia to do their
work when they are absent.

>>> rt.show(rt.actors.users.Authorities, language="en")
==== ================= =================
 ID   Author            User
---- ----------------- -----------------
 1    Hubert Huppertz   Theresia Thelen
 2    Alicia Allmanns   Theresia Thelen
 3    Mélanie Mélard    Theresia Thelen
==== ================= =================
<BLANKLINE>


