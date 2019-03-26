# -*- coding: UTF-8 -*-
# Copyright 2013-2019 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

"""Adds functionality for managing job supply projects.

Technical specs see :ref:`weleup`.

.. autosummary::
   :toctree:

   fixtures.std

"""

from __future__ import unicode_literals

from lino import ad

from django.utils.translation import ugettext_lazy as _


class Plugin(ad.Plugin):
    "See :class:`lino.core.plugin.Plugin`."
    # verbose_name = _("Art.60§7")
    verbose_name = _("Job supplying")  # Mise à l'emploi
    needs_plugins = ['lino_welfare.modlib.isip']

