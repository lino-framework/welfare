# Copyright 2013-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""
Lino Welfare extension of :mod:`lino.modlib.cal`

.. autosummary::
   :toctree:

    models
    fixtures.std
    fixtures.demo
    fixtures.demo2



"""

from lino.modlib.cal import Plugin


class Plugin(Plugin):
    """See :class:`lino.core.plugin.Plugin`."""

    extends_models = ['Event', 'EventType', 'Guest', 'Task']
