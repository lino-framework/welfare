# -*- coding: UTF-8 -*-
# Copyright 2015 Luc Saffre
# License: BSD (see file COPYING for details)
"""Choicelists for `lino_welfare.modlib.newcomers`.

"""

from lino_welfare.modlib.pcsw.roles import SocialAgent
from lino.modlib.reception.roles import ReceptionUser


class NewcomersAgent(SocialAgent, ReceptionUser):
    pass

