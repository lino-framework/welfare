# -*- coding: UTF-8 -*-
# Copyright 2014 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

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
