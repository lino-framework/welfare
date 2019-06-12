# Copyright 2014-2016 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

"""
Lino-Welfare extension of :mod:`lino.modlib.users`.

.. autosummary::
   :toctree:

    fixtures.demo
    fixtures.demo2

"""

from lino.modlib.users import Plugin


class Plugin(Plugin):
    
    extends_models = ['User']

