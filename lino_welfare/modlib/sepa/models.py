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

"""
Database models for the :mod:`lino_welfare.modlib.sepa`.
"""

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from lino.modlib.sepa.models import *


class AccountTypes(dd.ChoiceList):
    verbose_name = _("Account type")
    verbose_name_plural = _("Account types")
add = AccountTypes.add_item

add("01", _("Giro"), 'giro')
add("02", _("Savings"), 'savings')
add("03", _("Deposits"), 'deposits')
add("04", _("Other"), 'other')
# Tagesgeldkonto?


class Account(Account):

    account_type = AccountTypes.field(default=AccountTypes.giro)
    managed = models.BooleanField(
        _("Managed"), default=False,
        help_text=_("Whether this account is being managed by the PCSW."))


class AccountsByClient(AccountsByPartner):
    column_names = 'account_type managed iban bic primary'
