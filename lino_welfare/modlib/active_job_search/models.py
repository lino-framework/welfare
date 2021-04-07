# -*- coding: UTF-8 -*-
# Copyright 2014-2017 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

"""
The :xfile:`models.py` module for the
:mod:`lino_welfare.modlib.active_job_search` app.

"""

from django.db import models
from django.utils.translation import gettext_lazy as _

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

# if dd.is_installed('active_job_search'):
    # When executing a py2rst directive under Sphinx, this module has been
    # imported by autodoc even when DJANGO_SETTINGS_MODULE points to some demo
    # project that doesn't use this plugin but has a pcsw plugin.  And in that
    # case, the fields would get added to the Django model and cause a database
    # error when trying to get a pcsw.Client.

    # no longer needed because we simply no longer include the models.py in the
    # autosummary

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
