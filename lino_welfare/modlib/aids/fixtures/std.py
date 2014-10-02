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

    IncomeConfirmation = rt.modules.aids.IncomeConfirmation
    RefundConfirmation = rt.modules.aids.RefundConfirmation
    SimpleConfirmation = rt.modules.aids.SimpleConfirmation
    ConfirmationTypes = rt.modules.aids.ConfirmationTypes

    aidType = Instantiator(
        'aids.AidType',
        confirmation_type=ConfirmationTypes.get_for_model(
            IncomeConfirmation)).build
    kw = dd.babelkw(
        'name',
        de="Eingliederungseinkommen",
        en="Eingliederungseinkommen",
        fr="Revenu d'intégration")
    kw.update(short_name="EiEi")
    kw.update(
        dd.babelkw(
            'long_name',
            de="""\
{{when}} das durch Gesetz vom 26. Mai 2002 eingeführte
<b>Eingliederungseinkommen</b>
{%- if obj.amount %}
in Höhe von <b>{{decfmt(obj.amount)}} €/Monat</b>
{% endif -%}
{%- if obj.category %}
(Kategorie: <b>{{obj.category}}</b>)
{% endif -%}
{{iif(past, "bezogen hat", "bezieht")}}.
""",
            fr="""\
{{iif(past, "a bénéficié", "bénéficie")}}
{{when}} du <b>revenu d'intégration</b> prévu par la loi
du 26 mai 2002
{%- if obj.amount %}
d'un montant de <b>{{decfmt(obj.amount)}} €/mois</b>
{% endif -%}
{%- if obj.category %}
(Catégorie: <b>{{obj.category}}</b>)
{% endif -%}.
"""))
    yield aidType(**kw)

    kw = dd.babelkw(
        'name',
        de="Ausländerbeihilfe",
        en="Ausländerbeihilfe",
        fr="Aide aux immigrants")
    kw.update(dd.babelkw('long_name',
                         de="""\
{{when}} eine laut Gesetz vom 2. April 1965 eingeführte
<b>Sozialhilfe für Ausländer</b>
{%- if obj.amount %}
in Höhe von <b>{{decfmt(obj.amount)}} €/Monat</b>
{% endif -%}
{%- if obj.category %}
(Kategorie: <b>{{obj.category}}</b>)
{% endif -%}
{{iif(past, "bezogen hat", "bezieht")}}
""",
                         fr="""\
{{iif(past, "a bénéficié", "bénéficie")}}
{{when}} d'une <b>aide sociale pour étrangers</b>
prévue par la loi du 2 avril 1965
{%- if obj.amount %}
d'un montant de <b>{{decfmt(obj.amount)}} €/mois</b>
{% endif -%}
{%- if obj.category %}
(Catégorie: <b>{{obj.category}}</b>)
{% endif -%}.
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
            de="""\
{{when}} eine feste Beihilfe
{{iif(past, "bezogen hat", "bezieht")}}.""",
            fr="""\
{{iif(past, "a bénéficié", "bénéficie")}}
{{when}} d'une aide fixe."""))
    yield aidType(**kw)

    aidType = Instantiator(
        'aids.AidType', "name",
        confirmation_type=ConfirmationTypes.get_for_model(
            SimpleConfirmation)).build
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
        confirmation_type=ConfirmationTypes.get_for_model(
            RefundConfirmation)).build
    kw = dd.babelkw(
        'name',
        de="Übernahme von Arzt- und/oder Medikamentenkosten",
        en="Medical costs",
        fr="Remboursement de frais médicaux")
    kw.update(short_name="AMK")
    fkw = dd.str2kw('name', _("Pharmacy"))  # Apotheke
    cct_pharmacy = rt.modules.pcsw.ClientContactType.objects.get(**fkw)
    kw.update(pharmacy_type=cct_pharmacy)
    kw.update(dd.babelkw('long_name',
                         de="""\
für den Zeitraum {{when}} Anrecht auf
Übernahme folgender <b>Arzt- und/oder Medikamentenkosten</b>
durch das ÖSHZ {{iif(past, "hat", "hatte")}}:
<ul>
{%- if obj.doctor -%}
<li><b>Arzthonorare</b> in Höhe der LIKIV-Tarife für die Visite
{%- if obj.doctor_type_id %}
beim {{obj.doctor_type}} {% else %} bei
{% endif -%}
<b>{{obj.doctor.get_full_name()}}</b>.
</li>
{%- endif -%}
{%- if obj.pharmacy -%}
<li><b>Arzneikosten</b> für die durch
{%- if obj.doctor %}
<b>{{obj.doctor.get_full_name()}}</b> verschriebenen und
{% endif -%}
<b>{{obj.pharmacy.get_full_name()}}</b> ausgehändigten Medikamente.
</li>
{%- endif -%}
</ul>

Falls weitere Behandlungen notwendig sind, benötigen wir unbedingt
einen Kostenvoranschlag. Danke.

""",
                         fr="""\
"""))

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
        confirmation_type=ConfirmationTypes.get_for_model(
            SimpleConfirmation)).build
    yield aidType(_("Möbellager"))
    yield aidType(_("Heizkosten"))

    kw = dd.babelkw(
        'name',
        de="Lebensmittelbank",
        en="Food bank",
        fr="Banque alimentaire")
    kw.update(confirmed_by_primary_coach=False)
    kw.update(
        dd.babelkw(
            'long_name',
            de="""\
{{when}} aus Gründen der sozial-finanziellen Lage Anrecht auf
eine Sozialhilfe in Naturalien durch Nutzung der
Lebensmittelbank {{iif(past, "hat", "hatte")}}.
""",
            fr="""\
{{iif(past, "a bénéficié", "bénéficie")}}
{{when}} du droit d'utiliser la banque alimentaire.
"""))

    yield aidType(**kw)

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

