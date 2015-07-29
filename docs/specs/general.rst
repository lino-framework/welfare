.. _welfare.tested.general:
.. _welfare.specs.general:

================================
General overview of Lino Welfare
================================

.. How to test only this document:

    $ python setup.py test -s tests.SpecsTests.test_general

    doctest init:

    >>> from __future__ import print_function
    >>> import os
    >>> os.environ['DJANGO_SETTINGS_MODULE'] = \
    ...    'lino_welfare.projects.std.settings.doctests'
    >>> from lino.api.doctest import *
    
.. contents:: 
   :local:
   :depth: 2


Database structure
==================

Lino Welfare consists of many *modules* (called **plugins** or
"apps"), each of which defines a series of *database tables* (called
**models**).  Each model defines a number of **fields**.

For each database model, Lino defines at least one **table** which it
calls "default table".

The following table gives an overview of these things.


>>> print(settings.SITE.get_db_overview_rst()) 
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF -SKIP
55 apps: staticfiles, about, bootstrap3, lino, appypod, printing, system, contenttypes, humanize, users, changes, countries, properties, contacts, addresses, uploads, outbox, excerpts, extensible, cal, reception, accounts, badges, iban, sepa, ledger, vatless, finan, boards, welfare, sales, pcsw, languages, cv, integ, isip, jobs, art61, immersion, active_job_search, courses, newcomers, cbss, households, humanlinks, debts, notes, aids, polls, beid, davlink, export_excel, dupable_clients, plausibility, tinymce.
149 models:
============================== =============================== ========= =======
 Name                           Default table                   #fields   #rows
------------------------------ ------------------------------- --------- -------
 accounts.Account               accounts.Accounts               19        76
 accounts.Group                 accounts.Groups                 9         14
 active_job_search.Proof        active_job_search.Proofs        7         10
 addresses.Address              addresses.Addresses             16        167
 aids.AidType                   aids.AidTypes                   23        11
 aids.Category                  aids.Categories                 5         3
 aids.Granting                  aids.Grantings                  12        55
 aids.IncomeConfirmation        aids.IncomeConfirmations        17        54
 aids.RefundConfirmation        aids.RefundConfirmations        18        12
 aids.SimpleConfirmation        aids.SimpleConfirmations        15        19
 art61.Contract                 art61.Contracts                 30        7
 art61.ContractType             art61.ContractTypes             10        1
 badges.Award                   badges.Awards                   6         0
 badges.Badge                   badges.Badges                   5         0
 boards.Board                   boards.Boards                   7         3
 boards.Member                  boards.Members                  4         0
 cal.Calendar                   cal.Calendars                   7         11
 cal.Event                      cal.OneEvent                    24        528
 cal.EventType                  cal.EventTypes                  19        8
 cal.Guest                      cal.Guests                      9         521
 cal.GuestRole                  cal.GuestRoles                  5         4
 cal.Priority                   cal.Priorities                  6         4
 cal.RecurrentEvent             cal.RecurrentEvents             22        9
 cal.RemoteCalendar             cal.RemoteCalendars             7         0
 cal.Room                       cal.Rooms                       5         0
 cal.Subscription               cal.Subscriptions               4         8
 cal.Task                       cal.Tasks                       19        34
 cbss.IdentifyPersonRequest     cbss.IdentifyPersonRequests     21        5
 cbss.ManageAccessRequest       cbss.ManageAccessRequests       24        1
 cbss.Purpose                   cbss.Purposes                   7         106
 cbss.RetrieveTIGroupsRequest   cbss.RetrieveTIGroupsRequests   15        2
 cbss.Sector                    cbss.Sectors                    11        209
 changes.Change                 changes.Changes                 9         0
 contacts.Company               contacts.Companies              30        49
 contacts.CompanyType           contacts.CompanyTypes           9         16
 contacts.Partner               contacts.Partners               26        172
 contacts.Person                contacts.Persons                33        109
 contacts.Role                  contacts.Roles                  4         10
 contacts.RoleType              contacts.RoleTypes              6         5
 contenttypes.ContentType       contenttypes.ContentTypes       4         150
 contenttypes.HelpText          contenttypes.HelpTexts          4         5
 countries.Country              countries.Countries             9         8
 countries.Place                countries.Places                10        78
 courses.Course                 courses.Courses                 5         3
 courses.CourseContent          courses.CourseContents          2         2
 courses.CourseOffer            courses.CourseOffers            6         3
 courses.CourseProvider         courses.CourseProviders         31        2
 courses.CourseRequest          courses.CourseRequests          10        20
 cv.Duration                    cv.Durations                    5         5
 cv.EducationLevel              cv.EducationLevels              8         5
 cv.Experience                  cv.Experiences                  17        30
 cv.Function                    cv.Functions                    7         4
 cv.LanguageKnowledge           cv.LanguageKnowledges           9         119
 cv.Obstacle                    cv.Obstacles                    6         0
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
 debts.Actor                    debts.Actors                    6         63
 debts.Budget                   debts.Budgets                   11        14
 debts.Entry                    debts.Entries                   16        716
 dupable_clients.Word           dupable_clients.Words           3         131
 excerpts.Excerpt               excerpts.Excerpts               12        16
 excerpts.ExcerptType           excerpts.ExcerptTypes           18        16
 finan.BankStatement            finan.BankStatements            11        0
 finan.BankStatementItem        finan.BankStatementItemTable    10        0
 finan.Grouper                  finan.Groupers                  10        0
 finan.GrouperItem              finan.GrouperItemTable          9         0
 finan.JournalEntry             finan.FinancialVouchers         9         0
 finan.JournalEntryItem         finan.JournalEntryItemTable     10        0
 finan.PaymentOrder             finan.PaymentOrders             11        0
 finan.PaymentOrderItem         finan.PaymentOrderItemTable     9         0
 households.Household           households.Households           29        14
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
 jobs.Candidature               jobs.Candidatures               8         74
 jobs.Contract                  jobs.Contracts                  28        13
 jobs.ContractType              jobs.ContractTypes              10        5
 jobs.Job                       jobs.Jobs                       10        8
 jobs.JobProvider               jobs.JobProviders               31        3
 jobs.JobType                   jobs.JobTypes                   5         5
 jobs.Offer                     jobs.Offers                     9         1
 jobs.Schedule                  jobs.Schedules                  5         3
 languages.Language             languages.Languages             6         5
 ledger.Journal                 ledger.Journals                 20        3
 ledger.MatchRule               ledger.MatchRules               3         0
 ledger.Movement                ledger.Movements                11        44
 ledger.PaymentTerm             ledger.PaymentTerms             8         0
 ledger.Voucher                 ledger.Vouchers                 8         20
 newcomers.Broker               newcomers.Brokers               2         2
 newcomers.Competence           newcomers.Competences           5         7
 newcomers.Faculty              newcomers.Faculties             6         5
 notes.EventType                notes.EventTypes                10        9
 notes.Note                     notes.Notes                     17        110
 notes.NoteType                 notes.NoteTypes                 12        13
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
 plausibility.Problem           plausibility.Problems           6         60
 polls.AnswerChoice             polls.AnswerChoices             4         88
 polls.AnswerRemark             polls.AnswerRemarks             4         0
 polls.Choice                   polls.Choices                   7         35
 polls.ChoiceSet                polls.ChoiceSets                5         8
 polls.Poll                     polls.Polls                     11        2
 polls.Question                 polls.Questions                 9         38
 polls.Response                 polls.Responses                 7         6
 properties.PropChoice          properties.PropChoices          7         2
 properties.PropGroup           properties.PropGroups           5         0
 properties.PropType            properties.PropTypes            9         3
 properties.Property            properties.Properties           7         0
 sepa.Account                   sepa.Accounts                   8         13
 system.SiteConfig              system.SiteConfigs              28        1
 tinymce.TextFieldTemplate      tinymce.TextFieldTemplates      5         2
 uploads.Upload                 uploads.Uploads                 17        11
 uploads.UploadType             uploads.UploadTypes             11        9
 users.Authority                users.Authorities               3         3
 users.User                     users.Users                     21        11
 vatless.AccountInvoice         vatless.Invoices                17        20
 vatless.InvoiceItem            vatless.InvoiceItems            6         24
============================== =============================== ========= =======
<BLANKLINE>



List of window layouts
======================


The following table lists information about all *data entry form
definitions* (called **window layouts**) used by Lino Welfare.

Each window layout is **viewable** by a given set of user profiles.

Each window layout defines a given set of fields.

There are *detail* layouts, *insert* layouts and *action parameter* layouts.

>>> settings.SITE.catch_layout_exceptions = False
>>> from lino.utils.diag import window_actions
>>> print(window_actions())
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF -SKIP
- about.About.show (viewable for all except anonymous) : server_status
- about.Models.detail (viewable for all except anonymous) : app, name, docstring, rows
- accounts.AccountCharts.detail (viewable for admin) : name
- accounts.Accounts.detail (viewable for admin) : ref, name, name_fr, name_de, name_nl, group, type, required_for_household, required_for_person, periods, default_amount
- accounts.Accounts.insert (viewable for admin) : ref, group, type, name, name_fr, name_de, name_nl
- accounts.Groups.detail (viewable for admin) : ref, name, name_fr, name_de, name_nl, id, account_type, entries_layout
- accounts.Groups.insert (viewable for admin) : name, name_fr, name_de, name_nl, account_type, ref
- active_job_search.Proofs.insert (viewable for all except anonymous) : date, client, company, id, spontaneous, response, remarks
- addresses.Addresses.detail (viewable for admin) : country, city, zip_code, addr1, street, street_no, street_box, addr2, address_type, remark, data_source, partner
- addresses.Addresses.insert (viewable for admin) : country, city, street, street_no, street_box, address_type, remark
- aids.AidTypes.detail (viewable for 110, 210, 220, 410, admin) : id, short_name, confirmation_type, name, name_fr, name_de, name_nl, excerpt_title, excerpt_title_fr, excerpt_title_de, excerpt_title_nl, body_template, print_directly, is_integ_duty, is_urgent, confirmed_by_primary_coach, board, company, contact_person, contact_role, pharmacy_type
- aids.AidTypes.insert (viewable for 110, 210, 220, 410, admin) : name, name_fr, name_de, name_nl, confirmation_type
- aids.Categories.insert (viewable for 110, 210, 220, 410, admin) : id, name, name_fr, name_de, name_nl
- aids.Grantings.detail (viewable for all except anonymous) : id, client, user, signer, workflow_buttons, request_date, board, decision_date, aid_type, category, start_date, end_date, custom_actions
- aids.Grantings.insert (viewable for all except anonymous) : client, aid_type, signer, board, decision_date, start_date, end_date
- aids.GrantingsByClient.insert (viewable for all except anonymous) : aid_type, board, decision_date, start_date, end_date
- aids.IncomeConfirmations.insert (viewable for all except anonymous) : client, user, signer, workflow_buttons, printed, company, contact_person, language, granting, start_date, end_date, category, amount, id, remark
- aids.IncomeConfirmationsByGranting.insert (viewable for all except anonymous) : client, granting, start_date, end_date, category, amount, company, contact_person, language, remark
- aids.RefundConfirmations.insert (viewable for all except anonymous) : id, client, user, signer, workflow_buttons, granting, start_date, end_date, doctor_type, doctor, pharmacy, company, contact_person, language, printed, remark
- aids.RefundConfirmationsByGranting.insert (viewable for all except anonymous) : start_date, end_date, doctor_type, doctor, pharmacy, company, contact_person, language, printed, remark
- aids.SimpleConfirmations.insert (viewable for all except anonymous) : id, client, user, signer, workflow_buttons, granting, start_date, end_date, company, contact_person, language, printed, remark
- aids.SimpleConfirmationsByGranting.insert (viewable for all except anonymous) : start_date, end_date, company, contact_person, language, remark
- art61.ContractTypes.insert (viewable for 110, admin) : id, name, name_fr, name_de, name_nl, ref
- art61.Contracts.detail (viewable for 100, 110, admin) : id, client, user, language, type, company, contact_person, contact_role, applies_from, duration, applies_until, exam_policy, job_title, status, cv_duration, regime, reference_person, printed, date_decided, date_issued, date_ended, ending, subsidize_10, subsidize_20, subsidize_30, responsibilities
- art61.Contracts.insert (viewable for 100, 110, admin) : client, company, type
- boards.Boards.detail (viewable for admin) : id, name, name_fr, name_de, name_nl
- boards.Boards.insert (viewable for admin) : name, name_fr, name_de, name_nl
- cal.Calendars.detail (viewable for 110, 410, admin) : name, name_fr, name_de, name_nl, color, id, description
- cal.Calendars.insert (viewable for 110, 410, admin) : name, name_fr, name_de, name_nl, color
- cal.EventTypes.detail (viewable for 110, 410, admin) : name, name_fr, name_de, name_nl, event_label, event_label_fr, event_label_de, event_label_nl, max_conflicting, all_rooms, locks_user, id, invite_client, is_appointment, email_template, attach_to_email
- cal.EventTypes.insert (viewable for 110, 410, admin) : name, name_fr, name_de, name_nl, invite_client
- cal.Events.detail (viewable for 110, 410, admin) : event_type, summary, project, start_date, start_time, end_date, end_time, user, assigned_to, room, priority, access_class, transparent, owner, workflow_buttons, description, id, created, modified, state
- cal.Events.insert (viewable for 110, 410, admin) : summary, start_date, start_time, end_date, end_time, event_type, project
- cal.EventsByClient.insert (viewable for all except anonymous, 210, 220) : event_type, summary, start_date, start_time, end_date, end_time
- cal.GuestRoles.insert (viewable for admin) : id, name, name_fr, name_de, name_nl
- cal.GuestStates.wf1 (viewable for admin) : notify_subject, notify_body, notify_silent
- cal.GuestStates.wf2 (viewable for admin) : notify_subject, notify_body, notify_silent
- cal.Guests.checkin (viewable for admin) : notify_subject, notify_body, notify_silent
- cal.Guests.detail (viewable for admin) : event, partner, role, state, remark, workflow_buttons, waiting_since, busy_since, gone_since
- cal.Guests.insert (viewable for admin) : event, partner, role
- cal.RecurrentEvents.detail (viewable for 110, 410, admin) : name, name_fr, name_de, name_nl, id, user, event_type, start_date, start_time, end_date, end_time, every_unit, every, max_events, monday, tuesday, wednesday, thursday, friday, saturday, sunday, description
- cal.RecurrentEvents.insert (viewable for 110, 410, admin) : name, name_fr, name_de, name_nl, start_date, end_date, every_unit, event_type
- cal.Rooms.insert (viewable for 110, 410, admin) : id, name, name_fr, name_de, name_nl
- cal.Tasks.detail (viewable for 110, 410, admin) : start_date, due_date, id, workflow_buttons, summary, project, user, delegated, owner, created, modified, description
- cal.Tasks.insert (viewable for 110, 410, admin) : summary, user, project
- cal.TasksByController.insert (viewable for all except anonymous, 210, 220) : summary, start_date, due_date, user, delegated
- cbss.IdentifyPersonRequests.detail (viewable for all except anonymous) : id, person, user, sent, status, printed, national_id, first_name, middle_name, last_name, birth_date, tolerance, gender, environment, ticket, response_xml, info_messages, debug_messages
- cbss.IdentifyPersonRequests.insert (viewable for all except anonymous) : person, national_id, first_name, middle_name, last_name, birth_date, tolerance, gender
- cbss.ManageAccessRequests.detail (viewable for all except anonymous) : id, person, user, sent, status, printed, action, start_date, end_date, purpose, query_register, national_id, sis_card_no, id_card_no, first_name, last_name, birth_date, result, environment, ticket, response_xml, info_messages, debug_messages
- cbss.ManageAccessRequests.insert (viewable for all except anonymous) : person, action, start_date, end_date, purpose, query_register, national_id, sis_card_no, id_card_no, first_name, last_name, birth_date
- cbss.RetrieveTIGroupsRequests.detail (viewable for all except anonymous) : id, person, user, sent, status, printed, national_id, language, history, environment, ticket, response_xml, info_messages, debug_messages
- cbss.RetrieveTIGroupsRequests.insert (viewable for all except anonymous) : person, national_id, language, history
- changes.Changes.detail (viewable for admin) : time, user, type, master, object, id, diff
- contacts.Companies.detail (viewable for all except anonymous) : overview, prefix, name, type, vat_id, client_contact_type, url, email, phone, gsm, fax, remarks, VouchersByPartner, id, language, activity, is_obsolete, created, modified
- contacts.Companies.insert (viewable for all except anonymous) : name, language, email, type, id
- contacts.Companies.merge_row (viewable for admin) : merge_to, reason
- contacts.Partners.detail (viewable for all except anonymous) : overview, id, language, activity, client_contact_type, url, email, phone, gsm, fax, country, region, city, zip_code, addr1, street_prefix, street, street_no, street_box, addr2, remarks, VouchersByPartner, is_obsolete, created, modified
- contacts.Partners.insert (viewable for all except anonymous) : name, language, email
- contacts.Persons.create_household (viewable for all except anonymous) : partner, type, head
- contacts.Persons.detail (viewable for all except anonymous) : overview, title, first_name, middle_name, last_name, gender, birth_date, age, id, language, email, phone, gsm, fax, MembersByPerson, LinksByHuman, remarks, VouchersByPartner, activity, url, client_contact_type, is_obsolete, created, modified
- contacts.Persons.insert (viewable for all except anonymous) : first_name, last_name, gender, language
- contenttypes.ContentTypes.insert (viewable for admin) : id, name, app_label, model, base_classes
- countries.Countries.detail (viewable for all except anonymous) : isocode, name, name_fr, name_de, name_nl, short_code, inscode, actual_country
- countries.Countries.insert (viewable for all except anonymous) : isocode, inscode, name, name_fr, name_de, name_nl
- countries.Places.insert (viewable for 110, 410, admin) : name, name_fr, name_de, name_nl, country, type, parent, zip_code, id
- courses.CourseContents.insert (viewable for 110, admin) : id, name
- courses.CourseOffers.detail (viewable for 100, 110, admin) : id, title, content, provider, guest_role, description
- courses.CourseOffers.insert (viewable for 100, 110, admin) : provider, content, title
- courses.CourseProviders.detail (viewable for 100, 110, admin) : overview, prefix, name, type, vat_id, client_contact_type, url, email, phone, gsm, fax
- courses.CourseRequests.insert (viewable for 110, admin) : date_submitted, person, content, offer, urgent, course, state, date_ended, id, remark, UploadsByController
- courses.Courses.detail (viewable for 110, admin) : id, start_date, offer, title, remark
- courses.Courses.insert (viewable for 110, admin) : start_date, offer, title
- cv.Durations.insert (viewable for 110, admin) : id, name, name_fr, name_de, name_nl
- cv.EducationLevels.insert (viewable for 110, admin) : name, name_fr, name_de, name_nl, is_study, is_training
- cv.Experiences.insert (viewable for 110, admin) : person, start_date, end_date, termination_reason, company, country, city, sector, function, title, status, duration, regime, is_training, remarks
- cv.Functions.insert (viewable for 110, admin) : id, name, name_fr, name_de, name_nl, sector, remark
- cv.Regimes.insert (viewable for 110, admin) : id, name, name_fr, name_de, name_nl
- cv.Sectors.insert (viewable for 110, admin) : id, name, name_fr, name_de, name_nl, remark
- cv.Statuses.insert (viewable for 110, admin) : id, name, name_fr, name_de, name_nl
- cv.Studies.insert (viewable for 110, admin) : person, start_date, end_date, type, content, education_level, state, school, country, city, remarks
- cv.StudyTypes.detail (viewable for 110, admin) : name, name_fr, name_de, name_nl, id, education_level, is_study, is_training
- cv.StudyTypes.insert (viewable for 110, admin) : name, name_fr, name_de, name_nl, is_study, is_training, education_level
- cv.Trainings.detail (viewable for all except anonymous) : person, start_date, end_date, type, state, certificates, sector, function, school, country, city, remarks
- cv.Trainings.insert (viewable for all except anonymous) : person, start_date, end_date, type, state, certificates, sector, function, school, country, city
- debts.Budgets.detail (viewable for admin) : date, partner, id, user, intro, ResultByBudget, DebtsByBudget, AssetsByBudgetSummary, conclusion, dist_amount, printed, total_debt, include_yearly_incomes, print_empty_rows, print_todos, DistByBudget, data_box, summary_box
- debts.Budgets.insert (viewable for admin) : partner, date, user
- excerpts.ExcerptTypes.detail (viewable for admin) : id, name, name_fr, name_de, name_nl, content_type, build_method, template, body_template, email_template, shortcut, primary, print_directly, certifying, print_recipient, backward_compat, attach_to_email
- excerpts.ExcerptTypes.insert (viewable for admin) : name, name_fr, name_de, name_nl, content_type, primary, certifying, build_method, template, body_template
- excerpts.Excerpts.detail (viewable for all except anonymous) : id, excerpt_type, project, user, build_method, company, contact_person, language, owner, build_time, body_template_content
- finan.BankStatements.detail (viewable for all except anonymous) : date, balance1, balance2, user, workflow_buttons, id, journal, year, number
- finan.BankStatements.insert (viewable for all except anonymous) : date, user, balance1, balance2
- finan.FinancialVouchers.detail (viewable for all except anonymous) : date, user, narration, workflow_buttons, id, journal, year, number
- finan.FinancialVouchers.insert (viewable for all except anonymous) : date, user, narration
- finan.Groupers.detail (viewable for all except anonymous) : date, partner, user, workflow_buttons, id, journal, year, number
- finan.Groupers.insert (viewable for all except anonymous) : date, user, partner
- finan.PaymentOrders.detail (viewable for all except anonymous) : date, user, narration, total, execution_date, workflow_buttons, id, journal, year, number
- households.Households.detail (viewable for all except anonymous) : type, prefix, name, id
- households.HouseholdsByType.detail (viewable for all except anonymous) : type, name, language, id, country, region, city, zip_code, street_prefix, street, street_no, street_box, addr2, phone, gsm, email, url, remarks
- households.Types.insert (viewable for 110, 410, admin) : name, name_fr, name_de, name_nl
- humanlinks.Links.insert (viewable for 110, 410, admin) : parent, child, type
- immersion.ContractTypes.detail (viewable for 110, admin) : id, name, name_fr, name_de, name_nl, exam_policy, template, overlap_group, full_name
- immersion.ContractTypes.insert (viewable for 110, admin) : name, name_fr, name_de, name_nl, exam_policy
- immersion.Contracts.detail (viewable for 100, 110, admin) : id, client, user, language, type, goal, company, contact_person, contact_role, applies_from, applies_until, exam_policy, sector, function, reference_person, printed, date_decided, date_issued, date_ended, ending, responsibilities
- immersion.Contracts.insert (viewable for 100, 110, admin) : client, company, type, goal
- immersion.Goals.insert (viewable for 110, admin) : id, name, name_fr, name_de, name_nl
- integ.ActivityReport.show (viewable for 100, 110, admin) : body
- isip.ContractEndings.insert (viewable for 110, 410, admin) : name, use_in_isip, use_in_jobs, is_success, needs_date_ended
- isip.ContractPartners.insert (viewable for 110, admin) : company, contact_person, contact_role, duties_company
- isip.ContractTypes.insert (viewable for 110, 410, admin) : id, ref, exam_policy, needs_study_type, name, name_fr, name_de, name_nl, full_name
- isip.Contracts.detail (viewable for 100, 110, admin) : id, client, type, user, user_asd, study_type, applies_from, applies_until, exam_policy, language, date_decided, date_issued, printed, date_ended, ending, stages, goals, duties_asd, duties_dsbe, duties_person
- isip.Contracts.insert (viewable for 100, 110, admin) : client, type
- isip.ExamPolicies.insert (viewable for 110, 410, admin) : id, name, name_fr, name_de, name_nl, max_events, every, every_unit, event_type, monday, tuesday, wednesday, thursday, friday, saturday, sunday
- jobs.ContractTypes.insert (viewable for 110, 410, admin) : id, name, name_fr, name_de, name_nl, ref
- jobs.Contracts.detail (viewable for 100, 110, admin) : id, client, user, user_asd, language, job, type, company, contact_person, contact_role, applies_from, duration, applies_until, exam_policy, regime, schedule, hourly_rate, refund_rate, reference_person, printed, date_decided, date_issued, date_ended, ending, responsibilities
- jobs.Contracts.insert (viewable for 100, 110, admin) : client, job
- jobs.JobProviders.detail (viewable for 100, 110, admin) : overview, prefix, name, type, vat_id, client_contact_type, url, email, phone, gsm, fax
- jobs.JobTypes.insert (viewable for 110, 410, admin) : id, name, is_social
- jobs.Jobs.insert (viewable for 100, 110, admin) : name, provider, contract_type, type, id, sector, function, capacity, hourly_rate, remark
- jobs.JobsOverview.show (viewable for 100, 110, admin) : preview
- jobs.Offers.insert (viewable for 100, 110, admin) : name, provider, sector, function, selection_from, selection_until, start_date, remark
- jobs.OldJobsOverview.show (viewable for 100, 110, admin) : body
- jobs.Schedules.insert (viewable for 110, 410, admin) : id, name, name_fr, name_de, name_nl
- languages.Languages.insert (viewable for all except anonymous, 210, 220) : id, iso2, name, name_fr, name_de, name_nl
- ledger.ActivityReport.show (viewable for nobody) : body
- ledger.Journals.detail (viewable for all except anonymous) : ref, trade_type, seqno, id, voucher_type, journal_group, force_sequence, account, dc, build_method, template, name, name_fr, name_de, name_nl, printed_name, printed_name_fr, printed_name_de, printed_name_nl
- ledger.Journals.insert (viewable for all except anonymous) : ref, name, name_fr, name_de, name_nl, trade_type, voucher_type
- ledger.Situation.show (viewable for nobody) : body
- newcomers.AvailableCoachesByClient.assign_coach (viewable for 200, 220, 300, admin) : notify_subject, notify_body, notify_silent
- newcomers.Faculties.detail (viewable for 110, 410, admin) : id, name, name_fr, name_de, name_nl, weight
- newcomers.Faculties.insert (viewable for 110, 410, admin) : name, name_fr, name_de, name_nl, weight
- notes.EventTypes.insert (viewable for 110, 410, admin) : id, name, name_fr, name_de, name_nl, remark
- notes.NoteTypes.detail (viewable for 110, 410, admin) : id, name, name_fr, name_de, name_nl, build_method, template, special_type, email_template, attach_to_email, remark
- notes.NoteTypes.insert (viewable for 110, 410, admin) : name, name_fr, name_de, name_nl, build_method
- notes.Notes.detail (viewable for all except anonymous) : date, time, event_type, type, project, subject, company, contact_person, user, language, build_time, id, body, UploadsByController
- notes.Notes.insert (viewable for all except anonymous) : event_type, type, subject, project
- outbox.Mails.detail (viewable for 110, 410, admin) : subject, project, date, user, sent, id, owner, AttachmentsByMail, UploadsByController, body
- outbox.Mails.insert (viewable for 110, 410, admin) : project, subject, body
- pcsw.ClientContactTypes.insert (viewable for 110, 410, admin) : id, name, name_fr, name_de, name_nl
- pcsw.ClientStates.wf1 (viewable for 200, 300, admin) : reason, remark
- pcsw.Clients.create_visit (viewable for all except anonymous) : user, summary
- pcsw.Clients.detail (viewable for all except anonymous) : overview, gender, id, first_name, middle_name, last_name, birth_date, age, national_id, nationality, declared_name, civil_state, birth_country, birth_place, language, email, phone, fax, gsm, image, AgentsByClient, SimilarClients, LinksByHuman, cbss_relations, MembersByPerson, workflow_buttons, broker, faculty, refusal_reason, in_belgium_since, residence_type, residence_until, group, is_seeking, unemployed_since, work_permit_suspended_until, needs_residence_permit, needs_work_permit, UploadsByClient, skills, obstacles, ExcerptsByProject, VouchersByProject, activity, client_state, noble_condition, unavailable_until, unavailable_why, is_obsolete, created, modified, remarks
- pcsw.Clients.insert (viewable for all except anonymous) : first_name, last_name, national_id, gender, language
- pcsw.Clients.merge_row (viewable for admin) : merge_to, aids_SimpleConfirmation, aids_IncomeConfirmation, aids_RefundConfirmation, pcsw_Coaching, pcsw_Dispense, dupable_clients_Word, reason
- pcsw.CoachingEndings.insert (viewable for 110, 410, admin) : id, name, name_fr, name_de, name_nl, seqno
- pcsw.Coachings.create_visit (viewable for 110, 410, admin) : user, summary
- plausibility.Checkers.detail (viewable for admin) : value, name, text
- polls.AnswerRemarks.insert (viewable for all except anonymous) : remark, response, question
- polls.ChoiceSets.insert (viewable for admin) : name, name_fr, name_de, name_nl
- polls.Polls.detail (viewable for all except anonymous) : ref, title, workflow_buttons, details, default_choiceset, default_multiple_choices, id, user, created, modified, state
- polls.Polls.insert (viewable for all except anonymous) : ref, title, default_choiceset, default_multiple_choices, questions_to_add
- polls.Questions.insert (viewable for admin) : poll, number, is_heading, choiceset, multiple_choices, title, details
- polls.Responses.detail (viewable for all except anonymous) : poll, partner, date, workflow_buttons, AnswersByResponse, user, state, remark
- polls.Responses.insert (viewable for all except anonymous) : user, date, poll
- properties.PropGroups.insert (viewable for admin) : id, name, name_fr, name_de, name_nl
- properties.PropTypes.insert (viewable for admin) : id, name, name_fr, name_de, name_nl, choicelist, default_value
- reception.BusyVisitors.detail (viewable for all except anonymous) : event, client, role, state, remark, workflow_buttons
- reception.GoneVisitors.detail (viewable for all except anonymous) : event, client, role, state, remark, workflow_buttons
- reception.MyWaitingVisitors.detail (viewable for all except anonymous, 210, 220) : event, client, role, state, remark, workflow_buttons
- reception.WaitingVisitors.detail (viewable for all except anonymous) : event, client, role, state, remark, workflow_buttons
- system.SiteConfigs.detail (viewable for admin) : site_company, next_partner_id, job_office, master_budget, signer1, signer2, signer1_function, signer2_function, system_note_type, default_build_method, propgroup_skills, propgroup_softskills, propgroup_obstacles, residence_permit_upload_type, work_permit_upload_type, driving_licence_upload_type, default_event_type, prompt_calendar, client_guestrole, team_guestrole, cbss_org_unit, sector, ssdn_user_id, ssdn_email, cbss_http_username, cbss_http_password
- tinymce.TextFieldTemplates.detail (viewable for admin) : id, name, user, description, text
- tinymce.TextFieldTemplates.insert (viewable for admin) : name, user
- uploads.AllUploads.detail (viewable for 110, 410, admin) : file, user, upload_area, type, description, owner
- uploads.AllUploads.insert (viewable for 110, 410, admin) : type, description, file, user
- uploads.UploadTypes.detail (viewable for 110, 410, admin) : id, upload_area, shortcut, name, name_fr, name_de, name_nl, warn_expiry_unit, warn_expiry_value, wanted, max_number
- uploads.UploadTypes.insert (viewable for 110, 410, admin) : upload_area, name, name_fr, name_de, name_nl, warn_expiry_unit, warn_expiry_value
- uploads.Uploads.detail (viewable for all except anonymous) : user, project, id, type, description, start_date, end_date, needed, company, contact_person, contact_role, file, owner, remark
- uploads.Uploads.insert (viewable for all except anonymous) : type, file, start_date, end_date, description
- uploads.UploadsByClient.insert (viewable for all except anonymous) : file, type, end_date, description
- uploads.UploadsByController.insert (viewable for all except anonymous) : file, type, end_date, description
- users.Users.change_password (viewable for admin) : current, new1, new2
- users.Users.detail (viewable for admin) : username, profile, partner, first_name, last_name, initials, email, language, id, created, modified, remarks, event_type, access_class, calendar, newcomer_quota, coaching_type, coaching_supervisor, newcomer_consultations, newcomer_appointments
- users.Users.insert (viewable for admin) : username, email, first_name, last_name, partner, language, profile
- vatless.Invoices.detail (viewable for all except anonymous) : id, date, project, partner, user, due_date, your_ref, workflow_buttons, amount, journal, year, number, narration, state
- vatless.Invoices.insert (viewable for all except anonymous) : journal, project, partner, date, amount
- vatless.InvoicesByJournal.insert (viewable for all except anonymous) : project, partner, date, amount
<BLANKLINE>


Permissions
===========

Test whether everybody can display the detail of a client:

>>> o = pcsw.Client.objects.get(id=177)
>>> r = dd.plugins.extjs.renderer
>>> for u in 'robin', 'alicia', 'theresia', 'caroline', 'kerstin':
...     print(E.tostring(rt.login(u, renderer=r).obj2html(o)))
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
<a href="javascript:Lino.pcsw.Clients.detail.run(null,{ &quot;record_id&quot;: 177 })">BRECHT Bernd (177)</a>
<a href="javascript:Lino.pcsw.Clients.detail.run(null,{ &quot;record_id&quot;: 177 })">BRECHT Bernd (177)</a>
<a href="javascript:Lino.pcsw.Clients.detail.run(null,{ &quot;record_id&quot;: 177 })">BRECHT Bernd (177)</a>
<a href="javascript:Lino.pcsw.Clients.detail.run(null,{ &quot;record_id&quot;: 177 })">BRECHT Bernd (177)</a>
<a href="javascript:Lino.pcsw.Clients.detail.run(null,{ &quot;record_id&quot;: 177 })">BRECHT Bernd (177)</a>

Miscellaneous tests
===================

See :blogref:`20130508`:

>>> for model in (debts.Entry,):
...     for o in model.objects.all():
...         o.full_clean()

Default template for excerpts
=============================

Check whether Lino returns the right default template for excerpts.

In :mod:`lino.modlib.excerpts` we define a template
:xfile:`excerpts/Default.odt`, but :mod:`lino_welfare.modlib.welfare`
overrides this template.

The rule is that **the *last* plugin wins** when Lino searches for
templates.

This means that if we want to see the welfare-specific version, our
:meth:`get_installed_apps <lino.core.site.Site.get_installed_apps>` in
:mod:`lino_welare.projects.std.settings` must yield
:mod:`lino_welfare.modlib.welfare` **after**
:mod:`lino.modlib.excerpts`.

The following test verifies this rule:

>>> print(settings.SITE.find_config_file('Default.odt', 'excerpts'))
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF -SKIP
/.../welfare/config/excerpts/Default.odt

