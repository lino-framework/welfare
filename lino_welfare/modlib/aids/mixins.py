# -*- coding: UTF-8 -*-
# Copyright 2014-2015 Luc Saffre
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
Model mixins for `lino_welfare.modlib.aids`.

.. autosummary::


"""

from __future__ import unicode_literals

import logging
logger = logging.getLogger(__name__)

from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import pgettext_lazy as pgettext

from lino.api import dd, rt
from lino import mixins

from lino.utils.xmlgen.html import E
from lino.utils.ranges import encompass

from lino.modlib.users.mixins import UserAuthored
from lino.modlib.contacts.mixins import ContactRelated
from lino.modlib.excerpts.mixins import Certifiable
from lino.mixins.periods import rangefmt

from .choicelists import ConfirmationStates
from .roles import AidsStaff


def e2text(v):
    return E.tostring(v)
#     if isinstance(v, types.GeneratorType):
#         return "".join([e2text(x) for x in v])
#     if E.iselement(v):
#         return E.tostring(v)
#     return unicode(v)


class SignConfirmation(dd.Action):
    """Sign this database object.

    This is available if signer is either empty or equals the
    requesting user.  Except for system managers who can sign as
    somebody else by manually setting the signer field before running
    this action.

    """
    label = pgettext("aids", "Sign")
    show_in_workflow = True
    show_in_bbar = False

    # icon_name = 'flag_green'
    required_states = "requested"
    help_text = _("You sign this confirmation, making most "
                  "fields read-only.")

    def get_action_permission(self, ar, obj, state):
        user = ar.get_user()
        if obj.signer_id and obj.signer != user \
           and not isinstance(user.profile.role, AidsStaff):
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
        if obj.signer != user and not isinstance(
                user.profile.role, AidsStaff):
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


class Confirmable(mixins.DatePeriod):
    """Base class for both :class:`Granting` and :class:`Confirmation`.

    .. attribute:: signer
 
    The agent who has signed or is expected to sign this item.

    .. attribute:: state

    The confirmation state of this object. Pointer to
    :class:`ConfirmationStates`.

    """
    class Meta:
        abstract = True

    manager_roles_required = dd.login_required()
    workflow_state_field = 'state'

    signer = models.ForeignKey(
        settings.SITE.user_model,
        verbose_name=pgettext("aids", "Signer"),
        blank=True, null=True,
        related_name="%(app_label)s_%(class)s_set_by_signer",
    )

    state = ConfirmationStates.field(default=ConfirmationStates.requested)

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
    def get_parameter_fields(cls, **fields):
        fields.update(signer=models.ForeignKey(
            settings.SITE.user_model,
            verbose_name=pgettext("aids", "Signer"),
            blank=True, null=True))
        fields.update(state=ConfirmationStates.field(blank=True))
        return super(Confirmable, cls).get_parameter_fields(**fields)

    @classmethod
    def get_simple_parameters(cls):
        s = super(Confirmable, cls).get_simple_parameters()
        s.add('signer')
        s.add('state')
        return s

    def full_clean(self):
        super(Confirmable, self).full_clean()
        if self.signer is None and self.state == ConfirmationStates.confirmed:
            self.state = ConfirmationStates.requested
            # raise ValidationError(_("Cannot confirm without signer!"))

    def get_row_permission(self, ar, state, ba):
        """A signed confirmation cannot be modified, even not by a privileged
        user.

        """
        if not super(Confirmable, self).get_row_permission(ar, state, ba):
            return False
        if self.state == ConfirmationStates.confirmed \
           and self.signer is not None \
           and self.signer != ar.get_user():
            return ba.action.readonly
        return True

    def disabled_fields(self, ar):
        if self.state is ConfirmationStates.requested:
            return set()
        return self.CONFIRMED_FIELDS

    def get_printable_context(self, ar=None, **kw):
        kw.update(when=self.get_period_text())
        return super(Confirmable, self).get_printable_context(ar, **kw)

    def confirmation_text(self):
        kw = dict()
        kw.update(when=self.get_period_text())
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

    def get_excerpt_title(self):
        at = self.get_aid_type()
        if at:
            return at.get_excerpt_title()
        return unicode(self)


class Confirmation(
        Confirmable, UserAuthored, ContactRelated,
        mixins.Created, Certifiable):
    """Base class for all aid confirmations.

    Subclassed by :class:`SimpleConfirmation
    <lino_welfare.modlib.aids.models.SimpleConfirmation>`,
    :class:`IncomeConfirmation
    <lino_welfare.modlib.aids.models.IncomeConfirmation>` and
    :class:`RefundConfirmation
    <lino_welfare.modlib.aids.models.RefundConfirmation>`.

    """
    class Meta:
        abstract = True

    allow_cascaded_delete = ['client']

    client = dd.ForeignKey(
        'pcsw.Client', related_name="%(app_label)s_%(class)s_set_by_client")
    granting = models.ForeignKey('aids.Granting', blank=True, null=True)
    remark = dd.RichTextField(
        _("Remark"), blank=True, format='html')
    language = dd.LanguageField(blank=True)

    @classmethod
    def get_parameter_fields(cls, **fields):
        fields.update(client=dd.ForeignKey(
            'pcsw.Client', blank=True, null=True))
        fields.update(
            granting=dd.ForeignKey('aids.Granting', blank=True, null=True))
        fields.update(gender=dd.Genders.field(blank=True, null=True))
        return super(Confirmation, cls).get_parameter_fields(**fields)

    @classmethod
    def get_simple_parameters(cls):
        s = super(Confirmation, cls).get_simple_parameters()
        s |= set(['client', 'granting'])
        return s

    def __unicode__(self):
        if self.granting is not None:
            return '%s/%s' % (self.granting, self.pk)
        return '%s #%s' % (self._meta.verbose_name, self.pk)

    def full_clean(self):
        super(Confirmation, self).full_clean()
        if self.granting is None:
            return
        gp = self.granting.get_period()
        if self.start_date or self.end_date:
            cp = self.get_period()
            if not encompass(gp, cp):
                msg = _(
                    "Date range %(p1)s lies outside of granted "
                    "period %(p2)s.") % dict(p2=rangefmt(gp), p1=rangefmt(cp))
                raise ValidationError(msg)
        if not self.language:
            obj = self.recipient
            if obj is None:
                self.language = self.client.language
            else:
                if isinstance(obj, rt.modules.contacts.Role):
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
            return rt.modules.aids.Granting.objects.get_by_aidtype(
                self.granting.client, self, **aidtype_filter)

    def get_urgent_granting(self):
        """Return the one and only one urgent aid granting for the client and
        period defined for this confirmation.  Return None if there is
        no such granting, or if there is more than one such granting.

        Used in :xfile:`medical_refund.body.html`.

        """
        return self.get_granting(is_urgent=True)

    @classmethod
    def get_template_group(cls):
        # Used by excerpts and printable.  The individual confirmation
        # models use a common tree of templates.
        return 'aids/Confirmation'

    def get_body_template(self):
        """Overrides :meth:`lino.core.model.Model.get_body_template`."""
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


