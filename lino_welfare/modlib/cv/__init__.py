# -*- coding: UTF-8 -*-
# Copyright 2012-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""This is an early implementation still used in
:mod:`lino_welfare.projects.eupen`.  But it uses
:mod:`lino.modlib.properties` which is deprecated.
New installations should use
:mod:`lino_welfare.projects.chatelet.modlib.cv` instead.

"""

from lino.modlib.cv import Plugin

from lino.api import _
try:

    from lino.core.permissions import UserRole

except ImportError:  # branch master

    class UserRole(object):
        pass


class IntegrationAgent(UserRole):
    verbose_name = _("Integration agent")


class Plugin(Plugin):

    ## settings
    person_model = 'pcsw.Client'

    # classic permission system (until June 2015)
    def get_default_required(self, **kwargs):
        return super(Plugin, self).get_default_required(**kwargs)

    # coming permission system before 201506
    def get_default_required_roles(self, *args):
        return super(Plugin, self).get_default_required_roles(
            IntegrationAgent, *args)
