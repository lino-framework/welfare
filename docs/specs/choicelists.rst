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

Here are the choicelists used in Lino Welfare (click on their internal
name to read the documentation):

>>> from lino.core.kernel import choicelist_choices
>>> for value, text in choicelist_choices():
...     print(u"{} : {}".format(value, text))
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
about.TimeZones : Zeitzonen
addresses.AddressTypes : Adressenarten
addresses.DataSources : Datenquellen
aids.AidRegimes : AidRegimes
aids.ConfirmationStates : Hilfebestätigungszustände
aids.ConfirmationTypes : Hilfebescheinigungsarten
art61.Subsidizations : Subsidizations
beid.BeIdCardTypes : eID-Kartenarten
beid.ResidenceTypes : Einwohnerregister
cal.AccessClasses : AccessClasses
cal.DisplayColors : DisplayColors
cal.DurationUnits : DurationUnits
cal.EntryStates : Kalendereintrag-Zustände
cal.EventEvents : Beobachtungskriterien
cal.GuestStates : Anwesenheits-Zustände
cal.PlannerColumns : PlannerColumns
cal.Recurrencies : Recurrencies
cal.ReservationStates : Zustände
cal.TaskStates : Aufgaben-Zustände
cal.Weekdays : Weekdays
cal.YearMonths : YearMonths
cbss.ManageActions : ManageActions
cbss.QueryRegisters : QueryRegisters
cbss.RequestLanguages : RequestLanguages
cbss.RequestStates : Zustände cbss request
changes.ChangeTypes : Änderungsarten
checkdata.Checkers : Datentests
clients.ClientEvents : Beobachtungskriterien
clients.ClientStates : Bearbeitungszustände Klienten
clients.KnownContactTypes : Standard-Klientenkontaktarten
contacts.CivilStates : Zivilstände
contacts.PartnerEvents : Beobachtungskriterien
countries.PlaceTypes : PlaceTypes
cv.CefLevel : CEF-Kategorien
cv.EducationEntryStates : EducationEntryStates
cv.HowWell : HowWell
debts.AccountTypes : Kontoarten
debts.TableLayouts : Table layouts
esf.ParticipationCertificates : Participation Certificates
esf.StatisticalFields : ESF fields
excerpts.Shortcuts : Excerpt shortcuts
households.MemberDependencies : Haushaltsmitgliedsabhängigkeiten
households.MemberRoles : Haushaltsmitgliedsrollen
humanlinks.LinkTypes : Verwandschaftsarten
isip.ContractEvents : Beobachtungskriterien
isip.OverlapGroups : Überlappungsgruppen
jobs.CandidatureStates : Kandidatur-Zustände
ledger.CommonAccounts : Gemeinkonten
ledger.JournalGroups : Journalgruppen
ledger.PeriodStates : Zustände
ledger.TradeTypes : Handelsarten
ledger.VoucherStates : Zustände Beleg
ledger.VoucherTypes : Belegarten
notes.SpecialTypes : Sondernotizarten
notify.MailModes : Benachrichtigungsmodi
notify.MessageTypes : Message Types
outbox.RecipientTypes : RecipientTypes
pcsw.RefusalReasons : Ablehnungsgründe
printing.BuildMethods : BuildMethods
properties.DoYouLike : DoYouLike
properties.HowWell : HowWell
sepa.AccountTypes : Kontoarten
system.Genders : Genders
system.PeriodEvents : Beobachtungskriterien
system.YesNo : Ja oder Nein
uploads.Shortcuts : Upload shortcuts
uploads.UploadAreas : Upload-Bereiche
users.UserTypes : Benutzerarten
xcourses.CourseRequestStates : Zustände Kursanfragen
xl.Priorities : Prioritäten
