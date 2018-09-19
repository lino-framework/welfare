.. doctest docs/specs/clients_chatelet.rst
.. _welfare.specs.clients.chatelet:

==================
Clients (Chatelet)
==================

.. doctest init:

    >>> import lino
    >>> lino.startup('lino_welfare.projects.chatelet.settings.doctests')
    >>> from lino.api.doctest import *

.. contents::
   :depth: 2
   :local:



The detail layout of a client
=============================

Here is a textual description of the fields and their layout used in
the :class:`ClientDetail
<lino_welfare.projects.eupen.modlib.pcsw.models.ClientDetail>` of a
Lino Welfare à la Chatelet.

>>> from lino.utils.diag import py2rst
>>> print(py2rst(pcsw.Clients.detail_layout, True))
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF -SKIP
(main) [visible for all]:
- **Personne** (general):
  - (general_1):
    - **None** (overview)
    - (general2):
      - (general2_1): **Sexe** (gender), **ID** (id), **Nationalité** (nationality)
      - **Nom de famille** (last_name)
      - (general2_3): **Prénom** (first_name), **Deuxième prénom** (middle_name)
      - (general2_4): **Date de naissance** (birth_date), **Âge** (age), **Langue** (language)
    - (general3): **adresse e-mail** (email), **Téléphone** (phone), **Fax** (fax), **GSM** (gsm)
    - **None** (image)
  - (general_2): **NISS** (national_id), **Etat civil** (civil_state), **Pays de naissance** (birth_country), **Lieu de naissance** (birth_place), **Nom déclaré** (declared_name), **besoin permis de séjour** (needs_residence_permit), **besoin permis de travail** (needs_work_permit)
  - (general_3): **en Belgique depuis** (in_belgium_since), **Titre de séjour** (residence_type), **Inscription jusque** (residence_until), **Phase d'insertion** (group), **Type d'aide sociale** (aid_type)
  - (general_4) [visible for 100 110 120 200 210 220 300 400 410 420 500 510 800 admin 910]:
    - **Rendez-vous** (reception.AppointmentsByPartner)
    - **Créer rendez-vous avec** (AgentsByClient)
    - **Inscriptions** (courses.EnrolmentsByPupil) [visible for 100 110 120 200 210 300 400 410 420 800 admin 910]
- **Intervenants** (coaching) [visible for 100 110 120 200 210 220 300 400 410 420 500 510 800 admin 910]:
  - (coaching_1) [visible for 110 120 200 220 300 420 800 admin 910]:
    - (newcomers_left):
      - (newcomers_left_1) [visible for all]: **Workflow** (workflow_buttons), **Document identifiant** (id_document)
      - **Spécificité** (faculty) [visible for all]
      - **Contacts** (clients.ContactsByClient) [visible for 100 110 120 200 210 220 300 400 410 420 500 510 800 admin 910]
    - **Agents disponibles** (newcomers.AvailableCoachesByClient)
  - **Interventions** (coachings.CoachingsByClient)
- **Situation familiale** (family) [visible for 100 110 120 200 210 300 400 410 420 500 510 800 admin 910]:
  - (family_1) [visible for all]:
    - (family_left): **Appartenance aux ménages** (households_MembersByPerson) [visible for 100 110 120 200 210 300 400 410 420 500 510 800 admin 910], **Garde d'enfant** (child_custody)
    - **Composition de ménage** (households.SiblingsByPerson) [visible for 100 110 120 200 210 300 400 410 420 500 510 800 admin 910]
  - **Liens de parenté** (humanlinks_LinksByHuman)
- **Parcours** (career) [visible for 100 110 120 420 admin 910]:
  - **Études** (cv.StudiesByPerson)
  - **Formations** (cv.TrainingsByPerson)
  - **Expériences professionnelles** (cv.ExperiencesByPerson)
- **Compétences** (competences) [visible for 100 110 120 420 admin 910]:
  - (competences_1) [visible for 100 110 120 200 210 220 300 400 410 420 500 510 800 admin 910]:
    - **Compétences professionnelles** (cv.SkillsByPerson) [visible for 100 110 120 420 admin 910]
    - **Tests de niveau** (badges.AwardsByHolder)
    - **Compétences sociales** (cv.SoftSkillsByPerson) [visible for 100 110 120 420 admin 910]
  - (competences_2) [visible for all]: **Connaissances de langue** (cv_LanguageKnowledgesByPerson) [visible for 100 110 120 420 admin 910], **Autres atouts** (skills)
- **Freins** (obstacles_tab) [visible for 100 110 120 420 admin 910]:
  - (obstacles_tab_1) [visible for 100 110 120 200 300 400 410 420 admin 910]:
    - **Freins** (cv.ObstaclesByPerson) [visible for 100 110 120 420 admin 910]
    - **Antécédents judiciaires** (pcsw.ConvictionsByClient)
  - **Autres freins** (obstacles) [visible for all]
- **PIIS** (isip_tab) [visible for 100 110 120 200 210 300 400 410 420 500 510 800 admin 910]:
  - **PIISs** (isip.ContractsByClient) [visible for 100 110 120 210 420 admin 910]
  - **Octrois d'aide** (aids.GrantingsByClient)
- **O.I.** (courses_tab) [visible for 100 110 120 200 210 300 400 410 420 800 admin 910]:
  - **Ateliers d'insertion sociale** (courses.BasicEnrolmentsByPupil)
  - **Ateliers d'Insertion socioprofessionnelle** (courses.JobEnrolmentsByPupil)
- **Stages d'immersion** (immersion.ContractsByClient) [visible for 100 110 120 210 420 admin 910]
- **RAE** (job_search_1) [visible for 100 110 120 200 210 300 400 410 420 500 510 800 admin 910]:
  - (suche):
    - (suche_1) [visible for all]: **cherche du travail** (is_seeking), **Inoccupé depuis** (unemployed_since), **Cherche du travail depuis** (seeking_since), **Suspendu jusque** (work_permit_suspended_until)
    - **Dispenses** (pcsw.DispensesByClient) [visible for 100 110 120 200 300 400 410 420 admin 910]
    - **Exclusions** (pcsw.ExclusionsByClient) [visible for 100 110 120 200 300 400 410 420 admin 910]
  - (papers) [visible for 100 110 120 200 300 400 410 420 admin 910]:
    - **Preuves de recherche** (active_job_search.ProofsByClient) [visible for 100 110 120 420 admin 910]
    - **Interviews** (polls_ResponsesByPartner)
- **Mise à l'emploi** (contracts) [visible for 100 110 120 200 210 300 400 410 420 admin 910]:
  - **Candidatures** (jobs.CandidaturesByPerson)
  - **Mises à l'emploi art60§7** (jobs.ContractsByClient)
  - **Mises à l'emploi art.61 et activations** (art61.ContractsByClient) [visible for 100 110 120 210 420 admin 910]
- **Historique** (history) [visible for 100 110 120 200 210 300 400 410 420 500 510 800 admin 910]:
  - **Observations** (notes.NotesByProject)
  - (history_right):
    - **Fichiers téléchargés** (uploads.UploadsByClient)
    - **Existing excerpts** (excerpts_ExcerptsByProject)
    - **Fiches FSE** (esf.SummariesByClient) [visible for 100 110 120 420 admin 910]
- **Calendrier** (calendar) [visible for 100 110 120 200 210 220 300 400 410 420 500 510 800 admin 910]:
  - **Entrées calendrier** (cal.EntriesByClient)
  - **Tâches** (cal.TasksByProject)
- **Divers** (misc) [visible for 110 120 410 420 admin 910]:
  - (misc_1) [visible for all]: **Activité** (activity), **État** (client_state), **Titre de noblesse** (noble_condition), **Indisponible jusque** (unavailable_until), **raison** (unavailable_why)
  - (misc_2) [visible for all]: **obsolete** (is_obsolete), **ESF data** (has_esf), **Créé** (created), **Modifié** (modified)
  - **Remarques** (remarks) [visible for all]
  - (misc_4) [visible for 100 110 120 200 210 220 300 400 410 420 500 510 800 admin 910]:
    - **Problèmes de données** (checkdata_ProblemsByOwner)
    - **contact pour** (contacts.RolesByPerson)
- **Médiation de dettes** (debts) [visible for 120 300 420 admin 910]:
  - **Is partner of these budgets:** (debts.BudgetsByPartner)
  - **Is actor in these budgets:** (debts.ActorsByPartner)
<BLANKLINE>


Some panels are not visible to everybody. Their visibility is marked
between brackets (e.g. `[visible for all except anonymous, 210]`).

The window itself is visible to everybody:

>>> ui = dd.plugins.extjs
>>> lh = rt.models.pcsw.Clients.detail_layout.get_layout_handle(ui)
>>> lh.main
<TabPanel main in lino_welfare.projects.chatelet.modlib.pcsw.models.ClientDetail on lino_welfare.modlib.pcsw.models.Clients>
>>> list(lh.main.required_roles)
[]

The "General" tab is visible to everybody:

>>> list(lh['general'].required_roles)
[]

But e.g. the "Miscellaneous" tab is visible only to users having
the :class:`SocialStaff
<lino_welfare.modlib.pcsw.roles.SocialStaff>` role:

>>> misc = lh['misc']
>>> misc
<Panel misc in lino_welfare.projects.chatelet.modlib.pcsw.models.ClientDetail on lino_welfare.modlib.pcsw.models.Clients>

>>> list(misc.required_roles)
[<class 'lino_welfare.modlib.pcsw.roles.SocialStaff'>]



