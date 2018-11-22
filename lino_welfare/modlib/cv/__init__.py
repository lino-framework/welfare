# -*- coding: UTF-8 -*-
# Copyright 2012-2015 Rumma & Ko Ltd
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

"""This is an early implementation still used in
:mod:`lino_welfare.projects.eupen`.  But it uses
:mod:`lino_xl.lib.properties` which is deprecated.
New installations should use
:mod:`lino_welfare.chatelet.lib.cv` instead.

"""

from lino_xl.lib.cv import Plugin


class Plugin(Plugin):

    ## settings
    person_model = 'pcsw.Client'

