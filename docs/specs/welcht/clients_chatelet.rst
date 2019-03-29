.. doctest docs/specs/welcht/clients_chatelet.rst
.. _welfare.specs.clients.chatelet:

==================
Clients (Chatelet)
==================

.. contents::
   :local:

.. include:: /shared/include/tested.rst

>>> import lino
>>> lino.startup('lino_welfare.projects.mathieu.settings.doctests')
>>> from lino.api.doctest import *


The detail layout of a client
=============================

Here is a textual description of the fields and their layout used in
the :class:`ClientDetail
<lino_welfare.eupen.lib.pcsw.models.ClientDetail>` of a
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
    - **Inscriptions dans Ateliers** (courses.EnrolmentsByPupil) [visible for 100 110 120 200 210 300 400 410 420 800 admin 910]
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
  - **Tests de niveau** (badges.AwardsByHolder) [visible for 100 110 120 200 210 220 300 400 410 420 500 510 800 admin 910]
  - **Autres atouts** (skills) [visible for all]
- **Freins** (obstacles_tab) [visible for 100 110 120 420 admin 910]:
  - **Freins** (cv.ObstaclesByPerson)
  - **Autres freins** (obstacles) [visible for all]
- **PIISs** (isip.ContractsByClient) [visible for 100 110 120 210 400 410 420 admin 910]
- **O.I.** (courses_tab) [visible for 100 110 120 200 210 300 400 410 420 800 admin 910]:
  - **Inscriptions dans Ateliers d'insertion sociale** (courses.BasicEnrolmentsByPupil)
  - **Inscriptions dans Ateliers d'Insertion socioprofessionnelle** (courses.JobEnrolmentsByPupil)
- **Stages d'immersion** (immersion.ContractsByClient) [visible for 100 110 120 210 400 410 420 admin 910]
- **Mise à l'emploi** (contracts) [visible for 100 110 120 200 210 300 400 410 420 admin 910]:
  - **Candidatures** (jobs.CandidaturesByPerson)
  - **Mises à l'emploi art60§7** (jobs.ContractsByClient)
  - **Mises à l'emploi art.61 et activations** (art61.ContractsByClient) [visible for 100 110 120 210 400 410 420 admin 910]
- **Historique** (history):
  - **Observations** (notes.NotesByProject) [visible for 100 110 120 200 210 300 400 410 420 500 510 800 admin 910]
  - (history_right):
    - **Fichiers téléchargés** (uploads.UploadsByClient) [visible for 100 110 120 200 210 300 400 410 420 500 510 800 admin 910]
    - (history_right_2): **cherche du travail** (is_seeking), **Inoccupé depuis** (unemployed_since), **Cherche du travail depuis** (seeking_since)
    - **Situation chômage** (pcsw.ExclusionsByClient) [visible for 100 110 120 200 300 400 410 420 admin 910]
    - **Fiches FSE** (esf.SummariesByClient) [visible for 100 110 120 420 admin 910]
- **Calendrier** (calendar) [visible for 100 110 120 200 210 220 300 400 410 420 500 510 800 admin 910]:
  - **Entrées calendrier** (cal.EntriesByClient)
  - **Tâches** (cal.TasksByProject)
- **Divers** (misc) [visible for 110 120 410 420 admin 910]:
  - (misc_1) [visible for all]: **Activité** (activity), **État** (client_state), **Titre de noblesse** (noble_condition), **Indisponible jusque** (unavailable_until), **Raison** (unavailable_why)
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
<TabPanel main in lino_welcht.lib.pcsw.models.ClientDetail on lino_welfare.modlib.pcsw.models.Clients>
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
<Panel misc in lino_welcht.lib.pcsw.models.ClientDetail on lino_welfare.modlib.pcsw.models.Clients>

>>> list(misc.required_roles)
[<class 'lino_welfare.modlib.pcsw.roles.SocialStaff'>]



Filtering clients about their career
====================================

Show all clients who were learning between 2011-03-11 and 2012-03-11
(at least):

>>> ses = rt.login('robin')
>>> translation.activate('en')

>>> pv = dict(start_date=i2d(20110311), end_date=i2d(20120311), observed_event=pcsw.ClientEvents.learning)
>>> pv.update(client_state=None)
>>> ses.show(pcsw.CoachedClients, column_names="name_column", param_values=pv)
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE -REPORT_UDIFF
==========================
 Name
--------------------------
 EVERS Eberhart (127)
 KELLER Karl (178)
 MALMENDIER Marc (146)
 MEESSEN Melissa (147)
 RADERMACHER Alfons (153)
 DA VINCI David (165)
 VAN VEEN Vincent (166)
==========================
<BLANKLINE>

Just as a random sample, let's verify one of these clients.  Vincent
van Veen does have a training, but that started only two days later:

>>> obj = pcsw.Client.objects.get(pk=166)
>>> ses.show(cv.TrainingsByPerson, obj, column_names="type start_date end_date")
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE -REPORT_UDIFF
================ ============ ============
 Education Type   Start date   End date
---------------- ------------ ------------
 Alpha            13/03/2011   13/03/2012
================ ============ ============
<BLANKLINE>

And he has no studies:

>>> ses.show(cv.StudiesByPerson, obj, column_names="type start_date end_date")
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE -REPORT_UDIFF
<BLANKLINE>
No data to display
<BLANKLINE>

... but here is a work experience which matches exactly our query:

>>> ses.show(cv.ExperiencesByPerson, obj, column_names="start_date end_date")
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE -REPORT_UDIFF
============ ============
 Start date   End date
------------ ------------
 11/03/2011   11/03/2012
============ ============
<BLANKLINE>
