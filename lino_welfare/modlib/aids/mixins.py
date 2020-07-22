# -*- coding: UTF-8 -*-
# Copyright 2014-2017 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

from __future__ import unicode_literals

from builtins import str
import logging
logger = logging.getLogger(__name__)

from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import pgettext_lazy as pgettext

from lino.api import dd, rt
from lino import mixins

from etgen.html import E, tostring
from lino.utils.ranges import encompass

from lino.modlib.checkdata.choicelists import Checker
from lino.modlib.users.mixins import UserAuthored
from lino_xl.lib.contacts.mixins import ContactRelated
from lino_xl.lib.excerpts.mixins import Certifiable
from lino.mixins.periods import rangefmt

from .choicelists import ConfirmationStates
from .roles import AidsStaff


def e2text(v):
    return tostring(v)
#     if isinstance(v, types.GeneratorType):
#         return "".join([e2text(x) for x in v])
#     if E.iselement(v):
#         return tostring(v)
#     return unicode(v)


class SignConfirmation(dd.Action):
    label = pgettext("aids", "Sign")
    show_in_workflow = True
    show_in_bbar = False

    # icon_name = 'flag_green'
    required_states = "requested"
    # help_text = _("You sign this confirmation, making most "
    #               "fields read-only.")

    def get_action_permission(self, ar, obj, state):
        user = ar.get_user()
        if obj.signer_id and obj.signer != user \
           and not user.user_type.has_required_roles([AidsStaff]):
            return False
        return super(SignConfirmation,
                     self).get_action_permission(ar, obj, state)

    def run_from_ui(self, ar, **kw):
        obj = ar.selected_rows[0]

        def ok(ar):
            if not obj.signer_id:
                obj.signer = ar.get_user()
            obj.state = ConfirmationStates.confirmed
            obj.save()
            ar.set_response(refresh=True)
        d = dict(text=obj.confirmation_text())
        d.update(client=e2text(obj.client.get_full_name(nominative=True)))
        msg = _("You confirm that %(client)s %(text)s") % d
        ar.confirm(ok, msg, _("Are you sure?"))


class RevokeConfirmation(dd.Action):
    label = pgettext("aids", "Revoke")
    show_in_workflow = True
    show_in_bbar = False

    # icon_name = 'flag_green'
    required_states = "confirmed"
    help_text = _("You revoke your signatore from this confirmation.")

    def get_action_permission(self, ar, obj, state):
        user = ar.get_user()
        if obj.signer != user and not user.user_type.has_required_roles([AidsStaff]):
            return False
        return super(RevokeConfirmation,
                     self).get_action_permission(ar, obj, state)

    def run_from_ui(self, ar, **kw):
        obj = ar.selected_rows[0]

        def ok(ar):
            # obj.signer = None
            obj.state = ConfirmationStates.requested
            obj.save()
            ar.set_response(refresh=True)
        d = dict(text=obj.confirmation_text())
        d.update(client=e2text(obj.client.get_full_name(nominative=True)))
        msg = _("You revoke your confirmation that %(client)s %(text)s") % d
        ar.confirm(ok, msg, _("Are you sure?"))


class Confirmable(mixins.DateRange):

    class Meta:
        abstract = True

    manager_roles_required = dd.login_required()
    workflow_state_field = 'state'

    signer = dd.ForeignKey(
        settings.SITE.user_model,
        verbose_name=pgettext("aids", "Signer"),
        blank=True, null=True,
        related_name="%(app_label)s_%(class)s_set_by_signer",
    )

    state = ConfirmationStates.field(
        default=ConfirmationStates.as_callable('requested'))

    sign = SignConfirmation()
    revoke = RevokeConfirmation()

    @classmethod
    def on_analyze(cls, site):
        cls.CONFIRMED_FIELDS = dd.fields_list(
            cls,
            cls.get_confirmable_fields())
        super(Confirmable, cls).on_analyze(site)

    @classmethod
    def get_confirmable_fields(cls):
        return ''

    @classmethod
    def setup_parameters(cls, fields):
        fields.update(signer=dd.ForeignKey(
            settings.SITE.user_model,
            verbose_name=pgettext("aids", "Signer"),
            blank=True, null=True))
        fields.update(state=ConfirmationStates.field(blank=True))
        super(Confirmable, cls).setup_parameters(fields)

    @classmethod
    def get_simple_parameters(cls):
        for p in super(Confirmable, cls).get_simple_parameters():
            yield p
        yield 'signer'
        yield 'state'

    def full_clean(self):
        super(Confirmable, self).full_clean()
        if self.signer is None and self.state == ConfirmationStates.confirmed:
            self.state = ConfirmationStates.requested
            # raise ValidationError(_("Cannot confirm without signer!"))

    def get_row_permission(self, ar, state, ba):
        if not super(Confirmable, self).get_row_permission(ar, state, ba):
            return False
        if self.state == ConfirmationStates.confirmed \
           and self.signer is not None \
           and self.signer != ar.get_user():
            return ba.action.readonly
        return True

    def disabled_fields(self, ar):
        if self.state != ConfirmationStates.requested:
            return self.CONFIRMED_FIELDS
        return super(Confirmable, self).disabled_fields(ar)

    def get_printable_context(self, ar=None, **kw):
        kw.update(when=self.get_period_text())
        return super(Confirmable, self).get_printable_context(ar, **kw)

    def confirmation_text(self):
        kw = dict()
        kw.update(when=self.get_period_text())
        at = self.get_aid_type()
        if at:
            kw.update(what=str(at))
        else:
            kw.update(what=str(self))
        return _("receives %(what)s %(when)s.") % kw

    def confirmation_address(self):
        at = self.get_aid_type()
        if at and at.address_type:
            addr = self.client.get_address_by_type(at)
        else:
            addr = self.client.get_primary_address()
        if addr is not None:
            return addr.living_at_text()

    def get_excerpt_title(self):
        at = self.get_aid_type()
        if at:
            return at.get_excerpt_title()
        return str(self)



class Confirmation(
        Confirmable, UserAuthored, ContactRelated,
        mixins.Created, Certifiable):

    class Meta:
        abstract = True

    allow_cascaded_delete = ['client']

    client = dd.ForeignKey(
        'pcsw.Client', related_name="%(app_label)s_%(class)s_set_by_client")
    granting = dd.ForeignKey('aids.Granting', blank=True, null=True)
    remark = dd.RichTextField(
        _("Remark"), blank=True, format='html')
    language = dd.LanguageField(blank=True)

    @classmethod
    def setup_parameters(cls, fields):
        # fields.update(client=dd.ForeignKey(
        #     'pcsw.Client', blank=True, null=True))
        # fields.update(
        #     granting=dd.ForeignKey('aids.Granting', blank=True, null=True))
        fields.update(gender=dd.Genders.field(blank=True, null=True))
        super(Confirmation, cls).setup_parameters(fields)

    @classmethod
    def get_simple_parameters(cls):
        s = list(super(Confirmation, cls).get_simple_parameters())
        s += ['client', 'granting']
        return s

    def __str__(self):
        if self.granting is not None:
            return '%s/%s' % (self.granting, self.pk)
        return '%s #%s' % (self._meta.verbose_name, self.pk)

    def get_date_range_veto(obj):
        pk = dd.plugins.aids.no_date_range_veto_until
        if pk < 0 or obj.granting_id is None or obj.granting_id <= pk:
            return
        gp = obj.granting.get_period()
        if obj.start_date or obj.end_date:
            cp = obj.get_period()
            if cp[1] is None: cp = (cp[0], cp[0])
            if not encompass(gp, cp):
                return _(
                    "Date range %(p1)s lies outside of granted "
                    "period %(p2)s.") % dict(
                        p2=rangefmt(gp), p1=rangefmt(cp))

    def full_clean(self):
        super(Confirmation, self).full_clean()
        if self.granting is None:
            return
        msg = self.get_date_range_veto()
        if msg is not None:
            raise ValidationError(msg)
        if not self.language:
            obj = self.recipient
            if obj is None:
                self.language = self.client.language
            else:
                if isinstance(obj, rt.models.contacts.Role):
                    self.language = obj.person.language
                else:
                    self.language = obj.language

    def on_create(self, ar):
        if self.granting_id:
            self.signer = self.granting.signer
            self.client = self.granting.client
            if self.granting.aid_type_id:
                at = self.granting.aid_type
                self.company = at.company
                self.contact_person = at.contact_person
                self.contact_role = at.contact_role
        super(Confirmation, self).on_create(ar)

    @classmethod
    def get_confirmable_fields(cls):
        return 'client signer granting remark start_date end_date'

    def get_print_language(self):
        return self.language

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
            return rt.models.aids.Granting.objects.get_by_aidtype(
                self.granting.client, self, **aidtype_filter)

    def get_urgent_granting(self):
        return self.get_granting(is_urgent=True)

    @classmethod
    def get_template_group(cls):
        # Used by excerpts and printable.  The individual confirmation
        # models use a common tree of templates.
        return u'aids/Confirmation'

    def get_body_template(self):
        # Overrides :meth:`lino.core.model.Model.get_body_template`.
        at = self.get_aid_type()
        if at is not None:
            return at.body_template


dd.update_field(Confirmation, 'start_date',  default=dd.today,
                verbose_name=_('Period from'))
dd.update_field(Confirmation, 'end_date', default=dd.today,
                verbose_name=_('until'))
# dd.update_field(Confirmation, 'user', verbose_name=_('Requested by'))
dd.update_field(Confirmation, 'company',
                verbose_name=_("Recipient (Organization)"))
dd.update_field(Confirmation, 'contact_person',
                verbose_name=_("Recipient (Person)"))


class ConfirmationChecker(Checker):
    model = Confirmation

    verbose_name = _("Check for confirmations outside of granted period")

    def get_responsible_user(self, obj):
        return obj.client.get_primary_coach()

    def get_checkdata_problems(self, obj, fix=False):
        if obj.granting is None:
            msg = _("Confirmation without granting")
            yield (False, msg)
            return
        msg = obj.get_date_range_veto()
        if msg is not None:
            yield (False, msg)

ConfirmationChecker.activate()
