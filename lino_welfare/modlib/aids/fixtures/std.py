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
        'aids.AidType', "name",
        aid_regime=AidRegimes.financial).build
    yield aidType(_("Eingliederungseinkommen"))
    yield aidType(_("Ausländerbeihilfe"))
    yield aidType(_("Feste Beihilfe"))
    yield aidType(_("Erstattung"))
    yield aidType(_("Übernahmeschein"))
    yield aidType(_("DMH-Übernahmeschein"))

    aidType = Instantiator(
        'aids.AidType', "name",
        aid_regime=AidRegimes.medical).build
    yield aidType(_("Allgemeine medizinische Kosten"))

    aidType = Instantiator(
        'aids.AidType', "name",
        aid_regime=AidRegimes.other).build
    yield aidType(_("Möbellager"))
    yield aidType(_("Heizkosten"))

    Decider = Instantiator('aids.Decider', "name").build
    yield Decider("Sozialhilferat (SHR)")
    yield Decider("Ständiges Präsidium (SP)")
    yield Decider("Sozialhilfeausschuss (SAS)")

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
