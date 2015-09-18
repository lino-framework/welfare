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

from __future__ import unicode_literals
from __future__ import print_function

import logging
logger = logging.getLogger(__name__)

from django.utils.translation import ugettext_lazy as _

from lino.api import dd

from lino_welfare.modlib.integ.roles import IntegrationAgent
from lino_welfare.modlib.pcsw.roles import SocialStaff, SocialAgent
from lino.modlib.contacts.roles import ContactsStaff

from lino_welfare.modlib.pcsw.models import *

from lino.modlib.vatless.mixins import PartnerDetailMixin


class Client(Client):
    remarks2 = models.TextField(
        _("Remarks (Social Office)"), blank=True, editable=False)
    gesdos_id = models.CharField(_("Gesdos ID"), max_length=40, blank=True)
    tim_id = models.CharField(_("TIM ID"), max_length=10, blank=True)

    is_cpas = models.BooleanField(_("receives social help"), default=False)
    is_senior = models.BooleanField(_("is senior"), default=False)
    
    health_insurance = dd.ForeignKey(
        'contacts.Company', blank=True, null=True,
        verbose_name=_("Health insurance"),
        related_name='health_insurance_for')
    pharmacy = dd.ForeignKey(
        'contacts.Company', blank=True, null=True,
        verbose_name=_("Pharmacy"),
        related_name='pharmacy_for')

    # Arbeitslosengeld
    income_ag = models.BooleanField(_("unemployment benefit"), default=False)
    # Wartegeld
    income_wg = models.BooleanField(_("waiting pay"), default=False)
    # Krankengeld
    income_kg = models.BooleanField(_("sickness benefit"), default=False)
    income_rente = models.BooleanField(
        _("retirement pension"), default=False)  # Rente
    # Andere Einkommen
    income_misc = models.BooleanField(_("other incomes"), default=False)

    job_agents = models.CharField(max_length=100,
                                  blank=True,  # null=True,
                                  verbose_name=_("Job agents"))

    @classmethod
    def on_analyze(cls, site):
        super(Client, cls).on_analyze(site)
        cls.declare_imported_fields(
            '''remarks2
            health_insurance pharmacy
            is_cpas is_senior
            gesdos_id tim_id
            ''')

dd.update_field('contacts.Partner', 'remarks', editable=False)


class ClientDetail(ClientDetail, PartnerDetailMixin):

    main = "general contact coaching aids_tab \
    work_tab career languages \
    competences contracts history calendar ledger misc"

    general = dd.Panel("""
    overview:30 general2:40 general3:20 image:15
    reception.AppointmentsByPartner reception.AgentsByClient
    """, label=_("Person"))

    general2 = """
    gender:10 id:8 tim_id:8
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
    dupable_clients.SimilarClients:10 humanlinks.LinksByHuman:30 cbss_relations:30
    households.MembersByPerson:20 households.SiblingsByPerson:50
    """, label=_("Human Links"))

    suche = dd.Panel("""
    # job_office_contact job_agents
    pcsw.DispensesByClient:50x3
    pcsw.ExclusionsByClient:50x3
    """)

    papers = dd.Panel("""
    is_seeking unemployed_since work_permit_suspended_until
    needs_residence_permit needs_work_permit
    uploads.UploadsByClient
    """)  # ,label = _("Papers"))

    work_tab = dd.Panel("""
    suche:40  papers:40
    """, label=_("Job search"))

    aids_tab = dd.Panel("""
    status:55 income:25
    sepa.AccountsByClient
    aids.GrantingsByClient
    """, label=_("Aids"))

    status = """
    in_belgium_since:15 residence_type gesdos_id #tim_id
    job_agents group:16 aid_type
    """

    income = """
    income_ag  income_wg
    income_kg   income_rente
    income_misc
    """

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
    is_cpas is_senior is_obsolete
    created modified
    remarks:30 remarks2:30
    plausibility.ProblemsByOwner:30 contacts.RolesByPerson:20
    """, label=_("Miscellaneous"),
        required_roles=dd.required((SocialStaff, ContactsStaff)))

    career = dd.Panel("""
    cvs_emitted
    cv.StudiesByPerson
    cv.TrainingsByPerson
    cv.ExperiencesByPerson:40
    """, label=_("Career"), required_roles=dd.required(IntegrationAgent))

    languages = dd.Panel("""
    cv.LanguageKnowledgesByPerson
    courses.CourseRequestsByPerson
    """, label=_("Languages"))

    competences = dd.Panel("""
    cv.SkillsByPerson cv.SoftSkillsByPerson skills
    cv.ObstaclesByPerson obstacles badges.AwardsByHolder
    """, label=_("Competences"), required_roles=dd.required(IntegrationAgent))

    contracts = dd.Panel("""
    isip.ContractsByClient
    jobs.CandidaturesByPerson
    jobs.ContractsByClient
    """, label=_("Contracts"))

if settings.SITE.is_installed('cbss'):
    ClientDetail.main += ' cbss'
    ClientDetail.cbss = dd.Panel("""
cbss_identify_person cbss_manage_access cbss_retrieve_ti_groups
cbss_summary
    """, label=_("CBSS"), required_roles=dd.required(SocialAgent))


Clients.detail_layout = ClientDetail()

ClientContactTypes.detail_layout = """
id name can_refund is_bailiff
contacts.PartnersByClientContactType
pcsw.ClientContactsByType
"""
ClientContactTypes.column_names = "id name can_refund is_bailiff"
