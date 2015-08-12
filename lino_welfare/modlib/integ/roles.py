# -*- coding: UTF-8 -*-
# Copyright 2015 Luc Saffre
# License: BSD (see file COPYING for details)
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
