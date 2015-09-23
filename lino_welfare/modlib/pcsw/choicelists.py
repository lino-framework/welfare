# -*- coding: UTF-8 -*-
# Copyright 2008-2015 Luc Saffre
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

"""Choicelists for `lino_welfare.modlib.pcsw`.

"""

from __future__ import unicode_literals
from __future__ import print_function

import logging
logger = logging.getLogger(__name__)

from django.db.models import Count

from lino.mixins.periods import ObservedEvent
from lino.api import dd, _

from .utils import only_coached_on, has_contracts_filter
from .roles import SocialStaff


class CivilState(dd.ChoiceList):

    """
    Civil states, using Belgian codes.
    
    """
    required_roles = dd.required(SocialStaff)
    verbose_name = _("Civil state")
    verbose_name_plural = _("Civil states")

    @classmethod
    def old2new(cls, old):  # was used for migrating to 1.4...
        if old == '1':
            return cls.single
        if old == '2':
            return cls.married
        if old == '3':
            return cls.divorced
        if old == '4':
            return cls.widowed
        if old == '5':
            return cls.separated
        return ''

add = CivilState.add_item
add('10', _("Single"), 'single')
add('13', _("Single cohabitating"))
add('18', _("Single with child"))
add('20', _("Married"), 'married')
add('21', _("Married (living alone)"))
add('22', _("Married (living with another partner)"))
add('30', _("Widowed"), 'widowed')
add('33', _("Widow cohabitating"))
add('40', _("Divorced"), 'divorced')
add('50', _("Separated"), 'separated')  # Getrennt von Tisch und Bett /


#~ '10', 'Célibataire', 'Ongehuwd', 'ledig'
#~ '13', 'Célibataire cohab.', NULL, 'ledig mit zus.',
#~ '18', 'Célibataire avec enf', NULL, 'ledig mit kind',
#~ '20', 'Marié', 'Gehuwd', 'verheiratet',
#~ '21', 'Séparé de fait', NULL, 'verheiratet alleine',
#~ '22', 'Séparé de fait cohab', NULL, 'verheiratet zus.',
#~ '30', 'Veuf(ve)', NULL, 'Witwe(r)',
#~ '33', 'Veuf(ve) cohab.', NULL, 'Witwe(r) zus.',
#~ '40', 'Divorcé', NULL, 'geschieden',
#~ '50', 'séparé(e) de corps', NULL, 'von Tisch & Bet get.',


# http://en.wikipedia.org/wiki/European_driving_licence
class ResidenceType(dd.ChoiceList):

    """
    Types of registries for the Belgian residence.
    
    """
    verbose_name = _("Residence type")

add = ResidenceType.add_item
# Bevölkerungsregister registre de la population
add('1', _("Registry of citizens"))
# Fremdenregister        Registre des étrangers      vreemdelingenregister
add('2', _("Registry of foreigners"))
add('3', _("Waiting for registry"))    # Warteregister


class ClientEvents(dd.ChoiceList):
    """A choicelist of observable client events.

    """
    verbose_name = _("Observed event")
    verbose_name_plural = _("Observed events")
    max_length = 50


# class ClientIsActive(ObservedEvent):
#     text = _("Active")

#     def add_filter(self, qs, pv):
#         period = (pv.start_date, pv.end_date)
#         qs = only_coached_on(qs, period)
#         return qs

# ClientEvents.add_item_instance(ClientIsActive("active"))


class ClientHasCoaching(ObservedEvent):
    text = _("Coaching")

    def add_filter(self, qs, pv):
        period = (pv.start_date, pv.end_date)
        qs = only_coached_on(qs, period)
        return qs

ClientEvents.add_item_instance(ClientHasCoaching("active"))


class ClientCreated(ObservedEvent):
    """The choice for :class:`ClientEvents` which
    selects clients whose record has been *created* during the observed
    period.
    """
    text = _("Created")

    def add_filter(self, qs, pv):
        if pv.start_date:
            qs = qs.filter(created__gte=pv.start_date)
        if pv.end_date:
            qs = qs.filter(created__lte=pv.end_date)
        return qs

ClientEvents.add_item_instance(ClientCreated("created"))


class ClientModified(ObservedEvent):
    """The choice for :class:`ClientEvents` which selects clients whose
    main record has been *modified* during the observed period.

    """
    text = _("Modified")

    def add_filter(self, qs, pv):
        if pv.start_date:
            qs = qs.filter(modified__gte=pv.start_date)
        if pv.end_date:
            qs = qs.filter(modified__lte=pv.end_date)
        return qs

ClientEvents.add_item_instance(ClientModified("modified"))


class ClientHasDispense(ObservedEvent):
    text = _("Dispense")

    def add_filter(self, qs, pv):
        qs = qs.filter(
            dispense__end_date__gte=pv.start_date,
            dispense__start_date__lte=pv.end_date).distinct()
        return qs

ClientEvents.add_item_instance(ClientHasDispense("dispense"))


class ClientHasPenalty(ObservedEvent):
    text = _("Penalty")

    def add_filter(self, qs, pv):
        qs = qs.filter(
            dispense__end_date__gte=pv.start_date,
            dispense__start_date__lte=pv.end_date).distinct()
        return qs

ClientEvents.add_item_instance(ClientHasPenalty("penalty"))


class ClientHasNote(ObservedEvent):
    text = _("Note")

    def add_filter(self, qs, pv):
        if pv.start_date:
            qs = qs.filter(
                notes_note_set_by_project__date__gte=pv.start_date)
        if pv.end_date:
            qs = qs.filter(
                notes_note_set_by_project__date__lte=pv.end_date)
        qs = qs.annotate(num_notes=Count('notes_note_set_by_project'))
        qs = qs.filter(num_notes__gt=0)
        # print(20150519, qs.query)
        return qs

ClientEvents.add_item_instance(ClientHasNote("note"))


# elif ce == ClientEvents.dispense:
#     qs = qs.filter(
#         dispense__end_date__gte=period[0],
#         dispense__start_date__lte=period[1]).distinct()
# elif ce == ClientEvents.created:
#     qs = qs.filter(
#         created__gte=datetime.datetime.combine(
#             period[0], datetime.time()),
#         created__lte=datetime.datetime.combine(
#             period[1], datetime.time()))
#     #~ print 20130527, qs.query
# elif ce == ClientEvents.modified:
#     qs = qs.filter(
#         modified__gte=datetime.datetime.combine(
#             period[0], datetime.time()),
#         modified__lte=datetime.datetime.combine(
#             period[1], datetime.time()))
# elif ce == ClientEvents.penalty:
#     qs = qs.filter(
#         exclusion__excluded_until__gte=period[0],
#         exclusion__excluded_from__lte=period[1]).distinct()
# elif ce == ClientEvents.note:
#     qs = qs.filter(
#         notes_note_set_by_project__date__gte=period[0],
#         notes_note_set_by_project__date__lte=period[1]).distinct()


# add = ClientEvents.add_item
# add('10', _("Active"), 'active')
# add('20', _("ISIP"), 'isip')
# add('21', _("Art60§7 job supplyment"), 'jobs')
# add('22', _("Dispense"), 'dispense')
# if dd.is_installed('immersion'):
#     add('23', _("Immersion training"), 'immersion')
# if dd.is_installed('art61'):
#     add('24', _("Art61 job supplyment"), 'art61')
# add('30', _("Penalty"), 'penalty')
# add('31', _("Exclusion"), 'exclusion')
# add('40', _("Note"), 'note')
# add('50', _("Created"), 'created')
# add('60', _("Modified"), 'modified')
# add('70', _("Available"), 'available')


class ClientStates(dd.Workflow):
    required_roles = dd.required(SocialStaff)
    verbose_name_plural = _("Client states")

add = ClientStates.add_item
add('10', _("Newcomer"), 'newcomer', help_text=u"""\
Klient hat Antrag auf Hilfe eingereicht,
der jedoch noch nicht genehmigt wurde
oder es wurde noch kein Sachbearbeiter oder Sozi zur Begleitung zugewiesen.
(TIM: Attribut "N" (Neuantrag) gesetzt)""")  # "N" in PAR->Attrib
    #~ required=dict(states=['refused','coached'],user_groups='newcomers'))
add('20', _("Refused"), 'refused', help_text=u"""\
Alle bisherigen Hilfsanträge wurden abgelehnt.
(TIM kennt diesen Aktenzustand nicht)""")
# coached: neither newcomer nor former, IdPrt != "I"
add('30', _("Coached"), 'coached', help_text=u"""\
Es gibt mindestens eine Person im ÖSHZ, die sich um die Person kümmert.
(TIM: IdPrt == "S" und Attribut N (Neuantrag) nicht gesetzt)""")

add('50', _("Former"), 'former', help_text=u"""\
War mal begleitet, ist es aber jetzt nicht mehr.
Es existiert keine *aktive* Begleitung.
(TIM: Attribut `W (Warnung bei Auswahl)` oder Partnerart `I (Inaktive)`)""")

#~ add('60', _("Invalid"),'invalid',help_text=u"""\
#~ Klient ist laut TIM weder Ehemalig noch Neuantrag, hat aber keine gültige NISS.""")


class RefusalReasons(dd.ChoiceList):
    verbose_name = _("Refusal reason")
    verbose_name_plural = _("Refusal reasons")

add = RefusalReasons.add_item
add('10', _("Information request (No coaching needed)"))
add('20', _("PCSW is not competent"))
add('30', _("Client did not return"))

