# -*- coding: UTF-8 -*-
# Copyright 2008-2014 Luc Saffre
# License: BSD (see file COPYING for details)

"""
The :xfile:`models.py` module for the
:mod:`lino_welfare.modlib.isip` app
(eee :ddref:`isip`)

"""

from django.db import models
from django.db.models import Q
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from atelier.utils import AttrDict

from lino import dd, rt
from lino import mixins
notes = dd.resolve_app('notes')
contacts = dd.resolve_app('contacts')

from lino.modlib.excerpts.mixins import Certifiable

from lino.utils.ranges import isrange, overlap2, encompass
from lino.mixins.periods import rangefmt

from lino_welfare.modlib.system.models import Signers

config = dd.plugins.isip


cal = dd.resolve_app('cal')

COACHINGTYPE_ASD = 1
COACHINGTYPE_DSBE = 2


#
# CONTRACT TYPES
#
class ContractType(mixins.BabelNamed):

    #~ _lino_preferred_width = 20
    preferred_foreignkey_width = 20

    templates_group = 'isip/Contract'

    class Meta:
        verbose_name = _("ISIP Type")
        verbose_name_plural = _('ISIP Types')

    ref = models.CharField(_("Reference"), max_length=20, blank=True)
    full_name = models.CharField(
        _("Full name"), blank=True, max_length=200)

    exam_policy = dd.ForeignKey(
        "isip.ExamPolicy",
        related_name="%(app_label)s_%(class)s_set",
        blank=True, null=True)
    needs_study_type = models.BooleanField(
        _("needs Study type"), default=False)


class ContractTypes(dd.Table):
    required = dict(user_groups='integ', user_level='manager')
    model = ContractType
    column_names = 'name ref exam_policy needs_study_type *'
    detail_layout = """
    id ref exam_policy needs_study_type
    name
    full_name
    ContractsByType
    """


#
# EXAMINATION POLICIES
#
class ExamPolicy(mixins.BabelNamed, cal.RecurrenceSet):

    class Meta:
        verbose_name = _("Examination Policy")
        verbose_name_plural = _('Examination Policies')

    hidden_columns = 'start_date start_time end_date end_time'
    event_type = dd.ForeignKey(
        'cal.EventType', null=True, blank=True,
        help_text=_("""Generated events will receive this type."""))


class ExamPolicies(dd.Table):
    required = dict(user_groups='integ', user_level='manager')
    model = ExamPolicy
    column_names = 'name *'
    detail_layout = """
    id name
    # summary start_date end_date
    # description
    max_events every every_unit event_type
    monday tuesday wednesday thursday friday saturday sunday
    isip.ContractsByPolicy
    jobs.ContractsByPolicy
    """


JOBS_MODULE_NAME = settings.SITE.plugins.jobs.verbose_name


class ContractEnding(dd.Model):

    class Meta:
        verbose_name = _("Reason of termination")
        verbose_name_plural = _('Contract termination reasons')

    name = models.CharField(_("designation"), max_length=200)
    use_in_isip = models.BooleanField(config.verbose_name, default=True)
    use_in_jobs = models.BooleanField(JOBS_MODULE_NAME, default=True)
    is_success = models.BooleanField(_("Success"), default=False)
    needs_date_ended = models.BooleanField(
        _("Require date ended"), default=False)

    def __unicode__(self):
        return unicode(self.name)


class ContractEndings(dd.Table):
    required = dict(user_groups='integ', user_level='manager')
    model = 'isip.ContractEnding'
    column_names = 'name use_in_isip use_in_jobs is_success needs_date_ended *'
    order_by = ['name']
    detail_layout = """
    name
    use_in_isip use_in_jobs is_success needs_date_ended
    isip.ContractsByEnding
    jobs.ContractsByEnding
    """


def default_signer1():
    return settings.SITE.site_config.signer1


def default_signer2():
    return settings.SITE.site_config.signer2


class ContractPartnerBase(contacts.ContactRelated):
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
        return settings.SITE.modules.contacts.Person.objects.filter(
            rolesbyperson__company=company,
            rolesbyperson__type__use_in_contracts=True)

    @dd.chooser()
    def contact_role_choices(cls):
        return contacts.RoleType.objects.filter(use_in_contracts=True)


class ContractPartner(ContractPartnerBase):

    class Meta:
        verbose_name = _("Contract partner")
        verbose_name_plural = _("Contract partners")

    contract = dd.ForeignKey('isip.Contract')

    duties_company = dd.RichTextField(
        _("duties company"),
        blank=True, null=True, format='html')


class ContractPartners(dd.Table):
    model = 'isip.ContractPartner'
    columns = 'contract company contact_person contact_role'
    detail_layout = """
    company contact_person contact_role
    duties_company
    """


class PartnersByContract(ContractPartners):
    master_key = 'contract'
    columns = 'company contact_person contact_role duties_company'


class ContractBase(Signers, Certifiable, cal.EventGenerator):

    """Abstract base class for :class:`welfare.jobs.Contract` and
    :class:`welfare.isip.Contract`.

    """

    manager_level_field = 'integ_level'

    TASKTYPE_CONTRACT_APPLIES_UNTIL = 1

    class Meta:
        abstract = True

    client = models.ForeignKey(
        'pcsw.Client',
        related_name="%(app_label)s_%(class)s_set_by_client")

    language = dd.LanguageField()

    applies_from = models.DateField(_("applies from"), blank=True, null=True)
    applies_until = models.DateField(_("applies until"), blank=True, null=True)
    date_decided = models.DateField(
        blank=True, null=True, verbose_name=_("date decided"))
    date_issued = models.DateField(
        blank=True, null=True, verbose_name=_("date issued"))

    user_asd = models.ForeignKey(
        "users.User",
        verbose_name=_("responsible (ASD)"),
        related_name="%(app_label)s_%(class)s_set_by_user_asd",
        #~ related_name='contracts_asd',
        blank=True, null=True)

    exam_policy = models.ForeignKey(
        "isip.ExamPolicy",
        related_name="%(app_label)s_%(class)s_set",
        blank=True, null=True)

    ending = models.ForeignKey(
        "isip.ContractEnding",
        related_name="%(app_label)s_%(class)s_set",
        blank=True, null=True)
    date_ended = models.DateField(
        blank=True, null=True, verbose_name=_("date ended"))

    hidden_columns = 'date_decided date_issued \
    exam_policy user_asd ending date_ended signer1 signer2'

    def __unicode__(self):
        # ~ return u'%s # %s' % (self._meta.verbose_name,self.pk)
        # ~ return u'%s#%s (%s)' % (self.job.name,self.pk,
            #~ self.person.get_full_name(salutation=False))
        return u'%s#%s (%s)' % (self._meta.verbose_name, self.pk,
                                self.client.get_full_name(salutation=False))

    # backwards compat for document templates
    def get_person(self):
        return self.client
    person = property(get_person)

    def get_print_language(self):
        return self.language

    @dd.chooser()
    def ending_choices(cls):
        return ContractEnding.objects.filter(use_in_isip=True)

    def client_changed(self, ar):

        """If the contract's author is the client's primary coach, then set
        user_asd to None, otherwise set user_asd to the primary coach.
        We suppose that only integration agents write contracts.
        """

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

    def after_ui_save(self, ar):
        super(ContractBase, self).after_ui_save(ar)
        self.update_reminders(ar)

    def full_clean(self, *args, **kw):
        r = self.active_period()
        if not isrange(*r):
            raise ValidationError(_('Contract ends before it started.'))

        if self.type_id and self.type.exam_policy_id:
            if not self.exam_policy_id:
                self.exam_policy_id = self.type.exam_policy_id

        if self.client_id is not None:
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
        # Suggested evaluation events should be for the currently
        # responsible coach, not for the contract's author. This is
        # relevant if coach changes while contract is active.  See
        # :doc:`/tickets/104`
        d = evt.start_date
        coachings = evt.owner.client.get_coachings(
            (d, d), type__does_integ=True)
        if coachings.count() > 0:
            evt.user = coachings[0].user

    def update_cal_rset(self):
        return self.exam_policy

    def update_cal_from(self, ar):
        date = self.applies_from
        if not date:
            return None
        rset = self.update_cal_rset()
        return rset.get_next_suggested_date(ar, date)

    def update_cal_calendar(self):
        if self.exam_policy is not None:
            return self.exam_policy.event_type

    def update_cal_until(self):
        return self.date_ended or self.applies_until

    def update_cal_summary(self, i):
        ep = self.exam_policy
        if ep is not None and ep.event_type is not None:
            if ep.event_type.event_label:
                return ep.event_type.event_label + " " + str(i)
        return _("Evaluation %d") % i

    def update_reminders(self, ar):
        rv = super(ContractBase, self).update_reminders(ar)
        au = self.update_cal_until()
        if au:
            au = cal.DurationUnits.months.add_duration(au, -1)
        cal.update_auto_task(
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
        return rt.modules.aids.Granting.objects.get_by_aidtype(
            self.client, ap, **aidtype_filter)

    def get_aid_type(self):
        # may be used in `.odt` template for `isip.Contract`
        g = self.get_granting(is_integ_duty=True)
        if g is not None:
            return g.aid_type

    def suggest_cal_guests(self, event):
        # Automatic evaluation events have the client as mandatory
        # participant, plus possibly some other coach.
        Guest = rt.modules.cal.Guest
        GuestStates = rt.modules.cal.GuestStates
        st = GuestStates.accepted
        client = event.project
        yield Guest(event=event,
                    partner=client,
                    state=st,
                    role=settings.SITE.site_config.client_guestrole)

        period = (event.start_date, event.start_date)
        qs = client.get_coachings(period)
        qs = client.get_coachings(period, user__partner__isnull=False)
        for coaching in qs:
            role = coaching.type.eval_guestrole
            if role is not None:
                u = coaching.user
                if u != event.user and u.partner is not None:
                    yield Guest(event=event,
                                partner=u.partner,
                                role=role)

dd.update_field(ContractBase, 'signer1', default=default_signer1)
dd.update_field(ContractBase, 'signer2', default=default_signer2)


class ContractEvents(dd.ChoiceList):
    verbose_name = _("Observed event")
    verbose_name_plural = _("Observed events")
add = ContractEvents.add_item
add('10', _("Started"), 'started')
add('20', _("Active"), 'active')
add('30', _("Ended"), 'ended')
add('40', _("Signed"), 'signed')


class ContractBaseTable(dd.Table):
    parameters = dd.ObservedPeriod(
        user=dd.ForeignKey(settings.SITE.user_model, blank=True),

        observed_event=ContractEvents.field(
            blank=True, default=ContractEvents.active),

        ending_success=dd.YesNo.field(
            _("Successfully ended"),
            blank=True,
            help_text="""Contrats terminés avec succès."""),
        ending=models.ForeignKey(
            ContractEnding,
            blank=True, null=True,
            help_text="""Nur Konventionen mit diesem Beendigungsgrund."""),
        company=models.ForeignKey(
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
                qs = qs.filter(dd.inrange_filter('applies_until', period)
                               | dd.inrange_filter('date_ended', period))
            elif ce == ContractEvents.started:
                qs = qs.filter(dd.inrange_filter('applies_from', period))
            elif ce == ContractEvents.signed:
                qs = qs.filter(dd.inrange_filter('date_decided', period))
            elif ce == ContractEvents.active:
                f1 = Q(applies_until__isnull=True) | Q(
                    applies_until__gte=period[0])
                flt = f1 & (Q(date_ended__isnull=True) |
                            Q(date_ended__gte=period[0]))
                flt &= Q(applies_from__lte=period[1])
                qs = qs.filter(flt)
            else:
                raise Exception(repr(ce))

        if pv.ending_success == dd.YesNo.yes:
            qs = qs.filter(ending__isnull=False, ending__success=True)
        elif pv.ending_success == dd.YesNo.no:
            qs = qs.filter(ending__isnull=False, ending__success=False)

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
                yield "%s %s-%s" % (unicode(oe.text),
                                    dd.dtos(pv.start_date),
                                    dd.dtos(pv.end_date))

        if pv.company:
            yield unicode(pv.company)


class OverlappingContractsTest:
    """
    Volatile object used to test for overlapping contracts.
    """

    def __init__(self, client):
        """
        Test whether this client has overlapping contracts.
        """
        #~ from lino_welfare.modlib.isip.models import ContractBase
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
                return _("Date range overlaps with %(ctype)s #%(id)s") % dict(
                    ctype=con2.__class__._meta.verbose_name,
                    id=con2.pk
                )
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


class Contract(ContractBase):
    class Meta:
        verbose_name = _("ISIP")
        verbose_name_plural = _("ISIPs")

    type = models.ForeignKey(
        "isip.ContractType",
        related_name="%(app_label)s_%(class)s_set_by_type",
        verbose_name=_("Contract Type"), blank=True)

    stages = dd.RichTextField(
        _("stages"),
        blank=True, null=True, format='html')
    goals = dd.RichTextField(
        _("goals"),
        blank=True, null=True, format='html')
    duties_asd = dd.RichTextField(
        _("duties ASD"),
        blank=True, null=True, format='html')
    duties_dsbe = dd.RichTextField(
        _("duties DSBE"),
        blank=True, null=True, format='html')
    duties_person = dd.RichTextField(
        _("duties person"),
        blank=True, null=True, format='html')

    hidden_columns = (
        ContractBase.hidden_columns
        + " stages goals duties_asd duties_dsbe duties_person")

    study_type = models.ForeignKey('cv.StudyType', blank=True, null=True)

    @classmethod
    def get_certifiable_fields(cls):
        return """client type
        applies_from applies_until
        language
        stages goals duties_dsbe 
        duties_asd duties_person
        user user_asd exam_policy
        date_decided date_issued"""


dd.update_field(
    Contract, 'user',
    verbose_name=_("Integration agent"))  # was "responsible (DSBE)"


class ContractDetail(dd.FormLayout):
    general = dd.Panel("""
    id:8 client:25 type user:15 user_asd:15
    study_type applies_from applies_until exam_policy language:8
    date_decided date_issued printed date_ended ending:20
    PartnersByContract
    cal.TasksByController cal.EventsByController
    """, label=_("General"))

    isip = dd.Panel("""
    stages  goals
    duties_asd  duties_dsbe  duties_person
    """, label=_("ISIP"))

    main = "general isip"

    #~ def setup_handle(self,dh):
        #~ dh.general.label = _("General")
        #~ dh.isip.label = _("ISIP")


class Contracts(ContractBaseTable):
    required = dd.required(user_groups='integ')
    model = Contract
    column_names = 'id applies_from applies_until client user type *'
    order_by = ['id']
    detail_layout = ContractDetail()
    insert_layout = dd.FormLayout("""
    client
    type
    """, window_size=(60, 'auto'))

    parameters = dict(
        type=models.ForeignKey(ContractType, blank=True),
        study_type=models.ForeignKey('cv.StudyType', blank=True),
        **ContractBaseTable.parameters)

    params_layout = """
    user type start_date end_date observed_event
    company:20 study_type:15 ending_success:20 ending
    """

    @classmethod
    def get_request_queryset(cls, ar):
        #~ logger.info("20120608.get_request_queryset param_values = %r",ar.param_values)
        qs = super(Contracts, cls).get_request_queryset(ar)
        pv = ar.param_values
        if pv.company:
            qs = qs.filter(contractpartner__company=pv.company)
        if pv.study_type:
            qs = qs.filter(study_type=pv.study_type)
        return qs

    @classmethod
    def get_title_tags(self, ar):
        for t in super(Contracts, self).get_title_tags(ar):
            yield t

        if ar.param_values.study_type:
            yield unicode(ar.param_values.study_type)


class MyContracts(Contracts):

    @classmethod
    def param_defaults(self, ar, **kw):
        kw = super(MyContracts, self).param_defaults(ar, **kw)
        kw.update(user=ar.get_user())
        return kw


class ContractsByPerson(Contracts):
    master_key = 'client'
    column_names = 'applies_from applies_until user type *'


class ContractsByPolicy(Contracts):
    master_key = 'exam_policy'


class ContractsByType(Contracts):
    master_key = 'type'
    column_names = "applies_from client user id applies_until *"
    order_by = ["applies_from"]


class ContractsByEnding(Contracts):
    master_key = 'ending'


class ContractsByStudyType(Contracts):
    master_key = 'study_type'


class DelegatedTasksByContract(dd.Table):
    model = "cal.Task"
    master_key = "owner"
    column_names = "summary due_date"
    filter = models.Q(delegated=True)

    @classmethod
    def override_column_headers(self, ar, **kwargs):
        kwargs.update(summary=unicode(_("Proceedings")))
        return kwargs


class EventsByContract(dd.Table):
    model = "cal.Event"
    master_key = "owner"
    column_names = "summary start_date"

    @classmethod
    def override_column_headers(self, ar, **kwargs):
        kwargs.update(start_date=_("Date"))
        return kwargs


def site_setup(site):
    site.modules.cv.StudyTypes.set_detail_layout("""
    name education_level id
    isip.ContractsByStudyType
    cv.StudiesByType
    """)
