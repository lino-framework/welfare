# -*- coding: UTF-8 -*-
# Copyright 2012-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""The :mod:`lino_welfare.modlib.isip` package provides data definitions
for Individual Social Integration Projects (ISIPs)

This module is also used and extended by
:mod:`lino_welfare.modlib.jobs` and
:mod:`lino_welfare.modlib.immersion`.

.. autosummary::
   :toctree:

   models
   mixins
   choicelists

"""

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from lino.api import ad


class Plugin(ad.Plugin):
    "See :class:`lino.core.plugin.Plugin`."
    verbose_name = _("ISIP")
    needs_plugins = ['lino_welfare.modlib.integ']
