# -*- coding: UTF-8 -*-
# Copyright 2008-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""Choicelists for `lino_welfare.modlib.pcsw`.

"""

from __future__ import unicode_literals
from __future__ import print_function

import logging
logger = logging.getLogger(__name__)

import os
import cgi
import datetime

from django.db import models
from django.db.models import Q
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.utils import translation
from django.contrib.humanize.templatetags.humanize import naturaltime


from lino.api import dd, rt
from lino.core.utils import get_field

from lino.utils.xmlgen.html import E
from lino.modlib.cal.utils import DurationUnits, update_reminder


class CivilState(dd.ChoiceList):

    """
    Civil states, using Belgian codes.
    
    """
    required = dd.required(user_level='admin')
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
    verbose_name = _("Observed event")
    verbose_name_plural = _("Observed events")
add = ClientEvents.add_item
#~ add('10', _("Coached"),'coached')
add('10', _("Active"), 'active')
add('20', _("ISIP"), 'isip')
add('21', _("Art.60§7 contract"), 'jobs')
add('22', _("Dispense"), 'dispense')
if dd.is_installed('trainings'):
    add('23', _("Training"), 'training')
add('30', _("Penalty"), 'penalty')
add('31', _("Exclusion"), 'exclusion')
add('40', _("Note"), 'note')
add('50', _("Created"), 'created')
add('60', _("Modified"), 'modified')
add('70', _("Available"), 'available')


class ClientStates(dd.Workflow):
    required = dd.required(user_level='admin')
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

