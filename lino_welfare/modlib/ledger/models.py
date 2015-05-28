# -*- coding: UTF-8 -*-
# Copyright 2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""
Database models for :mod:`lino_welfare.modlib.ledger`.
"""

from __future__ import unicode_literals

from lino.modlib.ledger.models import *

from .mixins import PaymentRecipient


class Movement(Movement, PaymentRecipient):
    pass


class AccountInvoice(AccountInvoice, PaymentRecipient):
    pass
