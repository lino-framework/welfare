# -*- coding: UTF-8 -*-
# Copyright 2015-2019 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

"""

.. autosummary::
   :toctree:

   user_types

TODO: write prosa docs for the following modules:

   workflows
   models
   fixtures.std
   fixtures.demo
   fixtures.demo2

"""

from lino.api.ad import Plugin, _


class Plugin(Plugin):

    ui_label = _("Lino Welfare")

    # url_prefix = 'lino'

    # media_name = 'lino'
