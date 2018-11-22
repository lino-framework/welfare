# -*- coding: UTF-8 -*-
# Copyright 2014 Rumma & Ko Ltd
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

"""
Dummy module to satisfy `lino_xl.lib.courses` dependency
on a ``sales`` app.
"""

from __future__ import unicode_literals
from __future__ import print_function

from lino.api import dd, rt


class CreateInvoice(dd.Dummy):
    pass


class InvoiceGenerator(dd.Dummy):
    pass


class InvoicingsByGenerator(dd.Dummy):
    pass
