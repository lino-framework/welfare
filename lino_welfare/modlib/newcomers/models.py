# -*- coding: UTF-8 -*-
# Copyright 2012-2018 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)
"""Database models for :mod:`lino_welfare.modlib.newcomers`.

Defines the models :class:`Broker`, :class:`Faculty` and
:class:`Competence`.

Tables like :class:`NewClients`, :class:`AvailableCoaches`,
:class:`AvailableCoachesByClient`.

See also :ref:`welfare.specs.newcomers`.

"""

from builtins import str
import logging
logger = logging.getLogger(__name__)

import decimal

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.text import format_lazy


from lino.api import dd, rt
from lino.api.dd import dtos

from lino.utils.choosers import chooser
# from lino.utils import ssin
from lino import mixins
from django.conf import settings
from lino_xl.lib.cal.choicelists import amonthago
# from lino_xl.lib.notes.actions import NotableAction
from lino.modlib.notify.actions import NotifyingAction
from lino.modlib.users.choicelists import UserTypes
from lino.modlib.users.mixins import My, UserAuthored

from lino.core.diff import ChangeWatcher

from lino_welfare.modlib.users.desktop import Users
from lino_welfare.modlib.pcsw.roles import SocialStaff, SocialUser
from .roles import NewcomersUser, NewcomersOperator

# users = dd.resolve_app('users')
pcsw = dd.resolve_app('pcsw', strict=True)
from lino_xl.lib.clients.choicelists import ClientStates

WORKLOAD_BASE = decimal.Decimal('10')  # normal number of newcomers per month
MAX_WEIGHT = decimal.Decimal('10')
HUNDRED = decimal.Decimal('100.0')



class Broker(dd.Model):
    """A Broker (Vermittler) is an external institution who suggests
    newcomers.

    """
    class Meta:
        verbose_name = _("Broker")
        verbose_name_plural = _("Brokers")

    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Brokers(dd.Table):

    """
    List of Brokers on this site.
    """
    required_roles = dd.login_required(SocialStaff)
    model = 'newcomers.Broker'
    column_names = 'name *'
    order_by = ["name"]


class Faculty(mixins.BabelNamed):

    """A Faculty (Fachbereich) is a conceptual (not organizational)
    department of this PCSW.  Each Newcomer will be assigned to one
    and only one Faculty, based on his/her needs.

    """
    class Meta:
        verbose_name = _("Faculty")
        verbose_name_plural = _("Faculties")
    #~ body = dd.BabelTextField(_("Body"),blank=True,format='html')
    weight = models.IntegerField(
        _("Work effort"),  # Arbeitsaufwand
        default=MAX_WEIGHT,
        help_text=u"""\
Wieviel Aufwand ein Neuantrag in diesem Fachbereich allgemein verursacht
(0 = gar kein Aufwand, %d = maximaler Aufwand).""" % MAX_WEIGHT)


class Faculties(dd.Table):
    required_roles = dd.login_required(SocialStaff)
    #~ required_user_groups = ['newcomers']
    #~ required_user_level = UserLevels.manager
    model = 'newcomers.Faculty'
    column_names = 'name weight *'
    order_by = ["name"]
    detail_layout = """
    id name weight
    CompetencesByFaculty
    ClientsByFaculty
    """
    insert_layout = """
    name
    weight
    """



class Competence(UserAuthored, mixins.Sequenced):
    """
    A competence is when a given user is declared to be competent
    in a given faculty.
    """
    class Meta:
        #~ abstract = True
        verbose_name = _("Competence")
        verbose_name_plural = _("Competences")

    faculty = dd.ForeignKey('newcomers.Faculty')
    weight = models.IntegerField(
        _("Work effort"),  # Arbeitsaufwand
        blank=True,
          help_text=u"""\
Wieviel Aufwand mir persönlich ein Neuantrag in diesem Fachbereich verursacht
(0 = gar kein Aufwand, %d = maximaler Aufwand).""" % MAX_WEIGHT)

    def full_clean(self, *args, **kw):
        if self.weight is None:
            self.weight = self.faculty.weight
        super(Competence, self).full_clean(*args, **kw)

    def __str__(self):
        return u'%s #%s' % (self._meta.verbose_name, self.pk)

dd.update_field(Competence, 'user', verbose_name=_("User"))


class Competences(dd.Table):
    required_roles = dd.login_required(SocialStaff)
    model = 'newcomers.Competence'
    column_names = 'id user faculty weight *'
    order_by = ["id"]


class CompetencesByUser(Competences):
    required_roles = dd.login_required()
    master_key = 'user'
    column_names = 'seqno faculty weight *'
    order_by = ["seqno"]


class CompetencesByFaculty(Competences):
    master_key = 'faculty'
    column_names = 'user weight *'
    order_by = ["user"]


class MyCompetences(My, CompetencesByUser):
    pass


#~ class Newcomers(pcsw.Clients):
    #~ """
    #~ Clients who have the "Newcomer" checkbox on.
    #~ """
    #~ required = dict(user_groups=['newcomers'])

    #~ use_as_default_table = False
    #~ column_names = "name_column broker faculty address_column *"

    #~ label = _("Newcomers")

    #~ @classmethod
    #~ def param_defaults(self,ar,**kw):
        #~ kw = super(Newcomers,self).param_defaults(ar,**kw)
        #~ kw.update(client_state=ClientStates.newcomer)
        #~ kw.update(coached_on=None)
        #~ return kw


def faculty_weight(user, client):

    if not client or not client.faculty:
        w = MAX_WEIGHT
    else:
        try:
            w = Competence.objects.get(
                faculty=client.faculty, user=user).weight
        except Competence.DoesNotExist:
            w = MAX_WEIGHT
    if user.newcomer_quota != 0:
        # e.g. weight counts double for those who work halftime for newcomers
        # e.g. weight unchanged if user works 100% for newcomers
        w = w / (user.newcomer_quota / HUNDRED)
    return w


class NewClients(pcsw.CoachedClients):
    """A variant of :class:`pcsw.CoachedClients
    <lino_welfare.modlib.pcsw.models.CoachedClients>` designed for newcomers
    consultants.

    """
    required_roles = dd.login_required(NewcomersUser)
    label = _("New Clients")
    use_as_default_table = False

    help_text = u"""\
Liste der neuen Klienten zwecks Zuweisung
eines Begleiters oder Ablehnen des Hilfeantrags."""

    column_names = ("name_column:20 client_state broker faculty "
                    "national_id:10 gsm:10 address_column age:10 "
                    "email phone:10 *")

    parameters = dict(
        new_since=models.DateField(
            _("New clients since"),
            blank=True, null=True,
            help_text="Auch Klienten, die erst seit Kurzem begleitet sind."),
        **pcsw.CoachedClients.parameters)

    params_layout = 'client_state new_since also_obsolete coached_by'

    @classmethod
    def param_defaults(self, ar, **kw):
        kw = super(NewClients, self).param_defaults(ar, **kw)
        kw.update(client_state=ClientStates.newcomer)
        # kw.update(new_since=amonthago())
        return kw

    @classmethod
    def get_request_queryset(self, ar):
        qs = super(NewClients, self).get_request_queryset(ar)
        pv = ar.param_values
        if pv.new_since:
            qs = qs.filter(
                coachings_by_client__start_date__gte=pv.new_since)
        return qs

    @classmethod
    def get_title_tags(self, ar):
        for t in super(NewClients, self).get_title_tags(ar):
            yield t
        pv = ar.param_values
        if pv.new_since:
            yield str(self.parameters['new_since'].verbose_name) \
                + ' ' + dtos(pv.new_since)


class ClientsByFaculty(pcsw.Clients):
    master_key = 'faculty'
    column_names = "name_column broker address_column *"


class AvailableCoaches(Users):
    """List of users available for new coachings."""
    help_text = _("List of users available for new coachings")
    use_as_default_table = False
    required_roles = dd.login_required(NewcomersUser)
    auto_fit_column_widths = True
    editable = False  # even root should not edit here
    label = _("Available Coaches")
    column_names = 'name_column workflow_buttons:10 primary_clients new_clients newcomer_quota current_weight added_weight score'
    parameters = dict(
        for_client=dd.ForeignKey(
            'pcsw.Client',
            verbose_name=_("Show suggested agents for"), blank=True),
        since=models.DateField(
            _("New clients since"),
            blank=True, default=amonthago,
            help_text=_("New clients are those whose coaching "
                        "started after this date")),
    )
    params_layout = "for_client since"

    @chooser()
    def for_client_choices(cls):
        return NewClients.request().data_iterator

    @classmethod
    def get_request_queryset(self, ar):
        user_types = [p for p in UserTypes.items()
                    if isinstance(p.role, SocialUser)]
        return super(AvailableCoaches, self, ar).filter(
            models.Q(user_type__in=user_types))

    @classmethod
    def get_data_rows(self, ar):
        client = ar.param_values.for_client
        if client:
            # if client.client_state != ClientStates.newcomer:
            #     raise Warning(_("Only for newcomers"))
            if not client.faculty:
                raise Warning(_("Only for clients with given `faculty`."))

        total_weight = decimal.Decimal('0')
        data = []
        qs = super(AvailableCoaches, self).get_request_queryset(ar)
        qs = qs.filter(newcomer_quota__gt=0)
        for user in qs:
            if client:
                if client.faculty:
                    r = Competence.objects.filter(
                        user=user, faculty=client.faculty)
                    if r.count() == 0:
                        continue

            user.new_clients = NewClients.request(param_values=dict(
                coached_by=user,
                client_state=ClientStates.coached,
                new_since=ar.param_values.since))

            user._score = HUNDRED
            user._hw = faculty_weight(user, client)

            user._weight = decimal.Decimal('0')
            for nc in user.new_clients:
                user._weight += faculty_weight(user, nc)
            total_weight += user._weight
            total_weight += user._hw
            #~ total_quota += user.newcomer_quota

            data.append(user)

        #~ total_weight += user._hw

        if len(data) == 0:
            if client and client.faculty:
                raise Warning(_("No coaches available for %s.") %
                              client.faculty)
        elif total_weight != 0:
            for user in data:
                # hypothetic weight if this user would get this client
                #~ user._score = 100.0 - (user._weight * 100.0 / total_weight)
                user._score = HUNDRED * \
                    (user._weight + user._hw) / total_weight
                #~ logger.info("%s (%s+%s)/%s = %s%%",user.username,user._weight,user._hw,total_weight,user._score)

        # def fn(a, b):
        #     return cmp(a._score, b._score)
        data.sort(key=lambda a: a._score)
        return data

    @dd.requestfield(_("Primary clients"))
    def primary_clients(self, obj, ar):
        #~ return pcsw.ClientsByCoach1.request(ar.ui,master_instance=obj)
        return rt.models.coachings.CoachingsByUser.request(master_instance=obj)

    #~ @dd.requestfield(_("Active clients"))
    #~ def active_clients(self,obj,ar):
        #~ return integ.Clients.request(param_values=dict(coached_by=obj,only_active=True))

    @dd.requestfield(_("New Clients"))
    def new_clients(self, obj, ar):
        return obj.new_clients

    @dd.virtualfield(models.DecimalField(_("Current workload"),
                                         max_digits=8, decimal_places=0,
        help_text=u"""\
Momentane Gesamtbelastung dieses Benutzers durch neue Klienten. 
Summe der Belastungspunkte pro neuem Klient."""))
    def current_weight(self, obj, ar):
        #~ return "%+6.2f%%" % self.compute_workload(ar,obj)
        return obj._weight

    @dd.virtualfield(models.DecimalField(_("Added workload"),
                                         max_digits=8, decimal_places=0,
        help_text=u"""\
Mehrbelastung, die dieser Neuantrag im Falle einer Zuweisung diesem Benutzer verursachen würde."""))
    def added_weight(self, obj, ar):
        #~ return "%+6.2f%%" % self.compute_workload(ar,obj)
        return obj._hw

    #~ @dd.virtualfield(models.CharField(_("Score"),max_length=6,help_text=u"""\
    @dd.virtualfield(
        models.DecimalField(
            format_lazy(u"{}{}",_("Added workload"), " (%)"),
            max_digits=8, decimal_places=2,
            help_text=u"""Mehrbelastung im Verhältnis zur Gesamtbelastung."""))
    def score(self, obj, ar):
        #~ return "%+6.2f%%" % self.compute_workload(ar,obj)
        #~ return "%6.0f%%" % obj._score
        return obj._score


class AssignCoach(NotifyingAction):
    """
    Assign this agent as coach for this client.  This will set the
    client's state to `Coached` and send a notification to the new
    coach.

    Diesen Benutzer als Begleiter für diesen Klienten eintragen und
    den Zustand des Klienten auf "Begleitet" setzen.  Anschließend
    wird der Klient in der Liste "Neue Klienten" nicht mehr angezeigt.

    This action is available only in the
    :class:`AvailableCoachesByClient` table.
    """
    label = _("Assign")
    required_roles = dd.login_required(NewcomersOperator)
    # required_roles = dd.login_required(NewcomersUser)
    show_in_workflow = True

    def get_notify_subject(self, ar, obj, **kw):
        # return _('New client for %s') % obj
        # obj is a User instance
        client = ar.master_instance
        if client:
            return _('%(client)s assigned to %(coach)s') % dict(
                client=client, coach=obj)

    def get_notify_body(self, ar, obj, **kw):
        # obj is a User instance
        client = ar.master_instance
        if client:
            tpl = _("%(client)s is now coached by %(coach)s for %(faculty)s.")
            return tpl % dict(
                client=client, coach=obj, faculty=client.faculty)

    def get_notify_recipients(self, ar, obj):
        """Yield a list of (users, mailmode) tuples to be notified.

        """
        # obj is a User instance
        client = ar.master_instance
        if client:
            return client.get_change_observers(ar)

    # def get_change_owner(self, ar, obj):
    #     return ar.master_instance

    def run_from_ui(self, ar, **kw):
        # replaces the default implementation
        obj = ar.selected_rows[0]
        # obj is a User instance
        client = ar.master_instance
        watcher = ChangeWatcher(client)

        coaching = rt.models.coachings.Coaching(
            client=client, user=obj,
            start_date=settings.SITE.today(),
            primary=True,
            type=obj.coaching_type)
        coaching.adapt_primary()
        coaching.full_clean()
        coaching.save()
        dd.on_ui_created.send(coaching, request=ar.request)
        client.client_state = ClientStates.coached
        client.full_clean()
        client.save()
        watcher.send_update(ar)

        self.emit_message(ar, client)

        ar.success(ar.action_param_values.notify_body,
                   alert=True, refresh_all=True, **kw)


class AvailableCoachesByClient(AvailableCoaches):
    """
    List of users available for coaching this client.  Visible only to
    Newcomers consultants.
    """
    master = 'pcsw.Client'
    label = _("Available Coaches")
    required_roles = dd.login_required(NewcomersOperator)

    assign_coach = AssignCoach()

    #~ display_mode = 'html'
    editable = False
    hide_sums = True

    @classmethod
    def get_data_rows(self, ar):
        ar.param_values.for_client = ar.master_instance
        return super(AvailableCoachesByClient, self).get_data_rows(ar)


settings.SITE.add_user_field('newcomer_quota', models.IntegerField(
    _("Newcomers Quota"),
    default=0,
    help_text=u"""\
Wieviel Arbeitszeit dieser Benutzer für Neuanträge zur Verfügung steht
(100 = ganztags, 50 = halbtags, 0 = gar nicht).
Wenn zwei Benutzer die gleiche Belastungspunktzahl haben,
aber einer davon sich nur zu 50% um Neuanträge kümmert,
gilt er als doppelt so belastet wie sein Kollege.
"""))


dd.inject_field(
    'pcsw.Client',
    'broker',
    dd.ForeignKey(
        'newcomers.Broker',
        blank=True, null=True,
        help_text=_("The Broker who sent this Newcomer.")))

dd.inject_field(
    'pcsw.Client',
    'faculty',
    dd.ForeignKey(
        'newcomers.Faculty',
        blank=True, null=True,
        help_text=_("The Faculty this client has been attributed to.")),
    active=True)


