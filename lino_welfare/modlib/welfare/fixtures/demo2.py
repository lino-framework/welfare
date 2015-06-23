# -*- coding: UTF-8 -*-
# Copyright 2014-2015 Luc Saffre
# License: BSD (see file COPYING for details)
"""Makes sure that there is at least one excerpt for every ExcerptType.
Render all excerpts by running their do_print method.

For each client who has a non-empty `card_number` we create a
corresponding image file in the local media directory in order to
avoid runtime error when printing documents who include this picture
(`eid_content.odt` and `file_sheet.odt`).

"""

import os
import shutil

from lino.api import rt, dd

from lino.modlib.beid.mixins import get_image_path


def objects():

    ses = rt.login('melanie')

    ExcerptType = rt.modules.excerpts.ExcerptType
    Excerpt = rt.modules.excerpts.Excerpt
    Client = rt.modules.pcsw.Client

    for obj in Client.objects.exclude(card_number=''):
        fn = obj.get_image_path()
        if not os.path.exists(fn):
            src = get_image_path(None)
            #dd.logger.info("20150531 copy %s to %s...", src, fn)
            rt.makedirs_if_missing(os.path.dirname(fn))
            shutil.copyfile(src, fn)
        #else:
            #dd.logger.info("20150531  %s exists", fn)
        
    for et in ExcerptType.objects.all():
        if Excerpt.objects.filter(excerpt_type=et).count() == 0:
            model = et.content_type.model_class()
            qs = model.objects.all()
            if qs.count() > 0:
                ses.selected_rows = [qs[0]]
                yield et.get_or_create_excerpt(ses)

    for obj in Excerpt.objects.all():
        # dd.logger.info("20150526 rendering %s", obj)
        rv = ses.run(obj.do_print)
        assert rv['success']

