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

from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import pgettext_lazy as pgettext

from lino import dd, rt, mixins
from lino.utils.xmlgen.html import E
from lino.utils.ranges import encompass

from lino.modlib.system.mixins import PeriodEvents
from lino.modlib.contacts.utils import parse_name
from lino.modlib.contacts.mixins import ContactRelated
from lino.modlib.excerpts.mixins import Certifiable
from lino.modlib.addresses.mixins import AddressTypes
from lino.mixins.periods import rangefmt

boards = dd.resolve_app('boards')


def e2text(v):
    if isinstance(v, types.GeneratorType):
        return "".join([e2text(x) for x in v])
    if E.iselement(v):
        return E.tostring(v)
    return unicode(v)


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
    def get_column_names(self, ar):
        return 'name value text et_template *'

    @dd.virtualfield(models.CharField(_("Template"), max_length=20))
    def et_template(cls, choice, ar):
        et = rt.modules.excerpts.ExcerptType.get_for_model(choice.model)
        if et:
            return et.template

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


class Category(mixins.BabelNamed):

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


class AidType(ContactRelated, mixins.BabelNamed):

    # templates_group = 'aids/Aid'

    class Meta:
        verbose_name = _("Aid Type")
        verbose_name_plural = _("Aid Types")

    # not used:
    aid_regime = AidRegimes.field(default=AidRegimes.financial)

    confirmation_type = ConfirmationTypes.field(blank=True)

    excerpt_title = dd.BabelCharField(
        _("Excerpt title"),
        max_length=200,
        blank=True,
        help_text=_(
            "The title to be used when printing confirmation excerpts."))

    short_name = models.CharField(max_length=50, blank=True)

    board = models.ForeignKey('boards.Board', blank=True, null=True)

    print_directly = models.BooleanField(_("Print directly"), default=True)

    is_integ_duty = models.BooleanField(
        _("Integration duty"), default=False,
        help_text=_("Whether aid grantings of this type are considered "
                    "as duty for integration contract."))

    is_urgent = models.BooleanField(
        _("Urgent"), default=False,
        help_text=_("Whether aid grantings of this type are considered "
                    "as urgent."))

    confirmed_by_primary_coach = models.BooleanField(
        _("Confirmed by primary coach"), default=True)

    pharmacy_type = dd.ForeignKey(
        'pcsw.ClientContactType', blank=True, null=True)

    address_type = AddressTypes.field(
        blank=True, null=True,
        help_text=_("Which client address to print on confirmations. "
                    "If this is empty, Lino will use the primary address."))

    body_template = models.CharField(
        max_length=200,
        verbose_name=_("Body template"),
        blank=True, help_text="The body template to use instead of the "
        "default body template as defined for the excerpt type.")

    def get_excerpt_title(self):
        return dd.babelattr(self, 'excerpt_title') or unicode(self)

    @dd.chooser(simple_values=True)
    def body_template_choices(cls, confirmation_type):
        if not confirmation_type:
            return []
        tplgroup = confirmation_type.model.get_template_group()
        return settings.SITE.list_templates('.body.html', tplgroup)


class AidTypes(dd.Table):
    model = 'aids.AidType'
    required = dd.required(user_level='admin', user_groups='office')
    column_names = 'name board short_name *'
    order_by = ["name"]

    insert_layout = """
    name
    confirmation_type
    """

    detail_layout = """
    id short_name confirmation_type
    name
    excerpt_title
    print_directly is_integ_duty is_urgent confirmed_by_primary_coach \
    board body_template
    company contact_person contact_role pharmacy_type
    aids.GrantingsByType
    """


class ConfirmationStates(dd.Workflow):
    required = dd.required(user_level='admin')
    verbose_name_plural = _("Aid confirmation states")

add = ConfirmationStates.add_item
add('01', _("Unconfirmed"), 'requested')
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
        d = dict(text=obj.confirmation_text())
        d.update(client=e2text(obj.client.get_full_name(nominative=True)))
        msg = _("You confirm that %(client)s %(text)s") % d
        ar.confirm(ok, msg, _("Are you sure?"))


@dd.receiver(dd.pre_analyze)
def setup_aids_workflows(sender=None, **kw):

    ConfirmationStates.requested.add_transition(
        _("Revoke"), states='confirmed')


class Confirmable(mixins.DatePeriod):
    # base class for Granting and for Confirmation
    class Meta:
        abstract = True

    signer = models.ForeignKey(
        settings.SITE.user_model,
        verbose_name=pgettext("aids", "Signer"),
        blank=True, null=True,
        related_name="%(app_label)s_%(class)s_set_by_signer",
    )

    state = ConfirmationStates.field(default=ConfirmationStates.requested)
    workflow_state_field = 'state'

    sign = SignConfirmation()

    def disabled_fields(self, ar):
        if self.state is ConfirmationStates.requested:
            return set()
        return self.CONFIRMED_FIELDS

    @classmethod
    def on_analyze(cls, site):
        cls.CONFIRMED_FIELDS = dd.fields_list(
            cls,
            cls.get_confirmable_fields())
        super(Confirmable, cls).on_analyze(site)

    @classmethod
    def get_confirmable_fields(cls):
        return ''

    def is_past(self):
        return (self.end_date and self.end_date <= dd.today())

    def get_printable_context(self, **kw):
        kw.update(when=e2text(self.confirmation_when()))
        kw = super(Confirmable, self).get_printable_context(**kw)
        return kw

    def confirmation_text(self):
        kw = dict()
        kw.update(when=e2text(self.confirmation_when()))
        at = self.get_aid_type()
        if at:
            kw.update(what=unicode(at))
        else:
            kw.update(what=unicode(self))
        return _("receives %(what)s %(when)s.") % kw

    def confirmation_address(self):
        at = self.get_aid_type()
        if at and at.address_type:
            addr = self.client.get_address_by_type(at)
        else:
            addr = self.client.get_primary_address()
        if addr is not None:
            return addr.living_at_text()

    def confirmation_when(self):
        if self.start_date and self.end_date:
            yield " "
            if self.start_date == self.end_date:
                s = e2text(E.b(dd.fdl(self.start_date)))
                yield pgettext("date", "on %s") % s
            else:
                kw = dict()
                kw.update(a=e2text(E.b(dd.fdl(self.start_date))))
                kw.update(b=e2text(E.b(dd.fdl(self.end_date))))
                yield pgettext("date range", "between %(a)s and %(b)s") % kw
        elif self.start_date:
            yield pgettext("date range", "from")
            yield " "
            yield E.b(dd.fdl(self.start_date))
        elif self.end_date:
            yield " "
            yield pgettext("date range", "until")
            yield " "
            yield E.b(dd.fdl(self.end_date))

    def get_excerpt_title(self):
        at = self.get_aid_type()
        if at:
            return at.get_excerpt_title()
        return unicode(self)

##
## Granting
##


class GrantingManager(models.Manager):

    def get_by_aidtype(self, client, period, **aidtype_filter):
        at_list = rt.modules.aids.AidType.objects.filter(**aidtype_filter)
        qs = self.get_queryset()
        qs = qs.filter(client=client, aid_type__in=at_list)
        qs = PeriodEvents.active.add_filter(qs, period)
        if qs.count() == 1:
            return qs[0]
        return None


class Granting(Confirmable, boards.BoardDecision):

    class Meta:
        abstract = dd.is_abstract_model(__name__, 'Granting')
        verbose_name = _("Aid granting")
        verbose_name_plural = _("Aid grantings")

    objects = GrantingManager()

    client = models.ForeignKey('pcsw.Client')

    aid_type = models.ForeignKey('aids.AidType')

    def after_ui_create(self, ar):
        super(Granting, self).after_ui_create(ar)
        # dd.logger.info("20141001 %s %s", self.client_id, self.aid_type_id)
        if self.client_id and self.aid_type_id \
           and self.aid_type.confirmed_by_primary_coach:
            self.signer = self.client.get_primary_coach()
        
    def __unicode__(self):
        if self.aid_type_id is not None:
            t1 = self.aid_type.short_name or unicode(self.aid_type)
            return "%s/%s/%s" % (t1, dd.fds(self.start_date), self.client.id)
        return '%s #%s' % (self._meta.verbose_name, self.pk)

    def get_aid_type(self):
        return self.aid_type

    @classmethod
    def get_confirmable_fields(cls):
        return 'client signer aid_type board decision_date start_date end_date'

    @dd.displayfield(_("Actions"))
    def custom_actions(self, ar, **kw):
        if self.aid_type_id is None:
            return ''
        # kv = dict(client=self.client)
        # kv.update(granting=self)
        at = self.aid_type
        ct = at.confirmation_type
        if not ct:
            return ''
        # sar = ar.spawn(ct.table_class, known_values=kv)
        sar = ar.spawn(ct.table_class, master_instance=self)
        txt = _("Create confirmation")
        btn = sar.insert_button(txt, icon_name=None)
        if btn is not None:
            return E.div(btn)

    # def get_long_name(self):
    #     if self.aid_type_id:
    #         return self.aid_type.get_long_name()
    #     return ''


    # @dd.chooser()
    # def aid_type_choices(cls):
    #     return cls.get_aid_types()

    # @classmethod
    # def get_aid_types(cls):
    #     ct = ConfirmationTypes.get_by_value(dd.full_model_name(cls))
    #     # logger.info("20140811 get_aid_types %s", cls)
    #     return rt.modules.aids.AidType.objects.filter(confirmation_type=ct)

dd.update_field(Granting, 'start_date',
                verbose_name=_('Applies from'),
                default=dd.today,
                null=False, blank=False)
dd.update_field(Granting, 'end_date', verbose_name=_('until'))
# dd.update_field(Granting, 'user', verbose_name=_('Requested by'))


class Grantings(dd.Table):
    model = 'aids.Granting'
    required = dd.required(user_groups='office', user_level='admin')
    use_as_default_table = False
    order_by = ['-start_date']

    detail_layout = """
    id client user signer workflow_buttons
    board decision_date
    aid_type start_date end_date custom_actions
    aids.ConfirmationsByGranting
    """

    insert_layout = """
    client
    aid_type signer
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
            help_text=_("Only rows created by this user.")),
        signer=dd.ForeignKey(
            settings.SITE.user_model,
            verbose_name=_("Signer"),
            blank=True, null=True,
            help_text=_("Only rows confirmed (or to be confirmed) "
                        "by this user.")),
        state=ConfirmationStates.field(
            blank=True,
            help_text=_("Only rows having this state.")))

    params_layout = "board aid_type user signer state"

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
        if pv.signer:
            qs = qs.filter(signer=pv.signer)
        if pv.state:
            qs = qs.filter(state=pv.state)
        return qs

    @classmethod
    def get_title_tags(self, ar):
        for t in super(Grantings, self).get_title_tags(ar):
            yield t
        pv = ar.param_values

        for k in ('board', 'aid_type', 'user', 'signer', 'state'):
            v = pv[k]
            if v:
                yield unicode(self.parameters[k].verbose_name) \
                    + ' ' + unicode(v)


class MyPendingGrantings(Grantings):
    required = dd.required(user_groups='coaching')
    column_names = "client aid_type start_date " \
                   "end_date user workflow_buttons *"
    label = _("Grantings to confirm")

    @classmethod
    def get_welcome_messages(cls, ar):
        sar = ar.spawn(cls)
        num = sar.get_total_count()
        if num > 0:
            chunks = [unicode(_("You have %s items in ")) % num]
            # e = E.a(str(num), " ", unicode(cls.label),
            #         href=sar.get_request_url())
            chunks.append(ar.href_to_request(sar, unicode(cls.label)))
            chunks.append('.')
            yield E.span(*chunks)

    @classmethod
    def param_defaults(self, ar, **kw):
        kw = super(MyPendingGrantings, self).param_defaults(ar, **kw)
        kw.update(signer=ar.get_user())
        kw.update(state=ConfirmationStates.requested)
        return kw


class GrantingsByX(Grantings):
    required = dd.required(user_groups='office coaching')
    use_as_default_table = True
    auto_fit_column_widths = True


class GrantingsByClient(GrantingsByX):

    master_key = 'client'
    column_names = "description_column start_date end_date " \
                   "signer workflow_buttons " \
                   "board custom_actions *"
    # allow_create = False
    # stay_in_grid = True
    # stay_in_grid is not useless here --even though allow_create is
    # False-- because otherwise the actions invoked
    # by create_confirmation_buttons would open a detail window.

    insert_layout = """
    aid_type
    board decision_date
    start_date end_date
    """


class GrantingsByType(GrantingsByX):
    master_key = 'aid_type'
    column_names = "description_column client start_date end_date *"


##
## Confirmation
##

class Confirmation(
        Confirmable, mixins.UserAuthored, ContactRelated,
        mixins.Created, Certifiable):
              
    class Meta:
        abstract = True

    allow_cascaded_delete = ['client']

    client = models.ForeignKey(
        'pcsw.Client',
        related_name="%(app_label)s_%(class)s_set_by_client")
    granting = models.ForeignKey('aids.Granting', blank=True, null=True)
    remark = dd.RichTextField(
        _("Remark"),
        blank=True, format='html')

    def __unicode__(self):
        if self.granting is not None:
            return '%s/%s' % (self.granting, self.pk)
        return '%s #%s' % (self._meta.verbose_name, self.pk)

    def full_clean(self):
        super(Confirmation, self).full_clean()
        if self.granting is None:
            return
        gp = self.granting.get_period()
        cp = self.get_period()
        if not encompass(gp, cp):
            msg = _("Date range %(p1)s lies outside of granted "
                    "period %(p2)s.") % dict(p2=rangefmt(gp), p1=rangefmt(cp))
            raise ValidationError(msg)

    def on_create(self, ar):
        if self.granting_id:
            self.signer = self.granting.signer
            self.client = self.granting.client
            # self.language = self.client.language
            if self.granting.aid_type_id:
                at = self.granting.aid_type
                self.company = at.company
                self.contact_person = at.contact_person
                self.contact_role = at.contact_role
        super(Confirmation, self).on_create(ar)
        
    @classmethod
    def get_confirmable_fields(cls):
        return 'client signer granting remark start_date end_date'

    # def get_mailable_type(self):
    #     return self.granting.aid_type

    def get_print_language(self):
        obj = self.recipient
        if obj is not None:
            return obj.language
        return super(Confirmation, self).get_print_language()

    def get_excerpt_options(self, ar, **kw):
        # Set project field when creating an excerpt from Client.
        kw.update(project=self.client)
        return super(Confirmation, self).get_excerpt_options(ar, **kw)

    def get_aid_type(self):
        if self.granting_id and self.granting.aid_type_id:
            return self.granting.aid_type
        return None

    def get_granting(self, **aidtype_filter):
        if self.granting_id:
            return rt.modules.aids.Granting.objects.get_by_aidtype(
                self.granting.client, self, **aidtype_filter)

    def get_urgent_granting(self):
        # used in :xfile:`medical_refund.body.html`
        return self.get_granting(is_urgent=True)

    @classmethod
    def get_template_group(cls):
        # Used by excerpts and printable.  The individual confirmation
        # models use a common tree of templates.
        return 'aids/Confirmation'

    def get_body_template(self):
        # used by excerpts
        at = self.get_aid_type()
        if at is not None:
            return at.body_template


dd.update_field(Confirmation, 'start_date', default=dd.today,
                verbose_name=_('Period from'))
dd.update_field(Confirmation, 'end_date', verbose_name=_('until'))
# dd.update_field(Confirmation, 'user', verbose_name=_('Requested by'))
dd.update_field(Confirmation, 'company',
                verbose_name=_("Recipient (Organization)"))
dd.update_field(Confirmation, 'contact_person',
                verbose_name=_("Recipient (Person)"))


class Confirmations(dd.Table):
    model = 'aids.Confirmation'
    required = dd.required(user_groups='office', user_level='admin')
    order_by = ["-created"]
    column_names = "description_column created user printed " \
                   "start_date end_date *"

    parameters = dict(
        board=dd.ForeignKey(
            'boards.Board',
            blank=True, null=True,
            help_text=_("Only rows decided by this board.")),
        user=dd.ForeignKey(
            settings.SITE.user_model,
            verbose_name=_("Author"),
            blank=True, null=True,
            help_text=_("Only rows created by this user.")),
        aid_type=dd.ForeignKey(
            'aids.AidType',
            blank=True, null=True,
            help_text=_("Only confirmations about this aid type.")),
        signer=dd.ForeignKey(
            settings.SITE.user_model,
            verbose_name=_("Signer"),
            blank=True, null=True,
            help_text=_("Only rows confirmed (or to be confirmed) "
                        "by this user.")),
        state=ConfirmationStates.field(
            blank=True,
            help_text=_("Only rows having this state.")))

    params_layout = "board signer user aid_type state"

    @classmethod
    def get_request_queryset(self, ar):
        qs = super(Confirmations, self).get_request_queryset(ar)
        pv = ar.param_values
        if pv.aid_type:
            qs = qs.filter(granting__aid_type=pv.aid_type)
        if pv.board:
            qs = qs.filter(granting__board=pv.board)
        if pv.signer:
            qs = qs.filter(signer=pv.signer)
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


# class ConfirmationsToSign(Confirmations):
#     label = _("Aid confirmations to sign")
#     column_names = "client granting signer workflow_buttons *"

#     @classmethod
#     def param_defaults(self, ar, **kw):
#         kw = super(ConfirmationsToSign, self).param_defaults(ar, **kw)
#         kw.update(signer=ar.get_user())
#         kw.update(state=ConfirmationStates.requested)
#         return kw

class PrintConfirmation(dd.Action):

    label = _("Print")
    icon_name = "printer"

    def run_from_ui(self, ar, **kw):
        for obj in ar.selected_rows:
            obj.do_print.run_from_ui(ar)


class ConfirmationsByGranting(dd.VirtualTable):

    # This is a "pseudo-virtual" table because it operates on normal
    # database objects.  It needs to be virtual because Confirmation
    # is an abstract model.  In order to have a detail and a print
    # function, it must define `get_pk_field` and `get_row_by_pk`.

    label = _("Issued confirmations")
    required = dd.required(user_groups='office')
    master = 'aids.Granting'
    master_key = 'granting'
    column_names = "description_column created user printed " \
                   "start_date end_date *"
    do_print = PrintConfirmation()

    @classmethod
    def get_data_rows(self, ar):
        mi = ar.master_instance
        if mi is None:
            return []
        ct = mi.aid_type.confirmation_type
        if not ct:
            return []
        return ct.model.objects.filter(granting=mi).order_by()

    @classmethod
    def get_pk_field(self):
        # We return the pk of SimpleConfirmation although in reality
        # the table can also display other subclasses of
        # Confirmation. That's ok since the primary keys of these
        # subclasses are of same type and name (they are all automatic
        # id fields).
        return SimpleConfirmation._meta.pk

    @classmethod
    def get_row_by_pk(self, ar, pk):
        mi = ar.master_instance
        if mi is None:
            return None
        ct = mi.aid_type.confirmation_type
        if not ct:
            return None
        return ct.model.objects.get(pk=pk)

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
        abstract = dd.is_abstract_model(__name__, 'SimpleConfirmation')
        verbose_name = _("Simple confirmation")
        verbose_name_plural = _("Simple confirmations")


class SimpleConfirmations(Confirmations):
    model = 'aids.SimpleConfirmation'
    required = dd.required(user_groups='office')

    detail_layout = dd.FormLayout("""
    id client user signer workflow_buttons
    granting start_date end_date
    # confirmation_text
    company contact_person #language printed
    remark
    """)  # , window_size=(70, 24))


class SimpleConfirmationsByGranting(SimpleConfirmations):
    master_key = 'granting'
    insert_layout = dd.FormLayout("""
    start_date end_date
    company contact_person #language
    remark
    # client granting:25
    """, window_size=(50, 16))

    column_names = "id client granting start_date end_date *"


ConfirmationTypes.add_item(SimpleConfirmation, SimpleConfirmationsByGranting)


##
## IncomeConfirmation
##

class IncomeConfirmation(Confirmation):
    """This is when a social agent confirms that a client benefits of a
    given income during a given period.

    """

    class Meta:
        abstract = dd.is_abstract_model(__name__, 'IncomeConfirmation')
        verbose_name = _("Income confirmation")
        verbose_name_plural = _("Income confirmations")

    category = models.ForeignKey('aids.Category', blank=True, null=True)

    amount = dd.PriceField(_("Amount"), blank=True, null=True)

    # def confirmation_what(self, ar):
    #     if self.granting:
    #         yield E.b(self.granting.aid_type.get_long_name())
    #     if self.category:
    #         yield " (%s: %s)" % (_("Category"), self.category)
    #     if self.amount:
    #         yield " "
    #         yield _("with amount of")
    #         # "in Höhe von", "d'un montant de"
    #         s = " %s €" % self.amount
    #         s += "/%s" % _("month")
    #         yield E.b(s)


class IncomeConfirmations(Confirmations):
    model = 'aids.IncomeConfirmation'
    required = dd.required(user_groups='office')

    detail_layout = dd.FormLayout("""
    client user signer workflow_buttons printed
    company contact_person #language
    granting:25 start_date end_date
    category amount id
    remark
    """)  # , window_size=(70, 24))


class IncomeConfirmationsByGranting(IncomeConfirmations):
    master_key = 'granting'
    insert_layout = dd.FormLayout("""
    client granting:25
    start_date end_date
    category amount
    company contact_person #language
    remark
    """, window_size=(70, 20), hidden_elements='client granting')

    column_names = "id client granting category amount start_date end_date *"


class IncomeConfirmationsByCategory(IncomeConfirmations):
    master_key = 'category'

ConfirmationTypes.add_item(IncomeConfirmation, IncomeConfirmationsByGranting)

##
## REFUND CONFIRMATIONS
##


dd.inject_field(
    'pcsw.ClientContactType',
    'can_refund',
    models.BooleanField(
        _("Can refund"), default=False,
        help_text=_("")
    ))

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
        abstract = dd.is_abstract_model(__name__, 'RefundConfirmation')
        verbose_name = _("Refund confirmation")
        verbose_name_plural = _("Refund confirmations")

    doctor_type = dd.ForeignKey(
        'pcsw.ClientContactType', verbose_name=_("Doctor type"))
    doctor = dd.ForeignKey(
        'contacts.Person', verbose_name=_("Doctor"),
        blank=True, null=True)
    pharmacy = dd.ForeignKey(
        'contacts.Company', verbose_name=_("Pharmacy"),
        blank=True, null=True)

    def after_ui_create(self, ar):
        super(RefundConfirmation, self).after_ui_create(ar)
        logger.info("20141127 RefundConfirmation %s %s",
                    self.granting, self.client)

    def on_create(self, ar):
        super(RefundConfirmation, self).on_create(ar)
        qs = self.pharmacy_choices(self.granting)
        if qs.count() > 0:
            self.pharmacy = qs[0]

    @dd.chooser()
    def doctor_choices(cls, doctor_type):
        fkw = dict()
        if doctor_type:
            fkw.update(client_contact_type=doctor_type)
        return rt.modules.contacts.Person.objects.filter(**fkw)

    @dd.chooser()
    def pharmacy_choices(cls, granting):
        fkw = dict()
        pt = granting.aid_type.pharmacy_type
        if pt:
            fkw.update(client_contact_type=pt)
        return rt.modules.contacts.Company.objects.filter(**fkw)

    def create_doctor_choice(self, text):
        """
        Called when an unknown doctor name was given.
        Try to auto-create it.
        """
        if not self.doctor_type:
            raise ValidationError("Cannot auto-create without doctor type")
        Person = rt.modules.contacts.Person
        kw = parse_name(text)
        if len(kw) != 2:
            raise ValidationError(
                "Cannot find first and last names in %r to \
                auto-create doctor", text)
        kw.update(client_contact_type=self.doctor_type)
        kw.update(title=_("Dr."))
        p = Person(**kw)
        p.full_clean()
        p.save()
        return p

    @dd.chooser()
    def doctor_type_choices(cls):
        return rt.modules.pcsw.ClientContactType.objects.filter(
            can_refund=True)

    # def confirmation_what(self, ar):
    #     if self.granting:
    #         yield E.b(self.granting.aid_type.get_long_name())
    #         yield ". "
    #     if self.doctor and self.doctor_type_id:
    #         yield _("Recipes issued by")
    #         yield unicode(self.doctor_type)
    #         yield " "
    #         yield E.b(self.doctor.get_full_name())
    #     if self.pharmacy:
    #         yield _("Drugs delivered by")
    #         yield " "
    #         yield E.b(self.pharmacy.get_full_name())


class RefundConfirmations(Confirmations):
    model = 'aids.RefundConfirmation'
    required = dd.required(user_groups='office')

    detail_layout = dd.FormLayout("""
    id client user signer workflow_buttons
    granting:25 start_date end_date
    doctor_type doctor pharmacy
    company contact_person #language printed
    remark
    """)  # , window_size=(70, 24))


class RefundConfirmationsByGranting(RefundConfirmations):
    master_key = 'granting'
    insert_layout = dd.FormLayout("""
    # client granting:25
    start_date end_date
    doctor_type doctor pharmacy
    company contact_person #language printed
    remark
    """, window_size=(70, 20))

    column_names = "id client granting start_date end_date *"


ConfirmationTypes.add_item(RefundConfirmation, RefundConfirmationsByGranting)


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


menu_host = dd.plugins.pcsw


def setup_main_menu(site, ui, profile, m):
    m = m.add_menu(menu_host.app_label, menu_host.verbose_name)
    m.add_action('aids.MyPendingGrantings')


def setup_config_menu(site, ui, profile, m):
    m = m.add_menu(menu_host.app_label, menu_host.verbose_name)
    m.add_action('aids.AidTypes')
    m.add_action('aids.Categories')


def setup_explorer_menu(site, ui, profile, m):
    m = m.add_menu(menu_host.app_label, menu_host.verbose_name)
    m.add_action('aids.Grantings')
    # m.add_action('aids.AidRegimes')
    m.add_action('aids.IncomeConfirmations')
    m.add_action('aids.RefundConfirmations')
    m.add_action('aids.SimpleConfirmations')
    # m.add_action('aids.Helpers')
    # m.add_action('aids.HelperRoles')
