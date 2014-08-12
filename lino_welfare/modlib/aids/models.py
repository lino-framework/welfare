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
pcsw = dd.resolve_app('pcsw')


class ConfirmationType(dd.Choice):

    def __init__(self, model, table_class):
        self.table_class = table_class
        model = dd.resolve_model(model)
        self.model = model
        value = dd.full_model_name(model)
        text = model._meta.verbose_name + ' (%s)' % dd.full_model_name(model)
        name = None
        super(ConfirmationType, self).__init__(value, text, name)

    def get_aidtypes(self):
        return AidType.objects.filter(confirmation_type=self)


class ConfirmationTypes(dd.ChoiceList):
    item_class = ConfirmationType
    max_length = 100
    verbose_name = _("Aid confirmation types")

    @classmethod
    def get_for_model(self, model):
        for o in self.objects():
            if o.model is model:
                return o

    @classmethod
    def add_item(cls, model, table_class):
        return cls.add_item_instance(ConfirmationType(model, table_class))


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
    aids.IncomeConfirmationsByCategory
    """


class AidType(dd.BabelNamed):

    # templates_group = 'aids/Aid'

    class Meta:
        verbose_name = _("Aid Type")
        verbose_name_plural = _("Aid Types")

    aid_regime = AidRegimes.field(default=AidRegimes.financial)

    confirmation_type = ConfirmationTypes.field()

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
    verbose_name_plural = _("Aid confirmation states")

add = ConfirmationStates.add_item
add('01', _("Requested"), 'requested')
add('02', _("Signed"), 'signed')
add('03', _("Cancelled"), 'cancelled')


class SignConfirmation(dd.Action):
    label = _("Sign")
    show_in_workflow = True

    # icon_name = 'flag_green'
    required = dd.required(states="requested")
    help_text = _("You confirm that this aid confirmation is correct.")

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


##
## Confirmation
##

class Confirmation(boards.BoardDecision, dd.DatePeriod, dd.Created):
    class Meta:
        abstract = dd.is_abstract_model('aids.Confirmation')
        verbose_name = _("Aid confirmation")
        verbose_name_plural = _("Aid confirmations")

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

    aid_type = models.ForeignKey('aids.AidType')

    remark = dd.RichTextField(
        _("Remark"),
        blank=True, null=True, format='html')

    def __unicode__(self):
        return '%s #%s' % (self._meta.verbose_name, self.pk)

    def get_mailable_type(self):
        return self.aid_type

    def save(self, *args, **kwargs):
        # logger.info("20140724 %s", self.client)
        if self.signer is None:
            self.signer = self.client.get_primary_coach()
        super(Confirmation, self).save(*args, **kwargs)

    @dd.chooser()
    def aid_type_choices(cls):
        return cls.get_aid_types()

    @classmethod
    def get_aid_types(cls):
        ct = ConfirmationTypes.get_by_value(dd.full_model_name(cls))
        # logger.info("20140811 get_aid_types %s", cls)
        return dd.modules.aids.AidType.objects.filter(confirmation_type=ct)

    def get_excerpt_options(self, ar, **kw):
        # Set project field when creating an excerpt from Client.
        kw.update(project=self.client)
        return super(Confirmation, self).get_excerpt_options(ar, **kw)

    def get_mti_child(self):
        if self.aid_type_id is not None:
            M = self.aid_type.confirmation_type.model
            try:
                return M.objects.get(id=self.id)
            except M.DoesNotExist:
                logger.warning(
                    "No mti child %s in %s", self.id, M.objects.all().query)

    @dd.displayfield(_("Information"))
    def info(self, ar):
        mc = self.get_mti_child()
        if mc is None:
            return ar.obj2html(self)
        return ar.obj2html(mc)

    @dd.virtualfield(dd.HtmlBox(""))
    def confirmation_text(self, ar):
        mc = self.get_mti_child()
        if mc is None:
            return unicode(self)
        return mc.my_confirmation_text(ar)

    @dd.virtualfield(dd.HtmlBox(""))
    def my_confirmation_text(self, ar):

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

        def e2text(v):
            if isinstance(v, types.GeneratorType):
                return "".join([e2text(x) for x in v])
            if E.iselement(v):
                return E.tostring(v)
            return unicode(v)
            
        kw = dict()
        kw.update(what=e2text(self.confirmation_text_what(ar)))
        kw.update(when=e2text(when()))
        if kw['when'] or kw['what']:
            if self.end_date and self.end_date <= settings.SITE.today():
                s = _("received %(what)s %(when)s.") % kw
            else:
                s = _("receives %(what)s %(when)s.") % kw
        else:
            return ''
        return s

    def confirmation_text_what(self, ar):
        yield E.b(self.aid_type.get_long_name())

dd.update_field(Confirmation, 'start_date', verbose_name=_('Period from'))
dd.update_field(Confirmation, 'end_date', verbose_name=_('until'))
dd.update_field(Confirmation, 'user', verbose_name=_('Requested by'))


class Confirmations(dd.Table):
    model = 'aids.Confirmation'
    required = dd.required(user_groups='office', user_level='admin')

    order_by = ["-id"]

    # detail_layout = dd.FormLayout("""
    # id client user
    # aid_type:25 start_date end_date
    # board decision_date signer workflow_buttons
    # info
    # remark
    # """, window_size=(70, 24))

    # insert_layout = dd.FormLayout("""
    # aid_type
    # start_date end_date
    # remark
    # """, window_size=(50, 14))

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
    order_by = ["-created"]
    auto_fit_column_widths = True


class ConfirmationsByClient(ConfirmationsByX):

    master_key = 'client'
    column_names = "info created_natural signer workflow_buttons *"
    # stay_in_grid = True
    allow_create = False


class ConfirmationsByType(ConfirmationsByX):
    master_key = 'aid_type'
    column_names = "client start_date end_date *"


class ConfirmationsToSign(Confirmations):
    label = _("Aid confirmations to sign")
    column_names = "user aid_type client start_date end_date \
    workflow_buttons"

    @classmethod
    def param_defaults(self, ar, **kw):
        kw = super(ConfirmationsToSign, self).param_defaults(ar, **kw)
        kw.update(signer=ar.get_user())
        kw.update(state=ConfirmationStates.requested)
        return kw


##
## IncomeConfirmation
##

class IncomeConfirmation(Confirmation):
    """This is when a social agent confirms that a client benefits of a
    given income during a given period.

    """

    class Meta:
        abstract = dd.is_abstract_model('aids.IncomeConfirmation')
        verbose_name = _("Income confirmation")
        verbose_name_plural = _("Income confirmations")

    category = models.ForeignKey('aids.Category', blank=True, null=True)

    amount = dd.PriceField(_("Amount"), blank=True, null=True)

    def confirmation_text_what(self, ar):
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


class IncomeConfirmations(Confirmations):
    model = 'aids.IncomeConfirmation'

    detail_layout = dd.FormLayout("""
    id client user
    aid_type:25 start_date end_date
    category amount
    confirmation_text
    board decision_date signer workflow_buttons
    remark
    """, window_size=(70, 24))

    insert_layout = dd.FormLayout("""
    client
    aid_type:25 start_date end_date
    category amount
    remark
    """, window_size=(50, 14))

    column_names = "id client user signer aid_type category \
    start_date end_date *"


class IncomeConfirmationsByCategory(IncomeConfirmations):
    master_key = 'category'

ConfirmationTypes.add_item(IncomeConfirmation, IncomeConfirmations)

##
##
##


class RefundConfirmation(Confirmation):
    """This is when a social agent confirms that a client benefits of a
    refund aid (Kostenrückerstattung) during a given period.

    """

    class Meta:
        abstract = dd.is_abstract_model('aids.RefundConfirmation')
        verbose_name = _("Refund confirmation")
        verbose_name_plural = _("Refund confirmations")


class RefundConfirmations(Confirmations):
    model = 'aids.RefundConfirmation'

    detail_layout = dd.FormLayout("""
    id client user
    aid_type:25 start_date end_date
    #client_contact PartnersByConfirmation
    confirmation_text
    board decision_date signer workflow_buttons
    remark
    """, window_size=(70, 24))

    insert_layout = dd.FormLayout("""
    client
    aid_type:25 start_date end_date
    remark
    """, window_size=(50, 14))

    column_names = "id client user signer aid_type  \
    start_date end_date *"


ConfirmationTypes.add_item(RefundConfirmation, RefundConfirmations)


class SimpleConfirmation(Confirmation):
    """This is when a social agent confirms that a client benefits of some
simple aid during a given period.

    """

    class Meta:
        abstract = dd.is_abstract_model('aids.SimpleConfirmation')
        verbose_name = _("Simple confirmation")
        verbose_name_plural = _("Simple confirmations")


class SimpleConfirmations(Confirmations):
    model = 'aids.SimpleConfirmation'

    detail_layout = dd.FormLayout("""
    id client user
    aid_type:25 start_date end_date
    confirmation_text
    board decision_date signer workflow_buttons
    remark
    """, window_size=(70, 24))

    insert_layout = dd.FormLayout("""
    client
    aid_type:25 start_date end_date
    remark
    """, window_size=(50, 14))

    column_names = "id client user signer aid_type  \
    start_date end_date *"


ConfirmationTypes.add_item(SimpleConfirmation, SimpleConfirmations)


class RefundPartner(pcsw.ClientContactBase):

    class Meta:
        verbose_name = _("Refund partner")
        verbose_name_plural = _("Refund partners")

    confirmation = dd.ForeignKey('aids.RefundConfirmation')


class RefundPartners(dd.Table):
    model = "aids.RefundPartner"


class PartnersByConfirmation(RefundPartners):
    master_key = 'confirmation'
    column_names = 'type company contact_person *'

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
    m.add_action('aids.IncomeConfirmations')
    m.add_action('aids.RefundConfirmations')
    m.add_action('aids.SimpleConfirmations')
    m.add_action('aids.RefundPartners')
    # m.add_action('aids.Helpers')
    # m.add_action('aids.HelperRoles')
