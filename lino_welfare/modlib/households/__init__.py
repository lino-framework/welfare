# Copyright 2012-2014 Luc Saffre
# License: BSD (see file COPYING for details)

from lino.modlib.households import Plugin


class Plugin(Plugin):

    extends_models = ['Household', 'Member']
