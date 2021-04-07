# -*- coding: UTF-8 -*-
# Copyright 2014-2019 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
"""
For each client who has a non-empty `card_number` we create a
corresponding image file in the local media directory in order to
avoid runtime error when printing documents thaqt include this picture
(`eid_content.odt` and `file_sheet.odt`).

"""

import os
import shutil

from lino.api import rt, dd


def objects():

    Client = rt.models.pcsw.Client

    for obj in Client.objects.exclude(card_number=''):
        fn = obj.get_image_path()
        if not os.path.exists(fn):
            src = Client.card_number_to_image_path(None)
            #dd.logger.info("20150531 copy %s to %s...", src, fn)
            rt.makedirs_if_missing(os.path.dirname(fn))
            shutil.copyfile(src, fn)
            yield obj  # actually there's no need to save obj, but we
                       # must make this function a generator

        # else:
           # dd.logger.info("20150531 %s exists", fn)
