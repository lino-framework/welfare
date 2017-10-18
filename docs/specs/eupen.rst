.. doctest docs/specs/eupen.rst

.. _welfare.tested.eupen:
.. _welfare.specs.eupen:

=======================
Lino Welfare à la Eupen
=======================

.. doctest init:
   
    >>> from lino import startup
    >>> startup('lino_welfare.projects.eupen.settings.doctests')
    >>> from lino.api.doctest import *
    
.. contents:: 
   :local:
   :depth: 2


Overview
--------

Lino Welfare à la Eupen is the oldest Lino application in the world,
it was the first Lino who went into production. This was in 2010.


>>> print(analyzer.show_complexity_factors())
- 64 plugins
- 140 models
- 538 views
- 15 user types
- 14 dialog actions
<BLANKLINE>


Don't read me
-------------

The remaining part of this document is meant rather for testing than
for explaining.


The main menu
=============

.. _rolf:

Rolf
----

Rolf is the local system administrator, he has a complete menu:

>>> rt.login('rolf').show_menu()
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
- Kontakte : Personen,  ▶ Klienten, Organisationen, -, Partner (alle), Haushalte
- Büro : Meine Benachrichtigungen, Meine Auszüge, Ablaufende Uploads, Meine Uploads, Mein E-Mail-Ausgang, Meine Ereignisse/Notizen, Meine Datenkontrollliste
- Kalender : Kalender, Meine Termine, Überfällige Termine, Unbestätigte Termine, Meine Aufgaben, Meine Gäste, Meine Anwesenheiten, Meine überfälligen Termine
- Empfang : Klienten, Termine heute, Wartende Besucher, Beschäftigte Besucher, Gegangene Besucher, Meine Warteschlange
- ÖSHZ : Klienten, Meine Begleitungen, Zu bestätigende Hilfebeschlüsse
- Buchhaltung :
  - Rechnungseingänge : Rechnungseingänge (REG), Sammelrechnungen (SREG)
  - Ausgabeanweisungen : Ausgabeanweisungen (AAW)
  - Zahlungsaufträge : KBC Zahlungsaufträge (ZKBC)
- DSBE :
  - Klienten
  - VSEs
  - Art.60§7-Konventionen
  - Stellenanbieter
  - Stellen
  - Stellenangebote
  - Art.61-Konventionen
  - ZDSS : Meine IdentifyPerson-Anfragen, Meine ManageAccess-Anfragen, Meine Tx25-Anfragen
- Kurse : Kursanbieter, Kursangebote, Offene Kursanfragen
- Erstempfang : Neue Klienten, Verfügbare Begleiter
- Schuldnerberatung : Klienten, Meine Budgets
- Berichte :
  - Buchhaltung : Buchhaltungsbericht, Schuldner, Gläubiger
  - DSBE : Benutzer und ihre Klienten, Übersicht Art.60§7-Konventionen, Tätigkeitsbericht
- Konfigurierung :
  - System : Site-Parameter, Benutzer, Hilfetexte, Update all summary data
  - Orte : Länder, Orte
  - Kontakte : Organisationsarten, Funktionen, Gremien, Haushaltsarten
  - Eigenschaften : Eigenschaftsgruppen, Eigenschafts-Datentypen, Fachkompetenzen, Sozialkompetenzen, Hindernisse
  - Büro : Auszugsarten, Upload-Arten, Notizarten, Ereignisarten, Meine Einfügetexte
  - Kalender : Kalenderliste, Räume, Prioritäten, Regelmäßige Ereignisse, Gastrollen, Kalendereintragsarten, Wiederholungsregeln, Externe Kalender
  - Buchhaltung : Kontengruppen, Haushaltsartikel, Journale, Buchungsperioden, Zahlungsbedingungen
  - ÖSHZ : Dienste, Begleitungsbeendigungsgründe, Klientenkontaktarten, Integrationsphasen, Berufe, AG-Sperrgründe, Dispenzgründe, Hilfearten, Kategorien
  - Lebenslauf : Sprachen, Bildungsarten, Akademische Grade, Sektoren, Funktionen, Arbeitsregimes, Statuus, Vertragsdauern
  - DSBE : VSE-Arten, Vertragsbeendigungsgründe, Auswertungsstrategien, Art.60§7-Konventionsarten, Stellenarten, Stundenpläne, Art.61-Konventionsarten
  - Kurse : Kursinhalte
  - Erstempfang : Vermittler, Fachbereiche
  - ZDSS : Sektoren, Eigenschafts-Codes
  - Schuldnerberatung : Kontengruppen, Konten, Budget-Kopiervorlage
- Explorer :
  - Kontakte : Kontaktpersonen, Partner, Adressenarten, Adressen, Gremienmitglieder, Haushaltsmitgliedsrollen, Mitglieder, Verwandtschaftsbeziehungen, Verwandschaftsarten
  - System : Vollmachten, Benutzerarten, Datenbankmodelle, Benachrichtigungen, Änderungen, All dashboard widgets, Datentests, Datenprobleme
  - Eigenschaften : Eigenschaften
  - Büro : Auszüge, Uploads, Upload-Bereiche, E-Mail-Ausgänge, Anhänge, Ereignisse/Notizen, Einfügetexte
  - Kalender : Kalendereinträge, Aufgaben, Anwesenheiten, Abonnements, Termin-Zustände, Gast-Zustände, Aufgaben-Zustände
  - ÖSHZ : Begleitungen, Klientenkontakte, AG-Sperren, Vorstrafen, Klienten, Zivilstände, Bearbeitungszustände Klienten, eID-Kartenarten, Hilfebeschlüsse, Einkommensbescheinigungen, Kostenübernahmescheine, Einfache Bescheinigungen, Phonetische Wörter
  - Buchhaltung : Gemeinkonten, Begleichungsregeln, Belege, Belegarten, Bewegungen, Geschäftsjahre, Handelsarten, Journalgruppen, Rechnungen
  - SEPA : Bankkonten, Importierte  Bankkonten, Kontoauszüge, Transaktionen
  - Finanzjournale : Kontoauszüge, Diverse Buchungen, Zahlungsaufträge
  - Lebenslauf : Sprachkenntnisse, Ausbildungen, Studien, Berufserfahrungen
  - DSBE : VSEs, Art.60§7-Konventionen, Stellenanfragen, Vertragspartner, Art.61-Konventionen, ESF Summaries, ESF fields
  - Kurse : Kurse, Kursanfragen
  - Erstempfang : Kompetenzen
  - ZDSS : IdentifyPerson-Anfragen, ManageAccess-Anfragen, Tx25-Anfragen
  - Schuldnerberatung : Budgets, Einträge
- Site : Info

.. _hubert:

Hubert
------

Hubert is an Integration agent.

>>> with translation.override('de'):
...     rt.login('hubert').show_menu()
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF -SKIP
- Kontakte : Personen,  ▶ Klienten, Organisationen, -, Partner (alle), Haushalte
- Büro : Meine Benachrichtigungen, Meine Auszüge, Ablaufende Uploads, Meine Uploads, Mein E-Mail-Ausgang, Meine Ereignisse/Notizen, Meine Datenkontrollliste
- Kalender : Kalender, Meine Termine, Unbestätigte Termine, Meine Aufgaben, Meine Gäste, Meine Anwesenheiten, Meine überfälligen Termine
- Empfang : Klienten, Termine heute, Wartende Besucher, Beschäftigte Besucher, Gegangene Besucher, Meine Warteschlange
- ÖSHZ : Klienten, Meine Begleitungen, Zu bestätigende Hilfebeschlüsse
- DSBE :
  - Klienten
  - VSEs
  - Art.60§7-Konventionen
  - Stellenanbieter
  - Stellen
  - Stellenangebote
  - Art.61-Konventionen
  - ZDSS : Meine IdentifyPerson-Anfragen, Meine ManageAccess-Anfragen, Meine Tx25-Anfragen
- Kurse : Kursanbieter, Kursangebote, Offene Kursanfragen
- Berichte :
  - DSBE : Benutzer und ihre Klienten, Übersicht Art.60§7-Konventionen, Tätigkeitsbericht
- Konfigurierung :
  - Büro : Meine Einfügetexte
- Explorer :
  - Kontakte : Partner
  - SEPA : Importierte  Bankkonten, Kontoauszüge, Transaktionen
  - DSBE : VSEs, Art.60§7-Konventionen, Art.61-Konventionen
- Site : Info


.. _melanie:

Mélanie
-------

Mélanie is a manager of the Integration service.

>>> p = rt.login('melanie').get_user().user_type
>>> print(p)
Begleiter im DSBE (Manager)
>>> p.role  #doctest: +ELLIPSIS
<lino_welfare.modlib.integ.roles.IntegrationStaff object at ...>


Because Mélanie has her :attr:`language
<lino.modlib.users.models.User.language>` field set to French, we need
to explicitly override the language of :meth:`show_menu
<lino.core.requests.BaseRequest.show_menu>` to get her menu in German:

>>> rt.login('melanie').show_menu(language="de")
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF -SKIP
- Kontakte : Personen,  ▶ Klienten, Organisationen, -, Partner (alle), Haushalte
- Büro : Meine Benachrichtigungen, Meine Auszüge, Ablaufende Uploads, Meine Uploads, Mein E-Mail-Ausgang, Meine Ereignisse/Notizen, Meine Datenkontrollliste
- Kalender : Kalender, Meine Termine, Überfällige Termine, Unbestätigte Termine, Meine Aufgaben, Meine Gäste, Meine Anwesenheiten, Meine überfälligen Termine
- Empfang : Klienten, Termine heute, Wartende Besucher, Beschäftigte Besucher, Gegangene Besucher, Meine Warteschlange
- ÖSHZ : Klienten, Meine Begleitungen, Zu bestätigende Hilfebeschlüsse
- DSBE :
  - Klienten
  - VSEs
  - Art.60§7-Konventionen
  - Stellenanbieter
  - Stellen
  - Stellenangebote
  - Art.61-Konventionen
  - ZDSS : Meine IdentifyPerson-Anfragen, Meine ManageAccess-Anfragen, Meine Tx25-Anfragen
- Kurse : Kursanbieter, Kursangebote, Offene Kursanfragen
- Berichte :
  - DSBE : Benutzer und ihre Klienten, Übersicht Art.60§7-Konventionen, Tätigkeitsbericht
- Konfigurierung :
  - Orte : Länder, Orte
  - Kontakte : Organisationsarten, Funktionen, Haushaltsarten
  - Büro : Upload-Arten, Notizarten, Ereignisarten, Meine Einfügetexte
  - Kalender : Kalenderliste, Räume, Prioritäten, Regelmäßige Ereignisse, Kalendereintragsarten, Wiederholungsregeln, Externe Kalender
  - ÖSHZ : Dienste, Begleitungsbeendigungsgründe, Klientenkontaktarten, Integrationsphasen, Berufe, AG-Sperrgründe, Dispenzgründe, Hilfearten, Kategorien
  - Lebenslauf : Sprachen, Bildungsarten, Akademische Grade, Sektoren, Funktionen, Arbeitsregimes, Statuus, Vertragsdauern
  - DSBE : VSE-Arten, Vertragsbeendigungsgründe, Auswertungsstrategien, Art.60§7-Konventionsarten, Stellenarten, Stundenpläne, Art.61-Konventionsarten
  - Kurse : Kursinhalte
  - Erstempfang : Vermittler, Fachbereiche
- Explorer :
  - Kontakte : Kontaktpersonen, Partner, Adressenarten, Haushaltsmitgliedsrollen, Mitglieder, Verwandtschaftsbeziehungen, Verwandschaftsarten
  - Büro : Uploads, Upload-Bereiche, E-Mail-Ausgänge, Anhänge, Ereignisse/Notizen
  - Kalender : Aufgaben, Abonnements
  - ÖSHZ : Begleitungen, Klientenkontakte, AG-Sperren, Vorstrafen, Klienten, Bearbeitungszustände Klienten, Hilfebeschlüsse, Einkommensbescheinigungen, Kostenübernahmescheine, Einfache Bescheinigungen
  - SEPA : Bankkonten, Importierte  Bankkonten, Kontoauszüge, Transaktionen
  - Lebenslauf : Sprachkenntnisse, Ausbildungen, Studien, Berufserfahrungen
  - DSBE : VSEs, Art.60§7-Konventionen, Stellenanfragen, Vertragspartner, Art.61-Konventionen
  - Kurse : Kurse, Kursanfragen
  - Erstempfang : Kompetenzen
- Site : Info


Kerstin
-------

Kerstin is a debts consultant.

>>> p = rt.login('kerstin').get_user().user_type
>>> print(p)
Schuldenberater

>>> with translation.override('de'):
...     rt.login('kerstin').show_menu()
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF -SKIP
- Kontakte : Personen,  ▶ Klienten, Organisationen, -, Partner (alle), Haushalte
- Büro : Meine Benachrichtigungen, Meine Auszüge, Ablaufende Uploads, Meine Uploads, Mein E-Mail-Ausgang, Meine Ereignisse/Notizen, Meine Datenkontrollliste
- Kalender : Kalender, Meine Termine, Unbestätigte Termine, Meine Aufgaben, Meine Gäste, Meine Anwesenheiten, Meine überfälligen Termine
- Empfang : Klienten, Termine heute, Wartende Besucher, Beschäftigte Besucher, Gegangene Besucher, Meine Warteschlange
- ÖSHZ : Klienten, Meine Begleitungen, Zu bestätigende Hilfebeschlüsse
- DSBE :
  - ZDSS : Meine IdentifyPerson-Anfragen, Meine ManageAccess-Anfragen, Meine Tx25-Anfragen
- Erstempfang : Neue Klienten, Verfügbare Begleiter
- Schuldnerberatung : Klienten, Meine Budgets
- Konfigurierung :
  - Büro : Meine Einfügetexte
  - Schuldnerberatung : Budget-Kopiervorlage
- Explorer :
  - Kontakte : Partner
  - SEPA : Importierte  Bankkonten, Kontoauszüge, Transaktionen
  - DSBE : VSEs, Art.60§7-Konventionen
- Site : Info



Caroline
--------

Caroline is a newcomers consultant.

>>> p = rt.login('caroline').get_user().user_type
>>> print(p)
Berater Erstempfang

>>> with translation.override('de'):
...     rt.login('caroline').show_menu()
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
- Kontakte : Personen,  ▶ Klienten, Organisationen, -, Partner (alle), Haushalte
- Büro : Meine Benachrichtigungen, Meine Auszüge, Ablaufende Uploads, Meine Uploads, Mein E-Mail-Ausgang, Meine Ereignisse/Notizen, Meine Datenkontrollliste
- Kalender : Kalender, Meine Termine, Unbestätigte Termine, Meine Aufgaben, Meine Gäste, Meine Anwesenheiten, Meine überfälligen Termine
- Empfang : Klienten, Termine heute, Wartende Besucher, Beschäftigte Besucher, Gegangene Besucher, Meine Warteschlange
- ÖSHZ : Klienten, Meine Begleitungen, Zu bestätigende Hilfebeschlüsse
- DSBE :
  - ZDSS : Meine IdentifyPerson-Anfragen, Meine ManageAccess-Anfragen, Meine Tx25-Anfragen
- Erstempfang : Neue Klienten, Verfügbare Begleiter
- Konfigurierung :
  - Büro : Meine Einfügetexte
- Explorer :
  - Kontakte : Partner
  - SEPA : Importierte  Bankkonten, Kontoauszüge, Transaktionen
  - DSBE : VSEs, Art.60§7-Konventionen
- Site : Info


.. _theresia:

Theresia
--------

Theresia is a reception clerk.

>>> p = rt.login('theresia').get_user().user_type
>>> print(p)
Empfangsschalter


>>> rt.login('theresia').show_menu(language="de")
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF -SKIP
- Kontakte : Personen,  ▶ Klienten, Organisationen, -, Partner (alle), Haushalte
- Büro : Meine Auszüge, Ablaufende Uploads, Meine Uploads, Meine Ereignisse/Notizen
- Empfang : Klienten, Termine heute, Wartende Besucher, Beschäftigte Besucher, Gegangene Besucher
- ÖSHZ : Meine Begleitungen
- DSBE :
  - ZDSS : Meine IdentifyPerson-Anfragen, Meine ManageAccess-Anfragen, Meine Tx25-Anfragen
- Konfigurierung :
  - Orte : Länder, Orte
  - Kontakte : Organisationsarten, Funktionen, Haushaltsarten
  - ÖSHZ : Dienste, Begleitungsbeendigungsgründe, Klientenkontaktarten, Hilfearten, Kategorien
- Explorer :
  - Kontakte : Kontaktpersonen, Partner, Haushaltsmitgliedsrollen, Mitglieder, Verwandtschaftsbeziehungen, Verwandschaftsarten
  - ÖSHZ : Begleitungen, Klientenkontakte, Bearbeitungszustände Klienten, Hilfebeschlüsse, Einkommensbescheinigungen, Kostenübernahmescheine, Einfache Bescheinigungen
  - SEPA : Importierte  Bankkonten, Kontoauszüge, Transaktionen
- Site : Info


.. _welfare.specs.db_eupen:

Database structure
==================

>>> print(analyzer.show_database_structure())
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
- accounts.Account : id, ref, seqno, name, group, type, common_account, needs_partner, clearable, default_amount, name_fr, name_en, sales_allowed, purchases_allowed, wages_allowed, taxes_allowed, clearings_allowed, bank_po_allowed
- accounts.Group : id, name, ref, account_type, name_fr, name_en
- addresses.Address : id, country, city, zip_code, region, addr1, street_prefix, street, street_no, street_box, addr2, data_source, address_type, partner, remark, primary
- aids.AidType : id, name, company, contact_person, contact_role, excerpt_title, aid_regime, confirmation_type, short_name, board, print_directly, is_integ_duty, is_urgent, confirmed_by_primary_coach, pharmacy_type, address_type, body_template, name_fr, name_en, excerpt_title_fr, excerpt_title_en
- aids.Category : id, name, name_fr, name_en
- aids.Granting : id, start_date, end_date, user, decision_date, board, signer, state, client, aid_type, category, request_date
- aids.IncomeConfirmation : id, created, start_date, end_date, user, company, contact_person, contact_role, printed_by, signer, state, client, granting, remark, language, category, amount
- aids.RefundConfirmation : id, created, start_date, end_date, user, company, contact_person, contact_role, printed_by, signer, state, client, granting, remark, language, doctor_type, doctor, pharmacy
- aids.SimpleConfirmation : id, created, start_date, end_date, user, company, contact_person, contact_role, printed_by, signer, state, client, granting, remark, language
- art61.Contract : id, signer1, signer2, user, company, contact_person, contact_role, printed_by, client, language, applies_from, applies_until, date_decided, date_issued, user_asd, exam_policy, ending, date_ended, duration, reference_person, responsibilities, remark, type, job_title, status, cv_duration, regime, subsidize_10, subsidize_20, subsidize_30, subsidize_40, subsidize_50
- art61.ContractType : id, ref, name, full_name, exam_policy, overlap_group, template, name_fr, name_en
- b2c.Account : id, iban, bic, account_name, owner_name, last_transaction
- b2c.Statement : id, account, statement_number, start_date, end_date, balance_start, balance_end, local_currency
- b2c.Transaction : id, statement, seqno, amount, remote_account, remote_bic, message, eref, remote_owner, remote_owner_address, remote_owner_city, remote_owner_postalcode, remote_owner_country_code, txcd, txcd_issuer, booking_date, value_date
- boards.Board : id, start_date, end_date, name, name_fr, name_en
- boards.Member : id, board, person, role
- cal.Calendar : id, name, description, color, name_fr, name_en
- cal.Event : id, modified, created, project, start_date, start_time, end_date, end_time, build_time, build_method, user, assigned_to, owner_type, owner_id, summary, description, access_class, sequence, auto_type, event_type, transparent, room, priority, state
- cal.EventPolicy : id, start_date, start_time, end_date, end_time, name, every_unit, every, monday, tuesday, wednesday, thursday, friday, saturday, sunday, max_events, event_type, name_fr, name_en
- cal.EventType : id, seqno, name, attach_to_email, email_template, description, is_appointment, all_rooms, locks_user, start_date, event_label, max_conflicting, max_days, invite_client, name_fr, name_en, event_label_fr, event_label_en, esf_field
- cal.Guest : id, event, partner, role, state, remark, waiting_since, busy_since, gone_since
- cal.GuestRole : id, name, name_fr, name_en
- cal.Priority : id, name, ref, name_fr, name_en
- cal.RecurrentEvent : id, start_date, start_time, end_date, end_time, name, user, every_unit, every, monday, tuesday, wednesday, thursday, friday, saturday, sunday, max_events, event_type, description, name_fr, name_en
- cal.RemoteCalendar : id, seqno, type, url_template, username, password, readonly
- cal.Room : id, name, company, contact_person, contact_role, description, name_fr, name_en
- cal.Subscription : id, user, calendar, is_hidden
- cal.Task : id, modified, created, project, start_date, start_time, user, owner_type, owner_id, summary, description, access_class, sequence, auto_type, due_date, due_time, percent, state, delegated
- cbss.IdentifyPersonRequest : id, user, printed_by, person, sent, status, environment, ticket, request_xml, response_xml, debug_messages, info_messages, national_id, birth_date, sis_card_no, id_card_no, first_name, last_name, middle_name, gender, tolerance
- cbss.ManageAccessRequest : id, user, printed_by, person, sent, status, environment, ticket, request_xml, response_xml, debug_messages, info_messages, national_id, birth_date, sis_card_no, id_card_no, first_name, last_name, sector, purpose, start_date, end_date, action, query_register
- cbss.Purpose : id, name, sector_code, code, name_fr, name_en
- cbss.RetrieveTIGroupsRequest : id, user, printed_by, person, sent, status, environment, ticket, request_xml, response_xml, debug_messages, info_messages, national_id, language, history
- cbss.Sector : id, name, code, subcode, abbr, abbr_fr, abbr_en, name_fr, name_en
- changes.Change : id, time, type, user, object_type, object_id, master_type, master_id, diff, changed_fields
- coachings.ClientContact : id, company, contact_person, contact_role, type, client, remark
- coachings.ClientContactType : id, name, name_fr, name_en, is_bailiff, can_refund
- coachings.Coaching : id, start_date, end_date, user, client, type, primary, ending
- coachings.CoachingEnding : id, seqno, name, type, name_fr, name_en
- coachings.CoachingType : id, name, does_integ, does_gss, eval_guestrole, name_fr, name_en
- contacts.Company : id, email, language, url, phone, gsm, fax, modified, created, country, city, zip_code, region, addr1, street_prefix, street, street_no, street_box, addr2, prefix, name, remarks, is_obsolete, activity, client_contact_type, payment_term, partner_ptr, type, vat_id
- contacts.CompanyType : id, name, abbr, abbr_fr, abbr_en, name_fr, name_en
- contacts.Partner : id, email, language, url, phone, gsm, fax, modified, created, country, city, zip_code, region, addr1, street_prefix, street, street_no, street_box, addr2, prefix, name, remarks, is_obsolete, activity, client_contact_type, payment_term
- contacts.Person : id, email, language, url, phone, gsm, fax, modified, created, country, city, zip_code, region, addr1, street_prefix, street, street_no, street_box, addr2, prefix, name, remarks, is_obsolete, activity, client_contact_type, payment_term, partner_ptr, title, first_name, middle_name, last_name, gender, birth_date
- contacts.Role : id, type, person, company
- contacts.RoleType : id, name, name_fr, name_en, use_in_contracts
- contenttypes.ContentType : id, app_label, model
- countries.Country : name, isocode, short_code, iso3, inscode, actual_country, name_fr, name_en
- countries.Place : id, parent, name, country, zip_code, type, show_type, inscode, name_fr, name_en
- cv.Duration : id, name, name_fr, name_en
- cv.EducationLevel : id, seqno, name, is_study, is_training, name_fr, name_en
- cv.Experience : id, start_date, end_date, country, city, zip_code, sector, function, person, duration_text, company, title, status, duration, regime, is_training, remarks, termination_reason
- cv.Function : id, name, remark, sector, name_fr, name_en
- cv.LanguageKnowledge : id, person, language, spoken, written, spoken_passively, written_passively, native, cef_level
- cv.Regime : id, name, name_fr, name_en
- cv.Sector : id, name, remark, name_fr, name_en
- cv.Status : id, name, name_fr, name_en
- cv.Study : id, start_date, end_date, country, city, zip_code, person, duration_text, language, school, state, remarks, type, education_level, content
- cv.StudyType : id, name, is_study, is_training, education_level, name_fr, name_en
- cv.Training : id, start_date, end_date, country, city, zip_code, sector, function, person, duration_text, language, school, state, remarks, type, content, certificates
- dashboard.Widget : id, seqno, user, item_name, visible
- debts.Account : id, ref, seqno, name, group, type, required_for_household, required_for_person, periods, default_amount, name_fr, name_en
- debts.Actor : id, seqno, budget, partner, header, remark
- debts.Budget : id, user, printed_by, date, partner, print_todos, print_empty_rows, include_yearly_incomes, intro, conclusion, dist_amount
- debts.Entry : id, seqno, budget, account_type, account, partner, amount, actor, circa, distribute, todo, remark, description, periods, monthly_rate, bailiff
- debts.Group : id, name, ref, account_type, entries_layout, name_fr, name_en
- dupable_clients.Word : id, word, owner
- esf.ClientSummary : id, printed_by, year, month, esf10, esf20, esf21, esf30, esf40, esf41, esf42, esf43, esf44, esf50, esf60, esf70, master, education_level, children_at_charge, certified_handicap, other_difficulty, result, remark
- excerpts.Excerpt : id, project, build_time, build_method, user, owner_type, owner_id, company, contact_person, contact_role, excerpt_type, language
- excerpts.ExcerptType : id, name, build_method, template, attach_to_email, email_template, certifying, remark, body_template, content_type, primary, backward_compat, print_recipient, print_directly, shortcut, name_fr, name_en
- finan.BankStatement : id, user, journal, entry_date, voucher_date, accounting_period, number, narration, state, voucher_ptr, printed_by, item_account, item_remark, last_item_date, balance1, balance2
- finan.BankStatementItem : id, seqno, project, match, amount, dc, remark, account, partner, date, voucher
- finan.JournalEntry : id, user, journal, entry_date, voucher_date, accounting_period, number, narration, state, voucher_ptr, printed_by, project, item_account, item_remark, last_item_date
- finan.JournalEntryItem : id, seqno, project, match, amount, dc, remark, account, partner, date, voucher
- finan.PaymentOrder : id, user, journal, entry_date, voucher_date, accounting_period, number, narration, state, voucher_ptr, printed_by, item_account, item_remark, total, execution_date
- finan.PaymentOrderItem : id, seqno, project, match, amount, dc, remark, account, partner, bank_account, voucher
- gfks.HelpText : id, content_type, field, help_text
- households.Household : id, email, language, url, phone, gsm, fax, modified, created, country, city, zip_code, region, addr1, street_prefix, street, street_no, street_box, addr2, prefix, name, remarks, is_obsolete, activity, client_contact_type, payment_term, partner_ptr, type
- households.Member : id, start_date, end_date, title, first_name, middle_name, last_name, gender, birth_date, role, person, household, dependency, primary
- households.Type : id, name, name_fr, name_en
- humanlinks.Link : id, type, parent, child
- isip.Contract : id, signer1, signer2, user, printed_by, client, language, applies_from, applies_until, date_decided, date_issued, user_asd, exam_policy, ending, date_ended, type, study_type, stages, goals, duties_asd, duties_dsbe, duties_pcsw, duties_person, user_dsbe
- isip.ContractEnding : id, name, use_in_isip, use_in_jobs, is_success, needs_date_ended
- isip.ContractPartner : id, company, contact_person, contact_role, contract, duties_company
- isip.ContractType : id, name, full_name, exam_policy, overlap_group, template, ref, needs_study_type, name_fr, name_en
- isip.ExamPolicy : id, start_date, start_time, end_date, end_time, name, every_unit, every, monday, tuesday, wednesday, thursday, friday, saturday, sunday, max_events, event_type, name_fr, name_en
- jobs.Candidature : id, sector, function, person, job, date_submitted, remark, state, art60, art61
- jobs.Contract : id, signer1, signer2, user, company, contact_person, contact_role, printed_by, client, language, applies_from, applies_until, date_decided, date_issued, user_asd, exam_policy, ending, date_ended, duration, reference_person, responsibilities, remark, type, job, regime, schedule, hourly_rate, refund_rate
- jobs.ContractType : id, ref, name, full_name, exam_policy, overlap_group, template, name_fr, name_en
- jobs.Job : id, sector, function, name, type, provider, contract_type, hourly_rate, capacity, remark
- jobs.JobProvider : id, email, language, url, phone, gsm, fax, modified, created, country, city, zip_code, region, addr1, street_prefix, street, street_no, street_box, addr2, prefix, name, remarks, is_obsolete, activity, client_contact_type, payment_term, partner_ptr, type, vat_id, company_ptr
- jobs.JobType : id, seqno, name, remark, is_social
- jobs.Offer : id, sector, function, name, provider, selection_from, selection_until, start_date, remark
- jobs.Schedule : id, name, name_fr, name_en
- languages.Language : name, id, iso2, name_fr, name_en
- ledger.AccountingPeriod : id, ref, start_date, end_date, state, year, remark
- ledger.Journal : id, ref, seqno, name, build_method, template, trade_type, voucher_type, journal_group, auto_check_clearings, auto_fill_suggestions, force_sequence, account, partner, printed_name, dc, yearly_numbering, must_declare, printed_name_fr, printed_name_en, name_fr, name_en, sepa_account
- ledger.MatchRule : id, account, journal
- ledger.Movement : id, project, voucher, partner, seqno, account, amount, dc, match, cleared, value_date
- ledger.PaymentTerm : id, ref, name, days, months, end_of_month, printed_text, printed_text_fr, printed_text_en, name_fr, name_en
- ledger.Voucher : id, user, journal, entry_date, voucher_date, accounting_period, number, narration, state
- newcomers.Broker : id, name
- newcomers.Competence : id, seqno, user, faculty, weight
- newcomers.Faculty : id, name, weight, name_fr, name_en
- notes.EventType : id, name, remark, body, body_fr, body_en, name_fr, name_en
- notes.Note : id, project, build_time, build_method, user, owner_type, owner_id, company, contact_person, contact_role, date, time, type, event_type, subject, body, language, important
- notes.NoteType : id, name, build_method, template, attach_to_email, email_template, important, remark, special_type, name_fr, name_en
- notify.Message : id, created, user, owner_type, owner_id, message_type, seen, sent, body, mail_mode, subject
- outbox.Attachment : id, owner_type, owner_id, mail
- outbox.Mail : id, project, user, owner_type, owner_id, date, subject, body, sent
- outbox.Recipient : id, mail, partner, type, address, name
- pcsw.Activity : id, name, lst104
- pcsw.AidType : id, name, name_fr, name_en
- pcsw.Client : id, email, language, url, phone, gsm, fax, modified, created, country, city, zip_code, region, addr1, street_prefix, street, street_no, street_box, addr2, prefix, name, remarks, is_obsolete, activity, client_contact_type, payment_term, partner_ptr, title, first_name, middle_name, last_name, gender, birth_date, person_ptr, national_id, birth_country, birth_place, nationality, card_number, card_valid_from, card_valid_until, card_type, card_issuer, noble_condition, client_state, group, civil_state, residence_type, in_belgium_since, residence_until, unemployed_since, seeking_since, needs_residence_permit, needs_work_permit, work_permit_suspended_until, aid_type, declared_name, is_seeking, unavailable_until, unavailable_why, obstacles, skills, job_office_contact, refusal_reason, remarks2, gesdos_id, tim_id, is_cpas, is_senior, health_insurance, pharmacy, income_ag, income_wg, income_kg, income_rente, income_misc, job_agents, broker, faculty, has_esf
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
- sessions.Session : session_key, session_data, expire_date
- system.SiteConfig : id, default_build_method, simulate_today, site_company, signer1, signer2, signer1_function, signer2_function, next_partner_id, propgroup_skills, propgroup_softskills, propgroup_obstacles, default_event_type, site_calendar, max_auto_events, hide_events_before, client_calendar, client_guestrole, team_guestrole, prompt_calendar, master_budget, system_note_type, job_office, residence_permit_upload_type, work_permit_upload_type, driving_licence_upload_type, sector, cbss_org_unit, ssdn_user_id, ssdn_email, cbss_http_username, cbss_http_password
- tinymce.TextFieldTemplate : id, user, name, description, text
- uploads.Upload : id, project, start_date, end_date, file, mimetype, user, owner_type, owner_id, company, contact_person, contact_role, upload_area, type, description, remark, needed
- uploads.UploadType : id, name, upload_area, max_number, wanted, shortcut, warn_expiry_unit, warn_expiry_value, name_fr, name_en
- users.Authority : id, user, authorized
- users.User : id, email, language, modified, created, password, last_login, username, user_type, initials, first_name, last_name, remarks, newcomer_consultations, newcomer_appointments, notify_myself, mail_mode, access_class, event_type, calendar, coaching_type, coaching_supervisor, newcomer_quota, partner
- vatless.AccountInvoice : id, user, journal, entry_date, voucher_date, accounting_period, number, narration, state, voucher_ptr, project, partner, payment_term, match, bank_account, your_ref, due_date, amount
- vatless.InvoiceItem : id, seqno, project, account, voucher, title, amount
- xcourses.Course : id, offer, title, start_date, remark
- xcourses.CourseContent : id, name
- xcourses.CourseOffer : id, title, guest_role, content, provider, description
- xcourses.CourseProvider : id, email, language, url, phone, gsm, fax, modified, created, country, city, zip_code, region, addr1, street_prefix, street, street_no, street_box, addr2, prefix, name, remarks, is_obsolete, activity, client_contact_type, payment_term, partner_ptr, type, vat_id, company_ptr
- xcourses.CourseRequest : id, person, offer, content, date_submitted, urgent, state, course, remark, date_ended
<BLANKLINE>


List of window layouts
======================

The following table lists information about all *data entry form
definitions* (called **window layouts**) used by Lino Welfare.  There
are *detail* layouts, *insert* layouts and *action parameter* layouts.

Each window layout defines a given set of fields.

>>> #settings.SITE.catch_layout_exceptions = False

>>> print(analyzer.show_window_fields())
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
- about.About.show : server_status
- about.Models.detail : app, name, docstring, rows
- accounts.Accounts.detail : ref, group, type, common_account, id, name, name_fr, name_en, needs_partner, clearable, default_amount, MovementsByAccount
- accounts.Accounts.insert : ref, group, type, name, name_fr, name_en
- accounts.Groups.detail : ref, name, name_fr, name_en, account_type, id
- accounts.Groups.insert : name, name_fr, name_en, account_type, ref
- addresses.Addresses.detail : country, city, zip_code, addr1, street, street_no, street_box, addr2, address_type, remark, data_source, partner
- addresses.Addresses.insert : country, city, street, street_no, street_box, address_type, remark
- aids.AidTypes.detail : id, short_name, confirmation_type, name, name_fr, name_en, excerpt_title, excerpt_title_fr, excerpt_title_en, body_template, print_directly, is_integ_duty, is_urgent, confirmed_by_primary_coach, board, company, contact_person, contact_role, pharmacy_type
- aids.AidTypes.insert : name, name_fr, name_en, confirmation_type
- aids.Categories.detail : id, name, name_fr, name_en
- aids.Grantings.detail : id, client, user, signer, workflow_buttons, request_date, board, decision_date, aid_type, category, start_date, end_date, custom_actions
- aids.Grantings.insert : client, aid_type, signer, board, decision_date, start_date, end_date
- aids.GrantingsByClient.insert : aid_type, board, decision_date, start_date, end_date
- aids.IncomeConfirmations.detail : client, user, signer, workflow_buttons, printed, company, contact_person, language, granting, start_date, end_date, category, amount, id, remark
- aids.IncomeConfirmationsByGranting.insert : client, granting, start_date, end_date, category, amount, company, contact_person, language, remark
- aids.RefundConfirmations.detail : id, client, user, signer, workflow_buttons, granting, start_date, end_date, doctor_type, doctor, pharmacy, company, contact_person, language, printed, remark
- aids.RefundConfirmationsByGranting.insert : start_date, end_date, doctor_type, doctor, pharmacy, company, contact_person, language, printed, remark
- aids.SimpleConfirmations.detail : id, client, user, signer, workflow_buttons, granting, start_date, end_date, company, contact_person, language, printed, remark
- aids.SimpleConfirmationsByGranting.insert : start_date, end_date, company, contact_person, language, remark
- art61.ContractTypes.detail : id, name, name_fr, name_en, ref
- art61.Contracts.detail : id, client, user, language, type, company, contact_person, contact_role, applies_from, duration, applies_until, exam_policy, job_title, status, cv_duration, regime, reference_person, remark, printed, date_decided, date_issued, date_ended, ending, subsidize_10, subsidize_20, subsidize_30, subsidize_40, subsidize_50, responsibilities
- art61.Contracts.insert : client, company, type
- b2c.Accounts.detail : iban, bic, last_transaction, owner_name, account_name, partners
- b2c.Statements.detail : account, account__owner_name, account__account_name, statement_number, local_currency, balance_start, start_date, balance_end, end_date
- b2c.Transactions.detail : statement, seqno, booking_date, value_date, amount, remote_account, remote_bic, eref, txcd_text, remote_owner, remote_owner_address, remote_owner_city, remote_owner_postalcode, remote_owner_country_code, message
- boards.Boards.detail : id, name, name_fr, name_en
- boards.Boards.insert : name, name_fr, name_en
- cal.Calendars.detail : name, name_fr, name_en, color, id, description
- cal.Calendars.insert : name, name_fr, name_en, color
- cal.EntriesByClient.insert : event_type, summary, start_date, start_time, end_date, end_time
- cal.EventTypes.detail : name, name_fr, name_en, event_label, event_label_fr, event_label_en, max_conflicting, max_days, esf_field, email_template, id, all_rooms, locks_user, invite_client, is_appointment, attach_to_email
- cal.EventTypes.insert : name, name_fr, name_en, invite_client
- cal.Events.detail : event_type, summary, project, start_date, start_time, end_date, end_time, user, assigned_to, room, priority, access_class, transparent, owner, workflow_buttons, description, id, created, modified, state
- cal.Events.insert : summary, start_date, start_time, end_date, end_time, event_type, project
- cal.GuestRoles.detail : id, name, name_fr, name_en
- cal.GuestStates.wf1 : notify_subject, notify_body, notify_silent
- cal.GuestStates.wf2 : notify_subject, notify_body, notify_silent
- cal.Guests.checkin : notify_subject, notify_body, notify_silent
- cal.Guests.detail : event, partner, role, state, remark, workflow_buttons, waiting_since, busy_since, gone_since
- cal.Guests.insert : event, partner, role
- cal.RecurrentEvents.detail : name, name_fr, name_en, id, user, event_type, start_date, start_time, end_date, end_time, every_unit, every, max_events, monday, tuesday, wednesday, thursday, friday, saturday, sunday, description
- cal.RecurrentEvents.insert : name, name_fr, name_en, start_date, end_date, every_unit, event_type
- cal.Rooms.detail : id, name, name_fr, name_en, company, contact_person, description
- cal.Rooms.insert : id, name, name_fr, name_en, company, contact_person
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
- coachings.ClientContactTypes.detail : id, name, name_fr, name_en, can_refund, is_bailiff
- coachings.CoachingEndings.detail : id, name, name_fr, name_en, seqno
- coachings.Coachings.create_visit : user, summary
- contacts.Companies.detail : overview, prefix, name, type, vat_id, client_contact_type, url, email, phone, gsm, fax, remarks, payment_term, vatless_VouchersByPartner, ledger_MovementsByPartner, id, language, activity, is_obsolete, created, modified
- contacts.Companies.insert : name, email, type, id
- contacts.Companies.merge_row : merge_to, addresses_Address, sepa_Account, reason
- contacts.Partners.detail : overview, id, language, activity, client_contact_type, url, email, phone, gsm, fax, country, region, city, zip_code, addr1, street_prefix, street, street_no, street_box, addr2, remarks, payment_term, vatless_VouchersByPartner, ledger_MovementsByPartner, is_obsolete, created, modified
- contacts.Partners.insert : name, email
- contacts.Persons.create_household : partner, type, head
- contacts.Persons.detail : overview, title, first_name, middle_name, last_name, gender, birth_date, age, id, language, email, phone, gsm, fax, households_MembersByPerson, humanlinks_LinksByHuman, remarks, payment_term, vatless_VouchersByPartner, ledger_MovementsByPartner, activity, url, client_contact_type, is_obsolete, created, modified
- contacts.Persons.insert : first_name, last_name, gender, email
- countries.Countries.detail : isocode, name, name_fr, name_en, short_code, inscode, actual_country
- countries.Countries.insert : isocode, inscode, name, name_fr, name_en
- countries.Places.detail : name, name_fr, name_en, country, inscode, zip_code, parent, type, id
- countries.Places.merge_row : merge_to, reason
- cv.Durations.detail : id, name, name_fr, name_en
- cv.EducationLevels.detail : name, name_fr, name_en, is_study, is_training
- cv.Experiences.detail : person, company, country, city, sector, function, title, status, duration, regime, is_training, start_date, end_date, duration_text, termination_reason, remarks
- cv.ExperiencesByPerson.insert : start_date, end_date, company, function
- cv.Functions.detail : id, name, name_fr, name_en, sector, remark
- cv.LanguageKnowledgesByPerson.detail : language, native, cef_level, spoken_passively, spoken, written
- cv.LanguageKnowledgesByPerson.insert : language, native, cef_level, spoken_passively, spoken, written
- cv.Regimes.detail : id, name, name_fr, name_en
- cv.Sectors.detail : id, name, name_fr, name_en, remark
- cv.Statuses.detail : id, name, name_fr, name_en
- cv.Studies.detail : person, start_date, end_date, duration_text, type, content, education_level, state, school, country, city, remarks
- cv.StudiesByPerson.insert : start_date, end_date, type, content
- cv.StudyTypes.detail : name, name_fr, name_en, id, education_level, is_study, is_training
- cv.StudyTypes.insert : name, name_fr, name_en, is_study, is_training, education_level
- cv.Trainings.detail : person, start_date, end_date, duration_text, type, state, certificates, sector, function, school, country, city, remarks
- cv.Trainings.insert : person, start_date, end_date, type, state, certificates, sector, function, school, country, city
- debts.Accounts.detail : ref, name, name_fr, name_en, group, type, required_for_household, required_for_person, periods, default_amount
- debts.Accounts.insert : ref, group, type, name, name_fr, name_en
- debts.Budgets.detail : date, partner, id, user, intro, ResultByBudget, DebtsByBudget, AssetsByBudgetSummary, conclusion, dist_amount, printed, total_debt, include_yearly_incomes, print_empty_rows, print_todos, DistByBudget, data_box, summary_box
- debts.Budgets.insert : partner, date, user
- debts.Groups.detail : ref, name, name_fr, name_en, id, account_type, entries_layout
- debts.Groups.insert : name, name_fr, name_en, account_type, ref
- esf.Summaries.detail : master, year, month, children_at_charge, certified_handicap, other_difficulty, id, education_level, result, remark, results
- excerpts.ExcerptTypes.detail : id, name, name_fr, name_en, content_type, build_method, template, body_template, email_template, shortcut, primary, print_directly, certifying, print_recipient, backward_compat, attach_to_email
- excerpts.ExcerptTypes.insert : name, name_fr, name_en, content_type, primary, certifying, build_method, template, body_template
- excerpts.Excerpts.detail : id, excerpt_type, project, user, build_method, company, contact_person, language, owner, build_time, body_template_content
- finan.BankStatements.detail : entry_date, number, balance1, balance2, workflow_buttons, ItemsByBankStatement, journal, accounting_period, user, id, item_account, item_remark, MovementsByVoucher
- finan.BankStatements.insert : entry_date, balance1
- finan.DisbursementOrders.detail : journal, number, voucher_date, entry_date, accounting_period, item_account, total, workflow_buttons, narration, item_remark, ItemsByDisbursementOrder, state, user, id, MovementsByVoucher
- finan.DisbursementOrdersByJournal.insert : item_account, voucher_date
- finan.FinancialVouchers.detail : entry_date, number, workflow_buttons, narration, ItemsByJournalEntry, journal, accounting_period, user, id, item_account, item_remark, MovementsByVoucher
- finan.FinancialVouchers.insert : entry_date, narration
- finan.PaymentOrders.detail : entry_date, number, total, execution_date, workflow_buttons, narration, ItemsByPaymentOrder, journal, accounting_period, user, id, item_account, item_remark, MovementsByVoucher
- gfks.ContentTypes.detail : id, app_label, model, base_classes
- households.Households.detail : type, prefix, name, id
- households.HouseholdsByType.detail : type, prefix, name, language, id, country, region, city, zip_code, street_prefix, street, street_no, street_box, addr2, phone, gsm, email, url
- households.Types.detail : name, name_fr, name_en
- humanlinks.Links.detail : parent, type, child
- humanlinks.Links.insert : parent, type, child
- integ.ActivityReport.show : body
- isip.ContractEndings.detail : name, use_in_isip, use_in_jobs, is_success, needs_date_ended
- isip.ContractPartners.detail : company, contact_person, contact_role, duties_company
- isip.ContractTypes.detail : id, ref, exam_policy, needs_study_type, name, name_fr, name_en, full_name
- isip.Contracts.detail : id, client, type, user, user_dsbe, user_asd, study_type, applies_from, applies_until, exam_policy, language, date_decided, date_issued, printed, date_ended, ending, stages, goals, duties_person, duties_asd, duties_dsbe, duties_pcsw
- isip.Contracts.insert : client, type
- isip.ExamPolicies.detail : id, name, name_fr, name_en, max_events, every, every_unit, event_type, monday, tuesday, wednesday, thursday, friday, saturday, sunday
- jobs.ContractTypes.detail : id, name, name_fr, name_en, ref
- jobs.Contracts.detail : id, client, user, user_asd, language, job, type, company, contact_person, contact_role, applies_from, duration, applies_until, exam_policy, regime, schedule, hourly_rate, refund_rate, reference_person, remark, printed, date_decided, date_issued, date_ended, ending, responsibilities
- jobs.Contracts.insert : client, job
- jobs.JobProviders.detail : overview, prefix, name, type, vat_id, client_contact_type, url, email, phone, gsm, fax
- jobs.JobTypes.detail : id, name, is_social
- jobs.Jobs.detail : name, provider, contract_type, type, id, sector, function, capacity, hourly_rate, remark
- jobs.Jobs.insert : name, provider, contract_type, type, sector, function
- jobs.JobsOverview.show : body
- jobs.Offers.detail : name, provider, sector, function, selection_from, selection_until, start_date, remark
- jobs.Schedules.detail : id, name, name_fr, name_en
- languages.Languages.detail : id, iso2, name, name_fr, name_en
- ledger.AccountingReport.show : body
- ledger.Journals.detail : name, name_fr, name_en, ref, seqno, voucher_type, journal_group, build_method, template, id, trade_type, account, partner, dc, force_sequence, yearly_numbering, auto_fill_suggestions, auto_check_clearings, must_declare, printed_name, printed_name_fr, printed_name_en
- ledger.Journals.insert : ref, name, name_fr, name_en, journal_group, voucher_type
- ledger.PaymentTerms.detail : ref, months, days, end_of_month, name, name_fr, name_en, printed_text, printed_text_fr, printed_text_en
- ledger.Situation.show : body
- newcomers.AvailableCoachesByClient.assign_coach : notify_subject, notify_body, notify_silent
- newcomers.Faculties.detail : id, name, name_fr, name_en, weight
- newcomers.Faculties.insert : name, name_fr, name_en, weight
- notes.EventTypes.detail : id, name, name_fr, name_en, remark
- notes.NoteTypes.detail : id, name, name_fr, name_en, build_method, template, special_type, email_template, attach_to_email, remark
- notes.NoteTypes.insert : name, name_fr, name_en, build_method
- notes.Notes.detail : date, time, event_type, type, project, subject, important, company, contact_person, user, language, build_time, id, body, uploads_UploadsByController
- notes.Notes.insert : event_type, type, subject, project
- outbox.Mails.detail : subject, project, date, user, sent, id, owner, outbox_AttachmentsByMail, uploads_UploadsByController, body
- outbox.Mails.insert : project, subject, body
- pcsw.Clients.create_visit : user, summary
- pcsw.Clients.detail : overview, gender, id, tim_id, first_name, middle_name, last_name, birth_date, age, national_id, nationality, declared_name, civil_state, birth_country, birth_place, language, email, phone, fax, gsm, image, AgentsByClient, dupable_clients_SimilarClients, humanlinks_LinksByHuman, cbss_relations, households_MembersByPerson, workflow_buttons, id_document, broker, faculty, refusal_reason, in_belgium_since, residence_type, gesdos_id, job_agents, group, income_ag, income_wg, income_kg, income_rente, income_misc, seeking_since, unemployed_since, work_permit_suspended_until, needs_residence_permit, needs_work_permit, uploads_UploadsByClient, cvs_emitted, cv_LanguageKnowledgesByPerson, skills, obstacles, excerpts_ExcerptsByProject, MovementsByProject, activity, client_state, noble_condition, unavailable_until, unavailable_why, is_cpas, is_senior, is_obsolete, created, modified, remarks, remarks2, plausibility_ProblemsByOwner, cbss_identify_person, cbss_manage_access, cbss_retrieve_ti_groups, cbss_summary
- pcsw.Clients.insert : first_name, last_name, national_id, gender, language
- pcsw.Clients.merge_row : merge_to, aids_IncomeConfirmation, aids_RefundConfirmation, aids_SimpleConfirmation, coachings_Coaching, cv_LanguageKnowledge, dupable_clients_Word, pcsw_Dispense, properties_PersonProperty, addresses_Address, sepa_Account, reason
- pcsw.Clients.refuse_client : reason, remark
- plausibility.Checkers.detail : value, text
- plausibility.Problems.detail : checker, owner, message, user, id
- properties.PropGroups.detail : id, name, name_fr, name_en
- properties.PropTypes.detail : id, name, name_fr, name_en, choicelist, default_value
- properties.Properties.detail : id, group, type, name, name_fr, name_en
- reception.BusyVisitors.detail : event, client, role, state, remark, workflow_buttons
- reception.GoneVisitors.detail : event, client, role, state, remark, workflow_buttons
- reception.MyWaitingVisitors.detail : event, client, role, state, remark, workflow_buttons
- reception.WaitingVisitors.detail : event, client, role, state, remark, workflow_buttons
- sepa.AccountsByPartner.insert : iban, bic, remark
- system.SiteConfigs.detail : site_company, next_partner_id, job_office, master_budget, signer1, signer2, signer1_function, signer2_function, system_note_type, default_build_method, propgroup_skills, propgroup_softskills, propgroup_obstacles, residence_permit_upload_type, work_permit_upload_type, driving_licence_upload_type, default_event_type, prompt_calendar, hide_events_before, client_guestrole, team_guestrole, cbss_org_unit, sector, ssdn_user_id, ssdn_email, cbss_http_username, cbss_http_password
- tinymce.TextFieldTemplates.detail : id, name, user, description, text
- tinymce.TextFieldTemplates.insert : name, user
- uploads.AllUploads.detail : file, user, upload_area, type, description, owner
- uploads.AllUploads.insert : type, description, file, user
- uploads.UploadTypes.detail : id, upload_area, shortcut, name, name_fr, name_en, warn_expiry_unit, warn_expiry_value, wanted, max_number
- uploads.UploadTypes.insert : upload_area, name, name_fr, name_en, warn_expiry_unit, warn_expiry_value
- uploads.Uploads.detail : user, project, id, type, description, start_date, end_date, needed, company, contact_person, contact_role, file, owner, remark
- uploads.Uploads.insert : type, file, start_date, end_date, description
- uploads.UploadsByClient.insert : file, type, end_date, description
- uploads.UploadsByController.insert : file, type, end_date, description
- users.AllUsers.send_welcome_email : email, subject
- users.Users.change_password : current, new1, new2
- users.Users.detail : username, user_type, partner, first_name, last_name, initials, email, language, mail_mode, id, created, modified, remarks, event_type, access_class, calendar, newcomer_quota, coaching_type, coaching_supervisor, newcomer_consultations, newcomer_appointments
- users.Users.insert : username, email, first_name, last_name, partner, language, user_type
- users.UsersOverview.sign_in : username, password
- vatless.Invoices.detail : journal, number, entry_date, voucher_date, accounting_period, workflow_buttons, partner, payment_term, due_date, bank_account, your_ref, narration, amount, ItemsByInvoice, match, state, user, id, MovementsByVoucher
- vatless.Invoices.insert : journal, partner, entry_date
- vatless.InvoicesByJournal.insert : partner, entry_date
- vatless.ProjectInvoicesByJournal.detail : journal, number, entry_date, voucher_date, accounting_period, workflow_buttons, project, narration, partner, your_ref, payment_term, due_date, bank_account, amount, ItemsByProjectInvoice, match, state, user, id, MovementsByVoucher
- vatless.ProjectInvoicesByJournal.insert : project, partner, entry_date
- xcourses.CourseContents.detail : id, name
- xcourses.CourseOffers.detail : id, title, content, provider, guest_role, description
- xcourses.CourseOffers.insert : provider, content, title
- xcourses.CourseProviders.detail : overview, prefix, name, type, vat_id, client_contact_type, url, email, phone, gsm, fax
- xcourses.CourseRequests.detail : date_submitted, person, content, offer, urgent, course, state, date_ended, id, remark, uploads_UploadsByController
- xcourses.Courses.detail : id, start_date, offer, title, remark
- xcourses.Courses.insert : start_date, offer, title
<BLANKLINE>


Windows and permissions
=======================

Each window layout is **viewable** by a given set of user user_types.

>>> print(analyzer.show_window_permissions())
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
- about.About.show : visible for all
- about.Models.detail : visible for 100 110 120 200 210 220 300 400 410 500 510 800 admin 910
- accounts.Accounts.detail : visible for 510 admin 910
- accounts.Accounts.insert : visible for 510 admin 910
- accounts.Groups.detail : visible for 510 admin 910
- accounts.Groups.insert : visible for 510 admin 910
- addresses.Addresses.detail : visible for admin 910
- addresses.Addresses.insert : visible for admin 910
- aids.AidTypes.detail : visible for 110 210 410 500 510 800 admin 910
- aids.AidTypes.insert : visible for 110 210 410 500 510 800 admin 910
- aids.Categories.detail : visible for 110 210 410 500 510 800 admin 910
- aids.Grantings.detail : visible for 100 110 120 200 210 300 400 410 500 510 800 admin 910
- aids.Grantings.insert : visible for 100 110 120 200 210 300 400 410 500 510 800 admin 910
- aids.GrantingsByClient.insert : visible for 100 110 120 200 210 300 400 410 500 510 800 admin 910
- aids.IncomeConfirmations.detail : visible for 100 110 120 200 210 300 400 410 500 510 800 admin 910
- aids.IncomeConfirmationsByGranting.insert : visible for 100 110 120 200 210 300 400 410 500 510 800 admin 910
- aids.RefundConfirmations.detail : visible for 100 110 120 200 210 300 400 410 500 510 800 admin 910
- aids.RefundConfirmationsByGranting.insert : visible for 100 110 120 200 210 300 400 410 500 510 800 admin 910
- aids.SimpleConfirmations.detail : visible for 100 110 120 200 210 300 400 410 500 510 800 admin 910
- aids.SimpleConfirmationsByGranting.insert : visible for 100 110 120 200 210 300 400 410 500 510 800 admin 910
- art61.ContractTypes.detail : visible for 110 admin 910
- art61.Contracts.detail : visible for 100 110 120 admin 910
- art61.Contracts.insert : visible for 100 110 120 admin 910
- b2c.Accounts.detail : visible for 100 110 120 200 210 300 400 410 500 510 800 admin 910
- b2c.Statements.detail : visible for 100 110 120 200 210 300 400 410 500 510 800 admin 910
- b2c.Transactions.detail : visible for 100 110 120 200 210 300 400 410 500 510 800 admin 910
- boards.Boards.detail : visible for admin 910
- boards.Boards.insert : visible for admin 910
- cal.Calendars.detail : visible for 110 410 admin 910
- cal.Calendars.insert : visible for 110 410 admin 910
- cal.EntriesByClient.insert : visible for 100 110 120 200 300 400 410 500 510 admin 910
- cal.EventTypes.detail : visible for 110 410 admin 910
- cal.EventTypes.insert : visible for 110 410 admin 910
- cal.Events.detail : visible for 110 410 admin 910
- cal.Events.insert : visible for 110 410 admin 910
- cal.GuestRoles.detail : visible for admin 910
- cal.GuestStates.wf1 : visible for 100 110 120 200 210 220 300 400 410 500 510 800 admin 910
- cal.GuestStates.wf2 : visible for 100 110 120 200 210 220 300 400 410 500 510 800 admin 910
- cal.Guests.checkin : visible for 100 110 120 200 210 220 300 400 410 500 510 800 admin 910
- cal.Guests.detail : visible for 100 110 120 200 210 220 300 400 410 500 510 800 admin 910
- cal.Guests.insert : visible for 100 110 120 200 210 220 300 400 410 500 510 800 admin 910
- cal.RecurrentEvents.detail : visible for 110 410 admin 910
- cal.RecurrentEvents.insert : visible for 110 410 admin 910
- cal.Rooms.detail : visible for 110 410 admin 910
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
- coachings.ClientContactTypes.detail : visible for 110 210 410 admin 910
- coachings.CoachingEndings.detail : visible for 110 210 410 admin 910
- coachings.Coachings.create_visit : visible for 110 210 410 admin 910
- contacts.Companies.detail : visible for 100 110 120 200 210 220 300 400 410 500 510 800 admin 910
- contacts.Companies.insert : visible for 100 110 120 200 210 220 300 400 410 500 510 800 admin 910
- contacts.Companies.merge_row : visible for 110 210 410 800 admin 910
- contacts.Partners.detail : visible for 100 110 120 200 210 220 300 400 410 500 510 800 admin 910
- contacts.Partners.insert : visible for 100 110 120 200 210 220 300 400 410 500 510 800 admin 910
- contacts.Persons.create_household : visible for 100 110 120 200 210 220 300 400 410 500 510 800 admin 910
- contacts.Persons.detail : visible for 100 110 120 200 210 220 300 400 410 500 510 800 admin 910
- contacts.Persons.insert : visible for 100 110 120 200 210 220 300 400 410 500 510 800 admin 910
- countries.Countries.detail : visible for 110 210 410 800 admin 910
- countries.Countries.insert : visible for 110 210 410 800 admin 910
- countries.Places.detail : visible for 110 210 410 800 admin 910
- countries.Places.merge_row : visible for 110 210 410 800 admin 910
- cv.Durations.detail : visible for 110 admin 910
- cv.EducationLevels.detail : visible for 110 admin 910
- cv.Experiences.detail : visible for 110 admin 910
- cv.ExperiencesByPerson.insert : visible for 100 110 120 admin 910
- cv.Functions.detail : visible for 110 admin 910
- cv.LanguageKnowledgesByPerson.detail : visible for 100 110 120 admin 910
- cv.LanguageKnowledgesByPerson.insert : visible for 100 110 120 admin 910
- cv.Regimes.detail : visible for 110 admin 910
- cv.Sectors.detail : visible for 110 admin 910
- cv.Statuses.detail : visible for 110 admin 910
- cv.Studies.detail : visible for 110 admin 910
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
- finan.BankStatements.detail : visible for 500 510 admin 910
- finan.BankStatements.insert : visible for 500 510 admin 910
- finan.DisbursementOrders.detail : visible for 500 510 admin 910
- finan.DisbursementOrdersByJournal.insert : visible for 500 510 admin 910
- finan.FinancialVouchers.detail : visible for 500 510 admin 910
- finan.FinancialVouchers.insert : visible for 500 510 admin 910
- finan.PaymentOrders.detail : visible for 500 510 admin 910
- gfks.ContentTypes.detail : visible for admin 910
- households.Households.detail : visible for 100 110 120 200 210 300 400 410 500 510 800 admin 910
- households.HouseholdsByType.detail : visible for 100 110 120 200 210 300 400 410 500 510 800 admin 910
- households.Types.detail : visible for 110 210 410 800 admin 910
- humanlinks.Links.detail : visible for 110 210 410 800 admin 910
- humanlinks.Links.insert : visible for 110 210 410 800 admin 910
- integ.ActivityReport.show : visible for 100 110 120 admin 910
- isip.ContractEndings.detail : visible for 110 410 admin 910
- isip.ContractPartners.detail : visible for 110 410 admin 910
- isip.ContractTypes.detail : visible for 110 410 admin 910
- isip.Contracts.detail : visible for 100 110 120 200 300 400 410 admin 910
- isip.Contracts.insert : visible for 100 110 120 200 300 400 410 admin 910
- isip.ExamPolicies.detail : visible for 110 410 admin 910
- jobs.ContractTypes.detail : visible for 110 410 admin 910
- jobs.Contracts.detail : visible for 100 110 120 200 300 400 410 admin 910
- jobs.Contracts.insert : visible for 100 110 120 200 300 400 410 admin 910
- jobs.JobProviders.detail : visible for 100 110 120 admin 910
- jobs.JobTypes.detail : visible for 110 410 admin 910
- jobs.Jobs.detail : visible for 100 110 120 admin 910
- jobs.Jobs.insert : visible for 100 110 120 admin 910
- jobs.JobsOverview.show : visible for 100 110 120 admin 910
- jobs.Offers.detail : visible for 100 110 120 admin 910
- jobs.Schedules.detail : visible for 110 410 admin 910
- languages.Languages.detail : visible for 110 410 admin 910
- ledger.AccountingReport.show : visible for 500 510 admin 910
- ledger.Journals.detail : visible for 510 admin 910
- ledger.Journals.insert : visible for 510 admin 910
- ledger.PaymentTerms.detail : visible for 510 admin 910
- ledger.Situation.show : visible for 500 510 admin 910
- newcomers.AvailableCoachesByClient.assign_coach : visible for 110 120 200 220 300 800 admin 910
- newcomers.Faculties.detail : visible for 110 410 admin 910
- newcomers.Faculties.insert : visible for 110 410 admin 910
- notes.EventTypes.detail : visible for 110 410 admin 910
- notes.NoteTypes.detail : visible for 110 410 admin 910
- notes.NoteTypes.insert : visible for 110 410 admin 910
- notes.Notes.detail : visible for 100 110 120 200 210 220 300 400 410 500 510 800 admin 910
- notes.Notes.insert : visible for 100 110 120 200 210 220 300 400 410 500 510 800 admin 910
- outbox.Mails.detail : visible for 110 410 admin 910
- outbox.Mails.insert : visible for 110 410 admin 910
- pcsw.Clients.create_visit : visible for 100 110 120 200 210 220 300 400 410 500 510 800 admin 910
- pcsw.Clients.detail : visible for 100 110 120 200 210 220 300 400 410 500 510 800 admin 910
- pcsw.Clients.insert : visible for 100 110 120 200 210 220 300 400 410 500 510 800 admin 910
- pcsw.Clients.merge_row : visible for 110 210 410 800 admin 910
- pcsw.Clients.refuse_client : visible for 120 200 220 300 admin 910
- plausibility.Checkers.detail : visible for admin 910
- plausibility.Problems.detail : visible for 100 110 120 200 210 220 300 400 410 500 510 800 admin 910
- properties.PropGroups.detail : visible for admin 910
- properties.PropTypes.detail : visible for admin 910
- properties.Properties.detail : visible for admin 910
- reception.BusyVisitors.detail : visible for 100 110 120 200 210 220 300 400 410 500 510 800 admin 910
- reception.GoneVisitors.detail : visible for 100 110 120 200 210 220 300 400 410 500 510 800 admin 910
- reception.MyWaitingVisitors.detail : visible for 100 110 120 200 300 400 410 500 510 admin 910
- reception.WaitingVisitors.detail : visible for 100 110 120 200 210 220 300 400 410 500 510 800 admin 910
- sepa.AccountsByPartner.insert : visible for 100 110 120 200 210 300 400 410 500 510 800 admin 910
- system.SiteConfigs.detail : visible for admin 910
- tinymce.TextFieldTemplates.detail : visible for admin 910
- tinymce.TextFieldTemplates.insert : visible for admin 910
- uploads.AllUploads.detail : visible for 110 410 admin 910
- uploads.AllUploads.insert : visible for 110 410 admin 910
- uploads.UploadTypes.detail : visible for 110 410 admin 910
- uploads.UploadTypes.insert : visible for 110 410 admin 910
- uploads.Uploads.detail : visible for 100 110 120 200 210 220 300 400 410 500 510 800 admin 910
- uploads.Uploads.insert : visible for 100 110 120 200 210 220 300 400 410 500 510 800 admin 910
- uploads.UploadsByClient.insert : visible for 100 110 120 200 210 300 400 410 500 510 800 admin 910
- uploads.UploadsByController.insert : visible for 100 110 120 200 210 220 300 400 410 500 510 800 admin 910
- users.AllUsers.send_welcome_email : visible for admin 910
- users.Users.change_password : visible for 100 110 120 200 210 220 300 400 410 500 510 800 admin 910
- users.Users.detail : visible for 100 110 120 200 210 220 300 400 410 500 510 800 admin 910
- users.Users.insert : visible for 100 110 120 200 210 220 300 400 410 500 510 800 admin 910
- users.UsersOverview.sign_in : visible for all
- vatless.Invoices.detail : visible for 500 510 admin 910
- vatless.Invoices.insert : visible for 500 510 admin 910
- vatless.InvoicesByJournal.insert : visible for 500 510 admin 910
- vatless.ProjectInvoicesByJournal.detail : visible for 500 510 admin 910
- vatless.ProjectInvoicesByJournal.insert : visible for 500 510 admin 910
- xcourses.CourseContents.detail : visible for 110 admin 910
- xcourses.CourseOffers.detail : visible for 100 110 120 admin 910
- xcourses.CourseOffers.insert : visible for 100 110 120 admin 910
- xcourses.CourseProviders.detail : visible for 100 110 120 admin 910
- xcourses.CourseRequests.detail : visible for 110 admin 910
- xcourses.Courses.detail : visible for 110 admin 910
- xcourses.Courses.insert : visible for 110 admin 910
<BLANKLINE>



Visibility of eID reader actions
================================

Here is a list of the eid card reader actions and their availability
per user user_type.

>>> from lino_xl.lib.beid.actions import BaseBeIdReadCardAction
>>> print(analyzer.show_action_permissions(BaseBeIdReadCardAction))
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
- debts.Clients.find_by_beid : visible for 120 300 admin 910
- debts.Clients.read_beid : visible for 120 300 admin 910
- integ.Clients.find_by_beid : visible for 100 110 120 admin 910
- integ.Clients.read_beid : visible for 100 110 120 admin 910
- newcomers.ClientsByFaculty.find_by_beid : visible for 100 110 120 200 210 220 300 400 410 800 admin 910
- newcomers.ClientsByFaculty.read_beid : visible for 100 110 120 200 210 220 300 400 410 800 admin 910
- newcomers.NewClients.find_by_beid : visible for 120 200 220 300 admin 910
- newcomers.NewClients.read_beid : visible for 120 200 220 300 admin 910
- pcsw.AllClients.find_by_beid : visible for 110 410 admin 910
- pcsw.AllClients.read_beid : visible for 110 410 admin 910
- pcsw.Clients.find_by_beid : visible for 100 110 120 200 210 220 300 400 410 800 admin 910
- pcsw.Clients.read_beid : visible for 100 110 120 200 210 220 300 400 410 800 admin 910
- pcsw.ClientsByNationality.find_by_beid : visible for 100 110 120 200 210 220 300 400 410 800 admin 910
- pcsw.ClientsByNationality.read_beid : visible for 100 110 120 200 210 220 300 400 410 800 admin 910
- pcsw.CoachedClients.find_by_beid : visible for 100 110 120 200 300 400 410 admin 910
- pcsw.CoachedClients.read_beid : visible for 100 110 120 200 300 400 410 admin 910
- reception.Clients.find_by_beid : visible for 100 110 120 200 210 220 300 400 410 800 admin 910
- reception.Clients.read_beid : visible for 100 110 120 200 210 220 300 400 410 800 admin 910
<BLANKLINE>


Dialog actions
==============

Global list of all actions that have a parameter dialog.

>>> show_dialog_actions()
... #doctest: +REPORT_UDIFF +NORMALIZE_WHITESPACE
- cal.GuestStates.wf1 : Zusagen
  (main) [visible for all]: **Kurzbeschreibung** (notify_subject), **Beschreibung** (notify_body), **Keine Mitteilung an andere** (notify_silent)
- cal.GuestStates.wf2 : Absagen
  (main) [visible for all]: **Kurzbeschreibung** (notify_subject), **Beschreibung** (notify_body), **Keine Mitteilung an andere** (notify_silent)
- cal.Guests.checkin : Einchecken
  (main) [visible for all]: **Kurzbeschreibung** (notify_subject), **Beschreibung** (notify_body), **Keine Mitteilung an andere** (notify_silent)
- coachings.Coachings.create_visit : Visite erstellen
  (main) [visible for all]: **Benutzer** (user), **Begründung** (summary)
- contacts.Companies.merge_row : Fusionieren
  (main) [visible for all]:
  - **nach...** (merge_to)
  - **Auch vergängliche verknüpfte Objekte überweisen** (keep_volatiles): **Adressen** (addresses_Address), **Bankkonten** (sepa_Account)
  - **Begründung** (reason)
- contacts.Persons.create_household : Haushalt erstellen
  (main) [visible for all]: **Partner** (partner), **Haushaltsart** (type), **Vorstand** (head)
- countries.Places.merge_row : Fusionieren
  (main) [visible for all]: **nach...** (merge_to), **Begründung** (reason)
- newcomers.AvailableCoachesByClient.assign_coach : Zuweisen
  (main) [visible for all]: **Kurzbeschreibung** (notify_subject), **Beschreibung** (notify_body), **Keine Mitteilung an andere** (notify_silent)
- pcsw.Clients.create_visit : Visite erstellen
  (main) [visible for all]: **Benutzer** (user), **Begründung** (summary)
- pcsw.Clients.merge_row : Fusionieren
  (main) [visible for all]:
  - **nach...** (merge_to)
  - **Auch vergängliche verknüpfte Objekte überweisen** (keep_volatiles):
    - (keep_volatiles_1): **Einkommensbescheinigungen** (aids_IncomeConfirmation), **Kostenübernahmescheine** (aids_RefundConfirmation)
    - (keep_volatiles_2): **Einfache Bescheinigungen** (aids_SimpleConfirmation), **Begleitungen** (coachings_Coaching)
    - (keep_volatiles_3): **Sprachkenntnisse** (cv_LanguageKnowledge), **Phonetische Wörter** (dupable_clients_Word)
    - (keep_volatiles_4): **Dispenzen** (pcsw_Dispense), **Eigenschaften** (properties_PersonProperty)
    - (keep_volatiles_5): **Adressen** (addresses_Address), **Bankkonten** (sepa_Account)
  - **Begründung** (reason)
- pcsw.Clients.refuse_client : Ablehnen
  (main) [visible for all]: **Ablehnungsgrund** (reason), **Bemerkung** (remark)
- users.AllUsers.send_welcome_email : Welcome mail
  (main) [visible for all]: **E-Mail-Adresse** (email), **Betreff** (subject)
- users.Users.change_password : Passwort ändern
  (main) [visible for all]: **Aktuelles Passwort** (current), **Neues Passwort** (new1), **Neues Passwort nochmal** (new2)
- users.UsersOverview.sign_in : Anmelden
  (main) [visible for all]: **Benutzername** (username), **Passwort** (password)
<BLANKLINE>



Menu walk
=========

Here is the output of :func:`walk_menu_items
<lino.api.doctests.walk_menu_items>` for this database:

>>> walk_menu_items('rolf', severe=False)
... #doctest: -ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
- Kontakte --> Personen : 103
- Kontakte --> ▶ Klienten : 58
- Kontakte --> Organisationen : 52
- Kontakte --> Partner (alle) : 175
- Kontakte --> Haushalte : 15
- Büro --> Meine Benachrichtigungen : 2
- Büro --> Meine Auszüge : 0
- Büro --> Ablaufende Uploads : 1
- Büro --> Meine Uploads : 1
- Büro --> Mein E-Mail-Ausgang : 1
- Büro --> Meine Ereignisse/Notizen : 9
- Büro --> Meine Datenkontrollliste : 0
- Kalender --> Meine Termine : 4
- Kalender --> Überfällige Termine : 38
- Kalender --> Unbestätigte Termine : 2
- Kalender --> Meine Aufgaben : 1
- Kalender --> Meine Gäste : 1
- Kalender --> Meine Anwesenheiten : 1
- Kalender --> Meine überfälligen Termine : 3
- Empfang --> Klienten : 30
- Empfang --> Termine heute : 3
- Empfang --> Wartende Besucher : 8
- Empfang --> Beschäftigte Besucher : 4
- Empfang --> Gegangene Besucher : 7
- Empfang --> Meine Warteschlange : 0
- ÖSHZ --> Klienten : 30
- ÖSHZ --> Meine Begleitungen : 1
- ÖSHZ --> Zu bestätigende Hilfebeschlüsse : 1
- Buchhaltung --> Rechnungseingänge --> Rechnungseingänge (REG) : 0
- Buchhaltung --> Rechnungseingänge --> Sammelrechnungen (SREG) : 0
- Buchhaltung --> Ausgabeanweisungen --> Ausgabeanweisungen (AAW) : 0
- Buchhaltung --> Zahlungsaufträge --> KBC Zahlungsaufträge (ZKBC) : 0
- DSBE --> Klienten : 0
- DSBE --> VSEs : 1
- DSBE --> Art.60§7-Konventionen : 1
- DSBE --> Stellenanbieter : 4
- DSBE --> Stellen : 9
- DSBE --> Stellenangebote : 2
- DSBE --> Art.61-Konventionen : 1
- DSBE --> ZDSS --> Meine IdentifyPerson-Anfragen : 1
- DSBE --> ZDSS --> Meine ManageAccess-Anfragen : 1
- DSBE --> ZDSS --> Meine Tx25-Anfragen : 1
- Kurse --> Kursanbieter : 3
- Kurse --> Kursangebote : 4
- Kurse --> Offene Kursanfragen : 20
- Erstempfang --> Neue Klienten : 23
- Erstempfang --> Verfügbare Begleiter : 3
- Schuldnerberatung --> Klienten : 0
- Schuldnerberatung --> Meine Budgets : 4
- Berichte --> Buchhaltung --> Schuldner : 5
- Berichte --> Buchhaltung --> Gläubiger : 10
- Berichte --> DSBE --> Benutzer und ihre Klienten : 3
- Konfigurierung --> System --> Benutzer : 14
- Konfigurierung --> System --> Hilfetexte : 6
- Konfigurierung --> Orte --> Länder : 271
- Konfigurierung --> Orte --> Orte : 79
- Konfigurierung --> Kontakte --> Organisationsarten : 15
- Konfigurierung --> Kontakte --> Funktionen : 6
- Konfigurierung --> Kontakte --> Gremien : 4
- Konfigurierung --> Kontakte --> Haushaltsarten : 7
- Konfigurierung --> Eigenschaften --> Eigenschaftsgruppen : 4
- Konfigurierung --> Eigenschaften --> Eigenschafts-Datentypen : 4
- Konfigurierung --> Eigenschaften --> Fachkompetenzen : 0
- Konfigurierung --> Eigenschaften --> Sozialkompetenzen : 0
- Konfigurierung --> Eigenschaften --> Hindernisse : 0
- Konfigurierung --> Büro --> Auszugsarten : 22
- Konfigurierung --> Büro --> Upload-Arten : 10
- Konfigurierung --> Büro --> Notizarten : 14
- Konfigurierung --> Büro --> Ereignisarten : 11
- Konfigurierung --> Büro --> Meine Einfügetexte : 1
- Konfigurierung --> Kalender --> Kalenderliste : 13
- Konfigurierung --> Kalender --> Räume : 1
- Konfigurierung --> Kalender --> Prioritäten : 5
- Konfigurierung --> Kalender --> Regelmäßige Ereignisse : 16
- Konfigurierung --> Kalender --> Gastrollen : 5
- Konfigurierung --> Kalender --> Kalendereintragsarten : 11
- Konfigurierung --> Kalender --> Wiederholungsregeln : 7
- Konfigurierung --> Kalender --> Externe Kalender : 1
- Konfigurierung --> Buchhaltung --> Kontengruppen : 7
- Konfigurierung --> Buchhaltung --> Haushaltsartikel : 27
- Konfigurierung --> Buchhaltung --> Journale : 5
- Konfigurierung --> Buchhaltung --> Buchungsperioden : 30
- Konfigurierung --> Buchhaltung --> Zahlungsbedingungen : 9
- Konfigurierung --> ÖSHZ --> Dienste : 4
- Konfigurierung --> ÖSHZ --> Begleitungsbeendigungsgründe : 5
- Konfigurierung --> ÖSHZ --> Klientenkontaktarten : 11
- Konfigurierung --> ÖSHZ --> Integrationsphasen : 6
- Konfigurierung --> ÖSHZ --> Berufe : 1
- Konfigurierung --> ÖSHZ --> AG-Sperrgründe : 3
- Konfigurierung --> ÖSHZ --> Dispenzgründe : 5
- Konfigurierung --> ÖSHZ --> Hilfearten : 12
- Konfigurierung --> ÖSHZ --> Kategorien : 4
- Konfigurierung --> Lebenslauf --> Sprachen : 6
- Konfigurierung --> Lebenslauf --> Bildungsarten : 12
- Konfigurierung --> Lebenslauf --> Akademische Grade : 6
- Konfigurierung --> Lebenslauf --> Sektoren : 15
- Konfigurierung --> Lebenslauf --> Funktionen : 5
- Konfigurierung --> Lebenslauf --> Arbeitsregimes : 4
- Konfigurierung --> Lebenslauf --> Statuus : 8
- Konfigurierung --> Lebenslauf --> Vertragsdauern : 6
- Konfigurierung --> DSBE --> VSE-Arten : 6
- Konfigurierung --> DSBE --> Vertragsbeendigungsgründe : 5
- Konfigurierung --> DSBE --> Auswertungsstrategien : 7
- Konfigurierung --> DSBE --> Art.60§7-Konventionsarten : 6
- Konfigurierung --> DSBE --> Stellenarten : 6
- Konfigurierung --> DSBE --> Stundenpläne : 4
- Konfigurierung --> DSBE --> Art.61-Konventionsarten : 2
- Konfigurierung --> Kurse --> Kursinhalte : 3
- Konfigurierung --> Erstempfang --> Vermittler : 3
- Konfigurierung --> Erstempfang --> Fachbereiche : 6
- Konfigurierung --> ZDSS --> Sektoren : 210
- Konfigurierung --> ZDSS --> Eigenschafts-Codes : 107
- Konfigurierung --> Schuldnerberatung --> Kontengruppen : 9
- Konfigurierung --> Schuldnerberatung --> Konten : 52
- Explorer --> Kontakte --> Kontaktpersonen : 11
- Explorer --> Kontakte --> Partner : 175
- Explorer --> Kontakte --> Adressenarten : 6
- Explorer --> Kontakte --> Adressen : 180
- Explorer --> Kontakte --> Gremienmitglieder : 1
- Explorer --> Kontakte --> Haushaltsmitgliedsrollen : 8
- Explorer --> Kontakte --> Mitglieder : 64
- Explorer --> Kontakte --> Verwandtschaftsbeziehungen : 60
- Explorer --> Kontakte --> Verwandschaftsarten : 13
- Explorer --> System --> Vollmachten : 4
- Explorer --> System --> Benutzerarten : 15
- Explorer --> System --> Datenbankmodelle : 141
- Explorer --> System --> Benachrichtigungen : 14
- Explorer --> System --> Änderungen : 0
- Explorer --> System --> All dashboard widgets : 1
- Explorer --> System --> Datentests : 15
- Explorer --> System --> Datenprobleme : 64
- Explorer --> Eigenschaften --> Eigenschaften : 24
- Explorer --> Büro --> Auszüge : 69
- Explorer --> Büro --> Uploads : 12
- Explorer --> Büro --> Upload-Bereiche : 1
- Explorer --> Büro --> E-Mail-Ausgänge : 1
- Explorer --> Büro --> Anhänge : 1
- Explorer --> Büro --> Ereignisse/Notizen : 112
- Explorer --> Büro --> Einfügetexte : 3
- Explorer --> Kalender --> Kalendereinträge : 301
- Explorer --> Kalender --> Aufgaben : 36
- Explorer --> Kalender --> Anwesenheiten : 623
- Explorer --> Kalender --> Abonnements : 10
- Explorer --> Kalender --> Termin-Zustände : 5
- Explorer --> Kalender --> Gast-Zustände : 9
- Explorer --> Kalender --> Aufgaben-Zustände : 5
- Explorer --> ÖSHZ --> Begleitungen : 91
- Explorer --> ÖSHZ --> Klientenkontakte : 15
- Explorer --> ÖSHZ --> AG-Sperren : 1
- Explorer --> ÖSHZ --> Vorstrafen : 1
- Explorer --> ÖSHZ --> Klienten : 58
- Explorer --> ÖSHZ --> Zivilstände : 7
- Explorer --> ÖSHZ --> Bearbeitungszustände Klienten : 4
- Explorer --> ÖSHZ --> eID-Kartenarten : 11
- Explorer --> ÖSHZ --> Hilfebeschlüsse : 59
- Explorer --> ÖSHZ --> Einkommensbescheinigungen : 59
- Explorer --> ÖSHZ --> Kostenübernahmescheine : 13
- Explorer --> ÖSHZ --> Einfache Bescheinigungen : 20
- Explorer --> ÖSHZ --> Phonetische Wörter : 132
- Explorer --> Buchhaltung --> Gemeinkonten : 18
- Explorer --> Buchhaltung --> Begleichungsregeln : 3
- Explorer --> Buchhaltung --> Belege : 56
- Explorer --> Buchhaltung --> Belegarten : 6
- Explorer --> Buchhaltung --> Bewegungen : 602
- Explorer --> Buchhaltung --> Geschäftsjahre : 8
- Explorer --> Buchhaltung --> Handelsarten : 3
- Explorer --> Buchhaltung --> Journalgruppen : 5
- Explorer --> Buchhaltung --> Rechnungen : 31
- Explorer --> SEPA --> Bankkonten : 80
- Explorer --> SEPA --> Importierte  Bankkonten : 34
- Explorer --> SEPA --> Kontoauszüge : 34
- Explorer --> SEPA --> Transaktionen : 57
- Explorer --> Finanzjournale --> Kontoauszüge : 1
- Explorer --> Finanzjournale --> Diverse Buchungen : 1
- Explorer --> Finanzjournale --> Zahlungsaufträge : 27
- Explorer --> Lebenslauf --> Sprachkenntnisse : 113
- Explorer --> Lebenslauf --> Ausbildungen : 21
- Explorer --> Lebenslauf --> Studien : 23
- Explorer --> Lebenslauf --> Berufserfahrungen : 31
- Explorer --> DSBE --> VSEs : 34
- Explorer --> DSBE --> Art.60§7-Konventionen : 17
- Explorer --> DSBE --> Stellenanfragen : 75
- Explorer --> DSBE --> Vertragspartner : 39
- Explorer --> DSBE --> Art.61-Konventionen : 8
- Explorer --> DSBE --> ESF Summaries : 0
- Explorer --> DSBE --> ESF fields : 12
- Explorer --> Kurse --> Kurse : 4
- Explorer --> Kurse --> Kursanfragen : 20
- Explorer --> Erstempfang --> Kompetenzen : 8
- Explorer --> ZDSS --> IdentifyPerson-Anfragen : 6
- Explorer --> ZDSS --> ManageAccess-Anfragen : 2
- Explorer --> ZDSS --> Tx25-Anfragen : 7
- Explorer --> Schuldnerberatung --> Budgets : 15
- Explorer --> Schuldnerberatung --> Einträge : 717
<BLANKLINE>


The murderer bug
================

Before 20150623 it was possible to inadvertently cause a cascaded
delete by calling `delete` on an object in a script. For example the
following line would have deleted client 127 and all related data
instead of raising an exception:

>>> pcsw.Client.objects.get(id=127).delete()
Traceback (most recent call last):
...
Warning: Kann Partner Evers Eberhart nicht l\xf6schen weil 27 Anwesenheiten darauf verweisen.


Some requests
=============

Some choices lists:

>>> kw = dict()
>>> fields = 'count rows'
>>> demo_get('rolf', 'choices/cv/SkillsByPerson/property', fields, 6, **kw)
>>> demo_get('rolf', 'choices/cv/ObstaclesByPerson/property', fields, 15, **kw)


