# Copyright 2014 Luc Saffre
# License: BSD (see file COPYING for details)

"""
The Chatelet extension of :mod:`lino.modlib.courses`
"""

from lino.modlib.courses import Plugin
from django.utils.translation import ugettext_lazy as _


class Plugin(Plugin):
    extends_models = ['Course', 'Line']
    verbose_name = _("Workshops")
    pupil_model = 'pcsw.Client'
