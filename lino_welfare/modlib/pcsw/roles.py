# -*- coding: UTF-8 -*-
# Copyright 2015-2018 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from lino.core.roles import UserRole


class SocialCoordinator(UserRole):
    """
    Has limited access to data of social workers. Can see contracts.
    """
    pass

class SocialUser(UserRole):
    """Can access data managed by general social workers."""
    pass

class SocialStaff(SocialUser):
    """Can configure general social work functionality."""
    pass

