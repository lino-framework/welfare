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
import types

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import pgettext_lazy as pgettext

from lino import dd
from lino.utils.xmlgen.html import E
from django.conf import settings


contacts = dd.resolve_app('contacts')
boards = dd.resolve_app('boards')


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
    aids.ConfirmationsByCategory
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

    board = models.ForeignKey('boards.Board', blank=True, null=True)

    def get_long_name(self):
        return dd.babelattr(self, 'long_name') or unicode(self)


class AidTypes(dd.Table):
    model = 'aids.AidType'
    required = dd.required(user_level='admin', user_groups='office')
    column_names = 'aid_regime name board *'
    order_by = ["aid_regime", "name"]

    insert_layout = """
    name board
    long_name
    """

    detail_layout = """
    id aid_regime board
    name
    long_name
    aids.ConfirmationsByType
    """


class ConfirmationStates(dd.Workflow):
    required = dd.required(user_level='admin')
    verbose_name_plural = _("Income Confirmation states")

add = ConfirmationStates.add_item
add('01', _("Requested"), 'requested')
add('02', _("Signed"), 'signed')
add('03', _("Cancelled"), 'cancelled')


class SignConfirmation(dd.Action):
    label = _("Sign")
    show_in_workflow = True

    # icon_name = 'flag_green'
    required = dd.required(states="requested")
    help_text = _("You confirm that this income confirmation is correct.")

    def get_action_permission(self, ar, obj, state):
        if obj.signer is not None and obj.signer != ar.get_user():
            return False
        return super(SignConfirmation,
                     self).get_action_permission(ar, obj, state)

    def run_from_ui(self, ar, **kw):
        obj = ar.selected_rows[0]

        def ok(ar):
            obj.signer = ar.get_user()
            obj.state = ConfirmationStates.signed
            obj.save()
            ar.set_response(refresh=True)
        msg = obj.confirmation_text(ar) or _(
            "(Custom text specified as remark)")
        msg = "%s %s" % (obj.client, msg)
        ar.confirm(ok, msg, _("Are you sure?"))


@dd.receiver(dd.pre_analyze)
def setup_aids_workflows(sender=None, **kw):

    site = sender

    site.modules.aids.Confirmation.sign = SignConfirmation()

    ConfirmationStates.cancelled.add_transition(
        _("Cancel"), states='requested')

    ConfirmationStates.requested.add_transition(
        _("Reopen"), states='signed cancelled')


# class Aid(boards.BoardDecision, dd.DatePeriod):
class Confirmation(dd.UserAuthored, dd.DatePeriod):
    """An Income Confirmation is when a social agent confirms that
    a given Client benefits of a given aid during a given period.

    """

    class Meta:
        abstract = dd.is_abstract_model('aids.Confirmation')
        verbose_name = _("Income confirmation")
        verbose_name_plural = _("Income confirmations")

    allow_cascaded_delete = ['client']
    workflow_state_field = 'state'

    client = models.ForeignKey('pcsw.Client')

    signer = models.ForeignKey(
        settings.SITE.user_model,
        verbose_name=_("Signer"),
        blank=True, null=True,
        related_name="%(app_label)s_%(class)s_set_by_signer",
    )

    state = ConfirmationStates.field(default=ConfirmationStates.requested)

    aid_type = models.ForeignKey('aids.AidType', blank=True, null=True)
    category = models.ForeignKey('aids.Category', blank=True, null=True)

    amount = dd.PriceField(_("Amount"), blank=True, null=True)

    remark = dd.RichTextField(
        _("Remark"),
        blank=True, null=True, format='html')

    def __unicode__(self):
        return '%s #%s' % (self._meta.verbose_name, self.pk)

    def get_mailable_type(self):
        return self.aid_type

    def save(self, *args, **kwargs):
        logger.info("20140724 %s", self.client)
        if self.signer is None:
            self.signer = self.client.get_primary_coach()
        super(Confirmation, self).save(*args, **kwargs)

    @dd.chooser()
    def aid_type_choices(self):
        M = dd.resolve_model('aids.AidType')
        # logger.info("20140331 %s", aid_regime)
        return M.objects.filter(aid_regime=AidRegimes.financial)

    def get_excerpt_options(self, ar, **kw):
        # Set project field when creating an excerpt from Client.
        kw.update(project=self.client)
        return super(Confirmation, self).get_excerpt_options(ar, **kw)

    # @dd.displayfield(_("Confirmation text"))
    # @dd.virtualfield(dd.HtmlBox(_("Confirmation text")))
    @dd.virtualfield(dd.HtmlBox(""))
    def confirmation_text(self, ar):

        aid = self
        
        def when():
            if aid.start_date:
                yield pgettext("date range", "since")
                yield " "
                yield E.b(dd.fdl(aid.start_date))
            if aid.start_date and aid.end_date:
                yield " "
                yield _("and")
            if aid.end_date:
                yield " "
                yield pgettext("date range", "until")
                yield " "
                yield E.b(dd.fdl(self.end_date))

        def what():
            if self.aid_type:
                yield E.b(self.aid_type.get_long_name())
                if self.category:
                    yield " (%s: %s)" % (_("Category"), self.category)
                if self.amount:
                    yield " "
                    yield _("with amount of")
                    # "in Höhe von", "d'un montant de"
                    s = " %s €" % self.amount
                    s += "/%s" % _("month")
                    yield E.b(s)

        def e2text(v):
            if isinstance(v, types.GeneratorType):
                return "".join([e2text(x) for x in v])
            if E.iselement(v):
                return E.tostring(v)
            return unicode(v)
            
        kw = dict()
        kw.update(what=e2text(what()))
        kw.update(when=e2text(when()))
        if kw['when'] or kw['what']:
            if self.end_date and self.end_date <= settings.SITE.today():
                s = _("received %(what)s %(when)s.") % kw
            else:
                s = _("receives %(what)s %(when)s.") % kw
        else:
            return ''
        return s

        
dd.update_field(Confirmation, 'start_date', verbose_name=_('Period from'))
dd.update_field(Confirmation, 'end_date', verbose_name=_('until'))
dd.update_field(Confirmation, 'user', verbose_name=_('Requested by'))


class Confirmations(dd.Table):
    required = dd.required(user_groups='office', user_level='admin')

    model = 'aids.Confirmation'

    detail_layout = dd.FormLayout("""
    id client user
    aid_type:25 start_date end_date
    category amount
    confirmation_text
    signer workflow_buttons
    remark
    """, window_size=(70, 24))

    column_names = "id client user signer aid_type category \
    start_date end_date *"
    order_by = ["-id"]

    parameters = dict(
        user=dd.ForeignKey(
            settings.SITE.user_model,
            verbose_name=_("Requested by"),
            blank=True, null=True,
            help_text=_("Only rows requested by this user.")),
        signer=dd.ForeignKey(
            settings.SITE.user_model,
            verbose_name=_("Signer"),
            blank=True, null=True,
            help_text=_("Only rows signed (or to be signed) by this user.")),
        state=ConfirmationStates.field(
            blank=True,
            help_text=_("Only rows having this state.")))

    params_layout = "user signer state"

    @classmethod
    def get_request_queryset(self, ar):
        qs = super(Confirmations, self).get_request_queryset(ar)
        pv = ar.param_values
        if pv.signer:
            qs = qs.filter(signer=pv.signer)
        if pv.user:
            qs = qs.filter(user=pv.user)
        if pv.state:
            qs = qs.filter(state=pv.state)
        return qs

    @classmethod
    def get_title_tags(self, ar):
        for t in super(Confirmations, self).get_title_tags(ar):
            yield t
        pv = ar.param_values

        for k in ('signer', 'user'):
            v = pv[k]
            if v:
                yield unicode(self.parameters[k].verbose_name) \
                    + ' ' + unicode(v)




class ConfirmationsByX(Confirmations):
    required = dd.required(user_groups='office')
    column_names = "start_date end_date aid_type category amount workflow_buttons *"
    order_by = ["-start_date"]
    auto_fit_column_widths = True


class ConfirmationsByClient(ConfirmationsByX):

    master_key = 'client'

    insert_layout = dd.FormLayout("""
    aid_type
    start_date end_date
    remark
    """, window_size=(50, 14))
    column_names = "aid_type start_date end_date signer workflow_buttons *"
    stay_in_grid = True


class ConfirmationsByCategory(ConfirmationsByX):
    master_key = 'category'


class ConfirmationsByType(ConfirmationsByX):
    master_key = 'aid_type'
    column_names = "client start_date end_date category amount *"


class ConfirmationsToSign(Confirmations):
    label = _("Aid confirmations to sign")
    column_names = "user aid_type client start_date end_date amount \
    workflow_buttons"

    @classmethod
    def param_defaults(self, ar, **kw):
        kw = super(ConfirmationsToSign, self).param_defaults(ar, **kw)
        kw.update(signer=ar.get_user())
        kw.update(state=ConfirmationStates.requested)
        return kw

##
##
##
##
##


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

    aid = models.ForeignKey('aids.Confirmation')
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


##
##
##
##
##


def setup_main_menu(site, ui, profile, m):
    app = dd.apps.reception
    m = m.add_menu(app.app_name, app.verbose_name)
    m.add_action('aids.ConfirmationsToSign')


def setup_config_menu(site, ui, profile, m):
    app = dd.apps.reception
    m = m.add_menu(app.app_name, app.verbose_name)
    m.add_action('aids.AidTypes')
    m.add_action('aids.Categories')


def setup_explorer_menu(site, ui, profile, m):
    app = dd.apps.reception
    m = m.add_menu(app.app_name, app.verbose_name)
    m.add_action('aids.Confirmations')
    m.add_action('aids.AidRegimes')
    m.add_action('aids.Helpers')
    m.add_action('aids.HelperRoles')
