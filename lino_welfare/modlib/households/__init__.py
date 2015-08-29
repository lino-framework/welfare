# Copyright 2012-2014 Luc Saffre
# License: BSD (see file COPYING for details)

import datetime

from lino.modlib.households import Plugin


class Plugin(Plugin):

    extends_models = ['Household', 'Member']
    adult_age = datetime.timedelta(days=18*365)
