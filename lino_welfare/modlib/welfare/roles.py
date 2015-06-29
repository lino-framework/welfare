# -*- coding: UTF-8 -*-
# Copyright 2009-2015 Luc Saffre
# License: BSD (see file COPYING for details)

# Note that some roles are not needed *here*, but may be needed by
# code which imports * from here.

from lino.core.roles import Anonymous  

from lino.core.roles import SiteAdmin
from lino.modlib.office.roles import OfficeStaff
from lino.modlib.reception.roles import ReceptionUser
from lino.modlib.reception.roles import ReceptionOperator
from lino_welfare.modlib.pcsw.roles import SocialAgent
from lino_welfare.modlib.pcsw.roles import SocialStaff
from lino_welfare.modlib.integ.roles import IntegrationAgent
from lino_welfare.modlib.integ.roles import IntegrationStaff
from lino_welfare.modlib.debts.roles import DebtsUser, DebtsStaff
from lino_welfare.modlib.newcomers.roles import NewcomersAgent


class SiteAdmin(
        IntegrationStaff,
        DebtsStaff,
        NewcomersAgent,
        ReceptionOperator,
        SiteAdmin):
    pass

