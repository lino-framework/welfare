.. doctest docs/specs/choicelists.rst
   
===========================
Choicelists in Lino Welfare
===========================

.. doctest initializations:

    >>> from lino import startup
    >>> startup('lino_welfare.projects.eupen.settings.doctests')
    >>> from lino.api.doctest import *
    
This document is an overview on the choicelists used in Lino Welfare.

Choicelists are "hard-coded" tables. They are not stored in the
database but in the source code or the local configuration.

.. contents::
   :depth: 2
   :local:


Overview
========

Here are the choicelists used in Lino Welfare (click on their internal
name to read the documentation):

.. py2rst::

    from lino.core.kernel import CHOICELISTS
    for cls in sorted(CHOICELISTS.values(), key=lambda a: str(a)):
        print("- {0} (:class:`{1} <{2}.{3}>`)".format(
            cls.verbose_name_plural or cls.verbose_name, 
            cls, cls.__module__, cls.__name__))

.. tested, but not visible to reader:

    >>> from lino.core.kernel import choicelist_choices
    >>> for value, text in choicelist_choices():
    ...     print("%s : %s" % (value, str(text)))
    ... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
    about.TimeZones : Time zones
    accounts.AccountTypes : Kontoarten
    accounts.CommonAccounts : Gemeinkonten
    addresses.AddressTypes : Adressenarten
    addresses.DataSources : Datenquellen
    aids.AidRegimes : AidRegimes
    aids.ConfirmationStates : Hilfebestätigungszustände
    aids.ConfirmationTypes : Hilfebescheinigungsarten
    art61.Subsidizations : Subsidizations
    beid.BeIdCardTypes : eID-Kartenarten
    beid.CivilStates : Zivilstände
    beid.ResidenceTypes : Einwohnerregister
    cal.AccessClasses : AccessClasses
    cal.DurationUnits : DurationUnits
    cal.EntryStates : Termin-Zustände
    cal.EventEvents : Beobachtungskriterien
    cal.GuestStates : Gast-Zustände
    cal.PlannerColumns : PlannerColumns
    cal.Recurrencies : Recurrencies
    cal.TaskStates : Aufgaben-Zustände
    cal.Weekdays : Weekdays
    cbss.ManageActions : ManageActions
    cbss.QueryRegisters : QueryRegisters
    cbss.RequestLanguages : RequestLanguages
    cbss.RequestStates : Zustände
    changes.ChangeTypes : Änderungsarten
    checkdata.Checkers : Datentests
    clients.ClientEvents : Beobachtungskriterien
    clients.ClientStates : Bearbeitungszustände Klienten
    clients.KnownContactTypes : Standard-Klientenkontaktarten
    contacts.PartnerEvents : Beobachtungskriterien
    countries.PlaceTypes : PlaceTypes
    cv.CefLevel : CEF-Kategorien
    cv.EducationEntryStates : EducationEntryStates
    cv.HowWell : HowWell
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
    ledger.FiscalYears : Geschäftsjahre
    ledger.JournalGroups : Journalgruppen
    ledger.PeriodStates : Zustände
    ledger.TradeTypes : Handelsarten
    ledger.VoucherStates : Zustände
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
    xcourses.CourseRequestStates : Zustände


