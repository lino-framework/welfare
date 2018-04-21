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
:mod:`lino_welfare.modlib.welfare.user_types`.  You can define your
own local :attr:`user_types_module
<lino.core.site.Site.user_types_module>` but we recommend using the
standard set of user types.  See :doc:`usertypes`.

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


Demo users
==========

>>> rt.show('users.Users', language="en")
========== =================================== ============ ===========
 Username   User type                           First name   Last name
---------- ----------------------------------- ------------ -----------
 alicia     100 (Integration agent)             Alicia       Allmanns
 caroline   200 (Newcomers consultant)          Caroline     Carnol
 hubert     100 (Integration agent)             Hubert       Huppertz
 judith     400 (Social agent)                  Judith       Jousten
 kerstin    300 (Debts consultant)              Kerstin      Kerres
 melanie    110 (Integration agent (Manager))   Mélanie      Mélard
 nicolas
 patrick    910 (Security advisor)              Patrick      Paraneau
 robin      900 (Administrator)                 Robin        Rood
 rolf       900 (Administrator)                 Rolf         Rompen
 romain     900 (Administrator)                 Romain       Raffault
 theresia   210 (Reception clerk)               Theresia     Thelen
 wilfried   500 (Accountant)                    Wilfried     Willems
========== =================================== ============ ===========
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


