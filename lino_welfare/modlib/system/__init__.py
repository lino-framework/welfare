# Copyright 2013-2014 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

from lino.modlib.system import Plugin


class Plugin(Plugin):

    extends_models = ['SiteConfig']
