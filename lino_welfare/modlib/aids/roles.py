# -*- coding: UTF-8 -*-
# Copyright 2015-2018 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from lino.core.roles import UserRole


class AidsUser(UserRole):
    """Can issue aids grantings and confirmations."""
    pass


class AidsStaff(AidsUser):
    """Can configure the aids grantings functionality."""
    pass

