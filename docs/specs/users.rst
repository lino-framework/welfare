.. _welfare.tested.users:

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

A technical tour into the :mod:`lino.modlib.users` plugin.

.. contents::
   :depth: 2

User profiles
=============

This is the list of user profiles:

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
 900     admin       Administrator
======= =========== ===============================
<BLANKLINE>


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
