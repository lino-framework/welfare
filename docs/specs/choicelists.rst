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
about.TimeZones : about.TimeZones (Zeitzonen)
addresses.AddressTypes : addresses.AddressTypes (Adressenarten)
addresses.DataSources : addresses.DataSources (Datenquellen)
aids.AidRegimes : aids.AidRegimes
aids.ConfirmationStates : aids.ConfirmationStates (Hilfebestätigungszustände)
aids.ConfirmationTypes : aids.ConfirmationTypes (Hilfebescheinigungsarten)
art61.Subsidizations : art61.Subsidizations (Subsidizations)
beid.BeIdCardTypes : beid.BeIdCardTypes (eID-Kartenarten)
beid.ResidenceTypes : beid.ResidenceTypes (Einwohnerregister)
cal.AccessClasses : cal.AccessClasses
cal.DisplayColors : cal.DisplayColors
cal.DurationUnits : cal.DurationUnits
cal.EntryStates : cal.EntryStates (Kalendereintrag-Zustände)
cal.EventEvents : cal.EventEvents (Beobachtungskriterien)
cal.GuestStates : cal.GuestStates (Anwesenheits-Zustände)
cal.PlannerColumns : cal.PlannerColumns
cal.Recurrencies : cal.Recurrencies
cal.ReservationStates : cal.ReservationStates (Zustände)
cal.TaskStates : cal.TaskStates (Aufgaben-Zustände)
cal.Weekdays : cal.Weekdays
cal.YearMonths : cal.YearMonths
cbss.ManageActions : cbss.ManageActions
cbss.QueryRegisters : cbss.QueryRegisters
cbss.RequestLanguages : cbss.RequestLanguages
cbss.RequestStates : cbss.RequestStates (Zustände cbss request)
changes.ChangeTypes : changes.ChangeTypes (Änderungsarten)
checkdata.Checkers : checkdata.Checkers (Datentests)
clients.ClientEvents : clients.ClientEvents (Beobachtungskriterien)
clients.ClientStates : clients.ClientStates (Bearbeitungszustände Klienten)
clients.KnownContactTypes : clients.KnownContactTypes (Standard-Klientenkontaktarten)
contacts.CivilStates : contacts.CivilStates (Zivilstände)
contacts.PartnerEvents : contacts.PartnerEvents (Beobachtungskriterien)
countries.PlaceTypes : countries.PlaceTypes
cv.CefLevel : cv.CefLevel (CEF-Kategorien)
cv.EducationEntryStates : cv.EducationEntryStates
cv.HowWell : cv.HowWell
debts.AccountTypes : debts.AccountTypes (Kontoarten)
debts.TableLayouts : debts.TableLayouts (Table layouts)
esf.ParticipationCertificates : esf.ParticipationCertificates (Participation Certificates)
esf.StatisticalFields : esf.StatisticalFields (ESF fields)
excerpts.Shortcuts : excerpts.Shortcuts (Excerpt shortcuts)
households.MemberDependencies : households.MemberDependencies (Haushaltsmitgliedsabhängigkeiten)
households.MemberRoles : households.MemberRoles (Haushaltsmitgliedsrollen)
humanlinks.LinkTypes : humanlinks.LinkTypes (Verwandschaftsarten)
isip.ContractEvents : isip.ContractEvents (Beobachtungskriterien)
isip.OverlapGroups : isip.OverlapGroups (Überlappungsgruppen)
jobs.CandidatureStates : jobs.CandidatureStates (Kandidatur-Zustände)
ledger.CommonAccounts : ledger.CommonAccounts (Gemeinkonten)
ledger.JournalGroups : ledger.JournalGroups (Journalgruppen)
ledger.PeriodStates : ledger.PeriodStates (Zustände)
ledger.TradeTypes : ledger.TradeTypes (Handelsarten)
ledger.VoucherStates : ledger.VoucherStates (Zustände Beleg)
ledger.VoucherTypes : ledger.VoucherTypes (Belegarten)
notes.SpecialTypes : notes.SpecialTypes (Sondernotizarten)
notify.MailModes : notify.MailModes (Benachrichtigungsmodi)
notify.MessageTypes : notify.MessageTypes (Message Types)
outbox.RecipientTypes : outbox.RecipientTypes
pcsw.RefusalReasons : pcsw.RefusalReasons (Ablehnungsgründe)
printing.BuildMethods : printing.BuildMethods
properties.DoYouLike : properties.DoYouLike
properties.HowWell : properties.HowWell
sepa.AccountTypes : sepa.AccountTypes (Kontoarten)
system.Genders : system.Genders
system.PeriodEvents : system.PeriodEvents (Beobachtungskriterien)
system.YesNo : system.YesNo (Ja oder Nein)
uploads.Shortcuts : uploads.Shortcuts (Upload shortcuts)
uploads.UploadAreas : uploads.UploadAreas (Upload-Bereiche)
users.UserTypes : users.UserTypes (Benutzerarten)
xcourses.CourseRequestStates : xcourses.CourseRequestStates (Zustände Kursanfragen)
xl.Priorities : xl.Priorities (Prioritäten)
