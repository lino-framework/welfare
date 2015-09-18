# -*- coding: UTF-8 -*-
# Copyright 2008-2015 Luc Saffre
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
"""Separate module for defining the Coaching model."""

from __future__ import unicode_literals
from __future__ import print_function

import logging
logger = logging.getLogger(__name__)

from django.db import models
from django.db.models import Q
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from lino.api import dd
from lino import mixins

from lino.modlib.users.mixins import ByUser
from lino_welfare.modlib.pcsw.roles import SocialAgent, SocialStaff


class EndCoaching(dd.ChangeStateAction, dd.NotifyingAction):
    label = _("End coaching")
    help_text = _("User no longer coaches this client.")
    required_states = 'active standby'
    required_roles = dd.required(SocialAgent)

    def get_notify_subject(self, ar, obj, **kw):
        return _("%(client)s no longer coached by %(coach)s") % dict(
            client=obj.client, coach=obj.user)


INTEG_LABEL = dd.apps.integ.verbose_name
GSS_LABEL = _("GSS")  # General Social Service


class CoachingType(mixins.BabelNamed):

    """.. attribute:: does_integ

        Whether coachings of this type are to be considered as
        integration work. This is used when generating calendar events
        for evaluation meetings (see
        :meth:`lino_welfare.modlib.isip.mixins.ContractBase.setup_auto_event`)

    """
    class Meta:
        verbose_name = _("Coaching type")
        verbose_name_plural = _('Coaching types')

    does_integ = models.BooleanField(
        INTEG_LABEL, default=True,
        help_text=_("Whether this coaching type does %s.") % INTEG_LABEL)

    does_gss = models.BooleanField(
        GSS_LABEL, default=True,
        help_text=_("Whether this coaching type does %s.") % GSS_LABEL)

    eval_guestrole = dd.ForeignKey(
        'cal.GuestRole',
        verbose_name=_("Role in evaluations"),
        help_text=_("Role when participating in evaluation meetings."),
        blank=True, null=True)


class CoachingTypes(dd.Table):
    model = 'pcsw.CoachingType'
    column_names = 'name does_integ does_gss eval_guestrole *'
    required_roles = dd.required(SocialStaff)


class CoachingEnding(mixins.BabelNamed, mixins.Sequenced):

    class Meta:
        verbose_name = _("Reason of termination")
        verbose_name_plural = _('Coaching termination reasons')

    #~ name = models.CharField(_("designation"),max_length=200)
    type = dd.ForeignKey(
        CoachingType,
        blank=True, null=True,
        help_text=_("If not empty, allow this ending only on "
                    "coachings of specified type."))


class CoachingEndings(dd.Table):
    help_text = _("A list of reasons expressing why a coaching was ended")
    required_roles = dd.required(SocialStaff)
    model = 'pcsw.CoachingEnding'
    column_names = 'seqno name type *'
    order_by = ['seqno']
    detail_layout = """
    id name seqno
    CoachingsByEnding
    """


class Coaching(mixins.DatePeriod, dd.ImportedFields):

    """A Coaching (Begleitung, intervention) is when a Client is being
    coached by a User (a social assistant) during a given period.

    """

    class Meta:
        verbose_name = _("Coaching")
        verbose_name_plural = _("Coachings")

    user = models.ForeignKey(
        settings.SITE.user_model,
        verbose_name=_("Coach"),
        related_name="%(app_label)s_%(class)s_set_by_user",
    )

    allow_cascaded_delete = ['client']
    workflow_state_field = 'state'

    client = models.ForeignKey('pcsw.Client',
                               related_name="coachings_by_client")
    #~ state = CoachingStates.field(default=CoachingStates.active)
    #~ type = CoachingTypes.field()
    type = dd.ForeignKey(CoachingType, blank=True, null=True)
    primary = models.BooleanField(
        _("Primary"),
        default=False,
        help_text=_("""There's at most one primary coach per client. \
        Enabling this field will automatically make the other \
        coachings non-primary."""))

    ending = models.ForeignKey(CoachingEnding,
                               related_name="%(app_label)s_%(class)s_set",
                               blank=True, null=True)

    @classmethod
    def on_analyze(cls, site):
        super(Coaching, cls).on_analyze(site)
        #~ cls.declare_imported_fields('''client user primary start_date end_date''')
        cls.declare_imported_fields('''client user primary end_date''')

    @dd.chooser()
    def ending_choices(cls, type):
        qs = CoachingEnding.objects.filter(
            Q(type__isnull=True) | Q(type=type))
        return qs.order_by("seqno")

    def disabled_fields(self, ar):
        rv = super(Coaching, self).disabled_fields(ar)
        if settings.SITE.is_imported_partner(self.client):
            if self.primary:
                return self._imported_fields
            return set(['primary'])
        return rv

    def on_create(self, ar):
        """
        Default value for the `user` field is the requesting user.
        """
        if self.user_id is None:
            u = ar.get_user()
            if u is not None:
                self.user = u
        super(Coaching, self).on_create(ar)

    def disable_delete(self, ar=None):
        if ar is not None and settings.SITE.is_imported_partner(self.client):
            if self.primary:
                return _("Cannot delete companies and persons imported from TIM")
        return super(Coaching, self).disable_delete(ar)

    def before_ui_save(self, ar, **kw):
        #~ logger.info("20121011 before_ui_save %s",self)
        super(Coaching, self).before_ui_save(ar, **kw)
        if not self.type:
            self.type = ar.get_user().coaching_type
        if not self.start_date:
            self.start_date = settings.SITE.today()
        if self.ending and not self.end_date:
            self.end_date = settings.SITE.today()

    #~ def update_system_note(self,note):
        #~ note.project = self.client

    def __unicode__(self):
        #~ return _("Coaching of %(client)s by %(user)s") % dict(client=self.client,user=self.user)
        #~ return self.user.username+' / '+self.client.first_name+' '+self.client.last_name[0]
        return self.user.username + ' / ' + self.client.last_name + ' ' + self.client.first_name[0]

    def after_ui_save(self, ar, cw):
        super(Coaching, self).after_ui_save(ar, cw)
        if self.primary:
            for c in self.client.coachings_by_client.exclude(id=self.id):
                if c.primary:
                    c.primary = False
                    c.save()
                    ar.set_response(refresh_all=True)
        #~ return kw

    #~ def get_row_permission(self,user,state,ba):
        #~ """
        #~ """
        #~ logger.info("20121011 get_row_permission %s %s",self,ba)
        #~ if isinstance(ba.action,actions.SubmitInsert):
            #~ if not user.coaching_type:
                #~ return False
        #~ return super(Coaching,self).get_row_permission(user,state,ba)

    def full_clean(self, *args, **kw):
        if not self.start_date and not self.end_date:
            self.start_date = settings.SITE.today()
        if not self.type and self.user:
            self.type = self.user.coaching_type
        super(Coaching, self).full_clean(*args, **kw)

    #~ def save(self,*args,**kw):
        #~ super(Coaching,self).save(*args,**kw)

    def summary_row(self, ar, **kw):
        return [ar.href_to(self.client), " (%s)" % self.state.text]

    def get_related_project(self):
        return self.client

    def get_system_note_type(self, request):
        return settings.SITE.site_config.system_note_type

    def get_system_note_recipients(self, request, silent):
        if silent:
            return
        if self.user.email:
            yield "%s <%s>" % (unicode(self.user), self.user.email)
        for u in settings.SITE.user_model.objects.filter(
                coaching_supervisor=True).exclude(email=''):
            yield "%s <%s>" % (unicode(u), u.email)


dd.update_field(Coaching, 'start_date', verbose_name=_("Coached from"))
dd.update_field(Coaching, 'end_date', verbose_name=_("until"))


class Coachings(dd.Table):
    required_roles = dd.required(SocialStaff)
    help_text = _("Liste des accompagnements.")
    model = 'pcsw.Coaching'

    parameters = mixins.ObservedPeriod(
        coached_by=models.ForeignKey(
            'users.User',
            blank=True, null=True,
            verbose_name=_("Coached by"),
            help_text="""Nur Begleitungen dieses Benutzers."""),
        and_coached_by=models.ForeignKey(
            'users.User',
            blank=True, null=True,
            verbose_name=_("and by"),
            help_text="""... und auch Begleitungen dieses Benutzers."""),
        observed_event=dd.PeriodEvents.field(
            blank=True, default=dd.PeriodEvents.active),
        primary_coachings=dd.YesNo.field(
            _("Primary coachings"),
            blank=True, help_text="""Accompagnements primaires."""),
        coaching_type=models.ForeignKey(
            CoachingType,
            blank=True, null=True,
            help_text="""Nur Begleitungen dieses Dienstes."""),
        ending=models.ForeignKey(
            CoachingEnding,
            blank=True, null=True,
            help_text="""Nur Begleitungen mit diesem Beendigungsgrund."""),
    )
    params_layout = """
    start_date end_date observed_event coached_by and_coached_by
    primary_coachings coaching_type ending
    """
    params_panel_hidden = True

    #~ @classmethod
    #~ def param_defaults(self,ar,**kw):
        #~ kw = super(Coachings,self).param_defaults(ar,**kw)
        #~ D = datetime.date
        #~ kw.update(start_date = D.today())
        #~ kw.update(end_date = D.today())
        #~ return kw

    @classmethod
    def get_request_queryset(self, ar):
        qs = super(Coachings, self).get_request_queryset(ar)
        pv = ar.param_values
        coaches = []
        for u in (pv.coached_by, pv.and_coached_by):
            if u is not None:
                coaches.append(u)
        if len(coaches):
            qs = qs.filter(user__in=coaches)

        ce = pv.observed_event
        if ce is not None:
            qs = ce.add_filter(qs, pv)

        if pv.primary_coachings == dd.YesNo.yes:
            qs = qs.filter(primary=True)
        elif pv.primary_coachings == dd.YesNo.no:
            qs = qs.filter(primary=False)
        if pv.coaching_type is not None:
            qs = qs.filter(type=pv.coaching_type)
        if pv.ending is not None:
            qs = qs.filter(ending=pv.ending)
        return qs

    @classmethod
    def get_title_tags(self, ar):
        for t in super(Coachings, self).get_title_tags(ar):
            yield t

        pv = ar.param_values

        if pv.observed_event:
            yield unicode(pv.observed_event)

        if pv.coached_by:
            s = unicode(self.parameters['coached_by'].verbose_name) + \
                ' ' + unicode(pv.coached_by)
            if pv.and_coached_by:
                s += " %s %s" % (unicode(_('and')),
                                 pv.and_coached_by)
            yield s

        if pv.primary_coachings:
            yield unicode(self.parameters['primary_coachings'].verbose_name) \
                + ' ' + unicode(pv.primary_coachings)

    @classmethod
    def get_create_permission(self, ar):
        """Reception clerks can see coachings, but cannot modify them nor add
        new ones.

        """
        
        if not isinstance(ar.get_user().profile.role, SocialAgent):
        #if not ar.get_user().profile.coaching_level:
            return False
        return super(Coachings, self).get_create_permission(ar)


class CoachingsByClient(Coachings):
    """
    The :class:`Coachings` table in a :class:`Clients` detail.
    """
    required_roles = dd.required()
    #~ debug_permissions = 20121016
    master_key = 'client'
    order_by = ['start_date']
    column_names = 'start_date end_date user:12 primary type:12 ending id'
    hidden_columns = 'id'
    auto_fit_column_widths = True


class CoachingsByEnding(Coachings):
    master_key = 'ending'


class CoachingsByUser(Coachings):
    required_roles = dd.required(SocialAgent)
    master_key = 'user'
    column_names = 'start_date end_date client type primary id'


class MyCoachings(CoachingsByUser, ByUser):
    column_names = 'client start_date end_date type primary id'
    order_by = ['client__name']

    @classmethod
    def param_defaults(self, ar, **kw):
        kw = super(CoachingsByUser, self).param_defaults(ar, **kw)
        kw.update(start_date=dd.today())
        kw.update(end_date=dd.today())
        return kw

