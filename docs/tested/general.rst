.. _welfare.tested.general:

=======
General
=======

.. include:: /include/tested.rst

.. How to test only this document:
  $ python setup.py test -s tests.DocsTests.test_general


..  
    >>> import os
    >>> os.environ['DJANGO_SETTINGS_MODULE'] = \
    ...    'lino_welfare.projects.docs.settings.doctests'
    >>> from __future__ import print_function
    >>> from lino.runtime import *
    >>> from django.utils import translation
    >>> from lino.utils.xmlgen.html import E

.. contents:: 
   :local:
   :depth: 3


The test database
=================

Test whether :meth:`get_db_overview_rst
<lino.core.site_def.Site.get_db_overview_rst>` returns the expected
result:

>>> print(settings.SITE.get_db_overview_rst()) 
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
48 apps: about, bootstrap3, lino, system, contenttypes, humanize, users, changes, countries, properties, contacts, addresses, uploads, outbox, extensible, cal, reception, accounts, badges, iban, sepa, excerpts, dedupe, boards, lino_welfare, statbel, sales, pcsw, cv, languages, isip, jobs, integ, active_job_search, courses, newcomers, cbss, households, humanlinks, debts, notes, aids, projects, polls, beid, davlink, appypod, export_excel.
126 models:
============================== =============================== ========= =======
 Name                           Default table                   #fields   #rows
------------------------------ ------------------------------- --------- -------
 accounts.Account               accounts.Accounts               14        49
 accounts.Chart                 accounts.Charts                 5         1
 accounts.Group                 accounts.Groups                 8         7
 active_job_search.Proof        active_job_search.Proofs        7         10
 addresses.Address              addresses.Addresses             16        121
 aids.AidType                   aids.AidTypes                   23        11
 aids.Category                  aids.Categories                 5         3
 aids.Granting                  aids.GrantingsByX               10        55
 aids.IncomeConfirmation        aids.IncomeConfirmations        16        54
 aids.RefundConfirmation        aids.RefundConfirmations        17        12
 aids.SimpleConfirmation        aids.SimpleConfirmations        14        19
 badges.Award                   badges.Awards                   6         0
 badges.Badge                   badges.Badges                   5         0
 boards.Board                   boards.Boards                   7         3
 boards.Member                  boards.Members                  4         0
 cal.Calendar                   cal.Calendars                   7         10
 cal.Event                      cal.OneEvent                    24        597
 cal.EventType                  cal.EventTypes                  19        7
 cal.Guest                      cal.Guests                      9         1042
 cal.GuestRole                  cal.GuestRoles                  5         4
 cal.Priority                   cal.Priorities                  6         4
 cal.RecurrentEvent             cal.RecurrentEvents             22        9
 cal.RemoteCalendar             cal.RemoteCalendars             7         0
 cal.Room                       cal.Rooms                       5         0
 cal.Subscription               cal.Subscriptions               4         9
 cal.Task                       cal.Tasks                       19        34
 cbss.IdentifyPersonRequest     cbss.IdentifyPersonRequests     20        5
 cbss.ManageAccessRequest       cbss.ManageAccessRequests       23        1
 cbss.Purpose                   cbss.Purposes                   7         106
 cbss.RetrieveTIGroupsRequest   cbss.RetrieveTIGroupsRequests   14        2
 cbss.Sector                    cbss.Sectors                    11        209
 changes.Change                 changes.Changes                 9         0
 contacts.Company               contacts.Companies              30        49
 contacts.CompanyType           contacts.CompanyTypes           9         16
 contacts.Partner               contacts.Partners               26        172
 contacts.Person                contacts.Persons                33        109
 contacts.Role                  contacts.Roles                  4         10
 contacts.RoleType              contacts.RoleTypes              6         5
 contenttypes.ContentType       contenttypes.ContentTypes       4         126
 contenttypes.HelpText          contenttypes.HelpTexts          4         5
 countries.Country              countries.Countries             8         8
 countries.Place                countries.Places                10        78
 courses.Course                 courses.Courses                 5         3
 courses.CourseContent          courses.CourseContents          2         2
 courses.CourseOffer            courses.CourseOffers            6         3
 courses.CourseProvider         courses.CourseProviders         31        2
 courses.CourseRequest          courses.CourseRequests          10        20
 cv.Duration                    cv.Durations                    5         5
 cv.EducationLevel              cv.EducationLevels              6         5
 cv.Experience                  cv.Experiences                  17        30
 cv.Function                    cv.Functions                    7         4
 cv.LanguageKnowledge           cv.LanguageKnowledges           9         119
 cv.Regime                      cv.Regimes                      5         3
 cv.Sector                      cv.Sectors                      6         14
 cv.Status                      cv.Statuses                     5         7
 cv.Study                       cv.Studies                      14        2
 cv.StudyType                   cv.StudyTypes                   6         8
 cv.Training                    cv.Trainings                    14        0
 cv.TrainingType                cv.TrainingTypes                5         3
 debts.Actor                    debts.Actors                    6         63
 debts.Budget                   debts.Budgets                   11        14
 debts.Entry                    debts.Entries                   16        686
 excerpts.Excerpt               excerpts.ExcerptsByX            12        92
 excerpts.ExcerptType           excerpts.ExcerptTypes           18        11
 households.Household           households.Households           29        14
 households.Member              households.Members              13        63
 households.Type                households.Types                5         6
 humanlinks.Link                humanlinks.Links                4         59
 isip.Contract                  isip.Contracts                  22        30
 isip.ContractEnding            isip.ContractEndings            6         4
 isip.ContractPartner           isip.ContractPartners           6         35
 isip.ContractType              isip.ContractTypes              9         5
 isip.ExamPolicy                isip.ExamPolicies               20        5
 jobs.Candidature               jobs.Candidatures               8         74
 jobs.Contract                  jobs.Contracts                  28        24
 jobs.ContractType              jobs.ContractTypes              9         5
 jobs.Job                       jobs.Jobs                       10        8
 jobs.JobProvider               jobs.JobProviders               31        3
 jobs.JobType                   jobs.JobTypes                   5         5
 jobs.Offer                     jobs.Offers                     9         1
 jobs.Schedule                  jobs.Schedules                  5         3
 languages.Language             languages.Languages             6         5
 newcomers.Broker               newcomers.Brokers               2         2
 newcomers.Competence           newcomers.Competences           5         7
 newcomers.Faculty              newcomers.Faculties             6         5
 notes.EventType                notes.EventTypes                10        9
 notes.Note                     notes.Notes                     17        110
 notes.NoteType                 notes.NoteTypes                 11        13
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
 polls.AnswerChoice             polls.AnswerChoices             4         0
 polls.AnswerRemark             polls.AnswerRemarkTable         4         0
 polls.Choice                   polls.Choices                   7         31
 polls.ChoiceSet                polls.ChoiceSets                5         7
 polls.Poll                     polls.Polls                     11        0
 polls.Question                 polls.Questions                 9         0
 polls.Response                 polls.Responses                 8         0
 projects.Project               projects.Projects               10        0
 projects.ProjectType           projects.ProjectTypes           5         0
 properties.PersonProperty      cv.PersonProperties             6         310
 properties.PropChoice          properties.PropChoices          7         2
 properties.PropGroup           properties.PropGroups           5         3
 properties.PropType            properties.PropTypes            9         3
 properties.Property            properties.Properties           7         23
 sepa.Account                   sepa.Accounts                   8         13
 system.SiteConfig              system.SiteConfigs              30        1
 system.TextFieldTemplate       system.TextFieldTemplates       5         2
 uploads.Upload                 uploads.Uploads                 16        6
 uploads.UploadType             uploads.UploadTypes             10        8
 users.Authority                users.Authorities               3         3
 users.User                     users.Users                     19        10
============================== =============================== ========= =======
<BLANKLINE>



List of detail layouts
======================

The following table lists information about all detail layouts.


>>> ses = rt.login('rolf') 
>>> ses.show('about.DetailLayouts')
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
=============================== ===================================== ===================================================================================
 Datasource                      Viewable for                          Fields
------------------------------- ------------------------------------- -----------------------------------------------------------------------------------
 about.About                     all                                   server_status
 about.Models                    all except anonymous                  app name docstring rows
 accounts.Accounts               admin                                 ref name name_fr ... periods default_amount
 accounts.Charts                 admin                                 id name name_fr name_de name_nl
 accounts.Groups                 admin                                 ref name name_fr ... account_type id
 active_job_search.Proofs        all except anonymous                  date client company ... response remarks
 addresses.Addresses             admin                                 country city zip_code ... data_source partner
 aids.AidTypes                   admin                                 id short_name confirmation_type ... contact_role pharmacy_type
 aids.Categories                 admin                                 id name name_fr name_de name_nl
 aids.Grantings                  admin                                 id client user ... end_date custom_actions
 aids.IncomeConfirmations        all except anonymous                  client user signer ... id remark
 aids.RefundConfirmations        all except anonymous                  id client user ... printed remark
 aids.SimpleConfirmations        all except anonymous                  id client user ... printed remark
 boards.Boards                   admin                                 id name name_fr name_de name_nl
 cal.Calendars                   110, 410, admin                       name name_fr name_de ... id description
 cal.EventTypes                  110, 410, admin                       name name_fr name_de ... email_template attach_to_email
 cal.Events                      110, 410, admin                       event_type summary project ... modified state
 cal.GuestRoles                  admin                                 id name name_fr name_de name_nl
 cal.Guests                      admin                                 event partner role ... busy_since gone_since
 cal.RecurrentEvents             110, 410, admin                       name name_fr name_de ... sunday description
 cal.Rooms                       110, 410, admin                       id name name_fr name_de name_nl
 cal.Tasks                       110, 410, admin                       start_date due_date id ... modified description
 cbss.IdentifyPersonRequests     all except anonymous, 210, 300        id person user ... info_messages debug_messages
 cbss.ManageAccessRequests       all except anonymous, 210, 300        id person user ... info_messages debug_messages
 cbss.RetrieveTIGroupsRequests   all except anonymous                  id person user ... info_messages debug_messages
 changes.Changes                 admin                                 time user type ... id diff
 contacts.Companies              all except anonymous                  overview prefix name ... created modified
 contacts.Partners               all except anonymous                  overview id language ... created modified
 contacts.Persons                all except anonymous                  overview title first_name ... created modified
 contenttypes.ContentTypes       admin                                 id name app_label model base_classes
 countries.Countries             all except anonymous                  isocode name name_fr ... short_code inscode
 countries.Places                admin                                 name name_fr name_de ... type id
 courses.CourseContents          110, 410, admin                       id name
 courses.CourseOffers            all except anonymous, 200, 210, 300   id title content ... guest_role description
 courses.CourseProviders         all except anonymous, 200, 210, 300   overview prefix name ... gsm fax
 courses.CourseRequests          110, 410, admin                       date_submitted person content ... remark UploadsByController
 courses.Courses                 admin                                 id start_date offer title remark
 cv.Durations                    110, admin                            id name name_fr name_de name_nl
 cv.EducationLevels              110, admin                            name name_fr name_de name_nl
 cv.Experiences                  110, admin                            person start_date end_date ... is_training remarks
 cv.Functions                    110, admin                            id name name_fr ... sector remark
 cv.Regimes                      110, admin                            id name name_fr name_de name_nl
 cv.Sectors                      110, admin                            id name name_fr ... name_nl remark
 cv.Statuses                     110, admin                            id name name_fr name_de name_nl
 cv.Studies                      110, admin                            person start_date end_date ... city remarks
 cv.StudyTypes                   admin                                 name name_fr name_de ... education_level id
 cv.TrainingTypes                admin                                 name name_fr name_de name_nl id
 cv.Trainings                    110, admin                            person start_date end_date ... city remarks
 debts.Budgets                   admin                                 date partner id ... data_box summary_box
 excerpts.ExcerptTypes           admin                                 id name name_fr ... backward_compat attach_to_email
 excerpts.Excerpts               admin                                 id excerpt_type project ... build_time body_template_content
 households.Households           all except anonymous                  type prefix name id
 households.HouseholdsByType     all except anonymous                  type name language ... url remarks
 households.Types                admin                                 name name_fr name_de name_nl
 humanlinks.Links                admin                                 parent child type
 integ.ActivityReport            100, 110, admin                       body
 isip.ContractEndings            110, admin                            name use_in_isip use_in_jobs is_success needs_date_ended
 isip.ContractPartners           all except anonymous                  company contact_person contact_role duties_company
 isip.ContractTypes              110, admin                            id ref exam_policy ... name_nl full_name
 isip.Contracts                  100, 110, admin                       id client type ... duties_dsbe duties_person
 isip.ExamPolicies               110, admin                            id name name_fr ... saturday sunday
 jobs.ContractTypes              110, admin                            id name name_fr ... name_nl ref
 jobs.Contracts                  100, 110, admin                       id client user ... ending responsibilities
 jobs.JobProviders               100, 110, admin                       overview prefix name ... gsm fax
 jobs.JobTypes                   110, admin                            id name is_social
 jobs.Jobs                       100, 110, admin                       name provider contract_type ... hourly_rate remark
 jobs.JobsOverview               100, 110, admin                       preview
 jobs.Offers                     100, 110, admin                       name provider sector ... start_date remark
 jobs.OldJobsOverview            100, 110, admin                       body
 jobs.Schedules                  110, admin                            id name name_fr name_de name_nl
 languages.Languages             all except anonymous                  id iso2 name ... name_de name_nl
 newcomers.Faculties             admin                                 id name name_fr ... name_nl weight
 notes.EventTypes                admin                                 id name name_fr ... name_nl remark
 notes.NoteTypes                 admin                                 id name name_fr ... attach_to_email remark
 notes.Notes                    all except anonymous                  date time event_type ... body UploadsByController
 outbox.Mails                    110, 410, admin                       subject project date ... UploadsByController body
 pcsw.ClientContactTypes         admin                                 id name name_fr name_de name_nl
 pcsw.Clients                    all except anonymous                  overview gender id ... modified remarks
 pcsw.CoachingEndings            110, admin                            id name name_fr ... name_nl seqno
 polls.ChoiceSets                all except anonymous                  name name_fr name_de name_nl
 polls.Polls                     all except anonymous                  title state details ... default_choiceset default_multiple_choices
 polls.Responses                 all except anonymous                  user poll state ... modified remark
 projects.Projects               admin                                 id client project_type ... remark result
 properties.PropGroups           admin                                 id name name_fr name_de name_nl
 properties.PropTypes            admin                                 id name name_fr ... choicelist default_value
 properties.Properties           admin                                 id group type ... name_de name_nl
 reception.BusyVisitors          all except anonymous, 210             event client role ... remark workflow_buttons
 reception.GoneVisitors          all except anonymous, 210             event client role ... remark workflow_buttons
 reception.MyWaitingVisitors     all except anonymous, 210             event client role ... remark workflow_buttons
 reception.WaitingVisitors       all except anonymous, 210             event client role ... remark workflow_buttons
 system.SiteConfigs              admin                                 site_company next_partner_id job_office ... cbss_http_username cbss_http_password
 system.TextFieldTemplates       admin                                 id name user description text
 uploads.AreaUploads             all except anonymous                  file user upload_area ... description owner
 uploads.MyUploads               all except anonymous                  file user upload_area ... description owner
 uploads.UploadTypes             admin                                 id upload_area name ... wanted max_number
 uploads.Uploads                 admin                                 user project id ... owner remark
 uploads.UploadsByType           admin                                 file user upload_area ... description owner
 users.Users                     admin                                 username profile partner ... coaching_type coaching_supervisor
=============================== ===================================== ===================================================================================
<BLANKLINE>



User profiles
=============

Rolf
----

Rolf is the local system administrator, he has a complete menu:

>>> ses = rt.login('rolf') 
>>> with translation.override('de'):
...     ses.show_menu()
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
- Kontakte : Personen,  ▶ Klienten, Organisationen, -, Partner (alle), Haushalte
- Büro : Meine Uploads, Mein E-Mail-Ausgang, Meine Auszüge, Meine Ereignisse/Notizen
- Kalender : Kalender, Meine Termine, Meine Aufgaben, Meine Gäste, Meine Anwesenheiten
- Empfang : Klienten, Termine heute, Wartende Besucher, Beschäftigte Besucher, Gegangene Besucher, Meine Warteschlange
- ÖSHZ : Meine Begleitungen, Zu bestätigende Hilfebeschlüsse
- DSBE : Klienten, VSEs, Art.60§7-Konventionen, Stellenanbieter, Stellen, Stellenangebote
- Kurse : Kursanbieter, Kursangebote, Offene Kursanfragen
- Erstempfang : Neue Klienten, Verfügbare Begleiter
- Schuldnerberatung : Klienten, Meine Budgets
- Polls : Meine Polls, Meine Responses
- Berichte :
  - System : Stale Controllables
  - ÖSHZ : Datenkontrolle Klienten
  - DSBE : Benutzer und ihre Klienten, Übersicht Art.60§7-Konventionen, Tätigkeitsbericht
- Konfigurierung :
  - Büro : Meine Einfügetexte, Upload-Arten, Auszugsarten, Notizarten, Ereignisarten
  - System : Site-Parameter, Benutzer, Hilfetexte
  - Orte : Länder, Orte
  - Eigenschaften : Eigenschaftsgruppen, Eigenschafts-Datentypen, Fachkompetenzen, Sozialkompetenzen, Hindernisse
  - Kontakte : Organisationsarten, Funktionen, Gremien, Haushaltsarten
  - Kalender : Kalenderliste, Räume, Prioritäten, Periodische Termine, Gastrollen, Ereignisarten, Externe Kalender
  - Buchhaltung : Kontenpläne, Kontengruppen, Konten
  - Badges : Badges
  - ÖSHZ : Integrationsphasen, Berufe, AG-Sperrgründe, Dienste, Begleitungsbeendigungsgründe, Dispenzgründe, Klientenkontaktarten, Hilfearten, Kategorien
  - Lebenslauf : Ausbildungsarten, Studienarten, Akademische Grade, Sektoren, Funktionen, Arbeitsregimes, Statuus, Vertragsdauern, Sprachen
  - DSBE : VSE-Arten, Vertragsbeendigungsgründe, Auswertungsstrategien, Art.60§7-Konventionsarten, Stellenarten, Stundenpläne
  - Kurse : Kursinhalte
  - Erstempfang : Vermittler, Fachbereiche
  - ZDSS : Sektoren, Eigenschafts-Codes
  - Schuldnerberatung : Budget-Kopiervorlage
  - Client projects : Client project types
  - Polls : Choice Sets
- Explorer :
  - Büro : Einfügetexte, Uploads, Upload-Bereiche, E-Mail-Ausgänge, Anhänge, Auszüge, Ereignisse/Notizen
  - System : Vollmachten, Benutzergruppen, Benutzer-Levels, Benutzerprofile, Datenbankmodelle, Änderungen
  - Eigenschaften : Eigenschaften
  - Kontakte : Kontaktpersonen, Adressenarten, Adressen, Gremienmitglieder, Rollen, Mitglieder, Verwandtschaftsbeziehungen, Verwandschaftsarten
  - Kalender : Aufgaben, Teilnehmer, Abonnements, Termin-Zustände, Gast-Zustände, Aufgaben-Zustände
  - Badges : Badge Awards
  - SEPA : Konten
  - ÖSHZ : Begleitungen, Klientenkontakte, AG-Sperren, Vorstrafen, Klienten, Zivilstände, Bearbeitungszustände Klienten, eID-Kartenarten, Hilfebeschlüsse, Einkommensbescheinigungen, Kostenübernahmescheine, Einfache Bescheinigungen
  - Lebenslauf : Sprachkenntnisse, Ausbildungen, Studien, Berufserfahrungen
  - DSBE : VSEs, Art.60§7-Konventionen, Stellenanfragen, Vertragspartner, Proofs of search
  - Kurse : Kurse, Kursanfragen
  - Erstempfang : Kompetenzen
  - ZDSS : IdentifyPerson-Anfragen, ManageAccess-Anfragen, Tx25-Anfragen
  - Schuldnerberatung : Budgets, Einträge
  - Client projects : Client Projects
  - Polls : Polls, Questions, Choices, Responses, Answer Choices, AnswerRemarks
- Site : Info
<BLANKLINE>



Hubert
------

Hubert is an Integration agent.

>>> ses = rt.login('hubert') 
>>> with translation.override('de'):
...     ses.show_menu()
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF +SKIP
- Kontakte : Personen,  ▶ Klienten, Organisationen, -, Partner (alle), Haushalte
- Büro : Mein E-Mail-Ausgang, Meine Auszüge, Meine Ereignisse/Notizen
- Kalender : Kalender, Meine Termine, Meine Aufgaben, Meine Gäste, Meine Anwesenheiten
- Empfang : Meine Warteschlange
- DSBE : Klienten, VSEs, Art.60§7-Konventionen, Stellenanbieter, Stellen, Stellenangebote
- Kurse : Kursanbieter, Kursangebote, Offene Kursanfragen
- Berichte :
  - DSBE : Benutzer und ihre Klienten, Übersicht Art.60§7-Konventionen, Tätigkeitsbericht
- Konfigurierung :
  - Büro : Meine Einfügetexte
  - Kontakte : Länder, Sprachen
- Explorer :
  - DSBE : VSEs, Art.60§7-Konventionen
- Site : Info



Mélanie
-------

Mélanie is the manager of the Integration service.

>>> ses = rt.login('melanie') 
>>> with translation.override('de'):
...     ses.show_menu()
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF +SKIP
- Kontakte : Personen,  ▶ Klienten, Organisationen, -, Partner (alle), Haushalte
- Büro : Mein E-Mail-Ausgang, Meine Auszüge, Meine Ereignisse/Notizen
- Kalender : Kalender, Meine Termine, Meine Aufgaben, Meine Gäste, Meine Anwesenheiten
- Empfang : Meine Warteschlange
- DSBE : Klienten, VSEs, Art.60§7-Konventionen, Stellenanbieter, Stellen, Stellenangebote
- Kurse : Kursanbieter, Kursangebote, Offene Kursanfragen
- Berichte :
  - DSBE : Benutzer und ihre Klienten, Übersicht Art.60§7-Konventionen, Tätigkeitsbericht
- Konfigurierung :
  - Büro : Meine Einfügetexte
  - Kontakte : Länder, Sprachen
  - Kalender : Kalenderliste, Räume, Prioritäten, Periodische Termine, Ereignisarten, Externe Kalender
  - ÖSHZ : Integrationsphasen, Begleitungsbeendigungsgründe, Dispenzgründe
  - DSBE : VSE-Arten, Vertragsbeendigungsgründe, Auswertungsstrategien, Art.60§7-Konventionsarten, Stellenarten, Sektoren, Funktionen, Stundenpläne, Regimes
  - Kurse : Kursinhalte
- Explorer :
  - Büro : E-Mail-Ausgänge, Anhänge
  - Kalender : Aufgaben, Abonnements
  - CV : Sprachkenntnisse
  - DSBE : VSEs, Art.60§7-Konventionen, Stellenanfragen, Ausbildungen und Studien
  - Kurse : Kursanfragen
- Site : Info


Kerstin
-------

Kerstin is a debts consultant.

>>> ses = rt.login('kerstin') 
>>> with translation.override('de'):
...     ses.show_menu()
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF +SKIP
- Kontakte : Personen,  ▶ Klienten, Organisationen, -, Partner (alle), Haushalte
- Büro : Mein E-Mail-Ausgang, Meine Auszüge, Meine Ereignisse/Notizen
- Kalender : Kalender, Meine Termine, Meine Aufgaben, Meine Gäste, Meine Anwesenheiten
- Empfang : Meine Warteschlange
- Schuldnerberatung : Klienten, Meine Budgets
- Konfigurierung :
  - Büro : Meine Einfügetexte
  - Kontakte : Länder, Sprachen
  - Schuldnerberatung : Budget-Kopiervorlage
- Site : Info



Caroline
--------

Caroline is a newcomers consultant.

>>> ses = rt.login('caroline') 
>>> with translation.override('de'):
...     ses.show_menu()
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF +SKIP
- Kontakte : Personen,  ▶ Klienten, Organisationen, -, Partner (alle), Haushalte
- Büro : Mein E-Mail-Ausgang, Meine Auszüge, Meine Ereignisse/Notizen
- Kalender : Kalender, Meine Termine, Meine Aufgaben, Meine Gäste, Meine Anwesenheiten
- Empfang : Meine Warteschlange
- Erstempfang : Neue Klienten, Verfügbare Begleiter
- Berichte :
  - DSBE : Benutzer und ihre Klienten
- Konfigurierung :
  - Büro : Meine Einfügetexte
  - Kontakte : Länder, Sprachen
- Site : Info



Theresia
--------

Theresia is a reception clerk.

>>> ses = rt.login('theresia') 
>>> with translation.override('de'):
...     ses.show_menu()
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF +SKIP
- Empfang : Klienten, Termine heute, Wartende Besucher, Beschäftigte Besucher, Gegangene Besucher
- Site : Info


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

Check whether Lino returns the right default template for excerpts 
(see :blogref:`20140208`):

>>> ffn = settings.SITE.find_config_file('Default.odt', 'excerpts')
>>> ffn.endswith('lino_welfare/config/excerpts/Default.odt')
True


