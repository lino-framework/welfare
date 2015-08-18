# -*- coding: UTF-8 -*-
# Copyright 2013-2015 Luc Saffre

"""
Lino Welfare extension of :mod:`lino.modlib.notes`

.. autosummary::
   :toctree:

    models
    fixtures.std
    fixtures.demo

"""

from lino.modlib.notes import Plugin


class Plugin(Plugin):

    extends_models = ['Note']
