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

"""Choicelists for `lino_welfare.modlib.fse`.

"""
from __future__ import unicode_literals

from lino.api import dd, _


class ParticipationCertificates(dd.ChoiceList):
    verbose_name = _("Participation Certificate")
    verbose_name_plural = _("Participation Certificates")
add = ParticipationCertificates.add_item
add('10', _("Epreuve d’évaluation réussie sans titre spécifique"))


class DossierColumns(dd.ChoiceList):
    verbose_name = _("Dossier column")
    verbose_name_plural = _("Dossier columns")
add = DossierColumns.add_item
add('10', _("Informative sessions"))
add('20', _("Individual consultation"))
add('21', _("Evaluation session"))
add('30', _("Certified SIS"))
add('40', _("Level test"))
add('41', _("ICT"))
add('42', _("Mobility"))
add('43', _("Math and French"))




