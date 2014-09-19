# -*- coding: UTF-8 -*-
# Copyright 2008-2014 Luc Saffre
# License: BSD (see file COPYING for details)


from lino import dd


def objects():

    for et in dd.modules.excerpts.ExcerptType.objects.all():
        model = et.content_type.model_class()
        qs = model.objects.all()
        if qs.count() > 0:
            ses = dd.login('melanie')  # user=AGENTS.pop())
            ses.selected_rows = [qs[0]]
            yield et.get_or_create_excerpt(ses)

