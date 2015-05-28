# Copyright 2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""
Lino Welfare extension of :mod:`lino.modlib.finan`

.. autosummary::
   :toctree:

    models



"""

from lino.modlib.finan import Plugin


class Plugin(Plugin):
    """See :class:`lino.core.plugin.Plugin`."""

    extends_models = ['BankStatementItem']
