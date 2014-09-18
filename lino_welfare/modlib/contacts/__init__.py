# Copyright 2013-2014 Luc Saffre
# License: BSD (see file COPYING for details)

"""
Lino-Welfare extension of :mod:`lino.modlib.contacts`
"""

from lino.modlib.contacts import Plugin


class Plugin(Plugin):

    extends_models = ['Partner', 'Person', 'Company']
