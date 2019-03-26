# Copyright 2013-2019 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

"""
Lino-Welfare extension of :mod:`lino_xl.lib.sepa`

.. autosummary::
   :toctree:



"""

from lino_xl.lib.sepa import Plugin


class Plugin(Plugin):
    
    extends_models = ['Account']
