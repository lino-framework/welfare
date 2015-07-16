# -*- coding: UTF-8 -*-
# Copyright 2015 Luc Saffre
# License: BSD (see file COPYING for details)

from __future__ import unicode_literals

from lino.api import dd, rt, _


def objects():

    ExcerptType = rt.modules.excerpts.ExcerptType
    Enrolment = rt.modules.courses.Enrolment
    # ContentType = rt.modules.contenttypes.ContentType
    kw = dict(
        # template='Default.odt',
        body_template='enrolment.body.html',
        print_recipient=False, certifying=True)
    kw.update(dd.str2kw('name', _("Enrolment")))
    yield ExcerptType.update_for_model(Enrolment, **kw)

    # kw = dict(
    #     body_template='intervention.body.html',
    #     print_recipient=False, certifying=True)
    # kw.update(dd.str2kw('name', _("Intervention request")))
    # kw.update(content_type=ContentType.objects.get_for_model(Enrolment))
    # yield ExcerptType(**kw)

