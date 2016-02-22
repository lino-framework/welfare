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
from django.conf import settings

from lino.api import rt, dd, _
from lino import mixins
from lino.utils.xmlgen.html import E
from lino.modlib.summaries.mixins import Summary

from lino_welfare.modlib.integ.roles import IntegrationAgent
from lino_xl.lib.excerpts.mixins import Certifiable
from .choicelists import ParticipationCertificates, StatisticalFields


class ClientSummary(Certifiable, Summary):

    class Meta:
        verbose_name = _("FSE Summary")
        verbose_name_plural = _("FSE Summaries")

    summary_period = 'yearly'

    master = dd.ForeignKey('pcsw.Client')
    education_level = dd.ForeignKey('cv.EducationLevel', blank=True, null=True)
    children_at_charge = models.BooleanField(
        _("Children at charge"), default=False)
    certified_handicap = models.BooleanField(
        _("Certified handicap"), default=False)
    other_difficulty = models.BooleanField(
        _("Other difficulty"), default=False)
    result = ParticipationCertificates.field(blank=True)
    remark = models.CharField(
        _("Remark"),
        blank=True, max_length=200)

    @classmethod
    def get_summary_master_model(cls):
        return rt.modules.pcsw.Client

    @classmethod
    def get_summary_masters(cls):
        return rt.modules.pcsw.Client.objects.filter(has_fse=True)

    def get_summary_collectors(self):
        qs = rt.modules.cal.Guest.objects.all()
        qs = self.add_date_filter(qs, 'event__start_date', partner=self.master)
        yield self.collect_from_guest, qs

    def collect_from_guest(self, obj):
        for sf in StatisticalFields.objects():
            value = sf.collect_value_from_guest(obj)
            if value:
                value += getattr(self, sf.field_name)
                setattr(self, sf.field_name, value)

    @dd.displayfield(_("Results"))
    def results(self, ar):
        if ar is None:
            return
        cells = []
        for sf in StatisticalFields.objects():
            v = getattr(self, sf.field_name)
            cells.append(E.td(
                unicode(sf.text), E.br(), unicode(v), **ar.cellattrs))
        return E.table(E.tr(*cells), **ar.tableattrs)


class Summaries(dd.Table):
    model = 'fse.ClientSummary'
    detail_layout = """
    master year month
    children_at_charge certified_handicap other_difficulty id
    education_level result remark
    results
    """
    insert_layout = """
    master
    education_level result
    remark
    """


class AllSummaries(Summaries):
    required_roles = dd.required(dd.SiteStaff)


class SummariesByClient(Summaries):
    """Lists the FSE summaries for a given client."""
    master_key = 'master'
    auto_fit_column_widths = True
    insert_layout = """
    education_level result
    remark
    """

    @classmethod
    def setup_columns(cls):
        cls.column_names = "year"
        for sf in StatisticalFields.items():
            if sf.field_name is not None:
                cls.column_names += ' ' + sf.field_name
        

dd.inject_field(
    'pcsw.Client', 'has_fse', models.BooleanField(_("FSE data"), default=True))

