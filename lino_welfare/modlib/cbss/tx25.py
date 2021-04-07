# -*- coding: UTF-8 -*-
# Copyright 2011-2018 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)


# This is a masterpiece of untransparent code, difficult to understand
# and maintain.  But I didn't find a better solution.  Maybe an XSLT
# expert might help us to rewrite this from scratch. The purpose is very
# simple: transform the content of a Tx25 response into a printable
# document.  A Tx25 response is a rather complex data structure with
# lots and lots of elements.  It contains a handler for every element
# type

# In case you need to understand, consult the source code of
# :class:`RowFactory`.


from django.db import models
from django.utils.translation import gettext as _
from django.utils.encoding import force_str

from lino.api import dd
from lino.utils import AttrDict, IncompleteDate

from etgen import html as xghtml
E = xghtml.E

from .utils import cbss2gender
from .models import reply_has_result
from .ui import ConfidentialResultsTable


def rn2date(rd):
    return IncompleteDate(
        int(rd.Century + rd.Year),
        int(rd.Month),
        int(rd.Day))


def deldate(n):
    if hasattr(n, 'DelDate'):
        return [' (' + str(_('until ')) +
                dd.dtos(rn2date(n.DelDate)) + ')']
    return []


# def simpleattr(n,name):
    # v = getattr(n,name,None)
    # if v:
        # return [ ', '+name+' ' + unicode(v)]
    # return []

def simpletype(v):
    return Info(xghtml.E.b(str(v)))


def boldstring(v):
    return Info(xghtml.E.b(str(v)))


def validate_element(c):
    if c is None:
        raise Exception("Invalid element %r" % c)


class Info(object):

    def __init__(self, *chunks):
        for c in chunks:
            validate_element(c)
        self.chunks = list(chunks)

    def addfrom(self, node, name, prefix=None, fmt=boldstring, suffix=''):
        v = getattr(node, name, None)
        if not v:
            return self
        if prefix is None:
            prefix = '%s ' % name
        else:
            prefix = force_str(prefix)
            if prefix and prefix[-1] not in ' :(':
                prefix += ': '
        if len(self.chunks):
            if not prefix.startswith(' '):
                prefix = ', ' + prefix
        self.chunks += [prefix] + fmt(v).chunks
        if suffix:
            self.chunks.append(force_str(suffix))
        return self

    def add_deldate(self, n):
        self.chunks += deldate(n)

    def add_codelabel(self, n):
        self.chunks += code_label(n).chunks
        # if hasattr(n,'Label'):
            # self.addfrom(n,'Label')
            # self.addfrom(n,'Code','(',simpletype,')')
        # else:
            # self.addfrom(n,'Code','[',boldstring,']')
        return self


def code_label(n):
    chunks = []
    if hasattr(n, 'Label') and n.Label:
        chunks.append(xghtml.E.b(n.Label))
    if hasattr(n, 'Code') and n.Code:
        chunks += [' (', n.Code, ')']
    return Info(*chunks)


# CodeLabel = code_label
# def CodeLabel(n):
    # info = Info()
    # return info


def NameType(n):
    info = Info()
    s = ' '.join([ln.Label for ln in n.LastName])
    info.chunks.append(xghtml.E.b(s))
    if hasattr(n, 'FirstName'):
        info.chunks.append(', ')
        s = ' '.join([fn.Label for fn in n.FirstName])
        info.chunks.append(s)
    return info


# def addinfo(node,name,prefix=None,fmt=simpletype,suffix=''):
    # v = getattr(node,name,None)
    # if not v: return []
    # if prefix is None:
        # prefix = ', %s ' % name
    # info = [force_str(prefix)] + fmt(v)
    # if suffix:
        # info.append(force_str(suffix))
    # return info
def DateType(n):
    return Info(dd.dtos(rn2date(n)))


def ForfeitureDateType(n):
    info = Info(dd.dtos(rn2date(n)))
    info.addfrom(n, 'Graphic', ' (', simpletype, ')')
    return info


def ExpiryDateType(n):
    info = Info(dd.dtos(rn2date(n)))
    info.addfrom(n, 'Graphic', ' (', simpletype, ')')
    return info


def TribunalType(n):
    return code_label(n)


def PlaceType(n):
    return code_label(n)


def SituationType111(n):
    return code_label(n)

def JustificationType(n):
    return code_label(n)

def GraphicPlaceType(n):
    info = CountryType(n.Country)
    info.addfrom(n, 'Graphic', '')
    # if hasattr(n,'Graphic'):
        # info.append(', graphic:'+n.Graphic)
    return info


def ForeignJudgementType(n):
    return GraphicPlaceType(n.Place)


def BelgianJudgementType(n):
    info = Info()
    info.addfrom(n, 'Tribunal', None, TribunalType)
    info.addfrom(n, 'Date', None, DateType)
    info.addfrom(n, 'Place', None, PlaceType)
    # info += TribunalType(n.Tribunal)
    # info += DateType(n.Date)
    # info += PlaceType(n.Place)
    return info


def CountryType(n):
    return code_label(n)


def LieuType(n):
    info = Info()
    if hasattr(n, 'Place1'):
        # info += code_label(n.Place1)
        info.addfrom(n, 'Place1', None, code_label)
    elif hasattr(n, 'Place2'):
        info.addfrom(n, 'Place2', None, GraphicPlaceType)
    else:
        place = n.Place3
        # info += GraphicPlaceType(place)
        info.addfrom(place, 'BelgianJudgement', '', BelgianJudgementType)
        info.addfrom(place, 'ForeignJudgement', '', ForeignJudgementType)
        # if hasattr(place,'BelgianJudgement'):
            # info += BelgianJudgementType(place.BelgianJudgement)
        # else:
            # info += ForeignJudgementType(place.ForeignJudgement)
    return info


def DiplomaticPostType(n):
    return code_label(n)


def TerritoryType(n):
    return code_label(n)


def ProvinceType(n):
    return code_label(n)


def IssuerType(n):
    # prefixes can be empty since this is a xs:choice
    info = Info().addfrom(n, 'Place', '', PlaceType)
    info.addfrom(n, 'Province', '', ProvinceType, ' (%s)' %
                 str(_("Province")))
    info.addfrom(n, 'PosteDiplomatique', '', DiplomaticPostType, ' (%s)' %
                 str(_("Diplomatic post")))
    return info


def ResidenceType(n):
    return code_label(n)


def NationalNumberType(n):
    info = Info().addfrom(n, 'NationalNumber', '')
    return info  # [n.NationalNumber]


def PartnerType(n):
    info = Info().addfrom(n, 'NationalNumber', '', NationalNumberType)
    # info.addfrom(n,'Name','',NameType)
    info.addfrom(n, 'Name', ' ', NameType)
    return info


def NotaryType(n):
    info = Info().addfrom(n, 'NameNotary')
    info.addfrom(n, 'Place', ' in ', PlaceType)
    info.addfrom(n, 'Country', ', ', CountryType)
    return info


def NotificationType(n):
    info = Info().addfrom(n, 'NotificationDate', None, DateType)
    info.addfrom(n, 'Place', ' in ', PlaceType)
    return info


def ReasonType(n):
    return code_label(n)


def CessationType(n):
    return code_label(n)


def DeclarationType(n):
    return code_label(n)


def Residence(n):
    info = Info().addfrom(n, 'Residence', '', ResidenceType)
    info.addfrom(n, 'Fusion', _("Fusion"))
    info.addfrom(n, 'Language', _("Language"))
    info.add_deldate(n)
    return info


def IT003(n):  # AscertainedLegalMainAddresses : Détermination de résidence
    # raise Exception(str(n))
    def InvestigationResultType(n):
        return code_label(n)
    info = Info().addfrom(n, 'InvestigationResult',
                          '', InvestigationResultType)
    info.addfrom(n, 'Graphic1', '')
    info.addfrom(n, 'Graphic2', '')
    info.add_deldate(n)
    return info


def IT005(n):  # AddressChangeIntention
    # raise Exception(str(n))
    info = Info().addfrom(n, 'OriginPlace', _('Move from '), PlaceType)
    info.addfrom(n, 'DestinationPlace', _('Move to '), PlaceType)
    info.add_deldate(n)
    return info


def IT006(n):
    info = Info()
    info.addfrom(n, 'Country', '', CountryType)
    info.addfrom(n, 'Graphic', ' ')
    info.add_deldate(n)
    return info


def IT008(n):  # ReturnPermissions
    info = Info()
    info.addfrom(n, 'Date', _("Date"), DateType)
    info.addfrom(n, 'ExpiryDate', _("expires "), DateType)
    info.add_deldate(n)
    return info


def IT011(n):  # Pseudonymes
    info = Info()
    info.addfrom(n, 'Name', '', NameType)
    info.add_deldate(n)
    return info


def IT013(n):
    info = Info()
    info.addfrom(n, 'ModificationType', '', ModificationTypeType)
    info.addfrom(n, 'Graphic', '')
    info.add_deldate(n)
    return info


def IT018(n):
    info = Info()
    info.addfrom(n, 'Address', '', AddressType)
    info.add_deldate(n)
    return info


def IT024(n):
    info = Info()
    info.add_deldate(n)
    return info


def TypeOfBurialType(n):
    return code_label(n)


def LegalRepresentativeType(n):
    info = Info()
    info.addfrom(n, 'NationalNumber', " ", NationalNumberType)
    info.addfrom(n, 'Graphic', " ")
    return info


def IT152(n):  # BurialModes, Mode de sépulture
    info = Info()
    info.addfrom(n, 'Date', _("Date"), DateType)
    info.addfrom(n, 'TypeOfBurial', "", TypeOfBurialType)
    info.addfrom(n, 'LegalRepresentative', "", LegalRepresentativeType)
    info.add_deldate(n)
    return info


def IT023(n):  # PostalAddressAbroad, Adresse postale à l'étranger
    info = Info()
    info.addfrom(n, 'Date', _("Date"), DateType)
    info.addfrom(n, 'Address', "", AddressType)
    info.add_deldate(n)
    return info


def TypeOfAbsenceType(n):
    return Info(E.b(n.Code))


def IT026(n):  # TemporaryAbsences
    info = Info()
    info.addfrom(n, 'Date', _("Date"), DateType)
    info.addfrom(n, 'TypeOfAbsence', "", TypeOfAbsenceType)
    info.addfrom(n, 'Graphic1', " ")
    info.addfrom(n, 'Graphic2', " ")
    info.add_deldate(n)
    return info


def IT028(n):
    info = Info()
    info.addfrom(n, 'LegalFact', '', code_label)
    info.addfrom(n, 'Graphic', '')
    info.addfrom(n, 'ExpiryDate', _("expires "), DateType)
    info.add_deldate(n)
    return info


def IT208(n):
    info = Info()
    # info.addfrom(n,'Date','',DateType)
    info.addfrom(n, 'PseudoNationalNumber', '')
    info.add_deldate(n)
    return info


def IT073(n):
    info = Info()
    info.addfrom(n, 'Category', '', CategoryType)
    info.addfrom(n, 'CertificateNumber', _("no."))
    info.add_deldate(n)
    return info


def IT074(n):
    info = Info()
    info.addfrom(n, 'SerialNumber')
    info.addfrom(n, 'IdentificationNumber')
    info.add_deldate(n)
    return info


def FiliationType(n):
    return code_label(n)


def ParentType(n):
    info = Info()
    info.addfrom(n, 'Name', '', NameType)
    info.addfrom(n, 'NationalNumber', ' (', NationalNumberType, ')')
    return info


def StreetType(n):
    # we don't print the code of streets
    info = Info()
    info.addfrom(n, 'Label', '')
    # info.addfrom(n,'NationalNumber',' (',NationalNumberType,')')
    return info
    # return code_label(n)


def IT020(n):
    def AddressType020(n):
        info = Info()
        info.addfrom(n, 'ZipCode', '')
        info.addfrom(n, 'Street', '', StreetType)
        info.addfrom(n, 'HouseNumber', _('no. '))
        info.addfrom(n, 'Box', ' ')
        return info
    info = Info()
    info.addfrom(n, "Address", '', AddressType020)
    return info


def IT110(n):
    # Filiation ascendante
    info = Info()
    info.addfrom(n, 'FiliationType', '', FiliationType)
    info.addfrom(n, 'Parent1', _('of '), ParentType)
    info.addfrom(n, 'Parent2', _('and '), ParentType)
    info.addfrom(n, 'ActNumber', _("Act no. "))
    info.addfrom(n, 'Place', _("in "), PlaceType)
    info.addfrom(n, 'Graphic', " ")
    info.add_deldate(n)
    return info


def IT111(n):
    # Statut de la personne représentée ou assistée

    info = Info()
    info.addfrom(n, 'Date', _("Date"), DateType)

    info.addfrom(n, 'Justification', '', JustificationType)
    info.addfrom(n, 'Situation', '', SituationType111)
    info.addfrom(n, 'Graphic', " ")
    info.add_deldate(n)

    return info


def IT113(n):  # Guardian : Personne qui représente ou assiste
    info = Info()
    info.addfrom(n, 'Date', _("Date"), DateType)
    info.addfrom(n, 'Status', _("Status"), code_label)
    info.addfrom(n, 'Justification', _("Justification"), code_label)
    info.addfrom(n, 'Place', _("in "), PlaceType)
    info.addfrom(n, 'Graphic', " ")
    info.addfrom(n, 'Country', " ", CountryType)
    info.add_deldate(n)
    return info


def IT140(n):
    info = Info().addfrom(n, 'Name', ' ', NameType)
    info.addfrom(n, 'NationalNumber', ' (', NationalNumberType, ')')
    # info += _(' as ')
    info.addfrom(n, 'FamilyRole', _('as '), code_label)
    info.addfrom(n, 'Housing', None, HousingType)
    info.add_deldate(n)
    return info


def IT141(n):
    info = Info()
    info.addfrom(n, 'Housing', None, HousingType)
    info.addfrom(n, 'FamilyRole', '', code_label)
    info.addfrom(n, 'Name', _('in family headed by '), NameType)
    info.addfrom(n, 'NationalNumber', ' (', NationalNumberType, ')')
    info.add_deldate(n)
    return info


def NationalityType(n):
    return code_label(n)


def IT213(n):  # Alias
    info = Info()
    info.addfrom(n, 'Name', '', NameType)
    info.addfrom(n, 'Nationality', None, NationalityType)
    info.addfrom(n, 'BirthDate', _(' born '), DateType)
    info.addfrom(n, 'BirthPlace', _(' in '))
    info.add_deldate(n)
    return info


def TypeOfLicenseType(n):
    return code_label(n)


def TypeOfLicenseType194(n):
    return code_label(n)


def DeliveryType206(n):
    v = getattr(n, 'Place', None)
    if v:
        return PlaceType(v)
    return CountryType(n.Country)


def DeliveryType194(n):
    info = Info().addfrom(n, 'Place', _('in '), PlaceType)
    info.addfrom(n, 'Label', '')
    info.addfrom(n, 'Code', ' (', simpletype, ')')
    # info.add_codelabel(n)
    # info += code_label(n)
    return info


def CategoryType(n):
    return code_label(n)


def GearBoxType(n):
    return code_label(n)


def MedicalType(n):
    return code_label(n)


def LicenseCategoriesType(n):
    info = Info()
    # raise Exception(str(n))
    # for cat in n.Category:
        # info.addfrom(cat,'Category',' ',CategoryType)
    info.chunks.append('/'.join([cat.Label for cat in n.Category]))
    # info += code_label(n)
    return info


def ForfeitureReasonType(n):
    return code_label(n)


def IT191(n):
    # info = code_label(n.TypeOfLicense)
    info = Info().addfrom(n, 'TypeOfLicense', '', TypeOfLicenseType)
    info.addfrom(n, 'LicenseNumber', _('no. '))
    info.addfrom(n, 'Place', _('delivered in '), PlaceType)
    info.addfrom(n, 'DeliveryCountry', ' (', CountryType, ')')
    info.addfrom(n, 'ForfeitureReason', None, ForfeitureReasonType)
    info.addfrom(n, 'ForfeitureDate', None, ForfeitureDateType)
    # info.append()
    # info.append(E.b(n.LicenseNumber))
    # info.append(', categories '
      # + ' '.join([cat.Label for cat in n.Categories.Category]))
    # info.append(_(' delivered in '))
    # info += code_label(n.Delivery.Place)
    info.add_deldate(n)
    return info


def IT194(n):
    info = Info().addfrom(n, 'TypeOfLicense', '', TypeOfLicenseType194)
    info.addfrom(n, 'Categories', _('categories '), LicenseCategoriesType)
    info.addfrom(n, 'LicenseNumber', _('no. '))
    info.addfrom(n, 'Delivery', _('delivered '), DeliveryType194)
    info.addfrom(n, 'GearBox', None, GearBoxType)
    info.addfrom(n, 'Medical', None, MedicalType)
    info.addfrom(n, 'ExpiryDate', _('expires '), ExpiryDateType)
    info.add_deldate(n)
    return info


def IT198(n):
    info = Info().addfrom(n, 'PermitNumber', _('no. '))
    info.addfrom(n, 'Categories', _('categories '), LicenseCategoriesType)
    info.addfrom(n, 'LicenseNumber', _('no. '))
    info.addfrom(n, 'Delivery', _('delivered '), DeliveryType194)
    info.addfrom(n, 'GearBox', None, GearBoxType)
    info.addfrom(n, 'Medical', None, MedicalType)
    info.addfrom(n, 'ExpiryDate', _('expires '), ExpiryDateType)
    info.add_deldate(n)
    return info


def TypeOfPassportType(n):
    return code_label(n)


def PassportIdentType(n):
    info = Info()
    info.addfrom(n, 'PassportType', _('type '), TypeOfPassportType)
    info.addfrom(n, 'PassportNumber', _('no. '))
    return info


def IT199(n):
    info = Info()
    # info.chunks.append('Number ')
    # info.chunks.append(E.b(n.PassportIdent.PassportNumber))
    # info.append(', status ')
    info.addfrom(n, 'Status', _("status"), code_label)
    info.addfrom(n, 'PassportIdent', '', PassportIdentType)
    info.addfrom(n, 'Issuer', _('issued by '), IssuerType)
    info.addfrom(n, 'RenewalNumber', _('renewal no. '), boldstring)
    info.addfrom(n, 'SerialNumber', _('serial no. '), boldstring)
    info.addfrom(n, 'SecondNumber', _('second no. '), boldstring)
    info.addfrom(n, 'ReplacementOf', _('replacement of '), boldstring)
    info.addfrom(n, 'AdditionTo', _('addition to '), boldstring)
    info.addfrom(n, 'ProductionDate', _('produced '), DateType)
    info.addfrom(n, 'ExpiryDate', _('expires '), DateType)
    # info.append(', type ')
    # info += code_label(n.PassportIdent.PassportType)
    # info.append(', expires ')
    # info.append(E.b(dd.dtos(rn2date(n.ExpiryDate))))
    # info.append(', delivered by ')
    # info += code_label(n.Issuer.PosteDiplomatique)
    # info.append(_(' renewal no. '))
    # info.append(E.b(n.RenewalNumber))
    info.add_deldate(n)
    return info


def HousingType(n):
    return code_label(n)


def ModificationTypeType(n):
    return code_label(n)


def AddressType(n):
    info = Info()
    # pd = n.Address.Address
    info.addfrom(n, 'Country', '', CountryType)
    # info.append(', ')
    info.addfrom(n, 'Graphic1', '')
    info.addfrom(n, 'Graphic2', '')
    info.addfrom(n, 'Graphic3', '')
    # info.append(E.b(pd.Graphic1))
    # info.append(', ')
    # info.append(E.b(pd.Graphic2))
    # info.append(', ')
    # info.append(E.b(pd.Graphic3))
    # info.addfrom(pd,'Graphic3')
    return info


def CertificateType(n):
    return code_label(n)


def IT200(n):
    info = Info().addfrom(n, 'PublicSecurityNumber', _('no. '))
    info.add_deldate(n)
    return info


def IT202(n):
    info = Info()
    info.addfrom(n, 'Graphic1', '')
    info.addfrom(n, 'Graphic2', '')
    info.addfrom(n, 'Limosa', '', LimosaType)
    info.add_deldate(n)
    return info


def LimosaType(n):
    info = Info()
    info.addfrom(n, 'Reason1', '', LimosaReasonType)
    info.addfrom(n, 'Reason2', '', LimosaReasonType)
    info.addfrom(n, 'NationalNumber', _('SSIN '), NationalNumberType)
    return info


def LimosaReasonType(n):
    return code_label(n)


def IT205(n):
    info = code_label(n)
    info.add_deldate(n)
    return info


def OrganizationType(n):
    return code_label(n)


def GeneralInfoType(n):
    info = code_label(n)
    info.addfrom(n, 'Organization', _("Organization"), OrganizationType)
    return info


def OrigineType(n):
    return Info().add_codelabel(n)


def AppealType(n):
    return code_label(n)


def StatusAppealType(n):
    return code_label(n)


def ProcedureType(n):
    info = Info()
    info.addfrom(n, 'Origine', None, OrigineType)
    info.addfrom(n, 'Reference')
    info.addfrom(n, 'Appeal', None, AppealType)
    info.addfrom(n, 'OpenClose', None, StatusAppealType)
    info.addfrom(n, 'NationalNumber', _('SSIN '), NationalNumberType)
    return info


def DecisionCancelledType(n):
    info = Info()
    info.addfrom(n, 'Date', None, DateType)
    info.addfrom(n, 'Reference')
    return info


def DelayLeaveGrantedType(n):
    info = Info()
    info.addfrom(n, 'Date', None, DateType)
    return info


def StrikingOutType(n):
    info = Info()
    info.addfrom(n, 'Reference')
    info.addfrom(n, 'OpenClose', None, OpenCloseType)
    info.addfrom(n, 'Status', None, StrikingStatusType)
    return info


def StrikingStatusType(n):
    return code_label(n)


def TerritoryLeftType(n):
    return code_label(n)


def OpenCloseType(n):
    return code_label(n)


def ProtectionType(n):
    info = code_label(n)
    info.addfrom(n, 'Reference')
    info.addfrom(n, 'Term')
    return info


def AdviceFromCGVSType(n):
    info = code_label(n)
    info.addfrom(n, 'Reference')
    return info


def ApplicationFiledType(n):
    info = code_label(n)
    info.addfrom(n, 'Place', _("in "), PlaceType)
    return info


def DecisionType206(n):
    # print 20150513, unicode(n).encode("ascii", errors="replace")
    info = code_label(n)
    info.addfrom(n, 'Reference', _("Reference"))
    info.addfrom(n, 'OpenClose', _("Open/Close"), OpenCloseType)
    info.addfrom(n, 'Comments')
    info.addfrom(n, 'Term')
    return info


def NotificationByDVZType(n):
    info = Info()
    info.addfrom(n, 'Place', _("in "), PlaceType)
    info.addfrom(n, 'Reference')
    return info


def NotificationByOrgType(n):
    info = Info()
    info.addfrom(n, 'Reference')
    return info


def AppealLodgedType(n):
    info = Info()
    info.addfrom(n, 'Reference')
    return info


def IT206(n):
    def Status(n):
        info = Info()
        info.addfrom(n, 'Status')
        return info

    info = Info()
    info.addfrom(n, 'GeneralInfo', '', GeneralInfoType)
    info.addfrom(n, 'Procedure', _("Procedure"), ProcedureType)
    info.addfrom(n, 'StrikingOut', None, StrikingOutType)
    info.addfrom(n, 'DecisionCancelled',
                 _("Decision cancelled"), DecisionCancelledType)
    info.addfrom(n, 'Protection', _("Protection"), ProtectionType)
    info.addfrom(n, 'DelayLeaveGranted', None, DelayLeaveGrantedType)
    info.addfrom(n, 'Escape', _("Escape"), Status)
    info.addfrom(n, 'UnrestrictedStay', None, Status)
    info.addfrom(n, 'ApplicationRenounced', _("Application renounced"), Status)
    info.addfrom(n, 'TerritoryLeft', _("Territory left"), TerritoryLeftType)
    info.addfrom(n, 'AdviceFromCGVS', None, AdviceFromCGVSType)
    info.addfrom(n, 'Decision', _("Decision"), DecisionType206)
    info.addfrom(n, 'ApplicationFiled',
                 _("Application filed"), ApplicationFiledType)
    info.addfrom(n, 'NotificationByDVZ', None, NotificationByDVZType)
    info.addfrom(n, 'NotificationByOrg', None, NotificationByOrgType)
    info.addfrom(n, 'AppealLodged', None, AppealLodgedType)
    info.add_deldate(n)
    return info


def InitiativeType(n):
    return code_label(n)


def SocialWelfareType(n):
    info = Info()
    info.addfrom(n, 'Place', _("in "), PlaceType)
    info.addfrom(n, 'Initiative', None, InitiativeType)
    info.add_deldate(n)
    return info


def RefugeeCentreType(n):
    return code_label(n)


def IT207(n):
    info = Info()
    info.addfrom(n, 'SocialWelfare',
                 _("Social Welfare Centre"), SocialWelfareType)
    info.addfrom(n, 'RefugeeCentre', _("Refugee Centre"), RefugeeCentreType)
    info.add_deldate(n)
    return info


def RegistrationRegisterType(n):
    return code_label(n)


def IT210(n):
    info = Info()
    info.addfrom(n, 'RegistrationRegister',
                 _("Registration register"), RegistrationRegisterType)
    info.add_deldate(n)
    return info


def IdentificationType(n):
    return code_label(n)


def IT211(n):
    info = Info()
    info.addfrom(n, 'TypeOfDocument', '', IdentificationType)
    info.add_deldate(n)
    return info


def ChoosenResidenceType(n):
    return code_label(n)


def IT212(n):
    info = Info().addfrom(n, 'Residence', None, ChoosenResidenceType)
    info.addfrom(n, 'Graphic', '')
    info.add_deldate(n)
    return info


def IT251(n):
    info = Info()
    info.add_deldate(n)
    return info


def IT192(n):
    info = Info().addfrom(n, 'Declaration', '', DeclarationType)
    info.addfrom(n, 'Place', _('in '), PlaceType)
    info.add_deldate(n)
    return info


HANDLERS = dict()


def register_it_handler(name, label, subname, itname):
    HANDLERS[name] = (label, subname, itname)

register_it_handler('WorkPermits', _("Work Permits"), 'WorkPermit', 'IT198')
register_it_handler(
    'PublicSecurityNumbers',
    _("Public Security Numbers"), 'PublicSecurityNumber', 'IT200')
register_it_handler('SpecialInfos', _("Special Infos"), 'SpecialInfo', 'IT202')
register_it_handler('RefugeeTypes', _("Refugee Types"), 'RefugeeType', 'IT205')
register_it_handler('StatusOfRefugee', _("Status of refugee"),
                    'StatusOfRefugee', 'IT206')
register_it_handler('Passports', _("Passports"), 'Passport', 'IT199')
register_it_handler(
    'OrganizationsInCharge',
    _("Organizations in charge"), 'OrganizationInCharge', 'IT207')
register_it_handler(
    'RegistrationRegisters',
    _("Registration registers"), 'RegistrationRegister', 'IT210')
register_it_handler('ChoosenResidences',
                    _("Choosen residences"), 'ChoosenResidence', 'IT212')
register_it_handler('OrganDonations', _("Organ Donations"),
                    'OrganDonation', 'IT192')
register_it_handler('ResidenceUpdateDates',
                    _("Residence Update Dates"), 'ResidenceUpdateDate',
                    'IT251')
register_it_handler('DocumentTypes', _("Document Types"),
                    'DocumentType', 'IT211')
register_it_handler('NameModifications',
                    _("Name Modifications"), 'NameModification', 'IT013')
register_it_handler('CountriesOfOrigin',
                    _("Countries Of Origin"), 'CountryOfOrigin', 'IT006')
register_it_handler('ReturnPermissions',
                    _("Return permissions"), 'ReturnPermission', 'IT008')
register_it_handler('AddressDeclarationAbroad',
                    _("Address Declaration Abroad"), 'Address', 'IT018')
register_it_handler('TemporaryRegistrations',
                    _("Inscriptions Temporaires"),
                    'TemporaryRegistration', 'IT028')
register_it_handler('SpecialRetirementCertificates',
                    _("Special Retirement Certificates"),
                    'SpecialRetirementCertificate',
                    'IT074')
register_it_handler('RetirementCertificates',
                    _("Retirement Certificates"), 'RetirementCertificate',
                    'IT073')
register_it_handler('Guardians',
                    _("Guardians"), 'Guardian', 'IT113')
register_it_handler('PseudoNationalNumbers',
                    _("Pseudo National Numbers"), 'PseudoNationalNumber',
                    'IT208')
register_it_handler('TemporaryAbsences',
                    _("Temporary absences"), 'TemporaryAbsence', 'IT026')
register_it_handler('BurialModes',
                    _("Burial modes"), 'BurialMode', 'IT152')
register_it_handler('PostalAddressAbroad',
                    _("Postal address abroad"), 'PostalAddressAbroad', 'IT023')
register_it_handler('ParentalAuthorities',
                    _("Parental authorities"), 'ParentalAuthority', 'IT111')


class RowFactory(object):

    # The result of a Tx25 consist of data rows, each of which has a
    # given type.  Consult the source code of this class to see how it
    # works.


    def start_group(self, group):
        self.current_group = group
        self.counter = 0

    def datarow(self, node, since, info):
        group = self.current_group
        self.counter += 1
        if node.__class__.__name__.startswith('IT'):
            itnum = node.__class__.__name__[2:]
        else:
            itnum = ''
        if hasattr(node, 'Type'):
            group += " " + node.Type
        # if hasattr(node,'Status'):
            # group += " " + unicode(node.Status)
        if hasattr(node, 'Structure'):
            group += " " + node.Structure
        return AttrDict(group=group,
                        counter=self.counter,
                        type=itnum,
                        since=rn2date(since),
                        info=E.p(*info.chunks))

    def get_it_handler(self, itnode):
        t = HANDLERS.get(itnode.__class__.__name__, None)
        if t is None:
            return t
        g, subname, itname = t
        it = globals().get(itname)

        def f(node, name):
            self.start_group(g)
            for n in getattr(node, subname):
                info = it(n)
                yield self.datarow(n, n.Date, info)
        return f

    def IT000(self, n, name):
        self.start_group(_("National Number"))
        n = n.NationalNumber
        info = Info(
            E.b(n.NationalNumber),
            ' (' + str(cbss2gender(n.Sex)) + ')')
        yield self.datarow(n, n.Date, info)

    def IT019(self, n, name):
        self.start_group(_("Address Change Declaration"))
        info = Info()

        def AddressType(n):
            info = Info()
            info.addfrom(n, 'Graphic', '')
            return info

        info.addfrom(n, 'Address', '', AddressType)
        info.add_deldate(n)
        yield self.datarow(n, n.Date, info)

    def FileOwner(self, fo, name):
        self.start_group(_("Residences"))
        for n in fo.Residences:
            info = Residence(n)
            yield self.datarow(n, n.Date, info)

    def AscertainedLegalMainAddresses(self, fo, name):
        # Détermination de résidence
        self.start_group(_("Ascertained Legal Main Addresses"))
        # raise Exception(str(fo))
        # raise Exception(repr([n for n in fo]))
        for n in fo.AscertainedLegalMainAddress:
            info = IT003(n)
            yield self.datarow(n, n.Date, info)

    def Pseudonyms(self, fo, name):
        self.start_group(_("Pseudonyms"))  # Pseudonymes
        for n in fo.Pseudonym:
            info = IT011(n)
            yield self.datarow(n, n.Date, info)

    def Aliases(self, fo, name):
        self.start_group(_("Aliases"))
        for n in fo.Alias:
            info = IT213(n)
            yield self.datarow(n, n.Date, info)

    def AddressChangeIntention(self, fo, name):
        self.start_group(
            _("Address Change Intention"))  # Intention de changer l'adresse
        for n in fo.Address:
            info = IT005(n)
            yield self.datarow(n, n.Date, info)

    def AddressReferences(self, fo, name):
        self.start_group(_("Address References"))  # Adresse de référence
        for n in fo.AddressReference:
            info = IT024(n)
            yield self.datarow(n, n.Date, info)

    def Names(self, node, name):
        self.start_group(_("Names"))
        # group = name
        for n in node.Name:
            info = Info().addfrom(n, 'Name', '', NameType)
            yield self.datarow(n, n.Date, info)

    def LegalMainAddresses(self, node, name):
        self.start_group(_("Legal Main Addresses"))
        for n in node.LegalMainAddress:
            yield self.datarow(n, n.Date, IT020(n))

    def ResidenceAbroad(self, node, name):  # IT022
        def ResidenceAbroadAddressType(n):
            info = Info('Address')
            info.addfrom(n, 'PosteDiplomatique', None, DiplomaticPostType)
            info.addfrom(n, 'Territory', ' ', TerritoryType)
            info.addfrom(n, 'Address', ' ', AddressType)
            return info
        self.start_group(_("Residence Abroad"))
        for n in node.ResidenceAbroad:
            info = Info()
            info.addfrom(n, 'Address', '', ResidenceAbroadAddressType)

            # info += code_label(n.Address.PosteDiplomatique)
            # info.append(', ')
            # info += code_label(n.Address.Territory)
            # info.append(', ')
            info.add_deldate(n)
            yield self.datarow(n, n.Date, info)

    def Nationalities(self, node, name):
        self.start_group(_("Nationalities"))
        for n in node.Nationality:
            info = code_label(n.Nationality)
            yield self.datarow(n, n.Date, info)

    def Occupations(self, node, name):
        self.start_group(_("Occupations"))
        for n in node.Occupation:
            info = code_label(n.Occupation)
            info.addfrom(n, 'SocialCategory', ' (SC ', code_label, ')')
            yield self.datarow(n, n.Date, info)

    def IT100(self, n, name):
        self.start_group(_("Birth Place"))
        info = Info()
        info.addfrom(n, 'Place1', _('in '), PlaceType)
        info.addfrom(n, 'Place2', _('in '), GraphicPlaceType)
        info.addfrom(n, 'ActNumber', _("Act no. "))
        info.addfrom(n, 'SuppletoryRegister')
        yield self.datarow(n, n.Date, info)

    def IT101(self, n, name):
        self.start_group(
            _("Declared Birth Date"))  # Date de naissance déclarée
        info = Info()
        info.addfrom(n, 'DeclaredBirthDate', '', DateType)
        info.addfrom(n, 'Certificate', '', CertificateType)
        info.add_deldate(n)
        yield self.datarow(n, n.Date, info)

    def Filiations(self, node, name):
        self.start_group(_("Filiations"))
        for n in node.Filiation:
            info = IT110(n)
            yield self.datarow(n, n.Date, info)

    def CivilStates(self, node, name):
        self.start_group(_("Civil States"))  # IT120
        for n in node.CivilState:
            info = code_label(n.CivilState)
            if hasattr(n, 'Spouse'):
                # info.append(' with ')
                # info += name2info(n.Spouse.Name)
                info.addfrom(n.Spouse, 'Name', _('with '), NameType)
                info.chunks.append(' (')
                info.chunks.append(n.Spouse.NationalNumber.NationalNumber)
                info.chunks.append(')')
            info.addfrom(n, 'Lieu', _('in '), LieuType)
            # info += LieuType(n.Lieu)
            info.addfrom(n, 'ActNumber', _("Act no. "))
            # info.addfrom(n,'ActNumber')
            info.addfrom(n, 'SuppletoryRegister')
            info.add_deldate(n)
            yield self.datarow(n, n.Date, info)

    def HeadOfFamily(self, node, name):
        self.start_group(_("Head Of Family"))
        for n in node.HeadOfFamily:
            info = IT140(n)
            yield self.datarow(n, n.Date, info)

    def FamilyMembers(self, node, name):
        self.start_group(_("Family Members"))
        for n in node.FamilyMember:
            info = IT141(n)
            yield self.datarow(n, n.Date, info)

    def DrivingLicensesOldModel(self, node, name):
        self.start_group(_("Driving Licenses Old Model"))
        for n in node.DrivingLicense:
            info = IT194(n)
            yield self.datarow(n, n.Date, info)

    def DrivingLicenses(self, node, name):
        self.start_group(_("Driving Licenses"))
        for n in node.DrivingLicense:
            info = IT191(n)
            yield self.datarow(n, n.Date, info)

    def IdentityCards(self, node, name):
        self.start_group(_("Identity Cards"))
        for n in node.IdentityCard:
            info = code_label(n.TypeOfCard)
            info.chunks.append(' ')
            info.chunks.append(_('no. '))
            info.chunks.append(E.b(n.CardNumber))
            info.addfrom(n, 'ExpiryDate', _('expires '), DateType)
            # info.chunks.append(E.b(dd.dtos(rn2date(n.ExpiryDate))))
            info.addfrom(n, 'Delivery', _('delivered in '), DeliveryType206)
            # info.chunks.append(', delivered in ')
            # info += code_label(n.Delivery.Place)
            yield self.datarow(n, n.Date, info)

    def LegalCohabitations(self, node, name):
        def CessationType(n):
            info = Info()
            info.addfrom(n, 'Reason', _("Reason"), ReasonType)
            info.addfrom(n, 'Place', _('in '), PlaceType)
            info.addfrom(n, 'Notification', _('in '), NotificationType)
            return info

        def DeclarationType(n):
            info = Info()
            info.addfrom(n, 'RegistrationDate', '', DateType)
            info.addfrom(n, 'Partner', _('with '), PartnerType)
            info.addfrom(n, 'Place', _('in '), PlaceType)
            info.addfrom(n, 'Notary', _('in '), NotaryType)
            return info

        self.start_group(_("Legal cohabitations"))
        for n in node.LegalCohabitation:
            info = Info()
            info.addfrom(n, 'Declaration', _("Declaration"), DeclarationType)
            info.addfrom(n, 'Cessation', _("Cessation"), CessationType)
            info.add_deldate(n)
            yield self.datarow(n, n.Date, info)

    def IT253(self, node, name):
        self.start_group(_("Creation Date"))
        n = node  # res.CreationDate
        info = Info()
        yield self.datarow(n, n.Date, info)

    def IT254(self, node, name):
        self.start_group(_("Last Update"))
        n = node  # res.LastUpdateDate
        info = Info()
        yield self.datarow(n, n.Date, info)


class RetrieveTIGroupsResult(ConfidentialResultsTable):

    master = 'cbss.RetrieveTIGroupsRequest'
    master_key = None
    column_names = 'group:18 type:5 since:14 info:50'

    @dd.displayfield(_("Group"))
    def group(self, obj, ar):
        if obj.counter == 1:
            return obj.group
        return ''

    @dd.displayfield(_("TI"))
    def type(self, obj, ar):
        if obj.counter == 1:
            return obj.type
        return ''

    @dd.virtualfield(models.DateField(_("Since")))
    def since(self, obj, ar):
        return obj.since

    @dd.displayfield(_("Info"))
    def info(self, obj, ar):
        return obj.info

    @classmethod
    def get_data_rows(self, ar):
        rti = ar.master_instance
        if rti is None:
            # print "20130425 rti is None"
            return
        self.check_permission(rti, ar)

        # if not ipr.status in (RequestStates.ok,RequestStates.fictive):
        # if not rti.status in (RequestStates.ok,RequestStates.warnings):
            # return
        reply = rti.get_service_reply()
        if reply is None:
            # print "20130425 reply is None"
            return
        # print "20130425 ok"
        reply_has_result(reply)

        res = reply.rrn_it_implicit

        rf = RowFactory()
        for name, node in res:
            # print 20130425, name, node.__class__
            m = getattr(rf, node.__class__.__name__, None)
            if m is None:
                m = rf.get_it_handler(node)
                if m is None:
                    raise Exception("No handler for %s (%s)"
                                    % (name, node.__class__.__name__))
            for row in m(node, name):
                yield row
