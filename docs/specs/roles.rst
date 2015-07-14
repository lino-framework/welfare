.. _welfare.specs.roles:
==========================
User profiles Lino Welfare
==========================

.. How to test only this document:

    $ python setup.py test -s tests.SpecsTests.test_roles
    
    doctest init:

    >>> from __future__ import print_function
    >>> import os
    >>> os.environ['DJANGO_SETTINGS_MODULE'] = \
    ...    'lino_welfare.projects.std.settings.doctests'
    >>> from lino.utils.xmlgen.html import E
    >>> from lino.api.doctest import *
    >>> from lino.api import rt
    >>> from lino_welfare.projects.std.roles import *

This document describes the default user profiles used by Lino Welfare.

.. contents::
   :depth: 1
   :local:


First section
=============

A reception clerk is not an integration agent:

>>> isinstance(ReceptionClerk, IntegrationAgent)
False

