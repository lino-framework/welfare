# -*- coding: UTF-8 -*-
# Copyright 2015 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

"""
Database models for the :mod:`lino_welfare.modlib.sepa`.
"""

from __future__ import unicode_literals

from django.utils.translation import gettext_lazy as _

from lino_xl.lib.sepa.models import *


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
    """A bank account of a partner.

    .. attribute:: account_type

    .. attribute:: managed

        Whether this account is being managed by the PCSW.

        This attribute may be deprecated since managed accounts
        usually also have imported :attr:`statements
        <lino_xl.lib.b2c.models.Account.statements>`.

    """

    account_type = AccountTypes.field(
        default=AccountTypes.as_callable('giro'))
    managed = models.BooleanField(
        _("Managed"), default=False,
        help_text=_("Whether this account is being managed by the PCSW."))


class AccountsByClient(AccountsByPartner):
    """Shows the accounts for a given client. This includes additional
    information :attr:`managed <Account.managed>`,
    :attr:`account_type <Account.account_type>` and
    :attr:`statements <lino_xl.lib.b2c.models.Account.statements>`.

    """
    column_names = 'account_type iban bic primary managed statements'

