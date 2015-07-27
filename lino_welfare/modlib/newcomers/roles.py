# -*- coding: UTF-8 -*-
# Copyright 2015 Luc Saffre
# License: BSD (see file COPYING for details)
"""Choicelists for `lino_welfare.modlib.newcomers`.




"""

from lino.modlib.beid.roles import BeIdUser
from lino.modlib.contacts.roles import ContactsUser
from lino_welfare.modlib.pcsw.roles import SocialAgent


class NewcomersAgent(SocialAgent):
    """A **newcomers agent** is a *social agent* who also manages
    newcomers.

    """
    pass


class NewcomersOperator(ContactsUser, BeIdUser):
    """A **newcomers operator** is a user who is not *social agent* but
    can e.g. register newcomers and assign them a coach.

    """
    pass

