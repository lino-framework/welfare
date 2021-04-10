.. doctest docs/specs/users.rst
.. _welfare.specs.users:

=============
Users
=============

..  doctest init:

    >>> from lino import startup
    >>> startup('lino_welfare.projects.gerd.settings.doctests')
    >>> from lino.api.doctest import *

This document describes how Lino Welfare uses the
:mod:`lino.modlib.users` plugin.

.. contents::
   :depth: 2

User types
=============

See :doc:`topics/usertypes`.

Demo users
==========

>>> rt.show('users.AllUsers', language="en")
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

>>> rt.show(rt.models.users.Authorities, language="en")
==== ================= =================
 ID   Author            User
---- ----------------- -----------------
 1    Hubert Huppertz   Theresia Thelen
 2    Alicia Allmanns   Theresia Thelen
 3    Mélanie Mélard    Theresia Thelen
==== ================= =================
<BLANKLINE>
