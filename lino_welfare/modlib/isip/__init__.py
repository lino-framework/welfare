# -*- coding: UTF-8 -*-
# Copyright 2012-2015 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

"""See :doc:`/specs/isip`.

"""

from __future__ import unicode_literals

from django.utils.translation import gettext_lazy as _

from lino.api import ad


class Plugin(ad.Plugin):
    "See :class:`lino.core.plugin.Plugin`."
    verbose_name = _("ISIP")
    needs_plugins = ['lino_welfare.modlib.integ']
