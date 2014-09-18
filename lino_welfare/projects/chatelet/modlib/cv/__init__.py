# Copyright 2014 Luc Saffre
# License: BSD (see file COPYING for details)

"""
Chatelet version of :mod:`welfare.ml.cv`
"""

from lino import ad

from django.utils.translation import ugettext_lazy as _


class Plugin(ad.Plugin):
    verbose_name = _("Career")

    ## settings
    person_model = 'pcsw.Client'
