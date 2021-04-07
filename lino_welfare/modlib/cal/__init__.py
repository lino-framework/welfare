# Copyright 2013-2016 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

"""
Lino Welfare extension of :mod:`lino_xl.lib.cal`

.. autosummary::
   :toctree:

    fixtures.std
    fixtures.demo
    fixtures.demo2


"""

from lino_xl.lib.cal import Plugin


class Plugin(Plugin):
    """See :class:`lino.core.plugin.Plugin`."""

    extends_models = ['Event', 'EventType', 'Guest', 'Task']

    partner_model = 'contacts.Partner'
