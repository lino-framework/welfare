# -*- coding: UTF-8 -*-
# Copyright 2015 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
"""Adds some training types and some training goals.

TODO: ask Mathieu and Gerd for their advice in establishing a more or
less complete/useful set of default data.  See also `leforem.be
<https://www.leforem.be/particuliers/seformer/stages/stages-en-entreprises.html>`_.

"""

from django.utils.translation import gettext_lazy as _

from lino.api import rt, dd


def objects():
    TT = rt.models.immersion.ContractType
    Goal = rt.models.immersion.Goal

    def str2obj(model, name, **kwargs):
        kwargs.update(dd.str2kw('name', name))
        return model(**kwargs)

    yield str2obj(Goal, _("Discover a job"))
    yield str2obj(Goal, _("Confirm a professional project"))
    yield str2obj(Goal, _("Gain work experience"))
    yield str2obj(Goal, _("Show competences"))

    yield str2obj(TT, _("Internal engagement"), template="Default.odt")
    yield str2obj(TT, _("Immersion training"), template="StageForem.odt")
    yield str2obj(TT, _("MISIP"), template="Default.odt")

    kw = dict(
        email_template='Default.eml.html',
        body_template='immersion.body.html',
        primary=True, certifying=True,
        #template='Default.odt',
        **dd.str2kw('name', _("Immersion training")))
    yield rt.models.excerpts.ExcerptType.update_for_model(
        'immersion.Contract', **kw)
