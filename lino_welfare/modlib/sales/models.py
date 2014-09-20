# -*- coding: UTF-8 -*-
# Copyright 2014 Luc Saffre
# License: BSD (see file COPYING for details)

"""
Dummy module to satisfy `lino.modlib.courses` dependency
on a ``sales`` app.
"""

from __future__ import unicode_literals
from __future__ import print_function

from lino import dd, rt


class CreateInvoice(dd.Dummy):
    pass


class Invoiceable(dd.Dummy):
    pass


class InvoicingsByInvoiceable(dd.Dummy):
    pass
