.. _welfare.specs.chatelet:

==========================
Lino Welfare à la Châtelet
==========================

.. How to test only this document:

    $ python setup.py test -s tests.SpecsTests.test_chatelet

    doctest init:

    >>> from __future__ import print_function
    >>> import lino
    >>> lino.startup('lino_welfare.projects.chatelet.settings.doctests')
    >>> from lino.api.doctest import *

This document describes the *Châtelet* variant of Lino Welfare.

- uses **internal courses**
  (:mod:`lino_welfare.projects.chatelet.modlib.courses`, a sub-plugin
  of :mod:`lino.modlib.courses`) instead of **external courses**
  (:mod:`lino_welfare.modlib.courses`). And the "Courses" are labelled
  "Workshops" ("Ateliers").
    
.. contents:: 
   :local:
   :depth: 2


Site settings
=============

The default language distribution (:attr:`languages
<lino.core.site.Site.languages>`) is French, Dutch, German and English:

>>> ' '.join([lng.name for lng in settings.SITE.languages])
'fr nl de en'

But Dutch is currently hidden because we don't yet have any Flemish
speaking users (:attr:`hidden_languages
<lino.core.site.Site.hidden_languages>`):

>>> settings.SITE.hidden_languages
'nl'


Database structure
==================

This is the list of models used in the Châtelet varianat of Lino Welfare:

>>> from lino.utils.diag import analyzer
>>> print(analyzer.show_db_overview())
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF -SKIP
56 apps: lino_startup, staticfiles, about, extjs, jinja, bootstrap3, appypod, printing, system, contenttypes, gfks, humanize, users, notifier, changes, office, countries, contacts, addresses, uploads, outbox, excerpts, extensible, cal, reception, cosi, accounts, badges, boards, welfare, sales, pcsw, languages, cv, integ, isip, jobs, art61, immersion, active_job_search, courses, newcomers, cbss, households, humanlinks, notes, aids, polls, summaries, wkhtmltopdf, fse, beid, davlink, export_excel, plausibility, tinymce.
127 models:
============================== =============================== ========= =======
 Name                           Default table                   #fields   #rows
------------------------------ ------------------------------- --------- -------
 accounts.Account               accounts.Accounts               11        0
 accounts.Group                 accounts.Groups                 7         0
 active_job_search.Proof        active_job_search.Proofs        7         10
 addresses.Address              addresses.Addresses             16        90
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
 cal.Calendar                   cal.Calendars                   7         11
 cal.Event                      cal.OneEvent                    24        575
 cal.EventType                  cal.EventTypes                  20        10
 cal.Guest                      cal.Guests                      9         521
 cal.GuestRole                  cal.GuestRoles                  5         4
 cal.Priority                   cal.Priorities                  6         4
 cal.RecurrentEvent             cal.RecurrentEvents             22        16
 cal.RemoteCalendar             cal.RemoteCalendars             7         0
 cal.Room                       cal.Rooms                       5         0
 cal.Subscription               cal.Subscriptions               4         8
 cal.Task                       cal.Tasks                       19        34
 cbss.IdentifyPersonRequest     cbss.IdentifyPersonRequests     21        5
 cbss.ManageAccessRequest       cbss.ManageAccessRequests       24        1
 cbss.Purpose                   cbss.Purposes                   7         106
 cbss.RetrieveTIGroupsRequest   cbss.RetrieveTIGroupsRequests   15        3
 cbss.Sector                    cbss.Sectors                    11        209
 changes.Change                 changes.Changes                 9         0
 contacts.Company               contacts.Companies              28        39
 contacts.CompanyType           contacts.CompanyTypes           9         16
 contacts.Partner               contacts.Partners               24        162
 contacts.Person                contacts.Persons                31        109
 contacts.Role                  contacts.Roles                  4         10
 contacts.RoleType              contacts.RoleTypes              6         5
 contenttypes.ContentType       gfks.ContentTypes               3         128
 countries.Country              countries.Countries             9         270
 countries.Place                countries.Places                10        78
 courses.Course                 courses.Courses                 30        7
 courses.Enrolment              courses.Enrolments              13        100
 courses.Line                   courses.Lines                   21        7
 courses.Slot                   courses.Slots                   5         0
 courses.Topic                  courses.Topics                  5         0
 cv.Duration                    cv.Durations                    5         5
 cv.EducationLevel              cv.EducationLevels              8         5
 cv.Experience                  cv.Experiences                  17        30
 cv.Function                    cv.Functions                    7         4
 cv.LanguageKnowledge           cv.LanguageKnowledges           9         119
 cv.Obstacle                    cv.Obstacles                    6         20
 cv.ObstacleType                cv.ObstacleTypes                5         4
 cv.Proof                       cv.Proofs                       5         4
 cv.Regime                      cv.Regimes                      5         3
 cv.Sector                      cv.Sectors                      6         14
 cv.Skill                       cv.Skills                       6         0
 cv.SoftSkill                   cv.SoftSkills                   5         0
 cv.SoftSkillType               cv.SoftSkillTypes               5         0
 cv.Status                      cv.Statuses                     5         7
 cv.Study                       cv.Studies                      14        22
 cv.StudyType                   cv.StudyTypes                   8         11
 cv.Training                    cv.Trainings                    16        20
 excerpts.Excerpt               excerpts.Excerpts               12        69
 excerpts.ExcerptType           excerpts.ExcerptTypes           18        17
 fse.ClientSummary              fse.Summaries                   19        126
 gfks.HelpText                  gfks.HelpTexts                  4         5
 households.Household           households.Households           27        14
 households.Member              households.Members              14        63
 households.Type                households.Types                5         6
 humanlinks.Link                humanlinks.Links                4         59
 immersion.Contract             immersion.Contracts             25        6
 immersion.ContractType         immersion.ContractTypes         9         3
 immersion.Goal                 immersion.Goals                 5         4
 isip.Contract                  isip.Contracts                  22        30
 isip.ContractEnding            isip.ContractEndings            6         4
 isip.ContractPartner           isip.ContractPartners           6         35
 isip.ContractType              isip.ContractTypes              11        5
 isip.ExamPolicy                isip.ExamPolicies               20        6
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
 notes.EventType                notes.EventTypes                10        9
 notes.Note                     notes.Notes                     18        111
 notes.NoteType                 notes.NoteTypes                 12        13
 notifier.Notification          notifier.Notifications          7         0
 outbox.Attachment              outbox.Attachments              4         0
 outbox.Mail                    outbox.Mails                    9         0
 outbox.Recipient               outbox.Recipients               6         0
 pcsw.Activity                  pcsw.Activities                 3         0
 pcsw.AidType                   pcsw.AidTypes                   5         0
 pcsw.Client                    pcsw.Clients                    67        63
 pcsw.ClientContact             pcsw.ClientContacts             7         14
 pcsw.ClientContactType         pcsw.ClientContactTypes         6         10
 pcsw.Coaching                  pcsw.Coachings                  8         90
 pcsw.CoachingEnding            pcsw.CoachingEndings            7         0
 pcsw.CoachingType              pcsw.CoachingTypes              8         3
 pcsw.Conviction                pcsw.Convictions                5         0
 pcsw.Dispense                  pcsw.Dispenses                  6         0
 pcsw.DispenseReason            pcsw.DispenseReasons            6         0
 pcsw.Exclusion                 pcsw.Exclusions                 6         0
 pcsw.ExclusionType             pcsw.ExclusionTypes             2         2
 pcsw.PersonGroup               pcsw.PersonGroups               4         0
 plausibility.Problem           plausibility.Problems           6         0
 polls.AnswerChoice             polls.AnswerChoices             4         88
 polls.AnswerRemark             polls.AnswerRemarks             4         0
 polls.Choice                   polls.Choices                   7         35
 polls.ChoiceSet                polls.ChoiceSets                5         8
 polls.Poll                     polls.Polls                     11        2
 polls.Question                 polls.Questions                 9         38
 polls.Response                 polls.Responses                 7         6
 system.SiteConfig              system.SiteConfigs              26        1
 tinymce.TextFieldTemplate      tinymce.TextFieldTemplates      5         2
 uploads.Upload                 uploads.Uploads                 17        11
 uploads.UploadType             uploads.UploadTypes             11        9
 users.Authority                users.Authorities               3         3
 users.User                     users.Users                     21        10
============================== =============================== ========= =======
<BLANKLINE>


User profiles
=============

We use the user profiles defined in
:mod:`lino_welfare.modlib.welfare.roles`:

>>> settings.SITE.user_profiles_module
'lino_welfare.modlib.welfare.roles'
>>> rt.show(users.UserProfiles)
======= =========== ============================================
 value   name        text
------- ----------- --------------------------------------------
 000     anonymous   Anonyme
 100                 Agent d'insertion
 110                 Agent d'insertion (chef de service)
 120                 Agent d'insertion (nouveaux bénéficiaires)
 200                 Consultant nouveaux bénéficiaires
 210                 Agent d'accueil
 220                 Agent d'accueil (nouveaux bénéficiaires)
 300                 Médiateur de dettes
 400                 Agent social
 410                 Agent social (Chef de service)
 500                 Comptable
 510                 Accountant (Manager)
 800                 Supervisor
 900     admin       Administrateur
======= =========== ============================================
<BLANKLINE>

Remarques

- 120 et 220 sont utilisés dans des centres où il n'y a pas de 200
  spécialisé.


List of window layouts
======================

The following table lists information about all *data entry form
definitions* (called **window layouts**) used by Lino Welfare.  There
are *detail* layouts, *insert* layouts and *action parameter* layouts.

.. 
   >>> #settings.SITE.catch_layout_exceptions = False

Each window layout defines a given set of fields.


>>> print(analyzer.show_window_fields())
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
- about.About.show : server_status
- about.Models.detail : app, name, docstring, rows
- accounts.Accounts.detail : ref, group, type, id, name, name_nl, name_de, name_en, needs_partner, clearable
- accounts.Accounts.insert : ref, group, type, name, name_nl, name_de, name_en
- accounts.Groups.detail : ref, name, name_nl, name_de, name_en, account_type, id
- accounts.Groups.insert : name, name_nl, name_de, name_en, account_type, ref
- active_job_search.Proofs.insert : date, client, company, id, spontaneous, response, remarks
- addresses.Addresses.detail : country, city, zip_code, addr1, street, street_no, street_box, addr2, address_type, remark, data_source, partner
- addresses.Addresses.insert : country, city, street, street_no, street_box, address_type, remark
- aids.AidTypes.detail : id, short_name, confirmation_type, name, name_nl, name_de, name_en, excerpt_title, excerpt_title_nl, excerpt_title_de, excerpt_title_en, body_template, print_directly, is_integ_duty, is_urgent, confirmed_by_primary_coach, board, company, contact_person, contact_role, pharmacy_type
- aids.AidTypes.insert : name, name_nl, name_de, name_en, confirmation_type
- aids.Categories.insert : id, name, name_nl, name_de, name_en
- aids.Grantings.detail : id, client, user, signer, workflow_buttons, request_date, board, decision_date, aid_type, category, start_date, end_date, custom_actions
- aids.Grantings.insert : client, aid_type, signer, board, decision_date, start_date, end_date
- aids.GrantingsByClient.insert : aid_type, board, decision_date, start_date, end_date
- aids.IncomeConfirmations.insert : client, user, signer, workflow_buttons, printed, company, contact_person, language, granting, start_date, end_date, category, amount, id, remark
- aids.IncomeConfirmationsByGranting.insert : client, granting, start_date, end_date, category, amount, company, contact_person, language, remark
- aids.RefundConfirmations.insert : id, client, user, signer, workflow_buttons, granting, start_date, end_date, doctor_type, doctor, pharmacy, company, contact_person, language, printed, remark
- aids.RefundConfirmationsByGranting.insert : start_date, end_date, doctor_type, doctor, pharmacy, company, contact_person, language, printed, remark
- aids.SimpleConfirmations.insert : id, client, user, signer, workflow_buttons, granting, start_date, end_date, company, contact_person, language, printed, remark
- aids.SimpleConfirmationsByGranting.insert : start_date, end_date, company, contact_person, language, remark
- art61.ContractTypes.insert : id, name, name_nl, name_de, name_en, ref
- art61.Contracts.detail : id, client, user, language, type, company, contact_person, contact_role, applies_from, duration, applies_until, exam_policy, job_title, status, cv_duration, regime, reference_person, printed, date_decided, date_issued, date_ended, ending, subsidize_10, subsidize_20, subsidize_30, subsidize_40, subsidize_50, responsibilities
- art61.Contracts.insert : client, company, type
- boards.Boards.detail : id, name, name_nl, name_de, name_en
- boards.Boards.insert : name, name_nl, name_de, name_en
- cal.Calendars.detail : name, name_nl, name_de, name_en, color, id, description
- cal.Calendars.insert : name, name_nl, name_de, name_en, color
- cal.EventTypes.detail : name, name_nl, name_de, name_en, event_label, event_label_nl, event_label_de, event_label_en, max_conflicting, all_rooms, locks_user, id, invite_client, is_appointment, email_template, attach_to_email
- cal.EventTypes.insert : name, name_nl, name_de, name_en, invite_client
- cal.Events.detail : event_type, summary, project, start_date, start_time, end_date, end_time, user, assigned_to, room, priority, access_class, transparent, owner, workflow_buttons, description, id, created, modified, state
- cal.Events.insert : summary, start_date, start_time, end_date, end_time, event_type, project
- cal.EventsByClient.insert : event_type, summary, start_date, start_time, end_date, end_time
- cal.GuestRoles.insert : id, name, name_nl, name_de, name_en
- cal.GuestStates.wf1 : notify_subject, notify_body, notify_silent
- cal.GuestStates.wf2 : notify_subject, notify_body, notify_silent
- cal.Guests.checkin : notify_subject, notify_body, notify_silent
- cal.Guests.detail : event, partner, role, state, remark, workflow_buttons, waiting_since, busy_since, gone_since
- cal.Guests.insert : event, partner, role
- cal.RecurrentEvents.detail : name, name_nl, name_de, name_en, id, user, event_type, start_date, start_time, end_date, end_time, every_unit, every, max_events, monday, tuesday, wednesday, thursday, friday, saturday, sunday, description
- cal.RecurrentEvents.insert : name, name_nl, name_de, name_en, start_date, end_date, every_unit, event_type
- cal.Rooms.insert : id, name, name_nl, name_de, name_en
- cal.Tasks.detail : start_date, due_date, id, workflow_buttons, summary, project, user, delegated, owner, created, modified, description
- cal.Tasks.insert : summary, user, project
- cal.TasksByController.insert : summary, start_date, due_date, user, delegated
- cbss.IdentifyPersonRequests.detail : id, person, user, sent, status, printed, national_id, first_name, middle_name, last_name, birth_date, tolerance, gender, environment, ticket, response_xml, info_messages, debug_messages
- cbss.IdentifyPersonRequests.insert : person, national_id, first_name, middle_name, last_name, birth_date, tolerance, gender
- cbss.ManageAccessRequests.detail : id, person, user, sent, status, printed, action, start_date, end_date, purpose, query_register, national_id, sis_card_no, id_card_no, first_name, last_name, birth_date, result, environment, ticket, response_xml, info_messages, debug_messages
- cbss.ManageAccessRequests.insert : person, action, start_date, end_date, purpose, query_register, national_id, sis_card_no, id_card_no, first_name, last_name, birth_date
- cbss.RetrieveTIGroupsRequests.detail : id, person, user, sent, status, printed, national_id, language, history, environment, ticket, response_xml, info_messages, debug_messages
- cbss.RetrieveTIGroupsRequests.insert : person, national_id, language, history
- changes.Changes.detail : time, user, type, master, object, id, diff
- contacts.Companies.detail : overview, prefix, name, type, vat_id, client_contact_type, url, email, phone, gsm, fax, remarks, id, language, activity, is_obsolete, created, modified
- contacts.Companies.insert : name, language, email, type, id
- contacts.Companies.merge_row : merge_to, reason
- contacts.Partners.detail : overview, id, language, activity, client_contact_type, url, email, phone, gsm, fax, country, region, city, zip_code, addr1, street_prefix, street, street_no, street_box, addr2, remarks, is_obsolete, created, modified
- contacts.Partners.insert : name, language, email
- contacts.Persons.create_household : partner, type, head
- contacts.Persons.detail : overview, title, first_name, middle_name, last_name, gender, birth_date, age, id, language, email, phone, gsm, fax, MembersByPerson, LinksByHuman, remarks, activity, url, client_contact_type, is_obsolete, created, modified
- contacts.Persons.insert : first_name, last_name, gender, language
- countries.Countries.detail : isocode, name, name_nl, name_de, name_en, short_code, inscode, actual_country
- countries.Countries.insert : isocode, inscode, name, name_nl, name_de, name_en
- countries.Places.insert : name, name_nl, name_de, name_en, country, type, parent, zip_code, id
- countries.Places.merge_row : merge_to, reason
- courses.Courses.detail : line, teacher, start_date, end_date, start_time, end_time, enrolments_until, room, workflow_buttons, id, user, description, description_nl, description_de, description_en, max_places, max_events, max_date, every_unit, every, monday, tuesday, wednesday, thursday, friday, saturday, sunday
- courses.Courses.insert : start_date, line, teacher
- courses.Enrolments.detail : request_date, user, course, pupil, remark, workflow_buttons, printed, motivation, problems
- courses.Enrolments.insert : request_date, user, course, pupil, remark
- courses.EnrolmentsByCourse.insert : pupil, places, option, remark, request_date, user
- courses.EnrolmentsByPupil.insert : course, places, option, remark, request_date, user
- courses.Lines.detail : id, name, name_nl, name_de, name_en, ref, topic, fees_cat, tariff, options_cat, body_template, event_type, guest_role, every_unit, every, description, description_nl, description_de, description_en, excerpt_title, excerpt_title_nl, excerpt_title_de, excerpt_title_en
- courses.Lines.insert : name, name_nl, name_de, name_en, ref, topic, every_unit, every, event_type, description, description_nl, description_de, description_en
- courses.Slots.detail : name, start_time, end_time
- courses.Slots.insert : start_time, end_time, name
- courses.Topics.insert : id, name, name_nl, name_de, name_en
- cv.Durations.insert : id, name, name_nl, name_de, name_en
- cv.EducationLevels.insert : name, name_nl, name_de, name_en, is_study, is_training
- cv.Experiences.insert : person, start_date, end_date, termination_reason, company, country, city, sector, function, title, status, duration, regime, is_training, remarks
- cv.Functions.insert : id, name, name_nl, name_de, name_en, sector, remark
- cv.Regimes.insert : id, name, name_nl, name_de, name_en
- cv.Sectors.insert : id, name, name_nl, name_de, name_en, remark
- cv.Statuses.insert : id, name, name_nl, name_de, name_en
- cv.Studies.insert : person, start_date, end_date, type, content, education_level, state, school, country, city, remarks
- cv.StudyTypes.detail : name, name_nl, name_de, name_en, id, education_level, is_study, is_training
- cv.StudyTypes.insert : name, name_nl, name_de, name_en, is_study, is_training, education_level
- cv.Trainings.detail : person, start_date, end_date, type, state, certificates, sector, function, school, country, city, remarks
- cv.Trainings.insert : person, start_date, end_date, type, state, certificates, sector, function, school, country, city
- excerpts.ExcerptTypes.detail : id, name, name_nl, name_de, name_en, content_type, build_method, template, body_template, email_template, shortcut, primary, print_directly, certifying, print_recipient, backward_compat, attach_to_email
- excerpts.ExcerptTypes.insert : name, name_nl, name_de, name_en, content_type, primary, certifying, build_method, template, body_template
- excerpts.Excerpts.detail : id, excerpt_type, project, user, build_method, company, contact_person, language, owner, build_time, body_template_content
- fse.Summaries.detail : master, year, month, children_at_charge, certified_handicap, other_difficulty, id, education_level, result, remark, results
- fse.Summaries.insert : master, education_level, result, remark
- fse.SummariesByClient.insert : education_level, result, remark
- gfks.ContentTypes.insert : id, app_label, model, base_classes
- households.Households.detail : type, prefix, name, id
- households.HouseholdsByType.detail : type, name, language, id, country, region, city, zip_code, street_prefix, street, street_no, street_box, addr2, phone, gsm, email, url, remarks
- households.Types.insert : name, name_nl, name_de, name_en
- humanlinks.Links.insert : parent, child, type
- immersion.ContractTypes.detail : id, name, name_nl, name_de, name_en, exam_policy, template, overlap_group, full_name
- immersion.ContractTypes.insert : name, name_nl, name_de, name_en, exam_policy
- immersion.Contracts.detail : id, client, user, language, type, goal, company, contact_person, contact_role, applies_from, applies_until, exam_policy, sector, function, reference_person, printed, date_decided, date_issued, date_ended, ending, responsibilities
- immersion.Contracts.insert : client, company, type, goal
- immersion.Goals.insert : id, name, name_nl, name_de, name_en
- integ.ActivityReport.show : body
- isip.ContractEndings.insert : name, use_in_isip, use_in_jobs, is_success, needs_date_ended
- isip.ContractPartners.insert : company, contact_person, contact_role, duties_company
- isip.ContractTypes.insert : id, ref, exam_policy, needs_study_type, name, name_nl, name_de, name_en, full_name
- isip.Contracts.detail : id, client, type, user, user_asd, study_type, applies_from, applies_until, exam_policy, language, date_decided, date_issued, printed, date_ended, ending, stages, goals, duties_asd, duties_dsbe, duties_person
- isip.Contracts.insert : client, type
- isip.ExamPolicies.insert : id, name, name_nl, name_de, name_en, max_events, every, every_unit, event_type, monday, tuesday, wednesday, thursday, friday, saturday, sunday
- jobs.ContractTypes.insert : id, name, name_nl, name_de, name_en, ref
- jobs.Contracts.detail : id, client, user, user_asd, language, job, type, company, contact_person, contact_role, applies_from, duration, applies_until, exam_policy, regime, schedule, hourly_rate, refund_rate, reference_person, remark, printed, date_decided, date_issued, date_ended, ending, responsibilities
- jobs.Contracts.insert : client, job
- jobs.JobProviders.detail : overview, prefix, name, type, vat_id, client_contact_type, url, email, phone, gsm, fax
- jobs.JobTypes.insert : id, name, is_social
- jobs.Jobs.insert : name, provider, contract_type, type, id, sector, function, capacity, hourly_rate, remark
- jobs.JobsOverview.show : preview
- jobs.Offers.insert : name, provider, sector, function, selection_from, selection_until, start_date, remark
- jobs.Schedules.insert : id, name, name_nl, name_de, name_en
- languages.Languages.insert : id, iso2, name, name_nl, name_de, name_en
- newcomers.AvailableCoachesByClient.assign_coach : notify_subject, notify_body, notify_silent
- newcomers.Faculties.detail : id, name, name_nl, name_de, name_en, weight
- newcomers.Faculties.insert : name, name_nl, name_de, name_en, weight
- notes.EventTypes.insert : id, name, name_nl, name_de, name_en, remark
- notes.NoteTypes.detail : id, name, name_nl, name_de, name_en, build_method, template, special_type, email_template, attach_to_email, remark
- notes.NoteTypes.insert : name, name_nl, name_de, name_en, build_method
- notes.Notes.detail : date, time, event_type, type, project, subject, important, company, contact_person, user, language, build_time, id, body, UploadsByController
- notes.Notes.insert : event_type, type, subject, project
- notifier.Notifications.insert : overview
- outbox.Mails.detail : subject, project, date, user, sent, id, owner, AttachmentsByMail, UploadsByController, body
- outbox.Mails.insert : project, subject, body
- pcsw.ClientContactTypes.insert : id, name, name_nl, name_de, name_en
- pcsw.ClientStates.wf1 : reason, remark
- pcsw.Clients.create_visit : user, summary
- pcsw.Clients.detail : overview, gender, id, nationality, last_name, first_name, middle_name, birth_date, age, language, email, phone, fax, gsm, image, national_id, civil_state, birth_country, birth_place, declared_name, needs_residence_permit, needs_work_permit, in_belgium_since, residence_type, residence_until, group, aid_type, AgentsByClient, workflow_buttons, id_document, faculty, MembersByPerson, child_custody, LinksByHuman, skills, obstacles, is_seeking, unemployed_since, seeking_since, work_permit_suspended_until, ResponsesByPartner, ExcerptsByProject, activity, client_state, noble_condition, unavailable_until, unavailable_why, is_obsolete, created, modified, remarks
- pcsw.Clients.insert : first_name, last_name, national_id, gender, language
- pcsw.Clients.merge_row : merge_to, aids_IncomeConfirmation, aids_RefundConfirmation, aids_SimpleConfirmation, pcsw_Coaching, pcsw_Dispense, reason
- pcsw.CoachingEndings.insert : id, name, name_nl, name_de, name_en, seqno
- pcsw.Coachings.create_visit : user, summary
- plausibility.Checkers.detail : value, name, text
- plausibility.Problems.detail : user, owner, checker, id, message
- polls.AnswerRemarks.insert : remark, response, question
- polls.ChoiceSets.insert : name, name_nl, name_de, name_en
- polls.Polls.detail : ref, title, workflow_buttons, details, default_choiceset, default_multiple_choices, id, user, created, modified, state
- polls.Polls.insert : ref, title, default_choiceset, default_multiple_choices, questions_to_add
- polls.Questions.insert : poll, number, is_heading, choiceset, multiple_choices, title, details
- polls.Responses.detail : poll, partner, date, workflow_buttons, AnswersByResponse, user, state, remark
- polls.Responses.insert : user, date, poll
- reception.BusyVisitors.detail : event, client, role, state, remark, workflow_buttons
- reception.GoneVisitors.detail : event, client, role, state, remark, workflow_buttons
- reception.MyWaitingVisitors.detail : event, client, role, state, remark, workflow_buttons
- reception.WaitingVisitors.detail : event, client, role, state, remark, workflow_buttons
- system.SiteConfigs.detail : site_company, next_partner_id, job_office, signer1, signer2, signer1_function, signer2_function, system_note_type, default_build_method, propgroup_skills, propgroup_softskills, propgroup_obstacles, residence_permit_upload_type, work_permit_upload_type, driving_licence_upload_type, default_event_type, prompt_calendar, client_guestrole, team_guestrole, cbss_org_unit, sector, ssdn_user_id, ssdn_email, cbss_http_username, cbss_http_password
- tinymce.TextFieldTemplates.detail : id, name, user, description, text
- tinymce.TextFieldTemplates.insert : name, user
- uploads.AllUploads.detail : file, user, upload_area, type, description, owner
- uploads.AllUploads.insert : type, description, file, user
- uploads.UploadTypes.detail : id, upload_area, shortcut, name, name_nl, name_de, name_en, warn_expiry_unit, warn_expiry_value, wanted, max_number
- uploads.UploadTypes.insert : upload_area, name, name_nl, name_de, name_en, warn_expiry_unit, warn_expiry_value
- uploads.Uploads.detail : user, project, id, type, description, start_date, end_date, needed, company, contact_person, contact_role, file, owner, remark
- uploads.Uploads.insert : type, file, start_date, end_date, description
- uploads.UploadsByClient.insert : file, type, end_date, description
- uploads.UploadsByController.insert : file, type, end_date, description
- users.Users.change_password : current, new1, new2
- users.Users.detail : username, profile, partner, first_name, last_name, initials, email, language, timezone, id, created, modified, remarks, event_type, access_class, calendar, newcomer_quota, coaching_type, coaching_supervisor, newcomer_consultations, newcomer_appointments
- users.Users.insert : username, email, first_name, last_name, partner, language, profile
<BLANKLINE>



Windows and permissions
=======================

Each window layout is **viewable** by a given set of user profiles.

>>> print(analyzer.show_window_permissions())
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
- about.About.show : visible for all
- about.Models.detail : visible for 100 110 120 200 210 220 300 400 410 500 510 800 admin
- accounts.Accounts.detail : visible for 510 admin
- accounts.Accounts.insert : visible for 510 admin
- accounts.Groups.detail : visible for 510 admin
- accounts.Groups.insert : visible for 510 admin
- active_job_search.Proofs.insert : visible for 110 admin
- addresses.Addresses.detail : visible for admin
- addresses.Addresses.insert : visible for admin
- aids.AidTypes.detail : visible for 110 210 220 410 500 510 800 admin
- aids.AidTypes.insert : visible for 110 210 220 410 500 510 800 admin
- aids.Categories.insert : visible for 110 210 220 410 500 510 800 admin
- aids.Grantings.detail : visible for 100 110 120 200 210 220 300 400 410 500 510 800 admin
- aids.Grantings.insert : visible for 100 110 120 200 210 220 300 400 410 500 510 800 admin
- aids.GrantingsByClient.insert : visible for 100 110 120 200 210 220 300 400 410 500 510 800 admin
- aids.IncomeConfirmations.insert : visible for 100 110 120 200 210 220 300 400 410 500 510 800 admin
- aids.IncomeConfirmationsByGranting.insert : visible for 100 110 120 200 210 220 300 400 410 500 510 800 admin
- aids.RefundConfirmations.insert : visible for 100 110 120 200 210 220 300 400 410 500 510 800 admin
- aids.RefundConfirmationsByGranting.insert : visible for 100 110 120 200 210 220 300 400 410 500 510 800 admin
- aids.SimpleConfirmations.insert : visible for 100 110 120 200 210 220 300 400 410 500 510 800 admin
- aids.SimpleConfirmationsByGranting.insert : visible for 100 110 120 200 210 220 300 400 410 500 510 800 admin
- art61.ContractTypes.insert : visible for 110 admin
- art61.Contracts.detail : visible for 100 110 120 admin
- art61.Contracts.insert : visible for 100 110 120 admin
- boards.Boards.detail : visible for admin
- boards.Boards.insert : visible for admin
- cal.Calendars.detail : visible for 110 410 admin
- cal.Calendars.insert : visible for 110 410 admin
- cal.EventTypes.detail : visible for 110 410 admin
- cal.EventTypes.insert : visible for 110 410 admin
- cal.Events.detail : visible for 110 410 admin
- cal.Events.insert : visible for 110 410 admin
- cal.EventsByClient.insert : visible for 100 110 120 200 300 400 410 500 510 admin
- cal.GuestRoles.insert : visible for admin
- cal.GuestStates.wf1 : visible for admin
- cal.GuestStates.wf2 : visible for admin
- cal.Guests.checkin : visible for admin
- cal.Guests.detail : visible for admin
- cal.Guests.insert : visible for admin
- cal.RecurrentEvents.detail : visible for 110 410 admin
- cal.RecurrentEvents.insert : visible for 110 410 admin
- cal.Rooms.insert : visible for 110 410 admin
- cal.Tasks.detail : visible for 110 410 admin
- cal.Tasks.insert : visible for 110 410 admin
- cal.TasksByController.insert : visible for 100 110 120 200 300 400 410 500 510 admin
- cbss.IdentifyPersonRequests.detail : visible for 100 110 120 200 210 220 300 400 410 admin
- cbss.IdentifyPersonRequests.insert : visible for 100 110 120 200 210 220 300 400 410 admin
- cbss.ManageAccessRequests.detail : visible for 100 110 120 200 210 220 300 400 410 admin
- cbss.ManageAccessRequests.insert : visible for 100 110 120 200 210 220 300 400 410 admin
- cbss.RetrieveTIGroupsRequests.detail : visible for 100 110 120 200 210 220 300 400 410 admin
- cbss.RetrieveTIGroupsRequests.insert : visible for 100 110 120 200 210 220 300 400 410 admin
- changes.Changes.detail : visible for admin
- contacts.Companies.detail : visible for 100 110 120 200 210 220 300 400 410 500 510 800 admin
- contacts.Companies.insert : visible for 100 110 120 200 210 220 300 400 410 500 510 800 admin
- contacts.Companies.merge_row : visible for 110 210 220 410 800 admin
- contacts.Partners.detail : visible for 100 110 120 200 210 220 300 400 410 500 510 800 admin
- contacts.Partners.insert : visible for 100 110 120 200 210 220 300 400 410 500 510 800 admin
- contacts.Persons.create_household : visible for 100 110 120 200 210 220 300 400 410 500 510 800 admin
- contacts.Persons.detail : visible for 100 110 120 200 210 220 300 400 410 500 510 800 admin
- contacts.Persons.insert : visible for 100 110 120 200 210 220 300 400 410 500 510 800 admin
- countries.Countries.detail : visible for 100 110 120 200 210 220 300 400 410 500 510 800 admin
- countries.Countries.insert : visible for 100 110 120 200 210 220 300 400 410 500 510 800 admin
- countries.Places.insert : visible for 110 210 220 410 800 admin
- countries.Places.merge_row : visible for 110 210 220 410 800 admin
- courses.Courses.detail : visible for 100 110 120 200 210 220 300 400 410 500 510 800 admin
- courses.Courses.insert : visible for 100 110 120 200 210 220 300 400 410 500 510 800 admin
- courses.Enrolments.detail : visible for admin
- courses.Enrolments.insert : visible for admin
- courses.EnrolmentsByCourse.insert : visible for 100 110 120 200 210 220 300 400 410 500 510 800 admin
- courses.EnrolmentsByPupil.insert : visible for 100 110 120 200 210 220 300 400 410 500 510 800 admin
- courses.Lines.detail : visible for 100 110 120 200 210 220 300 400 410 500 510 800 admin
- courses.Lines.insert : visible for 100 110 120 200 210 220 300 400 410 500 510 800 admin
- courses.Slots.detail : visible for admin
- courses.Slots.insert : visible for admin
- courses.Topics.insert : visible for admin
- cv.Durations.insert : visible for 110 admin
- cv.EducationLevels.insert : visible for 110 admin
- cv.Experiences.insert : visible for 110 admin
- cv.Functions.insert : visible for 110 admin
- cv.Regimes.insert : visible for 110 admin
- cv.Sectors.insert : visible for 110 admin
- cv.Statuses.insert : visible for 110 admin
- cv.Studies.insert : visible for 110 admin
- cv.StudyTypes.detail : visible for 110 admin
- cv.StudyTypes.insert : visible for 110 admin
- cv.Trainings.detail : visible for 100 110 120 200 210 220 300 400 410 500 510 800 admin
- cv.Trainings.insert : visible for 100 110 120 200 210 220 300 400 410 500 510 800 admin
- excerpts.ExcerptTypes.detail : visible for admin
- excerpts.ExcerptTypes.insert : visible for admin
- excerpts.Excerpts.detail : visible for 100 110 120 200 210 220 300 400 410 500 510 800 admin
- fse.Summaries.detail : visible for 100 110 120 200 210 220 300 400 410 500 510 800 admin
- fse.Summaries.insert : visible for 100 110 120 200 210 220 300 400 410 500 510 800 admin
- fse.SummariesByClient.insert : visible for 100 110 120 200 210 220 300 400 410 500 510 800 admin
- gfks.ContentTypes.insert : visible for admin
- households.Households.detail : visible for 100 110 120 200 210 220 300 400 410 500 510 800 admin
- households.HouseholdsByType.detail : visible for 100 110 120 200 210 220 300 400 410 500 510 800 admin
- households.Types.insert : visible for 110 210 220 410 800 admin
- humanlinks.Links.insert : visible for 110 210 220 410 800 admin
- immersion.ContractTypes.detail : visible for 110 admin
- immersion.ContractTypes.insert : visible for 110 admin
- immersion.Contracts.detail : visible for 100 110 120 admin
- immersion.Contracts.insert : visible for 100 110 120 admin
- immersion.Goals.insert : visible for 110 admin
- integ.ActivityReport.show : visible for 100 110 120 admin
- isip.ContractEndings.insert : visible for 110 410 admin
- isip.ContractPartners.insert : visible for 110 admin
- isip.ContractTypes.insert : visible for 110 410 admin
- isip.Contracts.detail : visible for 100 110 120 admin
- isip.Contracts.insert : visible for 100 110 120 admin
- isip.ExamPolicies.insert : visible for 110 410 admin
- jobs.ContractTypes.insert : visible for 110 410 admin
- jobs.Contracts.detail : visible for 100 110 120 admin
- jobs.Contracts.insert : visible for 100 110 120 admin
- jobs.JobProviders.detail : visible for 100 110 120 admin
- jobs.JobTypes.insert : visible for 110 410 admin
- jobs.Jobs.insert : visible for 100 110 120 admin
- jobs.JobsOverview.show : visible for 100 110 120 admin
- jobs.Offers.insert : visible for 100 110 120 admin
- jobs.Schedules.insert : visible for 110 410 admin
- languages.Languages.insert : visible for 100 110 120 200 300 400 410 500 510 admin
- newcomers.AvailableCoachesByClient.assign_coach : visible for 110 120 200 220 300 800 admin
- newcomers.Faculties.detail : visible for 110 410 admin
- newcomers.Faculties.insert : visible for 110 410 admin
- notes.EventTypes.insert : visible for 110 410 admin
- notes.NoteTypes.detail : visible for 110 410 admin
- notes.NoteTypes.insert : visible for 110 410 admin
- notes.Notes.detail : visible for 100 110 120 200 210 220 300 400 410 500 510 800 admin
- notes.Notes.insert : visible for 100 110 120 200 210 220 300 400 410 500 510 800 admin
- notifier.Notifications.insert : visible for 100 110 120 200 210 220 300 400 410 500 510 800 admin
- outbox.Mails.detail : visible for 110 410 admin
- outbox.Mails.insert : visible for 110 410 admin
- pcsw.ClientContactTypes.insert : visible for 110 410 admin
- pcsw.ClientStates.wf1 : visible for 200 300 admin
- pcsw.Clients.create_visit : visible for 100 110 120 200 210 220 300 400 410 500 510 800 admin
- pcsw.Clients.detail : visible for 100 110 120 200 210 220 300 400 410 500 510 800 admin
- pcsw.Clients.insert : visible for 100 110 120 200 210 220 300 400 410 500 510 800 admin
- pcsw.Clients.merge_row : visible for 110 210 220 410 800 admin
- pcsw.CoachingEndings.insert : visible for 110 410 admin
- pcsw.Coachings.create_visit : visible for 110 410 admin
- plausibility.Checkers.detail : visible for admin
- plausibility.Problems.detail : visible for 100 110 120 200 210 220 300 400 410 500 510 800 admin
- polls.AnswerRemarks.insert : visible for 100 110 120 200 300 400 410 admin
- polls.ChoiceSets.insert : visible for 110 410 admin
- polls.Polls.detail : visible for 100 110 120 200 300 400 410 admin
- polls.Polls.insert : visible for 100 110 120 200 300 400 410 admin
- polls.Questions.insert : visible for 110 410 admin
- polls.Responses.detail : visible for 100 110 120 200 300 400 410 admin
- polls.Responses.insert : visible for 100 110 120 200 300 400 410 admin
- reception.BusyVisitors.detail : visible for 100 110 120 200 210 220 300 400 410 500 510 800 admin
- reception.GoneVisitors.detail : visible for 100 110 120 200 210 220 300 400 410 500 510 800 admin
- reception.MyWaitingVisitors.detail : visible for 100 110 120 200 300 400 410 500 510 admin
- reception.WaitingVisitors.detail : visible for 100 110 120 200 210 220 300 400 410 500 510 800 admin
- system.SiteConfigs.detail : visible for admin
- tinymce.TextFieldTemplates.detail : visible for admin
- tinymce.TextFieldTemplates.insert : visible for admin
- uploads.AllUploads.detail : visible for 110 410 admin
- uploads.AllUploads.insert : visible for 110 410 admin
- uploads.UploadTypes.detail : visible for 110 410 admin
- uploads.UploadTypes.insert : visible for 110 410 admin
- uploads.Uploads.detail : visible for 100 110 120 200 210 220 300 400 410 500 510 800 admin
- uploads.Uploads.insert : visible for 100 110 120 200 210 220 300 400 410 500 510 800 admin
- uploads.UploadsByClient.insert : visible for 100 110 120 200 210 220 300 400 410 500 510 800 admin
- uploads.UploadsByController.insert : visible for 100 110 120 200 210 220 300 400 410 500 510 800 admin
- users.Users.change_password : visible for admin
- users.Users.detail : visible for admin
- users.Users.insert : visible for admin
<BLANKLINE>


The main menu
=============

Romain
------

>>> rt.login('romain').show_menu()
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
- Contacts : Personnes,  ▶ Bénéficiaires, Organisations, -, Partenaires (tous), Ménages
- Office : Mes téléchargements à renouveler, Mes Fichiers téléchargés, Mon courrier sortant, Mes Extraits, Mes Observations, Mes problèmes de données
- Calendrier : Calendrier, Mes rendez-vous, Mes tâches, Mes visiteurs, Mes présences
- Réception : Bénéficiaires, Rendez-vous aujourd'hui, Salle d'attente, Visiteurs occupés, Visiteurs repartis, Visiteurs qui m'attendent
- CPAS : Bénéficiaires, Mes Interventions, Octrois à confirmer
- Intégration : Bénéficiaires, PIISs, Mises à l'emploi art60§7, Services utilisateurs, Postes de travail, Offres d'emploi, Mises à l'emploi art61, Stages d'immersion
- Ateliers : Ateliers en préparation, Ateliers actifs, Séries d'ateliers, Demandes d’inscription en attente, Demandes d’inscription confirmées
- Nouvelles demandes : Nouveaux bénéficiaires, Agents disponibles
- Questionnaires : Mes Questionnaires, Mes Interviews
- Rapports :
  - Système : Broken GFKs
  - Intégration : Agents et leurs clients, Situation contrats Art 60-7, Rapport d'activité
- Configuration :
  - Système : Paramètres du Site, Textes d'aide, Utilisateurs, Update all summary data
  - Endroits : Pays, Endroits
  - Contacts : Types d'organisation, Fonctions, Conseils, Types de ménage
  - Office : Types de fichiers téléchargés, Types d'extrait, Types d'observation, Types d'événements, Mes Text Field Templates
  - Calendrier : Calendriers, Locaux, Priorités, Recurrent event rules, Rôles de participants, Types d'entrée calendrier, Remote Calendars
  - Comptabilité : Groupes de comptes, Comptes
  - Ateliers : Savoirs de base, Topics, Timetable Slots
  - CPAS : Phases d'intégration, Activités, types d'exclusions, Services, Raisons d’arrêt d'intervention, Motifs de dispense, Types de contact client, Types d'aide sociale, Catégories 
  - Parcours : Langues, Types d'éducation, Niveaux académiques, Secteurs, Fonctions, Régimes de travail, Statuts, Types de contrat, Types de compétence sociale, Types de freins, Preuves de qualification
  - Intégration : Types de PIIS, Motifs d’arrêt de contrat, Régimes d'évaluation, Types de mise à l'emploi art60§7, Types de poste, Horaires, Types de mise à l'emploi art.61, Types de stage d'immersion, Objectifs
  - Nouvelles demandes : Intermédiaires, Spécificités
  - BCSS : Secteurs, Codes fonction
  - Questionnaires : Listes de choix
- Explorateur :
  - Système : types de contenu, Procurations, Profils d'utilisateur, Notifications, Changes, Tests de données, Problèmes de données
  - Contacts : Personnes de contact, Types d'adresses, Adresses, Membres du conseil, Household member roles, Membres de ménage, Personal Links, Type de parenté
  - Office : Fichiers téléchargés, Upload Areas, Mails envoyés, Pièces jointes, Extraits, Observations, Text Field Templates
  - Calendrier : Tâches, Participants, Abonnements, Event states, Guest states, Task states
  - Ateliers : Tests de niveau, Ateliers, Inscriptions, États d'inscription
  - CPAS : Interventions, Contacts client, Exclusions, Antécédents judiciaires, Bénéficiaires, Etats civils, Etats bénéficiaires, Type de carte eID, Octrois d'aide, Certificats de revenu, Refund confirmations, Confirmations simple
  - Parcours : Connaissances de langue, Formations, Études, Expériences professionnelles, Connaissances de langue, Compétences professionnelles, Compétences sociales, Freins
  - Intégration : PIISs, Mises à l'emploi art60§7, Candidatures, Services utilisateurs, Mises à l'emploi art61, Stages d'immersion, Preuves de recherche, FSE Summaries
  - Nouvelles demandes : Compétences
  - BCSS : Requêtes IdentifyPerson, Requêtes ManageAccess, Requêtes Tx25
  - Questionnaires : Questionnaires, Questions, Choix, Interviews, Choix de réponse, Answer Remarks
- Site : à propos

Theresia
--------

Theresia est un agent d'accueil. Elle ne voit pas les questionnaires,
les données de parcours, compétences professionnelles, compétences
sociales, freins.


>>> rt.login('theresia').show_menu()
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
- Contacts : Personnes,  ▶ Bénéficiaires, Organisations, -, Partenaires (tous), Ménages
- Office : Mes téléchargements à renouveler, Mes Fichiers téléchargés, Mes Extraits, Mes Observations
- Réception : Bénéficiaires, Rendez-vous aujourd'hui, Salle d'attente, Visiteurs occupés, Visiteurs repartis
- Ateliers : Ateliers en préparation, Ateliers actifs, Séries d'ateliers
- Configuration :
  - Endroits : Pays, Endroits
  - Contacts : Types d'organisation, Fonctions, Types de ménage
  - CPAS : Types d'aide sociale, Catégories
- Explorateur :
  - Contacts : Personnes de contact, Household member roles, Membres de ménage, Personal Links, Type de parenté
  - Ateliers : Ateliers
  - CPAS : Octrois d'aide, Certificats de revenu, Refund confirmations, Confirmations simple
- Site : à propos
