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
  - PROTECT : debts.Entry.account, finan.BankStatementItem.account, finan.GrouperItem.account, finan.JournalEntryItem.account, finan.PaymentOrderItem.account, ledger.Journal.account, ledger.MatchRule.account, ledger.Movement.account, vatless.InvoiceItem.account
- accounts.Group :
  - PROTECT : accounts.Account.group
- aids.AidType :
  - PROTECT : aids.Granting.aid_type
- aids.Category :
  - PROTECT : aids.Granting.category, aids.IncomeConfirmation.category
- aids.Granting :
  - PROTECT : aids.IncomeConfirmation.granting, aids.RefundConfirmation.granting, aids.SimpleConfirmation.granting
- art61.ContractType :
  - PROTECT : art61.Contract.type
- badges.Badge :
  - PROTECT : badges.Award.badge
- boards.Board :
  - PROTECT : aids.AidType.board, aids.Granting.board, boards.Member.board
- cal.Calendar :
  - PROTECT : cal.Subscription.calendar, system.SiteConfig.site_calendar, users.User.calendar
- cal.Event :
  - CASCADE : cal.Guest.event
- cal.EventType :
  - PROTECT : cal.Event.event_type, cal.RecurrentEvent.event_type, isip.ExamPolicy.event_type, system.SiteConfig.default_event_type, users.User.event_type
- cal.GuestRole :
  - PROTECT : cal.Guest.role, courses.CourseOffer.guest_role, pcsw.CoachingType.eval_guestrole, system.SiteConfig.client_guestrole
- cal.Priority :
  - PROTECT : cal.Event.priority
- cal.Room :
  - PROTECT : cal.Event.room
- cbss.Purpose :
  - PROTECT : cbss.ManageAccessRequest.purpose
- cbss.Sector :
  - PROTECT : cbss.ManageAccessRequest.sector
- contacts.Company :
  - CASCADE : courses.CourseProvider.company_ptr, jobs.JobProvider.company_ptr
  - PROTECT : active_job_search.Proof.company, aids.AidType.company, aids.IncomeConfirmation.company, aids.RefundConfirmation.company, aids.SimpleConfirmation.company, art61.Contract.company, contacts.Role.company, debts.Entry.bailiff, excerpts.Excerpt.company, immersion.Contract.company, isip.ContractPartner.company, jobs.Contract.company, notes.Note.company, pcsw.ClientContact.company, system.SiteConfig.site_company, uploads.Upload.company
- contacts.CompanyType :
  - PROTECT : contacts.Company.type
- contacts.Partner :
  - CASCADE : addresses.Address.partner, contacts.Company.partner_ptr, contacts.Person.partner_ptr, households.Household.partner_ptr, sepa.Account.partner
  - PROTECT : cal.Guest.partner, debts.Actor.partner, debts.Budget.partner, debts.Entry.partner, finan.BankStatementItem.partner, finan.Grouper.partner, finan.GrouperItem.partner, finan.JournalEntryItem.partner, finan.PaymentOrderItem.partner, ledger.Movement.partner, outbox.Recipient.partner, polls.Response.partner, users.User.partner, vatless.AccountInvoice.partner
- contacts.Person :
  - CASCADE : cv.LanguageKnowledge.person, cv.Obstacle.person, cv.Skill.person, cv.SoftSkill.person, pcsw.Client.person_ptr
  - PROTECT : aids.AidType.contact_person, aids.IncomeConfirmation.contact_person, aids.RefundConfirmation.contact_person, aids.SimpleConfirmation.contact_person, art61.Contract.signer1, badges.Award.holder, boards.Member.person, contacts.Role.person, cv.Experience.person, cv.Study.person, cv.Training.person, excerpts.Excerpt.contact_person, households.Member.person, humanlinks.Link.parent, immersion.Contract.signer1, isip.Contract.signer1, isip.ContractPartner.contact_person, jobs.Contract.signer1, notes.Note.contact_person, pcsw.ClientContact.contact_person, system.SiteConfig.signer1, uploads.Upload.contact_person
- contacts.Role :
  - PROTECT : pcsw.Client.job_office_contact
- contacts.RoleType :
  - PROTECT : aids.AidType.contact_role, aids.IncomeConfirmation.contact_role, aids.RefundConfirmation.contact_role, aids.SimpleConfirmation.contact_role, art61.Contract.contact_role, boards.Member.role, contacts.Role.type, excerpts.Excerpt.contact_role, immersion.Contract.contact_role, isip.ContractPartner.contact_role, jobs.Contract.contact_role, notes.Note.contact_role, pcsw.ClientContact.contact_role, system.SiteConfig.signer1_function, uploads.Upload.contact_role
- contenttypes.ContentType :
  - PROTECT : cal.Event.owner_type, cal.Task.owner_type, changes.Change.object_type, excerpts.Excerpt.owner_type, excerpts.ExcerptType.content_type, gfks.HelpText.content_type, notes.Note.owner_type, notifier.Notification.owner_type, outbox.Attachment.owner_type, outbox.Mail.owner_type, plausibility.Problem.owner_type, uploads.Upload.owner_type
- countries.Country :
  - PROTECT : addresses.Address.country, contacts.Partner.country, countries.Country.actual_country, countries.Place.country, cv.Experience.country, cv.Study.country, cv.Training.country, pcsw.Client.nationality
- countries.Place :
  - PROTECT : addresses.Address.city, contacts.Partner.city, countries.Place.parent, cv.Experience.city, cv.Study.city, cv.Training.city
- courses.Course :
  - PROTECT : courses.CourseRequest.course
- courses.CourseContent :
  - PROTECT : courses.CourseOffer.content, courses.CourseRequest.content
- courses.CourseOffer :
  - PROTECT : courses.Course.offer, courses.CourseRequest.offer
- courses.CourseProvider :
  - PROTECT : courses.CourseOffer.provider
- cv.Duration :
  - PROTECT : art61.Contract.cv_duration, cv.Experience.duration
- cv.EducationLevel :
  - PROTECT : cv.Study.education_level, cv.StudyType.education_level
- cv.Function :
  - PROTECT : cv.Experience.function, cv.Skill.function, cv.Training.function, immersion.Contract.function, jobs.Candidature.function, jobs.Job.function, jobs.Offer.function
- cv.ObstacleType :
  - PROTECT : cv.Obstacle.type
- cv.Proof :
  - PROTECT : cv.Skill.proof, cv.SoftSkill.proof
- cv.Regime :
  - PROTECT : art61.Contract.regime, cv.Experience.regime, jobs.Contract.regime
- cv.Sector :
  - PROTECT : cv.Experience.sector, cv.Function.sector, cv.Skill.sector, cv.Training.sector, immersion.Contract.sector, jobs.Candidature.sector, jobs.Job.sector, jobs.Offer.sector
- cv.SoftSkillType :
  - PROTECT : cv.SoftSkill.type
- cv.Status :
  - PROTECT : art61.Contract.status, cv.Experience.status
- cv.StudyType :
  - PROTECT : cv.Study.type, cv.Training.type, isip.Contract.study_type
- debts.Actor :
  - PROTECT : debts.Entry.actor
- debts.Budget :
  - CASCADE : debts.Actor.budget, debts.Entry.budget
  - PROTECT : system.SiteConfig.master_budget
- excerpts.Excerpt :
  - set_on_delete : aids.IncomeConfirmation.printed_by, aids.RefundConfirmation.printed_by, aids.SimpleConfirmation.printed_by, art61.Contract.printed_by, cbss.IdentifyPersonRequest.printed_by, cbss.ManageAccessRequest.printed_by, cbss.RetrieveTIGroupsRequest.printed_by, debts.Budget.printed_by, immersion.Contract.printed_by, isip.Contract.printed_by, jobs.Contract.printed_by
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
  - PROTECT : art61.Contract.ending, immersion.Contract.ending, isip.Contract.ending, jobs.Contract.ending
- isip.ContractType :
  - PROTECT : isip.Contract.type
- isip.ExamPolicy :
  - PROTECT : art61.Contract.exam_policy, art61.ContractType.exam_policy, immersion.Contract.exam_policy, immersion.ContractType.exam_policy, isip.Contract.exam_policy, isip.ContractType.exam_policy, jobs.Contract.exam_policy, jobs.ContractType.exam_policy
- jobs.ContractType :
  - PROTECT : jobs.Contract.type, jobs.Job.contract_type
- jobs.Job :
  - PROTECT : jobs.Candidature.job, jobs.Contract.job
- jobs.JobProvider :
  - PROTECT : jobs.Job.provider, jobs.Offer.provider
- jobs.JobType :
  - PROTECT : jobs.Job.type
- jobs.Schedule :
  - PROTECT : jobs.Contract.schedule
- languages.Language :
  - PROTECT : cv.LanguageKnowledge.language, cv.Study.language, cv.Training.language
- ledger.Journal :
  - PROTECT : ledger.MatchRule.journal, ledger.Voucher.journal
- ledger.PaymentTerm :
  - PROTECT : contacts.Partner.payment_term, vatless.AccountInvoice.payment_term
- ledger.Voucher :
  - CASCADE : ledger.Movement.voucher
  - PROTECT : finan.BankStatement.voucher_ptr, finan.Grouper.voucher_ptr, finan.JournalEntry.voucher_ptr, finan.PaymentOrder.voucher_ptr, vatless.AccountInvoice.voucher_ptr
- newcomers.Broker :
  - PROTECT : pcsw.Client.broker
- newcomers.Faculty :
  - PROTECT : newcomers.Competence.faculty, pcsw.Client.faculty
- notes.EventType :
  - PROTECT : notes.Note.event_type, system.SiteConfig.system_note_type
- notes.NoteType :
  - PROTECT : notes.Note.type
- outbox.Mail :
  - CASCADE : outbox.Attachment.mail, outbox.Recipient.mail
- pcsw.Activity :
  - PROTECT : contacts.Partner.activity
- pcsw.AidType :
  - PROTECT : pcsw.Client.aid_type
- pcsw.Client :
  - CASCADE : aids.IncomeConfirmation.client, aids.RefundConfirmation.client, aids.SimpleConfirmation.client, dupable_clients.Word.owner, pcsw.Coaching.client, pcsw.Dispense.client
  - PROTECT : active_job_search.Proof.client, aids.Granting.client, art61.Contract.client, cal.Event.project, cal.Task.project, cbss.IdentifyPersonRequest.person, cbss.ManageAccessRequest.person, cbss.RetrieveTIGroupsRequest.person, courses.CourseRequest.person, excerpts.Excerpt.project, finan.BankStatementItem.project, finan.GrouperItem.project, finan.JournalEntryItem.project, finan.PaymentOrderItem.project, immersion.Contract.client, isip.Contract.client, jobs.Candidature.person, jobs.Contract.client, ledger.Movement.project, notes.Note.project, outbox.Mail.project, pcsw.ClientContact.client, pcsw.Conviction.client, pcsw.Exclusion.person, uploads.Upload.project, vatless.InvoiceItem.project
- pcsw.ClientContactType :
  - PROTECT : aids.AidType.pharmacy_type, aids.RefundConfirmation.doctor_type, contacts.Partner.client_contact_type, pcsw.ClientContact.type
- pcsw.CoachingEnding :
  - PROTECT : pcsw.Coaching.ending
- pcsw.CoachingType :
  - PROTECT : pcsw.Coaching.type, pcsw.CoachingEnding.type, users.User.coaching_type
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
  - PROTECT : finan.PaymentOrderItem.bank_account, sepa.Statement.account, vatless.AccountInvoice.bank_account
- sepa.Statement :
  - PROTECT : sepa.Movement.statement
- uploads.UploadType :
  - PROTECT : uploads.Upload.type
- users.User :
  - PROTECT : aids.Granting.user, aids.IncomeConfirmation.user, aids.RefundConfirmation.user, aids.SimpleConfirmation.user, art61.Contract.user, cal.Event.user, cal.RecurrentEvent.user, cal.Subscription.user, cal.Task.user, cbss.IdentifyPersonRequest.user, cbss.ManageAccessRequest.user, cbss.RetrieveTIGroupsRequest.user, changes.Change.user, cv.Obstacle.user, debts.Budget.user, excerpts.Excerpt.user, immersion.Contract.user, isip.Contract.user, jobs.Contract.user, ledger.Voucher.user, newcomers.Competence.user, notes.Note.user, notifier.Notification.user, outbox.Mail.user, pcsw.Coaching.user, plausibility.Problem.user, polls.Poll.user, polls.Response.user, tinymce.TextFieldTemplate.user, uploads.Upload.user, users.Authority.user
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
 6    alicia     Allmanns Alicia   184
 9    caroline
 5    hubert     Huppertz Hubert   183
 10   judith     Jousten Judith    186
 12   kerstin
 4    melanie    Mélard Mélanie    182
 8    nicolas
 1    robin
 3    rolf
 2    romain
 7    theresia   Thelen Theresia   185
 11   wilfried
==== ========== ================= =====
<BLANKLINE>

The message is the same whether you try on the Person or on the Partner:

>>> obj = contacts.Person.objects.get(id=184)
>>> print(obj.disable_delete())
Cannot delete Partner Allmanns Alicia because 29 Participants refer to it.

>>> obj = contacts.Partner.objects.get(id=184)
>>> print(obj.disable_delete())
Cannot delete Partner Allmanns Alicia because 29 Participants refer to it.


You can delete a partner when a person or some other MTI child exists:

>>> obj = contacts.Partner.objects.get(id=190)
>>> print(obj.disable_delete())
Cannot delete Partner Die neue Alternative V.o.G. because 2 Budget Entries refer to it.

