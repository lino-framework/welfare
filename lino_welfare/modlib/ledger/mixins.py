# -*- coding: UTF-8 -*-
# Copyright 2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""
Model mixins for :mod:`lino_welfare.modlib.ledger`.
"""

from __future__ import unicode_literals


from lino.api import dd, _


class PaymentRecipient(dd.Model):
    class Meta:
        abstract = True

    recipient = dd.ForeignKey(
        'contacts.Partner', blank=True, null=True,
        verbose_name=_("Payment recipient"))

