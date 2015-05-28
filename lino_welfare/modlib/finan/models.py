# -*- coding: UTF-8 -*-
# Copyright 2013-2015 Luc Saffre
# License: BSD (see file COPYING for details)

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
