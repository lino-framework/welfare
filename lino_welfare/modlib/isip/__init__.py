# -*- coding: UTF-8 -*-
# Copyright 2012-2013 Luc Saffre
# License: BSD (see file COPYING for details)

"""
See :ddref:`isip`.
"""

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from lino import ad


class Plugin(ad.Plugin):
    verbose_name = _("ISIP")
