# -*- coding: UTF-8 -*-
# Copyright 2008-2014 Luc Saffre
# This file is part of the Lino project.
# Lino is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
# Lino is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with Lino; if not, see <http://www.gnu.org/licenses/>.


from lino import dd


def objects():

    for et in dd.modules.excerpts.ExcerptType.objects.all():
        model = et.content_type.model_class()
        ses = dd.login('melanie')  # user=AGENTS.pop())
        ses.selected_rows = [model.objects.all()[0]]
        yield et.get_or_create_excerpt(ses)

