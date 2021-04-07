# -*- coding: UTF-8 -*-
# Copyright 2016 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
"""
Standard data for `lino_welfare.modlib.esf`.
"""

from lino.api import dd, rt, _


def objects():

    ExcerptType = rt.models.excerpts.ExcerptType
    kw = dict(
        build_method='weasy2pdf',
        certifying=True)
    kw.update(dd.str2kw('name', _("Training report")))
    yield ExcerptType.update_for_model('esf.ClientSummary', **kw)
