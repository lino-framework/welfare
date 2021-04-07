# -*- coding: UTF-8 -*-
# Copyright 2011-2014 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

"""
This fixture is for one-time use in a real case, 
and maybe as starting example for future similar cases.

Usage
-----

Load the fixture using the following command::

    python manage.py initdb std all_languages props pp2lino
    
The following variant might help to save time during testing::
    
    python manage.py initdb std few_countries pp2lino --noinput


Notes techniques import de données PP vers Lino
-----------------------------------------------



"""

import os
import sys
#~ ENCODING = sys.stdout.encoding
#~ import csv
import codecs
import datetime

from django.conf import settings

from lino.utils import dblogger
from lino.utils.instantiator import Instantiator
from lino.core.utils import resolve_model, full_model_name
from lino.utils.mdbtools import Loader
from lino.core.utils import is_valid_url, is_valid_email

from lino_xl.lib.countries.models import Place, Country
from lino_xl.lib.notes.models import Note
from lino.modlib.users.models import User
from lino_xl.lib.cal import models as cal
#~ from lino_xl.lib.cal.utils import EventStatus
from lino_xl.lib.properties import models as properties
from lino_welfare.modlib.jobs import models as jobs
from lino_welfare.modlib.isip import models as isip
from lino_welfare.modlib.pcsw.models import PersonGroup
from lino_welfare.modlib.contacts.models import Company, Person


CboStatutJuridique = {
    'Personne Physique': 3,
    'SPRL': 2,
    'ASBL': 9,
    'SA': 1,
    'NV': 1,
    'Publique': 8,
    'BVBA': 2,
    'SCRL': 4,
    'SIREAS': None,
}

"""
The following two dictionaries need manual work: 
replace full names by their uppercase ISO2 country code.
"""

CboNationalite = {
    1: "BE",
    2: "CG",  # "Congolais(e)",
    3: 'RU',  # "Russe",
    4: 'RW',  # "Rwandaise",
    5: 'CL',  # "Chilien(ne)",
    6: "FR",
    7: 'RO',  # "Roumain(e)",
    8: "CH",
    9: 'CO',  # "Colombien(ne)",
    11: 'UY',  # "Uruguayen (ne)",
    12: 'MA',  # "Marocain(ne)",
    14: 'DZ',  # u"Algérien(ne)",
    15: 'MU',  # "Mauricien(ne)",
    16: 'TG',  # "Togolais(e)",
    17: None,  # u"Réfugié Politique",
    18: 'TR',  # "Turque",
    19: 'CM',  # "Camerounai (se)",
    20: 'PE',  # "Perouvien(ne)",
    21: 'MD',  # "Moldave(iene)",
    23: 'BI',  # "burundais(e)",
    24: 'SL',  # "Sierra Leonais(e)",
    25: 'MR',  # "Mauritanien(ne)",
    26: 'BR',  # u"Brésilien(ne)",
    27: 'PT',  # "Portugais(e)",
    28: 'LB',  # "libanais(e)",
    29: "DE",
    30: 'SY',  # "syrien(ne)",
    31: "GN",  # "Guinéen(ne)",
    32: 'LR',  # u"Libérien(ne)",
    33: "TN",
    34: 'NG',  # "Nigérian(nes)",
    35: 'UZ',  # u"ouzbékistan",
    36: 'BO',  # "bolivien(ne)",
    37: 'PL',  # "polonais(e)",
    38: 'SN',  # u"sénégalais(e)",
    39: "IR",  # "Iranien(ne)",
    40: 'IQ',  # "Iraquien(ne)",
    41: 'AM',  # "arménie",
    42: 'IT',  # "Italien(ne)",
    43: 'AO',  # "angolien(ne)",
    44: 'NE',  # "Nigerien(ne)",
    45: 'CN',  # "Chinnoise",
    46: 'BF',  # "burkina Faso",
    48: 'LA',  # "laotienne",
    49: 'CI',  # "ivoirien(ne)",
    50: u"US",
    51: 'GE',  # "georgien(ne)",
    52: 'GR',  # "grec",
    53: 'MK',  # "yougoslave",
    54: 'BA',  # u"bosnie-herzégovine",
    55: 'UA',  # "Ukrainien(ne)",
    56: 'EC',  # "Equatorien",
    57: 'PK',  # "pakistannais(e)",
    58: 'VN',  # "vietnamien(ne)",
    59: 'ID',  # u"indonésien(ne)",
    60: "Malgache",
    62: 'IN',  # "indien(ne)",
    63: 'AL',  # "albanais",
    64: 'ES',  # "Espagnol(e)",
    65: 'MK',  # "Macedoine",
    66: 'DJ',  # "Djiboutien(ne)",
    68: 'EG',  # "egyptien(ne)",
    69: "NL",
    70: 'KZ',  # "Kazakhstan",
    71: 'SO',  # "Somalien(ne)",
    72: "AF",
    73: 'CU',  # "Cubaine",
    74: 'TD',  # "tchad",
    75: 'GB',  # "Royaume-Uni",
    76: 'LT',  # "lituanienne ",
    77: 'KG',  # "kirghizistan",
    78: 'ET',  # "Ethiopie",
}

CboPays = {
    1: u"Afrique du Sud", 2: 'AL'  # u"Albanie"
    , 3: 'DZ'  # u"Algérie"
    , 4: 'DE'  # u"Allemagne"
    , 5: u"Andorre", 6: 'AO'  # u"Angola"
    # u"Argentine"
    # u"Arménie"
    # u"Australie"
    # u"Autriche"
    # u"Belgique"
    # u"Belize"
    # u"Bolivie"
    # u"Bosnie-Herzégovine"
    # u"Brésil"
    # u"Bulgarie"
    # u"Burkina"
    # u"Burundi"
    # u"Cambodge"
    # u"Cameroun"
    # u"Chili"
    # u"Chine"
    # u"Colombie"
    # u"Congo"
    # u"Cōte d'Ivoire"
    # u"Cuba"
    # u"Danemark"
    # u"République de Djibouti"
    # u"Dominique"
    # u"Egypte"
    # u"Equateur"
    # u"Espagne"
    # u"Estonie"
    # u"Etats-Unis"
    # u"Ethiopie"
    # u"Finlande"
    # u"France"
    # u"Géorgie"
    # u"Grčce"
    # u"Guatemala"
    # u"Guinée"
    # u"Inde"
    # u"Indonésie"
    # u"Iran"
    # u"Iraq"
    # u"Italie"
    # u"Kazakhstan"
    # u"Kirghizistan"
    # u"Laos"
    # u"Liban"
    # u"Lituanie"
    # u"Luxembourg"
    # u"Maroc"
    # u"Maurice"
    # u"Mauritanie"
    # u"Moldavie"
    # u"Monaco"
    # u"Niger"
    # u"Nigeria"
    # u"Ouzbékistan"
    # u"Pakistan"
    # u"Pays-Bas"
    # u"Pérou"
    # u"Pologne"
    # u"Portugal"
    # u"République centrafricaine"
    # u"République dominicaine"
    # u"Roumanie"
    # u"Russie"
    # u"Rwanda"
    # u"Sénégal"
    # u"Sierra Leone"
    # u"Somalie"
    # u"Suisse"
    # u"Syrie"
    # u"Tanzanie"
    # u"Tchad"
    # u"Togo"
    # u"Turquie"
    # u"Ukraine"
    # u"Uruguay"
    # u"Viźt Nam"
    # u"Yougoslavie"
    # u"Zaļre"
    # u"Afghanistan"
    # u"Uzbekistan"
    , 7: u"Antigua-et-Barbuda", 8: u"Arabie Saoudite", 9: 'AR', 10: 'AM', 11: 'AU', 12: 'AS', 13: u"Azerbaļdjan", 14: u"Bahamas", 15: u"Bahreļn", 16: u"Bangladesh", 17: u"Barbade", 18: u"Beiau", 19: 'BE', 20: 'BZ', 21: u"Bénin", 22: u"Bhoutan", 23: u"Biélorussie", 24: u"Birmanie", 25: 'BO', 26: 'BA', 27: u"Botswana", 28: 'BR', 29: u"Brunei", 30: 'BG', 31: 'BF', 32: 'BI', 33: 'KH', 34: 'CM', 35: u"Canada", 36: u"Cap-Vert", 37: 'CL', 38: 'CN', 39: u"Chypre", 40: 'CO', 41: u"Comores", 42: 'CG', 44: u"Cook (les īles)", 45: u"Corée du Nord", 46: u"Corée du Sud", 47: u"Costa Rica", 48: 'CI', 49: u"Croatie", 50: 'CU', 51: 'DK', 52: 'DJ', 53: 'DM', 54: 'EG', 55: u"Émirats arabes unis", 56: 'EC', 57: u"Erythrée", 58: 'ES', 59: 'EE', 60: 'US', 61: 'ET', 62: u"Fidji", 63: 'FI', 64: 'FR', 65: u"Gabon", 66: u"Gambie", 67: 'GE', 68: u"Ghana", 69: 'GR', 70: u"Grenade", 71: 'GT', 72: "GN", 73: u"Guinée-Bissao", 74: u"Guinée équatoriale", 75: u"Guyana", 76: u"Haļti", 77: u"Honduras", 78: u"Hongrie", 79: 'IN', 80: 'ID', 81: "IR", 82: 'IQ', 83: u"Irlande", 84: u"Islande", 85: u"Israėl", 86: 'IT', 87: u"Jamaļque", 88: u"Japon", 89: u"Jordanie", 90: 'KZ', 91: u"Kenya", 92: 'KG', 93: u"Kiribati", 94: u"Koweļt", 95: 'LA', 96: u"Lesotho", 97: u"Lettonie", 98: 'LB', 99: u"Libéria", 100: u"Libye", 101: u"Liechtenstein", 102: 'LT', 103: 'LU', 104: u"Macédoine", 105: u"Madagascar", 106: u"Malaisie", 107: u"Malawi", 108: u"Maldives", 109: u"Mali", 110: u"Malte", 111: 'MA', 112: u"Marshall", 113: 'MU', 114: 'MR', 115: u"Mexique", 116: u"Micronésie", 117: 'MD', 118: 'MC', 119: u"Mongolie", 120: u"Mozambique", 121: u"Namibie", 122: u"Nauru", 123: u"Népal", 124: u"Nicaragua", 125: 'NE', 126: 'NG', 127: u"Niue", 128: u"Norvčge", 129: u"Nouvelle-Zélande", 130: u"Oman", 131: u"Ouganda", 132: 'UZ', 133: 'PK', 134: u"Panama", 135: u"Papouasie - Nouvelle Guin", 136: u"Paraguay", 137: 'NL', 138: 'PE', 139: u"Philippines", 140: 'PL', 141: 'PT', 142: u"Qatar", 143: 'CF', 144: 'DO', 145: u"République tchčque", 146: 'RO', 147: u"Royaume-Uni", 148: 'RU', 149: 'RW', 150: u"Saint-Christophe-et-Niévč", 151: u"Sainte-Lucie", 152: u"Vatican", 153: u"Saint-Vincent-et-les Gren", 154: u"Salomon", 155: u"Salvador", 156: u"Samoa occidentales", 157: u"Sao Tomé-et-Principe", 158: 'SN', 159: u"Seychelles", 160: 'SL', 161: u"Singapour", 162: u"Slovaquie", 163: u"Slovénie", 164: 'SO', 165: u"Soudan", 166: u"Sri Lanka", 167: u"Sučde", 168: 'CH', 169: u"Suriname", 170: u"Swaziland", 171: 'SY', 172: u"Tadjikistan", 173: 'TZ', 174: 'TD', 175: u"Thaļlande", 176: 'TG', 177: u"Tonga", 178: u"Trinité-et-Tobago", 179: u"TN", 180: u"Turkménistan", 181: 'TR', 182: u"Tuvalu", 183: 'UA', 184: 'UY', 185: u"Vanuatu", 186: u"Venezuela", 187: 'VN', 188: u"Yémen", 189: 'MK', 190: 'ZRCD', 191: u"Zambie", 192: u"Zimbabwe", 193: 'AF', 194: 'UZ'
}


def k2iso(dd, k, ddname):
    if not k:
        return None
    k = int(k)
    if k == 0:
        return None
    country_id = dd.get(k)
    if country_id is None:
        dblogger.warning("Unknown %s id %s", ddname, k)
        return None
    if len(country_id) == 2:
        return country_id
    if len(country_id) == 4 and country_id == country_id.upper():
        return country_id
    dblogger.warning("Invalid %s code %s -> %r", ddname, k, country_id)


def nation2iso(k):
    return k2iso(CboNationalite, k, 'CboNationalite')


def pays2iso(k):
    return k2iso(CboPays, k, 'CboPays')


def code2user(pk, offset=0):
    if not pk:
        return None
    pk = int(pk) + offset
    try:
        return User.objects.get(id=pk)
    except User.DoesNotExist:
        dblogger.warning("Unkown user %r", pk)


def phase2group(ph):
    if not ph:
        return
    try:
        return PersonGroup.objects.get(name=ph)
    except PersonGroup.DoesNotExist:
        pass

#~ def get_contracttype(pk):
    #~ if pk == 0:
        #~ return
    #~ try:
        #~ ct = ContractType.objects.get(pk=pk)
    #~ except ContractType.DoesNotExist:
        #~ dblogger.warning("ContractType %r does not exist?!",pk)
        #~ return None
    #~ return ct


def get_by_id(model, pk, offset=0, warn=True):
    if not pk:
        return None
    pk = int(pk)
    if pk == 0:
        return None
    try:
        return model.objects.get(pk=pk + offset)
    except model.DoesNotExist:
        if warn:
            dblogger.warning("%s %r does not exist?!",
                             full_model_name(model), pk)
        return None


EVENTS = {}


OFFSET_USER_ISP = 100
OFFSET_PERSON = 1000
OFFSET_JOBPROVIDER = 3000
#~ """
#~ Both CboTypeContrat and CboTypeMiseEmplois go to Lino's ContractType table.
#~ The following offset is added to CboTypeContrat keys.
#~ Must be > item count of CboTypeMiseEmplois.
#~ """
#~ OFFSET_CONTRACT_TYPE_CPAS = 100
#~ assert OFFSET_CONTRACT_TYPE_CPAS > len(CboTypeMiseEmplois)

#~ """
#~ Both TBMiseEmplois and TBTypeDeContratCPAS go to Lino's Contract table.
#~ The following offset is added to TBTypeDeContratCPAS keys.
#~ Must be > record count of TBMiseEmplois.
#~ """
#~ OFFSET_CONTRACT_CPAS = 2000


def unused_get_or_create_job(provider, contract_type, job_type, sector, function):
    try:
        #~ if provider_id:
        return jobs.Job.objects.get(provider=provider,
                                    contract_type=contract_type,
                                    type=job_type,
                                    sector=sector,
                                    function=function)
        #~ else:
            #~ return Job.objects.get(provider__isnull=True,contract_type__id=contract_type_id)
    except jobs.Job.DoesNotExist:
        if provider is None:
            name = '%s(interne)' % function
        else:
            name = '%s@%s' % (function, provider)
        job = jobs.Job(
            provider=provider,
            contract_type=contract_type,
            type=job_type,
            name=name,
            sector=sector,
            function=function
        )
        job.full_clean()
        job.save()
        return job


class LinoMdbLoader(Loader):

    "Base for all Loaders in this module"
    mdb_file = settings.SITE.legacy_data_path


class PlaceLoader(LinoMdbLoader):

    """
    Converts rows from CboCommuneCodePostal to Place instances.
    """
    table_name = 'CboCommuneCodePostal'
    model = Place
    headers = u"""
    IDCommuneCodePostal Commune CodePostal
    """.split()

    def row2obj(self, row):
        pk = int(row['IDCommuneCodePostal'])
        kw = {}
        kw.update(id=pk)
        kw.update(name=row['Commune'])
        kw.update(zip_code=row['CodePostal'])
        kw.update(country=Country.objects.get(pk='BE'))
        yield self.model(**kw)


class NotesLoader(LinoMdbLoader):

    """
    Converts rows from TBJournal to Note instances.
    """
    table_name = 'TBJournal'
    model = Note
    headers = u"""
    IDJournal DateJournal JournalClient IDClient
    """.split()
    last_date = None

    def row2obj(self, row):
        pk = int(row['IDJournal'])
        kw = {}
        kw.update(id=pk)
        txt = row['JournalClient']
        if txt:
            if len(txt) > 200:
                kw.update(body=txt)
            else:
                kw.update(subject=txt)
            d = self.parsedate(row['DateJournal'])
            if d:
                self.last_date = d
            else:
                d = self.last_date
                #~ d = datetime.date.today()
                # ~ dblogger.warning("TBJournal #%s : date was empty",pk)
            kw.update(date=d)
            idclient = int(row['IDClient']) + OFFSET_PERSON
            kw.update(person_id=idclient)
            #~ kw.update(person=Person.objects.get(pk=idclient))
            yield self.model(**kw)


class UsersSGLoader(LinoMdbLoader):

    """
    Converts rows from TBASSG to User instances.
    """
    table_name = 'TBASSG'
    model = User
    headers = u"""
    IDASSSG TitreASSSG NomASSSG PrenomASSSG CodeASSSG TelASSSG StatutASSSG
    """.split()

    def row2obj(self, row):
        pk = int(row['IDASSSG'])
        kw = {}
        kw.update(id=pk)
        kw.update(title=row['TitreASSSG'])
        kw.update(first_name=row['PrenomASSSG'])
        kw.update(last_name=row['NomASSSG'])
        kw.update(username=row['CodeASSSG'])
        kw.update(phone=row['TelASSSG'])
        #~ kw.update(is_spis=False)
        st = row['StatutASSSG']
        if st == "Ouvert":
            kw.update(is_active=True)
        else:
            kw.update(is_active=False)
        yield self.model(**kw)


class UsersISPLoader(LinoMdbLoader):
    table_name = 'TBASISP'
    model = User
    headers = u"""
    IDASISP TitreASISP NomASISP PrenomASISP CodeASISP Tel StatutASISP
    """.split()

    def row2obj(self, row):
        pk = int(row['IDASISP'])
        kw = {}
        kw.update(id=pk + OFFSET_USER_ISP)
        kw.update(title=row['TitreASISP'])
        kw.update(first_name=row['PrenomASISP'])
        kw.update(last_name=row['NomASISP'])
        kw.update(username=row['CodeASISP'])
        kw.update(phone=row['Tel'])
        kw.update(integ_level=UserLevel.user)
        st = row['StatutASISP']
        if st == "Ouvert":
            kw.update(is_active=True)
        else:
            kw.update(is_active=False)
        yield self.model(**kw)


class JobProviderLoader(LinoMdbLoader):
    table_name = 'TBEndroitMiseAuTravail'

    model = jobs.JobProvider
    headers = u"""
    IDEndroitMiseAuTravail EndroitMiseAuTravail IDStatutJuridique 
    NumeroInitiativeEconomieSociale 
    AdresseSiegeSocial N Bte 
    IDCommuneCodePostal NONSS Tel Fax EMail GSM Banque NCompte 
    Titre NomContact PrénomContact Fonction Tel1 Fax1 EMail1 
    Remarque Internet 
    Titre2 NomContact2 PrénomContact2 Fonction2 Tel2 GSM2 Fax2 EMail2 
    Titre3 NomContact3 PrénomContact3 Fonction3 Tel3 GSM3 Fax3 EMail3
    """.split()

    def row2obj(self, row):
        kw = {}
        kw.update(id=int(row['IDEndroitMiseAuTravail']) + OFFSET_JOBPROVIDER)
        kw.update(name=row['EndroitMiseAuTravail'])
        companyType = CboStatutJuridique.get(row['IDStatutJuridique'], None)
        if companyType:
            kw.update(type=CompanyType.objects.get(id=companyType))
        # see contacts/fixtures/std.py

        #~ kw.update(street_prefix=row[u'Rue'])
        kw.update(street=row[u'AdresseSiegeSocial'])
        kw.update(street_no=row[u'N'])
        kw.update(street_box=row[u'Bte'])
        kw.update(phone=row[u'Tel'])
        kw.update(gsm=row[u'GSM'])
        kw.update(fax=row[u'Fax'])
        kw.update(remarks="""
        NumeroInitiativeEconomieSociale : %(NumeroInitiativeEconomieSociale)s
        NONSS : %(NONSS)s
        """ % row)
        url = row[u'Internet']
        if url:
            if not url.startswith('http'):
                url = 'http://' + url
            if is_valid_url(url):
                kw.update(url=url)
        kw.update(remarks=row[u'Remarque'])
        if is_valid_email(row[u'EMail']):
            kw.update(email=row[u'EMail'])
        yield self.model(**kw)


class PersonLoader(LinoMdbLoader):
    table_name = 'TBClient'

    model = Person  # resolve_model('contacts.Person')

    headers = [u'IDClient', u'DateArrivee', u'NumeroDossier',
               u'Titre', u'Nom', u'Prénom',
               u'Rue', u'Adresse', u'Numero', u'Boite',
               u'IDCommuneCodePostal', u'Tel1', u'Tel2', u'GSM1',
               u'GSM2', u'Email', u'DateNaissance', u'IDPays', u'IDNationalite',
               u'NumeroNational', u'Conjoint', u'NEnfant', u'IBIS', u'Sexe',
               u'Statut', u'DateFin', u'RISEQRIS', u'DateOctroi',
               u'MontantRISEQRIS', u'Qualification', u'Phase', u'PIIS',
               u'Tutorat', u'IDASISP', u'IDASSSG', u'Remarques', u'IDTokAns',
               u'RPE', u'Art 35', u'DateDebutArt35', u'DateFinArt35', u'ALE', u'Update',
               u'PermisDeTravail']

    def row2obj(self, row):
        kw = {}
        kw.update(id=int(row['IDClient']) + OFFSET_PERSON)
        title = row['Titre']
        if not title in ("Monsieur", "Madame"):
            kw.update(title=title)
        if row['Nom']:
            kw.update(last_name=row['Nom'])
        else:
            kw.update(last_name="?")

        kw.update(gender=row['Sexe'])

        #~ sex = row['Sexe']
        #~ if sex == "M"
            #~ kw.update(sex='M')
        #~ elif sex == "F"
            #~ kw.update(sex='F')
        #~ else:
            #~ kw.update(sex='M')
        kw.update(first_name=row[u'Prénom'])
        kw.update(street_prefix=row[u'Rue'])
        kw.update(street=row[u'Adresse'])
        kw.update(street_no=row[u'Numero'])
        kw.update(street_box=row[u'Boite'])
        kw.update(gesdos_id=row[u'NumeroDossier'])
        kw.update(phone=row[u'Tel1'])
        kw.update(gsm=row[u'GSM1'])

        kw.update(birth_country_id=pays2iso(row[u'IDPays']))
        kw.update(nationality_id=nation2iso(row[u'IDNationalite']))
        kw.update(national_id=row[u'NumeroNational'])

        kw.update(coach1=get_by_id(User, row[u'IDASISP'], OFFSET_USER_ISP))
        kw.update(coach2=get_by_id(User, row[u'IDASSSG']))

        #~ kw.update(coach1=code2user(row[u'IDASISP'],OFFSET_USER_ISP))
        #~ kw.update(coach2=code2user(row[u'IDASSSG']))

        kw.update(group=phase2group(row[u'Phase']))

        city_id = row[u'IDCommuneCodePostal']
        if city_id:
            city_id = int(city_id)
            kw.update(city_id=city_id)

        if is_valid_email(row[u'Email']):
            kw.update(email=row[u'Email'])
        if row[u'DateNaissance']:
            kw.update(birth_date=self.parsedate(row[u'DateNaissance']))
        if row[u'DateArrivee']:
            kw.update(coached_from=self.parsedate(row[u'DateArrivee']))
        kw.update(remarks="""
        Tel2 : %(Tel2)s
        GSM2 : %(GSM2)s
        Remarques : %(Remarques)s
        """ % row)
        yield self.model(**kw)


class RechercheProfilLoader(LinoMdbLoader):
    table_name = 'TbRechercheProfil'
    model = jobs.Offer
    headers = u"""IDRechercheProfil 
    DateOuvertureSelection DateClotureSelection 
    DateDebutContrat 
    IDEndroitMiseAuTravail 
    IdQualification IDDetailFonction 
    DescriptionDeFonction
    HorairesDeTravail ProfilDemande Encadrement 
    OffreSpecifique Commentaires GestionArt60 
    StatutPoste""".split()

    def row2obj(self, row):
        kw = {}
        kw.update(id=int(row['IDRechercheProfil']))
        #~ kw.update(name=row['TypeMiseEmplois'])
        kw.update(sector=get_by_id(jobs.Sector, row['IdQualification']))
        kw.update(function=get_by_id(jobs.Function, row['IdQualification']))
        kw.update(
            provider=get_by_id(jobs.JobProvider, row['IDEndroitMiseAuTravail']))
        kw.update(selection_from=self.parsedate(row['DateOuvertureSelection']))
        kw.update(selection_until=self.parsedate(row['DateClotureSelection']))
        kw.update(start_date=self.parsedate(row['DateDebutContrat']))
        kw.update(remark=u"""
DescriptionDeFonction: %(DescriptionDeFonction)s
HorairesDeTravail: %(HorairesDeTravail)s
ProfilDemande: %(ProfilDemande)s
Encadrement: %(Encadrement)s
OffreSpecifique: %(OffreSpecifique)s
Commentaires: %(Commentaires)s
GestionArt60: %(GestionArt60)s
StatutPoste: %(StatutPoste)s""" % row)
        yield self.model(**kw)


SECTORS = dict()


class ListeFonctionLoader(LinoMdbLoader):
    table_name = 'CboListeFonction'
    model = 'cv.Sector'
    headers = u"""IdQualification Qualification Code filtre DetailFonction""".split(
    )

    def row2obj(self, row):
        kw = {}
        kw.update(id=int(row['IdQualification']))
        kw.update(name=row['Qualification'])
        kw.update(remark=row['DetailFonction'])
        obj = self.model(**kw)
        SECTORS[row['Code']] = obj
        yield obj


class DetailFonctionsLoader(LinoMdbLoader):
    table_name = 'CboDetailFonction'
    model = 'cv.Function'
    headers = u"""IDDetailFonction DetailFonction Code Secteur""".split()

    def row2obj(self, row):
        kw = {}
        kw.update(id=int(row['IDDetailFonction']))
        #~ kw.update(name='(' + row['Code'] + ') ' + row['DetailFonction'])
        if row['DetailFonction']:
            kw.update(name=row['DetailFonction'])
        else:
            kw.update(name="Function%d" % kw.get('id'))
        kw.update(sector=SECTORS.get(row['Code']))
        yield self.model(**kw)


class JobsContractTypeLoader(LinoMdbLoader):
    table_name = 'CboTypeMiseEmplois'
    model = 'jobs.ContractType'
    headers = u"""IDTypeMiseEmplois TypeMiseEmplois""".split()

    def row2obj(self, row):
        kw = {}
        kw.update(id=int(row['IDTypeMiseEmplois']))
        kw.update(name=row['TypeMiseEmplois'])
        yield self.model(**kw)


class CboSubsideLoader(LinoMdbLoader):
    table_name = 'CboSubside'
    model = 'jobs.JobType'
    headers = u"""IDSubside TypeSubside article""".split()

    def row2obj(self, row):
        kw = {}
        kw.update(id=int(row['IDSubside']))
        kw.update(name=row['TypeSubside'])
        kw.update(remark=row['article'])
        yield self.model(**kw)


class IsipContractTypeLoader(LinoMdbLoader):
    table_name = 'CboTypeContrat'
    model = 'isip.ContractType'
    headers = u"""IDTypeContrat TypeContratCPAS""".split()

    def row2obj(self, row):
        kw = {}
        kw.update(id=int(row['IDTypeContrat']))
        kw.update(name=row['TypeContratCPAS'])
        yield self.model(**kw)


class TBMiseEmploisLoader(LinoMdbLoader):
    table_name = 'TBMiseEmplois'
    #~ model = jobs.Contract
    headers = u"""
    IDMiseEmplois IDTypeMiseEmplois 
    MotifArt60 IDSubside IDETP 
    DebutContrat FinContrat TotalJourContrat 
    IDASSSG IDASISP 
    IDEndroitMiseAuTravail 
    Memo 
    IDClient 
    Durée Statut Montant DCAS DCSSS 
    IdQualification IDDetailFonction Bareme ArticleBudgetaireSPPPSalaire CoutAnnuel 
    Remarques DateCandidature
    """.split()

    def row2obj(self, row):
        #~ dblogger.info("statut = %s",row['Statut'])

        kw = {}
        kw.update(id=int(row['IDMiseEmplois']))

        job = None

        function = get_by_id(jobs.Function, row['IDDetailFonction'])
        sector = get_by_id(jobs.Sector, row['IdQualification'])
        person = get_by_id(Person, row[u'IDClient'], OFFSET_PERSON)
        provider = get_by_id(jobs.JobProvider,
                             row[u'IDEndroitMiseAuTravail'], OFFSET_JOBPROVIDER)
        ct = get_by_id(jobs.ContractType, row['IDTypeMiseEmplois'])
        jt = get_by_id(jobs.JobType, row['IDSubside'])
        #~ job = get_or_create_job(provider,ct,jt,sector,function)

        statut = row['Statut']
        if statut == "Fiche Candidature" or ct is None:
            if ct is not None:
                dblogger.warning(
                    "TBMiseEmplois %s : ignored contract type", row)
            kw.update(person=person)
            kw.update(function=function)
            kw.update(sector=sector)
            #~ kw.update(job=job)
            yield jobs.Wish(**kw)
        elif statut in (u'En Attente', u'En Cours', u'Terminé'):
            kw.update(applies_from=self.parsedate(row[u'DebutContrat']))
            kw.update(applies_until=self.parsedate(row[u'FinContrat']))
            kw.update(type=ct)
            #~ kw.update(job=job)
            kw.update(user=get_by_id(User, row[u'IDASISP'], OFFSET_USER_ISP))
            kw.update(user_asd=get_by_id(User, row[u'IDASSSG']))
            kw.update(provider=provider)
            kw.update(person=person)
            kw.update(remark=u"""
            Bareme: %(Bareme)s
            ArticleBudgetaireSPPPSalaire: %(ArticleBudgetaireSPPPSalaire)s
            """ % row)
            yield jobs.Contract(**kw)
        else:
            dblogger.warning(
                "Ignored TBMiseEmplois %s : unknown statut %r", row, statut)


class IsipContractLoader(LinoMdbLoader):
    table_name = 'TBTypeDeContratCPAS'
    model = 'isip.Contract'
    headers = u"""
    IDTypeDeContratCPAS IDTypeContrat DateDebut DateFin 
    ASCPAS ASISP Statut Evaluation IDClient DateSignature 
    TypePIIS NiveauEtude
    """.split()

    def row2obj(self, row):
        kw = {}
        kw.update(id=int(row['IDTypeDeContratCPAS']))
        #~ ctype = int(row['IDTypeContrat'])
        #~ if ctype:
            #~ kw.update(type=ContractType.objects.get(pk=ctype+ OFFSET_CONTRACT_TYPE_CPAS))
        kw.update(applies_from=self.parsedate(row[u'DateDebut']))
        kw.update(applies_until=self.parsedate(row[u'DateFin']))
        kw.update(person=get_by_id(Person, row[u'IDClient'], OFFSET_PERSON))

        ct = get_by_id(isip.ContractType, row['IDTypeContrat'])
        kw.update(type=ct)
        if not ct:
            dblogger.warning(
                "Ignored TBTypeDeContratCPAS %s : no contract type", row)
        else:
            yield self.model(**kw)

EVENT_STATI = {
    'RDV': 0,  # EventStatus.tentative,
    'Oui': 1,  # EventStatus.confirmed,
    'Non': 4,  # EventStatus.absent,
    'Retour': 2,  # EventStatus.cancelled,
    u'Reporté': 3,  # EventStatus.rescheduled,
}


class EventLoader(LinoMdbLoader):
    table_name = 'TBConvocationClient'
    model = cal.Event
    headers = u"""IDConvocationClient DateConvocationClient 
    TypeDeLettre HeureConvocation Venu FaireCourrier 
    IDASISP IDClient
    RemarquesConvocationClient
    NCourrier MessageAnnulation RDVMQ1 RDVMQ2""".split()

    def row2obj(self, row):
        if row['DateConvocationClient']:
            kw = {}
            kw.update(id=int(row['IDConvocationClient']))
            kw.update(created=datetime.datetime.now())
            kw.update(start_date=self.parsedate(row['DateConvocationClient']))
            #~ if row['HeureConvocation'].strip():
                #~ dblogger.warning("Ignored start time %r",row['HeureConvocation'])
            kw.update(start_time=self.parsetime(row['HeureConvocation']))
            kw.update(description=row['RemarquesConvocationClient'])
            kw.update(
                project=get_by_id(Person, row[u'IDClient'], OFFSET_PERSON))
            kw.update(user=get_by_id(User, row[u'IDASISP'], OFFSET_USER_ISP))
            #~ kw.update(coach2=get_by_id(User,row[u'IDASSSG']))
            kw.update(type=EVENTS.get(row['TypeDeLettre']))
            kw.update(status_id=EVENT_STATI.get(row['Venu']))
            kw.update(channel=EVENT_CHANNELS.get(row['FaireCourrier']))
            kw.update(outbox_id=row['NCourrier'])
            yield self.model(**kw)


def objects():

    if not settings.SITE.legacy_data_path:
        raise Exception(
            "You must specify the name of your .mdb file in `settings.SITE.legacy_data_path`!")

    phin = Instantiator('pcsw.PersonGroup', 'name').build
    yield phin('1')
    yield phin('2')
    yield phin('3')
    yield phin('4')
    yield phin('4b')
    #~ User = resolve_model('users.User')
    #~ for o in PersonLoader().load(): yield o
    #~ for k,v in CboTypeMiseEmplois.items():
        #~ yield ContractType(id=k,name=v)
    #~ for k,v in CboTypeContrat.items():
        #~ yield ContractType(id=k+OFFSET_CONTRACT_TYPE_CPAS,name=v)
    yield UsersSGLoader()
    yield User(username="root", level=UserLevel.expert, first_name="Root", last_name="Superuser")
    # seems that these 5 users are missing in the .mdb file:
    for i in (5, 8, 9, 10, 14):
        yield User(id=i, username="user%d" % i, is_active=False)
    yield UsersISPLoader()
    yield PlaceLoader()
    yield PersonLoader()
    for name in (u"1er Convocation", u"Suivi", u"Rdv Manqué",
                 u"Mise en demeure", u"Report", u"Attestation RIS",
                 u"Attestation EQRIS", u"Eval 1er", u"Eval Inter",
                 u"Eval Fin", u"Eval Inter SIAJ"):
        obj = cal.EventType(name=name)
        EVENTS[name] = obj
        yield obj

    yield EventLoader()

    yield CboSubsideLoader()
    yield ListeFonctionLoader()
    yield DetailFonctionsLoader()
    yield JobProviderLoader()
    yield RechercheProfilLoader()
    yield JobsContractTypeLoader()
    yield IsipContractTypeLoader()
    yield TBMiseEmploisLoader()
    yield IsipContractLoader()
    yield NotesLoader()

    #~ reader = csv.reader(open(,'rb'))
