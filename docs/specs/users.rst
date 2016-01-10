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
:mod:`lino.modlib.users` plugin.

.. contents::
   :depth: 2

User profiles
=============

The default set of user profiles for Lino Welfare is defined in
:mod:`lino_welfare.modlib.welfare.roles` and leads to the following
list of profiles:

>>> rt.show(users.UserProfiles)
======= =========== ===============================
 value   name        text
------- ----------- -------------------------------
 000     anonymous   Anonymous
 100                 Integration agent
 110                 Integration agent (Manager)
 120                 Integration agent (Newcomers)
 200                 Newcomers consultant
 210                 Reception clerk
 220                 Newcomers reception clerk
 300                 Debts consultant
 400                 Social agent
 410                 Social agent (Manager)
 500                 Accountant
 510                 Accountant (Manager)
 800                 Supervisor
 900     admin       Administrator
======= =========== ===============================
<BLANKLINE>



Note that local administrators may define their own module, similar to
this, and have :attr:`lino.core.site.Site.user_profiles_module` point
to it.

The user profiles are only the tip of the iceberg.  A user profile is
an arbitrary choice of user roles made available for a given
application.  Lino defines a lot of user roles.  For example, the
following diagram visualizes the genealogy of a reception clerk:

.. inheritance-diagram:: lino_welfare.modlib.welfare.roles.ReceptionClerk


**Remarks:**

An integration agent (manager) has some staff permissions but is not a
:class:`lino.core.roles.SiteStaff`:

>>> from lino.core.roles import SiteStaff
>>> from lino.modlib.contacts.roles import ContactsStaff

>>> p110 = users.UserProfiles.get_by_value('110')
>>> p110.has_required_roles([SiteStaff])
False

A reception clerk is a
:class:`lino.modlib.contacts.roles.ContactsStaff`:

>>> p210 = users.UserProfiles.get_by_value('210')
>>> p210.has_required_roles([SiteStaff])
False
>>> p210.has_required_roles([ContactsStaff])
True




Authorities
===========

Alicia, Hubert and Mélanie give "authority" to Theresia to do their
work when they are absent.

>>> rt.show(users.Authorities)
==== ================= =================
 ID   Author            User
---- ----------------- -----------------
 1    Hubert Huppertz   Theresia Thelen
 2    Alicia Allmanns   Theresia Thelen
 3    Mélanie Mélard    Theresia Thelen
==== ================= =================
<BLANKLINE>


