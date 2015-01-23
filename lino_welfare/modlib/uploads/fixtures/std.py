# -*- coding: UTF-8 -*-
# Copyright 2015 Luc Saffre
# License: BSD (see file COPYING for details)
"""
Default data for :mod:`lino_welfare.modlib.uploads`.
"""

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from lino import dd
from lino.utils.instantiator import Instantiator
from lino.modlib.uploads.choicelists import Shortcuts

UPLOADTYPE_RESIDENCE_PERMIT = 1
UPLOADTYPE_WORK_PERMIT = 2
UPLOADTYPE_DRIVING_LICENSE = 3


def objects():

    uploadType = Instantiator(
        'uploads.UploadType',
        max_number=1, wanted=True).build
    yield uploadType(
        id=UPLOADTYPE_RESIDENCE_PERMIT,
        **dd.str2kw('name', _("Residence  permit")))
        # 'name', de=u"Aufenthaltserlaubnis",
        # fr=u"Permis de séjour", en="Residence permit"))

    yield uploadType(
        id=UPLOADTYPE_WORK_PERMIT,
        **dd.str2kw('name', _("Work permit")))
        # **dd.babelkw(
        # 'name', de=u"Arbeitserlaubnis",
        # fr=u"Permis de travail", en="Work permit"))
    yield uploadType(
        id=UPLOADTYPE_DRIVING_LICENSE,
        **dd.str2kw('name', _("Driving licence")))

    uploadType = Instantiator(
        'uploads.UploadType'  # , upload_area=UploadAreas.job_search
    ).build
    yield uploadType(**dd.str2kw('name', _("Contract")))
    uploadType = Instantiator(
        'uploads.UploadType'  # , upload_area=UploadAreas.medical
    ).build
    yield uploadType(
        **dd.babelkw(
            'name',
            de="Ärztliche Bescheinigung",
            fr="Certificat médical",
            en="Medical certificate"))
    yield uploadType(
        **dd.babelkw(
            'name',
            de="Behindertenausweis",
            fr="Certificat de handicap",
            en="Handicap certificate"))

    uploadType = Instantiator('uploads.UploadType').build
    yield uploadType(wanted=True, **dd.str2kw('name', _("Diploma")))

    yield uploadType(
        **dd.babelkw(
            'name', de=u"Personalausweis",
            fr=u"Carte d'identité", en="ID card"))
    yield uploadType(
        shortcut=Shortcuts.id_document,
        **dd.str2kw('name', _("Identifying document")))

