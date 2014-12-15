# -*- coding: UTF-8 -*-
# Copyright 2014 Luc Saffre
# License: BSD (see file COPYING for details)

"""
The :xfile:`models.py` module for the
:mod:`lino_welfare.modlib.active_job_search` app.

"""

from django.db import models
from django.utils.translation import ugettext_lazy as _

from lino import dd

config = dd.plugins.active_job_search


class Proof(dd.Model):
    
    class Meta:
        verbose_name = _("Proof of search")
        verbose_name_plural = _("Proofs of search")

    client = models.ForeignKey('pcsw.Client')

    date = models.DateField(_("Date"), blank=True, null=True)
    company = models.ForeignKey('contacts.Company', blank=True, null=True)
    spontaneous = models.BooleanField(_("Spontaneous"), default=False)
    response = models.BooleanField(_("Response to offer"), default=False)

    remarks = dd.RichTextField(
        _("Remarks"),
        blank=True, null=True, format='plain')


class Proofs(dd.Table):
    model = 'active_job_search.Proof'
    detail_layout = """
    date client company id
    spontaneous response
    remarks
    """


class ProofsByClient(Proofs):
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


menugroup = dd.plugins.integ


def setup_explorer_menu(site, ui, profile, m):
    m = m.add_menu(menugroup.app_label, menugroup.verbose_name)
    m.add_action('active_job_search.Proofs')
