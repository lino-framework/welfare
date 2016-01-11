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

"""
"""

from __future__ import unicode_literals
from __future__ import print_function

from django.db import models

from lino.api import dd, _
from lino import mixins

from .choicelists import ParticipationCertificates


class Dossier(mixins.DatePeriod):

    class Meta:
        verbose_name = _("FSE Dossier")
        verbose_name_plural = _("FSE Dossiers")

    client = dd.ForeignKey('pcsw.Client')
    academic_level = dd.ForeignKey('cv.EducationLevel')
    children_at_charge = models.BooleanField(
        _("Children at charge"), default=False)
    certified_handicap = models.BooleanField(
        _("Certified handicap"), default=False)
    other_difficulty = models.BooleanField(
        _("Other difficulty"), default=False)
    result = ParticipationCertificates.field()
    remark = models.CharField(
        _("Remark"),
        blank=True, max_length=200)


class Dossiers(dd.Table):
    model = 'fse.Dossier'


class AllDossiers(Dossiers):
    required_roles = dd.required(dd.SiteStaff)


class DossiersByClient(Dossiers):
    master_key = 'client'
    auto_fit_column_widths = True


