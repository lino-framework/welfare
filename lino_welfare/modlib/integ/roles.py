# -*- coding: UTF-8 -*-
# Copyright 2015-2021 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)


from lino.core.roles import UserRole

class IntegUser(UserRole):
    """Has access to data used by integration agents."""
    pass


class IntegrationStaff(IntegUser):
    """Can configure social integration functionality."""
    pass
