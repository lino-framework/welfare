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

from __future__ import unicode_literals

from lino.api import dd, rt, _


def objects():

    ExcerptType = rt.modules.excerpts.ExcerptType
    Enrolment = rt.modules.courses.Enrolment
    # ContentType = rt.modules.contenttypes.ContentType
    kw = dict(
        # template='Default.odt',
        body_template='enrolment.body.html',
        print_recipient=False, certifying=True)
    kw.update(dd.str2kw('name', _("Enrolment")))
    yield ExcerptType.update_for_model(Enrolment, **kw)

    # kw = dict(
    #     body_template='intervention.body.html',
    #     print_recipient=False, certifying=True)
    # kw.update(dd.str2kw('name', _("Intervention request")))
    # kw.update(content_type=ContentType.objects.get_for_model(Enrolment))
    # yield ExcerptType(**kw)

