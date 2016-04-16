.. _welfare.tested.eupen:
.. _welfare.specs.eupen:

=======================
Lino Welfare à la Eupen
=======================

.. How to test only this document:

    $ python setup.py test -s tests.SpecsTests.test_eupen

    >>> from __future__ import print_function
    >>> import lino
    >>> lino.startup('lino_welfare.projects.eupen.settings.doctests')
    >>> from lino.api.doctest import *
    
.. contents:: 
   :local:
   :depth: 2


The murder bug
==============

Before 20150623 it was possible to inadvertently cause a cascaded
delete by calling `delete` on an object in a script. For example the
following line would have deleted client 127 and all related data
instead of raising an exception:

>>> pcsw.Client.objects.get(id=127).delete()
Traceback (most recent call last):
...
Warning: Kann Partner Evers Eberhart nicht l\xf6schen weil 27 Teilnehmer darauf verweisen.


The main menu
=============

.. _rolf:

Rolf
----

Rolf is the local system administrator, he has a complete menu:

>>> rt.login('rolf').show_menu()
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
- Kontakte : Personen,  ▶ Klienten, Organisationen, -, Partner (alle), Haushalte
- Büro : Ablaufende Uploads, Meine Uploads, Mein E-Mail-Ausgang, Meine Auszüge, Meine Ereignisse/Notizen, Meine Datenkontrollliste
- Kalender : Kalender, Meine Termine, Meine Aufgaben, Meine Gäste, Meine Anwesenheiten
- Empfang : Klienten, Termine heute, Wartende Besucher, Beschäftigte Besucher, Gegangene Besucher, Meine Warteschlange
- ÖSHZ : Klienten, Meine Begleitungen, Zu bestätigende Hilfebeschlüsse
- Buchhaltung :
  - Rechnungseingänge : Rechnungseingänge (REG), Sammelrechnungen (SREG)
  - Ausgabeanweisungen : Ausgabeanweisungen (AAW)
  - Zahlungsaufträge : KBC Zahlungsaufträge (ZKBC)
- DSBE : Klienten, VSEs, Art.60§7-Konventionen, Stellenanbieter, Stellen, Stellenangebote, Art.61-Konventionen
- Kurse : Kursanbieter, Kursangebote, Offene Kursanfragen
- Erstempfang : Neue Klienten, Verfügbare Begleiter
- Schuldnerberatung : Klienten, Meine Budgets
- Berichte :
  - System : Broken GFKs
  - Buchhaltung : Situation, Tätigkeitsbericht, Schuldner, Gläubiger
  - DSBE : Benutzer und ihre Klienten, Übersicht Art.60§7-Konventionen, Tätigkeitsbericht
- Konfigurierung :
  - System : Site-Parameter, Hilfetexte, Benutzer, Update all summary data
  - Orte : Länder, Orte
  - Eigenschaften : Eigenschaftsgruppen, Eigenschafts-Datentypen, Fachkompetenzen, Sozialkompetenzen, Hindernisse
  - Kontakte : Organisationsarten, Funktionen, Gremien, Haushaltsarten
  - Büro : Upload-Arten, Auszugsarten, Notizarten, Ereignisarten, Meine Einfügetexte
  - Kalender : Kalenderliste, Räume, Prioritäten, Periodische Terminregeln, Gastrollen, Kalendereintragsarten, Externe Kalender
  - Buchhaltung : Kontengruppen, Haushaltsartikel, Journale, Buchungsperioden, Zahlungsbedingungen
  - ÖSHZ : Integrationsphasen, Berufe, AG-Sperrgründe, Dienste, Begleitungsbeendigungsgründe, Dispenzgründe, Klientenkontaktarten, Hilfearten, Kategorien
  - Lebenslauf : Sprachen, Bildungsarten, Akademische Grade, Sektoren, Funktionen, Arbeitsregimes, Statuus, Vertragsdauern
  - DSBE : VSE-Arten, Vertragsbeendigungsgründe, Auswertungsstrategien, Art.60§7-Konventionsarten, Stellenarten, Stundenpläne, Art.61-Konventionsarten
  - Kurse : Kursinhalte
  - Erstempfang : Vermittler, Fachbereiche
  - ZDSS : Sektoren, Eigenschafts-Codes
  - Schuldnerberatung : Kontengruppen, Konten, Budget-Kopiervorlage
- Explorer :
  - System : Datenbankmodelle, Vollmachten, Benutzerprofile, Notifications, Änderungen, Datentests, Datenprobleme
  - Eigenschaften : Eigenschaften
  - Kontakte : Kontaktpersonen, Adressenarten, Adressen, Gremienmitglieder, Haushaltsmitgliedsrollen, Mitglieder, Verwandtschaftsbeziehungen, Verwandschaftsarten
  - Büro : Uploads, Upload-Bereiche, E-Mail-Ausgänge, Anhänge, Auszüge, Ereignisse/Notizen, Einfügetexte
  - Kalender : Aufgaben, Teilnehmer, Abonnements, Termin-Zustände, Gast-Zustände, Aufgaben-Zustände
  - ÖSHZ : Begleitungen, Klientenkontakte, AG-Sperren, Vorstrafen, Klienten, Zivilstände, Bearbeitungszustände Klienten, eID-Kartenarten, Hilfebeschlüsse, Einkommensbescheinigungen, Kostenübernahmescheine, Einfache Bescheinigungen, Phonetische Wörter
  - Buchhaltung : Befriedigungsregeln, Belege, Belegarten, Bewegungen, Geschäftsjahre, Handelsarten, Journalgruppen, Rechnungen
  - SEPA : Bankkonten, Importierte  Bankkonten, Kontoauszüge, Transaktionen
  - Finanzjournale : Kontoauszüge, Diverse Buchungen, Zahlungsaufträge
  - Lebenslauf : Sprachkenntnisse, Ausbildungen, Studien, Berufserfahrungen
  - DSBE : VSEs, Art.60§7-Konventionen, Stellenanfragen, Vertragspartner, Art.61-Konventionen, FSE Summaries
  - Kurse : Kurse, Kursanfragen
  - Erstempfang : Kompetenzen
  - ZDSS : IdentifyPerson-Anfragen, ManageAccess-Anfragen, Tx25-Anfragen
  - Schuldnerberatung : Budgets, Einträge
- Site : Info
<BLANKLINE>

.. _hubert:

Hubert
------

Hubert is an Integration agent.

>>> with translation.override('de'):
...     rt.login('hubert').show_menu()
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF -SKIP
- Kontakte : Personen,  ▶ Klienten, Organisationen, -, Partner (alle), Haushalte
- Büro : Ablaufende Uploads, Meine Uploads, Mein E-Mail-Ausgang, Meine Auszüge, Meine Ereignisse/Notizen, Meine Datenkontrollliste
- Kalender : Kalender, Meine Termine, Meine Aufgaben, Meine Gäste, Meine Anwesenheiten
- Empfang : Klienten, Termine heute, Wartende Besucher, Beschäftigte Besucher, Gegangene Besucher, Meine Warteschlange
- ÖSHZ : Klienten, Meine Begleitungen, Zu bestätigende Hilfebeschlüsse
- DSBE : Klienten, VSEs, Art.60§7-Konventionen, Stellenanbieter, Stellen, Stellenangebote, Art.61-Konventionen
- Kurse : Kursanbieter, Kursangebote, Offene Kursanfragen
- Berichte :
  - DSBE : Benutzer und ihre Klienten, Übersicht Art.60§7-Konventionen, Tätigkeitsbericht
- Konfigurierung :
  - Orte : Länder
  - Büro : Meine Einfügetexte
  - Lebenslauf : Sprachen
- Explorer :
  - SEPA : Importierte  Bankkonten, Kontoauszüge, Transaktionen
  - DSBE : VSEs, Art.60§7-Konventionen, Art.61-Konventionen
- Site : Info


.. _melanie:

Mélanie
-------

Mélanie is a manager of the Integration service.

>>> p = rt.login('melanie').get_user().profile
>>> print(p)
Begleiter im DSBE (Manager)
>>> p.role.__class__
<class 'lino_welfare.modlib.integ.roles.IntegrationStaff'>

Because Mélanie has her :attr:`language
<lino.modlib.users.models.User.language>` field set to French, we need
to explicitly override the language of :meth:`show_menu
<lino.core.requests.BaseRequest.show_menu>` to get her menu in German:

>>> rt.login('melanie').show_menu(language="de")
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF -SKIP
- Kontakte : Personen,  ▶ Klienten, Organisationen, -, Partner (alle), Haushalte
- Büro : Ablaufende Uploads, Meine Uploads, Mein E-Mail-Ausgang, Meine Auszüge, Meine Ereignisse/Notizen, Meine Datenkontrollliste
- Kalender : Kalender, Meine Termine, Meine Aufgaben, Meine Gäste, Meine Anwesenheiten
- Empfang : Klienten, Termine heute, Wartende Besucher, Beschäftigte Besucher, Gegangene Besucher, Meine Warteschlange
- ÖSHZ : Klienten, Meine Begleitungen, Zu bestätigende Hilfebeschlüsse
- DSBE : Klienten, VSEs, Art.60§7-Konventionen, Stellenanbieter, Stellen, Stellenangebote, Art.61-Konventionen
- Kurse : Kursanbieter, Kursangebote, Offene Kursanfragen
- Berichte :
  - DSBE : Benutzer und ihre Klienten, Übersicht Art.60§7-Konventionen, Tätigkeitsbericht
- Konfigurierung :
  - Orte : Länder, Orte
  - Kontakte : Organisationsarten, Funktionen, Haushaltsarten
  - Büro : Upload-Arten, Notizarten, Ereignisarten, Meine Einfügetexte
  - Kalender : Kalenderliste, Räume, Prioritäten, Periodische Terminregeln, Kalendereintragsarten, Externe Kalender
  - ÖSHZ : Integrationsphasen, Berufe, AG-Sperrgründe, Dienste, Begleitungsbeendigungsgründe, Dispenzgründe, Klientenkontaktarten, Hilfearten, Kategorien
  - Lebenslauf : Sprachen, Bildungsarten, Akademische Grade, Sektoren, Funktionen, Arbeitsregimes, Statuus, Vertragsdauern
  - DSBE : VSE-Arten, Vertragsbeendigungsgründe, Auswertungsstrategien, Art.60§7-Konventionsarten, Stellenarten, Stundenpläne, Art.61-Konventionsarten
  - Kurse : Kursinhalte
  - Erstempfang : Vermittler, Fachbereiche
- Explorer :
  - Kontakte : Kontaktpersonen, Adressenarten, Haushaltsmitgliedsrollen, Mitglieder, Verwandtschaftsbeziehungen, Verwandschaftsarten
  - Büro : Uploads, Upload-Bereiche, E-Mail-Ausgänge, Anhänge, Ereignisse/Notizen
  - Kalender : Aufgaben, Abonnements
  - ÖSHZ : Begleitungen, Klientenkontakte, AG-Sperren, Vorstrafen, Klienten, Zivilstände, Bearbeitungszustände Klienten, Hilfebeschlüsse, Einkommensbescheinigungen, Kostenübernahmescheine, Einfache Bescheinigungen
  - SEPA : Bankkonten, Importierte  Bankkonten, Kontoauszüge, Transaktionen
  - Lebenslauf : Sprachkenntnisse, Ausbildungen, Studien, Berufserfahrungen
  - DSBE : VSEs, Art.60§7-Konventionen, Stellenanfragen, Vertragspartner, Art.61-Konventionen
  - Kurse : Kurse, Kursanfragen
  - Erstempfang : Kompetenzen
- Site : Info


Kerstin
-------

Kerstin is a debts consultant.

>>> p = rt.login('kerstin').get_user().profile
>>> print(p)
Schuldenberater
>>> p.role.__class__
<class 'lino_welfare.modlib.debts.roles.DebtsUser'>

>>> with translation.override('de'):
...     rt.login('kerstin').show_menu()
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF -SKIP
- Kontakte : Personen,  ▶ Klienten, Organisationen, -, Partner (alle), Haushalte
- Büro : Ablaufende Uploads, Meine Uploads, Mein E-Mail-Ausgang, Meine Auszüge, Meine Ereignisse/Notizen, Meine Datenkontrollliste
- Kalender : Kalender, Meine Termine, Meine Aufgaben, Meine Gäste, Meine Anwesenheiten
- Empfang : Klienten, Termine heute, Wartende Besucher, Beschäftigte Besucher, Gegangene Besucher, Meine Warteschlange
- ÖSHZ : Klienten, Meine Begleitungen, Zu bestätigende Hilfebeschlüsse
- Erstempfang : Neue Klienten, Verfügbare Begleiter
- Schuldnerberatung : Klienten, Meine Budgets
- Konfigurierung :
  - Orte : Länder
  - Büro : Meine Einfügetexte
  - Lebenslauf : Sprachen
  - Schuldnerberatung : Budget-Kopiervorlage
- Explorer :
  - SEPA : Importierte  Bankkonten, Kontoauszüge, Transaktionen
- Site : Info



Caroline
--------

Caroline is a newcomers consultant.

>>> p = rt.login('caroline').get_user().profile
>>> print(p)
Berater Erstempfang
>>> p.role.__class__
<class 'lino_welfare.modlib.newcomers.roles.NewcomersAgent'>

>>> with translation.override('de'):
...     rt.login('caroline').show_menu()
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
- Kontakte : Personen,  ▶ Klienten, Organisationen, -, Partner (alle), Haushalte
- Büro : Ablaufende Uploads, Meine Uploads, Mein E-Mail-Ausgang, Meine Auszüge, Meine Ereignisse/Notizen, Meine Datenkontrollliste
- Kalender : Kalender, Meine Termine, Meine Aufgaben, Meine Gäste, Meine Anwesenheiten
- Empfang : Klienten, Termine heute, Wartende Besucher, Beschäftigte Besucher, Gegangene Besucher, Meine Warteschlange
- ÖSHZ : Klienten, Meine Begleitungen, Zu bestätigende Hilfebeschlüsse
- Erstempfang : Neue Klienten, Verfügbare Begleiter
- Konfigurierung :
  - Orte : Länder
  - Büro : Meine Einfügetexte
  - Lebenslauf : Sprachen
- Explorer :
  - SEPA : Importierte  Bankkonten, Kontoauszüge, Transaktionen
- Site : Info


.. _theresia:

Theresia
--------

Theresia is a reception clerk.

>>> p = rt.login('theresia').get_user().profile
>>> print(p)
Empfangsschalter
>>> p.role.__class__
<class 'lino_welfare.modlib.welfare.roles.ReceptionClerk'>


>>> rt.login('theresia').show_menu(language="de")
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF -SKIP
- Kontakte : Personen,  ▶ Klienten, Organisationen, -, Partner (alle), Haushalte
- Büro : Ablaufende Uploads, Meine Uploads, Meine Auszüge, Meine Ereignisse/Notizen
- Empfang : Klienten, Termine heute, Wartende Besucher, Beschäftigte Besucher, Gegangene Besucher
- Konfigurierung :
  - Orte : Länder, Orte
  - Kontakte : Organisationsarten, Funktionen, Haushaltsarten
  - ÖSHZ : Hilfearten, Kategorien
- Explorer :
  - Kontakte : Kontaktpersonen, Haushaltsmitgliedsrollen, Mitglieder, Verwandtschaftsbeziehungen, Verwandschaftsarten
  - ÖSHZ : Hilfebeschlüsse, Einkommensbescheinigungen, Kostenübernahmescheine, Einfache Bescheinigungen
  - SEPA : Importierte  Bankkonten, Kontoauszüge, Transaktionen
- Site : Info



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
- accounts.Accounts.detail : ref, group, type, id, name, name_fr, name_en, needs_partner, clearable, MovementsByAccount
- accounts.Accounts.insert : ref, group, type, name, name_fr, name_en
- accounts.Groups.detail : ref, name, name_fr, name_en, account_type, id
- accounts.Groups.insert : name, name_fr, name_en, account_type, ref
- addresses.Addresses.detail : country, city, zip_code, addr1, street, street_no, street_box, addr2, address_type, remark, data_source, partner
- addresses.Addresses.insert : country, city, street, street_no, street_box, address_type, remark
- aids.AidTypes.detail : id, short_name, confirmation_type, name, name_fr, name_en, excerpt_title, excerpt_title_fr, excerpt_title_en, body_template, print_directly, is_integ_duty, is_urgent, confirmed_by_primary_coach, board, company, contact_person, contact_role, pharmacy_type
- aids.AidTypes.insert : name, name_fr, name_en, confirmation_type
- aids.Categories.insert : id, name, name_fr, name_en
- aids.Grantings.detail : id, client, user, signer, workflow_buttons, request_date, board, decision_date, aid_type, category, start_date, end_date, custom_actions
- aids.Grantings.insert : client, aid_type, signer, board, decision_date, start_date, end_date
- aids.GrantingsByClient.insert : aid_type, board, decision_date, start_date, end_date
- aids.IncomeConfirmations.insert : client, user, signer, workflow_buttons, printed, company, contact_person, language, granting, start_date, end_date, category, amount, id, remark
- aids.IncomeConfirmationsByGranting.insert : client, granting, start_date, end_date, category, amount, company, contact_person, language, remark
- aids.RefundConfirmations.insert : id, client, user, signer, workflow_buttons, granting, start_date, end_date, doctor_type, doctor, pharmacy, company, contact_person, language, printed, remark
- aids.RefundConfirmationsByGranting.insert : start_date, end_date, doctor_type, doctor, pharmacy, company, contact_person, language, printed, remark
- aids.SimpleConfirmations.insert : id, client, user, signer, workflow_buttons, granting, start_date, end_date, company, contact_person, language, printed, remark
- aids.SimpleConfirmationsByGranting.insert : start_date, end_date, company, contact_person, language, remark
- art61.ContractTypes.insert : id, name, name_fr, name_en, ref
- art61.Contracts.detail : id, client, user, language, type, company, contact_person, contact_role, applies_from, duration, applies_until, exam_policy, job_title, status, cv_duration, regime, reference_person, printed, date_decided, date_issued, date_ended, ending, subsidize_10, subsidize_20, subsidize_30, subsidize_40, subsidize_50, responsibilities
- art61.Contracts.insert : client, company, type
- b2c.Accounts.detail : iban, bic, last_transaction, owner_name, account_name, partners
- b2c.Statements.detail : account, account__owner_name, account__account_name, statement_number, local_currency, balance_start, start_date, balance_end, end_date
- b2c.Transactions.detail : statement, seqno, booking_date, value_date, amount, remote_account, remote_bic, eref, txcd_text, remote_owner, remote_owner_address, remote_owner_city, remote_owner_postalcode, remote_owner_country_code, message
- boards.Boards.detail : id, name, name_fr, name_en
- boards.Boards.insert : name, name_fr, name_en
- cal.Calendars.detail : name, name_fr, name_en, color, id, description
- cal.Calendars.insert : name, name_fr, name_en, color
- cal.EventTypes.detail : name, name_fr, name_en, event_label, event_label_fr, event_label_en, max_conflicting, all_rooms, locks_user, id, invite_client, is_appointment, email_template, attach_to_email
- cal.EventTypes.insert : name, name_fr, name_en, invite_client
- cal.Events.detail : event_type, summary, project, start_date, start_time, end_date, end_time, user, assigned_to, room, priority, access_class, transparent, owner, workflow_buttons, description, id, created, modified, state
- cal.Events.insert : summary, start_date, start_time, end_date, end_time, event_type, project
- cal.EventsByClient.insert : event_type, summary, start_date, start_time, end_date, end_time
- cal.GuestRoles.insert : id, name, name_fr, name_en
- cal.GuestStates.wf1 : notify_subject, notify_body, notify_silent
- cal.GuestStates.wf2 : notify_subject, notify_body, notify_silent
- cal.Guests.checkin : notify_subject, notify_body, notify_silent
- cal.Guests.detail : event, partner, role, state, remark, workflow_buttons, waiting_since, busy_since, gone_since
- cal.Guests.insert : event, partner, role
- cal.RecurrentEvents.detail : name, name_fr, name_en, id, user, event_type, start_date, start_time, end_date, end_time, every_unit, every, max_events, monday, tuesday, wednesday, thursday, friday, saturday, sunday, description
- cal.RecurrentEvents.insert : name, name_fr, name_en, start_date, end_date, every_unit, event_type
- cal.Rooms.insert : id, name, name_fr, name_en
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
- contacts.Companies.detail : overview, prefix, name, type, vat_id, client_contact_type, url, email, phone, gsm, fax, remarks, payment_term, VouchersByPartner, MovementsByPartner, id, language, activity, is_obsolete, created, modified
- contacts.Companies.insert : name, language, email, type, id
- contacts.Companies.merge_row : merge_to, reason
- contacts.Partners.detail : overview, id, language, activity, client_contact_type, url, email, phone, gsm, fax, country, region, city, zip_code, addr1, street_prefix, street, street_no, street_box, addr2, remarks, payment_term, VouchersByPartner, MovementsByPartner, is_obsolete, created, modified
- contacts.Partners.insert : name, language, email
- contacts.Persons.create_household : partner, type, head
- contacts.Persons.detail : overview, title, first_name, middle_name, last_name, gender, birth_date, age, id, language, email, phone, gsm, fax, MembersByPerson, LinksByHuman, remarks, payment_term, VouchersByPartner, MovementsByPartner, activity, url, client_contact_type, is_obsolete, created, modified
- contacts.Persons.insert : first_name, last_name, gender, language
- countries.Countries.detail : isocode, name, name_fr, name_en, short_code, inscode, actual_country
- countries.Countries.insert : isocode, inscode, name, name_fr, name_en
- countries.Places.insert : name, name_fr, name_en, country, type, parent, zip_code, id
- countries.Places.merge_row : merge_to, reason
- courses.CourseContents.insert : id, name
- courses.CourseOffers.detail : id, title, content, provider, guest_role, description
- courses.CourseOffers.insert : provider, content, title
- courses.CourseProviders.detail : overview, prefix, name, type, vat_id, client_contact_type, url, email, phone, gsm, fax
- courses.CourseRequests.insert : date_submitted, person, content, offer, urgent, course, state, date_ended, id, remark, UploadsByController
- courses.Courses.detail : id, start_date, offer, title, remark
- courses.Courses.insert : start_date, offer, title
- cv.Durations.insert : id, name, name_fr, name_en
- cv.EducationLevels.insert : name, name_fr, name_en, is_study, is_training
- cv.Experiences.insert : person, start_date, end_date, termination_reason, company, country, city, sector, function, title, status, duration, regime, is_training, remarks
- cv.Functions.insert : id, name, name_fr, name_en, sector, remark
- cv.Regimes.insert : id, name, name_fr, name_en
- cv.Sectors.insert : id, name, name_fr, name_en, remark
- cv.Statuses.insert : id, name, name_fr, name_en
- cv.Studies.insert : person, start_date, end_date, type, content, education_level, state, school, country, city, remarks
- cv.StudyTypes.detail : name, name_fr, name_en, id, education_level, is_study, is_training
- cv.StudyTypes.insert : name, name_fr, name_en, is_study, is_training, education_level
- cv.Trainings.detail : person, start_date, end_date, type, state, certificates, sector, function, school, country, city, remarks
- cv.Trainings.insert : person, start_date, end_date, type, state, certificates, sector, function, school, country, city
- debts.Accounts.detail : ref, name, name_fr, name_en, group, type, required_for_household, required_for_person, periods, default_amount
- debts.Accounts.insert : ref, group, type, name, name_fr, name_en
- debts.Budgets.detail : date, partner, id, user, intro, ResultByBudget, DebtsByBudget, AssetsByBudgetSummary, conclusion, dist_amount, printed, total_debt, include_yearly_incomes, print_empty_rows, print_todos, DistByBudget, data_box, summary_box
- debts.Budgets.insert : partner, date, user
- debts.Groups.detail : ref, name, name_fr, name_en, id, account_type, entries_layout
- debts.Groups.insert : name, name_fr, name_en, account_type, ref
- excerpts.ExcerptTypes.detail : id, name, name_fr, name_en, content_type, build_method, template, body_template, email_template, shortcut, primary, print_directly, certifying, print_recipient, backward_compat, attach_to_email
- excerpts.ExcerptTypes.insert : name, name_fr, name_en, content_type, primary, certifying, build_method, template, body_template
- excerpts.Excerpts.detail : id, excerpt_type, project, user, build_method, company, contact_person, language, owner, build_time, body_template_content
- finan.BankStatements.detail : voucher_date, balance1, balance2, user, workflow_buttons, journal, accounting_period, number, id, MovementsByVoucher
- finan.BankStatements.insert : voucher_date, balance1, balance2
- finan.DisbursementOrders.detail : journal, number, voucher_date, entry_date, accounting_period, item_account, total, workflow_buttons, narration, item_remark, state, user, id, MovementsByVoucher
- finan.DisbursementOrdersByJournal.insert : item_account, voucher_date
- finan.FinancialVouchers.detail : voucher_date, user, narration, workflow_buttons, journal, accounting_period, number, id, MovementsByVoucher
- finan.FinancialVouchers.insert : voucher_date, narration
- finan.PaymentOrders.detail : voucher_date, user, narration, total, execution_date, workflow_buttons, journal, accounting_period, number, id, MovementsByVoucher
- fse.Summaries.detail : master, year, month, children_at_charge, certified_handicap, other_difficulty, id, education_level, result, remark, results
- fse.Summaries.insert : master, education_level, result, remark
- fse.SummariesByClient.insert : education_level, result, remark
- gfks.ContentTypes.insert : id, app_label, model, base_classes
- households.Households.detail : type, prefix, name, id
- households.HouseholdsByType.detail : type, name, language, id, country, region, city, zip_code, street_prefix, street, street_no, street_box, addr2, phone, gsm, email, url, remarks
- households.Types.insert : name, name_fr, name_en
- humanlinks.Links.insert : parent, child, type
- integ.ActivityReport.show : body
- isip.ContractEndings.insert : name, use_in_isip, use_in_jobs, is_success, needs_date_ended
- isip.ContractPartners.insert : company, contact_person, contact_role, duties_company
- isip.ContractTypes.insert : id, ref, exam_policy, needs_study_type, name, name_fr, name_en, full_name
- isip.Contracts.detail : id, client, type, user, user_asd, study_type, applies_from, applies_until, exam_policy, language, date_decided, date_issued, printed, date_ended, ending, stages, goals, duties_asd, duties_dsbe, duties_person
- isip.Contracts.insert : client, type
- isip.ExamPolicies.insert : id, name, name_fr, name_en, max_events, every, every_unit, event_type, monday, tuesday, wednesday, thursday, friday, saturday, sunday
- jobs.ContractTypes.insert : id, name, name_fr, name_en, ref
- jobs.Contracts.detail : id, client, user, user_asd, language, job, type, company, contact_person, contact_role, applies_from, duration, applies_until, exam_policy, regime, schedule, hourly_rate, refund_rate, reference_person, remark, printed, date_decided, date_issued, date_ended, ending, responsibilities
- jobs.Contracts.insert : client, job
- jobs.JobProviders.detail : overview, prefix, name, type, vat_id, client_contact_type, url, email, phone, gsm, fax
- jobs.JobTypes.insert : id, name, is_social
- jobs.Jobs.insert : name, provider, contract_type, type, id, sector, function, capacity, hourly_rate, remark
- jobs.JobsOverview.show : body
- jobs.Offers.insert : name, provider, sector, function, selection_from, selection_until, start_date, remark
- jobs.Schedules.insert : id, name, name_fr, name_en
- languages.Languages.insert : id, iso2, name, name_fr, name_en
- ledger.ActivityReport.show : body
- ledger.Journals.detail : name, name_fr, name_en, ref, trade_type, seqno, id, voucher_type, journal_group, account, build_method, template, dc, force_sequence, yearly_numbering, auto_check_clearings, printed_name, printed_name_fr, printed_name_en
- ledger.Journals.insert : ref, name, name_fr, name_en, journal_group, voucher_type
- ledger.Situation.show : body
- newcomers.AvailableCoachesByClient.assign_coach : notify_subject, notify_body, notify_silent
- newcomers.Faculties.detail : id, name, name_fr, name_en, weight
- newcomers.Faculties.insert : name, name_fr, name_en, weight
- notes.EventTypes.insert : id, name, name_fr, name_en, remark
- notes.NoteTypes.detail : id, name, name_fr, name_en, build_method, template, special_type, email_template, attach_to_email, remark
- notes.NoteTypes.insert : name, name_fr, name_en, build_method
- notes.Notes.detail : date, time, event_type, type, project, subject, important, company, contact_person, user, language, build_time, id, body, UploadsByController
- notes.Notes.insert : event_type, type, subject, project
- notifier.Notifications.insert : overview
- outbox.Mails.detail : subject, project, date, user, sent, id, owner, AttachmentsByMail, UploadsByController, body
- outbox.Mails.insert : project, subject, body
- pcsw.ClientContactTypes.insert : id, name, name_fr, name_en, can_refund, is_bailiff
- pcsw.ClientStates.wf1 : reason, remark
- pcsw.Clients.create_visit : user, summary
- pcsw.Clients.detail : overview, gender, id, tim_id, first_name, middle_name, last_name, birth_date, age, national_id, nationality, declared_name, civil_state, birth_country, birth_place, language, email, phone, fax, gsm, image, AgentsByClient, SimilarClients, LinksByHuman, cbss_relations, MembersByPerson, workflow_buttons, id_document, broker, faculty, refusal_reason, in_belgium_since, residence_type, gesdos_id, job_agents, group, aid_type, income_ag, income_wg, income_kg, income_rente, income_misc, seeking_since, unemployed_since, work_permit_suspended_until, needs_residence_permit, needs_work_permit, UploadsByClient, cvs_emitted, skills, obstacles, ExcerptsByProject, MovementsByProject, activity, client_state, noble_condition, unavailable_until, unavailable_why, is_cpas, is_senior, is_obsolete, created, modified, remarks, remarks2, cbss_identify_person, cbss_manage_access, cbss_retrieve_ti_groups, cbss_summary
- pcsw.Clients.insert : first_name, last_name, national_id, gender, language
- pcsw.Clients.merge_row : merge_to, aids_IncomeConfirmation, aids_RefundConfirmation, aids_SimpleConfirmation, cv_LanguageKnowledge, dupable_clients_Word, pcsw_Coaching, pcsw_Dispense, properties_PersonProperty, reason
- pcsw.CoachingEndings.insert : id, name, name_fr, name_en, seqno
- pcsw.Coachings.create_visit : user, summary
- plausibility.Checkers.detail : value, name, text
- plausibility.Problems.detail : user, owner, checker, id, message
- properties.PropGroups.insert : id, name, name_fr, name_en
- properties.PropTypes.insert : id, name, name_fr, name_en, choicelist, default_value
- properties.Properties.insert : id, group, type, name, name_fr, name_en
- reception.BusyVisitors.detail : event, client, role, state, remark, workflow_buttons
- reception.GoneVisitors.detail : event, client, role, state, remark, workflow_buttons
- reception.MyWaitingVisitors.detail : event, client, role, state, remark, workflow_buttons
- reception.WaitingVisitors.detail : event, client, role, state, remark, workflow_buttons
- system.SiteConfigs.detail : site_company, next_partner_id, job_office, master_budget, signer1, signer2, signer1_function, signer2_function, system_note_type, default_build_method, propgroup_skills, propgroup_softskills, propgroup_obstacles, residence_permit_upload_type, work_permit_upload_type, driving_licence_upload_type, default_event_type, prompt_calendar, client_guestrole, team_guestrole, cbss_org_unit, sector, ssdn_user_id, ssdn_email, cbss_http_username, cbss_http_password
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
- users.Users.change_password : current, new1, new2
- users.Users.detail : username, profile, partner, first_name, last_name, initials, email, language, timezone, id, created, modified, remarks, event_type, access_class, calendar, newcomer_quota, coaching_type, coaching_supervisor, newcomer_consultations, newcomer_appointments
- users.Users.insert : username, email, first_name, last_name, partner, language, profile
- vatless.Invoices.detail : journal, number, voucher_date, entry_date, accounting_period, workflow_buttons, partner, payment_term, due_date, bank_account, your_ref, narration, amount, match, state, user, id, MovementsByVoucher
- vatless.Invoices.insert : journal, partner, voucher_date
- vatless.InvoicesByJournal.insert : partner, voucher_date
- vatless.ProjectInvoicesByJournal.detail : journal, number, voucher_date, entry_date, accounting_period, workflow_buttons, project, narration, partner, your_ref, payment_term, due_date, bank_account, amount, match, state, user, id, MovementsByVoucher
- vatless.ProjectInvoicesByJournal.insert : project, partner, voucher_date
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
- b2c.Accounts.detail : visible for 100 110 120 200 210 220 300 400 410 500 510 800 admin
- b2c.Statements.detail : visible for 100 110 120 200 210 220 300 400 410 500 510 800 admin
- b2c.Transactions.detail : visible for 100 110 120 200 210 220 300 400 410 500 510 800 admin
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
- courses.CourseContents.insert : visible for 110 admin
- courses.CourseOffers.detail : visible for 100 110 120 admin
- courses.CourseOffers.insert : visible for 100 110 120 admin
- courses.CourseProviders.detail : visible for 100 110 120 admin
- courses.CourseRequests.insert : visible for 110 admin
- courses.Courses.detail : visible for 110 admin
- courses.Courses.insert : visible for 110 admin
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
- debts.Accounts.detail : visible for admin
- debts.Accounts.insert : visible for admin
- debts.Budgets.detail : visible for admin
- debts.Budgets.insert : visible for admin
- debts.Groups.detail : visible for admin
- debts.Groups.insert : visible for admin
- excerpts.ExcerptTypes.detail : visible for admin
- excerpts.ExcerptTypes.insert : visible for admin
- excerpts.Excerpts.detail : visible for 100 110 120 200 210 220 300 400 410 500 510 800 admin
- finan.BankStatements.detail : visible for 500 510 admin
- finan.BankStatements.insert : visible for 500 510 admin
- finan.DisbursementOrders.detail : visible for 500 510 admin
- finan.DisbursementOrdersByJournal.insert : visible for 500 510 admin
- finan.FinancialVouchers.detail : visible for 500 510 admin
- finan.FinancialVouchers.insert : visible for 500 510 admin
- finan.PaymentOrders.detail : visible for 500 510 admin
- fse.Summaries.detail : visible for 100 110 120 200 210 220 300 400 410 500 510 800 admin
- fse.Summaries.insert : visible for 100 110 120 200 210 220 300 400 410 500 510 800 admin
- fse.SummariesByClient.insert : visible for 100 110 120 200 210 220 300 400 410 500 510 800 admin
- gfks.ContentTypes.insert : visible for admin
- households.Households.detail : visible for 100 110 120 200 210 220 300 400 410 500 510 800 admin
- households.HouseholdsByType.detail : visible for 100 110 120 200 210 220 300 400 410 500 510 800 admin
- households.Types.insert : visible for 110 210 220 410 800 admin
- humanlinks.Links.insert : visible for 110 210 220 410 800 admin
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
- ledger.ActivityReport.show : visible for 500 510 admin
- ledger.Journals.detail : visible for 510 admin
- ledger.Journals.insert : visible for 510 admin
- ledger.Situation.show : visible for 500 510 admin
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
- properties.PropGroups.insert : visible for admin
- properties.PropTypes.insert : visible for admin
- properties.Properties.insert : visible for admin
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
- vatless.Invoices.detail : visible for 500 510 admin
- vatless.Invoices.insert : visible for 500 510 admin
- vatless.InvoicesByJournal.insert : visible for 500 510 admin
- vatless.ProjectInvoicesByJournal.detail : visible for 500 510 admin
- vatless.ProjectInvoicesByJournal.insert : visible for 500 510 admin
<BLANKLINE>


Visibility of eID reader actions
================================

Here is a list of the eid card reader actions and their availability
per user profile.

>>> from lino_xl.lib.beid.mixins import BaseBeIdReadCardAction
>>> print(analyzer.show_action_permissions(BaseBeIdReadCardAction))
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
- debts.Clients.find_by_beid : visible for 300 admin
- debts.Clients.read_beid : visible for 300 admin
- integ.Clients.find_by_beid : visible for 100 110 120 admin
- integ.Clients.read_beid : visible for 100 110 120 admin
- newcomers.ClientsByFaculty.find_by_beid : visible for 100 110 120 200 210 220 300 400 410 800 admin
- newcomers.ClientsByFaculty.read_beid : visible for 100 110 120 200 210 220 300 400 410 800 admin
- newcomers.NewClients.find_by_beid : visible for 200 300 admin
- newcomers.NewClients.read_beid : visible for 200 300 admin
- pcsw.AllClients.find_by_beid : visible for 110 410 admin
- pcsw.AllClients.read_beid : visible for 110 410 admin
- pcsw.Clients.find_by_beid : visible for 100 110 120 200 210 220 300 400 410 800 admin
- pcsw.Clients.read_beid : visible for 100 110 120 200 210 220 300 400 410 800 admin
- pcsw.ClientsByNationality.find_by_beid : visible for 100 110 120 200 210 220 300 400 410 800 admin
- pcsw.ClientsByNationality.read_beid : visible for 100 110 120 200 210 220 300 400 410 800 admin
- pcsw.CoachedClients.find_by_beid : visible for 100 110 120 200 300 400 410 admin
- pcsw.CoachedClients.read_beid : visible for 100 110 120 200 300 400 410 admin
- reception.Clients.find_by_beid : visible for 100 110 120 200 210 220 300 400 410 800 admin
- reception.Clients.read_beid : visible for 100 110 120 200 210 220 300 400 410 800 admin
<BLANKLINE>



Some requests
=============

Some choices lists:

>>> kw = dict()
>>> fields = 'count rows'
>>> demo_get('rolf', 'choices/cv/SkillsByPerson/property', fields, 6, **kw)
>>> demo_get('rolf', 'choices/cv/ObstaclesByPerson/property', fields, 15, **kw)


