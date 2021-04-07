# Copyright 2012-2019 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

"""
Extends :mod:`lino_xl.lib.households.models`.

See :doc:`/specs/households`.

"""

from lino_xl.lib.households import Plugin


class Plugin(Plugin):

    extends_models = ['Household']
