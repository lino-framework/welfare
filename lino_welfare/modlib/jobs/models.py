# -*- coding: UTF-8 -*-
# Copyright 2008-2014 Luc Saffre
# License: BSD (see file COPYING for details)

"""
Mises au travail (Conventions Article 60 §7 ou Art 61).

"""
from __future__ import unicode_literals

import logging
logger = logging.getLogger(__name__)

import cgi
import datetime
ONE_DAY = datetime.timedelta(days=1)

from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import pgettext_lazy as pgettext
from django.utils.encoding import force_unicode

from lino import dd, rt, mixins
from lino.utils.xmlgen.html import E
from lino.utils.htmlgen import UL
from lino.modlib.countries.models import CountryCity
from lino.modlib.cal.utils import DurationUnits

from lino.modlib.cv.mixins import SectorFunction

uploads = dd.resolve_app('uploads')
notes = dd.resolve_app('notes')
contacts = dd.resolve_app('contacts')
isip = dd.resolve_app('isip')
pcsw = dd.resolve_app('pcsw')
cv = dd.resolve_app('cv')


class Schedule(mixins.BabelNamed):

    """List of choices for `jobs.Contract.schedule` field."""
    class Meta:
        verbose_name = _("Work Schedule")
        verbose_name_plural = _('Work Schedules')


class Schedules(dd.Table):
    required = dd.required(user_groups='integ', user_level='manager')
    model = 'jobs.Schedule'
    order_by = ['name']
    detail_layout = """
    id name
    ContractsBySchedule
    """


class JobProvider(contacts.Company):

    """Stellenanbieter (BISA, BW, ...)
    """
    class Meta:
        app_label = 'jobs'
        verbose_name = _("Job Provider")
        verbose_name_plural = _('Job Providers')

    def disable_delete(self, ar):
        # skip the is_imported_partner test
        return super(contacts.Partner, self).disable_delete(ar)


class JobProviderDetail(contacts.CompanyDetail):

    """
    This is the same as CompanyDetail, except that we
    
    - remove MTI fields from `remark` panel
    - add a new tab `jobs`
    
    """
    box5 = "remarks"

    jobs = dd.Panel("""
    JobsByProvider
    ContractsByProvider
    """, label=_("Jobs"))

    main = "general notes jobs"

    #~ def setup_handle(self,lh):
        #~ pcsw.CompanyDetail.setup_handle(self,lh)
        #~ lh.jobs.label = _("Jobs")


#~ class JobProviders(pcsw.Companies,dd.Table):
class JobProviders(contacts.Companies, dd.Table):

    """
    List of Companies that have `Company.is_jobprovider` activated.
    """
    required = dd.required(user_groups='integ')
    #~ required_user_groups = ['integ']
    #~ required_user_level = UserLevels.manager
    #~ use_as_default_table = False
    model = JobProvider
    app_label = 'jobs'
    detail_layout = JobProviderDetail()


#
# CONTRACT TYPES
#
class ContractType(mixins.PrintableType, mixins.BabelNamed):

    """This is the homologue of :class:`welfare.isip.ContractType` (see
    there for general documentation).
    
    They are separated tables because ISIP contracts are in practice
    very different from JOBS contracts, and also their types should 
    not be mixed.

    """

    preferred_foreignkey_width = 20

    templates_group = 'jobs/Contract'

    class Meta:
        verbose_name = _("Job Contract Type")
        verbose_name_plural = _('Job Contract Types')
        ordering = ['name']

    ref = models.CharField(_("Reference"), max_length=20, blank=True)
    exam_policy = dd.ForeignKey(
        "isip.ExamPolicy",
        related_name="%(app_label)s_%(class)s_set",
        blank=True, null=True)


class ContractTypes(dd.Table):
    required = dd.required(user_groups='integ', user_level='manager')
    #~ required_user_groups = ['integ']
    #~ required_user_level = UserLevels.manager
    model = ContractType
    column_names = 'name ref *'
    detail_layout = """
    id name ref
    ContractsByType
    """


class Contract(isip.ContractBase, isip.ContractPartnerBase):

    """
    A Contract

    [NOTE1] If applies_from and duration are set, then the default value
    for applies_until is computed 26 workdays per month:

    - duration `312` -> 12 months
    - duration `468` -> 18 months
    - duration `624` -> 24 months

    """

    class Meta:
        verbose_name = _("Job contract")
        verbose_name_plural = _('Job contracts')

    type = models.ForeignKey(
        "jobs.ContractType",
        related_name="%(app_label)s_%(class)s_set_by_type",
        blank=True)

    job = models.ForeignKey("jobs.Job")
    duration = models.IntegerField(_("duration (days)"),
                                   blank=True, null=True, default=None)
    regime = dd.ForeignKey('cv.Regime', blank=True, null=True)
    schedule = dd.ForeignKey('jobs.Schedule', blank=True, null=True)
    hourly_rate = dd.PriceField(_("hourly rate"), blank=True, null=True)
    refund_rate = models.CharField(_("refund rate"), max_length=200,
                                   blank=True)
    reference_person = models.CharField(_("reference person"), max_length=200,
                                        blank=True)
    responsibilities = dd.RichTextField(_("responsibilities"),
                                        blank=True, null=True, format='html')
    remark = models.TextField(_("Remark"), blank=True)

    @dd.chooser()
    def company_choices(cls):
        return JobProvider.objects.all()

    @dd.chooser()
    def ending_choices(cls):
        return isip.ContractEnding.objects.filter(use_in_jobs=True)

    @dd.chooser(simple_values=True)
    def duration_choices(cls):
        return [312, 468, 624]

    @dd.chooser(simple_values=True)
    def refund_rate_choices(cls):
        return [
            u"0%",
            u"25%",
            u"50%",
            u"100%",
        ]

    def disabled_fields(self, ar):
        "As super, but add also job provider's company and type"
        df = super(Contract, self).disabled_fields(ar)
        if self.job_id is not None:
            if self.job.provider:
                df.add('company')
            if self.job.contract_type:
                df.add('type')
        return df

    def after_ui_save(self, ar):
        super(Contract, self).after_ui_save(ar)
        if self.job_id is not None:
            if self.applies_until and self.applies_until > settings.SITE.today():
                n = 0
                for candi in self.client.candidature_set.filter(
                        state=CandidatureStates.active):
                    candi.state = CandidatureStates.inactive
                    candi.save()
                    n += 1
                if n:
                    ar.info(unicode(
                        _("(%d candidatures have been marked inactive)")) % n)
                    ar.set_response(alert=_("Success"))

    def full_clean(self, *args, **kw):
        if self.client_id is not None:
            if self.applies_from:
                if self.client.birth_date:
                    def duration(refdate):
                        if type(refdate) != datetime.date:
                            raise Exception("%r is not a date!" % refdate)
                        delta = refdate - self.client.birth_date.as_date()
                        age = delta.days / 365
                        if age < 36:
                            return 312
                        elif age < 50:
                            return 468
                        else:
                            return 624

                    if self.duration is None:
                        if self.applies_until:
                            self.duration = duration(self.applies_until)
                        else:
                            self.duration = duration(self.applies_from)
                            self.applies_until = self.applies_from + \
                                datetime.timedelta(days=self.duration)

                if self.duration and not self.applies_until:
                    # [NOTE1]
                    self.applies_until = DurationUnits.months.add_duration(
                        self.applies_from, self.duration / 26) - ONE_DAY

        if self.job_id is not None:
            if self.job.provider is not None:
                self.company = self.job.provider
            if self.job.contract_type is not None:
                self.type = self.job.contract_type
            if self.hourly_rate is None:
                self.hourly_rate = self.job.hourly_rate

        super(Contract, self).full_clean(*args, **kw)

    @classmethod
    def get_certifiable_fields(cls):
        return (
            'client job company contact_person contact_role type '
            'applies_from applies_until duration '
            'language schedule regime hourly_rate refund_rate '
            'reference_person responsibilities '
            'user user_asd exam_policy '
            'date_decided date_issued ')


dd.update_field(Contract, 'user', verbose_name=_("responsible (IS)"))


class ContractDetail(dd.FormLayout):
    box1 = """
    id:8 client:25 user:15 user_asd:15 language:8
    job type company contact_person contact_role
    applies_from duration applies_until exam_policy
    regime:20 schedule:30 hourly_rate:10 refund_rate:10
    reference_person printed
    date_decided date_issued date_ended ending:20
    # signer1 signer2
    responsibilities
    """

    right = """
    cal.EventsByController
    cal.TasksByController
    """

    main = """
    box1:70 right:30
    """


class Contracts(isip.ContractBaseTable):
    #~ debug_permissions = "20130222"
    required = dd.required(user_groups='integ')
    #~ required_user_groups = ['integ']
    #~ required_user_level = UserLevels.manager
    model = Contract
    column_names = 'id job applies_from applies_until user type *'
    order_by = ['id']
    active_fields = 'job company contact_person contact_role'
    detail_layout = ContractDetail()
    insert_layout = dd.FormLayout("""
    client
    job
    """, window_size=(60, 'auto'))

    parameters = dict(
        type=models.ForeignKey(
            'jobs.ContractType', blank=True,
            verbose_name=_("Only contracts of type")),
        **isip.ContractBaseTable.parameters)

    params_layout = """
    user type start_date end_date observed_event
    company ending_success ending
    """

    @classmethod
    def get_request_queryset(cls, ar):
        qs = super(Contracts, cls).get_request_queryset(ar)
        pv = ar.param_values
        if pv.company:
            qs = qs.filter(company=pv.company)
        return qs


class ContractsByPerson(Contracts):

    """
    """
    master_key = 'client'
    auto_fit_column_widths = True
    column_names = 'job applies_from applies_until user type *'
    hidden_columns = """
    language contact_person contact_role
    printed regime schedule hourly_rate
    date_decided date_issued user_asd exam_policy ending date_ended
    duration reference_person responsibilities remark
    """


class ContractsByProvider(Contracts):
    master_key = 'company'
    column_names = 'client job applies_from applies_until user type *'


class ContractsByPolicy(Contracts):
    master_key = 'exam_policy'


class ContractsByType(Contracts):
    master_key = 'type'
    column_names = "applies_from client job user *"
    order_by = ["applies_from"]


class ContractsByEnding(Contracts):
    master_key = 'ending'


class ContractsByJob(Contracts):
    column_names = 'client applies_from applies_until user type *'
    master_key = 'job'


class ContractsByRegime(Contracts):
    """
    Shows Job Contracts for a given Regime.
    """
    master_key = 'regime'
    column_names = 'job applies_from applies_until user type *'


class ContractsBySchedule(Contracts):
    master_key = 'schedule'
    column_names = 'job applies_from applies_until user type *'


class MyContracts(Contracts):
    column_names = "applies_from client job type company applies_until date_ended ending *"
    #~ label = _("My contracts")
    #~ order_by = "reminder_date"
    #~ column_names = "reminder_date client company *"
    #~ order_by = ["applies_from"]
    #~ filter = dict(reminder_date__isnull=False)

    @classmethod
    def param_defaults(self, ar, **kw):
        kw = super(MyContracts, self).param_defaults(ar, **kw)
        kw.update(user=ar.get_user())
        return kw


class Offer(SectorFunction):

    "A Job Offer"
    class Meta:
        verbose_name = _("Job Offer")
        verbose_name_plural = _('Job Offers')
        ordering = ['name']

    name = models.CharField(max_length=100,
                            blank=True,
                            verbose_name=_("Name"))

    provider = models.ForeignKey(JobProvider,
                                 blank=True, null=True)

    selection_from = models.DateField(_("selection from"),
                                      blank=True, null=True)
    selection_until = models.DateField(_("selection until"),
                                       blank=True, null=True)
    start_date = models.DateField(_("start date"),
                                  blank=True, null=True)

    remark = dd.RichTextField(
        blank=True,
        verbose_name=_("Remark"),
        format='plain')

    def __unicode__(self):
        if self.name:
            return self.name
        return u'%s @ %s' % (self.function, self.provider)


class Offers(dd.Table):
    required = dd.required(user_groups='integ')
    #~ required_user_groups = ['integ']
    #~ required_user_level = UserLevels.manager
    model = Offer
    detail_layout = """
    name provider sector function
    selection_from selection_until start_date
    remark
    ExperiencesByOffer CandidaturesByOffer
    """


class Job(SectorFunction):

    """
    A place where a Client can work. The Job Provider
    
    """

    preferred_foreignkey_width = 20

    class Meta:
        verbose_name = _("Job")
        verbose_name_plural = _('Jobs')
        ordering = ['name']

    name = models.CharField(max_length=100,
                            verbose_name=_("Name"))

    type = models.ForeignKey("jobs.JobType",
                             blank=True, null=True,
                             verbose_name=_("Job Type"))

    provider = models.ForeignKey('jobs.JobProvider',
                                 blank=True, null=True)

    contract_type = models.ForeignKey('jobs.ContractType',
                                      blank=True, null=True,
                                      verbose_name=_("Contract Type"))

    hourly_rate = dd.PriceField(_("hourly rate"), blank=True, null=True)

    capacity = models.IntegerField(_("capacity"),
                                   default=1)

    remark = models.TextField(
        blank=True,
        verbose_name=_("Remark"))

    def __unicode__(self):
        if self.provider:
            return _('%(job)s at %(provider)s') % dict(
                job=self.name, provider=self.provider.name)
        return self.name

    def unused_disabled_fields(self, ar):
        # disabled 20140519. must convert this to Certifiable
        if self.contract_set.filter(build_time__isnull=False).count():
            return set(('contract_type', 'provider'))
        return set()


    #~ @dd.chooser()
    #~ def provider_choices(cls):
        #~ return CourseProviders.request().queryset

    #~ @classmethod
    #~ def setup_report(model,rpt):
        #~ rpt.add_action(DirectPrintAction('candidates',_("List of candidates"),'courses/candidates.odt'))
        #~ rpt.add_action(DirectPrintAction('participants',_("List of participants"),'courses/participants.odt'))

    #~ def get_print_language(self,pm):
        #~ "Used by DirectPrintAction"
        #~ return DEFAULT_LANGUAGE

    #~ def participants(self):
        #~ u"""
        #~ Liste von :class:`CourseRequest`-Instanzen,
        #~ die in diesem Kurs eingetragen sind.
        #~ """
        #~ return ParticipantsByCourse().request(master_instance=self)

    #~ def candidates(self):
        #~ u"""
        #~ Liste von :class:`CourseRequest`-Instanzen,
        #~ die noch in keinem Kurs eingetragen sind, aber für diesen Kurs in Frage
        #~ kommen.
        #~ """
        #~ return CandidatesByCourse().request(master_instance=self)


#~ class Wish(SectorFunction):
    #~ class Meta:
        #~ verbose_name = _("Job Wish")
        #~ verbose_name_plural = _('Job Wishes')
    #~ person = models.ForeignKey("contacts.Person")

#~ class Wishes(dd.Table):
    #~ model = Wish

#~ class WishesByPerson(Wishes):
    #~ master_key = 'person'

#~ class WishesBySector(Wishes):
    #~ master_key = 'sector'

#~ class WishesByFunction(Wishes):
    #~ master_key = 'function'


#~ class WishesByOffer(dd.Table):
    #~ """
    #~ Shows the persons that whish this Offer.

    #~ It is a slave report without
    #~ :attr:`master_key <lino.dd.Table.master_key>`,
    #~ which is allowed only because it also overrides
    #~ :meth:`get_request_queryset`
    #~ """

    #~ model = Wish
    #~ master = Offer
    #~ label = _("Candidate Job Wishes")

    #~ can_add = perms.never
    #~ can_change = perms.never

    #~ def get_request_queryset(self,rr):
        #~ """
        #~ Needed because the Offer is not the direct master.
        #~ """
        #~ offer = rr.master_instance
        #~ if offer is None:
            #~ return []
        #~ kw = {}
        #~ qs = self.model.objects.order_by('date_submitted')

        #~ if offer.function:
            #~ qs = qs.filter(function=offer.function)
        #~ if offer.sector:
            #~ qs = qs.filter(sector=offer.sector)

        #~ return qs

class CandidatureStates(dd.ChoiceList):
    help_text = _("The possible states of a candidature.")
    verbose_name = _("Candidature state")
    verbose_name_plural = _("Candidature states")

add = CandidatureStates.add_item
add('10', pgettext("jobs", "Active"), 'active')
add('20', _("Probation"), 'probation')
add('25', _("Probation failed"), 'failed')
add('27', pgettext("jobs", "Working"), 'working')
add('30', pgettext("jobs", "Inactive"), 'inactive')


class Candidature(SectorFunction):

    """
    A candidature is when a Client applies for a known :class:`Job`.
    
    """
    class Meta:
        verbose_name = _("Job Candidature")
        verbose_name_plural = _('Job Candidatures')
        get_latest_by = 'date_submitted'

    #~ person = models.ForeignKey(settings.SITE.person_model)
    person = models.ForeignKey('pcsw.Client')

    job = models.ForeignKey("jobs.Job",
                            blank=True, null=True)
        #~ verbose_name=_("Requested Job"))

    #~ date_submitted = models.DateField(_("date submitted"),auto_now_add=True)
    date_submitted = models.DateField(_("date submitted"),
                                      help_text=_("Date when the IA introduced this candidature."))
    #~ u"Datum, an dem die Anfrage erstellt wurde."

    #~ contract = models.ForeignKey("jobs.Contract",blank=True,null=True,
        #~ verbose_name=_("Contract found"))
    #~ u"""
    #~ Der Vertrag, durch den diese Anfrage befriedigt wurde
    #~ (ein Objekt vom Typ :class:`Contract`).
    #~ So lange dieses Feld leer ist, gilt die Anfrage als offen.
    #~ """

    remark = models.TextField(
        blank=True, null=True,
        verbose_name=_("Remark"))

    #~ active = models.BooleanField(_("Active"),default=True)
    state = CandidatureStates.field(default=CandidatureStates.active)

    def __unicode__(self):
        return force_unicode(_('Candidature by %(person)s') % dict(
            person=self.person.get_full_name(salutation=False)))

    #~ @dd.chooser()
    #~ def contract_choices(cls,job,person):
        #~ if person and job:
            #~ return person.contract_set.filter(job=job)
        #~ return []

    #~ def clean(self,*args,**kw):
        #~ if self.contract:
            #~ if self.contract.person != self.person:
                #~ raise ValidationError(
                  #~ "Cannot satisfy a Candidature with a Contract on another Person")
        #~ super(Candidature,self).clean(*args,**kw)

    def on_create(self, ar):
        self.date_submitted = settings.SITE.today()
        super(Candidature, self).on_create(ar)


class Candidatures(dd.Table):

    """
    List of :class:`Candidatures <Candidature>`.
    """
    required = dd.required(user_groups='integ', user_level='manager')
    #~ required_user_groups = ['integ']
    #~ required_user_level = UserLevels.manager
    model = Candidature
    order_by = ['date_submitted']
    column_names = 'date_submitted job:25 state * id'


class CandidaturesByPerson(Candidatures):

    """
    ...
    """
    required = dd.required(user_groups='integ')
    #~ required_user_level = None
    master_key = 'person'
    hidden_columns = 'id'
    auto_fit_column_widths = True


class CandidaturesBySector(Candidatures):
    master_key = 'sector'


class CandidaturesByFunction(Candidatures):
    master_key = 'function'


class CandidaturesByJob(Candidatures):
    required = dd.required(user_groups='integ')
    #~ required_user_level = None
    master_key = 'job'
    column_names = 'date_submitted person:25 state * id'

    @classmethod
    def create_instance(self, req, **kw):
        obj = super(CandidaturesByJob, self).create_instance(req, **kw)
        if obj.job is not None:
            obj.type = obj.job.type
        return obj


class SectorFunctionByOffer(dd.Table):

    """Shows the Candidatures or Experiences for this Offer.
    
    It is a slave report without :attr:`master_key
    <dd.Table.master_key>`, which is allowed only because it overrides
    :meth:`dd.Table.get_request_queryset`.

    """
    master = Offer

    @classmethod
    def get_request_queryset(self, rr):
        """
        Needed because the Offer is not the direct master.
        """
        offer = rr.master_instance
        if offer is None:
            return []
        kw = {}
        #~ qs = self.model.objects.order_by('date_submitted')
        qs = self.model.objects.order_by(self.model._meta.get_latest_by)

        if offer.function:
            qs = qs.filter(function=offer.function)
        if offer.sector:
            qs = qs.filter(sector=offer.sector)

        #~ required_id_sets = []

        #~ if offer.function:
            #~ q = JobRequest.objects.filter(function=offer.function)
            #~ required_id_sets.append(set(q.values_list('person__id',flat=True)))
        #~ if offer.sector:
            #~ q = JobRequest.objects.filter(sector=offer.sector)
            #~ required_id_sets.append(set(q.values_list('person__id',flat=True)))

        #~ if required_id_sets:
            #~ s = set(required_id_sets[0])
            #~ for i in required_id_sets[1:]:
                #~ s.intersection_update(i)
                # ~ # keep only elements found in both s and i.
            #~ qs = qs.filter(id__in=s)

        return qs


class CandidaturesByOffer(SectorFunctionByOffer):
    model = Candidature
    label = _("Candidates")
    column_names = "date_submitted  person job state"


class ExperiencesByOffer(SectorFunctionByOffer):
    model = 'cv.Experience'
    label = _("Experiences")
    column_names = "start_date end_date person company country"


class Jobs(dd.Table):
    help_text = _("""
    Eine Stelle ist ein Arbeitsplatz bei einem Stellenabieter.
    """)
    required = dd.required(user_groups='integ')
    #~ required_user_groups = ['integ']
    #~ required_user_level = UserLevels.manager
    model = Job
    #~ order_by = ['start_date']
    column_names = 'name provider * id'

    detail_layout = """
    name provider contract_type type id
    sector function capacity hourly_rate
    remark CandidaturesByJob
    ContractsByJob
    """


class JobType(mixins.Sequenced):

    """
    The list of Job Types is used for statistical analysis,
    e.g. in :class:``
    """

    class Meta:
        verbose_name = _("Job Type")
        verbose_name_plural = _('Job Types')

    name = models.CharField(max_length=200,
                            blank=True,
                            verbose_name=_("Designation"))

    remark = models.CharField(_("Remark"), max_length=200, blank=True)
    is_social = models.BooleanField(_("Social economy"), default=False)

    def __unicode__(self):
        return unicode(self.name)


class JobTypes(dd.Table):
    required = dd.required(user_groups='integ', user_level='manager')
    model = JobType
    order_by = ['name']
    detail_layout = """
    id name is_social
    JobsByType
    """


class JobsByProvider(Jobs):
    master_key = 'provider'


class JobsByType(Jobs):
    master_key = 'type'


if True:  # settings.SITE.user_model:

    from lino.core.dbutils import resolve_model, UnresolvedModel
    #~ USER_MODEL = resolve_model(settings.SITE.user_model)

    class ContractsSearch(Contracts):

        """
        Shows the Job contracts owned by this user.
        """
        label = _("Job Contracts Search")
        group_by = ['client__group']
        column_names = 'id applies_from applies_until job client client__city client__national_id client__gender user type *'

        use_as_default_table = False

        def on_group_break(self, group):
            if group == 0:
                yield self.total_line(0)
            else:
                yield self.total_line(group)

        def total_line(self, group):
            return


COLS = 8


class OldJobsOverview(mixins.EmptyTable):

    """
    """
    required = dd.required(user_groups=['integ'])
    label = _("Contracts Situation")
    #~ detail_layout = JobsOverviewDetail()
    detail_layout = "body"

    parameters = dict(
        #~ date = models.DateField(default=settings.SITE.today,blank=True,null=True),
        date=models.DateField(blank=True, null=True, verbose_name=_("Date")),
        contract_type=models.ForeignKey(ContractType, blank=True, null=True),
        job_type=models.ForeignKey(JobType, blank=True, null=True),
    )
    params_panel_hidden = True

    #~ @dd.displayfield(_("Body"))
    @dd.virtualfield(dd.HtmlBox())
    def body(cls, self, ar):
        #~ logger.info("20120221 3 body(%s)",req)
        #~ logger.info("Waiting 5 seconds...")
        #~ time.sleep(5)
        #~ today = self.date or settings.SITE.today()
        today = ar.param_values.date or settings.SITE.today()
        period = (today, today)
        html = ''
        rows = []

        if ar.param_values.job_type:
            jobtypes = [ar.param_values.job_type]
        else:
            jobtypes = JobType.objects.all()
        for jobtype in jobtypes:
            cells = []
            #~ for job in jobtype.job_set.all():
            for job in jobtype.job_set.order_by('provider'):
                working = []
                candidates = []
                probation = []
                #~ qs = job.contract_set.all()
                qs = job.contract_set.order_by('applies_from')
                if ar.param_values.contract_type:
                    qs = qs.filter(type=ar.param_values.contract_type)
                for ct in qs:
                    if ct.applies_from:
                        until = ct.date_ended or ct.applies_until
                        if not until or (ct.applies_from <= today and until >= today):
                            working.append(ct)

                qs = job.candidature_set.order_by('date_submitted').filter(
                    state=CandidatureStates.active)
                qs = pcsw.only_coached_on(qs, period, 'person')
                for cand in qs:
                    candidates.append(cand)

                qs = job.candidature_set.order_by('date_submitted').filter(
                    state=CandidatureStates.probation)
                qs = pcsw.only_coached_on(qs, period, 'person')
                for cand in qs:
                    probation.append(cand)

                if candidates + working + probation:
                    s = "<p>"
                    s += "<b>%s (%s)</b>" % (
                        cgi.escape(unicode(job)), job.capacity)
                    if job.remark:
                        s += " <i>%s</i>" % cgi.escape(job.remark)
                    s += "</p>"
                    s += UL(['%s bis %s' % (
                        ct.person.last_name.upper(),
                        dd.dtos(ct.applies_until)
                    ) for ct in working])
                    if candidates:
                        s += "<p>%s:</p>" % cgi.escape(unicode(_("Candidates")))
                        s += UL([i.person for i in candidates])
                    if probation:
                        s += "<p>%s:</p>" % cgi.escape(unicode(_("Probation")))
                        s += UL([i.person for i in probation])
                    cells.append(s)
            if cells:
                html += '<h1>%s</h1>' % cgi.escape(unicode(jobtype))
                #~ head = ''.join(['<col width="30" />' for c in cells])
                #~ head = '<colgroup>%s</colgroup>' % head
                s = ''.join(['<td valign="top">%s</td>' % c for c in cells])
                s = '<tr>%s</tr>' % s
                #~ s = head + s
                html += '<table border="1" width="100%%">%s</table>' % s
        html = '<div class="htmlText">%s</div>' % html
        #~ logger.info(html[46:58])
        #~ html = str(html)
        #~ assert type(html) == type('')
        return html


class JobsOverviewByType(Jobs):

    """
    """
    required = dd.required(user_groups=['integ'])
    label = _("Contracts Situation")
    column_names = "job_desc:20 working:30 probation:30 candidates:30"
    master_key = 'type'

    parameters = dict(
        date=models.DateField(blank=True, null=True, verbose_name=_("Date")),
        contract_type=models.ForeignKey(ContractType, blank=True, null=True),
        #~ job_type = models.ForeignKey(JobType,blank=True,null=True),
    )

    params_panel_hidden = True

    @dd.displayfield(_("Job"))
    def job_desc(self, obj, ar):
        chunks = [ar.obj2html(obj, unicode(obj.function))]
        chunks.append(pgettext("(place)", " at "))
        chunks.append(ar.obj2html(obj.provider))
        chunks.append(' (%d)' % obj.capacity)
        if obj.remark:
            chunks.append(' ')
            chunks.append(E.i(obj.remark))
        return E.p(*chunks)

    @dd.displayfield(pgettext("jobs", "Working"))
    def working(self, obj, ar):
        return obj._working

    @dd.displayfield(_("Candidates"))
    def candidates(self, obj, ar):
        return obj._candidates

    @dd.displayfield(_("Probation"))
    def probation(self, obj, ar):
        return obj._probation

    @classmethod
    def get_data_rows(self, ar):
        """
        """
        data_rows = self.get_request_queryset(ar)

        today = ar.param_values.date or settings.SITE.today()
        period = (today, today)

        def UL(items):
            #~ return E.ul(*[E.li(i) for i in items])
            newitems = []
            first = True
            for i in items:
                if first:
                    first = False
                else:
                    newitems.append(E.br())
                newitems.append(i)
            return E.p(*newitems)

        for job in data_rows:
            showit = False
            working = []
            qs = job.contract_set.order_by('applies_from')
            if ar.param_values.contract_type:
                qs = qs.filter(type=ar.param_values.contract_type)
            for ct in qs:
                if ct.applies_from:
                    until = ct.date_ended or ct.applies_until
                    if not until or (
                            ct.applies_from <= today and until >= today):
                        working.append(ct)
            if len(working) > 0:
                job._working = UL([
                    E.span(
                        #~ ar.obj2html(ct.person,ct.person.last_name.upper()),
                        ar.obj2html(ct.person),
                        # pgettext("(place)", " at ")
                        # + unicode(ct.company.name),
                        ' bis %s' % dd.dtos(ct.applies_until)
                    )
                    for ct in working])
                showit = True
            else:
                job._working = ''

            candidates = []
            qs = job.candidature_set.order_by('date_submitted').filter(
                state=CandidatureStates.active)
            qs = pcsw.only_coached_on(qs, period, 'person')
            for cand in qs:
                candidates.append(cand)
            if candidates:
                job._candidates = UL([
                    #~ ar.obj2html(i.person,i.person.last_name.upper())
                    ar.obj2html(i.person)
                    for i in candidates])
                showit = True
            else:
                job._candidates = ''

            probation = []
            qs = job.candidature_set.order_by('date_submitted').filter(
                state=CandidatureStates.probation)
            qs = pcsw.only_coached_on(qs, period, 'person')
            for cand in qs:
                probation.append(cand)
            if probation:
                job._probation = UL([
                    #~ E.span(ar.obj2html(i.person,i.person.last_name.upper()))
                    E.span(ar.obj2html(i.person))
                    for i in probation])
                showit = True
            else:
                job._probation = ''

            if showit:
                yield job


class JobsOverview(mixins.EmptyTable):

    """
    New version of `welfare.jobs.JobsOverview`.
    """
    required = dd.required(user_groups=['integ'])
    label = _("Contracts Situation")
    #~ detail_layout = JobsOverviewDetail()
    detail_layout = "preview"

    parameters = dict(
        today=models.DateField(
            blank=True, null=True, verbose_name=_("Date")),
        #~ contract_type = models.ForeignKey(ContractType,blank=True,null=True),
        job_type=models.ForeignKey(JobType, blank=True, null=True),
    )
    params_panel_hidden = True

    @classmethod
    def create_instance(self, ar, **kw):
        kw.update(today=ar.param_values.today or settings.SITE.today())
        if ar.param_values.job_type:
            kw.update(jobtypes=[ar.param_values.job_type])
        else:
            kw.update(jobtypes=JobType.objects.all())
        return super(JobsOverview, self).create_instance(ar, **kw)

    @dd.virtualfield(dd.HtmlBox())
    def preview(cls, self, ar):
        #~ logger.info("20130723 preview %s",self.jobtypes)
        html = []
        for jobtype in self.jobtypes:
            html.append(E.h2(unicode(jobtype)))
            sar = ar.spawn(JobsOverviewByType,
                           master_instance=jobtype,
                           param_values=dict(date=self.today))
            html.append(sar.table2xhtml())
        #~ logger.info("20130723 preview %s",html)
        #~ return E.div(*html,class_='htmlText')
        return E.div(*html)

    @classmethod
    def to_rst(self, ar, column_names=None, **kwargs):
        obj = self.create_instance(ar)
        return """\
        .. raw:: html
        
           %s
        """ % E.tostring(obj.preview).replace('\n', ' ')


dd.inject_field(
    contacts.Company, 'is_jobprovider',
    dd.EnableChild(
        'jobs.JobProvider',
        verbose_name=_("is Job Provider"),
        help_text=_("Whether this Company is also a Job Provider.")))


@dd.receiver(dd.post_analyze)
def set_detail_layouts(sender=None, **kwargs):
    rt.modules.cv.Regimes.set_detail_layout("""
    id name
    cv.ExperiencesByRegime
    jobs.ContractsByRegime
    """)
