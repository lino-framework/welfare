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
contacts = dd.require_app_models('contacts')

from lino.modlib.excerpts.mixins import Certifiable


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
    verbose_name = _("Aid confirmation type")
    verbose_name_plural = _("Aid confirmation types")

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

    short_name = models.CharField(max_length=50, blank=True)

    board = models.ForeignKey('boards.Board', blank=True, null=True)

    print_directly = models.BooleanField(_("Print directly"), default=True)

    confirmed_by_primary_coach = models.BooleanField(
        _("Confirmed by primary coach"), default=True)

    def get_long_name(self):
        return dd.babelattr(self, 'long_name') or unicode(self)


class AidTypes(dd.Table):
    model = 'aids.AidType'
    required = dd.required(user_level='admin', user_groups='office')
    column_names = 'aid_regime name board short_name *'
    order_by = ["aid_regime", "name"]

    insert_layout = """
    name board
    long_name
    """

    detail_layout = """
    id short_name aid_regime board
    name
    long_name
    print_directly confirmed_by_primary_coach
    aids.GrantingsByType
    """


class ConfirmationStates(dd.Workflow):
    required = dd.required(user_level='admin')
    verbose_name_plural = _("Aid confirmation states")

add = ConfirmationStates.add_item
add('01', _("Requested"), 'requested')
add('02', _("Confirmed"), 'confirmed')
# add('03', _("Cancelled"), 'cancelled')


class SignConfirmation(dd.Action):
    label = pgettext("aids", "Sign")
    show_in_workflow = True
    show_in_bbar = False

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
            obj.state = ConfirmationStates.confirmed
            obj.save()
            ar.set_response(refresh=True)
        msg = obj.confirmation_text(ar) + obj.remark
        msg = _("You confirm that %(client)s %(text)s") % dict(
            client=obj.client, text=msg)
        ar.confirm(ok, msg, _("Are you sure?"))


@dd.receiver(dd.pre_analyze)
def setup_aids_workflows(sender=None, **kw):

    ConfirmationStates.requested.add_transition(
        _("Revoke"), states='confirmed')


##
## Granting
##

class Granting(boards.BoardDecision, dd.DatePeriod):

    class Meta:
        abstract = dd.is_abstract_model('aids.Granting')
        verbose_name = _("Aid granting")
        verbose_name_plural = _("Aid grantings")

    client = models.ForeignKey('pcsw.Client')

    aid_type = models.ForeignKey('aids.AidType')

    def __unicode__(self):
        if self.aid_type_id is not None:
            t1 = self.aid_type.short_name or unicode(self.aid_type)
            return "%s/%s/%s" % (dd.fds(self.start_date), self.client.id, t1)
            # t1 = "%s (%s)" % (t1, self.client.id)
            # return _('%s since %s') % (
            #     t1, dd.fds(self.start_date))
        return '%s #%s' % (self._meta.verbose_name, self.pk)

    @dd.displayfield(_("Actions"))
    def custom_actions(self, ar, **kw):
        if self.aid_type_id is None:
            return ''
        kv = dict(client=self.client)
        kv.update(granting=self)
        at = self.aid_type
        ct = at.confirmation_type
        sar = ar.spawn(ct.table_class, known_values=kv)
        txt = _("Create %s") % ct.model._meta.verbose_name
        btn = sar.insert_button(txt, icon_name=None)
        return E.div(btn)


    # @dd.chooser()
    # def aid_type_choices(cls):
    #     return cls.get_aid_types()

    # @classmethod
    # def get_aid_types(cls):
    #     ct = ConfirmationTypes.get_by_value(dd.full_model_name(cls))
    #     # logger.info("20140811 get_aid_types %s", cls)
    #     return dd.modules.aids.AidType.objects.filter(confirmation_type=ct)

dd.update_field(Granting, 'start_date',
                verbose_name=_('Applies from'),
                default=dd.today,
                null=False, blank=False)
dd.update_field(Granting, 'end_date', verbose_name=_('until'))
# dd.update_field(Granting, 'user', verbose_name=_('Requested by'))


class Grantings(dd.Table):
    model = 'aids.Granting'
    required = dd.required(user_groups='office', user_level='admin')
    order_by = ['-start_date']

    detail_layout = """
    id client board decision_date
    aid_type start_date end_date custom_actions
    aids.ConfirmationsByGranting
    """

    insert_layout = """
    client
    aid_type
    board decision_date
    start_date end_date
    """

    parameters = dict(
        board=dd.ForeignKey(
            'boards.Board',
            blank=True, null=True,
            help_text=_("Only rows decided by this board.")),
        aid_type=dd.ForeignKey(
            'aids.AidType',
            blank=True, null=True,
            help_text=_("Only confirmations about this aid type.")),
        user=dd.ForeignKey(
            settings.SITE.user_model,
            verbose_name=_("Author"),
            blank=True, null=True,
            help_text=_("Only rows created by this user.")))

    params_layout = "board aid_type user"

    @classmethod
    def get_request_queryset(self, ar):
        qs = super(Grantings, self).get_request_queryset(ar)
        pv = ar.param_values
        if pv.aid_type:
            qs = qs.filter(aid_type=pv.aid_type)
        if pv.board:
            qs = qs.filter(board=pv.board)
        if pv.user:
            qs = qs.filter(user=pv.user)
        return qs

    @classmethod
    def get_title_tags(self, ar):
        for t in super(Grantings, self).get_title_tags(ar):
            yield t
        pv = ar.param_values

        for k in ('board', 'aid_type', 'user'):
            v = pv[k]
            if v:
                yield unicode(self.parameters[k].verbose_name) \
                    + ' ' + unicode(v)


class GrantingsByX(Grantings):
    required = dd.required(user_groups='office')
    auto_fit_column_widths = True


class GrantingsByClient(GrantingsByX):

    master_key = 'client'
    column_names = "description_column start_date end_date " \
                   "board custom_actions *"
    # allow_create = False
    stay_in_grid = True
    # stay_in_grid is not useless here --even though allow_create is
    # False-- because otherwise the actions invoked
    # bycreate_confirmation_buttons would open a detail window.

    # @classmethod
    # def create_buttons(self, client, ar):
    #     # called from pcsw.Client.create_confirmation_buttons
    #     elems = [_("Create an aid confirmation:")]
    #     items = []
    #     kv = dict(client=client)
    #     for ct in ConfirmationTypes.items():
    #         li = [E.b(unicode(ct.model._meta.verbose_name)), ' : ']
    #         for at in AidType.objects.filter(confirmation_type=ct):
    #             kv.update(aid_type=at)
    #             sar = ar.spawn(ct.table_class, known_values=kv)
    #             li += [sar.insert_button(
    #                 at.short_name or unicode(at), icon_name=None), ', ']
    #         items.append(E.li(*li))
    #     elems.append(E.ul(*items))
    #     return E.div(*elems)


class GrantingsByType(GrantingsByX):
    master_key = 'aid_type'
    column_names = "description_column client start_date end_date *"


##
## Confirmation
##

class Confirmation(
        dd.UserAuthored, contacts.ContactRelated,
        dd.DatePeriod, dd.Created, Certifiable):
              
    class Meta:
        abstract = True

    allow_cascaded_delete = ['client']

    client = models.ForeignKey(
        'pcsw.Client',
        related_name="%(app_label)s_%(class)s_set_by_client")
    language = dd.LanguageField()
    granting = models.ForeignKey('aids.Granting', blank=True, null=True)
    remark = dd.RichTextField(
        _("Remark"),
        blank=True, format='html')

    signer = models.ForeignKey(
        settings.SITE.user_model,
        verbose_name=pgettext("aids", "Signer"),
        blank=True, null=True,
        related_name="%(app_label)s_%(class)s_set_by_signer",
    )

    state = ConfirmationStates.field(default=ConfirmationStates.requested)
    workflow_state_field = 'state'

    sign = SignConfirmation()

    def __unicode__(self):
        # if self.granting is not None:
        #     return '%s #%s' % (unicode(self.granting.aid_type), self.pk)
        return '%s #%s' % (self._meta.verbose_name, self.pk)

    def on_create(self, ar):
        if self.client_id and self.granting_id \
           and self.granting.aid_type.confirmed_by_primary_coach:
            self.signer = self.client.get_primary_coach()
        super(Confirmation, self).on_create(ar)
        
    # def get_mailable_type(self):
    #     return self.granting.aid_type

    def get_print_language(self):
        return self.language

    def get_excerpt_options(self, ar, **kw):
        # Set project field when creating an excerpt from Client.
        kw.update(project=self.client)
        return super(Confirmation, self).get_excerpt_options(ar, **kw)

    @dd.displayfield(_("Information"))
    def info(self, ar):
        return ar.obj2html(self)

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

        def e2text(v):
            if isinstance(v, types.GeneratorType):
                return "".join([e2text(x) for x in v])
            if E.iselement(v):
                return E.tostring(v)
            return unicode(v)
            
        kw = dict()
        kw.update(what=e2text(self.confirmation_what(ar)))
        kw.update(when=e2text(when()))
        if kw['when'] or kw['what']:
            if self.end_date and self.end_date <= settings.SITE.today():
                s = _("received %(what)s %(when)s.") % kw
            else:
                s = _("receives %(what)s %(when)s.") % kw
        else:
            return ''
        return s

    def confirmation_what(self, ar):
        if self.granting:
            yield E.b(self.granting.aid_type.get_long_name())


dd.update_field(Confirmation, 'start_date', verbose_name=_('Period from'))
dd.update_field(Confirmation, 'end_date', verbose_name=_('until'))
dd.update_field(Confirmation, 'user', verbose_name=_('Requested by'))
dd.update_field(Confirmation, 'company',
                verbose_name=_("Recipient (Organization)"))
dd.update_field(Confirmation, 'contact_person',
                verbose_name=_("Recipient (Person)"))


class Confirmations(dd.Table):
    model = 'aids.Confirmation'
    required = dd.required(user_groups='office', user_level='admin')
    order_by = ["-created"]

    parameters = dict(
        board=dd.ForeignKey(
            'boards.Board',
            blank=True, null=True,
            help_text=_("Only rows decided by this board.")),
        signer=dd.ForeignKey(
            settings.SITE.user_model,
            verbose_name=_("Signer"),
            blank=True, null=True,
            help_text=_("Only rows confirmed (or to be confirmed) "
                        "by this user.")),
        user=dd.ForeignKey(
            settings.SITE.user_model,
            verbose_name=_("Author"),
            blank=True, null=True,
            help_text=_("Only rows created by this user.")),
        aid_type=dd.ForeignKey(
            'aids.AidType',
            blank=True, null=True,
            help_text=_("Only confirmations about this aid type.")),
        state=ConfirmationStates.field(
            blank=True,
            help_text=_("Only rows having this state.")))

    params_layout = "board signer user aid_type state"

    @classmethod
    def get_request_queryset(self, ar):
        qs = super(Confirmations, self).get_request_queryset(ar)
        pv = ar.param_values
        if pv.signer:
            qs = qs.filter(signer=pv.signer)
        if pv.aid_type:
            qs = qs.filter(granting__aid_type=pv.aid_type)
        if pv.board:
            qs = qs.filter(granting__board=pv.board)
        if pv.state:
            qs = qs.filter(state=pv.state)
        return qs

    @classmethod
    def get_title_tags(self, ar):
        for t in super(Confirmations, self).get_title_tags(ar):
            yield t
        pv = ar.param_values

        for k in ('signer', 'board', 'aid_type', 'state'):
            v = pv[k]
            if v:
                yield unicode(self.parameters[k].verbose_name) \
                    + ' ' + unicode(v)


class ConfirmationsToSign(Confirmations):
    label = _("Aid confirmations to sign")
    column_names = "client granting signer workflow_buttons *"

    @classmethod
    def param_defaults(self, ar, **kw):
        kw = super(ConfirmationsToSign, self).param_defaults(ar, **kw)
        kw.update(signer=ar.get_user())
        kw.update(state=ConfirmationStates.requested)
        return kw


class ConfirmationsByGranting(dd.VirtualTable):
    label = _("Issued confirmations")
    required = dd.required(user_groups='office')
    master = 'aids.Granting'
    master_key = 'granting'
    column_names = "description_column created user printed " \
                   "start_date end_date *"

    @classmethod
    def get_data_rows(self, ar):
        mi = ar.master_instance
        logger.info("20140813 ConfirmationsByGranting %s", mi)
        if mi is None:
            return []
        ct = mi.aid_type.confirmation_type
        return ct.model.objects.filter(granting=mi).order_by()

    @dd.virtualfield('aids.SimpleConfirmation.start_date')
    def start_date(self, obj, ar):
        return obj.start_date

    @dd.virtualfield('aids.SimpleConfirmation.end_date')
    def end_date(self, obj, ar):
        return obj.end_date

    @dd.virtualfield('aids.SimpleConfirmation.created')
    def created(self, obj, ar):
        return obj.created

    @dd.virtualfield('aids.SimpleConfirmation.user')
    def user(self, obj, ar):
        return obj.user

    @dd.displayfield(_('Printed'))
    def printed(self, obj, ar):
        return obj.printed(ar)

    @dd.displayfield(_("Description"))
    def description_column(self, obj, ar):
        return ar.obj2html(obj)


##
## SimpleConfirmation
##


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
    id client signer workflow_buttons
    granting start_date end_date
    confirmation_text
    company contact_person language printed
    remark
    """)  # , window_size=(70, 24))

    insert_layout = dd.FormLayout("""
    client
    granting start_date end_date
    company contact_person language
    remark
    """, window_size=(50, 16))

    column_names = "id client granting start_date end_date *"


ConfirmationTypes.add_item(SimpleConfirmation, SimpleConfirmations)


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

    def confirmation_what(self, ar):
        if self.granting:
            yield E.b(self.granting.aid_type.get_long_name())
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
    client signer workflow_buttons printed
    company contact_person language
    granting:25 start_date end_date
    category amount id
    confirmation_text
    remark
    """)  # , window_size=(70, 24))

    insert_layout = dd.FormLayout("""
    client granting:25
    signer start_date end_date
    category amount
    company contact_person language
    remark
    """, window_size=(70, 20))

    column_names = "id client granting category amount start_date end_date *"


class IncomeConfirmationsByCategory(IncomeConfirmations):
    master_key = 'category'

ConfirmationTypes.add_item(IncomeConfirmation, IncomeConfirmations)

##
##
##


dd.inject_field(
    pcsw.ClientContactType,
    'can_refund',
    models.BooleanField(
        _("Can refund"), default=False,
        help_text=_("")
    ))

pcsw.ClientContactTypes.detail_layout = pcsw.ClientContactTypes.detail_layout.replace('id name', 'id name can_refund')

# class DoctorTypes(dd.ChoiceList):
#     verbose_name = _("Doctor type")
# add = DoctorTypes.add_item
# add('10', _("Family doctor"), 'family')
# add('20', _("Dentist"), 'dentist')
# add('30', _("Pediatrician"), 'pediatrician')


class RefundConfirmation(Confirmation):
    """This is when a social agent confirms that a client benefits of a
    refund aid (Kostenrückerstattung) during a given period.

    """

    class Meta:
        abstract = dd.is_abstract_model('aids.RefundConfirmation')
        verbose_name = _("Refund confirmation")
        verbose_name_plural = _("Refund confirmations")

    urgent = models.BooleanField(_("urgent"), default=False)
    partner_type = dd.ForeignKey(
        'pcsw.ClientContactType', verbose_name=_("Doctor type"))
    # doctor_type = DoctorTypes.field(default=DoctorTypes.family)
    partner = dd.ForeignKey(
        'contacts.Person', verbose_name=_("Doctor"), blank=True)

    @dd.chooser()
    def partner_choices(cls, partner_type):
        return dd.modules.contacts.Partner.objects.filter(
            client_contact_type=partner_type)
    # def on_create(self, ar):
    #     self.doctor = self.client.
    #     super(RefundConfirmation, self).on_create(ar)

    def confirmation_what(self, ar):
        if self.granting:
            yield E.b(self.granting.aid_type.get_long_name())
        yield ". "
        yield _("Recipes issued by")
        yield unicode(self.partner_type)
        yield " "
        yield E.b(unicode(self.partner))


class RefundConfirmations(Confirmations):
    model = 'aids.RefundConfirmation'

    detail_layout = dd.FormLayout("""
    id client signer workflow_buttons
    granting:25 start_date end_date
    partner_type partner urgent
    confirmation_text
    company contact_person language printed
    remark
    """)  # , window_size=(70, 24))

    insert_layout = dd.FormLayout("""
    client
    granting:25 start_date end_date
    partner_type partner urgent
    company contact_person language printed
    remark
    """, window_size=(70, 20))

    column_names = "id client granting start_date end_date *"


ConfirmationTypes.add_item(RefundConfirmation, RefundConfirmations)


##
##
##

class SubmitInsertAndPrint(dd.SubmitInsert):
    """A customized variant of the standard :class:`SubmitInsert
    <dd.SubmitInsert>` which prints the `Confirmation` after
    successful creation.

    """
    def run_from_ui(self, ar, **kw):
        elem = ar.create_instance_from_request()
        self.save_new_instance(ar, elem)
        ar.set_response(close_window=True)
        if elem.granting and elem.granting.aid_type.print_directly:
            elem.do_print.run_from_ui(ar, **kw)

"""
Overrides the :attr:`submit_insert <dd.Model.submit_insert>`
action of :class:`welfare.aids.Confirmation` with
"""
dd.update_model(Confirmation, submit_insert=SubmitInsertAndPrint())


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
    # m.add_action('aids.Helpers')
    # m.add_action('aids.HelperRoles')
