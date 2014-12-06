# -*- coding: UTF-8 -*-
# Copyright 2008-2014 Luc Saffre
# License: BSD (see file COPYING for details)

"""Contains PCSW-specific models and tables that have not yet been
moved into a separate module because they are really very PCSW
specific.

"""

from __future__ import unicode_literals
from __future__ import print_function

import logging
logger = logging.getLogger(__name__)

import os
import cgi
import datetime

from django.db import models
from django.db.models import Q
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.utils import translation
from django.utils.encoding import force_unicode
from django.contrib.humanize.templatetags.humanize import naturaltime


from lino import dd, rt
from lino.core import dbutils
from lino.core.dbutils import get_field

from lino.utils.xmlgen.html import E

households = dd.resolve_app('households')
# reception = dd.resolve_app('reception')
cal = dd.resolve_app('cal')
extensible = dd.resolve_app('extensible')
properties = dd.resolve_app('properties')
contacts = dd.resolve_app('contacts')
dedupe = dd.resolve_app('dedupe')
cv = dd.resolve_app('cv')
uploads = dd.resolve_app('uploads')
users = dd.resolve_app('users')
isip = dd.resolve_app('isip')
jobs = dd.resolve_app('jobs')
notes = dd.resolve_app('notes')
beid = dd.resolve_app('beid')

from lino.utils import ssin

from .coaching import *


class CivilState(dd.ChoiceList):

    """
    Civil states, using Belgian codes.
    
    """
    required = dd.required(user_level='admin')
    verbose_name = _("Civil state")
    verbose_name_plural = _("Civil states")

    @classmethod
    def old2new(cls, old):  # was used for migrating to 1.4...
        if old == '1':
            return cls.single
        if old == '2':
            return cls.married
        if old == '3':
            return cls.divorced
        if old == '4':
            return cls.widowed
        if old == '5':
            return cls.separated
        return ''

add = CivilState.add_item
add('10', _("Single"), 'single')
add('13', _("Single cohabitating"))
add('18', _("Single with child"))
add('20', _("Married"), 'married')
add('21', _("Married (living alone)"))
add('22', _("Married (living with another partner)"))
add('30', _("Widowed"), 'widowed')
add('33', _("Widow cohabitating"))
add('40', _("Divorced"), 'divorced')
add('50', _("Separated"), 'separated')  # Getrennt von Tisch und Bett /


#~ '10', 'Célibataire', 'Ongehuwd', 'ledig'
#~ '13', 'Célibataire cohab.', NULL, 'ledig mit zus.',
#~ '18', 'Célibataire avec enf', NULL, 'ledig mit kind',
#~ '20', 'Marié', 'Gehuwd', 'verheiratet',
#~ '21', 'Séparé de fait', NULL, 'verheiratet alleine',
#~ '22', 'Séparé de fait cohab', NULL, 'verheiratet zus.',
#~ '30', 'Veuf(ve)', NULL, 'Witwe(r)',
#~ '33', 'Veuf(ve) cohab.', NULL, 'Witwe(r) zus.',
#~ '40', 'Divorcé', NULL, 'geschieden',
#~ '50', 'séparé(e) de corps', NULL, 'von Tisch & Bet get.',


# http://en.wikipedia.org/wiki/European_driving_licence
class ResidenceType(dd.ChoiceList):

    """
    Types of registries for the Belgian residence.
    
    """
    verbose_name = _("Residence type")

add = ResidenceType.add_item
# Bevölkerungsregister registre de la population
add('1', _("Registry of citizens"))
# Fremdenregister        Registre des étrangers      vreemdelingenregister
add('2', _("Registry of foreigners"))
add('3', _("Waiting for registry"))    # Warteregister


class ClientEvents(dd.ChoiceList):
    verbose_name = _("Observed event")
    verbose_name_plural = _("Observed events")
add = ClientEvents.add_item
#~ add('10', _("Coached"),'coached')
add('10', _("Active"), 'active')
add('20', _("ISIP"), 'isip')
add('21', _("Art.60§7 contract"), 'jobs')
add('22', _("Dispense"), 'dispense')
add('30', _("Penalty"), 'penalty')
add('31', _("Exclusion"), 'exclusion')
add('40', _("Note"), 'note')
add('50', _("Created"), 'created')
add('60', _("Modified"), 'modified')
#~ add('20', _("Started"),'started')
#~ add('30', _("Ended"),'ended')


class ClientStates(dd.Workflow):
    required = dd.required(user_level='admin')
    verbose_name_plural = _("Client states")

add = ClientStates.add_item
add('10', _("Newcomer"), 'newcomer', help_text=u"""\
Klient hat Antrag auf Hilfe eingereicht,
der jedoch noch nicht genehmigt wurde
oder es wurde noch kein Sachbearbeiter oder Sozi zur Begleitung zugewiesen.
(TIM: Attribut "N" (Neuantrag) gesetzt)""")  # "N" in PAR->Attrib
    #~ required=dict(states=['refused','coached'],user_groups='newcomers'))
add('20', _("Refused"), 'refused', help_text=u"""\
Alle bisherigen Hilfsanträge wurden abgelehnt.
(TIM kennt diesen Aktenzustand nicht)""")
# coached: neither newcomer nor former, IdPrt != "I"
add('30', _("Coached"), 'coached', help_text=u"""\
Es gibt mindestens eine Person im ÖSHZ, die sich um die Person kümmert.
(TIM: IdPrt == "S" und Attribut N (Neuantrag) nicht gesetzt)""")

add('50', _("Former"), 'former', help_text=u"""\
War mal begleitet, ist es aber jetzt nicht mehr.
Es existiert keine *aktive* Begleitung.
(TIM: Attribut `W (Warnung bei Auswahl)` oder Partnerart `I (Inaktive)`)""")

#~ add('60', _("Invalid"),'invalid',help_text=u"""\
#~ Klient ist laut TIM weder Ehemalig noch Neuantrag, hat aber keine gültige NISS.""")


class RefusalReasons(dd.ChoiceList):
    pass

add = RefusalReasons.add_item
add('10', _("Information request (No coaching needed)"))
add('20', _("PCSW is not competent"))
add('30', _("Client did not return"))


class RefuseClient(dd.ChangeStateAction):

    """
    This is not a docstring
    """
    label = _("Refuse")
    required = dict(states='newcomer', user_groups='newcomers')

    #~ icon_file = 'flag_blue.png'
    help_text = _("Refuse this newcomer request.")

    parameters = dict(
        reason=RefusalReasons.field(),
        remark=dd.RichTextField(_("Remark"), blank=True),
    )

    params_layout = dd.Panel("""
    reason
    remark
    """, window_size=(50, 15))

    def run_from_ui(self, ar, **kw):
        obj = ar.selected_rows[0]
        assert isinstance(obj, Client)
        obj.refusal_reason = ar.action_param_values.reason
        subject = _("%(client)s has been refused.") % dict(client=obj)
        body = unicode(ar.action_param_values.reason)
        if ar.action_param_values.remark:
            body += '\n' + ar.action_param_values.remark
        kw.update(message=subject)
        kw.update(alert=_("Success"))
        super(RefuseClient, self).run_from_ui(ar)
        #~ self.add_system_note(ar,obj)
        silent = False
        ar.add_system_note(
            obj,
            subject,
            body,
            silent)
        ar.success(**kw)


class Client(contacts.Person,
             # dd.BasePrintable,
             beid.BeIdCardHolder):

    """A :class:`Client` is a specialized :class:`Person`.

    """
    class Meta:
        verbose_name = _("Client")
        verbose_name_plural = _("Clients")
        abstract = dd.is_abstract_model(__name__, 'Client')
        #~ ordering = ['last_name','first_name']

    workflow_state_field = 'client_state'

    group = models.ForeignKey("pcsw.PersonGroup", blank=True, null=True,
                              verbose_name=_("Integration phase"))

    birth_place = models.CharField(_("Birth place"),
                                   max_length=200,
                                   blank=True,
                                   #~ null=True
                                   )
    birth_country = dd.ForeignKey(
        "countries.Country",
        blank=True, null=True,
        verbose_name=_("Birth country"), related_name='by_birth_place')

    civil_state = CivilState.field(blank=True)

    residence_type = ResidenceType.field(blank=True)

    in_belgium_since = models.DateField(
        _("Lives in Belgium since"), blank=True, null=True)
    residence_until = models.DateField(
        _("Residence until"), blank=True, null=True)
    unemployed_since = models.DateField(
        _("Seeking work since"), blank=True, null=True)
    needs_residence_permit = models.BooleanField(
        _("Needs residence permit"), default=False)
    needs_work_permit = models.BooleanField(
        _("Needs work permit"), default=False)
    work_permit_suspended_until = models.DateField(
        blank=True, null=True, verbose_name=_("suspended until"))
    aid_type = models.ForeignKey("pcsw.AidType", blank=True, null=True)
        #~ verbose_name=_("aid type"))

    declared_name = models.BooleanField(_("Declared name"), default=False)

    is_seeking = models.BooleanField(_("is seeking work"), default=False)
    unavailable_until = models.DateField(
        blank=True, null=True, verbose_name=_("Unavailable until"))
    unavailable_why = models.CharField(max_length=100,
                                       blank=True,  # null=True,
                                       verbose_name=_("reason"))

    obstacles = models.TextField(_("Other obstacles"), blank=True, null=True)
    skills = models.TextField(_("Other skills"), blank=True, null=True)

    job_office_contact = models.ForeignKey(
        "contacts.Role",
        blank=True, null=True,
        verbose_name=_(
            "Contact person at local job office"),
        related_name='persons_job_office')

    client_state = ClientStates.field(default=ClientStates.newcomer)

    refusal_reason = RefusalReasons.field(blank=True)

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

    mails_by_project = dd.ShowSlaveTable(
        'outbox.MailsByProject',
        sort_index=100,
        icon_name="transmit")

    def disabled_fields(self, ar):
        rv = super(Client, self).disabled_fields(ar)
        if not ar.get_user().profile.newcomers_level:
            rv = rv | set(['broker', 'faculty', 'refusal_reason'])
        #~ logger.info("20130808 pcsw %s", rv)
        return rv

    def get_queryset(self, ar):
        return self.model.objects.select_related(
            'country', 'city', 'nationality')

    def get_excerpt_options(self, ar, **kw):
        # Set project field when creating an excerpt from Client.
        kw.update(project=self)
        return super(Client, self).get_excerpt_options(ar, **kw)

    def get_coachings(self, period=None, **flt):
        qs = self.coachings_by_client.filter(**flt)
        if period is not None:
            qs = self.coachings_by_client.filter(
                only_active_coachings_filter(period))
        return qs

    @dd.chooser()
    def job_office_contact_choices(cls):
        sc = settings.SITE.site_config  # get_site_config()
        if sc.job_office is not None:
            #~ return sc.job_office.contact_set.all()
            #~ return sc.job_office.rolesbyparent.all()
            return sc.job_office.rolesbycompany.all()
            #~ return links.Link.objects.filter(a=sc.job_office)
        return []

    def __unicode__(self):
        #~ return u"%s (%s)" % (self.get_full_name(salutation=False),self.pk)
        if self.is_obsolete:
            return "%s %s (%s*)" % (
                self.last_name.upper(), self.first_name, self.pk)
        return "%s %s (%s)" % (
            self.last_name.upper(), self.first_name, self.pk)

    def get_overview_elems(self, ar):
        elems = super(Client, self).get_overview_elems(ar)
        elems.append(E.br())
        elems.append(self.eid_info(ar))
        # elems += [
        #     E.br(), ar.instance_action_button(self.create_excerpt)]

        # elems = [E.div(*elems)]
        return elems

    def before_state_change(obj, ar, oldstate, newstate):

        if newstate.name == 'former':
            qs = obj.coachings_by_client.filter(end_date__isnull=True)
            if qs.count():
                def ok(ar):
                    for co in qs:
                        #~ co.state = CoachingStates.ended
                        co.end_date = dd.today()
                        co.save()
                    ar.success(refresh=True)
                return ar.confirm(
                    ok,
                    _("This will end %(count)d coachings of %(client)s.")
                    % dict(count=qs.count(), client=unicode(obj)))

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

    def after_ui_save(self, ar):
        super(Client, self).after_ui_save(ar)
        self.update_reminders(ar)
        #~ return kw

    def get_primary_coach(self):
        """Return the one and only primary coach (or `None` if there's less
        or more than one).

        """
        qs = self.coachings_by_client.filter(primary=True).distinct()
        if qs.count() == 1:
            return qs[0].user
        # logger.info("20140725 qs is %s", qs)
        return None

    primary_coach = property(get_primary_coach)

    def update_reminders(self, ar):
        """
        Creates or updates automatic tasks controlled directly by this Person.
        """
        #~ user = self.coach2 or self.coach1
        user = self.get_primary_coach()
        if user:
            with translation.override(user.language):
                M = cal.DurationUnits.months
                cal.update_reminder(1, self, user,
                                    self.card_valid_until,
                                    _("eID card expires in 2 months"), 2, M)
                cal.update_reminder(2, self, user,
                                    self.unavailable_until,
                                    _("becomes available again in 1 month"), 1, M)
                cal.update_reminder(3, self, user,
                                    self.work_permit_suspended_until,
                                    _("work permit suspension ends in 1 month"), 1, M)
                #~ cal.update_reminder(4,self,user,
                  #~ self.coached_until,
                  #~ _("coaching ends in 1 month"),1,M)

    @classmethod
    def get_reminders(model, ui, user, today, back_until):
        q = Q(coach1__exact=user) | Q(coach2__exact=user)

        def find_them(fieldname, today, delta, msg, **linkkw):
            filterkw = {fieldname + '__lte': today + delta}
            if back_until is not None:
                filterkw.update({
                    fieldname + '__gte': back_until
                })
            for obj in model.objects.filter(q, **filterkw).order_by(fieldname):
                linkkw.update(fmt='detail')
                url = ui.get_detail_url(obj, **linkkw)
                html = '<a href="%s">%s</a>&nbsp;: %s' % (url,
                                                          unicode(obj), cgi.escape(msg))
                yield ReminderEntry(getattr(obj, fieldname), html)

        #~ delay = 30
        #~ for obj in model.objects.filter(q,
              #~ card_valid_until__lte=date+datetime.timedelta(days=delay)).order_by('card_valid_until'):
            #~ yield ReminderEntry(obj,obj.card_valid_until,_("eID card expires in %d days") % delay,fmt='detail',tab=3)
        for o in find_them(
            'card_valid_until', today, datetime.timedelta(days=30),
                _("eID card expires"), tab=0):
            yield o
        for o in find_them(
            'unavailable_until', today, datetime.timedelta(days=30),
                _("becomes available again"), tab=1):
            yield o
        for o in find_them(
            'work_permit_suspended_until', today, datetime.timedelta(days=30),
                _("work permit suspension ends"), tab=1):
            yield o
        for o in find_them('coached_until', today, datetime.timedelta(days=30),
                           _("coaching ends"), tab=1):
            yield o

    @dd.virtualfield(dd.HtmlBox())
    def image(self, ar):
        url = self.get_image_url(ar)
        s = '<img src="%s" width="100%%"/>' % url
        s = '<a href="%s" target="_blank">%s</a>' % (url, s)
        return s

    def get_image_parts(self):
        if self.card_number:
            parts = ("beid", self.card_number + ".jpg")
            fn = os.path.join(settings.MEDIA_ROOT, *parts)
            if os.path.exists(fn):
                return parts
        # return ("pictures", "contacts.Person.jpg")
        return ("lino", "contacts.Person.jpg")

    def get_image_url(self, ar):
        return settings.SITE.build_media_url(*self.get_image_parts())

    def get_image_path(self):
        #~ TODO: handle configurability of card_number_to_picture_file
        return os.path.join(settings.MEDIA_ROOT, *self.get_image_parts())

    def get_skills_set(self):
        return self.personproperty_set.filter(
            group=settings.SITE.site_config.propgroup_skills)
    skills_set = property(get_skills_set)

    def properties_list(self, *prop_ids):
        """
        Yields a list of the :class:`PersonProperty <lino_welfare.modlib.cv.models.PersonProperty>` 
        properties of this person in the specified order.
        If this person has no entry for a 
        requested :class:`Property`, it is simply skipped.
        Used in notes/Note/cv.odt"""
        for pk in prop_ids:
            try:
                yield self.personproperty_set.get(property__id=pk)
            except cv.PersonProperty.DoesNotExist:
                pass

    def unused_get_property(self, prop_id):
        """used in notes/Note/cv.odt"""
        return self.personproperty_set.get(property__id=prop_id)
        #~ return PersonProperty.objects.get(property_id=prop_id,person=self)

    def unused_overview(self, request):
        def qsfmt(qs):
            s = qs.model._meta.verbose_name_plural + ': '
            if qs.count():
                s += ', '.join([unicode(lk) for lk in qs])
            else:
                s += '<b>%s</b>' % force_unicode(_("not filled in"))
            return force_unicode(s)

        lines = []
        #~ lines.append('<div>')
        lines.append(qsfmt(self.languageknowledge_set.all()))
        lines.append(qsfmt(self.study_set.all()))
        lines.append(qsfmt(self.contract_set.all()))
        #~ from django.utils.translation import string_concat
        #~ lines.append('</div>')
        return '<br/>'.join(lines)
    unused_overview.return_type = dd.HtmlBox(_("Overview"))

    @dd.displayfield(_("Residence permit"))
    def residence_permit(self, ar):
        kv = dict(type=settings.SITE.site_config.residence_permit_upload_type)
        r = ar.spawn(uploads.UploadsByController,
                     master_instance=self,
                     known_values=kv)
        return ar.renderer.quick_upload_buttons(r)

    @dd.displayfield(_("Work permit"))
    def work_permit(self, ar):
        kv = dict(type=settings.SITE.site_config.work_permit_upload_type)
        r = ar.spawn(uploads.UploadsByController,
                     master_instance=self,
                     known_values=kv)
        return ar.renderer.quick_upload_buttons(r)
    #~ work_permit.return_type = dd.DisplayField(_("Work permit"))

    @dd.displayfield(_("driving licence"))
    #~ @dd.virtualfield(dd.DisplayField(_("driving licence")))
    def driving_licence(self, ar):
        kv = dict(type=settings.SITE.site_config.driving_licence_upload_type)
        r = ar.spawn(uploads.UploadsByController,
                     master_instance=self, known_values=kv)
        return ar.renderer.quick_upload_buttons(r)
    #~ driving_licence.return_type = dd.DisplayField(_("driving licence"))

    def get_active_contract(self):
        """Return the one and only "active contract" of this client.  A
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

    @dd.virtualfield(models.ForeignKey('contacts.Company',
                                       _("Working at ")))
    def contract_company(obj, ar):
        c = obj.get_active_contract()
        if isinstance(c, jobs.Contract):
            return c.company

    @dd.displayfield(_("Active contract"))
    def active_contract(obj, ar):
        c = obj.get_active_contract()
        if c is not None:
            txt = unicode(daterange_text(c.applies_from, c.applies_until))
            if isinstance(c, jobs.Contract):
                if c.company is not None:
                    # txt += unicode(pgettext("(place)", " at "))
                    # txt += '\n'
                    # txt += unicode(c.company)
                    txt = (txt, E.br(), c.company.name)
            return ar.obj2html(c, txt)

    @dd.displayfield(_("Coaches"))
    def coaches(self, ar):
        today = settings.SITE.today()
        period = (today, today)
        items = [unicode(obj.user) for obj in self.get_coachings(period)]
        return ', '.join(items)

    def get_system_note_type(self, ar):
        return settings.SITE.site_config.system_note_type

    def get_system_note_recipients(self, ar, silent):
        for u in settings.SITE.user_model.objects.filter(
                coaching_supervisor=True).exclude(email=''):
            yield "%s <%s>" % (unicode(u), u.email)

    @dd.displayfield(_("Find appointment"))
    def find_appointment(self, ar):  # not used
        elems = []
        for obj in self.coachings_by_client.all():
            sar = extensible.CalendarPanel.request(
                subst_user=obj.user, current_project=self.pk)
            elems += [ar.href_to_request(sar, obj.user.username), ' ']
        return E.div(*elems)

    def get_beid_diffs(self, attrs):
        """Overrides :meth:`dd.beid.BeIdCardHolder.get_beid_diffs`.

        """
        Address = rt.modules.addresses.Address
        DataSources = rt.modules.addresses.DataSources
        diffs = []
        objects = [self]
        kw = dict(partner=self, data_source=DataSources.eid)
        try:
            addr = Address.objects.get(**kw)
        except Address.DoesNotExist:
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
                        unicode(fld.verbose_name), dd.obj2str(old),
                        dd.obj2str(new)))
                setattr(obj, fld.name, new)
        return objects, diffs

    @dd.virtualfield(dd.HtmlBox(_("CBSS")))
    def cbss_relations(self, ar):
        cbss = dd.resolve_app('cbss')
        elems = []
        sar = ar.spawn(
            cbss.RetrieveTIGroupsRequestsByPerson,
            master_instance=self,
            filter=models.Q(status__in=cbss.OK_STATES))
        btn = sar.insert_button()
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


from lino.modlib.excerpts.mixins import Shortcuts
Shortcuts.add_item('pcsw.Client', 'cvs_emitted', _("CVs emitted"))


class ClientDetail(dd.FormLayout):

    main = "general contact coaching aids_tab \
    work_tab career languages \
    competences contracts history calendar misc"

    general = dd.Panel("""
    overview:30 general2:40 general3:20 image:15
    reception.AppointmentsByPartner reception.CoachingsByClient
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
    dedupe.SimilarPersons:10 humanlinks.LinksByHuman:30 cbss_relations:30
    households.MembersByPerson:20 households.SiblingsByPerson:50
    """, label=_("Human Links"))

    coaching = dd.Panel("""
    newcomers_left:20 newcomers.AvailableCoachesByClient:40
    pcsw.ContactsByClient:20 pcsw.CoachingsByClient:40
    """, label=_("Coaching"))

    #~ suche = dd.Panel("""
    #~ is_seeking unemployed_since work_permit_suspended_until
    # ~ # job_office_contact job_agents
    #~ pcsw.ExclusionsByClient:50x3
    #~ """,label = _("Job search"))

    suche = dd.Panel("""
    # job_office_contact job_agents
    pcsw.DispensesByClient:50x3
    pcsw.ExclusionsByClient:50x3
    """)

    papers = dd.Panel("""
    is_seeking unemployed_since work_permit_suspended_until
    needs_residence_permit needs_work_permit
    # residence_permit work_permit driving_licence
    # uploads.UploadsByController
    uploads.UploadsByClient
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

    newcomers_left = dd.Panel("""
    workflow_buttons
    broker:12
    faculty:12
    refusal_reason
    """, required=dict(user_groups='newcomers'))

    #~ coaching_left = """
    #~ """
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
    # cal.EventsByProject
    cal.EventsByClient
    cal.TasksByProject
    """, label=_("Calendar"))

    misc = dd.Panel("""
    activity client_state noble_condition \
    unavailable_until:15 unavailable_why:30
    is_obsolete
    created modified
    remarks:30 contacts.RolesByPerson
    """, label=_("Miscellaneous"), required=dict(user_level='manager'))

    # the career tab will be overwritten by settings.chatelet
    career = dd.Panel("""
    cv.StudiesByPerson
    # cv.TrainingsByPerson
    cv.ExperiencesByPerson:40
    """, label=_("Career"))

    languages = dd.Panel("""
    cv.LanguageKnowledgesByPerson
    courses.CourseRequestsByPerson
    """, label=_("Languages"))

    competences = dd.Panel("""
    cv.SkillsByPerson cv.SoftSkillsByPerson skills
    cv.ObstaclesByPerson obstacles badges.AwardsByHolder
    """, label=_("Competences"), required=dict(user_groups='integ'))

    contracts = dd.Panel("""
    isip.ContractsByPerson
    jobs.CandidaturesByPerson
    jobs.ContractsByPerson
    """, label=_("Contracts"))


def only_coached_by(qs, user):
    return qs.filter(coachings_by_client__user=user).distinct()


def only_coached_on(qs, period, join=None):
    """
    Add a filter to the Queryset `qs` (on model Client) 
    which leaves only the clients that are (or were or will be) coached 
    on the specified date.
    """
    n = 'coachings_by_client__'
    if join:
        n = join + '__' + n
    return qs.filter(only_active_coachings_filter(period, n)).distinct()


def only_active_coachings_filter(period, prefix=''):
    """
    """
    assert len(period) == 2
    args = []
    if period[0]:
        args.append(Q(
            **{prefix + 'end_date__isnull': True}) | Q(
            **{prefix + 'end_date__gte': period[0]}))
    if period[1]:
        args.append(Q(**{prefix + 'start_date__lte': period[1]}))
    return Q(*args)


def add_coachings_filter(qs, user, period, primary):
    assert period is None or len(period) == 2
    if not (user or period or primary):
        return qs
    flt = Q()
    if period:
        flt &= only_active_coachings_filter(period, 'coachings_by_client__')
    if user:
        flt &= Q(coachings_by_client__user=user)
    if primary:
        flt &= Q(coachings_by_client__primary=True)
    return qs.filter(flt).distinct()


def daterange_text(a, b):
    """
    """
    if a == b:
        return dd.dtos(a)
    return dd.dtos(a) + "-" + dd.dtos(b)


ACTIVE_STATES = [ClientStates.coached, ClientStates.newcomer]


class Clients(contacts.Persons):
    # ~ debug_permissions = True # '20120925'
    # required = dd.Required(user_groups='coaching')
    model = 'pcsw.Client'
    params_panel_hidden = True

    #~ create_event = cal.CreateClientEvent()

    insert_layout = dd.FormLayout("""
    first_name last_name
    national_id
    gender language
    """, window_size=(60, 'auto'))

    column_names = "name_column:20 client_state national_id:10 \
    gsm:10 address_column age:10 email phone:10 id aid_type language:10"

    detail_layout = ClientDetail()

    parameters = dd.ObservedPeriod(
        aged_from=models.IntegerField(
            _("Aged from"), blank=True, null=True, help_text=u"""\
Nur Klienten, die mindestens so alt sind."""),
        aged_to=models.IntegerField(
            _("Aged to"), blank=True, null=True, help_text=u"""\
Nur Klienten, die höchstens so alt sind."""),
        coached_by=models.ForeignKey(
            'users.User', blank=True, null=True,
            verbose_name=_("Coached by"), help_text=u"""\
Nur Klienten, die eine Begleitung mit diesem Benutzer haben."""),
        and_coached_by=models.ForeignKey(
            'users.User', blank=True, null=True,
            verbose_name=_("and by"), help_text=u"""\
Nur Klienten, die auch mit diesem Benutzer eine Begleitung haben."""),
        nationality=dd.ForeignKey(
            'countries.Country', blank=True, null=True,
            verbose_name=_("Nationality")),
        observed_event=ClientEvents.field(blank=True),
        only_primary=models.BooleanField(
            _("Only primary clients"), default=False, help_text=u"""\
Nur Klienten, die eine effektive <b>primäre</b> Begleitung haben."""),
        client_state=ClientStates.field(blank=True, help_text=u"""\
Nur Klienten mit diesem Status (Aktenzustand)."""),
        #~ new_since = models.DateField(_("Newly coached since"),blank=True),
        **contacts.Persons.parameters)
    params_layout = """
    aged_from aged_to gender nationality also_obsolete
    client_state coached_by and_coached_by start_date end_date \
    observed_event only_primary
    """

    @classmethod
    def get_request_queryset(self, ar):
        #~ if ar.param_values.client_state == '':
            #~ raise Exception(20130901)
        #~ logger.info("20121010 Clients.get_request_queryset %s",ar.param_values)
        qs = super(Clients, self).get_request_queryset(ar)
        #~ if ar.param_values.new_since:
            #~ qs = only_new_since(qs,ar.param_values.new_since)

        #~ print(20130901,ar.param_values)

        # 20140912 don't remember why blank period was interpreted in
        # a special way for coached_by and and_coached_by...
        # if ar.param_values.start_date is None or ar.param_values.end_date is None:
        #     period = None
        # else:
        #     period = (ar.param_values.start_date, ar.param_values.end_date)

        period = [ar.param_values.start_date, ar.param_values.end_date]
        if period[0] is None:
            period[0] = period[1] or dd.today()
        if period[1] is None:
            period[1] = period[0]

        qs = add_coachings_filter(qs,
                                  ar.param_values.coached_by,
                                  period,
                                  ar.param_values.only_primary)
        if ar.param_values.and_coached_by:
            qs = add_coachings_filter(qs,
                                      ar.param_values.and_coached_by,
                                      period,
                                      False)

        ce = ar.param_values.observed_event
        if ce is None:
            pass
        elif ce == ClientEvents.active:
            if ar.param_values.client_state is None:
                qs = qs.filter(client_state__in=ACTIVE_STATES)
        elif ce == ClientEvents.isip:
            f1 = Q(isip_contract_set_by_client__applies_until__isnull=True) | Q(
                isip_contract_set_by_client__applies_until__gte=period[0])
            flt = f1 & (Q(isip_contract_set_by_client__date_ended__isnull=True)
                        | Q(isip_contract_set_by_client__date_ended__gte=period[0]))
            flt &= Q(isip_contract_set_by_client__applies_from__lte=period[1])
            qs = qs.filter(flt).distinct()
        elif ce == ClientEvents.jobs:
            f1 = Q(jobs_contract_set_by_client__applies_until__isnull=True) | Q(
                jobs_contract_set_by_client__applies_until__gte=period[0])
            flt = f1 & (Q(jobs_contract_set_by_client__date_ended__isnull=True)
                        | Q(jobs_contract_set_by_client__date_ended__gte=period[0]))
            flt &= Q(jobs_contract_set_by_client__applies_from__lte=period[1])
            qs = qs.filter(flt).distinct()

        elif ce == ClientEvents.dispense:
            qs = qs.filter(
                dispense__end_date__gte=period[0],
                dispense__start_date__lte=period[1]).distinct()
        elif ce == ClientEvents.created:
            qs = qs.filter(
                created__gte=datetime.datetime.combine(
                    period[0], datetime.time()),
                created__lte=datetime.datetime.combine(period[1], datetime.time()))
            #~ print 20130527, qs.query
        elif ce == ClientEvents.modified:
            qs = qs.filter(
                modified__gte=datetime.datetime.combine(
                    period[0], datetime.time()),
                modified__lte=datetime.datetime.combine(period[1], datetime.time()))
        elif ce == ClientEvents.penalty:
            qs = qs.filter(
                exclusion__excluded_until__gte=period[0],
                exclusion__excluded_from__lte=period[1]).distinct()
        elif ce == ClientEvents.note:
            qs = qs.filter(
                notes_note_set_by_project__date__gte=period[0],
                notes_note_set_by_project__date__lte=period[1]).distinct()
        else:
            raise Warning(repr(ce))

        if ar.param_values.client_state:
            qs = qs.filter(client_state=ar.param_values.client_state)

        if ar.param_values.nationality:
            qs = qs.filter(nationality__exact=ar.param_values.nationality)
        today = settings.SITE.today()
        if ar.param_values.aged_from:
            min_date = today - \
                datetime.timedelta(days=ar.param_values.aged_from * 365)
            qs = qs.filter(birth_date__lte=min_date.strftime("%Y-%m-%d"))
            #~ qs = qs.filter(birth_date__lte=today-datetime.timedelta(days=search.aged_from*365))
        if ar.param_values.aged_to:
            #~ q1 = models.Q(birth_date__isnull=True)
            #~ q2 = models.Q(birth_date__lte=today-datetime.timedelta(days=search.aged_to*365))
            #~ qs = qs.filter(q1|q2)
            max_date = today - \
                datetime.timedelta(days=ar.param_values.aged_to * 365)
            qs = qs.filter(birth_date__gte=max_date.strftime("%Y-%m-%d"))
            #~ qs = qs.filter(birth_date__gte=today-datetime.timedelta(days=search.aged_to*365))

        #~ print(20130901,qs.query)

        return qs

    @classmethod
    def param_defaults(self, ar, **kw):
        kw = super(Clients, self).param_defaults(ar, **kw)
        kw.update(client_state=ClientStates.coached)
        return kw

    @classmethod
    def get_title_tags(self, ar):
        for t in super(Clients, self).get_title_tags(ar):
            yield t
        if ar.param_values.aged_from or ar.param_values.aged_to:
            yield unicode(_("Aged %(min)s to %(max)s") % dict(
                min=ar.param_values.aged_from or'...',
                max=ar.param_values.aged_to or '...'))

        if ar.param_values.observed_event:
            yield unicode(ar.param_values.observed_event)

        if ar.param_values.client_state:
            yield unicode(ar.param_values.client_state)

        if ar.param_values.start_date is None or ar.param_values.end_date is None:
            period = None
        else:
            period = daterange_text(
                ar.param_values.start_date, ar.param_values.end_date)

        if ar.param_values.coached_by:
            s = unicode(self.parameters['coached_by'].verbose_name) + \
                ' ' + unicode(ar.param_values.coached_by)
            if ar.param_values.and_coached_by:
                s += " %s %s" % (unicode(_('and')),
                                 ar.param_values.and_coached_by)

            if period:
                yield s \
                    + _(' on %(date)s') % dict(date=period)
            else:
                yield s
        elif period:
            yield _("Coached on %s") % period

        if ar.param_values.only_primary:
            #~ yield unicode(_("primary"))
            yield unicode(self.parameters['only_primary'].verbose_name)

    @classmethod
    def apply_cell_format(self, ar, row, col, recno, td):
        if row.client_state == ClientStates.newcomer:
            td.attrib.update(bgcolor="green")

    @classmethod
    def get_row_classes(cls, obj, ar):
        if obj.client_state == ClientStates.newcomer:
            yield 'green'
        elif obj.client_state in (ClientStates.refused, ClientStates.former):
            yield 'yellow'
        #~ if not obj.has_valid_card_data():
            #~ return 'red'


class ClientsByNationality(Clients):
    #~ app_label = 'contacts'
    master_key = 'nationality'
    order_by = "city name".split()
    column_names = "city street street_no street_box addr2 name country language *"


class AllClients(Clients):
    column_names = '*'
    required = dd.Required(user_level='admin')

#~ class MyClients(integ.Clients):
    #~ label = _("Integration Clients")
    # ~ # label = _("My clients")
    #~ required = dict(user_groups = 'integ')
    #~ use_as_default_table = False

    #~ @classmethod
    #~ def param_defaults(self,ar,**kw):
        #~ kw = super(MyClients,self).param_defaults(ar,**kw)
        #~ kw.update(coached_by=ar.get_user())
        # ~ # print "20120918 MyClients.param_defaults", kw['coached_by']
        #~ return kw


class ClientsTest(Clients):
    help_text = _(
        "Table of Clients whose data seems unlogical or inconsistent.")
    required = dict(user_level='manager')
    use_as_default_table = False
    label = _("Data Test Clients")
    parameters = dict(
        invalid_niss=models.BooleanField(
            _("Check NISS validity"), default=True),
        overlapping_contracts=models.BooleanField(
            _("Check for overlapping contracts"), default=True),
        **Clients.parameters)
    params_layout = """
    aged_from aged_to gender also_obsolete
    client_state coached_by and_coached_by start_date end_date observed_event
    invalid_niss overlapping_contracts only_primary nationality
    """

    column_names = "name_column error_message national_id id"

    @classmethod
    def get_row_by_pk(self, ar, pk):
        """
        This would be to avoid "AttributeError 'Client' object has no attribute 'error_message'"
        after a PUT from GridView.
        Not tested.
        """
        obj = super(ClientsTest, self).get_row_by_pk(ar, pk)
        if obj is None:
            return obj
        return list(self.get_data_rows(ar, [obj]))[0]

    @classmethod
    def get_data_rows(self, ar, qs=None):
        """
        """
        #~ from lino_welfare.modlib.isip.models import OverlappingContractsTest
        #~ qs = Person.objects.all()

        if qs is None:
            qs = self.get_request_queryset(ar)

        #~ logger.info("Building ClientsTest data rows...")
        #~ for p in qs.order_by('name'):
        for obj in qs:
            messages = []
            if ar.param_values.overlapping_contracts:
                messages += isip.OverlappingContractsTest(obj).check_all()

            if ar.param_values.invalid_niss and obj.national_id is not None:
                try:
                    ssin.ssin_validator(obj.national_id)
                except ValidationError, e:
                    messages += e.messages

            if messages:
                #~ client.error_message = ';<br/>'.join([cgi.escape(m) for m in messages])
                obj.error_message = ';\n'.join(messages)
                #~ logger.info("%s : %s", p, p.error_message)
                yield obj

        #~ logger.info("Building ClientsTest data rows: done")

    @dd.displayfield(_('Error message'))
    def error_message(self, obj, ar):
        #~ return obj.error_message.replace('\n','<br/>')
        return obj.error_message


#
# PERSON GROUP
#
class PersonGroup(dd.Model):
    name = models.CharField(_("Designation"), max_length=200)
    ref_name = models.CharField(_("Reference name"), max_length=20, blank=True)
    active = models.BooleanField(_("Considered active"), default=True)
    #~ text = models.TextField(_("Description"),blank=True,null=True)

    class Meta:
        verbose_name = _("Integration Phase")
        verbose_name_plural = _("Integration Phases")

    def __unicode__(self):
        return self.name


class PersonGroups(dd.Table):
    help_text = _("Liste des phases d'intégration possibles.")
    model = 'pcsw.PersonGroup'
    required = dict(user_level='manager', user_groups='integ')

    order_by = ["ref_name"]


#
# ACTIVITIY (Berufscode)
#
class Activity(dd.Model):

    class Meta:
        verbose_name = _("activity")
        verbose_name_plural = _("activities")
    name = models.CharField(max_length=80)
    lst104 = models.BooleanField(_("Appears in Listing 104"), default=False)

    def __unicode__(self):
        return unicode(self.name)


class Activities(dd.Table):
    help_text = _("""Liste des "activités" ou "codes profession".""")
    model = 'pcsw.Activity'
    #~ required_user_level = UserLevels.manager
    required = dict(user_level='manager')
    #~ label = _('Activities')

#~ class ActivitiesByPerson(Activities):
    #~ master_key = 'activity'

#~ class ActivitiesByCompany(Activities):
    #~ master_key = 'activity'


class DispenseReason(mixins.BabelNamed, mixins.Sequenced):

    class Meta:
        verbose_name = _("Dispense reason")
        verbose_name_plural = _('Dispense reasons')

    #~ name = models.CharField(_("designation"),max_length=200)
    #~
    #~ def __unicode__(self):
        #~ return unicode(self.name)


class DispenseReasons(dd.Table):
    help_text = _("A list of reasons for being dispensed")
    required = dict(user_groups='coaching', user_level='manager')
    model = 'pcsw.DispenseReason'
    column_names = 'seqno name *'
    order_by = ['seqno']


class Dispense(dd.Model):

    class Meta:
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
    required = dict(user_groups='coaching', user_level='manager')
    model = 'pcsw.Dispense'


class DispensesByClient(Dispenses):
    master_key = 'client'
    column_names = 'start_date end_date reason remarks:10'
    hidden_columns = 'id'
    auto_fit_column_widths = True
    required = dict(user_groups='coaching')


class ExclusionType(dd.Model):

    class Meta:
        verbose_name = _("Exclusion Type")
        verbose_name_plural = _('Exclusion Types')

    name = models.CharField(max_length=200)

    def __unicode__(self):
        return unicode(self.name)


class ExclusionTypes(dd.Table):
    help_text = _("""Liste des raisons possibles d'arrêter temporairement 
    le paiement d'une aide financière prévue.""")
    required = dict(user_level='manager')
    #~ required_user_level = UserLevels.manager
    model = 'pcsw.ExclusionType'
    #~ label = _('Exclusion Types')


class Exclusion(dd.Model):

    class Meta:
        verbose_name = _("Penalty")
        verbose_name_plural = _('Penalties')

    person = models.ForeignKey('pcsw.Client')
    type = models.ForeignKey("pcsw.ExclusionType",
                             verbose_name=_("Reason"),
                             blank=True, null=True)
    excluded_from = models.DateField(blank=True, null=True,
                                     verbose_name=_("Excluded from"))
    excluded_until = models.DateField(blank=True, null=True,
                                      verbose_name=_("until"))
    remark = models.CharField(_("Remark"), max_length=200, blank=True)

    def __unicode__(self):
        s = unicode(self.type)
        if self.excluded_from:
            s += ' ' + unicode(self.excluded_from)
        if self.excluded_until:
            s += '-' + unicode(self.excluded_until)
        return s


class Exclusions(dd.Table):
    required = dd.required(user_level='admin')
    help_text = _("Liste des exclusions.")

    #~ required_user_level = UserLevels.manager
    model = 'pcsw.Exclusion'
    #~ label = _('Exclusions')


class ExclusionsByClient(Exclusions):
    required = dd.required(user_groups='coaching')
    #~ required_user_level = None
    master_key = 'person'
    column_names = 'excluded_from excluded_until type remark:10'
    auto_fit_column_widths = True


class Conviction(dd.Model):

    class Meta:
        verbose_name = _("Conviction")
        verbose_name_plural = _('Convictions')

    client = models.ForeignKey('pcsw.Client')
    date = models.DateField(_("Date"), blank=True)
    prejudicial = models.BooleanField(_("Prejudicial"), default=False)
    designation = models.CharField(
        _("Designation"), max_length=200, blank=True)

    def full_clean(self, *args, **kw):
        if self.date is None:
            self.date = dd.today()
        super(Conviction, self).full_clean(*args, **kw)

    def __unicode__(self):
        s = unicode(self.designation)
        if self.date:
            s += ' (%s)' % dd.fds(self.date)
        return s


class Convictions(dd.Table):
    required = dd.required(user_level='admin')
    model = 'pcsw.Conviction'


class ConvictionsByClient(Convictions):
    required = dd.required(user_groups='coaching')
    master_key = 'client'
    column_names = 'date designation prejudicial'
    auto_fit_column_widths = True


#
# AID TYPES
#
class AidType(mixins.BabelNamed):

    class Meta:
        verbose_name = _("aid type")
        verbose_name_plural = _('aid types')


class AidTypes(dd.Table):
    help_text = _("Liste des types d'aide financière.")
    model = 'pcsw.AidType'
    column_names = 'name *'
    #~ required_user_level = UserLevels.manager
    required = dict(user_level='manager')


class ClientContactType(mixins.BabelNamed):

    class Meta:
        verbose_name = _("Client Contact type")
        verbose_name_plural = _("Client Contact types")


class ClientContactTypes(dd.Table):
    help_text = _("Liste des types de contacts client.")
    model = 'pcsw.ClientContactType'
    required = dd.required(user_level='manager')

    # TODO: `can_refund` is injected in aids, `is_bailiff` in debts
    # NOTE: this is being overridden by lino_welfare.projects.eupen
    detail_layout = """
    id name
    contacts.PartnersByClientContactType
    pcsw.ClientContactsByType
    """

    column_names = 'id name *'

    stay_in_grid = True


class ClientContactBase(contacts.ContactRelated):
    # also used by lino_welfare.modlib.aids.models.RefundPartner
    class Meta:
        abstract = True
    type = dd.ForeignKey('pcsw.ClientContactType', blank=True, null=True)

    @dd.chooser()
    def company_choices(self, type):
        qs = contacts.Companies.request().data_iterator
        if type is not None:
            qs = qs.filter(client_contact_type=type)
        return qs

    @dd.chooser()
    def contact_person_choices(self, type):
        qs = contacts.Persons.request().data_iterator
        if type is not None:
            qs = qs.filter(client_contact_type=type)
        return qs

    def __unicode__(self):
        return unicode(self.contact_person or self.company or self.type)


class ClientContact(ClientContactBase):
    """
    client : the Client
    company : the Company
    contact_person : the Contact person in the Company
    contact_role : the role of the contact person in the Company
    """
    class Meta:
        verbose_name = _("Client Contact")
        verbose_name_plural = _("Client Contacts")
    #~ type = ClientContactTypes.field(blank=True)
    client = dd.ForeignKey('pcsw.Client')
    remark = models.TextField(_("Remarks"), blank=True)  # ,null=True)

    def full_clean(self, *args, **kw):
        if not self.remark and not self.type \
           and not self.company and not self.contact_person:
            raise ValidationError(_("Must fill at least one field."))
        super(ClientContact, self).full_clean(*args, **kw)


dd.update_field(ClientContact, 'contact_person',
                verbose_name=_("Contact person"))


class ClientContacts(dd.Table):
    required = dd.required(user_level='admin')
    help_text = _("Liste des contacts clients.")
    model = 'pcsw.ClientContact'


class ContactsByClient(ClientContacts):
    required = dd.required()
    master_key = 'client'
    column_names = 'type company contact_person remark *'
    label = _("Contacts")
    auto_fit_column_widths = True


class ClientContactsByType(ClientContacts):
    required = dd.required()
    master_key = 'type'
    column_names = 'company contact_person client remark *'
    label = _("Contacts")
    auto_fit_column_widths = True

config = dd.plugins.pcsw


def setup_main_menu(site, ui, profile, m):
    m = m.add_menu(config.app_label, config.verbose_name)
    m.add_action('pcsw.MyCoachings')


def setup_config_menu(site, ui, profile, m):
    m = m.add_menu(config.app_label, config.verbose_name)
    m.add_action('pcsw.PersonGroups')
    m.add_action('pcsw.Activities')
    m.add_action('pcsw.ExclusionTypes')
    m.add_action('pcsw.CoachingTypes')
    m.add_action('pcsw.CoachingEndings')
    m.add_action('pcsw.DispenseReasons')
    m.add_action('pcsw.ClientContactTypes')


def setup_explorer_menu(site, ui, profile, m):
    m = m.add_menu(config.app_label, config.verbose_name)
    m.add_action('pcsw.Coachings')
    m.add_action('pcsw.ClientContacts')
    m.add_action('pcsw.Exclusions')
    m.add_action('pcsw.Convictions')
    m.add_action(AllClients)
    #~ m.add_action(PersonSearches)
    m.add_action('pcsw.CivilState')
    m.add_action('pcsw.ClientStates')
    m.add_action('beid.BeIdCardTypes')


def setup_reports_menu(site, ui, profile, m):
    m = m.add_menu(config.app_label, config.verbose_name)
    #~ m.add_action(site.modules.jobs.OldJobsOverview)
    #~ m.add_action(site.modules.integ.UsersWithClients)
    m.add_action(ClientsTest)
    #~ m  = m.add_menu("pcsw",pcsw.MODULE_LABEL)
    # ~ m.add_action(ActivityReport1) # old version


def setup_quicklinks(self, ar, tb):
    tb.add_action('pcsw.Clients', 'find_by_beid')


def setup_workflows(site):

    #~ ClientStates.newcomer.add_transition(states='refused coached invalid former',user_groups='newcomers')
    if False:  # removed 20130904

        def allow_state_newcomer(action, user, obj, state):
            """
            A Client with at least one Coaching cannot become newcomer.
            """
            #~ if obj.client_state == ClientStates.coached:
            if obj.coachings_by_client.count() > 0:
                return False
            return True

        ClientStates.newcomer.add_transition(
            states='refused coached former',
            user_groups='newcomers', allow=allow_state_newcomer)

    ClientStates.refused.add_transition(RefuseClient)
    #~ ClientStates.refused.add_transition(_("Refuse"),states='newcomer invalid',user_groups='newcomers',notify=True)
    #~ ClientStates.coached.add_transition(_("Coached"),states='new',user_groups='newcomers')
    ClientStates.former.add_transition(
        _("Former"),
        #~ states='coached invalid',
        states='coached',
        user_groups='newcomers')
    #~ ClientStates.add_transition('new','refused',user_groups='newcomers')


dd.add_user_group('coaching', _("Coaching"))


# class SimilarPersons(dedupe.SimilarPersons):
    
#     @classmethod
#     def get_target_model(self, obj):
#         return contacts.Person
    
