# -*- coding: UTF-8 -*-
# Copyright 2015-2016 Luc Saffre
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

from lino_xl.lib.contacts.roles import ContactsUser
from lino_xl.lib.cv.roles import CareerUser
from lino_welfare.modlib.newcomers.roles import (NewcomersAgent,
                                                 NewcomersOperator)
from lino_welfare.modlib.integ.roles import IntegrationAgent
from lino_welfare.modlib.pcsw.roles import SocialStaff

from lino_welfare.modlib.pcsw.models import *


class ClientDetail(ClientDetail):

    main = "general coaching family \
    career competences obstacles_tab isip_tab \
    courses_tab immersion_tab \
    job_search contracts history calendar misc"

    general = dd.Panel("""
    overview:30 general2:40 general3:20 image:15
    national_id:15 civil_state:20 birth_country birth_place \
    declared_name:15 needs_residence_permit:20 needs_work_permit:20
    in_belgium_since:15 residence_type residence_until group:16 aid_type
    reception.AppointmentsByPartner:40 reception.AgentsByClient:30 \
    courses.EnrolmentsByPupil:40
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
    family_left:20 households.SiblingsByPerson:50
    humanlinks.LinksByHuman:30
    """, label=_("Family situation"),
    required_roles=dd.login_required(ContactsUser))

    family_left = """
    households.MembersByPerson
    child_custody
    """

    coaching = dd.Panel("""
    newcomers_left:20 newcomers.AvailableCoachesByClient:40
    coachings.CoachingsByClient:40
    """, label=_("Coaches"))

    newcomers_left = dd.Panel("""
    workflow_buttons id_document
    faculty:12
    clients.ContactsByClient:20
    """, required_roles=dd.login_required((NewcomersAgent, NewcomersOperator)))

    suche = dd.Panel("""
    is_seeking unemployed_since seeking_since work_permit_suspended_until
    pcsw.DispensesByClient
    pcsw.ExclusionsByClient
    # pcsw.ConvictionsByClient
    """, required_roles=dd.login_required(ContactsUser))

    papers = dd.Panel("""
    active_job_search.ProofsByClient
    polls.ResponsesByPartner
    """, required_roles=dd.login_required(ContactsUser))

    job_search = dd.Panel("""
    suche:40 papers:40
    """, label=dd.plugins.active_job_search.short_name)

    # projects_tab = dd.Panel("""
    # projects.ProjectsByClient
    # """, label=dd.plugins.projects.verbose_name)

    immersion_tab = dd.Panel("""
    immersion.ContractsByClient
    """, label=dd.plugins.immersion.verbose_name)

    # aids_tab = dd.Panel("""
    # sepa.AccountsByClient
    # aids.GrantingsByClient
    # """, label=_("Aids"))

    history = dd.Panel("history_left history_right", label=_("History"))

    history_left = """
    # reception.CreateNoteActionsByClient:20
    notes.NotesByProject
    # lino.ChangesByMaster
    """
    history_right = """
    uploads.UploadsByClient
    excerpts.ExcerptsByProject
    esf.SummariesByClient
    """

    calendar = dd.Panel("""
    # find_appointment
    # cal.EntriesByProject
    cal.EntriesByClient
    cal.TasksByProject
    """, label=_("Calendar"))

    misc = dd.Panel("""
    activity client_state noble_condition \
    unavailable_until:15 unavailable_why:30 #aid_type
    is_obsolete has_esf created modified
    remarks
    checkdata.ProblemsByOwner:30 contacts.RolesByPerson:20
    """, label=_("Miscellaneous"), required_roles=dd.login_required(SocialStaff))

    contracts = dd.Panel("""
    jobs.CandidaturesByPerson
    jobs.ContractsByClient
    art61.ContractsByClient
    """, label=dd.plugins.jobs.verbose_name)

    # sis_tab = dd.Panel("""
    # #isip.ContractsByClient
    # sis_motif sis_attentes
    # sis_moteurs sis_objectifs
    # """, label=_("SIS"))

    isip_tab = dd.Panel("""
    isip.ContractsByClient
    aids.GrantingsByClient
    """, label=dd.plugins.isip.short_name)

    courses_tab = dd.Panel("""
    courses.BasicEnrolmentsByPupil
    courses.JobEnrolmentsByPupil
    # oi_demarches
    """, label=dd.plugins.courses.short_name)
    # help_text=dd.plugins.courses.verbose_name)

    career = dd.Panel("""
    cv.StudiesByPerson
    cv.TrainingsByPerson
    cv.ExperiencesByPerson
    """, label=_("Career"))

    competences = dd.Panel("""
    cv.SkillsByPerson badges.AwardsByHolder cv.SoftSkillsByPerson
    cv.LanguageKnowledgesByPerson skills
    """, label=_("Competences"), required_roles=dd.login_required(
        CareerUser))

    obstacles_tab = dd.Panel("""
    cv.ObstaclesByPerson pcsw.ConvictionsByClient
    obstacles
    """, label=_("Obstacles"), required_roles=dd.login_required(
        CareerUser))



Clients.detail_layout = ClientDetail()

households = dd.resolve_app('households')
households.SiblingsByPerson.display_mode = 'grid'

# humanlinks = dd.resolve_app('humanlinks')
# humanlinks.LinksByHuman.display_mode = 'grid'

# cv = dd.resolve_app('cv')
# cv.ExperiencesByPerson.column_names = "company start_date end_date \
# function regime status is_training country remarks *"

# cv.StudiesByPerson.column_names = "type content start_date end_date \
# school country success language remarks *"

# ContactsByClient.column_names = 'company contact_person remark'
# dd.update_field(ClientContact, 'remark', verbose_name=_("Contact details"))


aids = dd.resolve_app('aids')
aids.GrantingsByClient.column_names = "detail_pointer request_date "\
                                      "aid_type category start_date"

notes = dd.resolve_app('notes')
notes.Note.hidden_elements = dd.fields_list(
    notes.Note, 'company contact_person contact_role')


# @dd.receiver(dd.on_ui_updated, sender=notes.Note)
# def myhandler(sender=None, watcher=None, request=None, **kwargs):
#     obj = watcher.watched
#     if obj.project is None:
#         return
#     recipients = []
#     period = (dd.today(), dd.today())
#     for c in obj.project.get_coachings(period, user__email__gt=''):
#         if c.user != request.user:
#             recipients.append(c.user.email)
#     if len(recipients) == 0:
#         return
#     context = dict(obj=obj, request=request)
#     subject = "Modification dans {obj}".format(**context)
#     tpl = rt.get_template('notes/note_updated.eml')
#     body = tpl.render(**context)
#     sender = request.user.email or settings.SERVER_EMAIL
#     # dd.logger.info("20150505 %s", recipients)
#     rt.send_email(subject, sender, body, recipients)


uploads = dd.resolve_app('uploads')
uploads.UploadsByClient.display_mode = 'grid'

