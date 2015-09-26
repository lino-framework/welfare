.. _welfare.specs.ddh:

=============================
Preventing accidental deletes
=============================

.. How to test only this document:

    $ python setup.py test -s tests.SpecsTests.test_ddh
    
    doctest init:

    >>> from __future__ import print_function
    >>> import os
    >>> os.environ['DJANGO_SETTINGS_MODULE'] = \
    ...    'lino_welfare.projects.std.settings.doctests'
    >>> from lino.api.doctest import *


Foreign Keys and their `on_delete` setting
==========================================

Here is the output of :meth:`lino.utils.diag.Analyzer.show_foreign_keys` in
Lino Welfare:


>>> from lino.utils.diag import analyzer
>>> print(analyzer.show_foreign_keys())
... #doctest: +NORMALIZE_WHITESPACE +REPORT_UDIFF
- accounts.Account :
  - PROTECT : ledger.Journal.account, ledger.Movement.account, ledger.MatchRule.account, debts.Entry.account, vatless.InvoiceItem.account, finan.GrouperItem.account, finan.JournalEntryItem.account, finan.BankStatementItem.account, finan.PaymentOrderItem.account
- accounts.Group :
  - PROTECT : accounts.Account.group
- aids.AidType :
  - PROTECT : aids.Granting.aid_type
- aids.Category :
  - PROTECT : aids.Granting.category, aids.IncomeConfirmation.category
- aids.Granting :
  - PROTECT : aids.SimpleConfirmation.granting, aids.IncomeConfirmation.granting, aids.RefundConfirmation.granting
- art61.ContractType :
  - PROTECT : art61.Contract.type
- badges.Badge :
  - PROTECT : badges.Award.badge
- boards.Board :
  - PROTECT : aids.AidType.board, aids.Granting.board, boards.Member.board
- cal.Calendar :
  - PROTECT : system.SiteConfig.site_calendar, users.User.calendar, cal.Subscription.calendar
- cal.Event :
  - CASCADE : cal.Guest.event
- cal.EventType :
  - PROTECT : system.SiteConfig.default_event_type, users.User.event_type, isip.ExamPolicy.event_type, cal.RecurrentEvent.event_type, cal.Event.event_type
- cal.GuestRole :
  - PROTECT : system.SiteConfig.client_guestrole, pcsw.CoachingType.eval_guestrole, courses.CourseOffer.guest_role, cal.Guest.role
- cal.Priority :
  - PROTECT : cal.Event.priority
- cal.Room :
  - PROTECT : cal.Event.room
- cbss.Purpose :
  - PROTECT : cbss.ManageAccessRequest.purpose
- cbss.Sector :
  - PROTECT : cbss.ManageAccessRequest.sector
- contacts.Company :
  - CASCADE : jobs.JobProvider.company_ptr, courses.CourseProvider.company_ptr
  - PROTECT : aids.AidType.company, aids.SimpleConfirmation.company, aids.IncomeConfirmation.company, aids.RefundConfirmation.company, excerpts.Excerpt.company, contacts.Role.company, debts.Entry.bailiff, system.SiteConfig.site_company, art61.Contract.company, immersion.Contract.company, uploads.Upload.company, jobs.Contract.company, pcsw.ClientContact.company, active_job_search.Proof.company, notes.Note.company, isip.ContractPartner.company
- contacts.CompanyType :
  - PROTECT : contacts.Company.type
- contacts.Partner :
  - CASCADE : addresses.Address.partner, households.Household.partner_ptr, contacts.Person.partner_ptr, contacts.Company.partner_ptr, sepa.Account.partner
  - PROTECT : polls.Response.partner, ledger.Movement.partner, debts.Budget.partner, debts.Actor.partner, debts.Entry.partner, vatless.AccountInvoice.partner, users.User.partner, outbox.Recipient.partner, sepa.Movement.partner, cal.Guest.partner, finan.Grouper.partner, finan.GrouperItem.partner, finan.JournalEntryItem.partner, finan.BankStatementItem.partner, finan.PaymentOrderItem.partner
- contacts.Person :
  - CASCADE : cv.LanguageKnowledge.person, cv.Skill.person, cv.SoftSkill.person, cv.Obstacle.person, pcsw.Client.person_ptr
  - PROTECT : aids.AidType.contact_person, aids.SimpleConfirmation.contact_person, aids.IncomeConfirmation.contact_person, aids.RefundConfirmation.contact_person, excerpts.Excerpt.contact_person, cv.Training.person, cv.Study.person, cv.Experience.person, badges.Award.holder, households.Member.person, contacts.Role.person, system.SiteConfig.signer1, art61.Contract.signer1, immersion.Contract.signer1, uploads.Upload.contact_person, jobs.Contract.signer1, pcsw.ClientContact.contact_person, boards.Member.person, notes.Note.contact_person, isip.ContractPartner.contact_person, isip.Contract.signer1, humanlinks.Link.parent
- contacts.Role :
  - PROTECT : pcsw.Client.job_office_contact
- contacts.RoleType :
  - PROTECT : aids.AidType.contact_role, aids.SimpleConfirmation.contact_role, aids.IncomeConfirmation.contact_role, aids.RefundConfirmation.contact_role, excerpts.Excerpt.contact_role, contacts.Role.type, system.SiteConfig.signer1_function, art61.Contract.contact_role, immersion.Contract.contact_role, uploads.Upload.contact_role, jobs.Contract.contact_role, pcsw.ClientContact.contact_role, boards.Member.role, notes.Note.contact_role, isip.ContractPartner.contact_role
- contenttypes.ContentType :
  - PROTECT : excerpts.ExcerptType.content_type, excerpts.Excerpt.owner_type, uploads.Upload.owner_type, gfks.HelpText.content_type, plausibility.Problem.owner_type, outbox.Mail.owner_type, outbox.Attachment.owner_type, notes.Note.owner_type, cal.Event.owner_type, cal.Task.owner_type, changes.Change.object_type
- countries.Country :
  - PROTECT : addresses.Address.country, cv.Training.country, cv.Study.country, cv.Experience.country, contacts.Partner.country, pcsw.Client.nationality, countries.Country.actual_country, countries.Place.country
- countries.Place :
  - PROTECT : addresses.Address.city, cv.Training.city, cv.Study.city, cv.Experience.city, contacts.Partner.city, countries.Place.parent
- courses.Course :
  - PROTECT : courses.CourseRequest.course
- courses.CourseContent :
  - PROTECT : courses.CourseOffer.content, courses.CourseRequest.content
- courses.CourseOffer :
  - PROTECT : courses.Course.offer, courses.CourseRequest.offer
- courses.CourseProvider :
  - PROTECT : courses.CourseOffer.provider
- cv.Duration :
  - PROTECT : cv.Experience.duration, art61.Contract.cv_duration
- cv.EducationLevel :
  - PROTECT : cv.StudyType.education_level, cv.Study.education_level
- cv.Function :
  - PROTECT : cv.Training.function, cv.Experience.function, cv.Skill.function, immersion.Contract.function, jobs.Offer.function, jobs.Job.function, jobs.Candidature.function
- cv.ObstacleType :
  - PROTECT : cv.Obstacle.type
- cv.Proof :
  - PROTECT : cv.Skill.proof, cv.SoftSkill.proof
- cv.Regime :
  - PROTECT : cv.Experience.regime, art61.Contract.regime, jobs.Contract.regime
- cv.Sector :
  - PROTECT : cv.Training.sector, cv.Function.sector, cv.Experience.sector, cv.Skill.sector, immersion.Contract.sector, jobs.Offer.sector, jobs.Job.sector, jobs.Candidature.sector
- cv.SoftSkillType :
  - PROTECT : cv.SoftSkill.type
- cv.Status :
  - PROTECT : cv.Experience.status, art61.Contract.status
- cv.StudyType :
  - PROTECT : cv.Training.type, cv.Study.type, isip.Contract.study_type
- debts.Actor :
  - PROTECT : debts.Entry.actor
- debts.Budget :
  - CASCADE : debts.Actor.budget, debts.Entry.budget
  - PROTECT : system.SiteConfig.master_budget
- excerpts.Excerpt :
  - set_on_delete : cbss.IdentifyPersonRequest.printed_by, cbss.ManageAccessRequest.printed_by, cbss.RetrieveTIGroupsRequest.printed_by, aids.SimpleConfirmation.printed_by, aids.IncomeConfirmation.printed_by, aids.RefundConfirmation.printed_by, debts.Budget.printed_by, art61.Contract.printed_by, immersion.Contract.printed_by, jobs.Contract.printed_by, isip.Contract.printed_by
- excerpts.ExcerptType :
  - PROTECT : excerpts.Excerpt.excerpt_type
- finan.BankStatement :
  - CASCADE : finan.BankStatementItem.voucher
- finan.Grouper :
  - CASCADE : finan.GrouperItem.voucher
- finan.JournalEntry :
  - CASCADE : finan.JournalEntryItem.voucher
- finan.PaymentOrder :
  - CASCADE : finan.PaymentOrderItem.voucher
- households.Household :
  - CASCADE : households.Member.household
- households.Type :
  - PROTECT : households.Household.type
- immersion.ContractType :
  - PROTECT : immersion.Contract.type
- immersion.Goal :
  - PROTECT : immersion.Contract.goal
- isip.Contract :
  - PROTECT : isip.ContractPartner.contract
- isip.ContractEnding :
  - PROTECT : art61.Contract.ending, immersion.Contract.ending, jobs.Contract.ending, isip.Contract.ending
- isip.ContractType :
  - PROTECT : isip.Contract.type
- isip.ExamPolicy :
  - PROTECT : art61.ContractType.exam_policy, art61.Contract.exam_policy, immersion.ContractType.exam_policy, immersion.Contract.exam_policy, jobs.ContractType.exam_policy, jobs.Contract.exam_policy, isip.ContractType.exam_policy, isip.Contract.exam_policy
- jobs.ContractType :
  - PROTECT : jobs.Contract.type, jobs.Job.contract_type
- jobs.Job :
  - PROTECT : jobs.Contract.job, jobs.Candidature.job
- jobs.JobProvider :
  - PROTECT : jobs.Offer.provider, jobs.Job.provider
- jobs.JobType :
  - PROTECT : jobs.Job.type
- jobs.Schedule :
  - PROTECT : jobs.Contract.schedule
- languages.Language :
  - PROTECT : cv.LanguageKnowledge.language, cv.Training.language, cv.Study.language
- ledger.Journal :
  - PROTECT : ledger.Voucher.journal, ledger.MatchRule.journal
- ledger.Movement :
  - PROTECT : ledger.Movement.match, vatless.AccountInvoice.match, finan.GrouperItem.match, finan.JournalEntryItem.match, finan.BankStatementItem.match, finan.PaymentOrderItem.match
- ledger.PaymentTerm :
  - PROTECT : vatless.AccountInvoice.payment_term
- ledger.Voucher :
  - CASCADE : ledger.Movement.voucher
  - PROTECT : vatless.AccountInvoice.voucher_ptr, finan.Grouper.voucher_ptr, finan.JournalEntry.voucher_ptr, finan.PaymentOrder.voucher_ptr, finan.BankStatement.voucher_ptr
- newcomers.Broker :
  - PROTECT : pcsw.Client.broker
- newcomers.Faculty :
  - PROTECT : newcomers.Competence.faculty, pcsw.Client.faculty
- notes.EventType :
  - PROTECT : system.SiteConfig.system_note_type, notes.Note.event_type
- notes.NoteType :
  - PROTECT : notes.Note.type
- outbox.Mail :
  - CASCADE : outbox.Recipient.mail, outbox.Attachment.mail
- pcsw.Activity :
  - PROTECT : contacts.Partner.activity
- pcsw.AidType :
  - PROTECT : pcsw.Client.aid_type
- pcsw.Client :
  - CASCADE : aids.SimpleConfirmation.client, aids.IncomeConfirmation.client, aids.RefundConfirmation.client, pcsw.Coaching.client, pcsw.Dispense.client, dupable_clients.Word.owner
  - PROTECT : cbss.IdentifyPersonRequest.person, cbss.ManageAccessRequest.person, cbss.RetrieveTIGroupsRequest.person, ledger.Movement.project, aids.Granting.client, excerpts.Excerpt.project, art61.Contract.client, immersion.Contract.client, vatless.InvoiceItem.project, uploads.Upload.project, jobs.Contract.client, jobs.Candidature.person, pcsw.Exclusion.person, pcsw.Conviction.client, pcsw.ClientContact.client, active_job_search.Proof.client, outbox.Mail.project, notes.Note.project, isip.Contract.client, courses.CourseRequest.person, cal.Event.project, cal.Task.project, finan.GrouperItem.project, finan.JournalEntryItem.project, finan.BankStatementItem.project, finan.PaymentOrderItem.project
- pcsw.ClientContactType :
  - PROTECT : aids.AidType.pharmacy_type, aids.RefundConfirmation.doctor_type, contacts.Partner.client_contact_type, pcsw.ClientContact.type
- pcsw.CoachingEnding :
  - PROTECT : pcsw.Coaching.ending
- pcsw.CoachingType :
  - PROTECT : users.User.coaching_type, pcsw.CoachingEnding.type, pcsw.Coaching.type
- pcsw.DispenseReason :
  - PROTECT : pcsw.Dispense.reason
- pcsw.ExclusionType :
  - PROTECT : pcsw.Exclusion.type
- pcsw.PersonGroup :
  - PROTECT : pcsw.Client.group
- polls.Choice :
  - PROTECT : polls.AnswerChoice.choice
- polls.ChoiceSet :
  - PROTECT : polls.Choice.choiceset, polls.Poll.default_choiceset, polls.Question.choiceset
- polls.Poll :
  - CASCADE : polls.Question.poll
  - PROTECT : polls.Response.poll
- polls.Question :
  - PROTECT : polls.AnswerChoice.question, polls.AnswerRemark.question
- polls.Response :
  - PROTECT : polls.AnswerChoice.response, polls.AnswerRemark.response
- properties.PropGroup :
  - PROTECT : properties.Property.group
- properties.PropType :
  - PROTECT : properties.PropChoice.type, properties.Property.type
- sepa.Account :
  - PROTECT : vatless.AccountInvoice.bank_account, sepa.Statement.account, sepa.Movement.bank_account, finan.PaymentOrderItem.bank_account
- sepa.Statement :
  - PROTECT : sepa.Movement.statement
- uploads.UploadType :
  - PROTECT : uploads.Upload.type
- users.User :
  - PROTECT : polls.Poll.user, polls.Response.user, cbss.IdentifyPersonRequest.user, cbss.ManageAccessRequest.user, cbss.RetrieveTIGroupsRequest.user, ledger.Voucher.user, newcomers.Competence.user, aids.Granting.user, aids.SimpleConfirmation.user, aids.IncomeConfirmation.user, aids.RefundConfirmation.user, excerpts.Excerpt.user, cv.Obstacle.user, debts.Budget.user, tinymce.TextFieldTemplate.user, art61.Contract.user, immersion.Contract.user, uploads.Upload.user, jobs.Contract.user, users.Authority.user, plausibility.Problem.user, pcsw.Coaching.user, outbox.Mail.user, notes.Note.user, isip.Contract.user, cal.Subscription.user, cal.RecurrentEvent.user, cal.Event.user, cal.Task.user, changes.Change.user
- vatless.AccountInvoice :
  - CASCADE : vatless.InvoiceItem.voucher
<BLANKLINE>




Users and partners
==================

It is not allowed to delete a person who is being used as the
:attr:`partner <lino.modlib.users.models.User.partner>` of a user
(although that field is nullable).

>>> rt.show(users.Users, column_names="id username partner partner__id")
==== ========== ================= =====
 ID   Username   Partner           ID
---- ---------- ----------------- -----
 6    alicia     Allmanns Alicia   194
 9    caroline
 5    hubert     Huppertz Hubert   193
 10   judith     Jousten Judith    196
 12   kerstin
 4    melanie    Mélard Mélanie    192
 8    nicolas
 1    robin
 3    rolf
 2    romain
 7    theresia   Thelen Theresia   195
 11   wilfried
==== ========== ================= =====
<BLANKLINE>

The message is the same whether you try on the Person or on the Partner:

>>> obj = contacts.Person.objects.get(id=194)
>>> print(obj.disable_delete())
Cannot delete Partner Allmanns Alicia because 1 Users refer to it.

>>> obj = contacts.Partner.objects.get(id=194)
>>> print(obj.disable_delete())
Cannot delete Partner Allmanns Alicia because 1 Users refer to it.


You can delete a partner when a person or some other MTI child exists:

>>> obj = contacts.Partner.objects.get(id=200)
>>> print(obj.disable_delete())
Cannot delete Partner Die neue Alternative V.o.G. because 2 Budget Entries refer to it.

