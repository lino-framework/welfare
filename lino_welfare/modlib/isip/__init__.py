# -*- coding: UTF-8 -*-
# Copyright 2012-2015 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

"""See :doc:`/specs/isip`.

"""

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from lino.api import ad


class Plugin(ad.Plugin):
    "See :class:`lino.core.plugin.Plugin`."
    verbose_name = _("ISIP")
    needs_plugins = ['lino_welfare.modlib.integ']
