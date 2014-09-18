# Copyright 2014 Luc Saffre
# License: BSD (see file COPYING for details)

"""
Lino-Welfare extension of :mod:`lino_welfare.modlib.pcsw`
"""

from lino_welfare.modlib.pcsw import Plugin


class Plugin(Plugin):
    extends_models = ['Client']
