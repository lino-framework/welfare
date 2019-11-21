.. doctest docs/specs/welcht/chatelet.rst
.. _welfare.specs.chatelet:


===================================
The Lino Welfare "Châtelet" variant
===================================


.. contents::
   :local:
   :depth: 2


.. include:: /../docs/shared/include/tested.rst

>>> from lino import startup
>>> startup('lino_welfare.projects.mathieu.settings.doctests')
>>> from lino.api.doctest import *


Overview
========

The *Châtelet* variant of Lino Welfare went online in 2013.

From the beginning on it was clear that some functionalities differ.

For example it uses **internal courses** (:mod:`lino_welcht.lib.courses`, a
sub-plugin of :mod:`lino_xl.lib.courses`) instead of **external courses**
(:mod:`lino_welfare.modlib.xcourses`). And the "Courses" are labelled
"Workshops" ("Ateliers").  It does not use certain plugins (e.g. cbss, aids),
adds some plugins (eg art61, immersion, esf), uses some plugins differently...

In February 2019 the code was moved to its own repository :mod:`lino_welcht`.



Hidden site languages
=====================

The default language distribution (:attr:`languages
<lino.core.site.Site.languages>`) is French, Dutch, German and
English, but Dutch is currently hidden because we don't yet have any
Flemish speaking users (:attr:`hidden_languages
<lino.core.site.Site.hidden_languages>`):

>>> print(' '.join([lng.name for lng in settings.SITE.languages]))
fr nl de en
>>> settings.SITE.hidden_languages
'nl'



The main menu
=============

Romain
------

>>> rt.login('romain').show_menu() #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
- Contacts : Personnes,  ▶ Bénéficiaires, Organisations, -, Partenaires (tous), Ménages
- Bureau : Mes Notifications, Mes Extraits, Mes téléchargements à renouveler, Mes Fichiers téléchargés, Mon courrier sortant, Mes Observations, Mes problèmes de données
- Calendrier : Calendrier, Mes rendez-vous, Rendez-vous dépassés, Mes rendez-vous à confirmer, Mes tâches, Mes visiteurs, Mes présences, Mes rendez-vous dépassés, Calendrier
- Réception : Bénéficiaires, Rendez-vous aujourd'hui, Salle d'attente, Visiteurs occupés, Visiteurs repartis, Visiteurs qui m'attendent
- CPAS : Bénéficiaires, Mes Interventions, Octrois à confirmer
- Intégration :
  - Bénéficiaires
  - PIISs
  - Mises à l'emploi art60§7
  - Services utilisateurs
  - Postes de travail
  - Offres d'emploi
  - Mises à l'emploi art61
  - Stages d'immersion
  - BCSS : Mes Requêtes IdentifyPerson, Mes Requêtes ManageAccess, Mes Requêtes Tx25
- Ateliers : Mes Ateliers, Ateliers d'insertion sociale, Ateliers d'Insertion socioprofessionnelle, -, Séries d'ateliers, Demandes d’inscription en attente, Demandes d’inscription confirmées
- Nouvelles demandes : Nouveaux bénéficiaires, Agents disponibles
- Médiation de dettes : Bénéficiaires, Mes Budgets
- Questionnaires : Mes Questionnaires, Mes Interviews
- Rapports :
  - Intégration : Agents et leurs clients, Situation contrats Art 60-7, Rapport d'activité
- Configuration :
  - Système : Paramètres du Site, Utilisateurs, Textes d'aide
  - Endroits : Pays, Endroits
  - Contacts : Types d'organisation, Fonctions, Conseils, Types de ménage
  - Bureau : Types d'extrait, Libraries de fichiers, Types de fichiers téléchargés, Types d'observation, Types d'événements, Mes Text Field Templates
  - Calendrier : Calendriers, Locaux, Évènements periodiques, Rôles de participants, Types d'entrée calendrier, Règles de récurrence, Calendriers externes, Lignes de planificateur
  - Ateliers : Savoirs de base, Topics, Timetable Slots
  - CPAS : Droits chômage, Types d'aide sociale, Catégories , Types de contact client, Services, Raisons d’arrêt d'intervention
  - Parcours : Types d'éducation, Niveaux académiques, Secteurs, Fonctions, Régimes de travail, Statuts, Types de contrat, Types de compétence sociale, Types de freins, Preuves de qualification, Langues
  - Intégration : Types de PIIS, Motifs d’arrêt de contrat, Régimes d'évaluation, Types de mise à l'emploi art60§7, Types de poste, Horaires, Types de mise à l'emploi art.61, Types de stage d'immersion, Objectifs
  - Nouvelles demandes : Intermédiaires, Spécificités
  - BCSS : Secteurs, Codes fonction
  - Médiation de dettes : Groupes de comptes, Comptes, Budget modèle
  - Questionnaires : Listes de choix
- Explorateur :
  - Contacts : Personnes de contact, Partenaires, Types d'adresses, Adresses, Membres du conseil, Rôles de membres de ménage, Membres de ménage, Liens de parenté, Types de parenté
  - Système : Procurations, Types d'utilisateur, Rôles d'utilisateur, Notifications, Changes, All dashboard widgets, Types de contenu, Tests de données, Problèmes de données
  - Bureau : Extraits, Fichiers téléchargés, Upload Areas, Mails envoyés, Pièces jointes, Observations, Text Field Templates
  - Calendrier : Entrées calendrier, Tâches, Présences, Abonnements, Entry states, Presence states, Task states
  - Ateliers : Tests de niveau, Ateliers, Inscriptions, États Inscription, Course layouts, États Atelier
  - CPAS : Exclusions du chômage, Antécédents judiciaires, Bénéficiaires, Etats civils, Etats bénéficiaires, Types de carte eID, Octrois d'aide, Certificats de revenu, Refund confirmations, Confirmations simple, Contacts client, Types de contact connus, Interventions
  - Parcours : Connaissances de langue, Formations, Études, Expériences professionnelles, Connaissances de langue, Compétences professionnelles, Compétences sociales, Freins
  - Intégration : PIISs, Mises à l'emploi art60§7, Candidatures, Services utilisateurs, Mises à l'emploi art61, Stages d'immersion, Preuves de recherche, Fiches FSE, Champs FSE
  - Nouvelles demandes : Compétences
  - BCSS : Requêtes IdentifyPerson, Requêtes ManageAccess, Requêtes Tx25
  - Médiation de dettes : Budgets, Entrées
  - Questionnaires : Questionnaires, Questions, Choix, Interviews, Choix de réponse, Answer Remarks
- Site : à propos

Theresia
--------

Theresia est un agent d'accueil. Elle ne voit pas les questionnaires,
les données de parcours, compétences professionnelles, compétences
sociales, freins. Elle peut faire des requètes CBSS. Elle peut
modifier les intervention d'autres utilisateurs.

>>> rt.login('theresia').user.user_type
users.UserTypes:210

>>> rt.login('theresia').show_menu() #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
- Contacts : Personnes,  ▶ Bénéficiaires, Organisations, -, Partenaires (tous), Ménages
- Bureau : Mes Extraits, Mes téléchargements à renouveler, Mes Fichiers téléchargés, Mes Observations
- Réception : Bénéficiaires, Rendez-vous aujourd'hui, Salle d'attente, Visiteurs occupés, Visiteurs repartis
- CPAS : Mes Interventions
- Intégration :
  - BCSS : Mes Requêtes IdentifyPerson, Mes Requêtes ManageAccess, Mes Requêtes Tx25
- Ateliers : Mes Ateliers, Ateliers d'insertion sociale, Ateliers d'Insertion socioprofessionnelle, -, Séries d'ateliers
- Configuration :
  - Endroits : Pays, Endroits
  - Contacts : Types d'organisation, Fonctions, Types de ménage
  - CPAS : Types d'aide sociale, Catégories , Types de contact client, Services, Raisons d’arrêt d'intervention
- Explorateur :
  - Contacts : Personnes de contact, Partenaires, Rôles de membres de ménage, Membres de ménage, Liens de parenté, Types de parenté
  - CPAS : Etats bénéficiaires, Octrois d'aide, Certificats de revenu, Refund confirmations, Confirmations simple, Contacts client, Types de contact connus, Interventions
- Site : à propos



Database structure
==================

This is the list of models used in the Châtelet variant of Lino Welfare:

>>> from lino.utils.diag import analyzer
>>> print(analyzer.show_db_overview()) #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF -SKIP
61 apps: lino, staticfiles, about, jinja, bootstrap3, extjs, printing, system, office, xl, countries, contacts, appypod, humanize, users, contenttypes, gfks, memo, notify, changes, checkdata, addresses, excerpts, uploads, outbox, extensible, cal, reception, badges, boards, clients, coachings, pcsw, welfare, sales, languages, cv, integ, isip, jobs, art61, immersion, active_job_search, courses, newcomers, cbss, households, humanlinks, debts, notes, aids, polls, summaries, weasyprint, esf, beid, dashboard, export_excel, tinymce, lino_welcht, sessions.
135 models:
============================== =============================== ========= =======
 Name                           Default table                   #fields   #rows
------------------------------ ------------------------------- --------- -------
 active_job_search.Proof        active_job_search.Proofs        7         10
 addresses.Address              addresses.Addresses             16        92
 aids.AidType                   aids.AidTypes                   23        11
 aids.Category                  aids.Categories                 5         3
 aids.Granting                  aids.Grantings                  12        55
 aids.IncomeConfirmation        aids.IncomeConfirmations        17        54
 aids.RefundConfirmation        aids.RefundConfirmations        18        12
 aids.SimpleConfirmation        aids.SimpleConfirmations        15        19
 art61.Contract                 art61.Contracts                 32        7
 art61.ContractType             art61.ContractTypes             10        1
 badges.Award                   badges.Awards                   6         0
 badges.Badge                   badges.Badges                   5         0
 boards.Board                   boards.Boards                   7         3
 boards.Member                  boards.Members                  4         0
 cal.Calendar                   cal.Calendars                   7         ...
 cal.DailyPlannerRow            cal.DailyPlannerRows            8         3
 cal.Event                      cal.OneEvent                    24        548
 cal.EventPolicy                cal.EventPolicies               21        6
 cal.EventType                  cal.EventTypes                  27        13
 cal.Guest                      cal.Guests                      9         588
 cal.GuestRole                  cal.GuestRoles                  6         4
 cal.RecurrentEvent             cal.RecurrentEvents             23        15
 cal.RemoteCalendar             cal.RemoteCalendars             7         0
 cal.Room                       cal.Rooms                       10        0
 cal.Subscription               cal.Subscriptions               4         9
 cal.Task                       cal.Tasks                       20        34
 cbss.IdentifyPersonRequest     cbss.IdentifyPersonRequests     21        5
 cbss.ManageAccessRequest       cbss.ManageAccessRequests       24        1
 cbss.Purpose                   cbss.Purposes                   7         106
 cbss.RetrieveTIGroupsRequest   cbss.RetrieveTIGroupsRequests   15        6
 cbss.Sector                    cbss.Sectors                    11        209
 changes.Change                 changes.Changes                 10        0
 checkdata.Problem              checkdata.Problems              6         0
 clients.ClientContact          clients.ClientContacts          7         14
 clients.ClientContactType      clients.ClientContactTypes      8         10
 coachings.Coaching             coachings.Coachings             8         90
 coachings.CoachingEnding       coachings.CoachingEndings       7         4
 coachings.CoachingType         coachings.CoachingTypes         8         3
 contacts.Company               contacts.Companies              28        39
 contacts.CompanyType           contacts.CompanyTypes           9         16
 contacts.Partner               contacts.Partners               25        162
 contacts.Person                contacts.Persons                32        109
 contacts.Role                  contacts.Roles                  4         10
 contacts.RoleType              contacts.RoleTypes              6         5
 contenttypes.ContentType       gfks.ContentTypes               3         135
 countries.Country              countries.Countries             9         270
 countries.Place                countries.Places                11        78
 courses.Course                 courses.Activities              31        7
 courses.Enrolment              courses.Enrolments              15        100
 courses.Line                   courses.Lines                   24        7
 courses.Slot                   courses.Slots                   5         0
 courses.Topic                  courses.Topics                  5         0
 cv.Duration                    cv.Durations                    5         5
 cv.EducationLevel              cv.EducationLevels              8         5
 cv.Experience                  cv.Experiences                  18        30
 cv.Function                    cv.Functions                    7         4
 cv.LanguageKnowledge           cv.LanguageKnowledges           10        114
 cv.Obstacle                    cv.Obstacles                    6         20
 cv.ObstacleType                cv.ObstacleTypes                5         4
 cv.Proof                       cv.Proofs                       5         4
 cv.Regime                      cv.Regimes                      5         3
 cv.Sector                      cv.Sectors                      6         14
 cv.Skill                       cv.Skills                       6         0
 cv.SoftSkill                   cv.SoftSkills                   5         0
 cv.SoftSkillType               cv.SoftSkillTypes               5         0
 cv.Status                      cv.Statuses                     5         7
 cv.Study                       cv.Studies                      15        22
 cv.StudyType                   cv.StudyTypes                   8         11
 cv.Training                    cv.Trainings                    17        20
 dashboard.Widget               dashboard.Widgets               5         0
 debts.Account                  debts.Accounts                  13        51
 debts.Actor                    debts.Actors                    6         63
 debts.Budget                   debts.Budgets                   11        14
 debts.Entry                    debts.Entries                   16        716
 debts.Group                    debts.Groups                    8         8
 esf.ClientSummary              esf.Summaries                   23        189
 excerpts.Excerpt               excerpts.Excerpts               12        71
 excerpts.ExcerptType           excerpts.ExcerptTypes           18        19
 gfks.HelpText                  gfks.HelpTexts                  4         5
 households.Household           households.Households           27        14
 households.Member              households.Members              14        63
 households.Type                households.Types                5         6
 humanlinks.Link                humanlinks.Links                4         59
 immersion.Contract             immersion.Contracts             25        6
 immersion.ContractType         immersion.ContractTypes         9         3
 immersion.Goal                 immersion.Goals                 5         4
 isip.Contract                  isip.Contracts                  24        30
 isip.ContractEnding            isip.ContractEndings            6         4
 isip.ContractPartner           isip.ContractPartners           6         35
 isip.ContractType              isip.ContractTypes              11        5
 isip.ExamPolicy                isip.ExamPolicies               21        6
 jobs.Candidature               jobs.Candidatures               10        74
 jobs.Contract                  jobs.Contracts                  28        13
 jobs.ContractType              jobs.ContractTypes              10        5
 jobs.Job                       jobs.Jobs                       10        8
 jobs.JobProvider               jobs.JobProviders               29        3
 jobs.JobType                   jobs.JobTypes                   5         5
 jobs.Offer                     jobs.Offers                     9         1
 jobs.Schedule                  jobs.Schedules                  5         3
 languages.Language             languages.Languages             6         5
 newcomers.Broker               newcomers.Brokers               2         2
 newcomers.Competence           newcomers.Competences           5         7
 newcomers.Faculty              newcomers.Faculties             6         5
 notes.EventType                notes.EventTypes                10        10
 notes.Note                     notes.Notes                     18        111
 notes.NoteType                 notes.NoteTypes                 12        13
 notify.Message                 notify.Messages                 11        12
 outbox.Attachment              outbox.Attachments              4         0
 outbox.Mail                    outbox.Mails                    9         0
 outbox.Recipient               outbox.Recipients               6         0
 pcsw.Activity                  pcsw.Activities                 3         0
 pcsw.AidType                   pcsw.AidTypes                   5         0
 pcsw.Client                    pcsw.Clients                    68        63
 pcsw.Conviction                pcsw.Convictions                5         0
 pcsw.Dispense                  pcsw.Dispenses                  6         0
 pcsw.DispenseReason            pcsw.DispenseReasons            6         4
 pcsw.Exclusion                 pcsw.Exclusions                 9         0
 pcsw.ExclusionType             pcsw.ExclusionTypes             2         2
 pcsw.PersonGroup               pcsw.PersonGroups               4         5
 pcsw.UnemploymentRight         pcsw.UnemploymentRights         4         0
 polls.AnswerChoice             polls.AnswerChoices             4         88
 polls.AnswerRemark             polls.AnswerRemarks             4         0
 polls.Choice                   polls.Choices                   7         39
 polls.ChoiceSet                polls.ChoiceSets                5         9
 polls.Poll                     polls.Polls                     11        2
 polls.Question                 polls.Questions                 9         38
 polls.Response                 polls.Responses                 7         6
 sessions.Session               sessions.SessionTable           3         ...
 system.SiteConfig              system.SiteConfigs              29        1
 tinymce.TextFieldTemplate      tinymce.TextFieldTemplates      5         2
 uploads.Upload                 uploads.Uploads                 19        11
 uploads.UploadType             uploads.UploadTypes             11        9
 uploads.Volume                 uploads.Volumes                 5         0
 users.Authority                users.Authorities               3         3
 users.User                     users.AllUsers                  26        12
============================== =============================== ========= =======
<BLANKLINE>


user types
=============

We use the user types described in :ref:`welfare.usertypes`. Here are their
French labels.

>>> settings.SITE.user_types_module
'lino_welfare.modlib.welfare.user_types'
>>> rt.show(users.UserTypes)
======= =========== =====================================
 value   name        text
------- ----------- -------------------------------------
 000     anonymous   Anonyme
 100                 Agent d'insertion
 110                 Agent d'insertion (chef de service)
 120                 Integration agent (Flexible)
 200                 Consultant nouveaux bénéficiaires
 210                 Agent d'accueil
 220                 Reception clerk (Flexible)
 300                 Médiateur de dettes
 400                 Agent social
 410                 Agent social (Chef de service)
 420                 Social agent (Flexible)
 500                 Comptable
 510                 Accountant (Manager)
 800                 Supervisor
 900     admin       Administrateur
 910                 Security advisor
======= =========== =====================================
<BLANKLINE>


List of window layouts
======================

The following table lists information about all *data entry form
definitions* (called **window layouts**) used by Lino Welfare.  There
are *detail* layouts, *insert* layouts and *action parameter* layouts.

..
   >>> #settings.SITE.catch_layout_exceptions = False

Each window layout defines a given set of fields.


>>> print(analyzer.show_window_fields()) #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
- about.About.show :
- active_job_search.Proofs.detail : date, client, company, id, spontaneous, response, remarks
- addresses.Addresses.detail : country, city, zip_code, addr1, street, street_no, street_box, addr2, address_type, remark, data_source, partner
- addresses.Addresses.insert : country, city, street, street_no, street_box, address_type, remark
- aids.AidTypes.detail : id, short_name, confirmation_type, name, name_nl, name_de, name_en, excerpt_title, excerpt_title_nl, excerpt_title_de, excerpt_title_en, body_template, print_directly, is_integ_duty, is_urgent, confirmed_by_primary_coach, board, company, contact_person, contact_role, pharmacy_type
- aids.AidTypes.insert : name, name_nl, name_de, name_en, confirmation_type
- aids.Categories.detail : id, name, name_nl, name_de, name_en
- aids.Grantings.detail : id, client, user, signer, workflow_buttons, request_date, board, decision_date, aid_type, category, start_date, end_date, custom_actions
- aids.Grantings.insert : client, aid_type, signer, board, decision_date, start_date, end_date
- aids.GrantingsByClient.insert : aid_type, board, decision_date, start_date, end_date
- aids.IncomeConfirmations.detail : client, user, signer, workflow_buttons, printed, company, contact_person, language, granting, start_date, end_date, category, amount, id, remark
- aids.IncomeConfirmationsByGranting.insert : client, granting, start_date, end_date, category, amount, company, contact_person, language, remark
- aids.RefundConfirmations.detail : id, client, user, signer, workflow_buttons, granting, start_date, end_date, doctor_type, doctor, pharmacy, company, contact_person, language, printed, remark
- aids.RefundConfirmationsByGranting.insert : start_date, end_date, doctor_type, doctor, pharmacy, company, contact_person, language, printed, remark
- aids.SimpleConfirmations.detail : id, client, user, signer, workflow_buttons, granting, start_date, end_date, company, contact_person, language, printed, remark
- aids.SimpleConfirmationsByGranting.insert : start_date, end_date, company, contact_person, language, remark
- art61.ContractTypes.detail : id, name, name_nl, name_de, name_en, ref, overlap_group
- art61.ContractTypes.merge_row : merge_to, reason
- art61.Contracts.detail : id, client, user, language, type, company, contact_person, contact_role, applies_from, duration, applies_until, exam_policy, job_title, status, cv_duration, regime, reference_person, remark, printed, date_decided, date_issued, date_ended, ending, subsidize_10, subsidize_20, subsidize_30, subsidize_40, subsidize_50, responsibilities
- art61.Contracts.insert : client, company, type
- boards.Boards.detail : id, name, name_nl, name_de, name_en
- boards.Boards.insert : name, name_nl, name_de, name_en
- cal.Calendars.detail : name, name_nl, name_de, name_en, color, id, description
- cal.Calendars.insert : name, name_nl, name_de, name_en, color
- cal.DailyView.detail : navigation_panel
- cal.EntriesByClient.insert : event_type, summary, start_date, start_time, end_date, end_time
- cal.EntriesByGuest.insert : start_date, start_time, end_time, summary, event_type
- cal.EntriesByProject.insert : start_date, start_time, end_time, summary, event_type
- cal.EventTypes.detail : name, name_nl, name_de, name_en, event_label, event_label_nl, event_label_de, event_label_en, planner_column, max_conflicting, max_days, esf_field, email_template, id, all_rooms, locks_user, invite_client, is_appointment, attach_to_email
- cal.EventTypes.insert : name, name_nl, name_de, name_en, invite_client
- cal.EventTypes.merge_row : merge_to, reason
- cal.Events.detail : event_type, summary, project, start_date, start_time, end_date, end_time, user, assigned_to, room, priority, access_class, transparent, owner, workflow_buttons, description, id, created, modified, state
- cal.Events.insert : summary, start_date, start_time, end_date, end_time, event_type, project
- cal.GuestRoles.detail : ref, name, name_nl, name_de, name_en, id
- cal.GuestRoles.merge_row : merge_to, reason
- cal.GuestStates.wf1 : notify_subject, notify_body, notify_silent
- cal.GuestStates.wf2 : notify_subject, notify_body, notify_silent
- cal.Guests.checkin : notify_subject, notify_body, notify_silent
- cal.Guests.detail : event, client, role, state, remark, workflow_buttons, waiting_since, busy_since, gone_since
- cal.Guests.insert : event, partner, role
- cal.MonthlyView.detail : navigation_panel
- cal.RecurrentEvents.detail : name, name_nl, name_de, name_en, id, user, event_type, start_date, start_time, end_date, end_time, every_unit, every, max_events, monday, tuesday, wednesday, thursday, friday, saturday, sunday, description
- cal.RecurrentEvents.insert : name, name_nl, name_de, name_en, start_date, end_date, every_unit, event_type
- cal.Rooms.detail : id, name, name_nl, name_de, name_en, company, contact_person, display_color, description
- cal.Rooms.insert : id, name, name_nl, name_de, name_en, display_color, company, contact_person
- cal.Tasks.detail : start_date, due_date, id, workflow_buttons, summary, project, user, delegated, owner, created, modified, description
- cal.Tasks.insert : summary, user, project
- cal.TasksByController.insert : summary, start_date, due_date, user, delegated
- cal.WeeklyView.detail : navigation_panel
- cbss.IdentifyPersonRequests.detail : id, person, user, sent, status, printed, national_id, first_name, middle_name, last_name, birth_date, tolerance, gender, environment, ticket, info_messages, debug_messages
- cbss.IdentifyPersonRequests.insert : person, national_id, first_name, middle_name, last_name, birth_date, tolerance, gender
- cbss.ManageAccessRequests.detail : id, person, user, sent, status, printed, action, start_date, end_date, purpose, query_register, national_id, sis_card_no, id_card_no, first_name, last_name, birth_date, result, environment, ticket, info_messages, debug_messages
- cbss.ManageAccessRequests.insert : person, action, start_date, end_date, purpose, query_register, national_id, sis_card_no, id_card_no, first_name, last_name, birth_date
- cbss.RetrieveTIGroupsRequests.detail : id, person, user, sent, status, printed, national_id, language, history, environment, ticket, info_messages, debug_messages
- cbss.RetrieveTIGroupsRequests.insert : person, national_id, language, history
- changes.Changes.detail : time, user, type, master, object, id, diff
- checkdata.Checkers.detail : value, text
- checkdata.Problems.detail : checker, owner, message, user, id
- clients.ClientContactTypes.detail : id, name, name_nl, name_de, name_en
- coachings.CoachingEndings.detail : id, name, name_nl, name_de, name_en, seqno
- coachings.Coachings.create_visit : user, summary
- contacts.Companies.detail : overview, prefix, name, type, vat_id, client_contact_type, url, email, phone, gsm, fax, remarks, notes_NotesByCompany, id, language, activity, is_obsolete, created, modified
- contacts.Companies.insert : name, email, type
- contacts.Companies.merge_row : merge_to, addresses_Address, reason
- contacts.Partners.merge_row : merge_to, addresses_Address, reason
- contacts.Persons.create_household : head, type, partner
- contacts.Persons.detail : overview, title, first_name, middle_name, last_name, gender, birth_date, age, id, language, email, phone, gsm, fax, households_MembersByPerson, humanlinks_LinksByHuman, remarks, activity, url, client_contact_type, is_obsolete, created, modified
- contacts.Persons.insert : first_name, last_name, gender, email
- contacts.Persons.merge_row : merge_to, cv_LanguageKnowledge, cv_Obstacle, cv_Skill, cv_SoftSkill, addresses_Address, reason
- countries.Countries.detail : isocode, name, name_nl, name_de, name_en, short_code, inscode, actual_country
- countries.Countries.insert : isocode, inscode, name, name_nl, name_de, name_en
- countries.Places.detail : name, name_nl, name_de, name_en, country, inscode, zip_code, parent, type, id
- courses.Activities.detail : line, teacher, start_date, start_time, end_time, end_date, room, workflow_buttons, id, user, name, description, description_nl, description_de, description_en, max_events, max_date, every_unit, every, monday, tuesday, wednesday, thursday, friday, saturday, sunday, enrolments_until, max_places, confirmed, free_places, print_actions, EnrolmentsByCourse
- courses.Activities.insert : line, teacher, name, start_date
- courses.Activities.print_presence_sheet : start_date, end_date, show_remarks, show_states
- courses.Activities.print_presence_sheet_html : start_date, end_date, show_remarks, show_states
- courses.Enrolments.detail : request_date, user, course, pupil, remark, workflow_buttons, printed, motivation, problems
- courses.Enrolments.insert : request_date, user, course, pupil, remark
- courses.EnrolmentsByCourse.insert : pupil, remark, request_date, user
- courses.EnrolmentsByPupil.insert : course_area, course, places, remark, request_date, user
- courses.Lines.detail : id, name, name_nl, name_de, name_en, ref, company, contact_person, course_area, topic, body_template, event_type, guest_role, every_unit, every, excerpt_title, excerpt_title_nl, excerpt_title_de, excerpt_title_en, description, description_nl, description_de, description_en
- courses.Lines.insert : name, name_nl, name_de, name_en, ref, topic, every_unit, every, event_type, description, description_nl, description_de, description_en
- courses.Lines.merge_row : merge_to, reason
- courses.Slots.detail : name, start_time, end_time
- courses.Slots.insert : start_time, end_time, name
- courses.Topics.detail : id, name, name_nl, name_de, name_en
- cv.Durations.detail : id, name, name_nl, name_de, name_en
- cv.EducationLevels.detail : name, name_nl, name_de, name_en, is_study, is_training
- cv.Experiences.detail : person, company, country, city, sector, function, title, status, duration, regime, is_training, start_date, end_date, duration_text, termination_reason, remarks
- cv.ExperiencesByPerson.insert : start_date, end_date, company, function
- cv.Functions.detail : id, name, name_nl, name_de, name_en, sector, remark
- cv.LanguageKnowledgesByPerson.detail : language, native, has_certificate, cef_level, spoken_passively, spoken, written
- cv.LanguageKnowledgesByPerson.insert : language, native, has_certificate, cef_level, spoken_passively, spoken, written
- cv.Regimes.detail : id, name, name_nl, name_de, name_en
- cv.Sectors.detail : id, name, name_nl, name_de, name_en, remark
- cv.Statuses.detail : id, name, name_nl, name_de, name_en
- cv.Studies.detail : person, start_date, end_date, duration_text, type, content, education_level, state, school, country, city, remarks
- cv.StudiesByPerson.insert : start_date, end_date, type, content
- cv.StudyTypes.detail : name, name_nl, name_de, name_en, id, education_level, is_study, is_training
- cv.StudyTypes.insert : name, name_nl, name_de, name_en, is_study, is_training, education_level
- cv.Trainings.detail : person, start_date, end_date, duration_text, type, state, certificates, sector, function, school, country, city, remarks
- cv.Trainings.insert : person, start_date, end_date, type, state, certificates, sector, function, school, country, city
- debts.Accounts.detail : ref, name, name_nl, name_de, name_en, group, type, required_for_household, required_for_person, periods, default_amount
- debts.Accounts.insert : ref, group, type, name, name_nl, name_de, name_en
- debts.Accounts.merge_row : merge_to, reason
- debts.Budgets.detail : date, partner, id, user, intro, ResultByBudget, DebtsByBudget, AssetsByBudgetSummary, conclusion, dist_amount, printed, total_debt, include_yearly_incomes, print_empty_rows, print_todos, DistByBudget, data_box, summary_box
- debts.Budgets.insert : partner, date, user
- debts.Groups.detail : ref, name, name_nl, name_de, name_en, id, account_type, entries_layout
- debts.Groups.insert : name, name_nl, name_de, name_en, account_type, ref
- esf.Summaries.detail : master, year, month, children_at_charge, certified_handicap, other_difficulty, id, education_level, result, remark, results
- excerpts.ExcerptTypes.detail : id, name, name_nl, name_de, name_en, content_type, build_method, template, body_template, email_template, shortcut, primary, print_directly, certifying, print_recipient, backward_compat, attach_to_email
- excerpts.ExcerptTypes.insert : name, name_nl, name_de, name_en, content_type, primary, certifying, build_method, template, body_template
- excerpts.Excerpts.detail : id, excerpt_type, project, user, build_method, company, contact_person, language, owner, build_time, body_template_content
- gfks.ContentTypes.detail : id, app_label, model, base_classes
- households.Households.detail : type, prefix, name, id
- households.Households.insert : name, type
- households.Households.merge_row : merge_to, households_Member, addresses_Address, reason
- households.HouseholdsByType.detail : type, prefix, name, id
- households.HouseholdsByType.insert : name, language
- households.MembersByPerson.insert : person, role, household, primary
- households.Types.detail : name, name_nl, name_de, name_en
- humanlinks.Links.detail : parent, type, child
- humanlinks.Links.insert : parent, type, child
- immersion.ContractTypes.detail : id, name, name_nl, name_de, name_en, exam_policy, template, overlap_group, full_name
- immersion.ContractTypes.insert : name, name_nl, name_de, name_en, exam_policy
- immersion.Contracts.detail : id, client, user, language, type, goal, company, contact_person, contact_role, applies_from, applies_until, exam_policy, sector, function, reference_person, printed, date_decided, date_issued, date_ended, ending, remark
- immersion.Contracts.insert : client, company, type, goal
- immersion.Goals.detail : id, name, name_nl, name_de, name_en
- isip.ContractEndings.detail : name, use_in_isip, use_in_jobs, is_success, needs_date_ended
- isip.ContractPartners.detail : company, contact_person, contact_role, duties_company
- isip.ContractPartners.insert : company, contact_person, contact_role
- isip.ContractTypes.detail : id, ref, exam_policy, overlap_group, needs_study_type, name, name_nl, name_de, name_en, full_name
- isip.Contracts.detail : id, client, type, user, user_asd, study_type, applies_from, applies_until, exam_policy, language, date_decided, date_issued, printed, date_ended, ending, uploads_UploadsByController
- isip.Contracts.insert : client, type
- isip.ExamPolicies.detail : id, name, name_nl, name_de, name_en, max_events, every, every_unit, event_type, monday, tuesday, wednesday, thursday, friday, saturday, sunday
- jobs.ContractTypes.detail : id, name, name_nl, name_de, name_en, ref, overlap_group
- jobs.ContractTypes.merge_row : merge_to, reason
- jobs.Contracts.detail : id, client, user, user_asd, language, job, type, company, contact_person, contact_role, applies_from, duration, applies_until, exam_policy, regime, schedule, hourly_rate, refund_rate, reference_person, remark, printed, date_decided, date_issued, date_ended, ending, responsibilities
- jobs.Contracts.insert : client, job
- jobs.JobProviders.detail : overview, prefix, name, type, vat_id, client_contact_type, url, email, phone, gsm, fax, notes_NotesByCompany
- jobs.JobProviders.merge_row : merge_to, addresses_Address, reason
- jobs.JobTypes.detail : id, name, is_social
- jobs.Jobs.detail : name, provider, contract_type, type, id, sector, function, capacity, hourly_rate, remark
- jobs.Jobs.insert : name, provider, contract_type, type, sector, function
- jobs.JobsOverview.show : body
- jobs.Offers.detail : name, provider, sector, function, selection_from, selection_until, start_date, remark
- jobs.Schedules.detail : id, name, name_nl, name_de, name_en
- languages.Languages.detail : id, iso2, name, name_nl, name_de, name_en
- newcomers.AvailableCoachesByClient.assign_coach : notify_subject, notify_body, notify_silent
- newcomers.Faculties.detail : id, name, name_nl, name_de, name_en, weight
- newcomers.Faculties.insert : name, name_nl, name_de, name_en, weight
- notes.EventTypes.detail : id, name, name_nl, name_de, name_en, remark
- notes.NoteTypes.detail : id, name, name_nl, name_de, name_en, build_method, template, special_type, email_template, attach_to_email, remark
- notes.NoteTypes.insert : name, name_nl, name_de, name_en, build_method
- notes.Notes.detail : date, time, event_type, type, project, subject, important, company, contact_person, user, language, build_time, id, body, uploads_UploadsByController
- notes.Notes.insert : event_type, type, subject, project
- notes.NotesByOwner.insert : event_type, type, subject, project
- outbox.Mails.detail : subject, project, date, user, sent, id, owner, outbox_AttachmentsByMail, uploads_UploadsByController, body
- outbox.Mails.insert : project, subject, body
- pcsw.Clients.create_visit : user, summary
- pcsw.Clients.detail : overview, gender, id, nationality, last_name, first_name, middle_name, birth_date, age, language, email, phone, fax, gsm, image, national_id, civil_state, birth_country, birth_place, declared_name, needs_residence_permit, needs_work_permit, in_belgium_since, residence_type, residence_until, group, aid_type, AgentsByClient, workflow_buttons, id_document, faculty, households_MembersByPerson, child_custody, humanlinks_LinksByHuman, skills, obstacles, is_seeking, unemployed_since, seeking_since, activity, client_state, noble_condition, unavailable_until, unavailable_why, is_obsolete, has_esf, created, modified, remarks, checkdata_ProblemsByOwner
- pcsw.Clients.insert : first_name, last_name, national_id, gender, language
- pcsw.Clients.merge_row : merge_to, aids_IncomeConfirmation, aids_RefundConfirmation, aids_SimpleConfirmation, coachings_Coaching, esf_ClientSummary, pcsw_Dispense, cv_LanguageKnowledge, cv_Obstacle, cv_Skill, cv_SoftSkill, addresses_Address, reason
- pcsw.Clients.refuse_client : reason, remark
- polls.AnswerRemarks.detail : remark, response, question
- polls.AnswerRemarks.insert : remark, response, question
- polls.ChoiceSets.detail : name, name_nl, name_de, name_en
- polls.Polls.detail : ref, title, workflow_buttons, details, default_choiceset, default_multiple_choices, id, user, created, modified, state
- polls.Polls.insert : ref, title, default_choiceset, default_multiple_choices, questions_to_add
- polls.Polls.merge_row : merge_to, polls_Question, reason
- polls.Questions.detail : poll, number, is_heading, choiceset, multiple_choices, title, details
- polls.Responses.detail : poll, partner, date, workflow_buttons, polls_AnswersByResponseEditor, user, state, remark, polls_AnswersByResponsePrint
- polls.Responses.insert : user, date, poll
- system.SiteConfigs.detail : site_company, next_partner_id, job_office, master_budget, signer1, signer2, signer1_function, signer2_function, system_note_type, default_build_method, residence_permit_upload_type, work_permit_upload_type, driving_licence_upload_type, default_event_type, prompt_calendar, hide_events_before, client_guestrole, team_guestrole, cbss_org_unit, sector, ssdn_user_id, ssdn_email, cbss_http_username, cbss_http_password
- tinymce.TextFieldTemplates.detail : id, name, user, description, text
- tinymce.TextFieldTemplates.insert : name, user
- uploads.AllUploads.detail : file, user, volume, library_file, upload_area, type, description, owner
- uploads.AllUploads.insert : type, description, file, volume, library_file, user
- uploads.UploadTypes.detail : id, upload_area, shortcut, name, name_nl, name_de, name_en, warn_expiry_unit, warn_expiry_value, wanted, max_number
- uploads.UploadTypes.insert : upload_area, name, name_nl, name_de, name_en, warn_expiry_unit, warn_expiry_value
- uploads.Uploads.detail : user, project, id, type, description, start_date, end_date, needed, company, contact_person, contact_role, file, owner, remark
- uploads.Uploads.insert : type, file, start_date, end_date, description
- uploads.UploadsByClient.insert : file, type, end_date, description
- uploads.UploadsByController.insert : file, type, end_date, description
- uploads.Volumes.detail : ref, description, root_dir, base_url, overview
- uploads.Volumes.insert : ref, description, root_dir, base_url
- uploads.Volumes.merge_row : merge_to, reason
- users.AllUsers.change_password : current, new1, new2
- users.AllUsers.detail : username, user_type, partner, first_name, last_name, initials, email, language, mail_mode, id, created, modified, remarks, event_type, access_class, calendar, newcomer_quota, coaching_type, coaching_supervisor, newcomer_consultations, newcomer_appointments
- users.AllUsers.insert : username, email, first_name, last_name, partner, language, user_type
- users.AllUsers.send_welcome_email : email, subject
- users.UsersOverview.sign_in : username, password
<BLANKLINE>

.. Note the following items disappeared after 20190107

  - courses.StatusReport.show : body
  - integ.ActivityReport.show : body


Windows and permissions
=======================

Each window layout is **viewable** by a given set of user types.

>>> print(analyzer.show_window_permissions()) #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
- about.About.show : visible for all
- active_job_search.Proofs.detail : visible for 110 120 420 admin 910
- addresses.Addresses.detail : visible for admin 910
- addresses.Addresses.insert : visible for admin 910
- aids.AidTypes.detail : visible for 110 120 210 410 420 500 510 800 admin 910
- aids.AidTypes.insert : visible for 110 120 210 410 420 500 510 800 admin 910
- aids.Categories.detail : visible for 110 120 210 410 420 500 510 800 admin 910
- aids.Grantings.detail : visible for 100 110 120 200 210 300 400 410 420 500 510 800 admin 910
- aids.Grantings.insert : visible for 100 110 120 200 210 300 400 410 420 500 510 800 admin 910
- aids.GrantingsByClient.insert : visible for 100 110 120 200 210 300 400 410 420 500 510 800 admin 910
- aids.IncomeConfirmations.detail : visible for 100 110 120 200 210 300 400 410 420 500 510 800 admin 910
- aids.IncomeConfirmationsByGranting.insert : visible for 100 110 120 200 210 300 400 410 420 500 510 800 admin 910
- aids.RefundConfirmations.detail : visible for 100 110 120 200 210 300 400 410 420 500 510 800 admin 910
- aids.RefundConfirmationsByGranting.insert : visible for 100 110 120 200 210 300 400 410 420 500 510 800 admin 910
- aids.SimpleConfirmations.detail : visible for 100 110 120 200 210 300 400 410 420 500 510 800 admin 910
- aids.SimpleConfirmationsByGranting.insert : visible for 100 110 120 200 210 300 400 410 420 500 510 800 admin 910
- art61.ContractTypes.detail : visible for 110 120 420 admin 910
- art61.ContractTypes.merge_row : visible for admin 910
- art61.Contracts.detail : visible for 100 110 120 420 admin 910
- art61.Contracts.insert : visible for 100 110 120 420 admin 910
- boards.Boards.detail : visible for admin 910
- boards.Boards.insert : visible for admin 910
- cal.Calendars.detail : visible for 110 120 410 420 admin 910
- cal.Calendars.insert : visible for 110 120 410 420 admin 910
- cal.DailyView.detail : visible for 100 110 120 200 300 400 410 420 500 510 admin 910
- cal.EntriesByClient.insert : visible for 100 110 120 200 210 220 300 400 410 420 500 510 800 admin 910
- cal.EntriesByGuest.insert : visible for 100 110 120 200 210 220 300 400 410 420 500 510 800 admin 910
- cal.EntriesByProject.insert : visible for 100 110 120 200 210 220 300 400 410 420 500 510 800 admin 910
- cal.EventTypes.detail : visible for 110 120 410 420 admin 910
- cal.EventTypes.insert : visible for 110 120 410 420 admin 910
- cal.EventTypes.merge_row : visible for admin 910
- cal.Events.detail : visible for 110 120 410 420 admin 910
- cal.Events.insert : visible for 110 120 410 420 admin 910
- cal.GuestRoles.detail : visible for admin 910
- cal.GuestRoles.merge_row : visible for admin 910
- cal.GuestStates.wf1 : visible for 100 110 120 200 210 220 300 400 410 420 800 admin 910
- cal.GuestStates.wf2 : visible for 100 110 120 200 210 220 300 400 410 420 800 admin 910
- cal.Guests.checkin : visible for 100 110 120 200 210 220 300 400 410 420 800 admin 910
- cal.Guests.detail : visible for 100 110 120 200 210 220 300 400 410 420 800 admin 910
- cal.Guests.insert : visible for 100 110 120 200 210 220 300 400 410 420 800 admin 910
- cal.MonthlyView.detail : visible for 100 110 120 200 300 400 410 420 500 510 admin 910
- cal.RecurrentEvents.detail : visible for 110 120 410 420 admin 910
- cal.RecurrentEvents.insert : visible for 110 120 410 420 admin 910
- cal.Rooms.detail : visible for 110 120 410 420 admin 910
- cal.Rooms.insert : visible for 110 120 410 420 admin 910
- cal.Tasks.detail : visible for 110 120 410 420 admin 910
- cal.Tasks.insert : visible for 110 120 410 420 admin 910
- cal.TasksByController.insert : visible for 100 110 120 200 300 400 410 420 500 510 admin 910
- cal.WeeklyView.detail : visible for 100 110 120 200 300 400 410 420 500 510 admin 910
- cbss.IdentifyPersonRequests.detail : visible for 100 110 120 200 210 300 400 410 420 admin 910
- cbss.IdentifyPersonRequests.insert : visible for 100 110 120 200 210 300 400 410 420 admin 910
- cbss.ManageAccessRequests.detail : visible for 100 110 120 200 210 300 400 410 420 admin 910
- cbss.ManageAccessRequests.insert : visible for 100 110 120 200 210 300 400 410 420 admin 910
- cbss.RetrieveTIGroupsRequests.detail : visible for 100 110 120 200 210 300 400 410 420 admin 910
- cbss.RetrieveTIGroupsRequests.insert : visible for 100 110 120 200 210 300 400 410 420 admin 910
- changes.Changes.detail : visible for admin 910
- checkdata.Checkers.detail : visible for admin 910
- checkdata.Problems.detail : visible for 100 110 120 200 210 220 300 400 410 420 500 510 800 admin 910
- clients.ClientContactTypes.detail : visible for 110 120 210 410 420 800 admin 910
- coachings.CoachingEndings.detail : visible for 110 120 210 410 420 admin 910
- coachings.Coachings.create_visit : visible for 110 120 210 410 420 admin 910
- contacts.Companies.detail : visible for 100 110 120 200 210 220 300 400 410 420 500 510 800 admin 910
- contacts.Companies.insert : visible for 100 110 120 200 210 220 300 400 410 420 500 510 800 admin 910
- contacts.Companies.merge_row : visible for admin 910
- contacts.Partners.merge_row : visible for admin 910
- contacts.Persons.create_household : visible for 100 110 120 200 210 220 300 400 410 420 500 510 800 admin 910
- contacts.Persons.detail : visible for 100 110 120 200 210 220 300 400 410 420 500 510 800 admin 910
- contacts.Persons.insert : visible for 100 110 120 200 210 220 300 400 410 420 500 510 800 admin 910
- contacts.Persons.merge_row : visible for admin 910
- countries.Countries.detail : visible for 110 120 210 410 420 800 admin 910
- countries.Countries.insert : visible for 110 120 210 410 420 800 admin 910
- countries.Places.detail : visible for 110 120 210 410 420 800 admin 910
- courses.Activities.detail : visible for 100 110 120 200 210 300 400 410 420 800 admin 910
- courses.Activities.insert : visible for 100 110 120 200 210 300 400 410 420 800 admin 910
- courses.Activities.print_presence_sheet : visible for 100 110 120 200 210 300 400 410 420 800 admin 910
- courses.Activities.print_presence_sheet_html : visible for 100 110 120 200 210 300 400 410 420 800 admin 910
- courses.Enrolments.detail : visible for 100 110 120 200 210 300 400 410 420 800 admin 910
- courses.Enrolments.insert : visible for 100 110 120 200 210 300 400 410 420 800 admin 910
- courses.EnrolmentsByCourse.insert : visible for 100 110 120 200 210 300 400 410 420 800 admin 910
- courses.EnrolmentsByPupil.insert : visible for 100 110 120 200 210 300 400 410 420 800 admin 910
- courses.Lines.detail : visible for 100 110 120 200 210 300 400 410 420 800 admin 910
- courses.Lines.insert : visible for 100 110 120 200 210 300 400 410 420 800 admin 910
- courses.Lines.merge_row : visible for admin 910
- courses.Slots.detail : visible for admin 910
- courses.Slots.insert : visible for admin 910
- courses.Topics.detail : visible for admin 910
- cv.Durations.detail : visible for 110 120 420 admin 910
- cv.EducationLevels.detail : visible for 110 120 420 admin 910
- cv.Experiences.detail : visible for 110 120 420 admin 910
- cv.ExperiencesByPerson.insert : visible for 100 110 120 420 admin 910
- cv.Functions.detail : visible for 110 120 420 admin 910
- cv.LanguageKnowledgesByPerson.detail : visible for 100 110 120 420 admin 910
- cv.LanguageKnowledgesByPerson.insert : visible for 100 110 120 420 admin 910
- cv.Regimes.detail : visible for 110 120 420 admin 910
- cv.Sectors.detail : visible for 110 120 420 admin 910
- cv.Statuses.detail : visible for 110 120 420 admin 910
- cv.Studies.detail : visible for 110 120 420 admin 910
- cv.StudiesByPerson.insert : visible for 100 110 120 420 admin 910
- cv.StudyTypes.detail : visible for 110 120 420 admin 910
- cv.StudyTypes.insert : visible for 110 120 420 admin 910
- cv.Trainings.detail : visible for 100 110 120 420 admin 910
- cv.Trainings.insert : visible for 100 110 120 420 admin 910
- debts.Accounts.detail : visible for admin 910
- debts.Accounts.insert : visible for admin 910
- debts.Accounts.merge_row : visible for admin 910
- debts.Budgets.detail : visible for admin 910
- debts.Budgets.insert : visible for admin 910
- debts.Groups.detail : visible for admin 910
- debts.Groups.insert : visible for admin 910
- esf.Summaries.detail : visible for 100 110 120 200 210 220 300 400 410 420 500 510 800 admin 910
- excerpts.ExcerptTypes.detail : visible for admin 910
- excerpts.ExcerptTypes.insert : visible for admin 910
- excerpts.Excerpts.detail : visible for 100 110 120 200 210 220 300 400 410 420 500 510 800 admin 910
- gfks.ContentTypes.detail : visible for admin 910
- households.Households.detail : visible for 100 110 120 200 210 300 400 410 420 500 510 800 admin 910
- households.Households.insert : visible for 100 110 120 200 210 300 400 410 420 500 510 800 admin 910
- households.Households.merge_row : visible for admin 910
- households.HouseholdsByType.detail : visible for 100 110 120 200 210 300 400 410 420 500 510 800 admin 910
- households.HouseholdsByType.insert : visible for 100 110 120 200 210 300 400 410 420 500 510 800 admin 910
- households.MembersByPerson.insert : visible for 100 110 120 200 210 300 400 410 420 500 510 800 admin 910
- households.Types.detail : visible for 110 120 210 410 420 800 admin 910
- humanlinks.Links.detail : visible for 110 120 210 410 420 800 admin 910
- humanlinks.Links.insert : visible for 110 120 210 410 420 800 admin 910
- immersion.ContractTypes.detail : visible for 110 120 420 admin 910
- immersion.ContractTypes.insert : visible for 110 120 420 admin 910
- immersion.Contracts.detail : visible for 100 110 120 420 admin 910
- immersion.Contracts.insert : visible for 100 110 120 420 admin 910
- immersion.Goals.detail : visible for 110 120 420 admin 910
- isip.ContractEndings.detail : visible for 110 120 410 420 admin 910
- isip.ContractPartners.detail : visible for 110 120 410 420 admin 910
- isip.ContractPartners.insert : visible for 110 120 410 420 admin 910
- isip.ContractTypes.detail : visible for 110 120 410 420 admin 910
- isip.Contracts.detail : visible for 100 110 120 200 300 400 410 420 admin 910
- isip.Contracts.insert : visible for 100 110 120 200 300 400 410 420 admin 910
- isip.ExamPolicies.detail : visible for 110 120 410 420 admin 910
- jobs.ContractTypes.detail : visible for 110 120 410 420 admin 910
- jobs.ContractTypes.merge_row : visible for admin 910
- jobs.Contracts.detail : visible for 100 110 120 200 300 400 410 420 admin 910
- jobs.Contracts.insert : visible for 100 110 120 200 300 400 410 420 admin 910
- jobs.JobProviders.detail : visible for 100 110 120 420 admin 910
- jobs.JobProviders.merge_row : visible for admin 910
- jobs.JobTypes.detail : visible for 110 120 410 420 admin 910
- jobs.Jobs.detail : visible for 100 110 120 420 admin 910
- jobs.Jobs.insert : visible for 100 110 120 420 admin 910
- jobs.JobsOverview.show : visible for 100 110 120 420 admin 910
- jobs.Offers.detail : visible for 100 110 120 420 admin 910
- jobs.Schedules.detail : visible for 110 120 410 420 admin 910
- languages.Languages.detail : visible for 110 120 410 420 admin 910
- newcomers.AvailableCoachesByClient.assign_coach : visible for 110 120 200 220 300 420 800 admin 910
- newcomers.Faculties.detail : visible for 110 120 410 420 admin 910
- newcomers.Faculties.insert : visible for 110 120 410 420 admin 910
- notes.EventTypes.detail : visible for 110 120 410 420 admin 910
- notes.NoteTypes.detail : visible for 110 120 410 420 admin 910
- notes.NoteTypes.insert : visible for 110 120 410 420 admin 910
- notes.Notes.detail : visible for 100 110 120 200 210 220 300 400 410 420 500 510 800 admin 910
- notes.Notes.insert : visible for 100 110 120 200 210 220 300 400 410 420 500 510 800 admin 910
- notes.NotesByOwner.insert : visible for 100 110 120 200 210 220 300 400 410 420 500 510 800 admin 910
- outbox.Mails.detail : visible for 110 120 410 420 admin 910
- outbox.Mails.insert : visible for 110 120 410 420 admin 910
- pcsw.Clients.create_visit : visible for 100 110 120 200 210 220 300 400 410 420 500 510 800 admin 910
- pcsw.Clients.detail : visible for 100 110 120 200 210 220 300 400 410 420 500 510 800 admin 910
- pcsw.Clients.insert : visible for 100 110 120 200 210 220 300 400 410 420 500 510 800 admin 910
- pcsw.Clients.merge_row : visible for admin 910
- pcsw.Clients.refuse_client : visible for 120 200 220 300 420 admin 910
- polls.AnswerRemarks.detail : visible for 100 110 120 200 300 400 410 420 admin 910
- polls.AnswerRemarks.insert : visible for 100 110 120 200 300 400 410 420 admin 910
- polls.ChoiceSets.detail : visible for 110 120 410 420 admin 910
- polls.Polls.detail : visible for 100 110 120 200 300 400 410 420 admin 910
- polls.Polls.insert : visible for 100 110 120 200 300 400 410 420 admin 910
- polls.Polls.merge_row : visible for admin 910
- polls.Questions.detail : visible for 110 120 410 420 admin 910
- polls.Responses.detail : visible for 100 110 120 200 300 400 410 420 admin 910
- polls.Responses.insert : visible for 100 110 120 200 300 400 410 420 admin 910
- system.SiteConfigs.detail : visible for admin 910
- tinymce.TextFieldTemplates.detail : visible for admin 910
- tinymce.TextFieldTemplates.insert : visible for admin 910
- uploads.AllUploads.detail : visible for 110 120 410 420 admin 910
- uploads.AllUploads.insert : visible for 110 120 410 420 admin 910
- uploads.UploadTypes.detail : visible for 110 120 410 420 admin 910
- uploads.UploadTypes.insert : visible for 110 120 410 420 admin 910
- uploads.Uploads.detail : visible for 100 110 120 200 210 220 300 400 410 420 500 510 800 admin 910
- uploads.Uploads.insert : visible for 100 110 120 200 210 220 300 400 410 420 500 510 800 admin 910
- uploads.UploadsByClient.insert : visible for 100 110 120 200 210 300 400 410 420 500 510 800 admin 910
- uploads.UploadsByController.insert : visible for 100 110 120 200 210 220 300 400 410 420 500 510 800 admin 910
- uploads.Volumes.detail : visible for 110 120 410 420 admin 910
- uploads.Volumes.insert : visible for 110 120 410 420 admin 910
- uploads.Volumes.merge_row : visible for admin 910
- users.AllUsers.change_password : visible for admin 910
- users.AllUsers.detail : visible for admin 910
- users.AllUsers.insert : visible for admin 910
- users.AllUsers.send_welcome_email : visible for admin 910
- users.UsersOverview.sign_in : visible for all
<BLANKLINE>





UsersWithClients
================

>>> rt.show(integ.UsersWithClients) #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE -REPORT_UDIFF
====================== ============ =========== ======== ========= ========= =================== ====================== ========
 Intervenant            Évaluation   Formation   Search   Travail   Standby   Dossiers complèts   Bénéficiaires actifs   Total
---------------------- ------------ ----------- -------- --------- --------- ------------------- ---------------------- --------
 Alicia Allmanns        **1**        **1**                          **1**     **3**               **3**                  **7**
 Hubert Huppertz        **1**        **3**       **4**    **2**     **1**     **11**              **11**                 **19**
 Mélanie Mélard         **2**                    **2**    **4**     **3**     **11**              **11**                 **18**
 **Total (3 lignes)**   **4**        **4**       **6**    **6**     **5**     **25**              **25**                 **44**
====================== ============ =========== ======== ========= ========= =================== ====================== ========
<BLANKLINE>

Note that the numbers in this table depend on
:attr:`lino_welfare.modlib.integ.Plugin.only_primary` whose default
value in chatelet is `True`.

>>> dd.plugins.integ.only_primary
True




Dialog actions
==============

Voici une liste des actions qui ont un dialogue, càd pour lesquelles,
avant de les exécuter, Lino ouvre une fenêtre à part pour demander des
options.

>>> show_dialog_actions()  #doctest: +REPORT_UDIFF
- polls.AllResponses.toggle_choice : toggle_choice
  (main) [visible for all]: **Question** (question), **Choix** (choice)
- polls.MyResponses.toggle_choice : toggle_choice
  (main) [visible for all]: **Question** (question), **Choix** (choice)
- polls.Responses.toggle_choice : toggle_choice
  (main) [visible for all]: **Question** (question), **Choix** (choice)
- polls.ResponsesByPartner.toggle_choice : toggle_choice
  (main) [visible for all]: **Question** (question), **Choix** (choice)
- polls.ResponsesByPoll.toggle_choice : toggle_choice
  (main) [visible for all]: **Question** (question), **Choix** (choice)
- art61.ContractTypes.merge_row : Fusionner
  (main) [visible for all]: **vers...** (merge_to), **Raison** (reason)
- cal.EventTypes.merge_row : Fusionner
  (main) [visible for all]: **vers...** (merge_to), **Raison** (reason)
- cal.GuestRoles.merge_row : Fusionner
  (main) [visible for all]: **vers...** (merge_to), **Raison** (reason)
- cal.GuestStates.wf1 : Accepter
  (main) [visible for all]: **Résumé** (notify_subject), **Description** (notify_body), **Ne pas avertir les autres** (notify_silent)
- cal.GuestStates.wf2 : Rejeter
  (main) [visible for all]: **Résumé** (notify_subject), **Description** (notify_body), **Ne pas avertir les autres** (notify_silent)
- cal.Guests.checkin : Arriver
  (main) [visible for all]: **Résumé** (notify_subject), **Description** (notify_body), **Ne pas avertir les autres** (notify_silent)
- coachings.Coachings.create_visit : Enregistrer consultation
  (main) [visible for all]: **Utilisateur** (user), **Raison** (summary)
- contacts.Companies.merge_row : Fusionner
  (main) [visible for all]: **vers...** (merge_to), **Adresses** (addresses_Address), **Raison** (reason)
- contacts.Partners.merge_row : Fusionner
  (main) [visible for all]: **vers...** (merge_to), **Adresses** (addresses_Address), **Raison** (reason)
- contacts.Persons.create_household : Créer un ménage
  (main) [visible for all]: **Chef de ménage** (head), **Type de ménage** (type), **Partenaire** (partner)
- contacts.Persons.merge_row : Fusionner
  (main) [visible for all]:
  - **vers...** (merge_to)
  - **Also reassign volatile related objects** (keep_volatiles):
    - (keep_volatiles_1): **Connaissances de langue** (cv_LanguageKnowledge), **Freins** (cv_Obstacle)
    - (keep_volatiles_2): **Compétences professionnelles** (cv_Skill), **Compétences sociales** (cv_SoftSkill)
    - **Adresses** (addresses_Address)
  - **Raison** (reason)
- courses.Activities.print_presence_sheet : Fiche de présences
  (main) [visible for all]: **Date du** (start_date), **au ** (end_date), **Show remarks** (show_remarks), **Show states** (show_states)
- courses.Activities.print_presence_sheet_html : Fiche de présences (HTML)
  (main) [visible for all]: **Date du** (start_date), **au ** (end_date), **Show remarks** (show_remarks), **Show states** (show_states)
- courses.Lines.merge_row : Fusionner
  (main) [visible for all]: **vers...** (merge_to), **Raison** (reason)
- debts.Accounts.merge_row : Fusionner
  (main) [visible for all]: **vers...** (merge_to), **Raison** (reason)
- households.Households.merge_row : Fusionner
  (main) [visible for all]:
  - **vers...** (merge_to)
  - **Also reassign volatile related objects** (keep_volatiles): **Membres de ménage** (households_Member), **Adresses** (addresses_Address)
  - **Raison** (reason)
- jobs.ContractTypes.merge_row : Fusionner
  (main) [visible for all]: **vers...** (merge_to), **Raison** (reason)
- jobs.JobProviders.merge_row : Fusionner
  (main) [visible for all]: **vers...** (merge_to), **Adresses** (addresses_Address), **Raison** (reason)
- newcomers.AvailableCoachesByClient.assign_coach : Attribuer
  (main) [visible for all]: **Résumé** (notify_subject), **Description** (notify_body), **Ne pas avertir les autres** (notify_silent)
- pcsw.Clients.create_visit : Enregistrer consultation
  (main) [visible for all]: **Utilisateur** (user), **Raison** (summary)
- pcsw.Clients.merge_row : Fusionner
  (main) [visible for all]:
  - **vers...** (merge_to)
  - **Also reassign volatile related objects** (keep_volatiles):
    - (keep_volatiles_1): **Certificats de revenu** (aids_IncomeConfirmation), **Refund confirmations** (aids_RefundConfirmation)
    - (keep_volatiles_2): **Confirmations simple** (aids_SimpleConfirmation), **Interventions** (coachings_Coaching)
    - (keep_volatiles_3): **Fiches FSE** (esf_ClientSummary), **Dispenses** (pcsw_Dispense)
    - (keep_volatiles_4): **Connaissances de langue** (cv_LanguageKnowledge), **Freins** (cv_Obstacle)
    - (keep_volatiles_5): **Compétences professionnelles** (cv_Skill), **Compétences sociales** (cv_SoftSkill)
    - **Adresses** (addresses_Address)
  - **Raison** (reason)
- pcsw.Clients.refuse_client : Refuser
  (main) [visible for all]: **Raison de refus** (reason), **Remarque** (remark)
- polls.Polls.merge_row : Fusionner
  (main) [visible for all]: **vers...** (merge_to), **Questions** (polls_Question), **Raison** (reason)
- uploads.Volumes.merge_row : Fusionner
  (main) [visible for all]: **vers...** (merge_to), **Raison** (reason)
- users.AllUsers.change_password : Changer mot de passe
  (main) [visible for all]: **Mot de passe actuel** (current), **Nouveau mot de passe** (new1), **Encore une fois** (new2)
- users.AllUsers.send_welcome_email : Welcome mail
  (main) [visible for all]: **adresse e-mail** (email), **Sujet** (subject)
- users.UsersOverview.sign_in : Sign in
  (main) [visible for all]: **Nom d'utilisateur** (username), **Mot de passe** (password)
<BLANKLINE>




Menu walk
=========

Here is the output of :func:`walk_menu_items
<lino.api.doctests.walk_menu_items>` for this database:

>>> walk_menu_items('romain') #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
- Contacts --> Personnes : 103
- Contacts --> Bénéficiaires : 58
- Contacts --> Organisations : 40
- Contacts --> Partenaires (tous) : 163
- Contacts --> Ménages : 15
- Bureau --> Mes Notifications : 2
- Bureau --> Mes Extraits : 0
- Bureau --> Mes téléchargements à renouveler : 1
- Bureau --> Mes Fichiers téléchargés : 1
- Bureau --> Mon courrier sortant : 1
- Bureau --> Mes Observations : 10
- Bureau --> Mes problèmes de données : 0
- Calendrier --> Mes rendez-vous : 6
- Calendrier --> Rendez-vous dépassés : 74
- Calendrier --> Mes rendez-vous à confirmer : 3
- Calendrier --> Mes tâches : 1
- Calendrier --> Mes visiteurs : 1
- Calendrier --> Mes présences : 1
- Calendrier --> Mes rendez-vous dépassés : 2
- Réception --> Bénéficiaires : 30
- Réception --> Rendez-vous aujourd'hui : 4
- Réception --> Salle d'attente : 8
- Réception --> Visiteurs occupés : 4
- Réception --> Visiteurs repartis : 7
- Réception --> Visiteurs qui m'attendent : 0
- CPAS --> Bénéficiaires : 30
- CPAS --> Mes Interventions : 1
- CPAS --> Octrois à confirmer : 1
- Intégration --> Bénéficiaires : 0
- Intégration --> PIISs : 1
- Intégration --> Mises à l'emploi art60§7 : 1
- Intégration --> Services utilisateurs : 4
- Intégration --> Postes de travail : 9
- Intégration --> Offres d'emploi : 2
- Intégration --> Mises à l'emploi art61 : 1
- Intégration --> Stages d'immersion : 1
- Intégration --> BCSS --> Mes Requêtes IdentifyPerson : 1
- Intégration --> BCSS --> Mes Requêtes ManageAccess : 1
- Intégration --> BCSS --> Mes Requêtes Tx25 : 1
- Ateliers --> Mes Ateliers : 1
- Ateliers --> Ateliers d'insertion sociale : 6
- Ateliers --> Ateliers d'Insertion socioprofessionnelle : 3
- Ateliers --> Séries d'ateliers : 8
- Ateliers --> Demandes d’inscription en attente : 18
- Ateliers --> Demandes d’inscription confirmées : 18
- Nouvelles demandes --> Nouveaux bénéficiaires : 23
- Nouvelles demandes --> Agents disponibles : 3
- Médiation de dettes --> Bénéficiaires : 0
- Médiation de dettes --> Mes Budgets : 4
- Questionnaires --> Mes Questionnaires : 1
- Questionnaires --> Mes Interviews : 1
- Rapports --> Intégration --> Agents et leurs clients : 3
- Configuration --> Système --> Utilisateurs : 13
- Configuration --> Système --> Textes d'aide : 6
- Configuration --> Endroits --> Pays : 271
- Configuration --> Endroits --> Endroits : 79
- Configuration --> Contacts --> Types d'organisation : 17
- Configuration --> Contacts --> Fonctions : 6
- Configuration --> Contacts --> Conseils : 4
- Configuration --> Contacts --> Types de ménage : 7
- Configuration --> Bureau --> Types d'extrait : 20
- Configuration --> Bureau --> Libraries de fichiers : 1
- Configuration --> Bureau --> Types de fichiers téléchargés : 10
- Configuration --> Bureau --> Types d'observation : 14
- Configuration --> Bureau --> Types d'événements : 11
- Configuration --> Bureau --> Mes Text Field Templates : 1
- Configuration --> Calendrier --> Calendriers : ...
- Configuration --> Calendrier --> Locaux : 1
- Configuration --> Calendrier --> Évènements periodiques : 16
- Configuration --> Calendrier --> Rôles de participants : 5
- Configuration --> Calendrier --> Types d'entrée calendrier : 14
- Configuration --> Calendrier --> Règles de récurrence : 7
- Configuration --> Calendrier --> Calendriers externes : 1
- Configuration --> Calendrier --> Lignes de planificateur : 4
- Configuration --> Ateliers --> Savoirs de base : 1
- Configuration --> Ateliers --> Topics : 1
- Configuration --> Ateliers --> Timetable Slots : 1
- Configuration --> CPAS --> Droits chômage : 1
- Configuration --> CPAS --> Types d'aide sociale : 12
- Configuration --> CPAS --> Catégories : 4
- Configuration --> CPAS --> Types de contact client : 11
- Configuration --> CPAS --> Services : 4
- Configuration --> CPAS --> Raisons d’arrêt d'intervention : 5
- Configuration --> Parcours --> Types d'éducation : 12
- Configuration --> Parcours --> Niveaux académiques : 6
- Configuration --> Parcours --> Secteurs : 15
- Configuration --> Parcours --> Fonctions : 5
- Configuration --> Parcours --> Régimes de travail : 4
- Configuration --> Parcours --> Statuts : 8
- Configuration --> Parcours --> Types de contrat : 6
- Configuration --> Parcours --> Types de compétence sociale : 1
- Configuration --> Parcours --> Types de freins : 5
- Configuration --> Parcours --> Preuves de qualification : 5
- Configuration --> Parcours --> Langues : 6
- Configuration --> Intégration --> Types de PIIS : 6
- Configuration --> Intégration --> Motifs d’arrêt de contrat : 5
- Configuration --> Intégration --> Régimes d'évaluation : 7
- Configuration --> Intégration --> Types de mise à l'emploi art60§7 : 6
- Configuration --> Intégration --> Types de poste : 6
- Configuration --> Intégration --> Horaires : 4
- Configuration --> Intégration --> Types de mise à l'emploi art.61 : 2
- Configuration --> Intégration --> Types de stage d'immersion : 4
- Configuration --> Intégration --> Objectifs : 5
- Configuration --> Nouvelles demandes --> Intermédiaires : 3
- Configuration --> Nouvelles demandes --> Spécificités : 6
- Configuration --> BCSS --> Secteurs : 210
- Configuration --> BCSS --> Codes fonction : 107
- Configuration --> Médiation de dettes --> Groupes de comptes : 9
- Configuration --> Médiation de dettes --> Comptes : 52
- Configuration --> Questionnaires --> Listes de choix : 10
- Explorateur --> Contacts --> Personnes de contact : 11
- Explorateur --> Contacts --> Partenaires : 163
- Explorateur --> Contacts --> Types d'adresses : 6
- Explorateur --> Contacts --> Adresses : 93
- Explorateur --> Contacts --> Membres du conseil : 1
- Explorateur --> Contacts --> Rôles de membres de ménage : 9
- Explorateur --> Contacts --> Membres de ménage : 64
- Explorateur --> Contacts --> Liens de parenté : 60
- Explorateur --> Contacts --> Types de parenté : 13
- Explorateur --> Système --> Procurations : 4
- Explorateur --> Système --> Types d'utilisateur : 16
- Explorateur --> Système --> Rôles d'utilisateur : 42
- Explorateur --> Système --> Notifications : 13
- Explorateur --> Système --> Changes : 0
- Explorateur --> Système --> All dashboard widgets : 1
- Explorateur --> Système --> Types de contenu : 136
- Explorateur --> Système --> Tests de données : 14
- Explorateur --> Système --> Problèmes de données : 0
- Explorateur --> Bureau --> Extraits : 71
- Explorateur --> Bureau --> Fichiers téléchargés : 12
- Explorateur --> Bureau --> Upload Areas : 2
- Explorateur --> Bureau --> Mails envoyés : 1
- Explorateur --> Bureau --> Pièces jointes : 1
- Explorateur --> Bureau --> Observations : 112
- Explorateur --> Bureau --> Text Field Templates : 3
- Explorateur --> Calendrier --> Entrées calendrier : 343
- Explorateur --> Calendrier --> Tâches : 35
- Explorateur --> Calendrier --> Présences : 589
- Explorateur --> Calendrier --> Abonnements : 10
- Explorateur --> Calendrier --> Entry states : 5
- Explorateur --> Calendrier --> Presence states : 9
- Explorateur --> Calendrier --> Task states : 5
- Explorateur --> Ateliers --> Tests de niveau : 1
- Explorateur --> Ateliers --> Ateliers : 8
- Explorateur --> Ateliers --> Inscriptions : 84
- Explorateur --> Ateliers --> États Inscription : 6
- Explorateur --> Ateliers --> Course layouts : 2
- Explorateur --> Ateliers --> États Atelier : 4
- Explorateur --> CPAS --> Exclusions du chômage : 1
- Explorateur --> CPAS --> Antécédents judiciaires : 1
- Explorateur --> CPAS --> Bénéficiaires : 58
- Explorateur --> CPAS --> Etats civils : 7
- Explorateur --> CPAS --> Etats bénéficiaires : 4
- Explorateur --> CPAS --> Types de carte eID : 11
- Explorateur --> CPAS --> Octrois d'aide : 56
- Explorateur --> CPAS --> Certificats de revenu : 55
- Explorateur --> CPAS --> Refund confirmations : 13
- Explorateur --> CPAS --> Confirmations simple : 20
- Explorateur --> CPAS --> Contacts client : 15
- Explorateur --> CPAS --> Types de contact connus : 2
- Explorateur --> CPAS --> Interventions : 91
- Explorateur --> Parcours --> Connaissances de langue : 115
- Explorateur --> Parcours --> Formations : 21
- Explorateur --> Parcours --> Études : 23
- Explorateur --> Parcours --> Expériences professionnelles : 31
- Explorateur --> Parcours --> Connaissances de langue : 115
- Explorateur --> Parcours --> Compétences professionnelles : 1
- Explorateur --> Parcours --> Compétences sociales : 1
- Explorateur --> Parcours --> Freins : 21
- Explorateur --> Intégration --> PIISs : 31
- Explorateur --> Intégration --> Mises à l'emploi art60§7 : 14
- Explorateur --> Intégration --> Candidatures : 75
- Explorateur --> Intégration --> Services utilisateurs : 36
- Explorateur --> Intégration --> Mises à l'emploi art61 : 8
- Explorateur --> Intégration --> Stages d'immersion : 7
- Explorateur --> Intégration --> Preuves de recherche : 11
- Explorateur --> Intégration --> Fiches FSE : 189
- Explorateur --> Intégration --> Champs FSE : 12
- Explorateur --> Nouvelles demandes --> Compétences : 8
- Explorateur --> BCSS --> Requêtes IdentifyPerson : 6
- Explorateur --> BCSS --> Requêtes ManageAccess : 2
- Explorateur --> BCSS --> Requêtes Tx25 : 7
- Explorateur --> Médiation de dettes --> Budgets : 15
- Explorateur --> Médiation de dettes --> Entrées : 717
- Explorateur --> Questionnaires --> Questionnaires : 3
- Explorateur --> Questionnaires --> Questions : 39
- Explorateur --> Questionnaires --> Choix : 40
- Explorateur --> Questionnaires --> Interviews : 7
- Explorateur --> Questionnaires --> Choix de réponse : 89
- Explorateur --> Questionnaires --> Answer Remarks : 1
<BLANKLINE>


The first meeting of a budget
=============================

>>> translation.activate('en')

The following shows how we use the
:meth:`lino_welfare.modlib.debts.Actor.get_first_meeting` method for
printing the date and user of the first meeting.

Here is a list of all actors for which there is a first meeting.

>>> msg = "Budget {0} : First meeting on {1} with user {2}"
>>> for actor in debts.Actor.objects.all():
...     n = actor.get_first_meeting()
...     if n is not None:
...         print(msg.format(actor.budget.id, dd.fdl(n.date), n.user))
Budget 4 : First meeting on 22 July 2013 with user nicolas

The `syntax of appy.pod templates
<http://appyframework.org/podWritingTemplates.html>`_ does not yet
have a ``with`` statement.

The :xfile:`Default.odt` template uses this in a construct similar to
the following snippet:

>>> budget = debts.Budget.objects.get(pk=4)
>>> for actor in budget.get_actors():
...     print(actor.get_first_meeting_text())
None
First meeting on 22 July 2013 with nicolas
None
