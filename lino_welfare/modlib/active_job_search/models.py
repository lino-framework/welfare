# -*- coding: UTF-8 -*-
# Copyright 2014-2017 Rumma & Ko Ltd
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
The :xfile:`models.py` module for the
:mod:`lino_welfare.modlib.active_job_search` app.

"""

from django.db import models
from django.utils.translation import ugettext_lazy as _

from lino.api import dd

from lino_welfare.modlib.integ.roles import IntegrationStaff, IntegUser


class Proof(dd.Model):
    
    class Meta:
        app_label = 'active_job_search'
        verbose_name = _("Proof of search")
        verbose_name_plural = _("Proofs of search")

    client = dd.ForeignKey('pcsw.Client')

    date = models.DateField(_("Date"), blank=True, null=True)
    company = dd.ForeignKey('contacts.Company', blank=True, null=True)
    spontaneous = models.BooleanField(_("Spontaneous"), default=False)
    response = models.BooleanField(_("Response to offer"), default=False)

    remarks = dd.RichTextField(
        _("Remarks"),
        blank=True, null=True, format='plain')


class Proofs(dd.Table):
    required_roles = dd.login_required(IntegrationStaff)
    model = 'active_job_search.Proof'
    detail_layout = """
    date client company id
    spontaneous response
    remarks
    """


class ProofsByClient(Proofs):
    required_roles = dd.login_required(IntegUser)
    master_key = 'client'
    column_names = "date company spontaneous response *"
    auto_fit_column_widths = True


dd.inject_field(
    'pcsw.Client', 'geographic_area',
    models.CharField(
        _("Geographic area"), blank=True, max_length=200,
        help_text=_(
            "The area for which we are seeking a job.")))

dd.inject_field(
    'pcsw.Client', 'child_custody',
    models.TextField(
        _("Child custody"), blank=True,
        help_text=_("Notes concerning child custody.")))


