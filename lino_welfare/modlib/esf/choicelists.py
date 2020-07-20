# -*- coding: UTF-8 -*-
# Copyright 2016-2019 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

from __future__ import unicode_literals
import datetime

from django.db import models

from lino.utils import last_day_of_month

from lino.api import dd, _
from lino.utils.dates import weekdays
from lino.utils.quantities import Duration
from lino_xl.lib.cal.choicelists import GuestStates

ZERO = Duration("0:00")


class ParticipationCertificates(dd.ChoiceList):
    verbose_name = _("Participation Certificate")
    verbose_name_plural = _("Participation Certificates")
add = ParticipationCertificates.add_item
add('10', _("Epreuve d’évaluation réussie sans titre spécifique"))


class StatisticalField(dd.Choice):
    field_name = None
    field = None
    short_name = None

    def __init__(self, value, short_name, text, name=None, **kwargs):
        super(StatisticalField, self).__init__(
            value, text, name, **kwargs)
        self.field_name = "esf" + value
        self.short_name = short_name
        self.field = self.create_field()

    def collect_from_guest(self, obj, summary):
        pass

    def collect_from_immersion_contract(self, obj, summary):
        pass

    def collect_from_jobs_contract(self, obj, summary):
        pass


class GuestCount(StatisticalField):

    def create_field(self):
        return models.IntegerField(
            self.short_name, default=0, help_text=self.text)

    def collect_from_guest(self, obj, summary):
        if obj.event.event_type is None:
            return 0
        sf = obj.event.event_type.esf_field
        if sf is not None and sf.value == self.value:
            return 1
        return 0

class HoursField(StatisticalField):
    def create_field(self):
        return dd.DurationField(
            self.short_name, default=ZERO,
            help_text=self.text, max_length=8)

    def daterange2hours(self, sd, ed, summary):
        if summary.year is None:
            return
        if sd and ed:
            ssd = datetime.date(summary.year, summary.month or 1, 1)
            sd = max(sd, ssd)
            
            sed = last_day_of_month(
                datetime.date(summary.year, summary.month or 12, 1))
            ed = min(ed, sed)
            nb_of_days = weekdays(sd, ed)
            return Duration("38:00") * nb_of_days / 5
            # return Duration("8:00") * nb_of_days


class GuestHours(HoursField):
    def collect_from_guest(self, obj, summary):
        # obj is a `cal.Guest` instance
        if obj.event.event_type is None:
            return
        sf = obj.event.event_type.esf_field
        if sf is None or sf.value != self.value:
            return
        if obj.gone_since is None or obj.busy_since is None:
            return
        return Duration(obj.gone_since - obj.busy_since)


class GuestHoursEvent(HoursField):

    def collect_from_guest(self, obj, summary):
        if obj.event.event_type is None:
            return
        sf = obj.event.event_type.esf_field
        if sf is None or sf.value != self.value:
            return
        if obj.state not in GuestStates.present_states:
            return
        return obj.event.get_duration()


class GuestHoursFixed(HoursField):

    hours_per_guest = Duration('1:00')
    
    def collect_from_guest(self, obj, summary):
        if obj.event.event_type is None:
            return
        sf = obj.event.event_type.esf_field
        if sf is None or sf.value != self.value:
            return
        return sf.hours_per_guest


class ImmersionHours(HoursField):

    def collect_from_immersion_contract(self, obj, summary):
        # obj is a `immersion.Contract` instance
        return self.daterange2hours(
            obj.applies_from, obj.date_ended, summary)


class Art60Hours(HoursField):
    def collect_from_jobs_contract(self, obj, summary):
        # obj is a `jobs.Contract` instance
        return self.daterange2hours(
            obj.applies_from, obj.date_ended, summary)
        # return Duration("8:00") * obj.duration


class StatisticalFields(dd.ChoiceList):
    verbose_name = _("ESF field")
    verbose_name_plural = _("ESF fields")
    column_names = 'value name text type'
    item_class = StatisticalField
    required_roles = dd.login_required(dd.SiteStaff)

add = StatisticalFields.add_item_instance

# Séance d'info
add(GuestHoursFixed('10', "S.Inf", _("Informative sessions"),
                    hours_per_guest=Duration('2:00')))

# Entretien individuel
add(GuestHoursFixed('20', "E.Ind", _("Individual consultation")))

# Evaluation formation externe et art.61
add(GuestHoursFixed('21', "E.For", _("Evaluation of external training")))

# S.I.S. agréé
add(GuestHoursFixed('30', "SIS", _("Certified integration service")))

# Tests de niveau
add(GuestHoursFixed('40', "Tst", _("Level tests")))

# Initiation informatique
add(GuestHoursFixed('41', "Info", _("IT basics")))

# Mobilité
add(GuestHoursFixed('42', "Mob", _("Mobility")))

# Remédiation mathématique et français
add(GuestHoursFixed('43', "Rem", _("Remedial teaching")))

# Activons-nous
add(GuestHoursEvent('44', "AN!", _("Wake up!")))

# Mise en situation professionnelle : calculer les heures par stage
# d'immersion, en fonction des dates de début et de fin et de
# l'horaire de travail.
add(ImmersionHours('50', "MSP", _("Getting a professional situation")))

# Cyber-employ : Somme des présences aux ateliers "Cyber-emploi", mais
# pour ces ateliers on note les heures d'arrivée et de départ par
# participation.
add(GuestHoursEvent('60', "CyE", _("Cyber Job")))

# Mise à l’emploi sous contrat art.60§7
add(Art60Hours('70', "60§7", _("Art 60§7 job supplyment")))


@dd.receiver(dd.pre_analyze)
def inject_statistical_fields(sender, **kw):
    for sf in StatisticalFields.items():
        if sf.field_name is not None:
            dd.inject_field('esf.ClientSummary', sf.field_name, sf.field)

dd.inject_field(
    'cal.EventType', 'esf_field', StatisticalFields.field(blank=True))
