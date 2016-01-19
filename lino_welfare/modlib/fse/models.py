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

from lino_welfare.modlib.integ.roles import IntegrationAgent
from lino.modlib.excerpts.mixins import Certifiable
from .choicelists import ParticipationCertificates, DossierColumns


class Dossier(mixins.DatePeriod, Certifiable):

    class Meta:
        verbose_name = _("FSE Dossier")
        verbose_name_plural = _("FSE Dossiers")

    client = dd.ForeignKey('pcsw.Client')
    education_level = dd.ForeignKey('cv.EducationLevel')
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
    detail_layout = """
    client children_at_charge certified_handicap other_difficulty id
    education_level result remark
    HoursByDossier
    """
    insert_layout = """
    client
    education_level result
    remark
    """


class AllDossiers(Dossiers):
    required_roles = dd.required(dd.SiteStaff)


class DossiersByClient(Dossiers):
    """Lists the FSE dossiers for a given client."""
    master_key = 'client'
    auto_fit_column_widths = True
    column_names = "start_date end_date remark *"
    insert_layout = """
    education_level result
    remark
    """


class HoursByDossier(dd.VirtualTable):
    required_roles = dd.required(IntegrationAgent)
    label = _("Hours by dossier")
    master = 'fse.Dossier'

    slave_grid_format = 'html'

    @classmethod
    def get_data_rows(self, ar):
        if ar is None or ar.master_instance is None or ar.param_values is None:
            return
        pv = ar.param_values
        qs = rt.modules.cal.Guest.objects(
            partner=ar.master_instance,
            event__date__gte=pv.start_date,
            event__date__lte=pv.end_date)
        qs = qs.order_by('event__date')
        for obj in qs:
            hours = 1
            dc = obj.event_type.dossier_column
            obj._sums.collect(dc, hours)
            yield obj

    @dd.virtualfield('pcsw.Coaching.user')
    def user(self, obj, ar):
        return obj

    @dd.requestfield(_("Total"))
    def row_total(self, obj, ar):
        pv = ar.param_values
        return rt.modules.cal.Guests.request(
            partner=ar.master_instance,
            start_date=pv.start_date, end_date=pv.end_date)
        return obj.my_persons


@dd.receiver(dd.post_analyze)
def on_database_ready(sender, **kw):
    """
    Add columns to HoursByDossier from DossierColumns

    This must also be called before each test case.
    """
    self = HoursByDossier
    self.column_names = ''
    for dc in DossierColumns.objects():
        def w(dc):
            def func(self, obj, ar):
                if ar is None:
                    return None
                pv = ar.param_values
                return rt.modules.cal.Guests.request(
                    param_values=dict(
                        partner=ar.master_instance,
                        dossier_column=dc,
                        start_date=pv.start_date, end_date=pv.end_date))
            return func
        vf = dd.RequestField(w(dc), verbose_name=dc.text)
        self.add_virtual_field('FSE' + dc.value, vf)
        self.column_names += ' ' + vf.name

    self.column_names += ' row_total'
    self.clear_handle()  # avoid side effects when running multiple test cases
    settings.SITE.resolve_virtual_fields()


