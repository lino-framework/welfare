# -*- coding: UTF-8 -*-
# Copyright 2008-2017 Luc Saffre
# License: BSD (see file COPYING for details)

"""The :xfile:`models` module for this plugin.

"""

from __future__ import unicode_literals

from builtins import str
import logging
logger = logging.getLogger(__name__)

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import pgettext_lazy as pgettext

from lino.api import dd
from lino.mixins.printable import DirectPrintAction
from lino.modlib.uploads.mixins import UploadController

from .roles import CoursesUser, CoursesStaff
from lino_welfare.modlib.pcsw.roles import SocialUser


pcsw = dd.resolve_app('pcsw')
contacts = dd.resolve_app('contacts')
CLIENTS_TABLE = pcsw.CoachedClients


class CourseProvider(contacts.Company):

    """
    A CourseProvider is a Company that offers Courses.
    """
    class Meta:
        verbose_name = _("Course provider")
        verbose_name_plural = _("Course providers")

    def disable_delete(self, ar=None):
        # skip the is_imported_partner test
        return super(contacts.Partner, self).disable_delete(ar)


class CourseProviderDetail(contacts.CompanyDetail):
    """Same as CompanyDetail, except that we add a tab
    :guilabel:`Courses`.

    """
    box5 = "remarks"
    main = "general notes CourseOffersByProvider"


class CourseProviders(contacts.Companies):
    """Table of all course providers

    """
    required_roles = dd.login_required(CoursesUser)
    model = 'xcourses.CourseProvider'
    detail_layout = CourseProviderDetail()



class CourseContent(dd.Model):

    u"""
    Ein Kursinhalt (z.B. "Französisch", "Deutsch", "Alphabétisation",...)
    """

    class Meta:
        verbose_name = _("Course Content")
        verbose_name_plural = _('Course Contents')

    name = models.CharField(max_length=200,
                            blank=True,  # null=True,
                            verbose_name=_("Name"))
    u"""
    Bezeichnung des Kursinhalts (nach Konvention des DSBE).
    """

    def __str__(self):
        return str(self.name)


class CourseContents(dd.Table):
    required_roles = dd.login_required(CoursesStaff)
    model = 'xcourses.CourseContent'
    order_by = ['name']
    detail_layout = """
    id name
    xcourses.CourseOffersByContent
    xcourses.CourseRequestsByContent
    """



class CourseOffer(dd.Model):

    """
    """
    class Meta:
        verbose_name = _("Course Offer")
        verbose_name_plural = _('Course Offers')

    title = models.CharField(max_length=200,
                             verbose_name=_("Name"))
    u"""
    Der Titel des Kurses. Maximal 200 Zeichen.
    """

    guest_role = dd.ForeignKey(
        "cal.GuestRole", blank=True, null=True,
        help_text=_("Default guest role for particpants of events."))

    content = dd.ForeignKey("xcourses.CourseContent")
    """
    Der Inhalt des Kurses (ein :class:`CourseContent`)
    """

    provider = dd.ForeignKey('xcourses.CourseProvider')
    #~ provider = dd.ForeignKey(CourseProvider,
        #~ verbose_name=_("Course provider"))
    #~ """
    #~ Der Kursanbieter (eine :class:`Company`)
    #~ """

    description = dd.RichTextField(_("Description"), blank=True, format='html')

    def __str__(self):
        return u'%s (%s)' % (self.title, self.provider)


class CourseOffers(dd.Table):
    required_roles = dd.login_required(CoursesUser)
    model = 'xcourses.CourseOffer'

    insert_layout = """
    provider
    content
    title
    """
    detail_layout = """
    id:8 title content provider guest_role
    description
    CoursesByOffer
    """


class CourseOffersByProvider(CourseOffers):
    master_key = 'provider'


class CourseOffersByContent(CourseOffers):
    master_key = 'content'



class Course(dd.Model):

    u"""
    Ein konkreter Kurs, der an einem bestimmten Datum beginnt.
    Für jeden Kurs muss ein entsprechendes Angebot existieren,
    das u.A. den :class:`Kursinhalt <CourseContent>`
    und :class:`Kursanbieter <CourseProvider>`
    detailliert. Also selbst für einen einmalig stattfindenden
    Kurs muss ein Angebot erstellt werden.
    """
    class Meta:
        verbose_name = _("Course")
        verbose_name_plural = _('Courses')

    offer = dd.ForeignKey("xcourses.CourseOffer")

    title = models.CharField(
        max_length=200,
        blank=True,
        verbose_name=_("Name"))

    start_date = models.DateField(_("start date"))

    remark = models.CharField(
        max_length=200,
        blank=True,  # null=True,
        verbose_name=_("Remark"))
    u"""
    Bemerkung über diesen konkreten Kurs. Maximal 200 Zeichen.
    """

    def __str__(self):
        s = dd.dtos(self.start_date)
        if self.title:
            s += " " + self.title
        if self.offer:
            s += " " + str(self.offer)
        return s

    print_candidates = DirectPrintAction(
        label=_("List of candidates"),
        tplname='candidates')
    print_participants = DirectPrintAction(
        label=_("List of participants"),
        tplname='participants')

    def participants(self):
        u"""
        Liste von :class:`CourseRequest`-Instanzen,
        die in diesem Kurs eingetragen sind.
        """
        return ParticipantsByCourse.request(self).data_iterator

    def candidates(self):
        u"""
        Liste von :class:`CourseRequest`-Instanzen,
        die noch in keinem Kurs eingetragen sind, aber für diesen Kurs in Frage
        kommen.
        """
        return CandidatesByCourse.request(self).data_iterator


class Courses(dd.Table):
    # ~ debug_permissions = 20130429 # Melanie doesn't see :menulabel:`Explorer --> Courses`
    required_roles = dd.login_required(CoursesStaff)
    model = 'xcourses.Course'
    order_by = ['start_date']

    insert_layout = """
    start_date offer
    title
    """

    detail_layout = """
    id:8 start_date offer title
    remark
    xcourses.ParticipantsByCourse
    xcourses.CandidatesByCourse
    """



class CoursesByOffer(Courses):
    required_roles = dd.login_required(CoursesUser)
    master_key = 'offer'
    column_names = 'start_date * id'


class CourseRequestStates(dd.Workflow):
    help_text = _("List of possible states of a Course Request")

    #~ @classmethod
    #~ def migrate(cls,old):
        #~ """
        #~ Used by :meth:`lino_welfare.modlib.pcsw.migrate.migrate_from_1_4_4`.
        #~ """
        #~ cv = {
          #~ None: 'candidate',
          #~ 1:'award',
          #~ 2:'passed',
          #~ 3:'failed',
          #~ 4:'aborted'
          #~ }
        #~ return getattr(cls,cv[old])
        #~

    #~ @classmethod
    #~ def allow_state_candidate(cls,self,user):
        #~ if self.course:
            #~ return True
        #~ return False

add = CourseRequestStates.add_item
add('10', pgettext("courses", "Open"), "candidate")
#~ add('10', _("Candidate"),"candidate")
#~ add('10', _("Active"),"candidate")
add('20', pgettext("courses", "Registered"), "registered")
add('30', pgettext("courses", "Passed"), "passed")   # bestanden
add('40', _("Award"), "award")   # gut bestanden
add('50', pgettext("courses", "Failed"), "failed")   # nicht bestanden
add('60', pgettext("courses", "Aborted"), "aborted")   # abgebrochen
add('70', _("Inactive"), "inactive")


class RegisterCandidate(dd.ChangeStateAction):
    label = pgettext("courses", "Register")
    required_states = 'candidate'
    help_text = _("Register this candidate for this course.")

    def run_from_ui(self, ar, **kw):
        obj = ar.selected_rows[0]
        assert isinstance(obj, CourseRequest)
        if ar.actor.master is Course and ar.master_instance is not None:
            obj.course = ar.master_instance
        if not obj.course:
            return ar.error(_("Cannot register to unknown course."), alert=True)
        kw = super(RegisterCandidate, self).run_from_ui(ar, **kw)
        kw.update(refresh_all=True)
        kw.update(message=_("%(person)s has been registered to %(course)s") % dict(
            person=obj.person, course=obj.course))
        ar.success(**kw)


class UnRegisterCandidate(dd.ChangeStateAction):
    label = pgettext("courses", "Unregister")
    required_states = 'registered inactive'
    help_text = _("Unregister this candidate from this course.")

    def run_from_ui(self, ar, **kw):
        obj = ar.selected_rows[0]
        assert isinstance(obj, CourseRequest)
        course = obj.course
        obj.course = None
        kw = super(UnRegisterCandidate, self).run_from_ui(ar, **kw)
        kw.update(refresh_all=True)
        kw.update(message=_("%(person)s has been unregistered from %(course)s")
                  % dict(person=obj.person, course=course))
        #~ return kw
        ar.success(**kw)

class CourseRequest(UploadController):

    """A Course Request is created when a certain Person expresses her
    wish to participate in a Course with a certain CourseContent.

    """
    workflow_state_field = 'state'

    class Meta:
        verbose_name = _("Course Requests")
        verbose_name_plural = _('Course Requests')

    person = dd.ForeignKey("pcsw.Client",
                               help_text="Le client qui désire suivre un cours.")

    offer = dd.ForeignKey("xcourses.CourseOffer", blank=True, null=True)

    content = dd.ForeignKey("xcourses.CourseContent",
                                verbose_name=_("Course content"),
                                help_text=u"Der gewünschte Kursinhalt.)")

    #~ date_submitted = models.DateField(_("date submitted"),auto_now_add=True)
    date_submitted = models.DateField(_("date submitted"),
                                      help_text=_("When this request has been submitted."))
        #~ help_text=u"Das Datum, an dem die Anfrage erstellt wurde.")

    urgent = models.BooleanField(_("Needed for job search"),
                                 default=False,
                                 help_text=_("Check this if the request is needed for job search."))
        #~ help_text=u"Ankreuzen, wenn der Kurs für die Arbeitssuche benötigt wird.")


    state = CourseRequestStates.field(
        default=CourseRequestStates.as_callable('candidate'))

    course = dd.ForeignKey(
        "xcourses.Course", blank=True, null=True,
        help_text=_("The course which satisfies this request. "
                    "Leave blank on open requests."),
        verbose_name=_("Course found"))

    remark = models.TextField(
        blank=True, null=True,
        verbose_name=_("Remark"))
    u"""
    Bemerkung zu dieser konkreten Kursanfrage oder -teilnahme.
    """

    date_ended = models.DateField(
        blank=True, null=True, verbose_name=_("date ended"))
    u"""
    Datum der effektives Beendigung dieser Kursteilname.
    """

    def on_create(self, ar):
        self.date_submitted = settings.SITE.today()
        super(CourseRequest, self).on_create(ar)

    def save(self, *args, **kw):
        if self.offer and self.offer.content:
            self.content = self.offer.content
        super(CourseRequest, self).save(*args, **kw)

    @dd.chooser()
    def offer_choices(cls, content):
        if content:
            return CourseOffer.objects.filter(content=content)
        return CourseOffer.objects.all()

    def before_state_change(self, ar, old, new):
        if new.name in ('passed', 'award', 'failed', 'aborted'):
            if not self.date_ended:
                self.date_ended = settings.SITE.today()
        super(CourseRequest, self).before_state_change(ar, old, new)

    def get_row_permission(self, ar, state, ba):
        if not super(CourseRequest, self).get_row_permission(ar, state, ba):
            #~ if ba.action.action_name == 'wf7':
                #~ logger.info('20130424 courses.CourseRequest.get_row_permission() %r super said no',ba)
            return False
        if isinstance(ba.action, RegisterCandidate):
            if ar.actor.master is not Course or ar.master_instance is None:
                return False
        return True

    @classmethod
    def setup_parameters(cls, fields):
        fields.update(
            request_state=CourseRequestStates.field(blank=True),
            course_content=dd.ForeignKey(
                "xcourses.CourseContent", blank=True),
            course_offer=dd.ForeignKey("xcourses.CourseOffer", blank=True),
            course_provider=dd.ForeignKey(
                'xcourses.CourseProvider', blank=True))
        fields.update(CLIENTS_TABLE.parameters)
        super(CourseRequest, cls).setup_parameters(fields)

    @classmethod
    def get_request_queryset(self, ar):
        #~ raise Exception(20130424)
        qs = super(CourseRequest, self).get_request_queryset(ar)
        clients_qs = CLIENTS_TABLE.get_request_queryset(ar)
        #~ print 20130424, clients_qs
        qs = qs.filter(person__in=clients_qs)
        if ar.param_values.request_state:
            qs = qs.filter(state=ar.param_values.request_state)
        if ar.param_values.course_content:
            qs = qs.filter(content=ar.param_values.course_content)
        if ar.param_values.course_provider:
            qs = qs.filter(offer__provider=ar.param_values.course_provider)
        if ar.param_values.course_offer:
            qs = qs.filter(offer=ar.param_values.course_offer)
        return qs

    @classmethod
    def get_title_tags(self, ar):
        if ar.param_values.request_state:
            yield str(ar.param_values.request_state)
        if ar.param_values.course_content:
            yield str(ar.param_values.course_content)
        if ar.param_values.course_provider:
            yield str(ar.param_values.course_provider)
        if ar.param_values.course_offer:
            yield str(ar.param_values.course_offer)
        for t in super(CourseRequest, self).get_title_tags(ar):
            yield t
        for t in CLIENTS_TABLE.get_title_tags(ar):
            yield t


class CourseRequests(dd.Table):
    #~ debug_permissions = 20130424
    model = 'xcourses.CourseRequest'
    required_roles = dd.login_required(CoursesStaff)
    detail_layout = """
    date_submitted person content offer urgent
    course state date_ended id:8
    remark  uploads.UploadsByController
    """
    order_by = ['date_submitted']
    active_fields = 'offer'

    @classmethod
    def param_defaults(self, ar, **kw):
        kw = super(CourseRequests, self).param_defaults(ar, **kw)
        kw.update(client_state='')
        return kw


class CourseRequestsByPerson(CourseRequests):
    """
    Shows the course requests of a client.
    """
    required_roles = dd.login_required((CoursesUser, SocialUser))
    master_key = 'person'
    column_names = 'date_submitted:10 content:15 offer:15 course:20 urgent state date_ended remark:15 id'
    hidden_columns = 'id'
    auto_fit_column_widths = True


class CourseRequestsByContent(CourseRequests):
    required_roles = dd.login_required(CoursesUser)
    master_key = 'content'


class RequestsByCourse(CourseRequests):

    """
    Table of :class:`CourseRequest` instances of a :class:`Course`.
    """
    required_roles = dd.login_required(CoursesUser)
    master_key = 'course'

    @classmethod
    def create_instance(self, req, **kw):
        obj = super(RequestsByCourse, self).create_instance(req, **kw)
        if obj.course is not None:
            obj.content = obj.course.offer.content
        return obj


class ParticipantsByCourse(RequestsByCourse):

    """
    List of participating candidates for the given :class:`Course`.
    """
    label = _("Participants")
    column_names = 'person remark:20 date_ended workflow_buttons:60'
    auto_fit_column_widths = True


class CandidatesByCourse(RequestsByCourse):

    """
    List of :class:`Candidates <Candidate>` for the given :class:`Course`
    which are not registiered.
    """
    label = _("Candidates")
    column_names = 'person remark:20 date_submitted workflow_buttons:60 content'
    auto_fit_column_widths = True

    @classmethod
    def get_request_queryset(self, rr):
        if rr.master_instance is None:
            return []
        return self.model.objects.filter(course__isnull=True,
                                         state=CourseRequestStates.candidate,
                                         content=rr.master_instance.offer.content)

    @classmethod
    def create_instance(self, req, **kw):
        """Manually clear the `course` field.
        """
        obj = super(CandidatesByCourse, self).create_instance(req, **kw)
        obj.course = None
        return obj



class PendingCourseRequests(CourseRequests):

    """
    List of pending course requests.
    """
    required_roles = dd.login_required(CoursesUser)
    label = _("Pending Course Requests")
    order_by = ['date_submitted']
    filter = models.Q(course__isnull=True)
    # parameters = dict(
    #     request_state=CourseRequestStates.field(blank=True),
    #     course_content=dd.ForeignKey(
    #         "courses.CourseContent", blank=True),
    #     course_offer=dd.ForeignKey("courses.CourseOffer", blank=True),
    #     course_provider=dd.ForeignKey(
    #         'courses.CourseProvider', blank=True),
    #     **CLIENTS_TABLE.parameters)
    params_layout = CLIENTS_TABLE.params_layout + """\
    request_state course_content course_provider course_offer
    """

    @classmethod
    def setup_columns(self):
        """
        Builds columns dynamically for the different age slices.
        Called when kernel setup is done,
        before the UI handle is being instantiated.
        """
        self.column_names = 'date_submitted workflow_buttons:30 person age '
        self.column_names += 'address person__gsm person__phone person__coaches '
        #~ self.column_names += 'address person__gsm person__phone person__coach1 person__coach2 '
        #~ self.column_names += 'person__address_column person__age '
        self.column_names += 'content urgent remark'
        age_slices = [(16, 24), (25, 30), (31, 40),
                      (41, 50), (51, 60), (61, None)]
        for sl in age_slices:
            if sl[1] is None:
                label = ">%d" % sl[0]
            else:
                label = "%d-%d" % sl

            def w(sl):
                def func(self, obj, ar):
                    if obj._age_in_years is None:
                        return None
                    if obj._age_in_years < sl[0]:
                        return None
                    if obj._age_in_years > sl[1]:
                        return None
                    return 1
                return func
            vf = dd.VirtualField(models.IntegerField(label), w(sl))
            self.add_virtual_field('a' + str(sl[0]), vf)
            self.column_names += ' ' + vf.name + ':5'

        self.column_names += ' ax'

    @classmethod
    def get_data_rows(self, ar):
        #~ qs = super(PendingCourseRequests,self).get_request_queryset(ar)
        qs = self.get_request_queryset(ar)
        for obj in qs:
            age = obj.person.get_age()
            # if age is not None:
            #     age = age.days / 365
            obj._age_in_years = age
            yield obj

    editable = True

    @dd.virtualfield(models.IntegerField(_("Age")))
    def age(self, obj, request):
        return obj._age_in_years

    @dd.displayfield(_("Address"))
    def address(self, obj, ar):
        return obj.person.address_location(', ')

    #~ @dd.displayfield(_("Age"))
    #~ def age(self,obj,request):
        #~ if obj._age_in_years is None: return ''
        #~ return str(obj._age_in_years)

    #~ @dd.virtualfield(models.BooleanField(_("unknown age")))
    @dd.virtualfield(models.IntegerField(_("unknown age")))
    def ax(self, obj, request):
        if obj._age_in_years is None:
            return 1
        return 0
        #~ return obj._age_in_years is None



@dd.receiver(dd.pre_analyze)
def setup_courses_workflow(sender=None, **kw):

    CourseRequestStates.registered.add_transition(RegisterCandidate)
    CourseRequestStates.candidate.add_transition(UnRegisterCandidate)
    CourseRequestStates.passed.add_transition(required_states="registered")
    CourseRequestStates.failed.add_transition(required_states="registered")
    CourseRequestStates.aborted.add_transition(required_states="registered")

    CourseRequestStates.inactive.add_transition(required_states="candidate")
    # CourseRequestStates.candidate.add_transition(required_states="inactive")
        #~ debug_permissions = 20130424)
