# -*- coding: UTF-8 -*-
# Copyright 2012-2015 Luc Saffre
# License: BSD (see file COPYING for details)
"""
Standard data for `lino_welfare.modlib.debts`.
"""

from lino.api import dd, rt, _


def objects():

    from lino_welfare.modlib.debts.fixtures.minimal import objects
    yield objects()

    ExcerptType = rt.modules.excerpts.ExcerptType
    kw = dict(
        # template='Default.odt',
        certifying=True)
    kw.update(dd.str2kw('name', _("Financial situation")))
    yield ExcerptType.update_for_model('debts.Budget', **kw)
