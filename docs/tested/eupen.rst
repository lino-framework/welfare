.. _welfare.tested.eupen:

==================================
Eupen (tested tour)
==================================

.. How to test only this document:

  $ python setup.py test -s tests.DocsTests.test_eupen

.. contents:: 
   :local:
   :depth: 2

A tested document
=================

.. include:: /include/tested.rst

>>> from __future__ import print_function
>>> import os
>>> os.environ['DJANGO_SETTINGS_MODULE'] = \
...    'lino_welfare.projects.eupen.settings.doctests'
>>> from lino.api.doctest import *


User profiles
=============

.. _rolf:

Rolf
----

Rolf is the local system administrator, he has a complete menu:

>>> ses = rt.login('rolf') 
>>> with translation.override('de'):
...     ses.show_menu()
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
- Kontakte : Personen,  ▶ Klienten, Organisationen, -, Partner (alle), Haushalte
- Büro : Ablaufende Uploads, Meine Uploads, Mein E-Mail-Ausgang, Meine Auszüge, Meine Ereignisse/Notizen, Meine Datenkontrollliste
- Kalender : Kalender, Meine Termine, Meine Aufgaben, Meine Gäste, Meine Anwesenheiten
- Empfang : Klienten, Termine heute, Wartende Besucher, Beschäftigte Besucher, Gegangene Besucher, Meine Warteschlange
- ÖSHZ : Meine Begleitungen, Zu bestätigende Hilfebeschlüsse
- DSBE : Klienten, VSEs, Art.60§7-Konventionen, Stellenanbieter, Stellen, Stellenangebote, Art.61-Konventionen
- Kurse : Kursanbieter, Kursangebote, Offene Kursanfragen
- Erstempfang : Neue Klienten, Verfügbare Begleiter
- Schuldnerberatung : Klienten, Meine Budgets
- Berichte :
  - System : Broken GFKs
  - DSBE : Benutzer und ihre Klienten, Übersicht Art.60§7-Konventionen, Tätigkeitsbericht
- Konfigurierung :
  - System : Site-Parameter, Benutzer, Hilfetexte
  - Orte : Länder, Orte
  - Eigenschaften : Eigenschaftsgruppen, Eigenschafts-Datentypen, Fachkompetenzen, Sozialkompetenzen, Hindernisse
  - Kontakte : Organisationsarten, Funktionen, Gremien, Haushaltsarten
  - Büro : Upload-Arten, Auszugsarten, Notizarten, Ereignisarten, Meine Einfügetexte
  - Buchhaltung : Journale
  - MWSt. : Zahlungsbedingungen, MWSt-Regeln
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
  - System : Vollmachten, Benutzergruppen, Benutzer-Levels, Benutzerprofile, Datenbankmodelle, Änderungen, Datentests, Datenprobleme
  - Eigenschaften : Eigenschaften
  - Kontakte : Kontaktpersonen, Adressenarten, Adressen, Gremienmitglieder, Rollen, Mitglieder, Verwandtschaftsbeziehungen, Verwandschaftsarten
  - Büro : Uploads, Upload-Bereiche, E-Mail-Ausgänge, Anhänge, Auszüge, Ereignisse/Notizen, Einfügetexte
  - Kalender : Aufgaben, Teilnehmer, Abonnements, Termin-Zustände, Gast-Zustände, Aufgaben-Zustände
  - SEPA : Konten
  - MWSt. : VatRegimes, TradeTypes, VatClasses
  - Buchhaltung : Rechnungen, Belege, VoucherTypes, Bewegungen, Geschäftsjahre
  - Finanzjournale : Kontoauszüge, Diverse Buchungen, Zahlungsaufträge, Groupers
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

>>> ses = rt.login('hubert') 
>>> with translation.override('de'):
...     ses.show_menu()
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF -SKIP
- Kontakte : Personen,  ▶ Klienten, Organisationen, -, Partner (alle), Haushalte
- Büro : Ablaufende Uploads, Meine Uploads, Mein E-Mail-Ausgang, Meine Auszüge, Meine Ereignisse/Notizen, Meine Datenkontrollliste
- Kalender : Kalender, Meine Termine, Meine Aufgaben, Meine Gäste, Meine Anwesenheiten
- Empfang : Termine heute, Wartende Besucher, Beschäftigte Besucher, Gegangene Besucher, Meine Warteschlange
- ÖSHZ : Meine Begleitungen, Zu bestätigende Hilfebeschlüsse
- DSBE : Klienten, VSEs, Art.60§7-Konventionen, Stellenanbieter, Stellen, Stellenangebote, Art.61-Konventionen
- Kurse : Kursanbieter, Kursangebote, Offene Kursanfragen
- Berichte :
  - System : Broken GFKs
  - DSBE : Benutzer und ihre Klienten, Übersicht Art.60§7-Konventionen, Tätigkeitsbericht
- Konfigurierung :
  - Orte : Länder
  - Büro : Meine Einfügetexte
  - Lebenslauf : Sprachen
- Explorer :
  - Kontakte : Adressenarten, Rollen
  - Büro : Upload-Bereiche
  - SEPA : Konten
  - ÖSHZ : Einkommensbescheinigungen, Kostenübernahmescheine, Einfache Bescheinigungen
  - DSBE : VSEs, Art.60§7-Konventionen, Vertragspartner, Art.61-Konventionen
- Site : Info


.. _melanie:

Mélanie
-------

Mélanie is the manager of the Integration service.

>>> ses = rt.login('melanie') 
>>> with translation.override('de'):
...     ses.show_menu()
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF -SKIP
- Kontakte : Personen,  ▶ Klienten, Organisationen, -, Partner (alle), Haushalte
- Büro : Ablaufende Uploads, Meine Uploads, Mein E-Mail-Ausgang, Meine Auszüge, Meine Ereignisse/Notizen, Meine Datenkontrollliste
- Kalender : Kalender, Meine Termine, Meine Aufgaben, Meine Gäste, Meine Anwesenheiten
- Empfang : Termine heute, Wartende Besucher, Beschäftigte Besucher, Gegangene Besucher, Meine Warteschlange
- ÖSHZ : Meine Begleitungen, Zu bestätigende Hilfebeschlüsse
- DSBE : Klienten, VSEs, Art.60§7-Konventionen, Stellenanbieter, Stellen, Stellenangebote, Art.61-Konventionen
- Kurse : Kursanbieter, Kursangebote, Offene Kursanfragen
- Berichte :
  - System : Broken GFKs
  - DSBE : Benutzer und ihre Klienten, Übersicht Art.60§7-Konventionen, Tätigkeitsbericht
- Konfigurierung :
  - Orte : Länder
  - Büro : Meine Einfügetexte
  - Kalender : Kalenderliste, Räume, Prioritäten, Periodische Termine, Kalendereintragsarten, Externe Kalender
  - ÖSHZ : Integrationsphasen, Begleitungsbeendigungsgründe, Dispenzgründe
  - Lebenslauf : Sprachen, Akademische Grade, Sektoren, Funktionen, Arbeitsregimes, Statuus, Vertragsdauern
  - DSBE : VSE-Arten, Vertragsbeendigungsgründe, Auswertungsstrategien, Art.60§7-Konventionsarten, Stellenarten, Stundenpläne, Art.61-Konventionsarten
  - Kurse : Kursinhalte
- Explorer :
  - Kontakte : Adressenarten, Rollen
  - Büro : Upload-Bereiche, E-Mail-Ausgänge, Anhänge
  - Kalender : Aufgaben, Abonnements
  - SEPA : Konten
  - ÖSHZ : Einkommensbescheinigungen, Kostenübernahmescheine, Einfache Bescheinigungen
  - Lebenslauf : Sprachkenntnisse, Ausbildungen, Studien, Berufserfahrungen
  - DSBE : VSEs, Art.60§7-Konventionen, Stellenanfragen, Vertragspartner, Art.61-Konventionen
  - Kurse : Kursanfragen
- Site : Info


Kerstin
-------

Kerstin is a debts consultant.

>>> ses = rt.login('kerstin') 
>>> with translation.override('de'):
...     ses.show_menu()
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF -SKIP
- Kontakte : Personen,  ▶ Klienten, Organisationen, -, Partner (alle), Haushalte
- Büro : Ablaufende Uploads, Meine Uploads, Mein E-Mail-Ausgang, Meine Auszüge, Meine Ereignisse/Notizen, Meine Datenkontrollliste
- Kalender : Kalender, Meine Termine, Meine Aufgaben, Meine Gäste, Meine Anwesenheiten
- Empfang : Termine heute, Wartende Besucher, Beschäftigte Besucher, Gegangene Besucher, Meine Warteschlange
- ÖSHZ : Meine Begleitungen, Zu bestätigende Hilfebeschlüsse
 - Erstempfang : Neue Klienten, Verfügbare Begleiter
 - Schuldnerberatung : Klienten, Meine Budgets
- Berichte :
  - System : Broken GFKs
- Konfigurierung :
  - Orte : Länder
  - Büro : Meine Einfügetexte
  - Lebenslauf : Sprachen
  - Schuldnerberatung : Budget-Kopiervorlage
- Explorer :
  - Kontakte : Adressenarten, Rollen
  - Büro : Upload-Bereiche
  - SEPA : Konten
  - ÖSHZ : Einkommensbescheinigungen, Kostenübernahmescheine, Einfache Bescheinigungen
  - DSBE : Vertragspartner
- Site : Info



Caroline
--------

Caroline is a newcomers consultant.

>>> ses = rt.login('caroline') 
>>> with translation.override('de'):
...     ses.show_menu()
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
- Kontakte : Personen,  ▶ Klienten, Organisationen, -, Partner (alle), Haushalte
- Büro : Ablaufende Uploads, Meine Uploads, Mein E-Mail-Ausgang, Meine Auszüge, Meine Ereignisse/Notizen, Meine Datenkontrollliste
- Kalender : Kalender, Meine Termine, Meine Aufgaben, Meine Gäste, Meine Anwesenheiten
- Empfang : Termine heute, Wartende Besucher, Beschäftigte Besucher, Gegangene Besucher, Meine Warteschlange
- ÖSHZ : Meine Begleitungen, Zu bestätigende Hilfebeschlüsse
- Erstempfang : Neue Klienten, Verfügbare Begleiter
- Berichte :
  - System : Broken GFKs
- Konfigurierung :
  - Orte : Länder
  - Büro : Meine Einfügetexte
  - Lebenslauf : Sprachen
- Explorer :
  - Kontakte : Adressenarten, Rollen
  - Büro : Upload-Bereiche
  - SEPA : Konten
  - ÖSHZ : Einkommensbescheinigungen, Kostenübernahmescheine, Einfache Bescheinigungen
  - DSBE : Vertragspartner
- Site : Info


.. _theresia:

Theresia
--------

Theresia is a reception clerk.

>>> ses = rt.login('theresia') 
>>> with translation.override('de'):
...     ses.show_menu()
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF +SKIP
- Empfang : Klienten, Termine heute, Wartende Besucher, Beschäftigte Besucher, Gegangene Besucher
- Site : Info


Some requests
=============


Some choices lists:
>>> kw = dict()
>>> fields = 'count rows'
>>> demo_get(
...     'rolf', 'choices/cv/SkillsByPerson/property', fields, 6, **kw)
>>> demo_get(
...    'rolf', 'choices/cv/ObstaclesByPerson/property', fields, 15, **kw)
