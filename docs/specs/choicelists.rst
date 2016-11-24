===========================
Choicelists in Lino Welfare
===========================

.. How to test only this document:

    $ python setup.py test -s tests.SpecsTests.test_choicelists

    doctest initializations:

    >>> import lino
    >>> lino.startup('lino_welfare.projects.std.settings.doctests')
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

    from lino.core.choicelists import CHOICELISTS
    for cls in sorted(CHOICELISTS.values(), key=lambda a: str(a)):
        print("- {0} (:class:`{1} <{2}.{3}>`)".format(
            cls.verbose_name_plural or cls.verbose_name, 
            cls, cls.__module__, cls.__name__))

.. tested, but not visible to reader:

    >>> from lino.core.choicelists import choicelist_choices
    >>> for value, text in choicelist_choices():
    ...     print "%s : %s" % (value, unicode(text))
    ... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
    accounts.AccountTypes : AccountTypes
    addresses.AddressTypes : Address types
    addresses.DataSources : Data sources
    aids.AidRegimes : AidRegimes
    aids.ConfirmationStates : Aid confirmation states
    aids.ConfirmationTypes : Aid confirmation types
    art61.Subsidizations : Subsidizations
    beid.BeIdCardTypes : eID card types
    cal.AccessClasses : AccessClasses
    cal.DurationUnits : DurationUnits
    cal.EventEvents : Observed events
    cal.EventStates : Event states
    cal.GuestStates : Guest states
    cal.Recurrencies : Recurrencies
    cal.TaskStates : Task states
    cal.Weekdays : Weekdays
    cbss.ManageActions : ManageActions
    cbss.QueryRegisters : QueryRegisters
    cbss.RequestLanguages : RequestLanguages
    cbss.RequestStates : States
    changes.ChangeTypes : Change Types
    contacts.PartnerEvents : Observed events
    countries.PlaceTypes : PlaceTypes
    courses.CourseRequestStates : States
    cv.CefLevel : CEF levels
    cv.EducationEntryStates : EducationEntryStates
    cv.HowWell : HowWell
    debts.TableLayouts : Table layouts
    esf.ParticipationCertificates : Participation Certificates
    esf.StatisticalFields : ESF fields
    excerpts.Shortcuts : Excerpt shortcuts
    households.MemberDependencies : Household Member Dependencies
    households.MemberRoles : Household member roles
    humanlinks.LinkTypes : Parency types
    isip.ContractEvents : Observed events
    isip.OverlapGroups : Overlap groups
    jobs.CandidatureStates : Candidature states
    ledger.FiscalYears : Fiscal Years
    ledger.JournalGroups : Journal groups
    ledger.PeriodStates : States
    ledger.TradeTypes : Trade types
    ledger.VoucherStates : States
    ledger.VoucherTypes : Voucher types
    notes.SpecialTypes : Special note types
    notify.MailModes : Email notification modes
    notify.MessageTypes : Message Types
    outbox.RecipientTypes : RecipientTypes
    pcsw.CivilState : Civil states
    pcsw.ClientEvents : Observed events
    pcsw.ClientStates : Client states
    pcsw.RefusalReasons : Refusal reasons
    pcsw.ResidenceType : ResidenceType
    plausibility.Checkers : Plausibility checkers
    polls.PollStates : Poll States
    polls.ResponseStates : Response States
    printing.BuildMethods : BuildMethods
    properties.DoYouLike : DoYouLike
    properties.HowWell : HowWell
    sepa.AccountTypes : Account types
    system.Genders : Genders
    system.PeriodEvents : Observed events
    system.YesNo : Yes or no
    uploads.Shortcuts : Upload shortcuts
    uploads.UploadAreas : Upload Areas
    users.UserTypes : User types


