# -*- coding: UTF-8 -*-
# Copyright 2013-2015 Luc Saffre
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
Database models for :mod:`lino_welfare.modlib.cal`.
"""

from __future__ import unicode_literals

import datetime

from django.utils.translation import ugettext_lazy as _
from django.utils.translation import pgettext_lazy
from django.contrib.humanize.templatetags.humanize import naturalday

from django.db.models import Q

from lino.api import dd, rt

from lino.utils.xmlgen.html import E

from lino.modlib.finan.models import *

from lino_welfare.modlib.ledger.mixins import PaymentRecipient


class BankStatementItem(BankStatementItem, PaymentRecipient):
    pass
