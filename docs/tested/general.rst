.. _welfare.tested.general:

General
=======

.. include:: /include/tested.rst

.. How to test only this document:
  $ python setup.py test -s tests.DocsTests.test_general


..  
    >>> from __future__ import print_function
    >>> from lino import dd
    >>> from lino.runtime import *
    >>> from django.utils import translation


See :blogref:`20130508`:

>>> for model in (debts.Entry,):
...     for o in model.objects.all():
...         o.full_clean()

Check whether Lino returns the right default template for excerpts 
(see :blogref:`20140208`):

>>> ffn = settings.SITE.find_config_file('Default.odt', 'excerpts')
>>> ffn.endswith('lino_welfare/config/excerpts/Default.odt')
True



The test database
-----------------

Test whether :meth:`get_db_overview_rst 
<lino_site.Site.get_db_overview_rst>` returns the expected result:

(currently not tested because times are changing)

>>> print(settings.SITE.get_db_overview_rst()) 
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
44 apps: about, bootstrap3, system, contenttypes, humanize, users, changes, countries, properties, contacts, addresses, uploads, outbox, extensible, cal, households, reception, languages, accounts, badges, iban, sepa, excerpts, humanlinks, dedupe, boards, lino_welfare, statbel, sales, pcsw, cv, isip, jobs, integ, courses, newcomers, debts, cbss, notes, aids, beid, appypod, export_excel, djangosite.
110 models:
============================== ========= =======
 Name                           #fields   #rows
------------------------------ --------- -------
 accounts.Account               14        49
 accounts.Chart                 5         1
 accounts.Group                 8         7
 addresses.Address              16        114
 aids.AidType                   11        6
 aids.Category                  5         3
 aids.Confirmation              11        12
 aids.Helper                    5         0
 aids.HelperRole                6         3
 badges.Award                   6         0
 badges.Badge                   5         0
 boards.Board                   7         3
 boards.Member                  4         0
 cal.Calendar                   7         10
 cal.Event                      24        314
 cal.EventType                  19        7
 cal.Guest                      9         19
 cal.GuestRole                  7         4
 cal.Priority                   6         9
 cal.RecurrentEvent             22        9
 cal.RemoteCalendar             7         0
 cal.Room                       5         0
 cal.Subscription               4         8
 cal.Task                       18        34
 cbss.IdentifyPersonRequest     20        5
 cbss.ManageAccessRequest       23        1
 cbss.Purpose                   7         106
 cbss.RetrieveTIGroupsRequest   14        2
 cbss.Sector                    11        209
 changes.Change                 9         0
 contacts.Company               30        46
 contacts.CompanyType           9         16
 contacts.Partner               25        152
 contacts.Person                32        101
 contacts.Role                  4         10
 contacts.RoleType              6         5
 contenttypes.ContentType       4         111
 countries.Country              8         8
 countries.Place                10        76
 courses.Course                 5         3
 courses.CourseContent          2         2
 courses.CourseOffer            6         3
 courses.CourseProvider         31        2
 courses.CourseRequest          10        20
 cv.LanguageKnowledge           7         119
 debts.Actor                    6         10
 debts.Budget                   11        5
 debts.Entry                    16        245
 excerpts.Excerpt               12        8
 excerpts.ExcerptType           15        8
 households.Household           28        5
 households.Member              12        10
 households.Type                5         4
 humanlinks.Link                4         36
 isip.Contract                  22        17
 isip.ContractEnding            6         4
 isip.ContractPartner           6         16
 isip.ContractType              8         5
 isip.EducationLevel            6         5
 isip.ExamPolicy                20        5
 isip.StudyType                 7         8
 jobs.Candidature               8         74
 jobs.Contract                  28        16
 jobs.ContractType              9         5
 jobs.Experience                10        30
 jobs.Function                  7         4
 jobs.Job                       10        8
 jobs.JobProvider               31        3
 jobs.JobType                   4         5
 jobs.Offer                     9         1
 jobs.Regime                    5         3
 jobs.Schedule                  5         3
 jobs.Sector                    6         14
 jobs.Study                     14        2
 languages.Language             6         5
 newcomers.Broker               2         2
 newcomers.Competence           5         7
 newcomers.Faculty              6         5
 notes.EventType                10        9
 notes.Note                     17        110
 notes.NoteType                 11        13
 outbox.Attachment              4         0
 outbox.Mail                    9         0
 outbox.Recipient               6         0
 pcsw.Activity                  3         0
 pcsw.AidType                   5         0
 pcsw.Client                    75        63
 pcsw.ClientContact             7         0
 pcsw.ClientContactType         6         5
 pcsw.Coaching                  8         77
 pcsw.CoachingEnding            7         4
 pcsw.CoachingType              7         3
 pcsw.Dispense                  6         0
 pcsw.DispenseReason            6         4
 pcsw.Exclusion                 6         0
 pcsw.ExclusionType             2         2
 pcsw.PersonGroup               4         5
 properties.PersonProperty      6         310
 properties.PropChoice          7         2
 properties.PropGroup           5         3
 properties.PropType            9         3
 properties.Property            7         23
 sepa.Account                   8         13
 system.HelpText                4         5
 system.SiteConfig              30        1
 system.TextFieldTemplate       5         2
 uploads.Upload                 16        6
 uploads.UploadType             10        7
 users.Authority                3         3
 users.User                     19        10
============================== ========= =======
<BLANKLINE>

User profiles
-------------

Rolf is the local system administrator, he has a complete menu:

>>> ses = settings.SITE.login('rolf') 
>>> with translation.override('de'):
...     ses.show_menu()
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
- Kontakte : Personen,  ▶ Klienten, Organisationen, -, Partner (alle), Haushalte
- Büro : Meine Uploads, Mein E-Mail-Ausgang, Meine Auszüge, Meine Ereignisse/Notizen
- Kalender : Kalender, Meine Termine, Meine Aufgaben, Meine Gäste, Meine Anwesenheiten
- Empfang : Klienten, Termine heute, Wartende Besucher, Beschäftigte Besucher, Gegangene Besucher, Meine Warteschlange
- DSBE : Klienten, VSEs, Art.60§7-Konventionen, Stellenanbieter, Stellen, Stellenangebote
- Kurse : Kursanbieter, Kursangebote, Offene Kursanfragen
- Neuanträge : Neue Klienten, Verfügbare Begleiter
- Schuldnerberatung : Klienten, Meine Budgets
- Listings :
  - ÖSHZ : Datenkontrolle Klienten
  - DSBE : Benutzer und ihre Klienten, Übersicht Art.60§7-Konventionen, Tätigkeitsbericht
- Konfigurierung :
  - Büro : Meine Einfügetexte, Upload-Arten, Ausdruckarten, Notizarten, Ereignisarten
  - System : Site-Parameter, Benutzer, Teams, Inhaltstypen, Hilfetexte
  - Kontakte : Länder, Orte, Organisationsarten, Funktionen, Sprachen
  - Eigenschaften : Eigenschaftsgruppen, Eigenschafts-Datentypen, Fachkompetenzen, Sozialkompetenzen, Hindernisse
  - Kalender : Kalenderliste, Räume, Prioritäten, Periodische Termine, Gastrollen, Ereignisarten, Externe Kalender
  - Haushalte : Rollen in Haushalt, Haushaltsarten
  - Buchhaltung : Kontenpläne, Kontengruppen, Konten
  - ÖSHZ : Integrationsphasen, Berufe, AG-Sperrgründe, Dienste, Begleitungsbeendigungsgründe, Dispenzgründe, Klientenkontaktarten, Hilfearten
  - DSBE : VSE-Arten, Vertragsbeendigungsgründe, Auswertungsstrategien, Ausbildungsarten, Art.60§7-Konventionsarten, Stellenarten, Sektoren, Funktionen, Stundenpläne, Regimes
  - Kurse : Kursinhalte
  - Neuanträge : Vermittler, Fachbereiche
  - Schuldnerberatung : Budget-Kopiervorlage
  - ZDSS : Sektoren, Eigenschafts-Codes
- Explorer :
  - Büro : Einfügetexte, Uploads, E-Mail-Ausgänge, Anhänge, Ausdrucke, Ereignisse/Notizen
  - System : Vollmachten, Benutzergruppen, Benutzer-Levels, Benutzerprofile, Änderungen
  - Kontakte : Kontaktpersonen, Verwandschaften, Verwandschaftsarten
  - Kalender : Aufgaben, Gäste, Abonnements, Termin-Zustände, Gast-Zustände, Aufgaben-Zustände
  - Haushalte : Mitglieder
  - ÖSHZ : Begleitungen, Klientenkontakte, AG-Sperren, Klienten, Zivilstände, Bearbeitungszustände Klienten, eID-Kartenarten, Hilfen
  - CV : Sprachkenntnisse
  - DSBE : VSEs, Art.60§7-Konventionen, Stellenanfragen, Ausbildungen und Studien
  - Kurse : Kurse, Kursanfragen
  - Kompetenzen
  - Schuldnerberatung : Budgets, Einträge
  - ZDSS : IdentifyPerson-Anfragen, ManageAccess-Anfragen, Tx25-Anfragen
  - Eigenschaften
- Site : Info
<BLANKLINE>


Hubert is an Integration agent.

>>> ses = settings.SITE.login('hubert') 
>>> with translation.override('de'):
...     ses.show_menu()
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF +SKIP
- Kontakte : Personen,  ▶ Klienten, Organisationen, -, Partner (alle), Haushalte
- Büro : Mein E-Mail-Ausgang, Meine Ausdrucke, Meine Ereignisse/Notizen
- Kalender : Kalender, Meine Termine, Meine Aufgaben, Meine Gäste, Meine Anwesenheiten
- Empfang : Meine Warteschlange
- DSBE : Klienten, VSEs, Art.60§7-Konventionen, Stellenanbieter, Stellen, Stellenangebote
- Kurse : Kursanbieter, Kursangebote, Offene Kursanfragen
- Listings :
  - DSBE : Benutzer und ihre Klienten, Übersicht Art.60§7-Konventionen, Tätigkeitsbericht
- Konfigurierung :
  - Büro : Meine Einfügetexte
  - Kontakte : Länder, Sprachen
- Explorer :
  - DSBE : VSEs, Art.60§7-Konventionen
- Site : Info



Mélanie is the manager of the Integration service.

>>> ses = settings.SITE.login('melanie') 
>>> with translation.override('de'):
...     ses.show_menu()
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF +SKIP
- Kontakte : Personen,  ▶ Klienten, Organisationen, -, Partner (alle), Haushalte
- Büro : Mein E-Mail-Ausgang, Meine Ausdrucke, Meine Ereignisse/Notizen
- Kalender : Kalender, Meine Termine, Meine Aufgaben, Meine Gäste, Meine Anwesenheiten
- Empfang : Meine Warteschlange
- DSBE : Klienten, VSEs, Art.60§7-Konventionen, Stellenanbieter, Stellen, Stellenangebote
- Kurse : Kursanbieter, Kursangebote, Offene Kursanfragen
- Listings :
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


Kerstin is a debts consultant.

>>> ses = settings.SITE.login('kerstin') 
>>> with translation.override('de'):
...     ses.show_menu()
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF +SKIP
- Kontakte : Personen,  ▶ Klienten, Organisationen, -, Partner (alle), Haushalte
- Büro : Mein E-Mail-Ausgang, Meine Ausdrucke, Meine Ereignisse/Notizen
- Kalender : Kalender, Meine Termine, Meine Aufgaben, Meine Gäste, Meine Anwesenheiten
- Empfang : Meine Warteschlange
- Schuldnerberatung : Klienten, Meine Budgets
- Konfigurierung :
  - Büro : Meine Einfügetexte
  - Kontakte : Länder, Sprachen
  - Schuldnerberatung : Budget-Kopiervorlage
- Site : Info

Caroline is a newcomers consultant.

>>> ses = settings.SITE.login('caroline') 
>>> with translation.override('de'):
...     ses.show_menu()
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF +SKIP
- Kontakte : Personen,  ▶ Klienten, Organisationen, -, Partner (alle), Haushalte
- Büro : Mein E-Mail-Ausgang, Meine Ausdrucke, Meine Ereignisse/Notizen
- Kalender : Kalender, Meine Termine, Meine Aufgaben, Meine Gäste, Meine Anwesenheiten
- Empfang : Meine Warteschlange
- Neuanträge : Neue Klienten, Verfügbare Begleiter
- Listings :
  - DSBE : Benutzer und ihre Klienten
- Konfigurierung :
  - Büro : Meine Einfügetexte
  - Kontakte : Länder, Sprachen
- Site : Info

Theresia is a reception clerk.

>>> ses = settings.SITE.login('theresia') 
>>> with translation.override('de'):
...     ses.show_menu()
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF +SKIP
- Empfang : Klienten, Termine heute, Wartende Besucher, Beschäftigte Besucher, Gegangene Besucher
- Site : Info

