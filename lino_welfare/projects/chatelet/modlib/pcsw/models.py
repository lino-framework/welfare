# -*- coding: UTF-8 -*-
# Copyright 2014 Luc Saffre
# License: BSD (see file COPYING for details)

from __future__ import unicode_literals
from __future__ import print_function

import logging
logger = logging.getLogger(__name__)

from django.utils.translation import ugettext_lazy as _

from lino import dd, rt

from lino_welfare.modlib.pcsw.models import *


class Client(Client):
    sis_motif = models.TextField(_("Motif de l'orientation"), blank=True)
    sis_attentes = models.TextField(_("Attentes de la personne"), blank=True)
    sis_moteurs = models.TextField(_("Moteurs"), blank=True)
    sis_objectifs = models.TextField(_("Objectifs"), blank=True)
    oi_demarches = models.TextField(_("Démarches à réaliser"), blank=True)
    

class ClientDetail(dd.FormLayout):

    main = "general coaching family \
    career competences #aids_tab sis_tab isip.ContractsByPerson \
    oi_tab #projects_tab \
    job_search contracts history calendar misc"

    oi_tab = dd.Panel("""
    courses.BasicEnrolmentsByPupil
    courses.JobEnrolmentsByPupil
    oi_demarches
    """, label=_("Orientation interne"))

    general = dd.Panel("""
    overview:30 general2:40 general3:20 image:15
    national_id:15 civil_state birth_country birth_place declared_name
    in_belgium_since:15 residence_type residence_until group:16
    reception.AppointmentsByPartner reception.CoachingsByClient courses.EnrolmentsByPupil
    """, label=_("Person"))

    general2 = """
    gender:10 id:10 nationality:15
    last_name
    first_name middle_name
    birth_date age:10 language
    """

    general3 = """
    email
    phone
    fax
    gsm
    """

    family = dd.Panel("""
    households.MembersByPerson:20 households.SiblingsByPerson:50
    humanlinks.LinksByHuman:30
    """, label=_("Family situation"))

    coaching = dd.Panel("""
    newcomers_left:20 projects.ProjectsByClient
    newcomers.AvailableCoachesByClient:40
    pcsw.ContactsByClient:20 pcsw.CoachingsByClient:40
    """, label=_("Coaches"))

    suche = dd.Panel("""
    pcsw.DispensesByClient
    pcsw.ExclusionsByClient
    pcsw.ConvictionsByClient
    """)

    papers = dd.Panel("""
    is_seeking unemployed_since work_permit_suspended_until
    polls.ResponsesByPartner
    needs_residence_permit needs_work_permit
    uploads.UploadsByClient
    """)

    job_search = dd.Panel("""
    suche:40  papers:40
    """, label=_("Job search"))

    # projects_tab = dd.Panel("""
    # projects.ProjectsByClient
    # """, label=dd.plugins.projects.verbose_name)

    aids_tab = dd.Panel("""
    sepa.AccountsByClient
    aids.GrantingsByClient
    """, label=_("Aids"))

    newcomers_left = dd.Panel("""
    workflow_buttons
    broker:12
    faculty:12
    # refusal_reason
    """, required=dict(user_groups='newcomers'))

    #~ coaching_left = """
    #~ """
    history = dd.Panel("""
    # reception.CreateNoteActionsByClient:20
    notes.NotesByProject
    excerpts.ExcerptsByProject
    # lino.ChangesByMaster
    """, label=_("History"))

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
    aids.GrantingsByClient
    """, label=_("Miscellaneous"), required=dict(user_level='manager'))

    contracts = dd.Panel("""
    jobs.CandidaturesByPerson
    jobs.ContractsByPerson
    """, label=dd.plugins.jobs.verbose_name)

    sis_tab = dd.Panel("""
    #courses.IntegEnrolmentsByPupil #isip.ContractsByPerson
    sis_motif sis_attentes
    sis_moteurs sis_objectifs
    """, label=_("SIS"))

    career = dd.Panel("""
    cv.StudiesByPerson
    cv.TrainingsByPerson
    cv.ExperiencesByPerson
    """, label=_("Career"))

    competences = dd.Panel(
        "good_panel bad_panel",
        label=_("Competences"),
        required=dict(user_groups='integ'))

    good_panel = """
    cv.SkillsByPerson cv.SoftSkillsByPerson
    cv.LanguageKnowledgesByPerson skills
    """

    bad_panel = """
    cv.ObstaclesByPerson
    obstacles
    """

Clients.detail_layout = ClientDetail()

households = dd.resolve_app('households')
households.SiblingsByPerson.slave_grid_format = 'grid'

# humanlinks = dd.resolve_app('humanlinks')
# humanlinks.LinksByHuman.slave_grid_format = 'grid'

cv = dd.resolve_app('cv')
# cv.ExperiencesByPerson.column_names = "company start_date end_date \
# function regime status is_training country remarks *"

# cv.StudiesByPerson.column_names = "type content start_date end_date \
# school country success language remarks *"

ContactsByClient.column_names = 'company contact_person remark'
dd.update_field(ClientContact, 'remark', verbose_name=_("Contact details"))
