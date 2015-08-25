.. _welfare.tested.eupen:
.. _welfare.specs.eupen:

=======================
Lino Welfare à la Eupen
=======================

.. How to test only this document:

    $ python setup.py test -s tests.SpecsTests.test_eupen

    >>> from __future__ import print_function
    >>> import os
    >>> os.environ['DJANGO_SETTINGS_MODULE'] = \
    ...    'lino_welfare.projects.eupen.settings.doctests'
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
Warning: Kann Klient EVERS Eberhart (127) nicht l\xf6schen weil 4 Hilfebeschl\xfcsse darauf verweisen.


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
- DSBE : Klienten, VSEs, Art.60§7-Konventionen, Stellenanbieter, Stellen, Stellenangebote, Art.61-Konventionen
- Kurse : Kursanbieter, Kursangebote, Offene Kursanfragen
- Erstempfang : Neue Klienten, Verfügbare Begleiter
- Schuldnerberatung : Klienten, Meine Budgets
- Berichte :
  - System : Broken GFKs
  - DSBE : Benutzer und ihre Klienten, Übersicht Art.60§7-Konventionen, Tätigkeitsbericht
- Konfigurierung :
  - System : Site-Parameter, Hilfetexte, Benutzer
  - Orte : Länder, Orte
  - Eigenschaften : Eigenschaftsgruppen, Eigenschafts-Datentypen, Fachkompetenzen, Sozialkompetenzen, Hindernisse
  - Kontakte : Organisationsarten, Funktionen, Gremien, Haushaltsarten
  - Büro : Upload-Arten, Auszugsarten, Notizarten, Ereignisarten, Meine Einfügetexte
  - Kalender : Kalenderliste, Räume, Prioritäten, Periodische Termine, Gastrollen, Kalendereintragsarten, Externe Kalender
  - Buchhaltung : Kontenpläne, Kontengruppen, Konten
  - ÖSHZ : Integrationsphasen, Berufe, AG-Sperrgründe, Dienste, Begleitungsbeendigungsgründe, Dispenzgründe, Klientenkontaktarten, Hilfearten, Kategorien
  - Lebenslauf : Sprachen, Bildungsarten, Akademische Grade, Sektoren, Funktionen, Arbeitsregimes, Statuus, Vertragsdauern
  - DSBE : VSE-Arten, Vertragsbeendigungsgründe, Auswertungsstrategien, Art.60§7-Konventionsarten, Stellenarten, Stundenpläne, Art.61-Konventionsarten
  - Kurse : Kursinhalte
  - Erstempfang : Vermittler, Fachbereiche
  - ZDSS : Sektoren, Eigenschafts-Codes
  - Schuldnerberatung : Budget-Kopiervorlage
- Explorer :
  - System : Datenbankmodelle, Vollmachten, Benutzerprofile, Änderungen, Datentests, Datenprobleme
  - Eigenschaften : Eigenschaften
  - Kontakte : Kontaktpersonen, Adressenarten, Adressen, Gremienmitglieder, Haushaltsmitgliedsrollen, Mitglieder, Verwandtschaftsbeziehungen, Verwandschaftsarten
  - Büro : Uploads, Upload-Bereiche, E-Mail-Ausgänge, Anhänge, Auszüge, Ereignisse/Notizen, Einfügetexte
  - Kalender : Aufgaben, Teilnehmer, Abonnements, Termin-Zustände, Gast-Zustände, Aufgaben-Zustände
  - SEPA : Konten
  - ÖSHZ : Begleitungen, Klientenkontakte, AG-Sperren, Vorstrafen, Klienten, Zivilstände, Bearbeitungszustände Klienten, eID-Kartenarten, Hilfebeschlüsse, Einkommensbescheinigungen, Kostenübernahmescheine, Einfache Bescheinigungen, Phonetische Wörter
  - Lebenslauf : Sprachkenntnisse, Ausbildungen, Studien, Berufserfahrungen
  - DSBE : VSEs, Art.60§7-Konventionen, Stellenanfragen, Vertragspartner, Art.61-Konventionen
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
  - Kalender : Kalenderliste, Räume, Prioritäten, Periodische Termine, Kalendereintragsarten, Externe Kalender
  - ÖSHZ : Integrationsphasen, Berufe, AG-Sperrgründe, Dienste, Begleitungsbeendigungsgründe, Dispenzgründe, Klientenkontaktarten, Hilfearten, Kategorien
  - Lebenslauf : Sprachen, Bildungsarten, Akademische Grade, Sektoren, Funktionen, Arbeitsregimes, Statuus, Vertragsdauern
  - DSBE : VSE-Arten, Vertragsbeendigungsgründe, Auswertungsstrategien, Art.60§7-Konventionsarten, Stellenarten, Stundenpläne, Art.61-Konventionsarten
  - Kurse : Kursinhalte
  - Erstempfang : Vermittler, Fachbereiche
- Explorer :
  - Kontakte : Kontaktpersonen, Adressenarten, Haushaltsmitgliedsrollen, Mitglieder, Verwandtschaftsbeziehungen, Verwandschaftsarten
  - Büro : Uploads, Upload-Bereiche, E-Mail-Ausgänge, Anhänge, Ereignisse/Notizen
  - Kalender : Aufgaben, Abonnements
  - SEPA : Konten
  - ÖSHZ : Begleitungen, Klientenkontakte, AG-Sperren, Vorstrafen, Klienten, Zivilstände, Bearbeitungszustände Klienten, Hilfebeschlüsse, Einkommensbescheinigungen, Kostenübernahmescheine, Einfache Bescheinigungen
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
  - SEPA : Konten
  - ÖSHZ : Hilfebeschlüsse, Einkommensbescheinigungen, Kostenübernahmescheine, Einfache Bescheinigungen
- Site : Info



List of window layouts
======================

The following table lists information about all *data entry form
definitions* (called **window layouts**) used by Lino Welfare.  There
are *detail* layouts, *insert* layouts and *action parameter* layouts.

Each window layout is **viewable** by a given set of user profiles.
Each window layout defines a given set of fields.


>>> #settings.SITE.catch_layout_exceptions = False
>>> from lino.utils.diag import window_actions
>>> print window_actions()
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF -SKIP
- about.About.show (viewable for all except anonymous) : server_status
- about.Models.detail (viewable for all except anonymous) : app, name, docstring, rows
- accounts.AccountCharts.detail (viewable for admin) : name
- accounts.Accounts.detail (viewable for admin) : ref, name, name_fr, name_en, group, type, required_for_household, required_for_person, periods, default_amount
- accounts.Accounts.insert (viewable for admin) : ref, group, type, name, name_fr, name_en
- accounts.Groups.detail (viewable for admin) : ref, name, name_fr, name_en, id, account_type, entries_layout
- accounts.Groups.insert (viewable for admin) : name, name_fr, name_en, account_type, ref
- addresses.Addresses.detail (viewable for admin) : country, city, zip_code, addr1, street, street_no, street_box, addr2, address_type, remark, data_source, partner
- addresses.Addresses.insert (viewable for admin) : country, city, street, street_no, street_box, address_type, remark
- aids.AidTypes.detail (viewable for 110, 210, 220, 410, 500, admin) : id, short_name, confirmation_type, name, name_fr, name_en, excerpt_title, excerpt_title_fr, excerpt_title_en, body_template, print_directly, is_integ_duty, is_urgent, confirmed_by_primary_coach, board, company, contact_person, contact_role, pharmacy_type
- aids.AidTypes.insert (viewable for 110, 210, 220, 410, 500, admin) : name, name_fr, name_en, confirmation_type
- aids.Categories.insert (viewable for 110, 210, 220, 410, 500, admin) : id, name, name_fr, name_en
- aids.Grantings.detail (viewable for all except anonymous) : id, client, user, signer, workflow_buttons, request_date, board, decision_date, aid_type, category, start_date, end_date, custom_actions
- aids.Grantings.insert (viewable for all except anonymous) : client, aid_type, signer, board, decision_date, start_date, end_date
- aids.GrantingsByClient.insert (viewable for all except anonymous) : aid_type, board, decision_date, start_date, end_date
- aids.IncomeConfirmations.insert (viewable for all except anonymous) : client, user, signer, workflow_buttons, printed, company, contact_person, language, granting, start_date, end_date, category, amount, id, remark
- aids.IncomeConfirmationsByGranting.insert (viewable for all except anonymous) : client, granting, start_date, end_date, category, amount, company, contact_person, language, remark
- aids.RefundConfirmations.insert (viewable for all except anonymous) : id, client, user, signer, workflow_buttons, granting, start_date, end_date, doctor_type, doctor, pharmacy, company, contact_person, language, printed, remark
- aids.RefundConfirmationsByGranting.insert (viewable for all except anonymous) : start_date, end_date, doctor_type, doctor, pharmacy, company, contact_person, language, printed, remark
- aids.SimpleConfirmations.insert (viewable for all except anonymous) : id, client, user, signer, workflow_buttons, granting, start_date, end_date, company, contact_person, language, printed, remark
- aids.SimpleConfirmationsByGranting.insert (viewable for all except anonymous) : start_date, end_date, company, contact_person, language, remark
- art61.ContractTypes.insert (viewable for 110, admin) : id, name, name_fr, name_en, ref
- art61.Contracts.detail (viewable for 100, 110, 120, admin) : id, client, user, language, type, company, contact_person, contact_role, applies_from, duration, applies_until, exam_policy, job_title, status, cv_duration, regime, reference_person, printed, date_decided, date_issued, date_ended, ending, subsidize_10, subsidize_20, subsidize_30, responsibilities
- art61.Contracts.insert (viewable for 100, 110, 120, admin) : client, company, type
- boards.Boards.detail (viewable for admin) : id, name, name_fr, name_en
- boards.Boards.insert (viewable for admin) : name, name_fr, name_en
- cal.Calendars.detail (viewable for 110, 410, admin) : name, name_fr, name_en, color, id, description
- cal.Calendars.insert (viewable for 110, 410, admin) : name, name_fr, name_en, color
- cal.EventTypes.detail (viewable for 110, 410, admin) : name, name_fr, name_en, event_label, event_label_fr, event_label_en, max_conflicting, all_rooms, locks_user, id, invite_client, is_appointment, email_template, attach_to_email
- cal.EventTypes.insert (viewable for 110, 410, admin) : name, name_fr, name_en, invite_client
- cal.Events.detail (viewable for 110, 410, admin) : event_type, summary, project, start_date, start_time, end_date, end_time, user, assigned_to, room, priority, access_class, transparent, owner, workflow_buttons, description, id, created, modified, state
- cal.Events.insert (viewable for 110, 410, admin) : summary, start_date, start_time, end_date, end_time, event_type, project
- cal.EventsByClient.insert (viewable for all except anonymous, 210, 220) : event_type, summary, start_date, start_time, end_date, end_time
- cal.GuestRoles.insert (viewable for admin) : id, name, name_fr, name_en
- cal.GuestStates.wf1 (viewable for admin) : notify_subject, notify_body, notify_silent
- cal.GuestStates.wf2 (viewable for admin) : notify_subject, notify_body, notify_silent
- cal.Guests.checkin (viewable for admin) : notify_subject, notify_body, notify_silent
- cal.Guests.detail (viewable for admin) : event, partner, role, state, remark, workflow_buttons, waiting_since, busy_since, gone_since
- cal.Guests.insert (viewable for admin) : event, partner, role
- cal.RecurrentEvents.detail (viewable for 110, 410, admin) : name, name_fr, name_en, id, user, event_type, start_date, start_time, end_date, end_time, every_unit, every, max_events, monday, tuesday, wednesday, thursday, friday, saturday, sunday, description
- cal.RecurrentEvents.insert (viewable for 110, 410, admin) : name, name_fr, name_en, start_date, end_date, every_unit, event_type
- cal.Rooms.insert (viewable for 110, 410, admin) : id, name, name_fr, name_en
- cal.Tasks.detail (viewable for 110, 410, admin) : start_date, due_date, id, workflow_buttons, summary, project, user, delegated, owner, created, modified, description
- cal.Tasks.insert (viewable for 110, 410, admin) : summary, user, project
- cal.TasksByController.insert (viewable for all except anonymous, 210, 220) : summary, start_date, due_date, user, delegated
- cbss.IdentifyPersonRequests.detail (viewable for all except anonymous, 500) : id, person, user, sent, status, printed, national_id, first_name, middle_name, last_name, birth_date, tolerance, gender, environment, ticket, response_xml, info_messages, debug_messages
- cbss.IdentifyPersonRequests.insert (viewable for all except anonymous, 500) : person, national_id, first_name, middle_name, last_name, birth_date, tolerance, gender
- cbss.ManageAccessRequests.detail (viewable for all except anonymous, 500) : id, person, user, sent, status, printed, action, start_date, end_date, purpose, query_register, national_id, sis_card_no, id_card_no, first_name, last_name, birth_date, result, environment, ticket, response_xml, info_messages, debug_messages
- cbss.ManageAccessRequests.insert (viewable for all except anonymous, 500) : person, action, start_date, end_date, purpose, query_register, national_id, sis_card_no, id_card_no, first_name, last_name, birth_date
- cbss.RetrieveTIGroupsRequests.detail (viewable for all except anonymous, 500) : id, person, user, sent, status, printed, national_id, language, history, environment, ticket, response_xml, info_messages, debug_messages
- cbss.RetrieveTIGroupsRequests.insert (viewable for all except anonymous, 500) : person, national_id, language, history
- changes.Changes.detail (viewable for admin) : time, user, type, master, object, id, diff
- contacts.Companies.detail (viewable for all except anonymous) : overview, prefix, name, type, vat_id, client_contact_type, url, email, phone, gsm, fax, remarks, id, language, activity, is_obsolete, created, modified
- contacts.Companies.insert (viewable for all except anonymous) : name, language, email, type, id
- contacts.Companies.merge_row (viewable for 110, 210, 220, 410, admin) : merge_to, reason
- contacts.Partners.detail (viewable for all except anonymous) : overview, id, language, activity, client_contact_type, url, email, phone, gsm, fax, country, region, city, zip_code, addr1, street_prefix, street, street_no, street_box, addr2, remarks, is_obsolete, created, modified
- contacts.Partners.insert (viewable for all except anonymous) : name, language, email
- contacts.Persons.create_household (viewable for all except anonymous) : partner, type, head
- contacts.Persons.detail (viewable for all except anonymous) : overview, title, first_name, middle_name, last_name, gender, birth_date, age, id, language, email, phone, gsm, fax, MembersByPerson, LinksByHuman, remarks, activity, url, client_contact_type, is_obsolete, created, modified
- contacts.Persons.insert (viewable for all except anonymous) : first_name, last_name, gender, language
- countries.Countries.detail (viewable for all except anonymous) : isocode, name, name_fr, name_en, short_code, inscode, actual_country
- countries.Countries.insert (viewable for all except anonymous) : isocode, inscode, name, name_fr, name_en
- countries.Places.insert (viewable for 110, 210, 220, 410, admin) : name, name_fr, name_en, country, type, parent, zip_code, id
- countries.Places.merge_row (viewable for 110, 210, 220, 410, admin) : merge_to, reason
- courses.CourseContents.insert (viewable for 110, admin) : id, name
- courses.CourseOffers.detail (viewable for 100, 110, 120, admin) : id, title, content, provider, guest_role, description
- courses.CourseOffers.insert (viewable for 100, 110, 120, admin) : provider, content, title
- courses.CourseProviders.detail (viewable for 100, 110, 120, admin) : overview, prefix, name, type, vat_id, client_contact_type, url, email, phone, gsm, fax
- courses.CourseRequests.insert (viewable for 110, admin) : date_submitted, person, content, offer, urgent, course, state, date_ended, id, remark, UploadsByController
- courses.Courses.detail (viewable for 110, admin) : id, start_date, offer, title, remark
- courses.Courses.insert (viewable for 110, admin) : start_date, offer, title
- cv.Durations.insert (viewable for 110, admin) : id, name, name_fr, name_en
- cv.EducationLevels.insert (viewable for 110, admin) : name, name_fr, name_en, is_study, is_training
- cv.Experiences.insert (viewable for 110, admin) : person, start_date, end_date, termination_reason, company, country, city, sector, function, title, status, duration, regime, is_training, remarks
- cv.Functions.insert (viewable for 110, admin) : id, name, name_fr, name_en, sector, remark
- cv.Regimes.insert (viewable for 110, admin) : id, name, name_fr, name_en
- cv.Sectors.insert (viewable for 110, admin) : id, name, name_fr, name_en, remark
- cv.Statuses.insert (viewable for 110, admin) : id, name, name_fr, name_en
- cv.Studies.insert (viewable for 110, admin) : person, start_date, end_date, type, content, education_level, state, school, country, city, remarks
- cv.StudyTypes.detail (viewable for 110, admin) : name, name_fr, name_en, id, education_level, is_study, is_training
- cv.StudyTypes.insert (viewable for 110, admin) : name, name_fr, name_en, is_study, is_training, education_level
- cv.Trainings.detail (viewable for all except anonymous) : person, start_date, end_date, type, state, certificates, sector, function, school, country, city, remarks
- cv.Trainings.insert (viewable for all except anonymous) : person, start_date, end_date, type, state, certificates, sector, function, school, country, city
- debts.Budgets.detail (viewable for admin) : date, partner, id, user, intro, ResultByBudget, DebtsByBudget, AssetsByBudgetSummary, conclusion, dist_amount, printed, total_debt, include_yearly_incomes, print_empty_rows, print_todos, DistByBudget, data_box, summary_box
- debts.Budgets.insert (viewable for admin) : partner, date, user
- excerpts.ExcerptTypes.detail (viewable for admin) : id, name, name_fr, name_en, content_type, build_method, template, body_template, email_template, shortcut, primary, print_directly, certifying, print_recipient, backward_compat, attach_to_email
- excerpts.ExcerptTypes.insert (viewable for admin) : name, name_fr, name_en, content_type, primary, certifying, build_method, template, body_template
- excerpts.Excerpts.detail (viewable for all except anonymous) : id, excerpt_type, project, user, build_method, company, contact_person, language, owner, build_time, body_template_content
- gfks.ContentTypes.insert (viewable for admin) : id, name, app_label, model, base_classes
- households.Households.detail (viewable for all except anonymous) : type, prefix, name, id
- households.HouseholdsByType.detail (viewable for all except anonymous) : type, name, language, id, country, region, city, zip_code, street_prefix, street, street_no, street_box, addr2, phone, gsm, email, url, remarks
- households.Types.insert (viewable for 110, 210, 220, 410, admin) : name, name_fr, name_en
- humanlinks.Links.insert (viewable for 110, 210, 220, 410, admin) : parent, child, type
- integ.ActivityReport.show (viewable for 100, 110, 120, admin) : body
- isip.ContractEndings.insert (viewable for 110, 410, admin) : name, use_in_isip, use_in_jobs, is_success, needs_date_ended
- isip.ContractPartners.insert (viewable for 110, admin) : company, contact_person, contact_role, duties_company
- isip.ContractTypes.insert (viewable for 110, 410, admin) : id, ref, exam_policy, needs_study_type, name, name_fr, name_en, full_name
- isip.Contracts.detail (viewable for 100, 110, 120, admin) : id, client, type, user, user_asd, study_type, applies_from, applies_until, exam_policy, language, date_decided, date_issued, printed, date_ended, ending, stages, goals, duties_asd, duties_dsbe, duties_person
- isip.Contracts.insert (viewable for 100, 110, 120, admin) : client, type
- isip.ExamPolicies.insert (viewable for 110, 410, admin) : id, name, name_fr, name_en, max_events, every, every_unit, event_type, monday, tuesday, wednesday, thursday, friday, saturday, sunday
- jobs.ContractTypes.insert (viewable for 110, 410, admin) : id, name, name_fr, name_en, ref
- jobs.Contracts.detail (viewable for 100, 110, 120, admin) : id, client, user, user_asd, language, job, type, company, contact_person, contact_role, applies_from, duration, applies_until, exam_policy, regime, schedule, hourly_rate, refund_rate, reference_person, remark, printed, date_decided, date_issued, date_ended, ending, responsibilities
- jobs.Contracts.insert (viewable for 100, 110, 120, admin) : client, job
- jobs.JobProviders.detail (viewable for 100, 110, 120, admin) : overview, prefix, name, type, vat_id, client_contact_type, url, email, phone, gsm, fax
- jobs.JobTypes.insert (viewable for 110, 410, admin) : id, name, is_social
- jobs.Jobs.insert (viewable for 100, 110, 120, admin) : name, provider, contract_type, type, id, sector, function, capacity, hourly_rate, remark
- jobs.JobsOverview.show (viewable for 100, 110, 120, admin) : preview
- jobs.Offers.insert (viewable for 100, 110, 120, admin) : name, provider, sector, function, selection_from, selection_until, start_date, remark
- jobs.OldJobsOverview.show (viewable for 100, 110, 120, admin) : body
- jobs.Schedules.insert (viewable for 110, 410, admin) : id, name, name_fr, name_en
- languages.Languages.insert (viewable for all except anonymous, 210, 220) : id, iso2, name, name_fr, name_en
- newcomers.AvailableCoachesByClient.assign_coach (viewable for 110, 120, 200, 220, 300, admin) : notify_subject, notify_body, notify_silent
- newcomers.Faculties.detail (viewable for 110, 410, admin) : id, name, name_fr, name_en, weight
- newcomers.Faculties.insert (viewable for 110, 410, admin) : name, name_fr, name_en, weight
- notes.EventTypes.insert (viewable for 110, 410, admin) : id, name, name_fr, name_en, remark
- notes.NoteTypes.detail (viewable for 110, 410, admin) : id, name, name_fr, name_en, build_method, template, special_type, email_template, attach_to_email, remark
- notes.NoteTypes.insert (viewable for 110, 410, admin) : name, name_fr, name_en, build_method
- notes.Notes.detail (viewable for all except anonymous) : date, time, event_type, type, project, subject, important, company, contact_person, user, language, build_time, id, body, UploadsByController
- notes.Notes.insert (viewable for all except anonymous) : event_type, type, subject, project
- outbox.Mails.detail (viewable for 110, 410, admin) : subject, project, date, user, sent, id, owner, AttachmentsByMail, UploadsByController, body
- outbox.Mails.insert (viewable for 110, 410, admin) : project, subject, body
- pcsw.ClientContactTypes.insert (viewable for 110, 410, admin) : id, name, name_fr, name_en, can_refund, is_bailiff
- pcsw.ClientStates.wf1 (viewable for 200, 300, admin) : reason, remark
- pcsw.Clients.create_visit (viewable for all except anonymous) : user, summary
- pcsw.Clients.detail (viewable for all except anonymous) : overview, gender, id, tim_id, first_name, middle_name, last_name, birth_date, age, national_id, nationality, declared_name, civil_state, birth_country, birth_place, language, email, phone, fax, gsm, image, AgentsByClient, SimilarClients, LinksByHuman, cbss_relations, MembersByPerson, workflow_buttons, id_document, broker, faculty, refusal_reason, in_belgium_since, residence_type, gesdos_id, job_agents, group, aid_type, income_ag, income_wg, income_kg, income_rente, income_misc, is_seeking, unemployed_since, work_permit_suspended_until, needs_residence_permit, needs_work_permit, UploadsByClient, cvs_emitted, skills, obstacles, ExcerptsByProject, activity, client_state, noble_condition, unavailable_until, unavailable_why, is_cpas, is_senior, is_obsolete, created, modified, remarks, remarks2, cbss_identify_person, cbss_manage_access, cbss_retrieve_ti_groups, cbss_summary
- pcsw.Clients.insert (viewable for all except anonymous) : first_name, last_name, national_id, gender, language
- pcsw.Clients.merge_row (viewable for 110, 210, 220, 410, admin) : merge_to, aids_SimpleConfirmation, aids_IncomeConfirmation, aids_RefundConfirmation, cv_LanguageKnowledge, pcsw_Coaching, pcsw_Dispense, dupable_clients_Word, properties_PersonProperty, reason
- pcsw.CoachingEndings.insert (viewable for 110, 410, admin) : id, name, name_fr, name_en, seqno
- pcsw.Coachings.create_visit (viewable for 110, 410, admin) : user, summary
- plausibility.Checkers.detail (viewable for admin) : value, name, text
- plausibility.Problems.detail (viewable for all except anonymous) : user, owner, checker, id, message
- properties.PropGroups.insert (viewable for admin) : id, name, name_fr, name_en
- properties.PropTypes.insert (viewable for admin) : id, name, name_fr, name_en, choicelist, default_value
- properties.Properties.insert (viewable for admin) : id, group, type, name, name_fr, name_en
- reception.BusyVisitors.detail (viewable for all except anonymous) : event, client, role, state, remark, workflow_buttons
- reception.GoneVisitors.detail (viewable for all except anonymous) : event, client, role, state, remark, workflow_buttons
- reception.MyWaitingVisitors.detail (viewable for all except anonymous, 210, 220) : event, client, role, state, remark, workflow_buttons
- reception.WaitingVisitors.detail (viewable for all except anonymous) : event, client, role, state, remark, workflow_buttons
- system.SiteConfigs.detail (viewable for admin) : site_company, next_partner_id, job_office, master_budget, signer1, signer2, signer1_function, signer2_function, system_note_type, default_build_method, propgroup_skills, propgroup_softskills, propgroup_obstacles, residence_permit_upload_type, work_permit_upload_type, driving_licence_upload_type, default_event_type, prompt_calendar, client_guestrole, team_guestrole, cbss_org_unit, sector, ssdn_user_id, ssdn_email, cbss_http_username, cbss_http_password
- tinymce.TextFieldTemplates.detail (viewable for admin) : id, name, user, description, text
- tinymce.TextFieldTemplates.insert (viewable for admin) : name, user
- uploads.AllUploads.detail (viewable for 110, 410, admin) : file, user, upload_area, type, description, owner
- uploads.AllUploads.insert (viewable for 110, 410, admin) : type, description, file, user
- uploads.UploadTypes.detail (viewable for 110, 410, admin) : id, upload_area, shortcut, name, name_fr, name_en, warn_expiry_unit, warn_expiry_value, wanted, max_number
- uploads.UploadTypes.insert (viewable for 110, 410, admin) : upload_area, name, name_fr, name_en, warn_expiry_unit, warn_expiry_value
- uploads.Uploads.detail (viewable for all except anonymous) : user, project, id, type, description, start_date, end_date, needed, company, contact_person, contact_role, file, owner, remark
- uploads.Uploads.insert (viewable for all except anonymous) : type, file, start_date, end_date, description
- uploads.UploadsByClient.insert (viewable for all except anonymous) : file, type, end_date, description
- uploads.UploadsByController.insert (viewable for all except anonymous) : file, type, end_date, description
- users.Users.change_password (viewable for admin) : current, new1, new2
- users.Users.detail (viewable for admin) : username, profile, partner, first_name, last_name, initials, email, language, id, created, modified, remarks, event_type, access_class, calendar, newcomer_quota, coaching_type, coaching_supervisor, newcomer_consultations, newcomer_appointments
- users.Users.insert (viewable for admin) : username, email, first_name, last_name, partner, language, profile
<BLANKLINE>



Some requests
=============


Some choices lists:

>>> kw = dict()
>>> fields = 'count rows'
>>> demo_get('rolf', 'choices/cv/SkillsByPerson/property', fields, 6, **kw)
>>> demo_get('rolf', 'choices/cv/ObstaclesByPerson/property', fields, 15, **kw)

