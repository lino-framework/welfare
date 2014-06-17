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


contacts = dd.resolve_app('contacts')


class AidRegimes(dd.ChoiceList):
    verbose_name = _("Aid Regime")
add = AidRegimes.add_item
add('10', _("Financial aids"), 'financial')
add('20', _("Medical aids"), 'medical')
add('30', _("Other aids"), 'other')


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
    name
    """

    detail_layout = """
    id name
    aids.AidsByDecider
    """


class AidType(dd.BabelNamed):

    # templates_group = 'aids/Aid'

    class Meta:
        verbose_name = _("Aid Type")
        verbose_name_plural = _("Aid Types")

    aid_regime = AidRegimes.field(default=AidRegimes.financial)

    long_name = dd.BabelCharField(
        _("Long name"),
        max_length=200,
        blank=True,
        help_text=_("Replaces the short description in certain places."))

    def get_long_name(self):
        return settings.SITE.babelattr(
            self, 'long_name') or unicode(self)


class AidTypes(dd.Table):

    """
    Displays all rows of :class:`AidType`.
    """
    model = 'aids.AidType'
    required = dd.required(user_level='admin', user_groups='office')
    # column_names = 'aid_regime name build_method template *'
    column_names = 'aid_regime name *'
    order_by = ["aid_regime", "name"]

    insert_layout = """
    name
    long_name
    """

    detail_layout = """
    id aid_regime name
    long_name
    aids.AidsByType
    """


class HelperRole(dd.BabelNamed):

    class Meta:
        verbose_name = _("Helper Role")
        verbose_name_plural = _("Helper Roles")

    aid_regime = AidRegimes.field(default=AidRegimes.medical)


class HelperRoles(dd.Table):
    model = 'aids.HelperRole'


# class Helper(contacts.ContactRelated):
class Helper(dd.Model):

    class Meta:
        verbose_name = _("Helper")
        verbose_name_plural = _("Helpers")

    aid = models.ForeignKey('aids.Aid')
    role = models.ForeignKey('aids.HelperRole')
    # contact_type = models.ForeignKey('pcsw.ClientContactType')
    name = models.CharField(_("Name"), max_length=50, blank=True)
    remark = models.CharField(_("Remark"), max_length=200, blank=True)

    @dd.chooser()
    def role_choices(self, aid):
        M = dd.resolve_model('aids.HelperRole')
        if aid is None:
            return M.objects.all()
        return M.objects.filter(aid_regime=aid.aid_regime)


class Helpers(dd.Table):
    model = 'aids.Helper'


class HelpersByAid(Helpers):
    master_key = 'aid'
    # column_names = 'role company contact_person'
    column_names = 'role name remark'
    auto_fit_column_widths = True


class Aid(dd.Model):
    """An Aid is when the decision has been made that a given Client
    benefits of given type of aid during a given period.

    """

    class Meta:
        abstract = settings.SITE.is_abstract_model('aids.Aid')
        verbose_name = _("Aid")
        verbose_name_plural = _("Aids")

    client = models.ForeignKey('pcsw.Client')
    aid_regime = AidRegimes.field(default=AidRegimes.financial)
    aid_type = models.ForeignKey('aids.AidType')
    decided_date = models.DateField(
        verbose_name=_('Decided'), default=datetime.date.today)
    decider = models.ForeignKey(Decider, blank=True, null=True)
    applies_from = models.DateField(
        verbose_name=_('Applies from'),
        default=datetime.date.today)
    applies_until = models.DateField(
        verbose_name=_('Applies until'),
        default=datetime.date.today)

    category = models.ForeignKey('aids.Category', blank=True, null=True)

    amount = dd.PriceField(_("Amount"), blank=True, null=True)

    def __unicode__(self):
        return '%s #%s' % (self._meta.verbose_name, self.pk)

    def get_mailable_type(self):
        return self.aid_type

    @dd.chooser()
    def aid_type_choices(self, aid_regime):
        M = dd.resolve_model('aids.AidType')
        # logger.info("20140331 %s", aid_regime)
        if aid_regime is None:
            return M.objects.all()
        return M.objects.filter(aid_regime=aid_regime)

    def get_excerpt_options(self, ar, **kw):
        # Set project field when creating an excerpt from Client.
        kw.update(project=self.client)
        return super(Aid, self).get_excerpt_options(ar, **kw)


class AidDetail(dd.FormLayout):
    main = """
    id client aid_regime aid_type:25 category
    decider decided_date:10 applies_from applies_until amount
    aids.HelpersByAid
    """


class Aids(dd.Table):
    required = dd.required(user_groups='office', user_level='admin')

    model = 'aids.Aid'

    insert_layout = """
    client decider
    category aid_type
    """

    detail_layout = AidDetail()
    column_names = "id decided_date aid_type client"
    order_by = ["id"]


class AidsByX(Aids):
    required = dd.required(user_groups='office')
    column_names = "decided_date aid_type category amount *"
    order_by = ["-decided_date"]
    auto_fit_column_widths = True


class AidsByClient(AidsByX):
    """
    Common base for MedicalAidsByClient and FinancialAidsByClient.
    We must define insert_layout for each subclass although they are
    the same. See :blogref:`20140331`.
    """
    
    master_key = 'client'
    _aid_regime = None

    @classmethod
    def get_known_values(self):
        return dict(aid_regime=self._aid_regime)

    @classmethod
    def get_actor_label(self):
        if self._aid_regime is not None:
            return self._aid_regime.text
        return self._label or self.__name__


class MedicalAidsByClient(AidsByClient):
    _aid_regime = AidRegimes.medical

    insert_layout = """
    aid_type category
    applies_from applies_until
    """


class FinancialAidsByClient(AidsByClient):
    _aid_regime = AidRegimes.financial

    insert_layout = """
    aid_type
    category amount
    decider decided_date
    applies_from applies_until
    """

    detail_layout = dd.FormLayout("""
    id client aid_regime
    aid_type:25 category
    decider decided_date:10
    applies_from applies_until amount
    """, window_size=(50, 'auto'))


class AidsByDecider(AidsByX):
    master_key = 'decider'


class AidsByCategory(AidsByX):
    master_key = 'category'


class AidsByType(AidsByX):
    master_key = 'aid_type'


# pcsw = dd.resolve_app('pcsw')

# def setup_main_menu(site, ui, profile, m):
#     m = m.add_menu("aids", MODULE_LABEL)
#     m.add_action('aids.Aids')


def setup_config_menu(site, ui, profile, m):
    MODULE_LABEL = dd.apps.pcsw.verbose_name
    #~ m  = m.add_menu("aids",_("~Aids"))
    m = m.add_menu("pcsw", MODULE_LABEL)
    m.add_action('aids.AidTypes')
    m.add_action('aids.HelperRoles')
    m.add_action('aids.Categories')


def setup_explorer_menu(site, ui, profile, m):
    MODULE_LABEL = dd.apps.pcsw.verbose_name
    m = m.add_menu("pcsw", MODULE_LABEL)
    m.add_action('aids.Aids')
    m.add_action('aids.Helpers')
