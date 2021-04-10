# -*- coding: UTF-8 -*-
# Copyright 2008-2021 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

"""Choicelists for `lino_welfare.modlib.pcsw`.

"""

from lino.modlib.system.choicelists import ObservedEvent
from lino.api import dd, _

from lino_xl.lib.clients.choicelists import ClientEvents

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


# class ClientStates(dd.Workflow):
#     required_roles = dd.login_required(SocialStaff)
#     verbose_name_plural = _("Client states")

# add = ClientStates.add_item
# add('10', _("Newcomer"), 'newcomer', help_text=u"""\
# Klient hat Antrag auf Hilfe eingereicht,
# der jedoch noch nicht genehmigt wurde
# oder es wurde noch kein Sachbearbeiter oder Sozi zur Begleitung zugewiesen.
# (TIM: Attribut "N" (Neuantrag) gesetzt)""")  # "N" in PAR->Attrib
#     #~ required=dict(states=['refused','coached'],user_groups='newcomers'))
# add('20', _("Refused"), 'refused', help_text=u"""\
# Alle bisherigen Hilfsanträge wurden abgelehnt.
# (TIM kennt diesen Aktenzustand nicht)""")
# # coached: neither newcomer nor former, IdPrt != "I"
# add('30', _("Coached"), 'coached', help_text=u"""\
# Es gibt mindestens eine Person im ÖSHZ, die sich um die Person kümmert.
# (TIM: IdPrt == "S" und Attribut N (Neuantrag) nicht gesetzt)""")

# add('50', _("Former"), 'former', help_text=u"""\
# War mal begleitet, ist es aber jetzt nicht mehr.
# Es existiert keine *aktive* Begleitung.
# (TIM: Attribut `W (Warnung bei Auswahl)` oder Partnerart `I (Inaktive)`)""")

# #~ add('60', _("Invalid"),'invalid',help_text=u"""\
# #~ Klient ist laut TIM weder Ehemalig noch Neuantrag, hat aber keine gültige NISS.""")


class RefusalReasons(dd.ChoiceList):
    verbose_name = _("Refusal reason")
    verbose_name_plural = _("Refusal reasons")

add = RefusalReasons.add_item
add('10', _("Information request (No coaching needed)"))
add('20', _("PCSW is not competent"))
add('30', _("Client did not return"))
