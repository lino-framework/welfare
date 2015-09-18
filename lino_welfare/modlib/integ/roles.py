# -*- coding: UTF-8 -*-
# Copyright 2015 Luc Saffre
# This file is part of Lino Welfare.
#
# Lino Welfare is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# Lino Welfare is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License along with Lino Welfare.  If not, see
# <http://www.gnu.org/licenses/>.
"""User roles for `lino_welfare.modlib.integ`.

"""

from lino_welfare.modlib.pcsw.roles import SocialAgent, SocialStaff
from lino.modlib.cv.roles import CareerUser, CareerStaff
from lino_welfare.modlib.courses.roles import CoursesUser, CoursesStaff
from lino_welfare.modlib.newcomers.roles import NewcomersOperator
from lino.modlib.courses.roles import CoursesUser as CoursesUser2


class IntegrationAgent(SocialAgent, CareerUser, CoursesUser, CoursesUser2):
    """A *social agent* who can see database content specific to
    integration work: CV, language courses, workshops, ...

    See also :class:`lino_welfare.modlib.pcsw.choicelists.SocialAgent`.

    """


class IntegrationStaff(IntegrationAgent, SocialStaff, CareerStaff,
                       CoursesStaff, NewcomersOperator):
    pass
