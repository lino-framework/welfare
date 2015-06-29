# -*- coding: UTF-8 -*-
# Copyright 2015 Luc Saffre
# License: BSD (see file COPYING for details)
"""User roles for `lino_welfare.modlib.integ`.

"""

from lino_welfare.modlib.newcomers.roles import NewcomersAgent


class DebtsUser(NewcomersAgent):
    pass


class DebtsStaff(DebtsUser):
    pass


