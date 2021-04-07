# -*- coding: UTF-8 -*-
# Copyright 2015-2016 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

"""Adds demo user "Wilfried".

"""

from lino.api import dd, rt

current_group = None


def objects():
    User = rt.models.users.User
    wilfried = User(username="wilfried",
                    first_name="Wilfried", last_name="Willems",
                    user_type='500')
    yield wilfried
    # See sepa/fixtures/demo.py for the rest of legder fixtures (Since sepa depend on ledger)
