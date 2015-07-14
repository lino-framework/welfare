# -*- coding: UTF-8 -*-
# Copyright 2015 Luc Saffre
# License: BSD (see file COPYING for details)

from lino.core.roles import SiteUser


class AidsUser(SiteUser):
    """A user who can issue aids grantings and confirmations."""
    pass


class AidsStaff(AidsUser):
    """A user who can manage aids grantings and confirmations."""
    pass

