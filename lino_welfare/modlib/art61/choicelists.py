# -*- coding: UTF-8 -*-
# Copyright 2012-2015 Rumma & Ko Ltd
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

"""
Choicelists for `lino_welfare.modlib.art61`.

Original request:

- Gestion des subsides d'un projet art 61 : 3 nouveaux champs à cocher
  "Activa", "Tutorat" et "Région wallonne". + paramètres pour pouvoir
  filtrer.  Précision: il serait bien d'avoir une ChoiceList
  "Subsidiations" (`art61.Subsidizations`) configurable. Et puis un
  champ à cocher par subsidiation et par contrat. Ce sera l'occasion
  d'implémenter :class:`lino.core.choicelists.MultiChoiceListField`.


.. autosummary::

"""

from __future__ import unicode_literals
from __future__ import print_function

from lino.api import dd, _


class Subsidization(dd.Choice):

    def contract_field_name(self):
        return 'subsidize_' + self.value


class Subsidizations(dd.ChoiceList):
    verbose_name = _("Subsidization")
    verbose_name_plural = _("Subsidizations")
    item_class = Subsidization

add = Subsidizations.add_item
add('10', _("Activa"), 'activa')
add('20', _("Tutorate"), 'tutorat')  # Tutorat: unique en communauté
                                     # francaise. par Ahmed Medhoune
add('30', _("Walloon Region"), 'region')
add('40', _("SINE"), 'sine')
add('50', _("PTP"), 'ptp')


