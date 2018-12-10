# -*- coding: UTF-8 -*-
# Copyright 2015-2017 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

"""

.. autosummary::
   :toctree:

   models
   user_types
   workflows
   fixtures.std
   fixtures.demo
   fixtures.demo2

"""

from lino.api.ad import Plugin, _


class Plugin(Plugin):

    ui_label = _("Lino Welfare")

    # url_prefix = 'lino'

    # media_name = 'lino'
