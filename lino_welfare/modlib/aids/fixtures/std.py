# -*- coding: UTF-8 -*-
# Copyright 2014 Luc Saffre
# This file is part of the Lino-Welfare project.
# Lino-Welfare is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
# Lino-Welfare is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with Lino-Welfare; if not, see <http://www.gnu.org/licenses/>.

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from north.dbutils import babel_values
from lino.utils.instantiator import Instantiator
from lino import dd


def objects():

    AidRegimes = dd.modules.aids.AidRegimes

    aidType = Instantiator(
        'aids.AidType', aid_regime=AidRegimes.financial).build
    yield aidType(
        **dd.babelkw(
            'name',
            de="Eingliederungseinkommen",
            en="Eingliederungseinkommen",
            fr="Revenu d'intégration"))
    kw = dd.babelkw(
        'name',
        de="Ausländerbeihilfe",
        en="Ausländerbeihilfe",
        fr="Aide aux immigrants")
    kw.update(
        dd.babelkw(
            'long_name',
            de="laut Gesetz vom 2. April 1965 eingeführte \
            Sozialhilfe für Ausländer",
            fr="aide sociale pour étrangers \
            prévue par la loi du 2 avril 1965"))
    yield aidType(**kw)
    yield aidType(
        **dd.babelkw(
            'name',
            de="Feste Beihilfe",
            en="Feste Beihilfe",
            fr="Revenu fixe"))
    # yield aidType(_("Erstattung"))
    # yield aidType(_("Übernahmeschein"))
    # yield aidType(_("DMH-Übernahmeschein"))

    aidType = Instantiator(
        'aids.AidType', "name",
        aid_regime=AidRegimes.medical).build
    yield aidType(
        **dd.babelkw(
            'name',
            de="Allgemeine medizinische Kosten",
            en="General Medical Costs",
            fr="Remboursement de frais médicaux"))

    # aidType = Instantiator(
    #     'aids.AidType', "name",
    #     aid_regime=AidRegimes.other).build
    yield aidType(_("Möbellager"))
    yield aidType(_("Heizkosten"))

    aidRole = Instantiator(
        'aids.HelperRole', "name",
        aid_regime=AidRegimes.medical).build
    yield aidRole(
        **dd.babelkw(
            'name',
            de="Hausarzt",
            en="General physician",
            et="Perearst",
            fr="Médecin général"))
    yield aidRole(
        **dd.babelkw(
            'name',
            de="Facharzt",
            en="Special physician",
            et="Eriala arst",
            fr="Médecin spécialisé"))
    yield aidRole(
        **dd.babelkw(
            'name',
            de="Apotheke",
            en="Pharmacy",
            et="Apteek",
            fr="Pharmacie"))

    Category = dd.resolve_model('aids.Category')
    yield Category(**babel_values(
        'name',
        en="Living together",
        de="Zusammenlebend",
        fr="Cohabitant"))
    yield Category(**babel_values(
        'name',
        en="Living alone",
        de="Alleinstehend",
        fr="Persone isolée"))
    yield Category(**babel_values(
        'name',
        en="Person with family at charge",
        de="Person mit Familienlasten",
        fr="Personne qui cohabite avec une famille à sa charge"))

    Decider = dd.resolve_model('boards.Board')
    yield Decider(**dd.str2kw(
        'name', _("Social Board (SB)")))  # "Sozialhilferat (SHR)"
    yield Decider(**dd.str2kw(
        'name', _("Social Commission (SC)")))  # Sozialhilfeausschuss (SAS)
    yield Decider(**dd.str2kw(
        'name', _("Permanent Board (PB)")))  # Ständiges Präsidium (SP)

