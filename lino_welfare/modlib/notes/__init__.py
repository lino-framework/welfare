# -*- coding: UTF-8 -*-
# Copyright 2013-2015 Rumma & Ko Ltd

"""
Lino Welfare extension of :mod:`lino_xl.lib.notes`

.. autosummary::
   :toctree:

    fixtures.std
    fixtures.demo

"""

from lino_xl.lib.notes import Plugin


class Plugin(Plugin):

    extends_models = ['Note']
