.. _welfare.tested.general:

=======
General
=======

.. include:: /include/tested.rst

.. How to test only this document:
  $ python setup.py test -s tests.DocsTests.test_general


..  
    >>> from __future__ import print_function
    >>> from lino.runtime import *
    >>> from django.utils import translation
    >>> from lino.utils.xmlgen.html import E


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
48 apps: about, bootstrap3, lino, system, contenttypes, humanize, users, changes, countries, properties, contacts, addresses, uploads, outbox, extensible, cal, reception, languages, accounts, badges, iban, sepa, excerpts, dedupe, boards, lino_welfare, statbel, sales, pcsw, cv, isip, jobs, integ, courses, newcomers, cbss, households, humanlinks, debts, notes, aids, projects, polls, beid, davlink, appypod, export_excel, djangosite.
121 models:
============================== ========= =======
 Name                           #fields   #rows
------------------------------ --------- -------
 accounts.Account               14        49
 accounts.Chart                 5         1
 accounts.Group                 8         7
 addresses.Address              16        119
 aids.AidType                   23        11
 aids.Category                  5         3
 aids.Granting                  10        55
 aids.IncomeConfirmation        16        54
 aids.RefundConfirmation        17        12
 aids.SimpleConfirmation        14        19
 badges.Award                   6         0
 badges.Badge                   5         0
 boards.Board                   7         3
 boards.Member                  4         0
 cal.Calendar                   7         10
 cal.Event                      24        597
 cal.EventType                  19        7
 cal.Guest                      9         616
 cal.GuestRole                  5         4
 cal.Priority                   6         4
 cal.RecurrentEvent             22        9
 cal.RemoteCalendar             7         0
 cal.Room                       5         0
 cal.Subscription               4         9
 cal.Task                       19        34
 cbss.IdentifyPersonRequest     20        5
 cbss.ManageAccessRequest       23        1
 cbss.Purpose                   7         106
 cbss.RetrieveTIGroupsRequest   14        2
 cbss.Sector                    11        209
 changes.Change                 9         0
 contacts.Company               30        47
 contacts.CompanyType           9         16
 contacts.Partner               26        170
 contacts.Person                33        109
 contacts.Role                  4         10
 contacts.RoleType              6         5
 contenttypes.ContentType       4         122
 countries.Country              8         8
 countries.Place                10        78
 courses.Course                 5         3
 courses.CourseContent          2         2
 courses.CourseOffer            6         3
 courses.CourseProvider         31        2
 courses.CourseRequest          10        20
 cv.LanguageKnowledge           9         119
 debts.Actor                    6         63
 debts.Budget                   11        14
 debts.Entry                    16        686
 excerpts.Excerpt               12        92
 excerpts.ExcerptType           18        11
 households.Household           29        14
 households.Member              13        63
 households.Type                5         6
 humanlinks.Link                4         59
 isip.Contract                  22        30
 isip.ContractEnding            6         4
 isip.ContractPartner           6         35
 isip.ContractType              9         5
 isip.EducationLevel            6         5
 isip.ExamPolicy                20        5
 isip.StudyType                 7         8
 jobs.Candidature               8         74
 jobs.Contract                  28        24
 jobs.ContractType              9         5
 jobs.Experience                13        30
 jobs.Function                  7         4
 jobs.Job                       10        8
 jobs.JobProvider               31        3
 jobs.JobType                   4         5
 jobs.Offer                     9         1
 jobs.Regime                    5         3
 jobs.Schedule                  5         3
 jobs.Sector                    6         14
 jobs.Status                    5         7
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
 pcsw.Client                    65        63
 pcsw.ClientContact             7         14
 pcsw.ClientContactType         7         9
 pcsw.Coaching                  8         90
 pcsw.CoachingEnding            7         4
 pcsw.CoachingType              8         3
 pcsw.Dispense                  6         0
 pcsw.DispenseReason            6         4
 pcsw.Exclusion                 6         0
 pcsw.ExclusionType             2         2
 pcsw.PersonGroup               4         5
 polls.AnswerChoice             4         0
 polls.AnswerRemark             4         0
 polls.Choice                   7         31
 polls.ChoiceSet                5         7
 polls.Poll                     11        0
 polls.Question                 6         0
 polls.Response                 8         0
 projects.Project               10        0
 projects.ProjectType           5         0
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
 uploads.UploadType             10        8
 users.Authority                3         3
 users.User                     19        10
============================== ========= =======
<BLANKLINE>

User profiles
-------------

Rolf is the local system administrator, he has a complete menu:

>>> ses = rt.login('rolf') 
>>> with translation.override('de'):
...     ses.show_menu()
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
- Kontakte : Personen,  ▶ Klienten, Organisationen, -, Partner (alle), Haushalte
- Büro : Meine Uploads, Mein E-Mail-Ausgang, Meine Auszüge, Meine Ereignisse/Notizen
- Kalender : Kalender, Meine Termine, Meine Aufgaben, Meine Gäste, Meine Anwesenheiten
- Empfang : Klienten, Termine heute, Wartende Besucher, Beschäftigte Besucher, Gegangene Besucher, Meine Warteschlange
- ÖSHZ : Meine Begleitungen, Zu unterschreibende Hilfebeschlüsse
- DSBE : Klienten, VSEs, Art.60§7-Konventionen, Stellenanbieter, Stellen, Stellenangebote
- Kurse : Kursanbieter, Kursangebote, Offene Kursanfragen
- Neuanträge : Neue Klienten, Verfügbare Begleiter
- Schuldnerberatung : Klienten, Meine Budgets
- Polls : Meine Polls, Meine Responses
- Listings :
  - ÖSHZ : Datenkontrolle Klienten
  - DSBE : Benutzer und ihre Klienten, Übersicht Art.60§7-Konventionen, Tätigkeitsbericht
- Konfigurierung :
  - Büro : Meine Einfügetexte, Upload-Arten, Auszugsarten, Notizarten, Ereignisarten
  - System : Site-Parameter, Benutzer, Inhaltstypen, Hilfetexte
  - Orte : Länder, Orte
  - Eigenschaften : Eigenschaftsgruppen, Eigenschafts-Datentypen, Fachkompetenzen, Sozialkompetenzen, Hindernisse
  - Kontakte : Organisationsarten, Funktionen, Sprachen, Gremien, Haushaltsarten
  - Kalender : Kalenderliste, Räume, Prioritäten, Periodische Termine, Gastrollen, Ereignisarten, Externe Kalender
  - Buchhaltung : Kontenpläne, Kontengruppen, Konten
  - Badges : Badges
  - ÖSHZ : Integrationsphasen, Berufe, AG-Sperrgründe, Dienste, Begleitungsbeendigungsgründe, Dispenzgründe, Klientenkontaktarten, Hilfearten, Kategorien
  - DSBE : VSE-Arten, Vertragsbeendigungsgründe, Auswertungsstrategien, Ausbildungsarten, Akademische Grade, Art.60§7-Konventionsarten, Stellenarten, Sektoren, Funktionen, Stundenpläne, Regimes, Statuses
  - Kurse : Kursinhalte
  - Neuanträge : Vermittler, Fachbereiche
  - ZDSS : Sektoren, Eigenschafts-Codes
  - Schuldnerberatung : Budget-Kopiervorlage
  - Client projects : Client project types
  - Polls : Choice Sets
- Explorer :
  - Büro : Einfügetexte, Uploads, Upload-Bereiche, E-Mail-Ausgänge, Anhänge, Auszüge, Ereignisse/Notizen
  - System : Vollmachten, Benutzergruppen, Benutzer-Levels, Benutzerprofile, Änderungen
  - Eigenschaften : Eigenschaften
  - Kontakte : Kontaktpersonen, Adressenarten, Adressen, Gremienmitglieder, Rollen, Mitglieder, Verwandtschaftsbeziehungen, Verwandschaftsarten
  - Kalender : Aufgaben, Anwesenheiten, Abonnements, Termin-Zustände, Gast-Zustände, Aufgaben-Zustände
  - Badges : Badge Awards
  - SEPA : Konten
  - ÖSHZ : Begleitungen, Klientenkontakte, AG-Sperren, Klienten, Zivilstände, Bearbeitungszustände Klienten, eID-Kartenarten, Hilfebeschlüsse, Einkommensbescheinigungen, Kostenübernahmescheine, Einfache Bescheinigungen
  - DSBE : Sprachkenntnisse, VSEs, Art.60§7-Konventionen, Stellenanfragen, Ausbildungen und Studien, Vertragspartner
  - Kurse : Kurse, Kursanfragen
  - Kompetenzen
  - ZDSS : IdentifyPerson-Anfragen, ManageAccess-Anfragen, Tx25-Anfragen
  - Schuldnerberatung : Budgets, Einträge
  - Client projects : Client Projects
  - Polls : Polls, Questions, Choices, Responses, Answer Choices, AnswerRemarks
- Site : Info
<BLANKLINE>


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
- Listings :
  - DSBE : Benutzer und ihre Klienten, Übersicht Art.60§7-Konventionen, Tätigkeitsbericht
- Konfigurierung :
  - Büro : Meine Einfügetexte
  - Kontakte : Länder, Sprachen
- Explorer :
  - DSBE : VSEs, Art.60§7-Konventionen
- Site : Info



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

Caroline is a newcomers consultant.

>>> ses = rt.login('caroline') 
>>> with translation.override('de'):
...     ses.show_menu()
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF +SKIP
- Kontakte : Personen,  ▶ Klienten, Organisationen, -, Partner (alle), Haushalte
- Büro : Mein E-Mail-Ausgang, Meine Auszüge, Meine Ereignisse/Notizen
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

>>> ses = rt.login('theresia') 
>>> with translation.override('de'):
...     ses.show_menu()
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF +SKIP
- Empfang : Klienten, Termine heute, Wartende Besucher, Beschäftigte Besucher, Gegangene Besucher
- Site : Info


Permissions
-----------

Test whether everybody can display the detail of a client:

>>> o = pcsw.Client.objects.get(id=177)
>>> r = dd.plugins.extjs.renderer
>>> for u in 'robin', 'alicia', 'theresia':
...     print(E.tostring(rt.login(u, renderer=r).obj2html(o)))
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
<a href="javascript:Lino.pcsw.Clients.detail.run(null,{ &quot;record_id&quot;: 177 })">BRECHT Bernd (177)</a>
<a href="javascript:Lino.pcsw.Clients.detail.run(null,{ &quot;record_id&quot;: 177 })">BRECHT Bernd (177)</a>
<a href="javascript:Lino.pcsw.Clients.detail.run(null,{ &quot;record_id&quot;: 177 })">BRECHT Bernd (177)</a>
