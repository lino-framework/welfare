.. _welfare.specs.db_eupen:

==================
Database structure
==================

.. How to test only this document:

    $ python setup.py test -s tests.SpecsTests.test_db_eupen

    >>> from lino import startup
    >>> startup('lino_welfare.projects.eupen.settings.doctests')
    >>> from lino.api.doctest import *
    
.. contents:: 
   :local:
   :depth: 2


Database structure
==================

>>> print(analyzer.show_database_structure())
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
- accounts.Account : id, ref, seqno, name, group, type, needs_partner, clearable, default_amount, name_fr, name_en, sales_allowed, purchases_allowed, wages_allowed, clearings_allowed
- accounts.Group : id, name, ref, account_type, name_fr, name_en
- addresses.Address : id, country, city, zip_code, region, addr1, street_prefix, street, street_no, street_box, addr2, data_source, address_type, partner, remark, primary
- aids.AidType : id, name, company, contact_person, contact_role, excerpt_title, aid_regime, confirmation_type, short_name, board, print_directly, is_integ_duty, is_urgent, confirmed_by_primary_coach, pharmacy_type, address_type, body_template, name_fr, name_en, excerpt_title_fr, excerpt_title_en
- aids.Category : id, name, name_fr, name_en
- aids.Granting : id, start_date, end_date, user, decision_date, board, signer, state, client, aid_type, category, request_date
- aids.IncomeConfirmation : id, created, start_date, end_date, company, contact_person, contact_role, user, printed_by, signer, state, client, granting, remark, language, category, amount
- aids.RefundConfirmation : id, created, start_date, end_date, company, contact_person, contact_role, user, printed_by, signer, state, client, granting, remark, language, doctor_type, doctor, pharmacy
- aids.SimpleConfirmation : id, created, start_date, end_date, company, contact_person, contact_role, user, printed_by, signer, state, client, granting, remark, language
- art61.Contract : id, signer1, signer2, company, contact_person, contact_role, user, printed_by, client, language, applies_from, applies_until, date_decided, date_issued, user_asd, exam_policy, ending, date_ended, duration, reference_person, responsibilities, remark, type, job_title, status, cv_duration, regime, subsidize_10, subsidize_20, subsidize_30, subsidize_40, subsidize_50
- art61.ContractType : id, ref, name, full_name, exam_policy, overlap_group, template, name_fr, name_en
- b2c.Account : id, iban, bic, account_name, owner_name, last_transaction
- b2c.Statement : id, account, statement_number, start_date, end_date, balance_start, balance_end, local_currency
- b2c.Transaction : id, statement, seqno, amount, remote_account, remote_bic, message, eref, remote_owner, remote_owner_address, remote_owner_city, remote_owner_postalcode, remote_owner_country_code, txcd, txcd_issuer, booking_date, value_date
- boards.Board : id, start_date, end_date, name, name_fr, name_en
- boards.Member : id, board, person, role
- cal.Calendar : id, name, description, color, name_fr, name_en
- cal.Event : id, modified, created, project, start_date, start_time, end_date, end_time, build_time, build_method, user, assigned_to, owner_type, owner_id, summary, description, access_class, sequence, auto_type, event_type, transparent, room, priority, state
- cal.EventType : id, seqno, name, attach_to_email, email_template, description, is_appointment, all_rooms, locks_user, start_date, event_label, max_conflicting, invite_client, name_fr, name_en, event_label_fr, event_label_en, esf_field
- cal.Guest : id, event, partner, role, state, remark, waiting_since, busy_since, gone_since
- cal.GuestRole : id, name, name_fr, name_en
- cal.Priority : id, name, ref, name_fr, name_en
- cal.RecurrentEvent : id, start_date, start_time, end_date, end_time, name, user, every_unit, every, monday, tuesday, wednesday, thursday, friday, saturday, sunday, max_events, event_type, description, name_fr, name_en
- cal.RemoteCalendar : id, seqno, type, url_template, username, password, readonly
- cal.Room : id, name, name_fr, name_en
- cal.Subscription : id, user, calendar, is_hidden
- cal.Task : id, modified, created, project, start_date, start_time, user, owner_type, owner_id, summary, description, access_class, sequence, auto_type, due_date, due_time, percent, state, delegated
- cbss.IdentifyPersonRequest : id, user, printed_by, person, sent, status, environment, ticket, request_xml, response_xml, debug_messages, info_messages, national_id, birth_date, sis_card_no, id_card_no, first_name, last_name, middle_name, gender, tolerance
- cbss.ManageAccessRequest : id, user, printed_by, person, sent, status, environment, ticket, request_xml, response_xml, debug_messages, info_messages, national_id, birth_date, sis_card_no, id_card_no, first_name, last_name, sector, purpose, start_date, end_date, action, query_register
- cbss.Purpose : id, name, sector_code, code, name_fr, name_en
- cbss.RetrieveTIGroupsRequest : id, user, printed_by, person, sent, status, environment, ticket, request_xml, response_xml, debug_messages, info_messages, national_id, language, history
- cbss.Sector : id, name, code, subcode, abbr, abbr_fr, abbr_en, name_fr, name_en
- changes.Change : id, time, type, user, object_type, object_id, master_type, master_id, diff
- contacts.Company : id, modified, created, country, city, zip_code, region, addr1, street_prefix, street, street_no, street_box, addr2, url, phone, gsm, fax, name, language, email, remarks, is_obsolete, activity, client_contact_type, payment_term, partner_ptr, prefix, type, vat_id
- contacts.CompanyType : id, name, abbr, abbr_fr, abbr_en, name_fr, name_en
- contacts.Partner : id, modified, created, country, city, zip_code, region, addr1, street_prefix, street, street_no, street_box, addr2, url, phone, gsm, fax, name, language, email, remarks, is_obsolete, activity, client_contact_type, payment_term
- contacts.Person : id, modified, created, country, city, zip_code, region, addr1, street_prefix, street, street_no, street_box, addr2, url, phone, gsm, fax, name, language, email, remarks, is_obsolete, activity, client_contact_type, payment_term, partner_ptr, title, first_name, middle_name, last_name, gender, birth_date
- contacts.Role : id, type, person, company
- contacts.RoleType : id, name, name_fr, name_en, use_in_contracts
- contenttypes.ContentType : id, app_label, model
- countries.Country : name, isocode, short_code, iso3, inscode, actual_country, name_fr, name_en
- countries.Place : id, parent, name, country, zip_code, type, inscode, name_fr, name_en
- courses.Course : id, offer, title, start_date, remark
- courses.CourseContent : id, name
- courses.CourseOffer : id, title, guest_role, content, provider, description
- courses.CourseProvider : id, modified, created, country, city, zip_code, region, addr1, street_prefix, street, street_no, street_box, addr2, url, phone, gsm, fax, name, language, email, remarks, is_obsolete, activity, client_contact_type, payment_term, partner_ptr, prefix, type, vat_id, company_ptr
- courses.CourseRequest : id, person, offer, content, date_submitted, urgent, state, course, remark, date_ended
- cv.Duration : id, name, name_fr, name_en
- cv.EducationLevel : id, seqno, name, is_study, is_training, name_fr, name_en
- cv.Experience : id, start_date, end_date, country, city, zip_code, sector, function, person, company, title, status, duration, regime, is_training, remarks, termination_reason
- cv.Function : id, name, remark, sector, name_fr, name_en
- cv.LanguageKnowledge : id, person, language, spoken, written, spoken_passively, written_passively, native, cef_level
- cv.Regime : id, name, name_fr, name_en
- cv.Sector : id, name, remark, name_fr, name_en
- cv.Status : id, name, name_fr, name_en
- cv.Study : id, start_date, end_date, country, city, zip_code, person, language, school, state, remarks, type, education_level, content
- cv.StudyType : id, name, is_study, is_training, education_level, name_fr, name_en
- cv.Training : id, start_date, end_date, country, city, zip_code, sector, function, person, language, school, state, remarks, type, content, certificates
- debts.Account : id, ref, seqno, name, group, type, required_for_household, required_for_person, periods, default_amount, name_fr, name_en
- debts.Actor : id, seqno, budget, partner, header, remark
- debts.Budget : id, user, printed_by, date, partner, print_todos, print_empty_rows, include_yearly_incomes, intro, conclusion, dist_amount
- debts.Entry : id, seqno, budget, account_type, account, partner, amount, actor, circa, distribute, todo, remark, description, periods, monthly_rate, bailiff
- debts.Group : id, name, ref, account_type, entries_layout, name_fr, name_en
- dupable_clients.Word : id, word, owner
- esf.ClientSummary : id, printed_by, year, month, esf10, esf20, esf21, esf30, esf40, esf41, esf42, esf43, esf44, esf50, esf60, esf70, master, education_level, children_at_charge, certified_handicap, other_difficulty, result, remark
- excerpts.Excerpt : id, project, build_time, build_method, company, contact_person, contact_role, user, owner_type, owner_id, excerpt_type, language
- excerpts.ExcerptType : id, name, build_method, template, attach_to_email, email_template, certifying, remark, body_template, content_type, primary, backward_compat, print_recipient, print_directly, shortcut, name_fr, name_en
- finan.BankStatement : id, user, journal, voucher_date, entry_date, accounting_period, number, narration, state, voucher_ptr, printed_by, item_account, item_remark, last_item_date, balance1, balance2
- finan.BankStatementItem : id, seqno, project, match, amount, dc, remark, account, partner, date, voucher
- finan.JournalEntry : id, user, journal, voucher_date, entry_date, accounting_period, number, narration, state, voucher_ptr, printed_by, project, item_account, item_remark, last_item_date
- finan.JournalEntryItem : id, seqno, project, match, amount, dc, remark, account, partner, date, voucher
- finan.PaymentOrder : id, user, journal, voucher_date, entry_date, accounting_period, number, narration, state, voucher_ptr, printed_by, item_account, item_remark, total, execution_date
- finan.PaymentOrderItem : id, seqno, project, match, amount, dc, remark, account, partner, bank_account, voucher
- gfks.HelpText : id, content_type, field, help_text
- households.Household : id, modified, created, country, city, zip_code, region, addr1, street_prefix, street, street_no, street_box, addr2, url, phone, gsm, fax, name, language, email, remarks, is_obsolete, activity, client_contact_type, payment_term, partner_ptr, prefix, type
- households.Member : id, start_date, end_date, title, first_name, middle_name, last_name, gender, birth_date, role, person, household, primary, dependency
- households.Type : id, name, name_fr, name_en
- humanlinks.Link : id, type, parent, child
- isip.Contract : id, signer1, signer2, user, printed_by, client, language, applies_from, applies_until, date_decided, date_issued, user_asd, exam_policy, ending, date_ended, type, study_type, stages, goals, duties_asd, duties_dsbe, duties_person
- isip.ContractEnding : id, name, use_in_isip, use_in_jobs, is_success, needs_date_ended
- isip.ContractPartner : id, company, contact_person, contact_role, contract, duties_company
- isip.ContractType : id, name, full_name, exam_policy, overlap_group, template, ref, needs_study_type, name_fr, name_en
- isip.ExamPolicy : id, start_date, start_time, end_date, end_time, name, every_unit, every, monday, tuesday, wednesday, thursday, friday, saturday, sunday, max_events, event_type, name_fr, name_en
- jobs.Candidature : id, sector, function, person, job, date_submitted, remark, state, art60, art61
- jobs.Contract : id, signer1, signer2, company, contact_person, contact_role, user, printed_by, client, language, applies_from, applies_until, date_decided, date_issued, user_asd, exam_policy, ending, date_ended, duration, reference_person, responsibilities, remark, type, job, regime, schedule, hourly_rate, refund_rate
- jobs.ContractType : id, ref, name, full_name, exam_policy, overlap_group, template, name_fr, name_en
- jobs.Job : id, sector, function, name, type, provider, contract_type, hourly_rate, capacity, remark
- jobs.JobProvider : id, modified, created, country, city, zip_code, region, addr1, street_prefix, street, street_no, street_box, addr2, url, phone, gsm, fax, name, language, email, remarks, is_obsolete, activity, client_contact_type, payment_term, partner_ptr, prefix, type, vat_id, company_ptr
- jobs.JobType : id, seqno, name, remark, is_social
- jobs.Offer : id, sector, function, name, provider, selection_from, selection_until, start_date, remark
- jobs.Schedule : id, name, name_fr, name_en
- languages.Language : name, id, iso2, name_fr, name_en
- ledger.AccountingPeriod : id, ref, start_date, end_date, state, year, remark
- ledger.Journal : id, ref, seqno, name, build_method, template, trade_type, voucher_type, journal_group, auto_check_clearings, force_sequence, account, printed_name, dc, yearly_numbering, printed_name_fr, printed_name_en, name_fr, name_en
- ledger.MatchRule : id, account, journal
- ledger.Movement : id, project, voucher, partner, seqno, account, amount, dc, match, cleared, value_date
- ledger.PaymentTerm : id, ref, name, days, months, end_of_month, printed_text, printed_text_fr, printed_text_en, name_fr, name_en
- ledger.Voucher : id, user, journal, voucher_date, entry_date, accounting_period, number, narration, state
- newcomers.Broker : id, name
- newcomers.Competence : id, seqno, user, faculty, weight
- newcomers.Faculty : id, name, weight, name_fr, name_en
- notes.EventType : id, name, remark, body, body_fr, body_en, name_fr, name_en
- notes.Note : id, project, build_time, build_method, company, contact_person, contact_role, user, owner_type, owner_id, date, time, type, event_type, subject, body, language, important
- notes.NoteType : id, name, build_method, template, attach_to_email, email_template, important, remark, special_type, name_fr, name_en
- notify.Message : id, created, user, owner_type, owner_id, message_type, seen, sent, subject, body
- outbox.Attachment : id, owner_type, owner_id, mail
- outbox.Mail : id, project, user, owner_type, owner_id, date, subject, body, sent
- outbox.Recipient : id, mail, partner, type, address, name
- pcsw.Activity : id, name, lst104
- pcsw.AidType : id, name, name_fr, name_en
- pcsw.Client : id, modified, created, country, city, zip_code, region, addr1, street_prefix, street, street_no, street_box, addr2, url, phone, gsm, fax, name, language, email, remarks, is_obsolete, activity, client_contact_type, payment_term, partner_ptr, title, first_name, middle_name, last_name, gender, birth_date, person_ptr, national_id, nationality, card_number, card_valid_from, card_valid_until, card_type, card_issuer, noble_condition, group, birth_place, birth_country, civil_state, residence_type, in_belgium_since, residence_until, unemployed_since, seeking_since, needs_residence_permit, needs_work_permit, work_permit_suspended_until, aid_type, declared_name, is_seeking, unavailable_until, unavailable_why, obstacles, skills, job_office_contact, client_state, refusal_reason, remarks2, gesdos_id, tim_id, is_cpas, is_senior, health_insurance, pharmacy, income_ag, income_wg, income_kg, income_rente, income_misc, job_agents, broker, faculty, has_esf
- pcsw.ClientContact : id, company, contact_person, contact_role, type, client, remark
- pcsw.ClientContactType : id, name, name_fr, name_en, is_bailiff, can_refund
- pcsw.Coaching : id, start_date, end_date, user, client, type, primary, ending
- pcsw.CoachingEnding : id, seqno, name, type, name_fr, name_en
- pcsw.CoachingType : id, name, does_integ, does_gss, eval_guestrole, name_fr, name_en
- pcsw.Conviction : id, client, date, prejudicial, designation
- pcsw.Dispense : id, client, reason, remarks, start_date, end_date
- pcsw.DispenseReason : id, seqno, name, name_fr, name_en
- pcsw.Exclusion : id, person, type, excluded_from, excluded_until, remark
- pcsw.ExclusionType : id, name
- pcsw.PersonGroup : id, name, ref_name, active
- plausibility.Problem : id, user, owner_type, owner_id, checker, message
- properties.PersonProperty : id, group, property, value, person, remark
- properties.PropChoice : id, type, value, text, text_fr, text_en
- properties.PropGroup : id, name, name_fr, name_en
- properties.PropType : id, name, choicelist, default_value, limit_to_choices, multiple_choices, name_fr, name_en
- properties.Property : id, name, group, type, name_fr, name_en
- sepa.Account : id, partner, iban, bic, remark, primary, account_type, managed
- system.SiteConfig : id, default_build_method, simulate_today, site_company, signer1, signer2, signer1_function, signer2_function, next_partner_id, default_event_type, site_calendar, max_auto_events, hide_events_before, client_calendar, client_guestrole, team_guestrole, prompt_calendar, propgroup_skills, propgroup_softskills, propgroup_obstacles, master_budget, system_note_type, job_office, residence_permit_upload_type, work_permit_upload_type, driving_licence_upload_type, suppliers_account, aids_account, sector, cbss_org_unit, ssdn_user_id, ssdn_email, cbss_http_username, cbss_http_password
- tinymce.TextFieldTemplate : id, user, name, description, text
- uploads.Upload : id, project, start_date, end_date, file, mimetype, company, contact_person, contact_role, user, owner_type, owner_id, upload_area, type, description, remark, needed
- uploads.UploadType : id, name, upload_area, max_number, wanted, shortcut, warn_expiry_unit, warn_expiry_value, name_fr, name_en
- users.Authority : id, user, authorized
- users.User : id, modified, created, username, password, profile, initials, first_name, last_name, email, remarks, language, partner, access_class, event_type, calendar, coaching_type, coaching_supervisor, newcomer_consultations, newcomer_appointments, mail_mode, newcomer_quota
- vatless.AccountInvoice : id, user, journal, voucher_date, entry_date, accounting_period, number, narration, state, voucher_ptr, project, partner, payment_term, match, bank_account, your_ref, due_date, amount
- vatless.InvoiceItem : id, seqno, project, account, voucher, title, amount
<BLANKLINE>
