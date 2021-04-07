# -*- coding: UTF-8 -*-
# Copyright 2015-2018 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
"""

"""

from lino.core.roles import UserRole


class CoursesUser(UserRole):
    """Can manage external courses."""
    pass


class CoursesStaff(CoursesUser):
    """Can manage and configure external courses."""
    pass
