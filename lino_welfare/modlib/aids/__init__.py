# Copyright 2014 Luc Saffre
# License: BSD (see file COPYING for details)


"""
See :mod:`welfare.aids`
"""

from lino import ad
from django.utils.translation import ugettext_lazy as _


class Plugin(ad.Plugin):

    verbose_name = _("Aids")
