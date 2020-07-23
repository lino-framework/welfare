# -*- coding: UTF-8 -*-
# Copyright 2008-2019 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)


from __future__ import unicode_literals

from builtins import str

from lino.utils import AttrDict
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _

from lino import mixins
from lino.api import dd, rt
from lino.mixins.periods import rangefmt
from lino.modlib.uploads.choicelists import UploadAreas
from lino.modlib.uploads.mixins import UploadController
from lino.modlib.users.mixins import UserAuthored
from lino.utils import mti
from lino.utils.ranges import isrange
from lino.utils.ranges import overlap2, encompass
from lino_welfare.modlib.integ.roles import IntegUser
from lino_xl.lib.coachings.mixins import ClientChecker
from lino_welfare.modlib.system.models import Signers
from lino_xl.lib.cal.choicelists import DurationUnits
from lino_xl.lib.cal.mixins import EventGenerator
from lino_xl.lib.cal.utils import update_auto_task
from lino_xl.lib.contacts.mixins import ContactRelated
from lino_xl.lib.excerpts.mixins import Certifiable
from .choicelists import ContractEvents, OverlapGroups


# from lino.modlib.system.mixins import PeriodEvents


def default_signer1():
    return settings.SITE.site_config.signer1


def default_signer2():
    return settings.SITE.site_config.signer2


class ContractTypeBase(mixins.BabelNamed):

    class Meta:
        abstract = True

    full_name = models.CharField(_("Full name"), blank=True, max_length=200)

    exam_policy = dd.ForeignKey(
        "isip.ExamPolicy",
        related_name="%(app_label)s_%(class)s_set",
        blank=True, null=True)

    overlap_group = OverlapGroups.field(blank=True)
    template = models.CharField(_("Template"), max_length=200, blank=True)

    @dd.chooser(simple_values=True)
    def template_choices(cls):
        bm = rt.models.printing.BuildMethods.get_system_default()
        return rt.find_template_config_files(
            bm.template_ext, cls.templates_group)


class ContractPartnerBase(ContactRelated):
    class Meta:
        abstract = True

    def get_recipient(self):
        contact = self.get_contact()
        if contact is not None:
            return contact
        if self.company:
            return self.company
        return self.client
    recipient = property(get_recipient)

    @classmethod
    def contact_person_choices_queryset(cls, company):
        return rt.models.contacts.Person.objects.filter(
            rolesbyperson__company=company,
            rolesbyperson__type__use_in_contracts=True)

    @dd.chooser()
    def contact_role_choices(cls):
        return rt.models.contacts.RoleType.objects.filter(
            use_in_contracts=True)


class OverlappingContractsTest:

    def __init__(self, client):
        self.client = client
        self.actives = []
        for model in rt.models_by_base(ContractBase):
            for con1 in model.objects.filter(client=client):
                ap = con1.active_period()
                if ap[0] is None and ap[1] is None:
                    continue
                self.actives.append((ap, con1))

    def check(self, con1):
        ap = con1.active_period()
        if ap[0] is None and ap[1] is None:
            return
        if False:
            cp = (self.client.coached_from, self.client.coached_until)
            if not encompass(cp, ap):
                return _("Date range %(p1)s lies outside of coached "
                         "period %(p2)s.") \
                    % dict(p2=rangefmt(cp), p1=rangefmt(ap))
        for (p2, con2) in self.actives:
            if con1 != con2 and overlap2(ap, p2):
                if con1.type.overlap_group and con1.type.overlap_group == con2.type.overlap_group:
                    msg = _("Date range overlaps with {ctype} #{id}.")
                    msg = msg.format(
                        ctype=con2.__class__._meta.verbose_name,
                        id=con2.pk)
                    return msg
        return None

    def check_all(self):
        messages = []
        for (p1, con1) in self.actives:
            msg = self.check(con1)
            if msg:
                messages.append(
                    _("%(ctype)s #%(id)s : %(msg)s") % dict(
                        msg=msg,
                        ctype=con1.__class__._meta.verbose_name,
                        id=con1.pk))
        return messages


class OverlappingContractsChecker(ClientChecker):
    verbose_name = _("Check for overlapping contracts")

    def get_checkdata_problems(self, obj, fix=False):
        msg = '  '.join(OverlappingContractsTest(obj).check_all())
        if msg:
            yield (False, msg)

OverlappingContractsChecker.activate()



class ContractBase(Signers, Certifiable, EventGenerator, UserAuthored,
                   UploadController):

    manager_roles_required = dd.login_required(IntegUser)

    TASKTYPE_CONTRACT_APPLIES_UNTIL = 1

    class Meta:
        abstract = True

    client = dd.ForeignKey(
        'pcsw.Client',
        related_name="%(app_label)s_%(class)s_set_by_client")

    language = dd.LanguageField()

    applies_from = models.DateField(_("applies from"), blank=True, null=True)
    applies_until = models.DateField(_("applies until"), blank=True, null=True)
    date_decided = models.DateField(
        blank=True, null=True, verbose_name=_("date decided"))
    date_issued = models.DateField(
        blank=True, null=True, verbose_name=_("date issued"))

    user_asd = dd.ForeignKey(
        "users.User",
        verbose_name=_("responsible (ASD)"),
        related_name="%(app_label)s_%(class)s_set_by_user_asd",
        blank=True, null=True)

    exam_policy = dd.ForeignKey(
        "isip.ExamPolicy",
        related_name="%(app_label)s_%(class)s_set",
        blank=True, null=True)

    ending = dd.ForeignKey(
        "isip.ContractEnding",
        related_name="%(app_label)s_%(class)s_set",
        blank=True, null=True)
    date_ended = models.DateField(
        blank=True, null=True, verbose_name=_("date ended"))

    # hidden_columns = 'date_decided date_issued \
    # exam_policy user_asd ending date_ended signer1 signer2'

    def __str__(self):
        kw = dict(type=str(self._meta.verbose_name))
        if self.pk is None:
            kw.update(client=str(self.client))
            return '{type} ({client})'.format(**kw)
        kw.update(
            id=self.pk,
            client=self.client.get_full_name(salutation=False))
        return '{type}#{id} ({client})'.format(**kw)
        # return u'%s#%s (%s)' % (self._meta.verbose_name, self.pk,
        #                         self.client.get_full_name(salutation=False))

    def get_upload_area(self):
        return UploadAreas.contract

    def get_excerpt_title(self):
        return str(self.type)
        # return unicode(self._meta.verbose_name)

    def get_excerpt_templates(self, bm):
        if self.type_id:
            if self.type.template:
                # assert self.type.template.endswith(bm.template_ext)
                return [self.type.template]

    # backwards compat for document templates
    def get_person(self):
        return self.client
    person = property(get_person)

    def get_print_language(self):
        return self.language

    @dd.chooser()
    def ending_choices(cls):
        return rt.models.isip.ContractEnding.objects.filter(use_in_isip=True)

    def applies_until_changed(self, ar):
        self.date_ended = self.applies_until

    def client_changed(self, ar):

        if self.client_id is not None:
            #~ pc = self.person.get_primary_coach()
            #~ qs = self.person.get_coachings(self.applies_from,active=True)
            qs = self.client.get_coachings(
                (self.applies_from, self.applies_until),
                type__does_gss=True)
            if qs.count() == 1:
                user_asd = qs[0].user
                if user_asd is None or user_asd == self.user:
                    self.user_asd = None
                else:
                    self.user_asd = user_asd

    def on_create(self, ar):
        super(ContractBase, self).on_create(ar)
        self.client_changed(ar)

    def get_author(self):
        """If `user` is empty, then `user_asd` can edit this contract."""
        return self.user or self.user_asd

    def set_author(self, user):
        self.user = user
        if self.user_asd == user:
            self.user_asd = None

    def after_ui_save(self, ar, cw):
        super(ContractBase, self).after_ui_save(ar, cw)
        self.update_reminders(ar)

    def full_clean(self, *args, **kw):
        if not self.date_ended:
            self.date_ended = self.applies_until
        r = self.active_period()
        if not isrange(*r):
            raise ValidationError(_('Contract ends before it started.'))

        if self.type_id:
            if not self.exam_policy_id:
                if self.type.exam_policy_id:
                    self.exam_policy_id = self.type.exam_policy_id

            if self.client_id is not None:
                if self.type.overlap_group:
                    msg = OverlappingContractsTest(self.client).check(self)
                    if msg:
                        raise ValidationError(msg)
        super(ContractBase, self).full_clean(*args, **kw)

        if self.type_id is None:
            raise ValidationError(dict(
                type=[_("You must specify a contract type.")]))

    def update_owned_instance(self, other):
        if isinstance(other, mixins.ProjectRelated):
            other.project = self.client
        super(ContractBase, self).update_owned_instance(other)

    def setup_auto_event(self, evt):
        super(ContractBase, self).setup_auto_event(evt)
        self.client.setup_auto_event(evt)

    def update_cal_rset(self):
        return self.exam_policy

    def update_cal_from(self, ar):
        date = self.applies_from
        if not date:
            return None
        rset = self.update_cal_rset()
        return rset.get_next_suggested_date(ar, date)

    def update_cal_event_type(self):
        if self.exam_policy is not None:
            return self.exam_policy.event_type

    def update_cal_until(self):
        return self.date_ended or self.applies_until

    def update_cal_summary(self, event_type, i):
        if event_type is not None:
            if event_type.event_label:
                return event_type.event_label + " " + str(i)
        return _("Evaluation %d") % i

    def update_reminders(self, ar):
        rv = super(ContractBase, self).update_reminders(ar)
        au = self.update_cal_until()
        if au:
            au = DurationUnits.months.add_duration(au, -1)
        update_auto_task(
            self.TASKTYPE_CONTRACT_APPLIES_UNTIL,
            self.user,
            au,
            _("Contract ends in a month"),
            self)
        return rv

    def active_period(self):
        return (self.applies_from, self.date_ended or self.applies_until)

    def get_granting(self, **aidtype_filter):
        ap = self.active_period()
        ap = AttrDict(start_date=ap[0], end_date=ap[1])
        # print(20170529, ap)
        return rt.models.aids.Granting.objects.get_by_aidtype(
            self.client, ap, **aidtype_filter)

    def get_aid_type(self):
        # may be used in `.odt` template for `isip.Contract`
        g = self.get_granting(is_integ_duty=True)
        if g is not None:
            return g.aid_type

    def get_aid_confirmation(self):
        g = self.get_granting(is_integ_duty=True)
        if g and g.aid_type and g.aid_type.confirmation_type:
            return g
            # ct = g.aid_type.confirmation_type
            # qs = ct.model.objects.filter(granting=g)
            # if qs.count() > 0:
            #     return qs[qs.count()-1]

    def suggest_cal_guests(self, event):
        client = event.project
        if client is None:
            return
        Guest = rt.models.cal.Guest
        Person = rt.models.contacts.Person
        # GuestStates = rt.models.cal.GuestStates
        # st = GuestStates.accepted
        # yield Guest(event=event,
        #             partner=client,
        #             state=st,
        #             role=settings.SITE.site_config.client_guestrole)

        period = (event.start_date, event.start_date)
        qs = client.get_coachings(period)
        qs = client.get_coachings(period, user__partner__isnull=False)
        for coaching in qs:
            if coaching.type and coaching.type.eval_guestrole:
                u = coaching.user
                if u != event.user and u.partner is not None:
                    p = mti.get_child(u.partner, Person)
                    if p is not None:
                        yield Guest(event=event, partner=p,
                                    role=coaching.type.eval_guestrole)

    @classmethod
    def get_printable_demo_objects(cls):
        return cls.objects.all()

dd.update_field(ContractBase, 'signer1', default=default_signer1)
dd.update_field(ContractBase, 'signer2', default=default_signer2)


class ContractBaseTable(dd.Table):

    parameters = mixins.ObservedDateRange(
        user=dd.ForeignKey(settings.SITE.user_model, blank=True),

        observed_event=ContractEvents.field(
            blank=True, default=ContractEvents.as_callable('active')),

        ending_success=dd.YesNo.field(
            _("Successfully ended"),
            blank=True,
            help_text="""Contrats terminés avec succès."""),
        ending=dd.ForeignKey(
            'isip.ContractEnding',
            blank=True, null=True,
            help_text="""Nur Konventionen mit diesem Beendigungsgrund."""),
        company=dd.ForeignKey(
            'contacts.Company',
            blank=True, null=True,
            help_text=_("Only contracts with this company as partner."))
    )

    params_layout = """
    user type start_date end_date observed_event
    company ending_success ending
    """
    params_panel_hidden = True

    @classmethod
    def get_request_queryset(cls, ar):
        qs = super(ContractBaseTable, cls).get_request_queryset(ar)
        pv = ar.param_values
        #~ logger.info("20120608.get_request_queryset param_values = %r", pv)
        if pv.user:
            qs = qs.filter(user=pv.user)
        if pv.type:
            qs = qs.filter(type=pv.type)

        ce = pv.observed_event
        if pv.start_date is None or pv.end_date is None:
            period = None
        else:
            period = (pv.start_date, pv.end_date)
        if ce and period is not None:
            if ce == ContractEvents.ended:
                qs = qs.filter(dd.inrange_filter('date_ended', period))
            elif ce == ContractEvents.started:
                qs = qs.filter(dd.inrange_filter('applies_from', period))
            elif ce == ContractEvents.decided:
                qs = qs.filter(dd.inrange_filter('date_decided', period))
            elif ce == ContractEvents.issued:
                qs = qs.filter(dd.inrange_filter('date_issued', period))
            elif ce == ContractEvents.active:
                # f1 = Q(applies_until__isnull=True) | Q(
                #     applies_until__gte=period[0])
                # flt = f1 & (Q(date_ended__isnull=True) |
                #             Q(date_ended__gte=period[0]))
                qs = qs.filter(
                    date_ended__gte=period[0], applies_from__lte=period[1])
            else:
                raise Exception(repr(ce))

        if pv.ending_success == dd.YesNo.yes:
            qs = qs.filter(ending__isnull=False, ending__is_success=True)
        elif pv.ending_success == dd.YesNo.no:
            qs = qs.filter(ending__isnull=False, ending__is_success=False)

        if pv.ending is not None:
            qs = qs.filter(ending=pv.ending)
        #~ logger.info("20130524 %s",qs.query)
        return qs

    @classmethod
    def get_title_tags(self, ar):
        for t in super(ContractBaseTable, self).get_title_tags(ar):
            yield t

        pv = ar.param_values
        if pv.start_date is None or pv.end_date is None:
            pass
        else:
            oe = pv.observed_event
            if oe is not None:
                yield "%s %s-%s" % (str(oe.text),
                                    dd.dtos(pv.start_date),
                                    dd.dtos(pv.end_date))

        if pv.company:
            yield str(pv.company)
