.. _welfare.tested.general:

==================================
Lino Welfare General (tested tour)
==================================

.. How to test only this document:

  $ python setup.py test -s tests.DocsTests.test_general

.. contents:: 
   :local:
   :depth: 2

A tested document
=================

.. include:: /include/tested.rst

>>> from __future__ import print_function
>>> import os
>>> os.environ['DJANGO_SETTINGS_MODULE'] = \
...    'lino_welfare.projects.std.settings.doctests'
>>> from lino.api.doctest import *

The test database
=================

Test whether :meth:`get_db_overview_rst
<lino.core.site.Site.get_db_overview_rst>` returns the expected
result:

>>> print(settings.SITE.get_db_overview_rst()) 
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF -SKIP
54 apps: staticfiles, about, bootstrap3, lino, system, contenttypes, humanize, users, changes, countries, properties, contacts, addresses, uploads, outbox, excerpts, extensible, cal, reception, accounts, badges, iban, sepa, vat, ledger, finan, boards, welfare, sales, pcsw, languages, cv, integ, isip, jobs, art61, immersion, active_job_search, courses, newcomers, cbss, households, humanlinks, debts, notes, aids, polls, beid, davlink, appypod, export_excel, dupable_clients, plausibility, tinymce.
151 models:
============================== =============================== ========= =======
 Name                           Default table                   #fields   #rows
------------------------------ ------------------------------- --------- -------
 accounts.Account               accounts.Accounts               19        58
 accounts.Chart                 accounts.Charts                 5         2
 accounts.Group                 accounts.Groups                 9         14
 active_job_search.Proof        active_job_search.Proofs        7         10
 addresses.Address              addresses.Addresses             16        167
 aids.AidType                   aids.AidTypes                   23        11
 aids.Category                  aids.Categories                 5         3
 aids.Granting                  aids.GrantingsByX               12        51
 aids.IncomeConfirmation        aids.IncomeConfirmations        17        48
 aids.RefundConfirmation        aids.RefundConfirmations        18        12
 aids.SimpleConfirmation        aids.SimpleConfirmations        15        19
 art61.Contract                 art61.Contracts                 30        4
 art61.ContractType             art61.ContractTypes             9         1
 badges.Award                   badges.Awards                   6         0
 badges.Badge                   badges.Badges                   5         0
 boards.Board                   boards.Boards                   7         3
 boards.Member                  boards.Members                  4         0
 cal.Calendar                   cal.Calendars                   7         11
 cal.Event                      cal.OneEvent                    24        505
 cal.EventType                  cal.EventTypes                  19        8
 cal.Guest                      cal.Guests                      9         492
 cal.GuestRole                  cal.GuestRoles                  5         4
 cal.Priority                   cal.Priorities                  6         4
 cal.RecurrentEvent             cal.RecurrentEvents             22        9
 cal.RemoteCalendar             cal.RemoteCalendars             7         0
 cal.Room                       cal.Rooms                       5         0
 cal.Subscription               cal.Subscriptions               4         9
 cal.Task                       cal.Tasks                       19        33
 cbss.IdentifyPersonRequest     cbss.IdentifyPersonRequests     20        5
 cbss.ManageAccessRequest       cbss.ManageAccessRequests       23        1
 cbss.Purpose                   cbss.Purposes                   7         106
 cbss.RetrieveTIGroupsRequest   cbss.RetrieveTIGroupsRequests   14        2
 cbss.Sector                    cbss.Sectors                    11        209
 changes.Change                 changes.Changes                 9         0
 contacts.Company               contacts.Companies              32        49
 contacts.CompanyType           contacts.CompanyTypes           9         16
 contacts.Partner               contacts.Partners               28        172
 contacts.Person                contacts.Persons                35        109
 contacts.Role                  contacts.Roles                  4         10
 contacts.RoleType              contacts.RoleTypes              6         5
 contenttypes.ContentType       contenttypes.ContentTypes       4         152
 contenttypes.HelpText          contenttypes.HelpTexts          4         5
 countries.Country              countries.Countries             9         8
 countries.Place                countries.Places                10        78
 courses.Course                 courses.Courses                 5         3
 courses.CourseContent          courses.CourseContents          2         2
 courses.CourseOffer            courses.CourseOffers            6         3
 courses.CourseProvider         courses.CourseProviders         33        2
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
 excerpts.Excerpt               excerpts.ExcerptsByX            12        13
 excerpts.ExcerptType           excerpts.ExcerptTypes           18        13
 finan.BankStatement            finan.BankStatements            11        0
 finan.BankStatementItem        finan.BankStatementItemTable    11        0
 finan.Grouper                  finan.Groupers                  10        0
 finan.GrouperItem              finan.GrouperItemTable          10        0
 finan.JournalEntry             finan.FinancialVouchers         9         0
 finan.JournalEntryItem         finan.JournalEntryItemTable     11        0
 finan.PaymentOrder             finan.PaymentOrders             11        0
 finan.PaymentOrderItem         finan.PaymentOrderItemTable     10        0
 households.Household           households.Households           31        14
 households.Member              households.Members              13        63
 households.Type                households.Types                5         6
 humanlinks.Link                humanlinks.Links                4         59
 immersion.Contract             immersion.Contracts             25        7
 immersion.ContractType         immersion.ContractTypes         8         3
 immersion.Goal                 immersion.Goals                 5         4
 isip.Contract                  isip.Contracts                  22        26
 isip.ContractEnding            isip.ContractEndings            6         4
 isip.ContractPartner           isip.ContractPartners           6         30
 isip.ContractType              isip.ContractTypes              10        5
 isip.ExamPolicy                isip.ExamPolicies               20        6
 jobs.Candidature               jobs.Candidatures               8         74
 jobs.Contract                  jobs.Contracts                  28        16
 jobs.ContractType              jobs.ContractTypes              11        5
 jobs.Job                       jobs.Jobs                       10        8
 jobs.JobProvider               jobs.JobProviders               33        3
 jobs.JobType                   jobs.JobTypes                   5         5
 jobs.Offer                     jobs.Offers                     9         1
 jobs.Schedule                  jobs.Schedules                  5         3
 languages.Language             languages.Languages             6         5
 ledger.AccountInvoice          ledger.AccountInvoices          18        20
 ledger.InvoiceItem             ledger.InvoiceItemTable         9         0
 ledger.Journal                 ledger.Journals                 20        2
 ledger.MatchRule               ledger.MatchRules               3         0
 ledger.Movement                ledger.Movements                9         0
 ledger.Voucher                 ledger.Vouchers                 7         20
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
 pcsw.Client                    pcsw.Clients                    69        63
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
 system.SiteConfig              system.SiteConfigs              30        1
 tinymce.TextFieldTemplate      tinymce.TextFieldTemplates      5         2
 uploads.Upload                 uploads.Uploads                 17        11
 uploads.UploadType             uploads.UploadTypes             11        9
 users.Authority                users.Authorities               3         3
 users.User                     users.Users                     21        11
 vat.PaymentTerm                vat.PaymentTerms                8         0
 vat.VatRule                    vat.VatRules                    9         0
============================== =============================== ========= =======
<BLANKLINE>



List of window layouts
======================


The :class:`lino.modlib.about.models.WindowActions` table lists
information about all detail layouts, insert layouts and action
parameter layouts.

The primary purpose of the following is to get a warning when anything
changes.


>>> settings.SITE.catch_layout_exceptions = False
>>> rt.show(about.WindowActions)
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF -SKIP
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| Name                                            | Viewable for                        | Fields                                             |
+=================================================+=====================================+====================================================+
| about.About.show                                | all                                 | server_status                                      |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| about.Models.detail                             | all except anonymous                | app name docstring rows                            |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| accounts.Accounts.detail                        | admin                               | ref name name_fr name_de name_nl group type        |
|                                                 |                                     | required_for_household required_for_person periods |
|                                                 |                                     | default_amount                                     |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| accounts.Accounts.insert                        | all except anonymous                | ref group type name name_fr name_de name_nl        |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| accounts.Charts.detail                          | admin                               | id name name_fr name_de name_nl                    |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| accounts.Charts.insert                          | all except anonymous                | name name_fr name_de name_nl                       |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| accounts.Groups.detail                          | admin                               | ref name name_fr name_de name_nl id account_type   |
|                                                 |                                     | entries_layout                                     |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| accounts.Groups.insert                          | all except anonymous                | name name_fr name_de name_nl account_type ref      |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| active_job_search.Proofs.insert                 | all except anonymous                | date client company id spontaneous response        |
|                                                 |                                     | remarks                                            |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| addresses.Addresses.detail                      | admin                               | country city zip_code addr1 street street_no       |
|                                                 |                                     | street_box addr2 address_type remark data_source   |
|                                                 |                                     | partner                                            |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| addresses.Addresses.insert                      | all except anonymous                | country city street street_no street_box           |
|                                                 |                                     | address_type remark                                |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| aids.AidTypes.detail                            | admin                               | id short_name confirmation_type name name_fr       |
|                                                 |                                     | name_de name_nl excerpt_title excerpt_title_fr     |
|                                                 |                                     | excerpt_title_de excerpt_title_nl print_directly   |
|                                                 |                                     | is_integ_duty is_urgent confirmed_by_primary_coach |
|                                                 |                                     | board body_template company contact_person         |
|                                                 |                                     | contact_role pharmacy_type                         |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| aids.AidTypes.insert                            | all except anonymous                | name name_fr name_de name_nl confirmation_type     |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| aids.Categories.insert                          | all except anonymous                | id name name_fr name_de name_nl                    |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| aids.Grantings.detail                           | admin                               | id client user signer workflow_buttons             |
|                                                 |                                     | request_date board decision_date aid_type category |
|                                                 |                                     | start_date end_date custom_actions                 |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| aids.Grantings.insert                           | all except anonymous                | client aid_type signer board decision_date         |
|                                                 |                                     | start_date end_date                                |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| aids.GrantingsByClient.insert                   | all except anonymous                | aid_type board decision_date start_date end_date   |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| aids.IncomeConfirmations.insert                 | all except anonymous                | client user signer workflow_buttons printed        |
|                                                 |                                     | company contact_person language granting           |
|                                                 |                                     | start_date end_date category amount id remark      |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| aids.IncomeConfirmationsByGranting.insert       | all except anonymous                | client granting start_date end_date category       |
|                                                 |                                     | amount company contact_person language remark      |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| aids.RefundConfirmations.insert                 | all except anonymous                | id client user signer workflow_buttons granting    |
|                                                 |                                     | start_date end_date doctor_type doctor pharmacy    |
|                                                 |                                     | company contact_person language printed remark     |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| aids.RefundConfirmationsByGranting.insert       | all except anonymous                | start_date end_date doctor_type doctor pharmacy    |
|                                                 |                                     | company contact_person language printed remark     |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| aids.SimpleConfirmations.insert                 | all except anonymous                | id client user signer workflow_buttons granting    |
|                                                 |                                     | start_date end_date company contact_person         |
|                                                 |                                     | language printed remark                            |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| aids.SimpleConfirmationsByGranting.insert       | all except anonymous                | start_date end_date company contact_person         |
|                                                 |                                     | language remark                                    |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| art61.ContractTypes.insert                      | 100, 110, admin                     | id name name_fr name_de name_nl ref                |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| art61.Contracts.detail                          | 100, 110, admin                     | id client user language type company               |
|                                                 |                                     | contact_person contact_role applies_from duration  |
|                                                 |                                     | applies_until exam_policy job_title status         |
|                                                 |                                     | cv_duration regime reference_person printed        |
|                                                 |                                     | date_decided date_issued date_ended ending         |
|                                                 |                                     | subsidize_10 subsidize_20 subsidize_30             |
|                                                 |                                     | responsibilities                                   |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| art61.Contracts.insert                          | 100, 110, admin                     | client company type                                |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| boards.Boards.detail                            | admin                               | id name name_fr name_de name_nl                    |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| boards.Boards.insert                            | all except anonymous                | name name_fr name_de name_nl                       |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| cal.Calendars.detail                            | 110, 410, admin                     | name name_fr name_de name_nl color id description  |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| cal.Calendars.insert                            | all except anonymous                | name name_fr name_de name_nl color                 |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| cal.EventTypes.detail                           | 110, 410, admin                     | name name_fr name_de name_nl event_label           |
|                                                 |                                     | event_label_fr event_label_de event_label_nl       |
|                                                 |                                     | max_conflicting all_rooms locks_user id            |
|                                                 |                                     | invite_client is_appointment email_template        |
|                                                 |                                     | attach_to_email                                    |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| cal.EventTypes.insert                           | all except anonymous                | name name_fr name_de name_nl invite_client         |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| cal.Events.detail                               | 110, 410, admin                     | event_type summary project start_date start_time   |
|                                                 |                                     | end_date end_time user assigned_to room priority   |
|                                                 |                                     | access_class transparent owner workflow_buttons    |
|                                                 |                                     | description id created modified state              |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| cal.Events.insert                               | all except anonymous                | summary start_date start_time end_date end_time    |
|                                                 |                                     | event_type project                                 |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| cal.EventsByClient.insert                       | all except anonymous                | event_type summary start_date start_time end_date  |
|                                                 |                                     | end_time                                           |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| cal.GuestRoles.insert                           | all except anonymous                | id name name_fr name_de name_nl                    |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| cal.GuestStates.wf1                             | admin                               | notify_subject notify_body notify_silent           |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| cal.GuestStates.wf2                             | admin                               | notify_subject notify_body notify_silent           |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| cal.Guests.checkin                              | admin                               | notify_subject notify_body notify_silent           |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| cal.Guests.detail                               | admin                               | event partner role state remark workflow_buttons   |
|                                                 |                                     | waiting_since busy_since gone_since                |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| cal.Guests.insert                               | all except anonymous                | event partner role                                 |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| cal.RecurrentEvents.detail                      | 110, 410, admin                     | name name_fr name_de name_nl id user event_type    |
|                                                 |                                     | start_date start_time end_date end_time every_unit |
|                                                 |                                     | every max_events monday tuesday wednesday thursday |
|                                                 |                                     | friday saturday sunday description                 |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| cal.RecurrentEvents.insert                      | all except anonymous                | name name_fr name_de name_nl start_date end_date   |
|                                                 |                                     | every_unit event_type                              |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| cal.Rooms.insert                                | all except anonymous                | id name name_fr name_de name_nl                    |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| cal.Tasks.detail                                | 110, 410, admin                     | start_date due_date id workflow_buttons summary    |
|                                                 |                                     | project user delegated owner created modified      |
|                                                 |                                     | description                                        |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| cal.Tasks.insert                                | all except anonymous                | summary user project                               |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| cal.TasksByController.insert                    | all except anonymous                | summary start_date due_date user delegated         |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| cbss.IdentifyPersonRequests.detail              | all except anonymous, 210, 300      | id person user environment sent status ticket      |
|                                                 |                                     | national_id first_name middle_name last_name       |
|                                                 |                                     | birth_date tolerance gender response_xml           |
|                                                 |                                     | info_messages debug_messages                       |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| cbss.IdentifyPersonRequests.insert              | all except anonymous, 210, 300      | person national_id first_name middle_name          |
|                                                 |                                     | last_name birth_date tolerance gender              |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| cbss.ManageAccessRequests.detail                | all except anonymous, 210, 300      | id person user environment sent status ticket      |
|                                                 |                                     | action start_date end_date purpose query_register  |
|                                                 |                                     | national_id sis_card_no id_card_no first_name      |
|                                                 |                                     | last_name birth_date result response_xml           |
|                                                 |                                     | info_messages debug_messages                       |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| cbss.ManageAccessRequests.insert                | all except anonymous, 210, 300      | person action start_date end_date purpose          |
|                                                 |                                     | query_register national_id sis_card_no id_card_no  |
|                                                 |                                     | first_name last_name birth_date                    |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| cbss.RetrieveTIGroupsRequests.detail            | all except anonymous                | id person user environment sent status ticket      |
|                                                 |                                     | national_id language history response_xml          |
|                                                 |                                     | info_messages debug_messages                       |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| cbss.RetrieveTIGroupsRequests.insert            | all except anonymous                | person national_id language history                |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| changes.Changes.detail                          | admin                               | time user type master object id diff               |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| contacts.Companies.detail                       | all except anonymous                | overview prefix name type vat_id                   |
|                                                 |                                     | client_contact_type url email phone gsm fax        |
|                                                 |                                     | remarks id language activity is_obsolete created   |
|                                                 |                                     | modified VouchersByPartner                         |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| contacts.Companies.insert                       | all except anonymous                | name language email type id                        |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| contacts.Companies.merge_row                    | admin                               | merge_to reason                                    |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| contacts.Partners.detail                        | all except anonymous                | overview id language activity client_contact_type  |
|                                                 |                                     | url email phone gsm fax country region city        |
|                                                 |                                     | zip_code addr1 street_prefix street street_no      |
|                                                 |                                     | street_box addr2 remarks is_obsolete created       |
|                                                 |                                     | modified VouchersByPartner                         |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| contacts.Partners.insert                        | all except anonymous                | name language email                                |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| contacts.Persons.create_household               | all except anonymous                | partner type head                                  |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| contacts.Persons.detail                         | all except anonymous                | overview title first_name middle_name last_name    |
|                                                 |                                     | gender birth_date age id language email phone gsm  |
|                                                 |                                     | fax MembersByPerson LinksByHuman remarks activity  |
|                                                 |                                     | url client_contact_type is_obsolete created        |
|                                                 |                                     | modified VouchersByPartner                         |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| contacts.Persons.insert                         | all except anonymous                | first_name last_name gender language               |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| contenttypes.ContentTypes.insert                | all except anonymous                | id name app_label model base_classes               |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| countries.Countries.detail                      | all except anonymous                | isocode name name_fr name_de name_nl short_code    |
|                                                 |                                     | inscode actual_country                             |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| countries.Countries.insert                      | all except anonymous                | isocode inscode name name_fr name_de name_nl       |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| countries.Places.insert                         | all except anonymous                | name name_fr name_de name_nl country type parent   |
|                                                 |                                     | zip_code id                                        |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| courses.CourseContents.insert                   | all except anonymous, 200, 210, 300 | id name                                            |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| courses.CourseOffers.detail                     | all except anonymous, 200, 210, 300 | id title content provider guest_role description   |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| courses.CourseOffers.insert                     | all except anonymous, 200, 210, 300 | provider content title                             |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| courses.CourseProviders.detail                  | all except anonymous, 200, 210, 300 | overview prefix name type vat_id                   |
|                                                 |                                     | client_contact_type url email phone gsm fax        |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| courses.CourseRequests.insert                   | all except anonymous, 200, 210, 300 | date_submitted person content offer urgent course  |
|                                                 |                                     | state date_ended id remark UploadsByController     |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| courses.Courses.detail                          | admin                               | id start_date offer title remark                   |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| courses.Courses.insert                          | all except anonymous, 200, 210, 300 | start_date offer title                             |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| cv.Durations.insert                             | all except anonymous                | id name name_fr name_de name_nl                    |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| cv.EducationLevels.insert                       | all except anonymous                | name name_fr name_de name_nl is_study is_training  |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| cv.Experiences.insert                           | all except anonymous                | person start_date end_date termination_reason      |
|                                                 |                                     | company country city sector function title status  |
|                                                 |                                     | duration regime is_training remarks                |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| cv.Functions.insert                             | all except anonymous                | id name name_fr name_de name_nl sector remark      |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| cv.Regimes.insert                               | all except anonymous                | id name name_fr name_de name_nl                    |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| cv.Sectors.insert                               | all except anonymous                | id name name_fr name_de name_nl remark             |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| cv.Statuses.insert                              | all except anonymous                | id name name_fr name_de name_nl                    |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| cv.Studies.insert                               | all except anonymous                | person start_date end_date type content            |
|                                                 |                                     | education_level state school country city remarks  |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| cv.StudyTypes.detail                            | admin                               | name name_fr name_de name_nl id education_level    |
|                                                 |                                     | is_study is_training                               |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| cv.StudyTypes.insert                            | all except anonymous                | name name_fr name_de name_nl is_study is_training  |
|                                                 |                                     | education_level                                    |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| cv.Trainings.detail                             | all except anonymous                | person start_date end_date type state certificates |
|                                                 |                                     | sector function school country city remarks        |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| cv.Trainings.insert                             | all except anonymous                | person start_date end_date type state certificates |
|                                                 |                                     | sector function school country city                |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| debts.Budgets.detail                            | admin                               | date partner id user intro ResultByBudget          |
|                                                 |                                     | DebtsByBudget AssetsByBudgetSummary conclusion     |
|                                                 |                                     | dist_amount printed total_debt                     |
|                                                 |                                     | include_yearly_incomes print_empty_rows            |
|                                                 |                                     | print_todos DistByBudget data_box summary_box      |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| debts.Budgets.insert                            | 300, admin                          | partner date user                                  |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| excerpts.ExcerptTypes.detail                    | admin                               | id name name_fr name_de name_nl content_type       |
|                                                 |                                     | build_method template body_template email_template |
|                                                 |                                     | shortcut primary print_directly certifying         |
|                                                 |                                     | print_recipient backward_compat attach_to_email    |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| excerpts.ExcerptTypes.insert                    | all except anonymous                | name name_fr name_de name_nl content_type primary  |
|                                                 |                                     | certifying build_method template body_template     |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| excerpts.Excerpts.detail                        | admin                               | id excerpt_type project user build_method company  |
|                                                 |                                     | contact_person language owner build_time           |
|                                                 |                                     | body_template_content                              |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| finan.BankStatements.detail                     | all except anonymous                | date balance1 balance2 user workflow_buttons id    |
|                                                 |                                     | journal year number                                |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| finan.BankStatements.insert                     | all except anonymous                | date user balance1 balance2                        |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| finan.FinancialVouchers.detail                  | all except anonymous                | date user narration workflow_buttons id journal    |
|                                                 |                                     | year number                                        |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| finan.FinancialVouchers.insert                  | all except anonymous                | date user narration                                |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| finan.Groupers.detail                           | all except anonymous                | date partner user workflow_buttons id journal year |
|                                                 |                                     | number                                             |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| finan.Groupers.insert                           | all except anonymous                | date user partner                                  |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| finan.PaymentOrders.detail                      | all except anonymous                | date user narration total execution_date           |
|                                                 |                                     | workflow_buttons id journal year number            |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| households.Households.detail                    | all except anonymous                | type prefix name id                                |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| households.HouseholdsByType.detail              | all except anonymous                | type name language id country region city zip_code |
|                                                 |                                     | street_prefix street street_no street_box addr2    |
|                                                 |                                     | phone gsm email url remarks                        |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| households.Types.insert                         | all except anonymous                | name name_fr name_de name_nl                       |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| humanlinks.Links.insert                         | all except anonymous                | parent child type                                  |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| immersion.ContractTypes.detail                  | 110, admin                          | id name name_fr name_de name_nl exam_policy        |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| immersion.ContractTypes.insert                  | 100, 110, admin                     | name name_fr name_de name_nl exam_policy           |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| immersion.Contracts.detail                      | 100, 110, admin                     | id client user language type goal company          |
|                                                 |                                     | contact_person contact_role applies_from           |
|                                                 |                                     | applies_until exam_policy sector function          |
|                                                 |                                     | reference_person printed date_decided date_issued  |
|                                                 |                                     | date_ended ending responsibilities                 |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| immersion.Contracts.insert                      | 100, 110, admin                     | client company type goal                           |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| immersion.Goals.insert                          | 100, 110, admin                     | id name name_fr name_de name_nl                    |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| integ.ActivityReport.show                       | 100, 110, admin                     | body                                               |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| isip.ContractEndings.insert                     | 100, 110, admin                     | name use_in_isip use_in_jobs is_success            |
|                                                 |                                     | needs_date_ended                                   |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| isip.ContractPartners.insert                    | all except anonymous                | company contact_person contact_role duties_company |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| isip.ContractTypes.insert                       | 100, 110, admin                     | id ref exam_policy needs_study_type name name_fr   |
|                                                 |                                     | name_de name_nl full_name                          |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| isip.Contracts.detail                           | 100, 110, admin                     | id client type user user_asd study_type            |
|                                                 |                                     | applies_from applies_until exam_policy language    |
|                                                 |                                     | date_decided date_issued printed date_ended ending |
|                                                 |                                     | stages goals duties_asd duties_dsbe duties_person  |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| isip.Contracts.insert                           | 100, 110, admin                     | client type                                        |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| isip.ExamPolicies.insert                        | 100, 110, admin                     | id name name_fr name_de name_nl max_events every   |
|                                                 |                                     | every_unit event_type monday tuesday wednesday     |
|                                                 |                                     | thursday friday saturday sunday                    |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| jobs.ContractTypes.insert                       | 100, 110, admin                     | id name name_fr name_de name_nl ref                |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| jobs.Contracts.detail                           | 100, 110, admin                     | id client user user_asd language job type company  |
|                                                 |                                     | contact_person contact_role applies_from duration  |
|                                                 |                                     | applies_until exam_policy regime schedule          |
|                                                 |                                     | hourly_rate refund_rate reference_person printed   |
|                                                 |                                     | date_decided date_issued date_ended ending         |
|                                                 |                                     | responsibilities                                   |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| jobs.Contracts.insert                           | 100, 110, admin                     | client job                                         |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| jobs.JobProviders.detail                        | 100, 110, admin                     | overview prefix name type vat_id                   |
|                                                 |                                     | client_contact_type url email phone gsm fax        |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| jobs.JobTypes.insert                            | 100, 110, admin                     | id name is_social                                  |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| jobs.Jobs.insert                                | 100, 110, admin                     | name provider contract_type type id sector         |
|                                                 |                                     | function capacity hourly_rate remark               |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| jobs.JobsOverview.show                          | 100, 110, admin                     | preview                                            |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| jobs.Offers.insert                              | 100, 110, admin                     | name provider sector function selection_from       |
|                                                 |                                     | selection_until start_date remark                  |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| jobs.OldJobsOverview.show                       | 100, 110, admin                     | body                                               |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| jobs.Schedules.insert                           | 100, 110, admin                     | id name name_fr name_de name_nl                    |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| languages.Languages.insert                      | all except anonymous                | id iso2 name name_fr name_de name_nl               |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| ledger.AccountInvoices.detail                   | all except anonymous                | id date partner user due_date your_ref vat_regime  |
|                                                 |                                     | total_base total_vat total_incl workflow_buttons   |
|                                                 |                                     | journal year number narration                      |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| ledger.AccountInvoices.insert                   | all except anonymous                | journal partner date total_incl                    |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| ledger.ActivityReport.show                      | nobody                              | body                                               |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| ledger.InvoicesByJournal.insert                 | all except anonymous                | partner date total_incl                            |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| ledger.Journals.detail                          | all except anonymous                | ref trade_type seqno id voucher_type journal_group |
|                                                 |                                     | force_sequence account dc build_method template    |
|                                                 |                                     | name name_fr name_de name_nl printed_name          |
|                                                 |                                     | printed_name_fr printed_name_de printed_name_nl    |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| ledger.Journals.insert                          | all except anonymous                | ref name name_fr name_de name_nl trade_type        |
|                                                 |                                     | voucher_type                                       |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| ledger.Situation.show                           | nobody                              | body                                               |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| newcomers.AvailableCoachesByClient.assign_coach | 200, 300, admin                     | notify_subject notify_body notify_silent           |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| newcomers.Faculties.detail                      | admin                               | id name name_fr name_de name_nl weight             |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| newcomers.Faculties.insert                      | 200, 300, admin                     | name name_fr name_de name_nl weight                |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| notes.EventTypes.insert                         | all except anonymous                | id name name_fr name_de name_nl remark             |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| notes.NoteTypes.detail                          | admin                               | id name name_fr name_de name_nl build_method       |
|                                                 |                                     | template special_type email_template               |
|                                                 |                                     | attach_to_email remark                             |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| notes.NoteTypes.insert                          | all except anonymous                | name name_fr name_de name_nl build_method          |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| notes.Notes.detail                              | all except anonymous                | date time event_type type project subject company  |
|                                                 |                                     | contact_person user language build_time id body    |
|                                                 |                                     | UploadsByController                                |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| notes.Notes.insert                              | all except anonymous                | event_type type subject project                    |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| outbox.Mails.detail                             | 110, 410, admin                     | subject project date user sent id owner            |
|                                                 |                                     | AttachmentsByMail UploadsByController body         |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| outbox.Mails.insert                             | all except anonymous                | project subject body                               |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| pcsw.ClientContactTypes.insert                  | all except anonymous                | id name name_fr name_de name_nl                    |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| pcsw.ClientStates.wf1                           | 200, 300, admin                     | reason remark                                      |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| pcsw.Clients.create_visit                       | all except anonymous                | user summary                                       |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| pcsw.Clients.detail                             | all except anonymous                | overview gender id first_name middle_name          |
|                                                 |                                     | last_name birth_date age national_id nationality   |
|                                                 |                                     | declared_name civil_state birth_country            |
|                                                 |                                     | birth_place language email phone fax gsm image     |
|                                                 |                                     | AgentsByClient SimilarClients LinksByHuman         |
|                                                 |                                     | cbss_relations MembersByPerson workflow_buttons    |
|                                                 |                                     | broker faculty refusal_reason in_belgium_since     |
|                                                 |                                     | residence_type residence_until group is_seeking    |
|                                                 |                                     | unemployed_since work_permit_suspended_until       |
|                                                 |                                     | needs_residence_permit needs_work_permit           |
|                                                 |                                     | UploadsByClient skills obstacles ExcerptsByProject |
|                                                 |                                     | activity client_state noble_condition              |
|                                                 |                                     | unavailable_until unavailable_why is_obsolete      |
|                                                 |                                     | created modified remarks                           |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| pcsw.Clients.insert                             | all except anonymous                | first_name last_name national_id gender language   |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| pcsw.Clients.merge_row                          | admin                               | merge_to aids_SimpleConfirmation                   |
|                                                 |                                     | aids_IncomeConfirmation aids_RefundConfirmation    |
|                                                 |                                     | pcsw_Coaching pcsw_Dispense dupable_clients_Word   |
|                                                 |                                     | reason                                             |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| pcsw.CoachingEndings.insert                     | 100, 110, admin                     | id name name_fr name_de name_nl seqno              |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| pcsw.Coachings.create_visit                     | admin                               | user summary                                       |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| plausibility.Checkers.detail                    | admin                               | value name text                                    |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| polls.AnswerRemarks.insert                      | all except anonymous                | remark response question                           |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| polls.ChoiceSets.insert                         | all except anonymous                | name name_fr name_de name_nl                       |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| polls.Polls.detail                              | all except anonymous                | ref title workflow_buttons details                 |
|                                                 |                                     | default_choiceset default_multiple_choices id user |
|                                                 |                                     | created modified state                             |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| polls.Polls.insert                              | all except anonymous                | ref title default_choiceset                        |
|                                                 |                                     | default_multiple_choices questions_to_add          |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| polls.Questions.insert                          | all except anonymous                | poll number is_heading choiceset multiple_choices  |
|                                                 |                                     | title details                                      |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| polls.Responses.detail                          | all except anonymous                | poll partner date workflow_buttons                 |
|                                                 |                                     | AnswersByResponse user state remark                |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| polls.Responses.insert                          | all except anonymous                | user date poll                                     |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| properties.PropGroups.insert                    | all except anonymous                | id name name_fr name_de name_nl                    |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| properties.PropTypes.insert                     | all except anonymous                | id name name_fr name_de name_nl choicelist         |
|                                                 |                                     | default_value                                      |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| reception.BusyVisitors.detail                   | all except anonymous                | event client role state remark workflow_buttons    |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| reception.GoneVisitors.detail                   | all except anonymous                | event client role state remark workflow_buttons    |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| reception.MyWaitingVisitors.detail              | all except anonymous                | event client role state remark workflow_buttons    |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| reception.WaitingVisitors.detail                | all except anonymous                | event client role state remark workflow_buttons    |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| system.SiteConfigs.detail                       | admin                               | site_company next_partner_id job_office            |
|                                                 |                                     | master_budget signer1 signer2 signer1_function     |
|                                                 |                                     | signer2_function system_note_type                  |
|                                                 |                                     | default_build_method propgroup_skills              |
|                                                 |                                     | propgroup_softskills propgroup_obstacles           |
|                                                 |                                     | residence_permit_upload_type                       |
|                                                 |                                     | work_permit_upload_type                            |
|                                                 |                                     | driving_licence_upload_type default_event_type     |
|                                                 |                                     | prompt_calendar client_guestrole team_guestrole    |
|                                                 |                                     | cbss_org_unit sector ssdn_user_id ssdn_email       |
|                                                 |                                     | cbss_http_username cbss_http_password              |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| tinymce.TextFieldTemplates.detail               | admin                               | id name user description text                      |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| tinymce.TextFieldTemplates.insert               | all except anonymous                | name user                                          |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| uploads.UploadTypes.detail                      | admin                               | id upload_area shortcut name name_fr name_de       |
|                                                 |                                     | name_nl warn_expiry_unit warn_expiry_value wanted  |
|                                                 |                                     | max_number                                         |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| uploads.UploadTypes.insert                      | all except anonymous                | upload_area name name_fr name_de name_nl           |
|                                                 |                                     | warn_expiry_unit warn_expiry_value                 |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| uploads.Uploads.detail                          | admin                               | user project id type description start_date        |
|                                                 |                                     | end_date needed company contact_person             |
|                                                 |                                     | contact_role file owner remark                     |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| uploads.Uploads.insert                          | all except anonymous                | type file start_date end_date description          |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| uploads.UploadsByClient.insert                  | all except anonymous                | file type end_date description                     |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| uploads.UploadsByController.insert              | all except anonymous                | file type end_date description                     |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| users.Users.change_password                     | admin                               | current new1 new2                                  |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| users.Users.detail                              | admin                               | username profile partner first_name last_name      |
|                                                 |                                     | initials email language id created modified        |
|                                                 |                                     | remarks event_type access_class calendar           |
|                                                 |                                     | newcomer_quota coaching_type coaching_supervisor   |
|                                                 |                                     | newcomer_consultations newcomer_appointments       |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
| users.Users.insert                              | all except anonymous                | username email first_name last_name partner        |
|                                                 |                                     | language profile                                   |
+-------------------------------------------------+-------------------------------------+----------------------------------------------------+
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

:mod:`lino.modlib.excerpts` defines a template
:xfile:`excerpts/Default.odt`, and :mod:`lino_welfare.modlib.welfare`
:overrides this template.

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

