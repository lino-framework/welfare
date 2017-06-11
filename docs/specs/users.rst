.. _welfare.specs.users:

=============
Users
=============

.. How to test only this document:

    $ python setup.py test -s tests.SpecsTests.test_users
    
    doctest init:

    >>> from __future__ import print_function
    >>> import os
    >>> os.environ['DJANGO_SETTINGS_MODULE'] = \
    ...    'lino_welfare.projects.std.settings.doctests'
    >>> from lino.api.doctest import *

This document describes how Lino Welfare uses the
:mod:`lino.modlib.auth` plugin.

.. contents::
   :depth: 2

User types
=============

The default set of user types for Lino Welfare is defined in
:mod:`lino_welfare.modlib.welfare.user_types` and leads to the
following list of profiles:

>>> rt.show(auth.UserTypes)
======= =========== =============================== ==================================================================
 value   name        text                            User role
------- ----------- ------------------------------- ------------------------------------------------------------------
 000     anonymous   Anonymous                       lino.core.roles.UserRole
 100                 Integration agent               lino_welfare.modlib.integ.roles.IntegrationAgent
 110                 Integration agent (Manager)     lino_welfare.modlib.integ.roles.IntegrationStaff
 120                 Integration agent (Newcomers)   lino_welfare.modlib.welfare.user_types.IntegrationAgentNewcomers
 200                 Newcomers consultant            lino_welfare.modlib.welfare.user_types.NewcomersConsultant
 210                 Reception clerk                 lino_welfare.modlib.welfare.user_types.ReceptionClerk
 220                 Newcomers reception clerk       lino_welfare.modlib.welfare.user_types.ReceptionClerkNewcomers
 300                 Debts consultant                lino_welfare.modlib.debts.roles.DebtsUser
 400                 Social agent                    lino_welfare.modlib.pcsw.roles.SocialAgent
 410                 Social agent (Manager)          lino_welfare.modlib.pcsw.roles.SocialStaff
 500                 Accountant                      lino_welfare.modlib.welfare.user_types.LedgerUser
 510                 Accountant (Manager)            lino_welfare.modlib.welfare.user_types.AccountantManager
 800                 Supervisor                      lino_welfare.modlib.welfare.user_types.Supervisor
 900     admin       Administrator                   lino_welfare.modlib.welfare.user_types.SiteAdmin
 910                 Security advisor                lino_welfare.modlib.welfare.user_types.SecurityAdvisor
======= =========== =============================== ==================================================================
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

>>> p110 = auth.UserTypes.get_by_value('110')
>>> p110.has_required_roles([SiteStaff])
False

A reception clerk is a
:class:`lino_xl.lib.contacts.roles.ContactsStaff`:

>>> p210 = auth.UserTypes.get_by_value('210')
>>> p210.has_required_roles([SiteStaff])
False
>>> p210.has_required_roles([ContactsStaff])
True



Authorities
===========

Alicia, Hubert and Mélanie give "authority" to Theresia to do their
work when they are absent.

>>> rt.show(rt.actors.users.Authorities)
==== ================= =================
 ID   Author            User
---- ----------------- -----------------
 1    Hubert Huppertz   Theresia Thelen
 2    Alicia Allmanns   Theresia Thelen
 3    Mélanie Mélard    Theresia Thelen
==== ================= =================
<BLANKLINE>


