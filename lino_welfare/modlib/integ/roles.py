# -*- coding: UTF-8 -*-
# Copyright 2015-2018 Rumma & Ko Ltd
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

from lino_xl.lib.cv.roles import CareerUser, CareerStaff
from lino_xl.lib.notes.roles import NotesUser
from lino_welfare.modlib.pcsw.roles import SocialAgent, SocialStaff
from lino_welfare.modlib.xcourses.roles import CoursesUser, CoursesStaff
from lino_welfare.modlib.newcomers.roles import NewcomersOperator

class IntegrationAgent(SocialAgent, CareerUser, CoursesUser, NotesUser):
    """
    An **integration agent** is a *social agent* who can see database
    content specific to integration work: CV, language courses,
    workshops, ...

    See also :class:`lino_welfare.modlib.pcsw.choicelists.SocialAgent`.
    """


class IntegrationStaff(IntegrationAgent, SocialStaff, CareerStaff,
                       CoursesStaff, NewcomersOperator):
    pass
