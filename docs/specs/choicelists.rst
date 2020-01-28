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
=============================== ================= ================================== ================================== ===============================
 name                            preferred_width   de                                 fr                                 en
------------------------------- ----------------- ---------------------------------- ---------------------------------- -------------------------------
 about.TimeZones                 4                 Zeitzonen                          Zeitzonen                          Time zones
 addresses.AddressTypes          20                Adressenarten                      Types d'adresses                   Address types
 addresses.DataSources           24                Datenquellen                       Sources de données                 Data sources
 aids.AidRegimes                 18                None                               None                               None
 aids.ConfirmationStates         11                Hilfebestätigungszustände          Hilfebestätigungszustände          Aid confirmation states
 aids.ConfirmationTypes          49                Hilfebescheinigungsarten           Types de confirmation d'aide       Aid confirmation types
 art61.Subsidizations            14                Subsidizations                     Subsidiations                      Subsidizations
 beid.BeIdCardTypes              82                eID-Kartenarten                    Types de carte eID                 eID card types
 beid.ResidenceTypes             20                Einwohnerregister                  Titres de séjour                   Resident registers
 cal.AccessClasses               31                None                               None                               None
 cal.DisplayColors               7                 None                               None                               None
 cal.DurationUnits               8                 None                               None                               None
 cal.EntryStates                 14                Kalendereintrag-Zustände           Kalendereintrag-Zustände           Entry states
 cal.EventEvents                 8                 Beobachtungskriterien              Évènements observés                Observed events
 cal.GuestStates                 12                Anwesenheits-Zustände              Anwesenheits-Zustände              Presence states
 cal.PlannerColumns              6                 None                               None                               None
 cal.Recurrencies                20                None                               None                               None
 cal.ReservationStates           4                 Zustände                           États                              States
 cal.TaskStates                  9                 Aufgaben-Zustände                  Aufgaben-Zustände                  Task states
 cal.Weekdays                    10                None                               None                               None
 cal.YearMonths                  9                 None                               None                               None
 cbss.ManageActions              12                None                               None                               None
 cbss.QueryRegisters             8                 None                               None                               None
 cbss.RequestLanguages           14                None                               None                               None
 cbss.RequestStates              15                Zustände cbss request              États cbss request                 cbss request states
 changes.ChangeTypes             14                Änderungsarten                     Änderungsarten                     Change Types
 checkdata.Checkers              49                Datentests                         Tests de données                   Data checkers
 clients.ClientEvents            19                Beobachtungskriterien              Évènements observés                Observed events
 clients.ClientStates            9                 Bearbeitungszustände Klienten      Etats bénéficiaires                Client states
 clients.KnownContactTypes       9                 Standard-Klientenkontaktarten      Types de contact connus            Known contact types
 contacts.CivilStates            27                Zivilstände                        Etats civils                       Civil states
 contacts.PartnerEvents          18                Beobachtungskriterien              Évènements observés                Observed events
 countries.PlaceTypes            16                None                               None                               None
 cv.CefLevel                     4                 CEF-Kategorien                     Niveaux CEF                        CEF levels
 cv.EducationEntryStates         25                None                               None                               None
 cv.HowWell                      12                None                               None                               None
 debts.AccountTypes              15                Kontoarten                         Kontoarten                         Account types
 debts.TableLayouts              55                Table layouts                      Table layouts                      Table layouts
 esf.ParticipationCertificates   50                Participation Certificates         Participation Certificates         Participation Certificates
 esf.StatisticalFields           32                ESF fields                         Champs FSE                         ESF fields
 excerpts.Shortcuts              21                Excerpt shortcuts                  Excerpt shortcuts                  Excerpt shortcuts
 households.MemberDependencies   15                Haushaltsmitgliedsabhängigkeiten   Dépendances de membres de ménage   Household Member Dependencies
 households.MemberRoles          11                Haushaltsmitgliedsrollen           Rôles de membres de ménage         Household member roles
 humanlinks.LinkTypes            27                Verwandschaftsarten                Types de parenté                   Parency types
 isip.ContractEvents             11                Beobachtungskriterien              Évènements observés                Observed events
 isip.OverlapGroups              12                Überlappungsgruppen                Groupes de chevauchement           Overlap groups
 jobs.CandidatureStates          21                Kandidatur-Zustände                États de candidatures              Candidature states
 ledger.CommonAccounts           32                Gemeinkonten                       Comptes communs                    Common accounts
 ledger.JournalGroups            20                Journalgruppen                     Groupes de journaux                Journal groups
 ledger.PeriodStates             14                Zustände                           États                              States
 ledger.TradeTypes               13                Handelsarten                       Types de commerce                  Trade types
 ledger.VoucherStates            14                Belegzustände                      Belegzustände                      Voucher states
 ledger.VoucherTypes             47                Belegarten                         Types de pièce                     Voucher types
 notes.SpecialTypes              12                Sondernotizarten                   Sondernotizarten                   Special note types
 notify.MailModes                24                Benachrichtigungsmodi              Benachrichtigungsmodi              Notification modes
 notify.MessageTypes             14                Message Types                      Message Types                      Message Types
 outbox.RecipientTypes           13                None                               None                               None
 pcsw.RefusalReasons             43                Ablehnungsgründe                   Raisons de refus                   Refusal reasons
 printing.BuildMethods           20                None                               None                               None
 properties.DoYouLike            10                None                               None                               None
 properties.HowWell              12                None                               None                               None
 sepa.AccountTypes               9                 Kontoarten                         Kontoarten                         Account types
 system.Genders                  8                 None                               None                               None
 system.PeriodEvents             9                 Beobachtungskriterien              Évènements observés                Observed events
 system.YesNo                    12                Ja oder Nein                       Oui ou non                         Yes or no
 uploads.Shortcuts               26                Upload shortcuts                   Upload shortcuts                   Upload shortcuts
 uploads.UploadAreas             9                 Upload-Bereiche                    Domaines de téléchargement         Upload areas
 users.UserTypes                 43                Benutzerarten                      Types d'utilisateur                User types
 xcourses.CourseRequestStates    15                Zustände Kursanfragen              États Demande de cours             Course Requests states
 xl.Priorities                   8                 Prioritäten                        Priorités                          Priorities
=============================== ================= ================================== ================================== ===============================
<BLANKLINE>
