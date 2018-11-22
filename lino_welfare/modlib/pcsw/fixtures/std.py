# -*- coding: UTF-8 -*-
# Copyright 2011,2013 Rumma & Ko Ltd
# This file is part of Lino Welfare.
#
# Lino Welfare is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# Lino Welfare is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License along with Lino Welfare.  If not, see
# <http://www.gnu.org/licenses/>.
"""Adds default data for `PersonGroup` and `DispenseReason`.

"""

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from lino.utils.instantiator import Instantiator, i2d
from lino.api.dd import babelkw


from lino.api import dd, rt
from lino.modlib.uploads.choicelists import Shortcuts

UPLOADTYPE_RESIDENCE_PERMIT = 1
UPLOADTYPE_WORK_PERMIT = 2
UPLOADTYPE_DRIVING_LICENSE = 3


def uploads_objects():
    Recurrencies = rt.models.cal.Recurrencies
    UploadType = rt.models.uploads.UploadType

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


def objects():
    from lino.api import dd, rt
    pcsw = dd.resolve_app('pcsw')

    #~ persongroup = Instantiator('pcsw.PersonGroup','name').build
    # Auswertung / Bilan
    yield pcsw.PersonGroup(ref_name='1', name=_("Evaluation"))
    # Formation / Ausbildung
    yield pcsw.PersonGroup(ref_name='2', name=_("Formation"))
    yield pcsw.PersonGroup(ref_name='4', name=_("Search"))  # Suche / Recherche
    yield pcsw.PersonGroup(ref_name='4bis', name=_("Work"))  # Arbeit / Travail
    yield pcsw.PersonGroup(ref_name='9', name=_("Standby"))
    #~ yield persongroup(u"Bilan",ref_name='1')
    #~ yield persongroup(u"Formation",ref_name='2')
    #~ yield persongroup(u"Recherche",ref_name='4')
    #~ yield persongroup(u"Travail",ref_name='4bis')
    #~ yield persongroup(u"Standby",ref_name='9',active=False)

    yield pcsw.DispenseReason(**babelkw('name', de="Gesundheitlich", fr="Santé", en="Health"))
    yield pcsw.DispenseReason(**babelkw('name', de="Studium/Ausbildung", fr="Etude/Formation", en="Studies"))
    yield pcsw.DispenseReason(**babelkw('name', de="Familiär", fr="Cause familiale", en="Familiar"))
    yield pcsw.DispenseReason(**babelkw('name', de="Sonstige", fr="Autre", en="Other"))

    yield uploads_objects()
