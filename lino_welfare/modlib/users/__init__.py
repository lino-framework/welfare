# Copyright 2014 Luc Saffre
# License: BSD (see file COPYING for details)

"""
Lino-Welfare extension of :mod:`lino.modlib.users`
"""

from lino.modlib.users import Plugin


class Plugin(Plugin):
    
    extends_models = ['User']

