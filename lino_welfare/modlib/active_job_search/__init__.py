# -*- coding: UTF-8 -*-
# Copyright 2013-2014 Luc Saffre
# License: BSD (see file COPYING for details)

"""Recherche active d'emploi.

.. autosummary::
   :toctree:

    fixtures.demo
    models


"""

from lino import ad

from django.utils.translation import ugettext_lazy as _


class Plugin(ad.Plugin):
    verbose_name = _("Active Job Search")
