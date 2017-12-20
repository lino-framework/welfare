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

>>> rt.show(users.UserTypes)
====== =========== ================================== ==================================================================
 Wert   name        Text                               User role
------ ----------- ---------------------------------- ------------------------------------------------------------------
 000    anonymous   Anonym                             lino.core.roles.Anonymous
 100                Begleiter im DSBE                  lino_welfare.modlib.integ.roles.IntegrationAgent
 110                Begleiter im DSBE (Manager)        lino_welfare.modlib.integ.roles.IntegrationStaff
 120                Begleiter im DSBE (+Erstempfang)   lino_welfare.modlib.welfare.user_types.IntegrationAgentNewcomers
 200                Berater Erstempfang                lino_welfare.modlib.welfare.user_types.NewcomersConsultant
 210                Empfangsschalter                   lino_welfare.modlib.welfare.user_types.ReceptionClerk
 220                Empfangsschalter (+Erstempfang)    lino_welfare.modlib.welfare.user_types.ReceptionClerkNewcomers
 300                Schuldenberater                    lino_welfare.modlib.debts.roles.DebtsUser
 400                Sozi                               lino_welfare.modlib.pcsw.roles.SocialAgent
 410                Sozi (Manager)                     lino_welfare.modlib.pcsw.roles.SocialStaff
 500                Buchhalter                         lino_welfare.modlib.welfare.user_types.LedgerUser
 510                Accountant (Manager)               lino_welfare.modlib.welfare.user_types.AccountantManager
 800                Supervisor                         lino_welfare.modlib.welfare.user_types.Supervisor
 900    admin       Verwalter                          lino_welfare.modlib.welfare.user_types.SiteAdmin
 910                Security advisor                   lino_welfare.modlib.welfare.user_types.SecurityAdvisor
====== =========== ================================== ==================================================================
<BLANKLINE>


The user types are only the tip of the iceberg.  A user type is an
arbitrary choice of user roles made available for a given application.
Lino defines a lot of user roles.  For example, the following diagram
visualizes the genealogy of a reception clerk:

.. inheritance-diagram:: lino_welfare.modlib.welfare.user_types.ReceptionClerk


**Remarks:**

An integration agent (manager) has some staff permissions but is not a
:class:`lino.core.roles.SiteStaff`:

>>> from lino.core.roles import SiteStaff
>>> from lino_xl.lib.contacts.roles import ContactsStaff

>>> p110 = users.UserTypes.get_by_value('110')
>>> p110.has_required_roles([SiteStaff])
False

A reception clerk is a
:class:`lino_xl.lib.contacts.roles.ContactsStaff`:

>>> p210 = users.UserTypes.get_by_value('210')
>>> p210.has_required_roles([SiteStaff])
False
>>> p210.has_required_roles([ContactsStaff])
True



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


