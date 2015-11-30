.. _welfare.tested.general:
.. _welfare.specs.general:

================================
General overview of Lino Welfare
================================

.. How to test only this document:

    $ python setup.py test -s tests.SpecsTests.test_general

    doctest init:

    >>> from __future__ import print_function
    >>> import lino
    >>> lino.startup('lino_welfare.projects.std.settings.doctests')
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


>>> from lino.utils.diag import analyzer
>>> print(analyzer.show_db_overview())
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF -SKIP
61 apps: lino_startup, staticfiles, about, extjs, jinja, bootstrap3, appypod, printing, system, contenttypes, gfks, humanize, users, notifier, changes, office, countries, properties, contacts, addresses, uploads, outbox, excerpts, extensible, cal, reception, cosi, accounts, badges, boards, welfare, sales, pcsw, ledger, sepa, b2c, vatless, finan, languages, cv, integ, isip, jobs, art61, immersion, active_job_search, courses, newcomers, cbss, households, humanlinks, debts, notes, aids, polls, beid, davlink, export_excel, dupable_clients, plausibility, tinymce.
153 models:
============================== =============================== ========= =======
 Name                           Default table                   #fields   #rows
------------------------------ ------------------------------- --------- -------
 accounts.Account               accounts.Accounts               19        77
 accounts.Group                 accounts.Groups                 9         14
 active_job_search.Proof        active_job_search.Proofs        7         10
 addresses.Address              addresses.Addresses             16        179
 aids.AidType                   aids.AidTypes                   23        11
 aids.Category                  aids.Categories                 5         3
 aids.Granting                  aids.Grantings                  12        55
 aids.IncomeConfirmation        aids.IncomeConfirmations        17        54
 aids.RefundConfirmation        aids.RefundConfirmations        18        12
 aids.SimpleConfirmation        aids.SimpleConfirmations        15        19
 art61.Contract                 art61.Contracts                 30        7
 art61.ContractType             art61.ContractTypes             10        1
 b2c.Account                    b2c.Accounts                    6         34
 b2c.Statement                  b2c.Statements                  8         34
 b2c.Transaction                b2c.Transactions                17        57
 badges.Award                   badges.Awards                   6         0
 badges.Badge                   badges.Badges                   5         0
 boards.Board                   boards.Boards                   7         3
 boards.Member                  boards.Members                  4         0
 cal.Calendar                   cal.Calendars                   7         11
 cal.Event                      cal.OneEvent                    24        528
 cal.EventType                  cal.EventTypes                  19        9
 cal.Guest                      cal.Guests                      9         524
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
 cbss.RetrieveTIGroupsRequest   cbss.RetrieveTIGroupsRequests   15        3
 cbss.Sector                    cbss.Sectors                    11        209
 changes.Change                 changes.Changes                 9         0
 contacts.Company               contacts.Companies              29        51
 contacts.CompanyType           contacts.CompanyTypes           9         16
 contacts.Partner               contacts.Partners               25        174
 contacts.Person                contacts.Persons                32        109
 contacts.Role                  contacts.Roles                  4         10
 contacts.RoleType              contacts.RoleTypes              6         5
 contenttypes.ContentType       gfks.ContentTypes               3         154
 countries.Country              countries.Countries             9         8
 countries.Place                countries.Places                10        78
 courses.Course                 courses.Courses                 5         3
 courses.CourseContent          courses.CourseContents          2         2
 courses.CourseOffer            courses.CourseOffers            6         3
 courses.CourseProvider         courses.CourseProviders         30        2
 courses.CourseRequest          courses.CourseRequests          10        20
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
 debts.Actor                    debts.Actors                    6         63
 debts.Budget                   debts.Budgets                   11        14
 debts.Entry                    debts.Entries                   16        716
 dupable_clients.Word           dupable_clients.Words           3         131
 excerpts.Excerpt               excerpts.Excerpts               12        68
 excerpts.ExcerptType           excerpts.ExcerptTypes           18        17
 finan.BankStatement            finan.BankStatements            11        0
 finan.BankStatementItem        finan.BankStatementItemTable    11        0
 finan.Grouper                  finan.Groupers                  10        0
 finan.GrouperItem              finan.GrouperItemTable          10        0
 finan.JournalEntry             finan.FinancialVouchers         9         0
 finan.JournalEntryItem         finan.JournalEntryItemTable     11        0
 finan.PaymentOrder             finan.PaymentOrders             11        0
 finan.PaymentOrderItem         finan.PaymentOrderItemTable     11        0
 gfks.HelpText                  gfks.HelpTexts                  4         5
 households.Household           households.Households           28        14
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
 jobs.JobProvider               jobs.JobProviders               30        3
 jobs.JobType                   jobs.JobTypes                   5         5
 jobs.Offer                     jobs.Offers                     9         1
 jobs.Schedule                  jobs.Schedules                  5         3
 languages.Language             languages.Languages             6         5
 ledger.Journal                 ledger.Journals                 21        4
 ledger.MatchRule               ledger.MatchRules               3         4
 ledger.Movement                ledger.Movements                10        120
 ledger.PaymentTerm             ledger.PaymentTerms             9         7
 ledger.Voucher                 ledger.Vouchers                 8         30
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
 pcsw.Client                    pcsw.Clients                    66        63
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
 sepa.Account                   sepa.Accounts                   8         17
 system.SiteConfig              system.SiteConfigs              29        1
 tinymce.TextFieldTemplate      tinymce.TextFieldTemplates      5         2
 uploads.Upload                 uploads.Uploads                 17        11
 uploads.UploadType             uploads.UploadTypes             11        9
 users.Authority                users.Authorities               3         3
 users.User                     users.Users                     21        12
 vatless.AccountInvoice         vatless.Invoices                17        30
 vatless.InvoiceItem            vatless.InvoiceItems            7         90
============================== =============================== ========= =======
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

