# -*- coding: UTF-8 -*-
# Copyright 2015-2018 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)


from lino.core.roles import UserRole


class NewcomersOperator(UserRole):
    """Can do certain limited actions with newcomers."""
    pass

class NewcomersUser(NewcomersOperator):
    """
    An agent specialized in assigning new clients to other agents.
    """
    pass

