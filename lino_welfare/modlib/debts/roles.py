# -*- coding: UTF-8 -*-
# Copyright 2015-2018 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

from lino.core.roles import UserRole


class DebtsUser(UserRole):
    """Can act as a depts mediator."""
    pass


class DebtsStaff(DebtsUser):
    """Can configure debts mediation functionality."""
    pass


