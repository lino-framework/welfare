# -*- coding: UTF-8 -*-
# Copyright 2015-2018 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)


from lino.core.roles import UserRole


class NewcomersOperator(UserRole):
    """Can do certain limited actions with newcomers."""
    pass

class NewcomersUser(NewcomersOperator):
    """
    An agent specialized in assigning new clients to other agents.
    """
    pass

