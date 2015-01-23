# -*- coding: UTF-8 -*-
# Copyright 2015 Luc Saffre
# License: BSD (see file COPYING for details)
"""
Demo data for :mod:`lino_welfare.modlib.uploads`.
"""

from lino import dd, rt

from lino.modlib.uploads.choicelists import Shortcuts

from lino_welfare.modlib.uploads.fixtures.std import (
    UPLOADTYPE_RESIDENCE_PERMIT,
    UPLOADTYPE_WORK_PERMIT,
    UPLOADTYPE_DRIVING_LICENSE)


def objects():
    Upload = rt.modules.uploads.Upload
    UploadType = rt.modules.uploads.UploadType
    Client = rt.modules.pcsw.Client
    ClientStates = rt.modules.pcsw.ClientStates

    newcomer = Client.objects.get(id=121)
    assert newcomer.client_state == ClientStates.newcomer

    coached = Client.objects.get(id=124)
    # assert coached.client_state == ClientStates.coached
    # true only for eupen, not for chatelet

    id_card = UploadType.objects.get(shortcut=Shortcuts.id_document)
    residence_permit = UploadType.objects.get(id=UPLOADTYPE_RESIDENCE_PERMIT)
    work_permit = UploadType.objects.get(id=UPLOADTYPE_WORK_PERMIT)
    driving_license = UploadType.objects.get(id=UPLOADTYPE_DRIVING_LICENSE)

    # a reception clerk:
    clerk = rt.login('theresia').get_user()

    # a general social agent:
    agent = rt.login('caroline').get_user()

    # an integration agent:
    ai = rt.login('alicia').get_user()

    # this newcomer has 2 id cards. one of these is no longer valid
    # (and we know it: `needed` has been unchecked). The other is
    # still valid but will expire in 3 days.

    kw = dict(owner=newcomer, type=id_card)
    yield Upload(end_date=dd.demo_date(-30), needed=False,
                 user=clerk, **kw)
    yield Upload(end_date=dd.demo_date(3), user=clerk, **kw)

    # this coached client has three documents uploaded:

    kw = dict(owner=coached)
    yield Upload(type=residence_permit, end_date=dd.demo_date(300),
                 user=clerk, **kw)
    yield Upload(type=work_permit, end_date=dd.demo_date(100),
                 user=ai, **kw)
    yield Upload(type=driving_license, end_date=dd.demo_date(10),
                 user=agent, **kw)
