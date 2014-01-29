# -*- coding: UTF-8 -*-
# Copyright 2014 Luc Saffre
# This file is part of the Lino-Welfare project.
# Lino-Welfare is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
# Lino-Welfare is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with Lino-Welfare; if not, see <http://www.gnu.org/licenses/>.
"""
The :xfile:`models.py` file for :mod:`lino_welfare.modlib.aids`.
"""

from __future__ import unicode_literals

import logging
logger = logging.getLogger(__name__)

import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _

from lino import dd
from django.conf import settings


attestations = dd.resolve_app('attestations')


class Category(dd.BabelNamed):

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")


class Categories(dd.Table):
    model = 'aids.Category'
    required = dd.required(user_level='admin', user_groups='office')
    column_names = 'name *'
    order_by = ["name"]

    insert_layout = """
    id name
    """

    detail_layout = """
    id name
    aids.AidsByCategory
    """


class Decider(dd.BabelNamed):

    class Meta:
        verbose_name = _("Decider")
        verbose_name_plural = _("Deciders")


class Deciders(dd.Table):
    model = 'aids.Decider'
    required = dd.required(user_level='admin', user_groups='office')
    column_names = 'name *'
    order_by = ["name"]

    insert_layout = """
    id name
    """

    detail_layout = """
    id name
    aids.AidsByDecider
    """


class AidType(dd.BabelNamed, dd.PrintableType):

    templates_group = 'aids/Aid'

    class Meta:
        verbose_name = _("Aid Type")
        verbose_name_plural = _("Aid Types")

    remark = models.TextField(verbose_name=_("Remark"), blank=True)


class AidTypes(dd.Table):

    """
    Displays all rows of :class:`AidType`.
    """
    model = 'aids.AidType'
    required = dd.required(user_level='admin', user_groups='office')
    column_names = 'name build_method template *'
    order_by = ["name"]

    insert_layout = """
    name
    build_method
    """

    detail_layout = """
    id name
    build_method template
    aids.AidsByType
    """


class Aid(dd.ProjectRelated, attestations.Attestable):

    """
    Deserves more documentation.
    """

    class Meta:
        abstract = settings.SITE.is_abstract_model('aids.Aid')
        verbose_name = _("Aid")
        verbose_name_plural = _("Aids")

    decided_date = models.DateField(
        verbose_name=_('Decided'), default=datetime.date.today)
    decider = models.ForeignKey(Decider, blank=True, null=True)
    applies_from = models.DateField(
        verbose_name=_('Applies from'),
        default=datetime.date.today)
    applies_until = models.DateField(
        verbose_name=_('Applies until'),
        default=datetime.date.today)

    type = models.ForeignKey('aids.AidType')
    category = models.ForeignKey('aids.Category', blank=True, null=True)

    amount = dd.PriceField(_("Amount"), blank=True, null=True)

    def __unicode__(self):
        return '%s #%s' % (self._meta.verbose_name, self.pk)

    def get_mailable_type(self):
        return self.type


class AidDetail(dd.FormLayout):
    main = """
    id project type:25 category
    decider decided_date:10 applies_from applies_until
    outbox.MailsByController
    """


class Aids(dd.Table):
    required = dd.required(user_groups='office', user_level='admin')

    model = 'aids.Aid'
    detail_layout = AidDetail()
    column_names = "id decided_date type project"
    order_by = ["id"]


class AidsByX(Aids):
    required = dd.required(user_groups='office')
    column_names = "decided_date type category *"
    order_by = ["-decided_date"]


class AidsByType(AidsByX):
    master_key = 'type'


if settings.SITE.project_model is not None:

    class AidsByProject(AidsByX):
        master_key = 'project'


class AidsByDecider(AidsByX):
    master_key = 'decider'


class AidsByCategory(AidsByX):
    master_key = 'category'


system = dd.resolve_app('system')

MODULE_LABEL = dd.apps.aids.verbose_name


# def setup_main_menu(site, ui, profile, m):
#     m = m.add_menu("aids", MODULE_LABEL)
#     m.add_action('aids.Aids')


def setup_config_menu(site, ui, profile, m):
    #~ m  = m.add_menu("aids",_("~Aids"))
    m = m.add_menu("aids", MODULE_LABEL)
    m.add_action('aids.AidTypes')


def setup_explorer_menu(site, ui, profile, m):
    m = m.add_menu("aids", MODULE_LABEL)
    m.add_action('aids.Aids')

