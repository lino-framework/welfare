# -*- coding: UTF-8 -*-
# Copyright 2011-2019 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

"""Choicelists for `lino_welfare.modlib.cbss`.

"""

from lino.api import dd, _


class RequestStates(dd.Workflow):
    """
    The status of a :class:`CBSSRequest`.
    """
    #~ label = _("State")

add = RequestStates.add_item
#~ add('0',_("New"),'new')
add('10', _("Sent"), 'sent')
# sending failed. no ticket yet. can execute again.
add('20', _("Failed"), 'failed')
add('25', _("Validated"), 'validated')  # only when cbss_live_requests
add('30', _("OK"), 'ok')
add('40', _("Warnings"), 'warnings')  # OK and useable
# there's a ticket, but no usable result. cannot print.
add('50', _("Errors"), 'errors')
#~ add('6',_("Invalid reply"),'invalid')
#~ add('9',_("Fictive"),'fictive')

#~ class Environment(ChoiceList):
    #~ """
    #~ The environment where a :class:`CBSSRequest` is being executed.
    #~ """
    #~ label = _("Environment")
#~ add = Environment.add_item
#~ add('t',_("Test"),'test')
#~ add('a',_("Acceptance"),'acpt')
#~ add('p',_("Production"),'prod')

OK_STATES = (RequestStates.ok, RequestStates.warnings)


class ManageActions(dd.ChoiceList):

    u""" Possible values for the `action` field of a
    :class:`lino_welfare.modlib.cbss.models.ManageAccessRequest`.
    
    
    .. attribute:: REGISTER

      Ce service est sollicité au moment du démarrage de l’enquête
      sociale.  Le CPAS déclare au réseau de la sécurité sociale qu’il
      possède un dossier pour lequel il a l’autorisation (dispositions
      légales et réglementaires) d’obtenir des informations des autres
      institutions en vue de compléter son enquête dans le cadre de
      l’octroi du revenu d’intégration.  Cette déclaration concerne le
      répertoire sectoriel des CPAS à la SmalS-MvM et peut concerner
      plusieurs catégories de personnes : le demandeur, les
      cohabitants et les tiers concernés et ce, pour des finalités
      différentes.

    .. attribute:: UNREGISTER

      L’opération contraire est aussi mise à disposition.

    .. attribute:: LIST

      Il est en plus possible d’obtenir une liste des enregistrements
      dans le répertoire sectoriel des CPAS à la SmalS-MvM ainsi qu’au
      sein du réseau BCSS.
    
    """
    verbose_name = _("Action")

add = ManageActions.add_item
add('1', _("Register"), 'REGISTER')
add('2', _("Unregister"), 'UNREGISTER')
add('3', _("List"), 'LIST')


class QueryRegisters(dd.ChoiceList):
    """Possible values for the `query_register` field of a
    :class:`lino_welfare.modlib.cbss.models.ManageAccessRequest`.

    .. attribute:: PRIMARY

        Query only the primary register.

    .. attribute:: SECONDARY

        Query only the secondary register.

    .. attribute:: ALL

        Query both registers.

    """
    verbose_name = _("Query Register")

add = QueryRegisters.add_item
add('1', _("Primary"), 'PRIMARY')
add('2', _("Secondary"), 'SECONDARY')
add('3', _("All"), 'ALL')


class RequestLanguages(dd.ChoiceList):
    verbose_name = _("Language")
add = RequestLanguages.add_item
add("nl", _("Dutch"), "nl")
add("fr", _("French"), "fr")
add("de", _("German"), "de")
