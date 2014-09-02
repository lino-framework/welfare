# -*- coding: UTF-8 -*-
# Copyright 2014 Luc Saffre
# This file is part of the Lino Welfare project.
# Lino Welfare is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
# Lino Welfare is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with Lino Welfare; if not, see <http://www.gnu.org/licenses/>.

from __future__ import unicode_literals
from __future__ import print_function

import logging
logger = logging.getLogger(__name__)

from django.utils.translation import ugettext_lazy as _

from lino import dd

from lino_welfare.modlib.pcsw.models import *


class Client(Client):
    sis_motif = models.TextField(_("Motif de l'orientation"), blank=True)
    sis_attentes = models.TextField(_("Attentes de la personne"), blank=True)
    sis_moteurs = models.TextField(_("Moteurs"), blank=True)
    sis_objectifs = models.TextField(_("Objectifs"), blank=True)
    oi_demarches = models.TextField(_("Démarches à réaliser"), blank=True)
    

class ClientDetail(dd.FormLayout):

    main = "general parties family \
    career competences sis_tab oi_tab projects_tab \
    job_search contracts history calendar misc"

    oi_tab = dd.Panel("""
    courses.BasicEnrolmentsByPupil
    courses.JobEnrolmentsByPupil
    oi_demarches
    """, label=_("Orientation interne"))

    projects_tab = dd.Panel("""
    projects.ProjectsByClient
    """, label=dd.plugins.projects.verbose_name)

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
    humanlinks.LinksByHuman:30
    households.MembersByPerson:20 households.SiblingsByPerson:50
    """, label=_("Family situation"))

    parties = dd.Panel("""
    newcomers_left:20 newcomers.AvailableCoachesByClient:40
    pcsw.ContactsByClient:20 pcsw.CoachingsByClient:40
    """, label=_("Intervening parties"))

    suche = dd.Panel("""
    # job_office_contact job_agents
    pcsw.DispensesByClient:50x3
    pcsw.ExclusionsByClient:50x3
    """)

    papers = dd.Panel("""
    is_seeking unemployed_since work_permit_suspended_until
    needs_residence_permit needs_work_permit
    uploads.UploadsByClient
    """)

    job_search = dd.Panel("""
    suche:40  papers:40
    """, label=_("Job search"))

    # aids_tab = dd.Panel("""
    # sepa.AccountsByClient
    # aids.GrantingsByClient
    # """, label=_("Aids"))

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

    contracts = dd.Panel("""
    jobs.CandidaturesByPerson
    jobs.ContractsByPerson
    """, label=dd.plugins.jobs.verbose_name)

    sis_tab = dd.Panel("""
    courses.IntegEnrolmentsByPupil isip.ContractsByPerson
    sis_motif sis_attentes
    sis_moteurs sis_objectifs
    """, label=_("SIS"))

    career = dd.Panel("""
    jobs.StudiesByPerson
    # jobs.TrainingsByPerson
    jobs.ExperiencesByPerson
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

jobs = dd.resolve_app('jobs')
jobs.ExperiencesByPerson.column_names = "company started stopped \
function regime status is_training country remarks *"

jobs.StudiesByPerson.column_names = "type content started stopped \
school country success language remarks *"
