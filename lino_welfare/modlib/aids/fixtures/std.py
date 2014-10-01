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
from lino import dd, rt


def objects():

    AidRegimes = rt.modules.aids.AidRegimes
    IncomeConfirmation = rt.modules.aids.IncomeConfirmation
    RefundConfirmation = rt.modules.aids.RefundConfirmation
    SimpleConfirmation = rt.modules.aids.SimpleConfirmation
    ConfirmationTypes = rt.modules.aids.ConfirmationTypes

    aidType = Instantiator(
        'aids.AidType',
        confirmation_type=ConfirmationTypes.get_for_model(IncomeConfirmation),
        aid_regime=AidRegimes.financial).build
    kw = dd.babelkw(
        'name',
        de="Eingliederungseinkommen",
        en="Eingliederungseinkommen",
        fr="Revenu d'intégration")
    kw.update(short_name="EiEi")
    kw.update(
        dd.babelkw(
            'long_name',
            de="""das durch Gesetz vom 26. Mai 2002 eingeführte
            Eingliederungseinkommen {{iif(past, "bezogen hat", "bezieht")}}""",
            fr="""{{iif(past, "a bénéficié", "bénéficie")}}
            du revenu d'intégration prévue par la loi du 26 mai 2002"""))
    yield aidType(**kw)

    kw = dd.babelkw(
        'name',
        de="Ausländerbeihilfe",
        en="Ausländerbeihilfe",
        fr="Aide aux immigrants")
    kw.update(
        dd.babelkw(
            'long_name',
            de="""eine laut Gesetz vom 2. April 1965 eingeführte
            Sozialhilfe für Ausländer
            (Kategorie: {{obj.category or "undefiniert"}})
            {{iif(past, "bezogen hat", "bezieht")}}""",
            fr="""{{iif(past, "a bénéficié", "bénéficie")}}
            d'une aide sociale pour étrangers
            prévue par la loi du 2 avril 1965
            (Catégorie: {{obj.category or 'non spécifiée'}}).
            """))
    yield aidType(**kw)

    kw = dd.babelkw(
        'name',
        de="Feste Beihilfe",
        en="Feste Beihilfe",
        fr="Revenu fixe")
    kw.update(
        dd.babelkw(
            'long_name',
            de="""eine feste Beihilfe
            {{iif(past, "bezogen hat", "bezieht")}}""",
            fr="""{{iif(past, "a bénéficié", "bénéficie")}}
            d'une aide fixe"""))
    yield aidType(**kw)

    aidType = Instantiator(
        'aids.AidType', "name",
        confirmation_type=ConfirmationTypes.get_for_model(SimpleConfirmation),
        aid_regime=AidRegimes.medical).build
    kw = dd.babelkw(
        'name',
        de="Erstattung",
        en="Erstattung",
        fr="Remboursement")
    yield aidType(**kw)
    kw = dd.babelkw(
        'name',
        de="Übernahmeschein",
        en="Übernahmeschein",
        fr="Übernahmeschein")
    yield aidType(**kw)

    aidType = Instantiator(
        'aids.AidType', "name",
        confirmation_type=ConfirmationTypes.get_for_model(RefundConfirmation),
        aid_regime=AidRegimes.medical).build
    kw = dd.babelkw(
        'name',
        de="Arzt- u/o Medikamentenkosten",
        en="Medical Costs",
        fr="Remboursement de frais médicaux")
    kw.update(short_name="AMK")
    yield aidType(**kw)
    kw = dd.babelkw(
        'name',
        de="DMH-Übernahmeschein",
        en="DMH-Übernahmeschein",
        fr="DMH-Übernahmeschein")
    kw.update(short_name="AMK(DMH)")
    yield aidType(**kw)

    aidType = Instantiator(
        'aids.AidType', "name",
        confirmation_type=ConfirmationTypes.get_for_model(SimpleConfirmation),
        aid_regime=AidRegimes.other).build
    yield aidType(_("Möbellager"))
    yield aidType(_("Heizkosten"))

    kw = dd.babelkw(
        'name',
        de="Lebensmittelbank",
        en="Food bank",
        fr="Banque alimentaire")
    kw.update(
        dd.babelkw(
            'long_name',
            de="aus Gründen der sozial-finanziellen Lage Anrecht auf "
            "eine Sozialhilfe in Naturalien durch Nutzung der "
            "Lebensmittelbank",
            fr="le droit d'utiliser la banque alimentaire"))

    yield aidType(**kw)

    if False:
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

