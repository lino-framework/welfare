# -*- coding: UTF-8 -*-
# Copyright 2008-2020 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

import cgi
import datetime

from django.db import models
from django.db.models import Q
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.text import format_lazy
from django.utils import translation
from django.contrib.humanize.templatetags.humanize import naturaltime

from lino.utils import join_elems
from etgen.html import E

from lino.api import dd, rt, _
from lino.core.utils import get_field

from lino_xl.lib.cal.utils import update_reminder
from lino_xl.lib.cal.choicelists import DurationUnits
from lino_xl.lib.coachings.mixins import ClientChecker
from lino.modlib.uploads.choicelists import Shortcuts
from lino.modlib.uploads.mixins import UploadController

from lino_xl.lib.notes.choicelists import SpecialTypes
from lino_xl.lib.notes.mixins import Notable
from lino_welfare.modlib.dupable_clients.mixins import DupableClient

cal = dd.resolve_app('cal')
# contacts = dd.resolve_app('contacts')
from lino_welfare.modlib.contacts import models as contacts
cv = dd.resolve_app('cv')
uploads = dd.resolve_app('uploads')
from lino_xl.lib.beid.mixins import BeIdCardHolder
# from lino.modlib.vatless.mixins import PartnerDetailMixin

from lino_xl.lib.contacts.roles import SimpleContactsUser
# from lino.modlib.office.roles import OfficeOperator

from lino_welfare.modlib.newcomers.roles import (NewcomersUser,
                                                 NewcomersOperator)
from lino_welfare.modlib.integ.roles import IntegUser
from lino_welfare.modlib.cbss.choicelists import OK_STATES

from lino.utils import ssin

from lino import mixins
from lino.utils.dates import daterange_text

from lino_xl.lib.contacts.choicelists import CivilStates
from lino_xl.lib.beid.choicelists import ResidenceTypes
from lino_xl.lib.clients.choicelists import ClientEvents, ClientStates
from lino_xl.lib.coachings.utils import add_coachings_filter
from lino_xl.lib.coachings.mixins import Coachable
from lino_xl.lib.cv.mixins import BiographyOwner

from .roles import SocialUser, SocialStaff
from .choicelists import RefusalReasons

from .actions import RefuseClient, MarkClientFormer



class Client(contacts.Person, BiographyOwner, BeIdCardHolder,
             DupableClient, Coachable, Notable, UploadController):

    class Meta:
        app_label = 'pcsw'
        verbose_name = _("Client")
        verbose_name_plural = _("Clients")
        abstract = dd.is_abstract_model(__name__, 'Client')
        #~ ordering = ['last_name','first_name']

    quick_search_fields = "prefix name phone gsm street national_id"

    group = dd.ForeignKey("pcsw.PersonGroup", blank=True, null=True,
                          verbose_name=_("Integration phase"))

    civil_state = CivilStates.field(blank=True)

    residence_type = ResidenceTypes.field(blank=True)

    in_belgium_since = models.DateField(
        _("Lives in Belgium since"), blank=True, null=True)
    residence_until = models.DateField(
        _("Residence until"), blank=True, null=True)
    unemployed_since = models.DateField(
        _("Unemployed since"), blank=True, null=True,
        help_text=_("Since when the client has not been employed "
                    "in any regular job."))
    seeking_since = models.DateField(
        _("Seeking work since"), blank=True, null=True,
        help_text=_("Since when the client is seeking for a job."))
    needs_residence_permit = models.BooleanField(
        _("Needs residence permit"), default=False)
    needs_work_permit = models.BooleanField(
        _("Needs work permit"), default=False)
    work_permit_suspended_until = models.DateField(
        blank=True, null=True, verbose_name=_("suspended until"))
    aid_type = dd.ForeignKey("pcsw.AidType", blank=True, null=True)
        #~ verbose_name=_("aid type"))

    declared_name = models.BooleanField(_("Declared name"), default=False)

    is_seeking = models.BooleanField(_("is seeking work"), default=False)
    # removed in chatelet, maybe soon also in Eupen (replaced by seeking_since)

    unavailable_until = models.DateField(
        blank=True, null=True, verbose_name=_("Unavailable until"))
    unavailable_why = models.CharField(max_length=100,
                                       blank=True,  # null=True,
                                       verbose_name=_("Reason"))

    obstacles = models.TextField(_("Other obstacles"), blank=True, null=True)
    skills = models.TextField(_("Other skills"), blank=True, null=True)

    job_office_contact = dd.ForeignKey(
        "contacts.Role",
        blank=True, null=True,
        verbose_name=_(
            "Contact person at local job office"),
        related_name='persons_job_office')

    refusal_reason = RefusalReasons.field(blank=True)

    mark_former = MarkClientFormer()
    refuse_client = RefuseClient()

    mails_by_project = dd.ShowSlaveTable(
        'outbox.MailsByProject',
        sort_index=100,
        icon_name="transmit")

    @classmethod
    def on_analyze(cls, site):
        super(Client, cls).on_analyze(site)
        cls.declare_imported_fields(
            '''zip_code city country street street_no street_box
            birth_place language
            phone fax email
            card_type card_number card_valid_from card_valid_until
            noble_condition card_issuer
            national_id nationality
            ''')  # coach1

    def disabled_fields(self, ar):
        rv = super(Client, self).disabled_fields(ar)
        if not ar.get_user().user_type.has_required_roles(
                [NewcomersOperator]):
            rv = rv | set(['broker', 'faculty', 'refusal_reason'])
        #~ logger.info("20130808 pcsw %s", rv)
        return rv

    @classmethod
    def get_request_queryset(cls, *ar, **kwargs):
        qs = super(Client, cls).get_request_queryset(*ar, **kwargs)
        return qs.select_related('country', 'city', 'nationality')

    def get_excerpt_options(self, ar, **kw):
        # Set project field when creating an excerpt from Client.
        kw.update(project=self)
        return super(Client, self).get_excerpt_options(ar, **kw)

    def get_first_meeting(self, today=None):
        if today is None:
            today = dd.today()
        qs = SpecialTypes.first_meeting.get_notes(
            project=self, date__lte=today).order_by('date', 'time')
        # qs = self.notes_note_set_by_project.order_by('date', 'time')
        # nt = rt.models.notes.NoteType.objects.get(id=note_type)
        # qs = qs.filter(type=nt)
        if qs.count():
            return qs.reverse()[0]

    @dd.chooser()
    def job_office_contact_choices(cls):
        sc = settings.SITE.site_config  # get_site_config()
        if sc.job_office is not None:
            #~ return sc.job_office.contact_set.all()
            #~ return sc.job_office.rolesbyparent.all()
            return sc.job_office.rolesbycompany.all()
            #~ return links.Link.objects.filter(a=sc.job_office)
        return []

    def __str__(self):
        if self.is_obsolete:
            return "%s %s (%s*)" % (
                self.last_name.upper(), self.first_name, self.pk)
        return "%s %s (%s)" % (
            self.last_name.upper(), self.first_name, self.pk)

    def get_overview_elems(self, ar):
        elems = super(Client, self).get_overview_elems(ar)
        # elems.append(E.br())
        elems.append(ar.get_data_value(self, 'eid_info'))
        notes = []
        for note in rt.models.notes.Note.objects.filter(
                project=self, important=True):
            notes.append(E.b(ar.obj2html(note, note.subject)))
        if len(notes):
            notes = join_elems(notes, " / ")
            elems += E.p(*notes, **{'class':"lino-info-red"})
        return elems

    def update_owned_instance(self, owned):
        owned.project = self
        super(Client, self).update_owned_instance(owned)

    def full_clean(self, *args, **kw):
        if self.job_office_contact:
            if self.job_office_contact.person_id == self.id:
                raise ValidationError(_("Circular reference"))
        if False:
            if self.national_id:
                ssin.ssin_validator(self.national_id)
        #~ if not self.national_id:
            #~ self.national_id = str(self.id)
        if False:  # Regel deaktiviert seit 20121207
            if self.client_state == ClientStates.coached:
                ssin.ssin_validator(self.national_id)
        super(Client, self).full_clean(*args, **kw)

    def after_ui_save(self, ar, cw):
        super(Client, self).after_ui_save(ar, cw)
        self.update_reminders(ar)
        #~ return kw

    def update_reminders(self, ar):
        """
        Creates or updates automatic tasks controlled directly by this Person.
        """
        #~ user = self.coach2 or self.coach1
        user = self.get_primary_coach()
        if user:
            with translation.override(user.language):
                M = DurationUnits.months
                update_reminder(
                    1, self, user, self.card_valid_until,
                    _("eID card expires in 2 months"), 2, M)
                update_reminder(
                    2, self, user,
                    self.unavailable_until,
                    _("becomes available again in 1 month"), 1, M)
                update_reminder(
                    3, self, user, self.work_permit_suspended_until,
                    _("work permit suspension ends in 1 month"), 1, M)

    # removed 20190720 as it was dead code
    # @classmethod
    # def get_reminders(model, ui, user, today, back_until):
    #     q = Q(coach1__exact=user) | Q(coach2__exact=user)
    #
    #     def find_them(fieldname, today, delta, msg, **linkkw):
    #         filterkw = {fieldname + '__lte': today + delta}
    #         if back_until is not None:
    #             filterkw.update({
    #                 fieldname + '__gte': back_until
    #             })
    #         for obj in model.objects.filter(q, **filterkw).order_by(fieldname):
    #             linkkw.update(fmt='detail')
    #             ba = obj.get_detail_action()
    #             url = ui.get_detail_url(ba.actor, obj.pk, **linkkw)
    #             html = '<a href="%s">%s</a>&nbsp;: %s' % (
    #                 url, str(obj), cgi.escape(msg))
    #             yield ReminderEntry(getattr(obj, fieldname), html)
    #
    #     for o in find_them(
    #         'card_valid_until', today, datetime.timedelta(days=30),
    #             _("eID card expires"), tab=0):
    #         yield o
    #     for o in find_them(
    #         'unavailable_until', today, datetime.timedelta(days=30),
    #             _("becomes available again"), tab=1):
    #         yield o
    #     for o in find_them(
    #         'work_permit_suspended_until', today, datetime.timedelta(days=30),
    #             _("work permit suspension ends"), tab=1):
    #         yield o
    #     for o in find_them('coached_until', today, datetime.timedelta(days=30),
    #                        _("coaching ends"), tab=1):
    #         yield o

    def get_skills_set(self):
        return self.personproperty_set.filter(
            group=settings.SITE.site_config.propgroup_skills)
    skills_set = property(get_skills_set)

    def properties_list(self, *prop_ids):
        """Yields a list of the :class:`PersonProperty
        <lino_welfare.modlib.cv.models.PersonProperty>` properties of
        this person in the specified order.  If this person has no
        entry for a requested :class:`Property`, it is simply skipped.
        Used in :xfile:`cv.odt`.  `

        """
        return cv.properties_list(self, *prop_ids)

    def get_active_contract(self):
        """
        Return the one and only "active contract" of this client.  A
        contract is active if `applies_from` is <= `today` and
        `(date_ended or applies_until)` >= `today`.

        Returns `None` if there is either no contract or more than one
        active contract.
        """

        today = settings.SITE.today()
        q1 = Q(applies_from__lte=today)
        q2 = Q(applies_until__gte=today)
        q3 = Q(date_ended__isnull=True) | Q(date_ended__gte=today)
        flt = Q(q1, q2, q3)
        qs1 = self.isip_contract_set_by_client.filter(flt)
        qs2 = self.jobs_contract_set_by_client.filter(flt)
        if qs1.count() + qs2.count() == 1:
            if qs1.count() == 1:
                return qs1[0]
            if qs2.count() == 1:
                return qs2[0]
        return None

    @dd.virtualfield(models.DateField(_("Contract starts")))
    def applies_from(obj, ar):
        c = obj.get_active_contract()
        if c is not None:
            return c.applies_from

    @dd.virtualfield(models.DateField(_("Contract ends")))
    def applies_until(obj, ar):
        c = obj.get_active_contract()
        if c is not None:
            return c.applies_until

    @dd.virtualfield(dd.ForeignKey('contacts.Company',
                                   verbose_name=_("Working at ")))
    def contract_company(obj, ar):
        c = obj.get_active_contract()
        if isinstance(c, rt.models.jobs.Contract):
            return c.company

    @dd.displayfield(_("Active contract"))
    def active_contract(obj, ar):
        c = obj.get_active_contract()
        if c is not None:
            txt = str(daterange_text(c.applies_from, c.applies_until))
            if isinstance(c, rt.models.jobs.Contract):
                if c.company is not None:
                    # txt += unicode(pgettext("(place)", " at "))
                    # txt += '\n'
                    # txt += unicode(c.company)
                    txt = (txt, E.br(), c.company.name)
            if ar is None:
                return txt
            return ar.obj2html(c, txt)

    def get_beid_diffs(self, attrs):
        """Overrides
        :meth:`lino_xl.lib.beid.mixins.BeIdCardHolder.get_beid_diffs`.

        """
        Address = rt.models.addresses.Address
        DataSources = rt.models.addresses.DataSources
        diffs = []
        objects = [self]
        kw = dict(partner=self, data_source=DataSources.eid)
        try:
            addr = Address.objects.get(**kw)
        except Address.DoesNotExist:
            if Address.objects.filter(partner=self, primary=True).count() == 0:
                kw.update(primary=True)
            addr = Address(**kw)
        objects.append(addr)
        for fldname, new in attrs.items():
            if fldname in Address.ADDRESS_FIELDS:
                obj = addr
            else:
                obj = self
            fld = get_field(obj, fldname)
            old = getattr(obj, fldname)
            if old != new:
                diffs.append(
                    "%s : %s -> %s" % (
                        str(fld.verbose_name), dd.obj2str(old),
                        dd.obj2str(new)))
                setattr(obj, fld.name, new)
        return objects, diffs

    @dd.htmlbox(_("CBSS"))
    def cbss_relations(self, ar):
        if ar is None:
            return ''
        cbss = dd.resolve_app('cbss')
        SLAVE = cbss.RetrieveTIGroupsRequestsByPerson
        elems = []
        sar = ar.spawn(
            SLAVE, master_instance=self,
            filter=models.Q(status__in=OK_STATES))
        btn = SLAVE.insert_action.request_from(ar).ar2button()
        n = sar.get_total_count()
        if n > 0:
            items = []
            SHOWN_TYPES = ('110', '120', '140', '141')
            obj = sar.data_iterator[n - 1]
            res = obj.Result(ar)
            for row in res:
                if row.type in SHOWN_TYPES:
                    chunks = []
                    if row.counter == 1:
                        chunks += [
                            'IT%s (' % row.type,
                            E.b(row.group),
                            ') ']
                    chunks += [str(row.since), ' ', row.info]
                    items.append(E.li(*chunks))
            if len(items) > 0:
                elems.append(E.ul(*items))

            text = "%s %s" % (obj._meta.verbose_name, naturaltime(obj.sent))
            elems.append(ar.obj2html(obj, text))
        if btn is not None:
            elems += [' ', btn]
        if None in elems:
            raise Exception("20140513 None in %r" % elems)
        return E.div(*elems)

dd.update_field(Client, 'overview', verbose_name=None)


class ClientDetail(dd.DetailLayout):

    main = "general contact coaching aids_tab \
    work_tab career languages \
    competences contracts history calendar ledger misc"

    general = dd.Panel("""
    overview:30 general2:40 general3:20 image:15
    reception.AppointmentsByPartner reception.AgentsByClient
    """, label=_("Person"))

    general2 = """
    gender:10 id:10
    first_name middle_name last_name
    birth_date age:10 national_id:15
    nationality:15 declared_name
    civil_state birth_country birth_place
    """

    general3 = """
    language
    email
    phone
    fax
    gsm
    """

    contact = dd.Panel("""
    dupable_clients.SimilarClients:10 \
    humanlinks.LinksByHuman:30 cbss_relations:30
    households.MembersByPerson:20 households.SiblingsByPerson:50
    """, label=_("Human Links"))

    coaching = dd.Panel("""
    newcomers_left:20 newcomers.AvailableCoachesByClient:40
    clients.ContactsByClient:20 coachings.CoachingsByClient:40
    """, label=_("Coaches"))

    newcomers_left = dd.Panel("""
    workflow_buttons id_document
    broker:12
    faculty:12
    refusal_reason
    """, required_roles=dd.login_required(NewcomersOperator))

    suche = dd.Panel("""
    # job_office_contact job_agents
    pcsw.DispensesByClient:50x3
    pcsw.ExclusionsByClient:50x3
    """)

    papers = dd.Panel("""
    unemployed_since seeking_since work_permit_suspended_until
    needs_residence_permit needs_work_permit
    uploads.UploadsByProject
    """)  # ,label = _("Papers"))

    work_tab = dd.Panel("""
    suche:40  papers:40
    """, label=_("Job search"))

    aids_tab = dd.Panel("""
    in_belgium_since:15 residence_type residence_until
    group:16
    sepa.AccountsByClient
    aids.GrantingsByClient
    """, label=_("Aids"))

    history = dd.Panel("""
    # reception.CreateNoteActionsByClient:20
    notes.NotesByProject
    excerpts.ExcerptsByProject
    # lino.ChangesByMaster
    """, label=_("History"))

    #~ outbox = dd.Panel("""
    #~ outbox.MailsByProject
    # ~ # postings.PostingsByProject
    #~ """,label = _("Correspondence"))

    calendar = dd.Panel("""
    # find_appointment
    # cal.EntriesByProject
    cal.EntriesByClient
    cal.TasksByProject
    """, label=_("Calendar"))

    misc = dd.Panel("""
    activity client_state noble_condition \
    unavailable_until:15 unavailable_why:30
    is_obsolete created modified
    remarks
    checkdata.ProblemsByOwner:25 contacts.RolesByPerson:20
    """, label=_("Miscellaneous"),
        required_roles=dd.login_required(SocialStaff))

    career = dd.Panel("""
    cv.StudiesByPerson
    # cv.TrainingsByPerson
    cv.ExperiencesByPerson:40
    """, label=_("Career"), required_roles=dd.login_required(IntegUser))

    languages = dd.Panel("""
    cv.LanguageKnowledgesByPerson
    xcourses.CourseRequestsByPerson
    """, label=_("Languages"))

    competences = dd.Panel("""
    cv.SkillsByPerson cv.SoftSkillsByPerson skills
    cv.ObstaclesByPerson obstacles badges.AwardsByHolder
    """, label=_("Competences"), required_roles=dd.login_required(IntegUser))

    contracts = dd.Panel("""
    isip.ContractsByClient
    jobs.CandidaturesByPerson
    jobs.ContractsByClient
    """, label=_("Contracts"))

    if dd.is_installed('ledger'):
        ledger = dd.Panel("""
        #vatless.VouchersByProject
        ledger.MovementsByProject
        """, label=dd.plugins.ledger.verbose_name)


class Clients(contacts.Persons):
    # debug_permissions = '20150129'
    # required = dd.login_required(user_groups='coaching')
    required_roles = dd.login_required(SimpleContactsUser)
    # required_roles = dd.login_required((SocialUser, OfficeOperator))
    model = 'pcsw.Client'
    params_panel_hidden = True

    insert_layout = dd.InsertLayout("""
    first_name last_name
    national_id
    gender language
    """, window_size=(60, 'auto'))

    column_names = "name_column:20 client_state national_id:10 \
    gsm:10 address_column age:10 email phone:10 id aid_type language:10"

    detail_layout = 'pcsw.ClientDetail'

    parameters = mixins.ObservedDateRange(
        coached_by=dd.ForeignKey(
            'users.User', blank=True, null=True,
            verbose_name=_("Coached by"), help_text=u"""\
Nur Klienten, die eine Begleitung mit diesem Benutzer haben."""),
        and_coached_by=dd.ForeignKey(
            'users.User', blank=True, null=True,
            verbose_name=_("and by"), help_text=u"""\
Nur Klienten, die auch mit diesem Benutzer eine Begleitung haben."""),
        nationality=dd.ForeignKey(
            'countries.Country', blank=True, null=True,
            verbose_name=_("Nationality")),
        observed_event=ClientEvents.field(
            blank=True, help_text=format_lazy(u"{}{}{}",
                _("Extended filter criteria, e.g.:"),
                "<br/>",
                _("Active: All those who have some active coaching."))),
        only_primary=models.BooleanField(
            _("Only primary clients"), default=False, help_text=u"""\
Nur Klienten, die eine effektive <b>primäre</b> Begleitung haben."""),
#         client_state=ClientStates.field(
#             blank=True, default='',
#             help_text=u"""\
# Nur Klienten mit diesem Status (Aktenzustand)."""),
        #~ new_since = models.DateField(_("Newly coached since"),blank=True),
        **contacts.Persons.parameters)
    params_layout = """
    aged_from aged_to gender nationality also_obsolete
    client_state coached_by and_coached_by start_date end_date \
    observed_event only_primary
    """

    @classmethod
    def param_defaults(self, ar, **kw):
        kw = super(Clients, self).param_defaults(ar, **kw)
        kw.update(client_state='')
        return kw

    @classmethod
    def get_request_queryset(self, ar):
        """This converts the values of the different parameter panel fields to
        the query filter.

        The filter condition extends to the coachings if and only if
        at least on of the following is true:

        - `coached_by` is specified
        - some explicit date range is specified
        - `observed_event` is set to "active" (which means "All those
          who have some active coaching".

        """
        qs = super(Clients, self).get_request_queryset(ar)

        pv = ar.param_values
        period = [pv.start_date, pv.end_date]
        if period[0] is None:
            period[0] = period[1] or dd.today()
        if period[1] is None:
            period[1] = period[0]

        ce = pv.observed_event
        if ce:
            qs = ce.add_filter(qs, pv)

        if pv.coached_by:  # or pv.start_date or pv.end_date:
            qs = add_coachings_filter(
                qs, pv.coached_by, period, pv.only_primary)
            if pv.and_coached_by:
                qs = add_coachings_filter(
                    qs, pv.and_coached_by, period, False)

        # if ce is None:
        #     pass
        # elif ce == ClientEvents.active:
        #     pass
        # elif ce == ClientEvents.isip:
        #     flt = has_contracts_filter('isip_contract_set_by_client', period)
        #     qs = qs.filter(flt).distinct()
        # elif ce == ClientEvents.jobs:
        #     flt = has_contracts_filter('jobs_contract_set_by_client', period)
        #     qs = qs.filter(flt).distinct()
        # elif dd.is_installed('immersion') and ce == ClientEvents.immersion:
        #     flt = has_contracts_filter(
        #         'immersion_contract_set_by_client', period)
        #     qs = qs.filter(flt).distinct()

        # elif ce == ClientEvents.available:
        #     # Build a condition "has some ISIP or some jobs.Contract
        #     # or some immersion.Contract" and then `exclude` it.
        #     flt = has_contracts_filter('isip_contract_set_by_client', period)
        #     flt |= has_contracts_filter('jobs_contract_set_by_client', period)
        #     if dd.is_installed('immersion'):
        #         flt |= has_contracts_filter(
        #             'immersion_contract_set_by_client', period)
        #     qs = qs.exclude(flt).distinct()

        # elif ce == ClientEvents.dispense:
        #     qs = qs.filter(
        #         dispense__end_date__gte=period[0],
        #         dispense__start_date__lte=period[1]).distinct()
        # elif ce == ClientEvents.created:
        #     qs = qs.filter(
        #         created__gte=datetime.datetime.combine(
        #             period[0], datetime.time()),
        #         created__lte=datetime.datetime.combine(
        #             period[1], datetime.time()))
        #     #~ print 20130527, qs.query
        # elif ce == ClientEvents.modified:
        #     qs = qs.filter(
        #         modified__gte=datetime.datetime.combine(
        #             period[0], datetime.time()),
        #         modified__lte=datetime.datetime.combine(
        #             period[1], datetime.time()))
        # elif ce == ClientEvents.penalty:
        #     qs = qs.filter(
        #         exclusion__excluded_until__gte=period[0],
        #         exclusion__excluded_from__lte=period[1]).distinct()
        # elif ce == ClientEvents.note:
        #     qs = qs.filter(
        #         notes_note_set_by_project__date__gte=period[0],
        #         notes_note_set_by_project__date__lte=period[1]).distinct()
        # else:
        #     raise Warning(repr(ce))

        # if pv.client_state:
        #     qs = qs.filter(client_state=pv.client_state)

        if pv.nationality:
            qs = qs.filter(nationality__exact=pv.nationality)

        # print(20150305, qs.query)

        return qs

    @classmethod
    def get_title_tags(self, ar):
        for t in super(Clients, self).get_title_tags(ar):
            yield t
        pv = ar.param_values

        if pv.observed_event:
            yield str(pv.observed_event)

        # if pv.client_state:
        #     yield str(pv.client_state)

        if pv.start_date is None or pv.end_date is None:
            period = None
        else:
            period = daterange_text(
                pv.start_date, pv.end_date)

        if pv.coached_by:
            s = str(self.parameters['coached_by'].verbose_name) + \
                ' ' + str(pv.coached_by)
            if pv.and_coached_by:
                s += " %s %s" % (str(_('and')),
                                 pv.and_coached_by)

            if period:
                yield s \
                    + _(' on %(date)s') % dict(date=period)
            else:
                yield s
        elif period:
            yield _("Coached on %s") % period

        if pv.only_primary:
            #~ yield unicode(_("primary"))
            yield str(self.parameters['only_primary'].verbose_name)

    @classmethod
    def apply_cell_format(self, ar, row, col, recno, td):
        if row.client_state == ClientStates.newcomer:
            td.set(bgcolor="green")
            # td.attrib.update(bgcolor="green")

    @classmethod
    def get_row_classes(cls, obj, ar):
        if obj.client_state == ClientStates.newcomer:
            yield 'green'
        elif obj.client_state in (ClientStates.refused, ClientStates.former):
            yield 'yellow'
        #~ if not obj.has_valid_card_data():
            #~ return 'red'

class CoachedClients(Clients):
    required_roles = dd.login_required(SocialUser)

    @classmethod
    def param_defaults(self, ar, **kw):
        kw = super(CoachedClients, self).param_defaults(ar, **kw)
        kw.update(client_state=ClientStates.coached)
        return kw


class ClientsByNationality(Clients):
    #~ app_label = 'contacts'
    master_key = 'nationality'
    order_by = "city name".split()
    column_names = "city street street_no street_box addr2 name country language *"


class AllClients(Clients):
    column_names = "name_column:20 client_state national_id:10 \
    gsm:10 address_column age:10 email phone:10 id *"
    required_roles = dd.login_required(SocialStaff)


class IdentityChecker(ClientChecker):
    """Clients must have either valid eId data or an alternative
    identifying document.

    """
    verbose_name = _("Check for valid identification")
    need_valid_card_data = (ClientStates.coached, ClientStates.newcomer)

    def get_checkdata_problems(self, obj, fix=False):

        if obj.client_state in self.need_valid_card_data \
           and not obj.has_valid_card_data():
            qs = Shortcuts.id_document.get_uploads(project=obj)
            if qs.count() == 0:
                msg = _(
                    "Neither valid eId data "
                    "nor alternative identifying document.")
                yield (False, msg)

# IdentityChecker.activate()
# 20200723 "Meldung ist an dieser Stelle relativ unnütz und kommt wieder komplett raus"



#
# PERSON GROUP
#

class PersonGroup(dd.Model):
    name = models.CharField(_("Designation"), max_length=200)
    ref_name = models.CharField(_("Reference name"), max_length=20, blank=True)
    active = models.BooleanField(_("Considered active"), default=True)
    #~ text = models.TextField(_("Description"),blank=True,null=True)

    class Meta:
        app_label = 'pcsw'
        verbose_name = _("Integration Phase")
        verbose_name_plural = _("Integration Phases")

    def __str__(self):
        return self.name


class PersonGroups(dd.Table):
    help_text = _("Liste des phases d'intégration possibles.")
    model = 'pcsw.PersonGroup'
    required_roles = dd.login_required(SocialStaff)

    order_by = ["ref_name"]


#
# ACTIVITIY (Berufscode)
#

class Activity(dd.Model):

    class Meta:
        app_label = 'pcsw'
        verbose_name = _("activity")
        verbose_name_plural = _("activities")
    name = models.CharField(max_length=80)
    lst104 = models.BooleanField(_("Appears in Listing 104"), default=False)

    def __str__(self):
        return str(self.name)


class Activities(dd.Table):
    help_text = _("""Liste des "activités" ou "codes profession".""")
    model = 'pcsw.Activity'
    required_roles = dd.login_required(SocialStaff)

#~ class ActivitiesByPerson(Activities):
    #~ master_key = 'activity'

#~ class ActivitiesByCompany(Activities):
    #~ master_key = 'activity'


class DispenseReason(mixins.BabelNamed, mixins.Sequenced):

    class Meta:
        app_label = 'pcsw'
        verbose_name = _("Dispense reason")
        verbose_name_plural = _('Dispense reasons')

    #~ name = models.CharField(_("designation"),max_length=200)
    #~
    #~ def __unicode__(self):
        #~ return unicode(self.name)


class DispenseReasons(dd.Table):
    help_text = _("A list of reasons for being dispensed")
    required_roles = dd.login_required(SocialStaff)
    model = 'pcsw.DispenseReason'
    column_names = 'seqno name *'
    order_by = ['seqno']


class Dispense(dd.Model):

    class Meta:
        app_label = 'pcsw'
        verbose_name = _("Dispense")
        verbose_name_plural = _("Dispenses")
    allow_cascaded_delete = ['client']
    client = dd.ForeignKey('pcsw.Client')
    reason = dd.ForeignKey('pcsw.DispenseReason', verbose_name=_("Reason"))
    remarks = models.TextField(_("Remark"), blank=True)
    start_date = models.DateField(
        blank=True, null=True,
        verbose_name=_("Dispensed from"))
    end_date = models.DateField(
        blank=True, null=True,
        verbose_name=_("until"))


class Dispenses(dd.Table):
    order_by = ['start_date']
    help_text = _("Liste de dispenses")
    required_roles = dd.login_required(SocialStaff)
    model = 'pcsw.Dispense'


class DispensesByClient(Dispenses):
    master_key = 'client'
    column_names = 'start_date end_date reason remarks:10'
    hidden_columns = 'id'
    auto_fit_column_widths = True
    required_roles = dd.login_required(SocialUser)



class ExclusionType(dd.Model):

    class Meta:
        app_label = 'pcsw'
        verbose_name = _("Unemployment exclusion type")
        verbose_name_plural = _('Unemployment exclusion types')

    name = models.CharField(max_length=200)

    def __str__(self):
        return str(self.name)


class ExclusionTypes(dd.Table):
    help_text = _("""Liste des raisons possibles d'arrêter temporairement
    le paiement d'une aide financière prévue.""")
    required_roles = dd.login_required(SocialStaff)
    model = 'pcsw.ExclusionType'



class Exclusion(dd.Model):

    class Meta:
        app_label = 'pcsw'
        verbose_name = _("Exclusion from unemployment")
        verbose_name_plural = _('Exclusions from unemployment')

    person = dd.ForeignKey('pcsw.Client')
    type = dd.ForeignKey("pcsw.ExclusionType",
                         verbose_name=_("Reason"),
                         blank=True, null=True)
    excluded_from = models.DateField(blank=True, null=True,
                                     verbose_name=_("Excluded from"))
    excluded_until = models.DateField(blank=True, null=True,
                                      verbose_name=_("until"))
    remark = models.CharField(_("Remark"), max_length=200, blank=True)

    def __str__(self):
        s = str(self.type)
        if self.excluded_from:
            s += ' ' + str(self.excluded_from)
        if self.excluded_until:
            s += '-' + str(self.excluded_until)
        return s


class Exclusions(dd.Table):
    required_roles = dd.login_required(SocialStaff)
    help_text = _("Liste des exclusions.")

    model = 'pcsw.Exclusion'


class ExclusionsByClient(Exclusions):
    label = _("Unemployment situation")  # Situation chomage
    required_roles = dd.login_required(SocialUser)
    master_key = 'person'
    column_names = 'excluded_from excluded_until type remark:10'
    auto_fit_column_widths = True



class Conviction(dd.Model):

    class Meta:
        app_label = 'pcsw'
        verbose_name = _("Conviction")
        verbose_name_plural = _('Convictions')

    client = dd.ForeignKey('pcsw.Client')
    date = models.DateField(_("Date"), blank=True)
    prejudicial = models.BooleanField(_("Prejudicial"), default=False)
    designation = models.CharField(
        _("Designation"), max_length=200, blank=True)

    def full_clean(self, *args, **kw):
        if self.date is None:
            self.date = dd.today()
        super(Conviction, self).full_clean(*args, **kw)

    def __str__(self):
        s = str(self.designation)
        if self.date:
            s += ' (%s)' % dd.fds(self.date)
        return s


class Convictions(dd.Table):
    required_roles = dd.login_required(SocialStaff)
    model = 'pcsw.Conviction'


class ConvictionsByClient(Convictions):
    required_roles = dd.login_required(SocialUser)
    master_key = 'client'
    column_names = 'date designation prejudicial'
    auto_fit_column_widths = True


#
# AID TYPES
#
class AidType(mixins.BabelNamed):

    class Meta:
        app_label = 'pcsw'
        verbose_name = _("aid type")
        verbose_name_plural = _('aid types')


class AidTypes(dd.Table):
    help_text = _("Liste des types d'aide financière.")
    model = 'pcsw.AidType'
    column_names = 'name *'
    required_roles = dd.login_required(SocialStaff)


@dd.receiver(dd.pre_analyze)
def setup_client_workflow(sender=None, **kw):
    """Set up workflow for :class:`ClientStates
    <lino_welfare.modlib.pcsw.choicelists.ClientStates>`.

    """
    # ClientStates.refused.add_transition(RefuseClient)
    # ClientStates.former.add_transition(MarkClientFormer)
    ClientStates.newcomer.add_transition(
        required_states='former',
        required_roles=dd.login_required(NewcomersUser))
