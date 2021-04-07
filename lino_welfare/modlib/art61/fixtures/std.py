# -*- coding: UTF-8 -*-
# Copyright 2015 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

"""Adds a default contract type for art61.

"""

from lino.api import dd, rt


def objects():
    CT = rt.models.art61.ContractType
    yield CT(**dd.str2kw('name', rt.models.art61.Contract._meta.verbose_name))
