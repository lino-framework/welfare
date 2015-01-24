# -*- coding: UTF-8 -*-
# Copyright 2015 Luc Saffre
# License: BSD (see file COPYING for details)
"""
Default data for :mod:`lino_welfare.modlib.uploads`.
"""

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from lino.api import dd, rt
from lino.modlib.uploads.choicelists import Shortcuts

UPLOADTYPE_RESIDENCE_PERMIT = 1
UPLOADTYPE_WORK_PERMIT = 2
UPLOADTYPE_DRIVING_LICENSE = 3


def objects():
    Recurrencies = rt.modules.cal.Recurrencies
    UploadType = rt.modules.uploads.UploadType

    kw = dict(
        warn_expiry_unit=Recurrencies.monthly,
        warn_expiry_value=2)
    kw.update(max_number=1, wanted=True)
    kw.update(dd.str2kw('name', _("Residence permit")))
    # 'name', de=u"Aufenthaltserlaubnis",
    # fr=u"Permis de séjour", en="Residence permit"))
    yield UploadType(id=UPLOADTYPE_RESIDENCE_PERMIT, **kw)

    kw.update(dd.str2kw('name', _("Work permit")))
        # 'name', de=u"Arbeitserlaubnis",
        # fr=u"Permis de travail", en="Work permit"))
    yield UploadType(id=UPLOADTYPE_WORK_PERMIT, **kw)

    kw.update(warn_expiry_value=1)

    kw.update(dd.str2kw('name', _("Driving licence")))
    yield UploadType(id=UPLOADTYPE_DRIVING_LICENSE, **kw)

    kw.update(dd.str2kw('name', _("Identifying document")))
    yield UploadType(shortcut=Shortcuts.id_document, **kw)

    kw.update(max_number=-1, wanted=False)
    kw.update(warn_expiry_unit='')

    kw.update(dd.str2kw('name', _("Contract")))
    yield UploadType(**kw)

    kw.update(dd.str2kw('name', _("Medical certificate")))
    # de="Ärztliche Bescheinigung",
    # fr="Certificat médical",
    yield UploadType(**kw)

    kw.update(dd.str2kw('name', _("Handicap certificate")))
    # de="Behindertenausweis",
    # fr="Certificat de handicap",
    yield UploadType(**kw)

    kw.update(wanted=True)
    kw.update(dd.str2kw('name', _("Diploma")))
    yield UploadType(**kw)

    kw.update(wanted=False)
    kw.update(dd.str2kw('name', _("Identity card")))
    # fr=u"Carte d'identité", en="Identity card"))
    yield UploadType(**kw)


