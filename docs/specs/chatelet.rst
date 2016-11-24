.. _welfare.specs.chatelet:

==========================
Lino Welfare à la Châtelet
==========================

.. How to test only this document:

    $ python setup.py test -s tests.SpecsTests.test_chatelet

    doctest init:

    >>> from lino import startup
    >>> startup('lino_welfare.projects.chatelet.settings.doctests')
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

>>> print(' '.join([lng.name for lng in settings.SITE.languages]))
fr nl de en

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
59 apps: lino_startup, staticfiles, about, jinja, bootstrap3, extjs, printing, system, office, countries, contacts, appypod, humanize, users, contenttypes, gfks, channels, notify, changes, addresses, uploads, outbox, xl, excerpts, extensible, cal, reception, cosi, accounts, badges, boards, welfare, sales, pcsw, languages, cv, integ, isip, jobs, art61, immersion, active_job_search, courses, newcomers, cbss, households, humanlinks, debts, notes, aids, polls, summaries, weasyprint, esf, beid, davlink, export_excel, plausibility, tinymce.
132 models:
============================== =============================== ========= =======
 Name                           Default table                   #fields   #rows
------------------------------ ------------------------------- --------- -------
 accounts.Account               accounts.Accounts               12        0
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
 cal.Calendar                   cal.Calendars                   7         12
 cal.Event                      cal.OneEvent                    24        586
 cal.EventType                  cal.EventTypes                  20        11
 cal.Guest                      cal.Guests                      9         570
 cal.GuestRole                  cal.GuestRoles                  5         4
 cal.Priority                   cal.Priorities                  6         4
 cal.RecurrentEvent             cal.RecurrentEvents             22        15
 cal.RemoteCalendar             cal.RemoteCalendars             7         0
 cal.Room                       cal.Rooms                       5         0
 cal.Subscription               cal.Subscriptions               4         9
 cal.Task                       cal.Tasks                       19        34
 cbss.IdentifyPersonRequest     cbss.IdentifyPersonRequests     21        5
 cbss.ManageAccessRequest       cbss.ManageAccessRequests       24        1
 cbss.Purpose                   cbss.Purposes                   7         106
 cbss.RetrieveTIGroupsRequest   cbss.RetrieveTIGroupsRequests   15        6
 cbss.Sector                    cbss.Sectors                    11        209
 changes.Change                 changes.Changes                 9         0
 contacts.Company               contacts.Companies              28        39
 contacts.CompanyType           contacts.CompanyTypes           9         16
 contacts.Partner               contacts.Partners               24        162
 contacts.Person                contacts.Persons                31        109
 contacts.Role                  contacts.Roles                  4         10
 contacts.RoleType              contacts.RoleTypes              6         5
 contenttypes.ContentType       gfks.ContentTypes               3         133
 countries.Country              countries.Countries             9         270
 countries.Place                countries.Places                10        78
 courses.Course                 courses.Activities              30        7
 courses.Enrolment              courses.Enrolments              15        100
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
 debts.Account                  debts.Accounts                  13        51
 debts.Actor                    debts.Actors                    6         63
 debts.Budget                   debts.Budgets                   11        14
 debts.Entry                    debts.Entries                   16        716
 debts.Group                    debts.Groups                    8         8
 esf.ClientSummary              esf.Summaries                   23        189
 excerpts.Excerpt               excerpts.Excerpts               12        70
 excerpts.ExcerptType           excerpts.ExcerptTypes           18        18
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
 notes.EventType                notes.EventTypes                10        10
 notes.Note                     notes.Notes                     18        111
 notes.NoteType                 notes.NoteTypes                 12        13
 notify.Message                 notify.Messages                 10        12
 outbox.Attachment              outbox.Attachments              4         0
 outbox.Mail                    outbox.Mails                    9         0
 outbox.Recipient               outbox.Recipients               6         0
 pcsw.Activity                  pcsw.Activities                 3         0
 pcsw.AidType                   pcsw.AidTypes                   5         0
 pcsw.Client                    pcsw.Clients                    67        63
 pcsw.ClientContact             pcsw.ClientContacts             7         14
 pcsw.ClientContactType         pcsw.ClientContactTypes         7         10
 pcsw.Coaching                  pcsw.Coachings                  8         90
 pcsw.CoachingEnding            pcsw.CoachingEndings            7         4
 pcsw.CoachingType              pcsw.CoachingTypes              8         3
 pcsw.Conviction                pcsw.Convictions                5         0
 pcsw.Dispense                  pcsw.Dispenses                  6         0
 pcsw.DispenseReason            pcsw.DispenseReasons            6         4
 pcsw.Exclusion                 pcsw.Exclusions                 6         0
 pcsw.ExclusionType             pcsw.ExclusionTypes             2         2
 pcsw.PersonGroup               pcsw.PersonGroups               4         5
 plausibility.Problem           plausibility.Problems           6         0
 polls.AnswerChoice             polls.AnswerChoices             4         88
 polls.AnswerRemark             polls.AnswerRemarks             4         0
 polls.Choice                   polls.Choices                   7         35
 polls.ChoiceSet                polls.ChoiceSets                5         8
 polls.Poll                     polls.Polls                     11        2
 polls.Question                 polls.Questions                 9         38
 polls.Response                 polls.Responses                 7         6
 system.SiteConfig              system.SiteConfigs              29        1
 tinymce.TextFieldTemplate      tinymce.TextFieldTemplates      5         2
 uploads.Upload                 uploads.Uploads                 17        11
 uploads.UploadType             uploads.UploadTypes             11        9
 users.Authority                users.Authorities               3         3
 users.User                     users.Users                     22        12
============================== =============================== ========= =======
<BLANKLINE>


User profiles
=============

We use the user profiles defined in
:mod:`lino_welfare.modlib.welfare.roles`:

>>> settings.SITE.user_types_module
'lino_welfare.modlib.welfare.roles'
>>> rt.show(users.UserTypes)
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
 910                 Security advisor
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
- accounts.Accounts.detail : ref, group, type, id, name, name_nl, name_de, name_en, needs_partner, clearable, default_amount
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
- art61.Contracts.detail : id, client, user, language, type, company, contact_person, contact_role, applies_from, duration, applies_until, exam_policy, job_title, status, cv_duration, regime, reference_person, remark, printed, date_decided, date_issued, date_ended, ending, subsidize_10, subsidize_20, subsidize_30, subsidize_40, subsidize_50, responsibilities
- art61.Contracts.insert : client, company, type
- boards.Boards.detail : id, name, name_nl, name_de, name_en
- boards.Boards.insert : name, name_nl, name_de, name_en
- cal.Calendars.detail : name, name_nl, name_de, name_en, color, id, description
- cal.Calendars.insert : name, name_nl, name_de, name_en, color
- cal.EventTypes.detail : name, name_nl, name_de, name_en, event_label, event_label_nl, event_label_de, event_label_en, max_conflicting, all_rooms, locks_user, esf_field, id, invite_client, is_appointment, email_template, attach_to_email
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
- cbss.IdentifyPersonRequests.detail : id, person, user, sent, status, printed, national_id, first_name, middle_name, last_name, birth_date, tolerance, gender, environment, ticket, info_messages, debug_messages
- cbss.IdentifyPersonRequests.insert : person, national_id, first_name, middle_name, last_name, birth_date, tolerance, gender
- cbss.ManageAccessRequests.detail : id, person, user, sent, status, printed, action, start_date, end_date, purpose, query_register, national_id, sis_card_no, id_card_no, first_name, last_name, birth_date, result, environment, ticket, info_messages, debug_messages
- cbss.ManageAccessRequests.insert : person, action, start_date, end_date, purpose, query_register, national_id, sis_card_no, id_card_no, first_name, last_name, birth_date
- cbss.RetrieveTIGroupsRequests.detail : id, person, user, sent, status, printed, national_id, language, history, environment, ticket, info_messages, debug_messages
- cbss.RetrieveTIGroupsRequests.insert : person, national_id, language, history
- changes.Changes.detail : time, user, type, master, object, id, diff
- contacts.Companies.detail : overview, prefix, name, type, vat_id, client_contact_type, url, email, phone, gsm, fax, remarks, id, language, activity, is_obsolete, created, modified
- contacts.Companies.insert : name, language, email, type, id
- contacts.Companies.merge_row : merge_to, addresses_Address, reason
- contacts.Partners.detail : overview, id, language, activity, client_contact_type, url, email, phone, gsm, fax, country, region, city, zip_code, addr1, street_prefix, street, street_no, street_box, addr2, remarks, is_obsolete, created, modified
- contacts.Partners.insert : name, language, email
- contacts.Persons.create_household : partner, type, head
- contacts.Persons.detail : overview, title, first_name, middle_name, last_name, gender, birth_date, age, id, language, email, phone, gsm, fax, MembersByPerson, LinksByHuman, remarks, activity, url, client_contact_type, is_obsolete, created, modified
- contacts.Persons.insert : first_name, last_name, gender, language
- countries.Countries.detail : isocode, name, name_nl, name_de, name_en, short_code, inscode, actual_country
- countries.Countries.insert : isocode, inscode, name, name_nl, name_de, name_en
- countries.Places.insert : name, name_nl, name_de, name_en, country, type, parent, zip_code, id
- countries.Places.merge_row : merge_to, reason
- courses.Activities.detail : line, teacher, start_date, end_date, start_time, end_time, enrolments_until, room, workflow_buttons, id, user, name, description, description_nl, description_de, description_en, max_places, max_events, max_date, every_unit, every, monday, tuesday, wednesday, thursday, friday, saturday, sunday, EnrolmentsByCourse
- courses.Activities.insert : start_date, line, teacher
- courses.Enrolments.detail : request_date, user, course, pupil, remark, workflow_buttons, printed, motivation, problems
- courses.Enrolments.insert : request_date, user, course, pupil, remark
- courses.EnrolmentsByCourse.insert : pupil, places, option, remark, request_date, user
- courses.EnrolmentsByPupil.insert : course_area, course, places, option, remark, request_date, user
- courses.Lines.detail : id, name, name_nl, name_de, name_en, ref, course_area, topic, fees_cat, fee, options_cat, body_template, event_type, guest_role, every_unit, every, description, description_nl, description_de, description_en, excerpt_title, excerpt_title_nl, excerpt_title_de, excerpt_title_en
- courses.Lines.insert : name, name_nl, name_de, name_en, ref, topic, every_unit, every, event_type, description, description_nl, description_de, description_en
- courses.Slots.detail : name, start_time, end_time
- courses.Slots.insert : start_time, end_time, name
- courses.Topics.insert : id, name, name_nl, name_de, name_en
- cv.Durations.insert : id, name, name_nl, name_de, name_en
- cv.EducationLevels.insert : name, name_nl, name_de, name_en, is_study, is_training
- cv.Experiences.insert : person, start_date, end_date, termination_reason, company, country, city, sector, function, title, status, duration, regime, is_training, remarks
- cv.ExperiencesByPerson.insert : start_date, end_date, company, function  
- cv.Functions.insert : id, name, name_nl, name_de, name_en, sector, remark
- cv.Regimes.insert : id, name, name_nl, name_de, name_en
- cv.Sectors.insert : id, name, name_nl, name_de, name_en, remark
- cv.Statuses.insert : id, name, name_nl, name_de, name_en
- cv.Studies.insert : person, start_date, end_date, type, content, education_level, state, school, country, city, remarks
- cv.StudiesByPerson.insert : start_date, end_date, type, content  
- cv.StudyTypes.detail : name, name_nl, name_de, name_en, id, education_level, is_study, is_training
- cv.StudyTypes.insert : name, name_nl, name_de, name_en, is_study, is_training, education_level
- cv.Trainings.detail : person, start_date, end_date, type, state, certificates, sector, function, school, country, city, remarks
- cv.Trainings.insert : person, start_date, end_date, type, state, certificates, sector, function, school, country, city
- debts.Accounts.detail : ref, name, name_nl, name_de, name_en, group, type, required_for_household, required_for_person, periods, default_amount
- debts.Accounts.insert : ref, group, type, name, name_nl, name_de, name_en
- debts.Budgets.detail : date, partner, id, user, intro, ResultByBudget, DebtsByBudget, AssetsByBudgetSummary, conclusion, dist_amount, printed, total_debt, include_yearly_incomes, print_empty_rows, print_todos, DistByBudget, data_box, summary_box
- debts.Budgets.insert : partner, date, user
- debts.Groups.detail : ref, name, name_nl, name_de, name_en, id, account_type, entries_layout
- debts.Groups.insert : name, name_nl, name_de, name_en, account_type, ref
- esf.Summaries.detail : master, year, month, children_at_charge, certified_handicap, other_difficulty, id, education_level, result, remark, results
- excerpts.ExcerptTypes.detail : id, name, name_nl, name_de, name_en, content_type, build_method, template, body_template, email_template, shortcut, primary, print_directly, certifying, print_recipient, backward_compat, attach_to_email
- excerpts.ExcerptTypes.insert : name, name_nl, name_de, name_en, content_type, primary, certifying, build_method, template, body_template
- excerpts.Excerpts.detail : id, excerpt_type, project, user, build_method, company, contact_person, language, owner, build_time, body_template_content
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
- jobs.JobsOverview.show : body
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
- outbox.Mails.detail : subject, project, date, user, sent, id, owner, AttachmentsByMail, UploadsByController, body
- outbox.Mails.insert : project, subject, body
- pcsw.ClientContactTypes.insert : id, name, name_nl, name_de, name_en
- pcsw.Clients.create_visit : user, summary
- pcsw.Clients.detail : overview, gender, id, nationality, last_name, first_name, middle_name, birth_date, age, language, email, phone, fax, gsm, image, national_id, civil_state, birth_country, birth_place, declared_name, needs_residence_permit, needs_work_permit, in_belgium_since, residence_type, residence_until, group, aid_type, AgentsByClient, workflow_buttons, id_document, faculty, MembersByPerson, child_custody, LinksByHuman, skills, obstacles, is_seeking, unemployed_since, seeking_since, work_permit_suspended_until, ResponsesByPartner, ExcerptsByProject, activity, client_state, noble_condition, unavailable_until, unavailable_why, is_obsolete, has_esf, created, modified, remarks
- pcsw.Clients.insert : first_name, last_name, national_id, gender, language
- pcsw.Clients.merge_row : merge_to, aids_IncomeConfirmation, aids_RefundConfirmation, aids_SimpleConfirmation, pcsw_Coaching, pcsw_Dispense, cv_LanguageKnowledge, cv_Obstacle, cv_Skill, cv_SoftSkill, addresses_Address, reason
- pcsw.Clients.refuse_client : reason, remark
- pcsw.CoachingEndings.insert : id, name, name_nl, name_de, name_en, seqno
- pcsw.Coachings.create_visit : user, summary
- plausibility.Checkers.detail : value, text
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
- system.SiteConfigs.detail : site_company, next_partner_id, job_office, master_budget, signer1, signer2, signer1_function, signer2_function, system_note_type, default_build_method, propgroup_skills, propgroup_softskills, propgroup_obstacles, residence_permit_upload_type, work_permit_upload_type, driving_licence_upload_type, default_event_type, prompt_calendar, client_guestrole, team_guestrole, cbss_org_unit, sector, ssdn_user_id, ssdn_email, cbss_http_username, cbss_http_password
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
- about.Models.detail : visible for 100 110 120 200 210 220 300 400 410 500 510 800 admin 910
- accounts.Accounts.detail : visible for 510 admin 910
- accounts.Accounts.insert : visible for 510 admin 910
- accounts.Groups.detail : visible for 510 admin 910
- accounts.Groups.insert : visible for 510 admin 910
- active_job_search.Proofs.insert : visible for 110 admin 910
- addresses.Addresses.detail : visible for admin 910
- addresses.Addresses.insert : visible for admin 910
- aids.AidTypes.detail : visible for 110 210 410 500 510 800 admin 910
- aids.AidTypes.insert : visible for 110 210 410 500 510 800 admin 910
- aids.Categories.insert : visible for 110 210 410 500 510 800 admin 910
- aids.Grantings.detail : visible for 100 110 120 200 210 300 400 410 500 510 800 admin 910
- aids.Grantings.insert : visible for 100 110 120 200 210 300 400 410 500 510 800 admin 910
- aids.GrantingsByClient.insert : visible for 100 110 120 200 210 300 400 410 500 510 800 admin 910
- aids.IncomeConfirmations.insert : visible for 100 110 120 200 210 300 400 410 500 510 800 admin 910
- aids.IncomeConfirmationsByGranting.insert : visible for 100 110 120 200 210 300 400 410 500 510 800 admin 910
- aids.RefundConfirmations.insert : visible for 100 110 120 200 210 300 400 410 500 510 800 admin 910
- aids.RefundConfirmationsByGranting.insert : visible for 100 110 120 200 210 300 400 410 500 510 800 admin 910
- aids.SimpleConfirmations.insert : visible for 100 110 120 200 210 300 400 410 500 510 800 admin 910
- aids.SimpleConfirmationsByGranting.insert : visible for 100 110 120 200 210 300 400 410 500 510 800 admin 910
- art61.ContractTypes.insert : visible for 110 admin 910
- art61.Contracts.detail : visible for 100 110 120 admin 910
- art61.Contracts.insert : visible for 100 110 120 admin 910
- boards.Boards.detail : visible for admin 910
- boards.Boards.insert : visible for admin 910
- cal.Calendars.detail : visible for 110 410 admin 910
- cal.Calendars.insert : visible for 110 410 admin 910
- cal.EventTypes.detail : visible for 110 410 admin 910
- cal.EventTypes.insert : visible for 110 410 admin 910
- cal.Events.detail : visible for 110 410 admin 910
- cal.Events.insert : visible for 110 410 admin 910
- cal.EventsByClient.insert : visible for 100 110 120 200 300 400 410 500 510 admin 910
- cal.GuestRoles.insert : visible for admin 910
- cal.GuestStates.wf1 : visible for admin 910
- cal.GuestStates.wf2 : visible for admin 910
- cal.Guests.checkin : visible for admin 910
- cal.Guests.detail : visible for admin 910
- cal.Guests.insert : visible for admin 910
- cal.RecurrentEvents.detail : visible for 110 410 admin 910
- cal.RecurrentEvents.insert : visible for 110 410 admin 910
- cal.Rooms.insert : visible for 110 410 admin 910
- cal.Tasks.detail : visible for 110 410 admin 910
- cal.Tasks.insert : visible for 110 410 admin 910
- cal.TasksByController.insert : visible for 100 110 120 200 300 400 410 500 510 admin 910
- cbss.IdentifyPersonRequests.detail : visible for 100 110 120 200 210 300 400 410 admin 910
- cbss.IdentifyPersonRequests.insert : visible for 100 110 120 200 210 300 400 410 admin 910
- cbss.ManageAccessRequests.detail : visible for 100 110 120 200 210 300 400 410 admin 910
- cbss.ManageAccessRequests.insert : visible for 100 110 120 200 210 300 400 410 admin 910
- cbss.RetrieveTIGroupsRequests.detail : visible for 100 110 120 200 210 300 400 410 admin 910
- cbss.RetrieveTIGroupsRequests.insert : visible for 100 110 120 200 210 300 400 410 admin 910
- changes.Changes.detail : visible for admin 910
- contacts.Companies.detail : visible for 100 110 120 200 210 220 300 400 410 500 510 800 admin 910
- contacts.Companies.insert : visible for 100 110 120 200 210 220 300 400 410 500 510 800 admin 910
- contacts.Companies.merge_row : visible for 110 210 410 800 admin 910
- contacts.Partners.detail : visible for 100 110 120 200 210 220 300 400 410 500 510 800 admin 910
- contacts.Partners.insert : visible for 100 110 120 200 210 220 300 400 410 500 510 800 admin 910
- contacts.Persons.create_household : visible for 100 110 120 200 210 220 300 400 410 500 510 800 admin 910
- contacts.Persons.detail : visible for 100 110 120 200 210 220 300 400 410 500 510 800 admin 910
- contacts.Persons.insert : visible for 100 110 120 200 210 220 300 400 410 500 510 800 admin 910
- countries.Countries.detail : visible for 100 110 120 200 210 300 400 410 500 510 800 admin 910
- countries.Countries.insert : visible for 100 110 120 200 210 300 400 410 500 510 800 admin 910
- countries.Places.insert : visible for 110 210 410 800 admin 910
- countries.Places.merge_row : visible for 110 210 410 800 admin 910
- courses.Activities.detail : visible for 100 110 120 200 210 300 400 410 800 admin 910
- courses.Activities.insert : visible for 100 110 120 200 210 300 400 410 800 admin 910
- courses.Enrolments.detail : visible for 100 110 120 200 210 220 300 400 410 500 510 800 admin 910
- courses.Enrolments.insert : visible for 100 110 120 200 210 220 300 400 410 500 510 800 admin 910
- courses.EnrolmentsByCourse.insert : visible for 100 110 120 200 210 300 400 410 800 admin 910
- courses.EnrolmentsByPupil.insert : visible for 100 110 120 200 210 300 400 410 800 admin 910
- courses.Lines.detail : visible for 100 110 120 200 210 300 400 410 800 admin 910
- courses.Lines.insert : visible for 100 110 120 200 210 300 400 410 800 admin 910
- courses.Slots.detail : visible for admin 910
- courses.Slots.insert : visible for admin 910
- courses.Topics.insert : visible for admin 910
- cv.Durations.insert : visible for 110 admin 910
- cv.EducationLevels.insert : visible for 110 admin 910
- cv.Experiences.insert : visible for 110 admin 910
- cv.ExperiencesByPerson.insert : visible for 100 110 120 admin 910  
- cv.Functions.insert : visible for 110 admin 910
- cv.Regimes.insert : visible for 110 admin 910
- cv.Sectors.insert : visible for 110 admin 910
- cv.Statuses.insert : visible for 110 admin 910
- cv.Studies.insert : visible for 110 admin 910
- cv.StudiesByPerson.insert : visible for 100 110 120 admin 910  
- cv.StudyTypes.detail : visible for 110 admin 910
- cv.StudyTypes.insert : visible for 110 admin 910
- cv.Trainings.detail : visible for 100 110 120 200 210 220 300 400 410 500 510 800 admin 910
- cv.Trainings.insert : visible for 100 110 120 200 210 220 300 400 410 500 510 800 admin 910
- debts.Accounts.detail : visible for admin 910
- debts.Accounts.insert : visible for admin 910
- debts.Budgets.detail : visible for admin 910
- debts.Budgets.insert : visible for admin 910
- debts.Groups.detail : visible for admin 910
- debts.Groups.insert : visible for admin 910
- esf.Summaries.detail : visible for 100 110 120 200 210 220 300 400 410 500 510 800 admin 910
- excerpts.ExcerptTypes.detail : visible for admin 910
- excerpts.ExcerptTypes.insert : visible for admin 910
- excerpts.Excerpts.detail : visible for 100 110 120 200 210 220 300 400 410 500 510 800 admin 910
- gfks.ContentTypes.insert : visible for admin 910
- households.Households.detail : visible for 100 110 120 200 210 300 400 410 500 510 800 admin 910
- households.HouseholdsByType.detail : visible for 100 110 120 200 210 300 400 410 500 510 800 admin 910
- households.Types.insert : visible for 110 210 410 800 admin 910
- humanlinks.Links.insert : visible for 110 210 410 800 admin 910
- immersion.ContractTypes.detail : visible for 110 admin 910
- immersion.ContractTypes.insert : visible for 110 admin 910
- immersion.Contracts.detail : visible for 100 110 120 admin 910
- immersion.Contracts.insert : visible for 100 110 120 admin 910
- immersion.Goals.insert : visible for 110 admin 910
- integ.ActivityReport.show : visible for 100 110 120 admin 910
- isip.ContractEndings.insert : visible for 110 410 admin 910
- isip.ContractPartners.insert : visible for 110 410 admin 910
- isip.ContractTypes.insert : visible for 110 410 admin 910
- isip.Contracts.detail : visible for 100 110 120 200 300 400 410 admin 910
- isip.Contracts.insert : visible for 100 110 120 200 300 400 410 admin 910
- isip.ExamPolicies.insert : visible for 110 410 admin 910
- jobs.ContractTypes.insert : visible for 110 410 admin 910
- jobs.Contracts.detail : visible for 100 110 120 200 300 400 410 admin 910
- jobs.Contracts.insert : visible for 100 110 120 200 300 400 410 admin 910
- jobs.JobProviders.detail : visible for 100 110 120 admin 910
- jobs.JobTypes.insert : visible for 110 410 admin 910
- jobs.Jobs.insert : visible for 100 110 120 admin 910
- jobs.JobsOverview.show : visible for 100 110 120 admin 910
- jobs.Offers.insert : visible for 100 110 120 admin 910
- jobs.Schedules.insert : visible for 110 410 admin 910
- languages.Languages.insert : visible for 100 110 120 200 300 400 410 500 510 admin 910
- newcomers.AvailableCoachesByClient.assign_coach : visible for 110 120 200 220 300 800 admin 910
- newcomers.Faculties.detail : visible for 110 410 admin 910
- newcomers.Faculties.insert : visible for 110 410 admin 910
- notes.EventTypes.insert : visible for 110 410 admin 910
- notes.NoteTypes.detail : visible for 110 410 admin 910
- notes.NoteTypes.insert : visible for 110 410 admin 910
- notes.Notes.detail : visible for 100 110 120 200 210 220 300 400 410 500 510 800 admin 910
- notes.Notes.insert : visible for 100 110 120 200 210 220 300 400 410 500 510 800 admin 910
- outbox.Mails.detail : visible for 110 410 admin 910
- outbox.Mails.insert : visible for 110 410 admin 910
- pcsw.ClientContactTypes.insert : visible for 110 410 admin 910
- pcsw.Clients.create_visit : visible for 100 110 120 200 210 220 300 400 410 500 510 800 admin 910
- pcsw.Clients.detail : visible for 100 110 120 200 210 220 300 400 410 500 510 800 admin 910
- pcsw.Clients.insert : visible for 100 110 120 200 210 220 300 400 410 500 510 800 admin 910
- pcsw.Clients.merge_row : visible for 110 210 410 800 admin 910
- pcsw.Clients.refuse_client : visible for 120 200 220 300 admin 910
- pcsw.CoachingEndings.insert : visible for 110 410 admin 910
- pcsw.Coachings.create_visit : visible for 110 410 admin 910
- plausibility.Checkers.detail : visible for admin 910
- plausibility.Problems.detail : visible for 100 110 120 200 210 220 300 400 410 500 510 800 admin 910
- polls.AnswerRemarks.insert : visible for 100 110 120 200 300 400 410 admin 910
- polls.ChoiceSets.insert : visible for 110 410 admin 910
- polls.Polls.detail : visible for 100 110 120 200 300 400 410 admin 910
- polls.Polls.insert : visible for 100 110 120 200 300 400 410 admin 910
- polls.Questions.insert : visible for 110 410 admin 910
- polls.Responses.detail : visible for 100 110 120 200 300 400 410 admin 910
- polls.Responses.insert : visible for 100 110 120 200 300 400 410 admin 910
- reception.BusyVisitors.detail : visible for 100 110 120 200 210 220 300 400 410 500 510 800 admin 910
- reception.GoneVisitors.detail : visible for 100 110 120 200 210 220 300 400 410 500 510 800 admin 910
- reception.MyWaitingVisitors.detail : visible for 100 110 120 200 300 400 410 500 510 admin 910
- reception.WaitingVisitors.detail : visible for 100 110 120 200 210 220 300 400 410 500 510 800 admin 910
- system.SiteConfigs.detail : visible for admin 910
- tinymce.TextFieldTemplates.detail : visible for admin 910
- tinymce.TextFieldTemplates.insert : visible for admin 910
- uploads.AllUploads.detail : visible for 110 410 admin 910
- uploads.AllUploads.insert : visible for 110 410 admin 910
- uploads.UploadTypes.detail : visible for 110 410 admin 910
- uploads.UploadTypes.insert : visible for 110 410 admin 910
- uploads.Uploads.detail : visible for 100 110 120 200 210 220 300 400 410 500 510 800 admin 910
- uploads.Uploads.insert : visible for 100 110 120 200 210 220 300 400 410 500 510 800 admin 910
- uploads.UploadsByClient.insert : visible for 100 110 120 200 210 220 300 400 410 500 510 800 admin 910
- uploads.UploadsByController.insert : visible for 100 110 120 200 210 220 300 400 410 500 510 800 admin 910
- users.Users.change_password : visible for admin 910
- users.Users.detail : visible for admin 910
- users.Users.insert : visible for admin 910
<BLANKLINE>


The main menu
=============

Romain
------

>>> rt.login('romain').show_menu()
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
- Contacts : Personnes,  ▶ Bénéficiaires, Organisations, -, Partenaires (tous), Ménages
- Office : Mes Messages, Mes téléchargements à renouveler, Mes Fichiers téléchargés, Mon courrier sortant, Mes Extraits, Mes Observations, Mes problèmes de données
- Calendrier : Calendrier, Mes rendez-vous, Rendez-vous dépassés, Rendez-vous à confirmer, Mes tâches, Mes visiteurs, Mes présences
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
- Ateliers : Ateliers d'insertion sociale, Ateliers d'Insertion socioprofessionnelle, -, Séries d'ateliers, Demandes d’inscription en attente, Demandes d’inscription confirmées
- Nouvelles demandes : Nouveaux bénéficiaires, Agents disponibles
- Médiation de dettes : Bénéficiaires, Mes Budgets
- Questionnaires : Mes Questionnaires, Mes Interviews
- Rapports :
  - Système : Broken GFKs
  - Intégration : Agents et leurs clients, Situation contrats Art 60-7, Rapport d'activité
- Configuration :
  - Système : Paramètres du Site, Utilisateurs, Textes d'aide, Update all summary data
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
  - Médiation de dettes : Groupes de comptes, Comptes, Budget modèle
  - Questionnaires : Listes de choix
- Explorateur :
  - Contacts : Personnes de contact, Types d'adresses, Adresses, Membres du conseil, Household member roles, Membres de ménage, Personal Links, Type de parenté
  - Système : Procurations, Types d'utilisateur, types de contenu, Messages, Changes, Tests de données, Problèmes de données
  - Office : Fichiers téléchargés, Upload Areas, Mails envoyés, Pièces jointes, Extraits, Observations, Text Field Templates
  - Calendrier : Tâches, Présences, Abonnements, Event states, Guest states, Task states
  - Ateliers : Tests de niveau, Ateliers, Inscriptions, États d'inscription
  - CPAS : Interventions, Contacts client, Exclusions, Antécédents judiciaires, Bénéficiaires, Etats civils, Etats bénéficiaires, Type de carte eID, Octrois d'aide, Certificats de revenu, Refund confirmations, Confirmations simple
  - Parcours : Connaissances de langue, Formations, Études, Expériences professionnelles, Connaissances de langue, Compétences professionnelles, Compétences sociales, Freins
  - Intégration : PIISs, Mises à l'emploi art60§7, Candidatures, Services utilisateurs, Mises à l'emploi art61, Stages d'immersion, Preuves de recherche, Fiches FSE
  - Nouvelles demandes : Compétences
  - BCSS : Requêtes IdentifyPerson, Requêtes ManageAccess, Requêtes Tx25
  - Médiation de dettes : Budgets, Entrées
  - Questionnaires : Questionnaires, Questions, Choix, Interviews, Choix de réponse, Answer Remarks
- Site : à propos

Theresia
--------

Theresia est un agent d'accueil. Elle ne voit pas les questionnaires,
les données de parcours, compétences professionnelles, compétences
sociales, freins. Elle peut faire des requètes CBSS.


>>> rt.login('theresia').show_menu()
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
- Contacts : Personnes,  ▶ Bénéficiaires, Organisations, -, Partenaires (tous), Ménages
- Office : Mes téléchargements à renouveler, Mes Fichiers téléchargés, Mes Extraits, Mes Observations
- Réception : Bénéficiaires, Rendez-vous aujourd'hui, Salle d'attente, Visiteurs occupés, Visiteurs repartis
- Intégration :
  - BCSS : Mes Requêtes IdentifyPerson, Mes Requêtes ManageAccess, Mes Requêtes Tx25
- Ateliers : Ateliers d'insertion sociale, Ateliers d'Insertion socioprofessionnelle, -, Séries d'ateliers
- Configuration :
  - Endroits : Pays, Endroits
  - Contacts : Types d'organisation, Fonctions, Types de ménage
  - CPAS : Types d'aide sociale, Catégories
- Explorateur :
  - Contacts : Personnes de contact, Household member roles, Membres de ménage, Personal Links, Type de parenté
  - Ateliers : Ateliers
  - CPAS : Octrois d'aide, Certificats de revenu, Refund confirmations, Confirmations simple
- Site : à propos


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
- cal.GuestStates.wf1 : Accepter
  (main) [visible for all]: **Résumé** (notify_subject), **Description** (notify_body), **Ne pas avertir les autres** (notify_silent)
- cal.GuestStates.wf2 : Rejeter
  (main) [visible for all]: **Résumé** (notify_subject), **Description** (notify_body), **Ne pas avertir les autres** (notify_silent)
- cal.Guests.checkin : Arriver
  (main) [visible for all]: **Résumé** (notify_subject), **Description** (notify_body), **Ne pas avertir les autres** (notify_silent)
- contacts.Companies.merge_row : Fusionner
  (main) [visible for all]: **vers...** (merge_to), **Adresses** (addresses_Address), **Raison** (reason)
- contacts.Persons.create_household : Créer un ménage
  (main) [visible for all]: **Partenaire** (partner), **Type de ménage** (type), **Chef de ménage** (head)
- countries.Places.merge_row : Fusionner
  (main) [visible for all]: **vers...** (merge_to), **Raison** (reason)
- newcomers.AvailableCoachesByClient.assign_coach : Attribuer
  (main) [visible for all]: **Résumé** (notify_subject), **Description** (notify_body), **Ne pas avertir les autres** (notify_silent)
- pcsw.Clients.create_visit : Enregistrer consultation
  (main) [visible for all]: **Utilisateur** (user), **Raison** (summary)
- pcsw.Clients.merge_row : Fusionner
  (main) [visible for all]:
  - **vers...** (merge_to)
  - **Also reassign volatile related objects** (keep_volatiles):
    - (keep_volatiles_1): **Certificats de revenu** (aids_IncomeConfirmation), **Refund confirmations** (aids_RefundConfirmation)
    - (keep_volatiles_2): **Confirmations simple** (aids_SimpleConfirmation), **Interventions** (pcsw_Coaching)
    - (keep_volatiles_3): **Dispenses** (pcsw_Dispense), **Connaissances de langue** (cv_LanguageKnowledge)
    - (keep_volatiles_4): **Freins** (cv_Obstacle), **Compétences professionnelles** (cv_Skill)
    - (keep_volatiles_5): **Compétences sociales** (cv_SoftSkill), **Adresses** (addresses_Address)
  - **Raison** (reason)
- pcsw.Clients.refuse_client : Refuser
  (main) [visible for all]: **Raison de refus** (reason), **Remarque** (remark)
- pcsw.Coachings.create_visit : Enregistrer consultation
  (main) [visible for all]: **Utilisateur** (user), **Raison** (summary)
- users.Users.change_password : Changer mot de passe
  (main) [visible for all]: **Mot de passe actuel** (current), **Nouveau mot de passe** (new1), **Encore une fois** (new2)
<BLANKLINE>



UsersWithClients
================

>>> rt.show(integ.UsersWithClients)
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE -REPORT_UDIFF
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


Menu walk
=========

Here is the output of :func:`walk_menu_items
<lino.api.doctests.walk_menu_items>` for this database:

>>> walk_menu_items('romain')
... #doctest: -ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
- Contacts --> Personnes : 103
- Contacts -->  Bénéficiaires : 58
- Contacts --> Organisations : 40
- Contacts --> Partenaires (tous) : 163
- Contacts --> Ménages : 15
- Office --> Mes Messages : 2
- Office --> Mes téléchargements à renouveler : 1
- Office --> Mes Fichiers téléchargés : 1
- Office --> Mon courrier sortant : 1
- Office --> Mes Extraits : 0
- Office --> Mes Observations : 10
- Office --> Mes problèmes de données : 0
- Calendrier --> Mes rendez-vous : 13
- Calendrier --> Rendez-vous dépassés : 31
- Calendrier --> Rendez-vous à confirmer : 3
- Calendrier --> Mes tâches : 1
- Calendrier --> Mes visiteurs : 1
- Calendrier --> Mes présences : 1
- Réception --> Bénéficiaires : 30
- Réception --> Rendez-vous aujourd'hui : 10
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
- Ateliers --> Ateliers d'insertion sociale : 6
- Ateliers --> Ateliers d'Insertion socioprofessionnelle : 3
- Ateliers --> Séries d'ateliers : 8
- Ateliers --> Demandes d’inscription en attente : 21
- Ateliers --> Demandes d’inscription confirmées : 21
- Nouvelles demandes --> Nouveaux bénéficiaires : 23
- Nouvelles demandes --> Agents disponibles : 3
- Médiation de dettes --> Bénéficiaires : 0
- Médiation de dettes --> Mes Budgets : 4
- Questionnaires --> Mes Questionnaires : 1
- Questionnaires --> Mes Interviews : 1
- Rapports --> Système --> Broken GFKs : 0
- Rapports --> Intégration --> Agents et leurs clients : 3
- Configuration --> Système --> Utilisateurs : 13
- Configuration --> Système --> Textes d'aide : 6
- Configuration --> Endroits --> Pays : 271
- Configuration --> Endroits --> Endroits : 79
- Configuration --> Contacts --> Types d'organisation : 17
- Configuration --> Contacts --> Fonctions : 6
- Configuration --> Contacts --> Conseils : 4
- Configuration --> Contacts --> Types de ménage : 7
- Configuration --> Office --> Types de fichiers téléchargés : 10
- Configuration --> Office --> Types d'extrait : 19
- Configuration --> Office --> Types d'observation : 14
- Configuration --> Office --> Types d'événements : 11
- Configuration --> Office --> Mes Text Field Templates : 1
- Configuration --> Calendrier --> Calendriers : 13
- Configuration --> Calendrier --> Locaux : 1
- Configuration --> Calendrier --> Priorités : 5
- Configuration --> Calendrier --> Recurrent event rules : 16
- Configuration --> Calendrier --> Rôles de participants : 5
- Configuration --> Calendrier --> Types d'entrée calendrier : 12
- Configuration --> Calendrier --> Remote Calendars : 1
- Configuration --> Comptabilité --> Groupes de comptes : 1
- Configuration --> Comptabilité --> Comptes : 1
- Configuration --> Ateliers --> Savoirs de base : 1
- Configuration --> Ateliers --> Topics : 1
- Configuration --> Ateliers --> Timetable Slots : 1
- Configuration --> CPAS --> Phases d'intégration : 6
- Configuration --> CPAS --> Activités : 1
- Configuration --> CPAS --> types d'exclusions : 3
- Configuration --> CPAS --> Services : 4
- Configuration --> CPAS --> Raisons d’arrêt d'intervention : 5
- Configuration --> CPAS --> Motifs de dispense : 5
- Configuration --> CPAS --> Types de contact client : 11
- Configuration --> CPAS --> Types d'aide sociale : 12
- Configuration --> CPAS --> Catégories : 4
- Configuration --> Parcours --> Langues : 6
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
- Configuration --> Questionnaires --> Listes de choix : 9
- Explorateur --> Contacts --> Personnes de contact : 11
- Explorateur --> Contacts --> Types d'adresses : 6
- Explorateur --> Contacts --> Adresses : 91
- Explorateur --> Contacts --> Membres du conseil : 1
- Explorateur --> Contacts --> Household member roles : 8
- Explorateur --> Contacts --> Membres de ménage : 64
- Explorateur --> Contacts --> Personal Links : 60
- Explorateur --> Contacts --> Type de parenté : 13
- Explorateur --> Système --> Procurations : 4
- Explorateur --> Système --> Types d'utilisateur : 15
- Explorateur --> Système --> types de contenu : 134
- Explorateur --> Système --> Messages : 13
- Explorateur --> Système --> Changes : 0
- Explorateur --> Système --> Tests de données : 11
- Explorateur --> Système --> Problèmes de données : 0
- Explorateur --> Office --> Fichiers téléchargés : 12
- Explorateur --> Office --> Upload Areas : 1
- Explorateur --> Office --> Mails envoyés : 1
- Explorateur --> Office --> Pièces jointes : 1
- Explorateur --> Office --> Extraits : 70
- Explorateur --> Office --> Observations : 112
- Explorateur --> Office --> Text Field Templates : 3
- Explorateur --> Calendrier --> Tâches : 35
- Explorateur --> Calendrier --> Présences : 571
- Explorateur --> Calendrier --> Abonnements : 10
- Explorateur --> Calendrier --> Event states : 6
- Explorateur --> Calendrier --> Guest states : 9
- Explorateur --> Calendrier --> Task states : 4
- Explorateur --> Ateliers --> Tests de niveau : 1
- Explorateur --> Ateliers --> Ateliers : 8
- Explorateur --> Ateliers --> Inscriptions : 81
- Explorateur --> Ateliers --> États d'inscription : 5
- Explorateur --> CPAS --> Interventions : 91
- Explorateur --> CPAS --> Contacts client : 15
- Explorateur --> CPAS --> Exclusions : 1
- Explorateur --> CPAS --> Antécédents judiciaires : 1
- Explorateur --> CPAS --> Bénéficiaires : 58
- Explorateur --> CPAS --> Etats civils : 7
- Explorateur --> CPAS --> Etats bénéficiaires : 4
- Explorateur --> CPAS --> Type de carte eID : 10
- Explorateur --> CPAS --> Octrois d'aide : 56
- Explorateur --> CPAS --> Certificats de revenu : 55
- Explorateur --> CPAS --> Refund confirmations : 13
- Explorateur --> CPAS --> Confirmations simple : 20
- Explorateur --> Parcours --> Connaissances de langue : 120
- Explorateur --> Parcours --> Formations : 21
- Explorateur --> Parcours --> Études : 23
- Explorateur --> Parcours --> Expériences professionnelles : 31
- Explorateur --> Parcours --> Connaissances de langue : 120
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
- Explorateur --> Nouvelles demandes --> Compétences : 8
- Explorateur --> BCSS --> Requêtes IdentifyPerson : 6
- Explorateur --> BCSS --> Requêtes ManageAccess : 2
- Explorateur --> BCSS --> Requêtes Tx25 : 7
- Explorateur --> Médiation de dettes --> Budgets : 15
- Explorateur --> Médiation de dettes --> Entrées : 717
- Explorateur --> Questionnaires --> Questionnaires : 3
- Explorateur --> Questionnaires --> Questions : 39
- Explorateur --> Questionnaires --> Choix : 36
- Explorateur --> Questionnaires --> Interviews : 7
- Explorateur --> Questionnaires --> Choix de réponse : 89
- Explorateur --> Questionnaires --> Answer Remarks : 1
<BLANKLINE>
