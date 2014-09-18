# -*- coding: UTF-8 -*-
# Copyright 2014 Luc Saffre
# License: BSD (see file COPYING for details)

"""
The :xfile:`models.py` module for the :mod:`lino_welfare.modlib.cal` app.
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
