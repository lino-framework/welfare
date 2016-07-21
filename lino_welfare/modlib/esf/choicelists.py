# -*- coding: UTF-8 -*-
# Copyright 2016 Luc Saffre
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

"""Choicelists for `lino_welfare.modlib.esf`.

"""
from __future__ import unicode_literals

from django.db import models

from lino.api import dd, _
from lino.utils.dates import weekdays
from lino.utils.quantities import Duration

ZERO = Duration("0:00")


class ParticipationCertificates(dd.ChoiceList):
    verbose_name = _("Participation Certificate")
    verbose_name_plural = _("Participation Certificates")
add = ParticipationCertificates.add_item
add('10', _("Epreuve d’évaluation réussie sans titre spécifique"))


class StatisticalField(dd.Choice):

    field_name = None
    field = None

    def __init__(self, value, text, name=None, **kwargs):
        super(StatisticalField, self).__init__(
            value, text, name, **kwargs)
        self.field_name = "esf" + value
        self.field = self.create_field()

    def collect_from_guest(self, obj):
        pass

    def collect_from_immersion_contract(self, obj):
        pass

    def collect_from_jobs_contract(self, obj):
        pass


class GuestCount(StatisticalField):

    def create_field(self):
        return models.IntegerField(
            self.value, default=0, help_text=self.text)

    def collect_from_guest(self, obj):
        if obj.event.event_type is None:
            return 0
        sf = obj.event.event_type.esf_field
        if sf is not None and sf.value == self.value:
            return 1
        return 0


class HoursField(StatisticalField):
    def create_field(self):
        return dd.DurationField(
            self.value, default=ZERO,
            help_text=self.text)


class GuestHours(HoursField):
    def collect_from_guest(self, obj):
        # obj is a `cal.Guest` instance
        if obj.event.event_type is None:
            return
        sf = obj.event.event_type.esf_field
        if sf is None or sf.value != self.value:
            return
        if obj.gone_since is None or obj.busy_since is None:
            return
        return Duration(obj.gone_since - obj.busy_since)


class ImmersionHours(HoursField):

    def collect_from_immersion_contract(self, obj):
        # obj is a `immersion.Contract` instance
        sd = obj.applies_from
        ed = obj.date_ended
        if sd and ed:
            nb_of_days = weekdays(sd, ed)
            return Duration("8:00") * nb_of_days


class Art60Hours(HoursField):
    def collect_from_jobs_contract(self, obj):
        # obj is a `jobs.Contract` instance
        return Duration("8:00") * obj.duration


class StatisticalFields(dd.ChoiceList):
    verbose_name = _("ESF field")
    verbose_name_plural = _("ESF fields")
    item_class = StatisticalField

add = StatisticalFields.add_item_instance

# Séance d'info
add(GuestCount('10', _("Informative sessions")))

# Entretien individuel
add(GuestCount('20', _("Individual consultation")))

# Evaluation formation externe et art.61
add(GuestCount('21', _("Evaluation of external training")))

# S.I.S. agréé
add(GuestCount('30', _("Certified integration service")))

# Tests de niveau
add(GuestCount('40', _("Level tests")))

# Initiation informatique
add(GuestCount('41', _("IT basics")))

# Mobilité
add(GuestCount('42', _("Mobility")))

# Remédiation mathématique et français
add(GuestCount('43', _("Remedial teaching")))

# Activons-nous
add(GuestCount('44', _("Wake up!")))

# Mise en situation professionnelle : calculer les heures par stage
# d'immersion, en fonction des dates de début et de fin et de
# l'horaire de travail.
add(ImmersionHours('50', _("Getting a professional situation")))

# Cyber-employ : Somme des présences aux ateliers "Cyber-emploi", mais
# pour ces ateliers on note les heures d'arrivée et de départ par
# participation.
add(GuestHours('60', _("Cyber Job")))

# Mise à l’emploi sous contrat art.60§7
add(Art60Hours('70', _("Art 60§7 job supplyment")))


@dd.receiver(dd.pre_analyze)
def inject_statistical_fields(sender, **kw):
    for sf in StatisticalFields.items():
        if sf.field_name is not None:
            dd.inject_field('esf.ClientSummary', sf.field_name, sf.field)

dd.inject_field(
    'cal.EventType', 'esf_field', StatisticalFields.field(blank=True))
