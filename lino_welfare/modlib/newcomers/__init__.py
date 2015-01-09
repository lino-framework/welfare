# -*- coding: UTF-8 -*-
# Copyright 2013-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""The :mod:`lino_welfare.modlib.newcomers` package provides data
definitions for managing "newcomers".

.. autosummary::
   :toctree:

   models
   fixtures

"""

from django.utils.translation import ugettext_lazy as _

from lino import ad


class Plugin(ad.Plugin):
    verbose_name = _("Newcomers")
