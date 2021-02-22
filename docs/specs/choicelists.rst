.. doctest docs/specs/choicelists.rst

===========================
Choicelists in Lino Welfare
===========================

This document is an overview on the choicelists used in Lino Welfare.

Choicelists are "hard-coded" tables. They are not stored in the
database but in the source code or the local configuration.

.. contents::
   :depth: 2
   :local:


About this document
===================

>>> from lino import startup
>>> startup('lino_welfare.projects.gerd.settings.doctests')
>>> from lino.api.doctest import *


Overview
========

Here are the choicelists used in Lino Welfare:

>>> show_choicelists()
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF -SKIP
=============================== ======== ================= ================================== ================================== ===============================
 name                            #items   preferred_width   de                                 fr                                 en
------------------------------- -------- ----------------- ---------------------------------- ---------------------------------- -------------------------------
 about.TimeZones                 1        4                 Zeitzonen                          Zeitzonen                          Time zones
 addresses.AddressTypes          6        20                Adressenarten                      Types d'adresses                   Address types
 addresses.DataSources           2        24                Datenquellen                       Sources de données                 Data sources
 aids.AidRegimes                 3        18                None                               None                               None
 aids.ConfirmationStates         2        11                Hilfebestätigungszustände          Hilfebestätigungszustände          Aid confirmation states
 aids.ConfirmationTypes          3        49                Hilfebescheinigungsarten           Types de confirmation d'aide       Aid confirmation types
 art61.Subsidizations            5        14                Subsidizations                     Subsidiations                      Subsidizations
 beid.BeIdCardTypes              11       82                eID-Kartenarten                    Types de carte eID                 eID card types
 beid.ResidenceTypes             3        20                Einwohnerregister                  Titres de séjour                   Resident registers
 cal.AccessClasses               3        31                Zugriffsklassen                    Classes d'accès                    Access classes
 cal.DisplayColors               16       7                 Display colors                     Display colors                     Display colors
 cal.DurationUnits               7        8                 None                               None                               None
 cal.EntryStates                 5        14                Kalendereintrag-Zustände           Kalendereintrag-Zustände           Entry states
 cal.EventEvents                 2        8                 Beobachtungskriterien              Évènements observés                Observed events
 cal.GuestStates                 9        12                Anwesenheits-Zustände              Anwesenheits-Zustände              Presence states
 cal.PlannerColumns              2        6                 Tagesplanerkolonnen                Colonnes planificateur             Planner columns
 cal.Recurrencies                7        20                None                               None                               None
 cal.ReservationStates           0        4                 Zustände                           États                              States
 cal.TaskStates                  5        9                 Aufgaben-Zustände                  Aufgaben-Zustände                  Task states
 cal.Weekdays                    7        10                None                               None                               None
 cal.YearMonths                  12       9                 None                               None                               None
 cbss.ManageActions              3        12                None                               None                               None
 cbss.QueryRegisters             3        8                 None                               None                               None
 cbss.RequestLanguages           3        14                None                               None                               None
 cbss.RequestStates              6        15                Zustände cbss request              États cbss request                 cbss request states
 changes.ChangeTypes             6        14                Änderungsarten                     Änderungsarten                     Change Types
 checkdata.Checkers              19       49                Datentests                         Tests de données                   Data checkers
 clients.ClientEvents            10       19                Beobachtungskriterien              Évènements observés                Observed events
 clients.ClientStates            4        9                 Bearbeitungszustände Klienten      Etats bénéficiaires                Client states
 clients.KnownContactTypes       2        9                 Standard-Klientenkontaktarten      Types de contact connus            Known contact types
 contacts.CivilStates            7        27                Zivilstände                        Etats civils                       Civil states
 contacts.PartnerEvents          1        18                Beobachtungskriterien              Évènements observés                Observed events
 countries.PlaceTypes            23       16                None                               None                               None
 cv.CefLevel                     11       4                 CEF-Kategorien                     Niveaux CEF                        CEF levels
 cv.EducationEntryStates         3        25                None                               None                               None
 cv.HowWell                      5        12                None                               None                               None
 debts.AccountTypes              5        15                Kontoarten                         Kontoarten                         Account types
 debts.TableLayouts              5        55                Table layouts                      Table layouts                      Table layouts
 esf.ParticipationCertificates   1        50                Participation Certificates         Participation Certificates         Participation Certificates
 esf.StatisticalFields           12       32                ESF fields                         Champs FSE                         ESF fields
 excerpts.Shortcuts              1        21                Excerpt shortcuts                  Excerpt shortcuts                  Excerpt shortcuts
 households.MemberDependencies   3        15                Haushaltsmitgliedsabhängigkeiten   Dépendances de membres de ménage   Household Member Dependencies
 households.MemberRoles          9        11                Haushaltsmitgliedsrollen           Rôles de membres de ménage         Household member roles
 humanlinks.LinkTypes            13       27                Verwandschaftsarten                Types de parenté                   Parency types
 isip.ContractEvents             5        11                Beobachtungskriterien              Évènements observés                Observed events
 isip.OverlapGroups              2        12                Überlappungsgruppen                Groupes de chevauchement           Overlap groups
 jobs.CandidatureStates          5        21                Kandidatur-Zustände                États de candidatures              Candidature states
 ledger.CommonAccounts           23       32                Gemeinkonten                       Comptes communs                    Common accounts
 ledger.DC                       2        6                 Booking directions                 Booking directions                 Booking directions
 ledger.JournalGroups            5        20                Journalgruppen                     Groupes de journaux                Journal groups
 ledger.PeriodStates             2        14                Zustände                           États                              States
 ledger.TradeTypes               3        13                Handelsarten                       Types de commerce                  Trade types
 ledger.VoucherStates            4        14                Belegzustände                      Belegzustände                      Voucher states
 ledger.VoucherTypes             6        47                Belegarten                         Types de pièce                     Voucher types
 notes.SpecialTypes              1        12                Sondernotizarten                   Sondernotizarten                   Special note types
 notify.MailModes                5        24                Benachrichtigungsmodi              Benachrichtigungsmodi              Notification modes
 notify.MessageTypes             5        14                Message Types                      Message Types                      Message Types
 outbox.RecipientTypes           3        13                None                               None                               None
 pcsw.RefusalReasons             3        43                Ablehnungsgründe                   Raisons de refus                   Refusal reasons
 printing.BuildMethods           9        20                None                               None                               None
 properties.DoYouLike            5        10                None                               None                               None
 properties.HowWell              5        12                None                               None                               None
 sepa.AccountTypes               4        9                 Kontoarten                         Kontoarten                         Account types
 system.Genders                  2        8                 None                               None                               None
 system.PeriodEvents             3        9                 Beobachtungskriterien              Évènements observés                Observed events
 system.YesNo                    2        12                Ja oder Nein                       Oui ou non                         Yes or no
 uploads.Shortcuts               1        26                Upload shortcuts                   Upload shortcuts                   Upload shortcuts
 uploads.UploadAreas             2        9                 Upload-Bereiche                    Domaines de téléchargement         Upload areas
 users.UserTypes                 16       43                Benutzerarten                      Types d'utilisateur                User types
 xcourses.CourseRequestStates    7        15                Zustände Kursanfragen              États Demande de cours             Course Requests states
 xl.Priorities                   5        8                 Prioritäten                        Priorités                          Priorities
=============================== ======== ================= ================================== ================================== ===============================
<BLANKLINE>
