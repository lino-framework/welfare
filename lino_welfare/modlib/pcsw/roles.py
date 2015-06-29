# -*- coding: UTF-8 -*-
# Copyright 2015 Luc Saffre
# License: BSD (see file COPYING for details)

from lino_welfare.modlib.cbss.roles import CBSSUser
from lino.modlib.office.roles import OfficeStaff
from lino.modlib.beid.roles import BeIdUser
from lino.modlib.reception.roles import ReceptionUser
from lino_welfare.modlib.aids.roles import AidsStaff


class SocialAgent(ReceptionUser, CBSSUser, BeIdUser):
    """A **social agent** is a user who does individual coaching of
    clients.  Certain privacy-relevant client data is visible only
    to social agents.

    """


class SocialStaff(SocialAgent, OfficeStaff, AidsStaff):
    """A **social staff member** is a social agent who has access to more
    technical information about welfare clients.  For example the
    `Miscellaneous` panel.

    """
