# -*- coding: UTF-8 -*-
# Copyright 2012-2015 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
"""Database models for `lino_welfare.modlib.client_vouchers`.

See also :ref:`welfare.specs.ledger`.

"""

import logging
logger = logging.getLogger(__name__)

from decimal import Decimal

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import format_lazy


from lino.api import dd

from lino_xl.lib.ledger.mixins import (
    PartnerRelated, ProjectRelated, AccountVoucherItem, Matching)
from lino_xl.lib.ledger.models import Voucher, VoucherStates

from lino_xl.lib.ledger.roles import LedgerUser


class ClientVoucher(Voucher, ProjectRelated):

    class Meta:
        app_label = 'client_vouchers'
        verbose_name = _("Client voucher")
        verbose_name_plural = _("Client vouchers")

    state = VoucherStates.field(default='draft')
    amount = dd.PriceField(_("Amount"), blank=True, null=True)

    def compute_totals(self):
        if self.pk is None:
            return
        base = Decimal()
        for i in self.items.all():
            if i.amount is not None:
                base += i.amount
        self.amount = base

    def get_vat_sums(self):
        sums_dict = dict()

        def book(account, amount):
            if account in sums_dict:
                sums_dict[account] += amount
            else:
                sums_dict[account] = amount
        tt = self.get_trade_type()
        for i in self.items.order_by('seqno'):
            if i.amount:
                b = i.get_base_account(tt)
                if b is None:
                    raise Exception(
                        "No base account for %s (amount is %r)" % (
                            i, i.amount))
                book(b, i.amount)
        return sums_dict

    def get_wanted_movements(self):
        sums_dict = self.get_vat_sums()
        #~ logger.info("20120901 get_wanted_movements %s",sums_dict)
        sum = Decimal()
        for acc, m in sums_dict.items():
            if m:
                yield self.create_movement(
                    None, acc, not self.journal.dc, m)
                sum += m

        acc = self.get_trade_type().get_main_account()
        if acc is not None:
            yield self.create_movement(
                None, acc, self.journal.dc, sum,
                partner=self.partner,
                project=self.project,
                match=self.match)

    def full_clean(self, *args, **kw):
        self.compute_totals()
        super(ClientVoucher, self).full_clean(*args, **kw)

    def before_state_change(self, ar, old, new):
        if new.name == 'registered':
            self.compute_totals()
        elif new.name == 'draft':
            pass
        super(ClientVoucher, self).before_state_change(ar, old, new)


class VoucherItem(Matching, PartnerRelated, AccountVoucherItem):
    """An item of an :class:`ClientVoucher`."""

    class Meta:
        app_label = 'client_vouchers'
        verbose_name = _("Client voucher item")
        verbose_name_plural = _("Client voucher items")

    voucher = dd.ForeignKey(
        'client_vouchers.ClientVoucher', related_name='items')
    amount = dd.PriceField(_("Amount"), blank=True, null=True)

    @dd.chooser()
    def match_choices(cls, voucher, partner):
        return cls.get_match_choices(voucher.journal, partner)


from .ui import *
