.. _welfare.tested.eupen:

==================================
Eupen (tested tour)
==================================

.. How to test only this document:

    $ python setup.py test -s tests.DocsTests.test_eupen

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
  - Kontakte : Kontaktpersonen, Adressenarten, Adressen, Gremienmitglieder, Household member roles, Mitglieder, Verwandtschaftsbeziehungen, Verwandschaftsarten
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
Integrations-Assistent (Manager)
>>> p.role.__class__
<class 'lino_welfare.modlib.integ.roles.IntegrationStaff'>

>>> with translation.override('de'):
...     rt.login('melanie').show_menu()
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
  - Kontakte : Kontaktpersonen, Adressenarten, Household member roles, Mitglieder, Verwandtschaftsbeziehungen, Verwandschaftsarten
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
<class 'lino_welfare.projects.std.roles.ReceptionClerk'>


>>> with translation.override('de'):
...     rt.login('theresia') .show_menu()
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF -SKIP
- Kontakte : Personen,  ▶ Klienten, Organisationen, -, Partner (alle), Haushalte
- Büro : Ablaufende Uploads, Meine Uploads, Meine Auszüge, Meine Ereignisse/Notizen
- Empfang : Klienten, Termine heute, Wartende Besucher, Beschäftigte Besucher, Gegangene Besucher
- Konfigurierung :
  - Orte : Länder
  - ÖSHZ : Hilfearten, Kategorien
- Explorer :
  - ÖSHZ : Hilfebeschlüsse, Einkommensbescheinigungen, Kostenübernahmescheine, Einfache Bescheinigungen
- Site : Info



Some requests
=============


Some choices lists:

>>> kw = dict()
>>> fields = 'count rows'
>>> demo_get('rolf', 'choices/cv/SkillsByPerson/property', fields, 6, **kw)
>>> demo_get('rolf', 'choices/cv/ObstaclesByPerson/property', fields, 15, **kw)

