# -*- coding: UTF-8 -*-
# Copyright 2015-2018 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

# from lino_xl.lib.contacts.roles import ContactsUser
from lino.core.roles import UserRole

class CBSSUser(UserRole):
    """Can perform CBSS requests."""
    pass


class SecurityAdvisor(CBSSUser):
    """Can consult CBSS requests of other users."""
    pass
