# -*- coding: UTF-8 -*-
# Copyright 2015-2020 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)


"""
Creates fictive demo bookings to monthly payment orders and bank
statements.

This just calls the default :fixture:`payments` fixture of
:mod:`lino_xl.lib.finan` with customized journal names.


"""

from lino_xl.lib.finan.fixtures.payments import objects as xl_objects


def objects():

    yield xl_objects('AAW ZKBC')
