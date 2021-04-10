# -*- coding: UTF-8 -*-
# Copyright 2012-2021 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

"""
Standard data for `lino_welfare.modlib.debts`.
"""

from lino.api import dd, rt, _


def objects():

    from lino_welfare.modlib.debts.fixtures.minimal import objects
    yield objects()

    ExcerptType = rt.models.excerpts.ExcerptType
    kw = dict(
        # template='Default.odt',
        certifying=True)
    kw.update(dd.str2kw('name', _("Financial situation")))
    yield ExcerptType.update_for_model('debts.Budget', **kw)
