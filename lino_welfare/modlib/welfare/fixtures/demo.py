# -*- coding: UTF-8 -*-
# Copyright 2008-2020 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

"""
Adds PCSW-specific demo data.
"""

from builtins import range
from builtins import next
import datetime
ONE_DAY = datetime.timedelta(days=1)

from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from lino.api import dd, rt
from lino.utils import i2d, Cycler
from lino_xl.lib.beid.mixins import BeIdCardTypes
from lino.utils.instantiator import Instantiator
from lino.core.utils import resolve_model
from lino.utils import mti
from lino.utils.ssin import generate_ssin

from lino_xl.lib.cal.choicelists import DurationUnits
# from lino_xl.lib.cal.utils import WORKDAYS

isip = dd.resolve_app('isip')
jobs = dd.resolve_app('jobs')
pcsw = dd.resolve_app('pcsw')
# uploads = dd.resolve_app('uploads')
contacts = dd.resolve_app('contacts')
countries = dd.resolve_app('countries')
reception = dd.resolve_app('reception')
cal = dd.resolve_app('cal')
cv = dd.resolve_app('cv')

from lino_xl.lib.clients.choicelists import ClientStates

Company = dd.resolve_model('contacts.Company')

#~ dblogger.info('Loading')

#~ def coaching_stories(state):
CT_GSS = 1
CT_INTEG = 2
CT_OTHER = 3
COACHING_STORIES = dict()
COACHING_STORIES[ClientStates.former] = Cycler(
    [
        (-1000, -500, True, CT_GSS)
    ], [
        (None, -60, True, CT_INTEG)
    ], [
        (-900, -430, False, CT_GSS),
        (-430, -200, True, CT_GSS),
    ])
COACHING_STORIES[ClientStates.coached] = Cycler(
    # start end primary
    [   # hintereinander betreut durch drei verschiedene Benutzer
        (-810, None, False, CT_GSS),
        (-800, -440, False, CT_INTEG),
        (-440, -210, False, CT_INTEG),
        (-210, None, True, CT_INTEG),
    ], [
        (-223, None, True, CT_GSS),
        (-220, None, False, CT_INTEG),
    ], [  # neu im DSBE, ASD noch nicht eingegeben
        (-10,  None, True, CT_INTEG),
    ], [
        (-810, None, True, CT_GSS),
        (-440, -230, False, CT_OTHER),
        (-230, None, False, CT_INTEG),
    ], [
        (-210, None, True, CT_GSS),
        (-160, None, False, CT_INTEG),
        (-50, None, False, CT_OTHER),
    ])


#~ auth = models.get_app('auth')
#~ projects = models.get_app('projects')
#~ contacts = models.get_app('contacts')
#~ notes = models.get_app('notes')
#~ properties = models.get_app('properties')
#char_pv = Instantiator('properties.CharPropValue').build
#CharPropValue = resolve_model('properties.CharPropValue')
# ~ from lino_xl.lib.properties import models as properties # CharPropValue, BooleanPropValue
#~ CHAR = ContentType.objects.get_for_model(properties.CharPropValue)
#BOOL = ContentType.objects.get_for_model(properties.BooleanPropValue)
#~ INT = ContentType.objects.get_for_model(properties.IntegerPropValue)
#~ def fill_choices(p,model):
    #~ i = 0
    #~ choices = p.choices_list()
    #~ if len(choices) == 0:
        #~ return
    #~ for owner in model.objects.all():
        #~ p.set_value_for(owner,choices[i])
        #~ if i + 1 < len(choices):
            #~ i += 1
        #~ else:
            #~ i = 0
#~ StudyContent = resolve_model('pcsw.StudyContent')
SECTORS_LIST = u"""
Agriculture & horticulture | Agriculture & horticulture | Landwirtschaft & Garten
Maritime | Maritime | Seefahrt
Medical & paramedical | Médical & paramédical | Medizin & Paramedizin
Construction & buildings| Construction & bâtiment | Bauwesen & Gebäudepflege
Tourism | Horeca | Horeca
Education | Enseignement | Unterricht
Cleaning | Nettoyage | Reinigung
Transport | Transport | Transport
Textile | Textile | Textil
Cultural | Culture | Kultur
Information Technology | Informatique | Informatik
Esthetical | Cosmétique | Kosmetik
Sales | Vente | Verkauf
Administration & Finance | Administration & Finance | Verwaltung & Finanzwesen
"""

SCHOOLS = Cycler([s.strip() for s in """
Darul Uloom Leicester
Emmanuel Christian School, Leicester
Leicester High School for Girls
Leicester Grammar School
Leicester Islamic Academy
Leicester Montessori School
Sathya Sai School
Stoneygate School
St Crispin's School

Leicester College
Gateway College
Regent College, Leicester
Wyggeston and Queen Elizabeth I College
""".splitlines()])
# taken from https://en.wikipedia.org/wiki/List_of_schools_in_Leicester

def flexible_user_type(s):
    if 'chatelet' in settings.SETTINGS_MODULE:
        return s[0:1] + "20"
    return s


def objects():

    ClientContactType = rt.models.clients.ClientContactType

    Person = resolve_model('contacts.Person')
    Company = resolve_model('contacts.Company')
    #~ Contact = resolve_model('contacts.Contact')
    Role = resolve_model('contacts.Role')
    RoleType = resolve_model('contacts.RoleType')
    Authority = resolve_model('users.Authority')
    User = settings.SITE.user_model
    #~ Country = resolve_model('countries.Country')
    Client = resolve_model('pcsw.Client')

    person = Instantiator(Person).build
    client = Instantiator(Client).build
    company = Instantiator(Company).build
    #~ contact = Instantiator(Contact).build
    role = Instantiator(Role).build
    #~ link = Instantiator(Link).build
    #~ exam_policy = Instantiator('isip.ExamPolicy').build

    Place = resolve_model('countries.Place')
    #~ Job = resolve_model('jobs.Job')
    #~ Place = settings.SITE.models.countries.Place
    StudyType = resolve_model('cv.StudyType')
    #~ Country = resolve_model('countries.Country')
    Property = resolve_model('properties.Property')

    eupen = Place.objects.get(name__exact='Eupen')
    #~ stvith = Place.objects.get(zip_code__exact='4780')
    stvith = Place.objects.get(name__in=('Sankt Vith', 'Saint-Vith'))
    kettenis = Place.objects.get(name__exact='Kettenis')
    vigala = Place.objects.get(name__exact='Vigala')
    ee = countries.Country.objects.get(pk='EE')
    be = belgium = countries.Country.objects.get(isocode__exact='BE')
    andreas = Person.objects.get(name__exact="Arens Andreas")
    annette = Person.objects.get(name__exact="Arens Annette")
    hans = Person.objects.get(name__exact="Altenberg Hans")
    ulrike = Person.objects.get(name__exact="Charlier Ulrike")
    erna = Person.objects.get(name__exact=u"Ärgerlich Erna")

    ## Coaching types
    # We use only abbreviated names in `CoachingType.name` because the
    # users usually know these abbrevs.

    kw = dd.str2kw('name', _("Colleague"))
    COLLEAGUE = cal.GuestRole(**kw)
    yield COLLEAGUE

    # id must match `isip.ContactBase.person_changed`
    ASD = rt.models.coachings.CoachingType(
        id=isip.COACHINGTYPE_ASD,
        does_integ=False,
        does_gss=True,
        eval_guestrole=COLLEAGUE,
        **dd.babelkw(
            'name',
            de="ASD",  # (Allgemeiner Sozialdienst)
            nl="ASD",  # (Algemene Sociale Dienst)
            fr="SSG",  # (Service social général)
            en="General",  # (General Social Service)
        ))
    yield ASD

    DSBE = rt.models.coachings.CoachingType(
        id=isip.COACHINGTYPE_DSBE,
        does_gss=False,
        does_integ=True,
        eval_guestrole=COLLEAGUE,
        **dd.babelkw(
            'name',
            de="DSBE",  # (Dienst für Sozial-Berufliche Eingliederung)
            fr="SI",  # Service intégration
            en="Integ",  # Integration service
        ))
    yield DSBE

    DEBTS = rt.models.coachings.CoachingType(
        does_gss=False,
        does_integ=False,
        **dd.babelkw(
            'name',
            de="Schuldnerberatung",
            fr="Médiation de dettes",
            en="Debts mediation",
        ))
    yield DEBTS

    melanie = person(first_name="Mélanie", last_name="Mélard",
                     email=settings.SITE.demo_email,
                     city=eupen, country='BE', gender=dd.Genders.female,
                     language='fr')

    ## newcomers : Melanie does not work with newcomers because she is
    ## the boss. Hubert does live consultations (no appointments). And
    ## Alicia does only appointments but no life
    ## consultations. Caroline and Judith do both.
    yield melanie
    melanie = User(
        username="melanie", partner=melanie, user_type='110',
        coaching_type=DSBE,
        newcomer_consultations=False, newcomer_appointments=False)
    yield melanie

    hubert = person(first_name=u"Hubert", last_name=u"Huppertz",
                    email=settings.SITE.demo_email,
                    city=kettenis, country='BE', gender=dd.Genders.male)
    yield hubert
    hubert = User(
        username="hubert", partner=hubert,
        user_type=flexible_user_type('100'),
        coaching_type=DSBE,
        newcomer_consultations=True, newcomer_appointments=False)
    yield hubert

    alicia = person(
        first_name=u"Alicia", last_name=u"Allmanns",
        email=settings.SITE.demo_email,
        city=kettenis, country='BE',
        # gender=dd.Genders.female,  # don't set gender
        language='fr')
    yield alicia
    alicia = User(
        username="alicia", partner=alicia,
        user_type=flexible_user_type('100'),
        coaching_type=DSBE,
        newcomer_consultations=True, newcomer_appointments=True)
    yield alicia

    theresia = person(first_name="Theresia", last_name="Thelen",
                      email=settings.SITE.demo_email,
                      city=eupen, country='BE', gender=dd.Genders.female)
    yield theresia
    theresia = User(username="theresia", partner=theresia, user_type='210')
    yield theresia

    nicolas = User(username="nicolas", user_type='')
    yield nicolas

    # yield Authority(user=alicia, authorized=hubert)
    # yield Authority(user=alicia, authorized=melanie)
    # yield Authority(user=hubert, authorized=melanie)
    yield Authority(user=hubert, authorized=theresia)
    yield Authority(user=alicia, authorized=theresia)
    yield Authority(user=melanie, authorized=theresia)

    caroline = User(
        username="caroline", first_name="Caroline", last_name="Carnol",
        user_type=flexible_user_type('200'),
        coaching_type=ASD,
        newcomer_consultations=True, newcomer_appointments=True)
    yield caroline

    obj = person(first_name="Judith", last_name="Jousten",
                 email=settings.SITE.demo_email,
                 city=eupen, country='BE', gender=dd.Genders.female)
    yield obj
    judith = User(
        username="judith", partner=obj,
        user_type=flexible_user_type('400'),
        coaching_type=ASD,
        newcomer_consultations=True, newcomer_appointments=True)
    yield judith

    yield User(
        username="patrick", first_name="Patrick",
        last_name="Paraneau", user_type='910',
        email=settings.SITE.demo_email)

    # for obj in rt.models.coachings.CoachingType.objects.all():
    #     yield auth.Team(**dd.babelkw('name', **field2kw(obj, 'name')))

    obj = cal.GuestRole(
        # email_template="Visitor.eml.html",
        **dd.babelkw(
            'name',
            de="Besucher",
            fr="Visiteur",
            en="Visitor",
            et="Külaline",
        ))
    yield obj
    settings.SITE.site_config.update(client_guestrole=obj)

    yield cal.GuestRole(**dd.babelkw('name',
                                     de=u"Vorsitzender",
                                     fr=u"Président",
                                     en=u"Chairman",
                                     et=u"Eesistuja",
                                 ))
    yield cal.GuestRole(**dd.babelkw('name',
                                     de=u"Schriftführer",
                                     fr=u"Greffier",
                                     en=u"Reporter",
                                     et=u"Sekretär",
                                 ))

    calendar = Instantiator('cal.EventType').build

    kw = dict(invite_client=False, is_appointment=False)
    kw.update(dd.str2kw('name', _("Consultations with client")))
    kw.update(dd.str2kw('event_label', _("Consultation")))
    # kw.update(dd.babelkw(
    #     'name',
    #     de="Visiten (ohne Verabredung)",
    #     fr="Consultations sans rendez-vous",
    #     en="Prompt consultation",
    #     et="Külaline",
    # ))
    obj = calendar(**kw)
    yield obj
    settings.SITE.site_config.update(prompt_calendar=obj)

    kw = dict(invite_client=True)
    kw.update(dd.str2kw("name", _("External meetings with client")))
    kw.update(dd.str2kw("event_label", _("External meeting")))
    yield calendar(**kw)

    kw = dict(invite_client=True)
    kw.update(dd.str2kw("name", _("Informational meetings")))
    kw.update(dd.str2kw("event_label", _("Informational meeting")))
    yield calendar(**kw)

    kw = dict(invite_client=False)
    kw.update(dd.str2kw("name", _("Internal meetings")))
    kw.update(dd.str2kw("event_label", _("Internal meeting")))
    yield calendar(**kw)
    # yield calendar(**dd.babelkw('name',
    #                             de=u"Versammlung intern",
    #                             fr=u"Réunions internes",
    #                             en=u"Internal meetings"))

    kw = dict(invite_client=False)
    kw.update(dd.str2kw("name", _("External meetings")))
    kw.update(dd.str2kw("event_label", _("External meeting")))
    yield calendar(**kw)
    # yield calendar(**dd.babelkw('name',
    #                             de=u"Versammlung extern",
    #                             fr=u"Réunions externes",
    #                             en=u"External meetings"))

    kw = dict(invite_client=False)
    kw.update(dd.str2kw("name", _("Private")))
    yield calendar(**kw)
    # yield calendar(**dd.babelkw('name',
    #                             de="Privat",
    #                             fr="Privé",
    #                             en="Private"))

    sector = Instantiator(cv.Sector).build
    for ln in SECTORS_LIST.splitlines():
        if ln:
            a = ln.split('|')
            if len(a) == 3:
                kw = dict(en=a[0], fr=a[1], de=a[2])
                yield sector(**dd.babelkw('name', **kw))

    horeca = cv.Sector.objects.get(pk=5)
    function = Instantiator(cv.Function, sector=horeca).build
    yield function(**dd.babelkw('name',
                             de=u"Kellner",
                             fr=u'Serveur',
                             en=u'Waiter',
                             ))
    yield function(**dd.babelkw('name',
                             de=u"Koch",
                             fr=u'Cuisinier',
                             en=u'Cook',
                             ))
    yield function(**dd.babelkw('name',
                             de=u"Küchenassistent",
                             fr=u'Aide Cuisinier',
                             en=u'Cook assistant',
                             ))
    yield function(**dd.babelkw('name',
                             de=u"Tellerwäscher",
                             fr=u'Plongeur',
                             en=u'Dishwasher',
                             ))

    contractType = Instantiator(jobs.ContractType, "ref",
                                exam_policy=3).build
    yield contractType('art60-7a',
                       **dd.babelkw('name',
                                 de=u"Sozialökonomie",
                                 fr=u'économie sociale',
                                 en=u'social economy',
                                 ))
    yield contractType('art60-7b',
                       **dd.babelkw('name',
                                 de=u"Sozialökonomie - majoré",
                                 fr=u'économie sociale - majoré',
                                 en=u'social economy - increased',
                                 ))
    yield contractType('art60-7c',
                       **dd.babelkw('name',
                                 de=u"mit Rückerstattung",
                                 fr=u'avec remboursement',
                                 en=u'social economy with refund',
                                 ))
    yield contractType('art60-7d',
                       **dd.babelkw('name',
                                 de=u"mit Rückerstattung Schule",
                                 fr=u'avec remboursement école',
                                 en=u'social economy school',
                                 ))
    yield contractType('art60-7e',
                       **dd.babelkw('name',
                                 de=u"Stadt Eupen",
                                 fr=u"ville d'Eupen",
                                 en=u'town',
                                 ))

    contractType = Instantiator(isip.ContractType, "ref",
                                exam_policy=1).build
    yield contractType("vsea", needs_study_type=True, **dd.babelkw(
        'name',
        de=u"VSE Ausbildung",
        fr=u"VSE Ausbildung",
        en=u"VSE Ausbildung",
    ))
    yield contractType("vseb", **dd.babelkw('name',
                                         de=u"VSE Arbeitssuche",
                                         fr=u"VSE Arbeitssuche",
                                         en=u"VSE Arbeitssuche",
                                         ))
    yield contractType("vsec", **dd.babelkw('name',
                                         de=u"VSE Lehre",
                                         fr=u"VSE Lehre",
                                         en=u"VSE Lehre",
                                         ))
    yield contractType("vsed",
                       needs_study_type=True,
                       **dd.babelkw('name',
                                 de=u"VSE Vollzeitstudium",
                                 fr=u"VSE Vollzeitstudium",
                                 en=u"VSE Vollzeitstudium",
                             ))
    yield contractType("vsee", **dd.babelkw('name',
                                         de=u"VSE Sprachkurs",
                                         fr=u"VSE Sprachkurs",
                                         en=u"VSE Sprachkurs",
                                         ))

    t = RoleType.objects.get(pk=4)  # It manager
    t.use_in_contracts = False
    t.save()

    #~ country = Instantiator('countries.Country',"isocode name").build
    #~ yield country('SUHH',"Soviet Union")
    #~ cpas = company(name=u"ÖSHZ Eupen",city=eupen,country=belgium)
    cpas = company(name=u"ÖSHZ Kettenis", city=kettenis, country=belgium)
    yield cpas
    bisa = company(name=u"BISA", city=eupen, country=belgium)
    yield bisa
    bisa_dir = role(company=bisa, person=annette, type=1)
    yield bisa_dir
    rcycle = company(name=u"R-Cycle Sperrgutsortierzentrum",
                     city=eupen, country=belgium)
    yield rcycle
    rcycle_dir = role(company=rcycle, person=andreas, type=1)
    yield rcycle_dir
    yield role(company=rcycle, person=erna, type=2)
    # IT manager : no contracts
    yield role(company=rcycle, person=ulrike, type=4)
    yield company(name=u"Die neue Alternative V.o.G.", city=eupen, country=belgium)
    proaktiv = company(name=u"Pro Aktiv V.o.G.", city=eupen, country=belgium)
    yield proaktiv
    proaktiv_dir = role(company=proaktiv, person=hans, type=1)
    # IT manager : no contracts
    yield role(company=proaktiv, person=ulrike, type=4)
    yield proaktiv_dir
    yield company(name=u"Werkstatt Cardijn V.o.G.", city=eupen, country=belgium)
    yield company(name=u"Behindertenstätten Eupen", city=eupen, country=belgium)
    yield company(name=u"Beschützende Werkstätte Eupen", city=eupen, country=belgium)

    kw = dd.str2kw('name', _("Health insurance"))
    cct = ClientContactType(**kw)
    yield cct
    kw = dict(client_contact_type=cct, country=belgium)
    #~ kw = dict(is_health_insurance=True,country=belgium)
    yield company(name="Alliance Nationale des Mutualités Chrétiennes", **kw)
    yield company(name="Mutualité Chrétienne de Verviers - Eupen", **kw)
    yield company(name="Union Nationale des Mutualités Neutres", **kw)
    yield company(name="Mutualia - Mutualité Neutre", **kw)
    yield company(name="Solidaris - Mutualité socialiste et syndicale de la province de Liège", **kw)

    fkw = dd.str2kw('name', _("Pharmacy"))  # Apotheke
    cct = rt.models.clients.ClientContactType.objects.get(**fkw)
    kw = dict(client_contact_type=cct, country=belgium, city=eupen)
    yield company(
        name="Apotheke Reul",
        street='Klosterstraße', street_no=20, **kw)
    yield company(
        name="Apotheke Schunck", street='Bergstraße', street_no=59, **kw)
    yield company(
        name="Pharmacies Populaires de Verviers",
        street='Aachener Straße', street_no=258, **kw)
    yield company(
        name="Bosten-Bocken A", street='Haasstraße', street_no=6, **kw)

    kw = dd.str2kw('name', _("Advocate"))
    cct = ClientContactType(**kw)
    yield cct
    kw = dict(client_contact_type=cct, country=belgium, city=eupen)
    yield company(name=u"Brüll Christine", street=u'Schilsweg', street_no=4, **kw)
    yield company(name=u"Brocal Catherine", street=u'Neustraße', street_no=115, **kw)
    yield company(name=u"Bourseaux Alexandre", street=u'Aachener Straße', street_no=21, **kw)
    yield company(name=u"Baguette Stéphanie", street=u'Gospertstraße', street_no=24, **kw)

    # Bailiff = Gerichtsvollzieher = Huissier de justice
    kw = dd.str2kw('name', _("Bailiff"))
    if dd.is_installed('debts'):
        kw.update(is_bailiff=True)
    cct = ClientContactType(**kw)
    yield cct
    kw = dict(client_contact_type=cct, country=belgium, city=eupen)
    yield company(name="Demarteau Bernadette",
                  street='Aachener Straße', street_no=25, **kw)
    kw.update(city=stvith)
    yield company(name="Schmitz Marc", street='Rodter Straße',
                  street_no=43, street_box="B", **kw)

    # Inkasso-Unternehmen
    kw = dd.str2kw('name', _("Debt collecting company"))
    if dd.is_installed('debts'):
        kw.update(is_bailiff=True)
    cct = ClientContactType(**kw)
    yield cct
    kw = dict(client_contact_type=cct, country=belgium, city=eupen)
    yield company(name="Cashback sprl",
                  street='Vervierser Straße', street_no=1, **kw)
    yield company(name="Money Wizard AS",
                  street='Neustraße', street_no=1, **kw)

    # settings.SITE.site_config.debts_bailiff_type = cct
    # yield settings.SITE.site_config

    def person2client(p, **kw):
        c = mti.insert_child(p, Client)
        for k, v in kw.items():
            setattr(c, k, v)
        c.client_state = ClientStates.coached
        c.save()
        return Client.objects.get(pk=p.pk)

    #~ luc = Person.objects.get(name__exact="Saffre Luc")
    #~ luc = person2client(luc,national_id = '680601 053-29')
    #~ luc.birth_place = 'Eupen'
    #~ luc.birth_date = '1968-06-01'
    #~ luc.birth_country = be
    #~ luc.full_clean()
    #~ luc.save()
    #~
    #~ ly = person(first_name="Ly",last_name="Rumma",
      #~ city=vigala,country='EE',
      #~ gender=dd.Genders.female)
    #~ yield ly
    #~ mari = person(first_name="Mari",last_name="Saffre",
      #~ city=vigala,country='EE',
      #~ gender=dd.Genders.female)
    #~ yield mari
    #~ iiris = person(first_name="Iiris",last_name="Saffre",
      #~ city=vigala,country='EE',
      #~ gender=dd.Genders.female)
    #~ yield iiris

    gerd = person(first_name="Gerd",
                  last_name="Gerkens", city=kettenis,
                  email=settings.SITE.demo_email,  # 'gerd@example.com'
                  country='BE', gender=dd.Genders.male)
    yield gerd
    yield role(company=cpas, person=gerd, type=4)

    # see :blogentry:`20111007`
    tatjana = client(
        first_name=u"Tatjana", last_name=u"Kasennova",
        #~ first_name=u"Татьяна",last_name=u"Казеннова",
        city=kettenis, country='BE',
        #~ national_id='1237',
        birth_place="Moskau",  # birth_country='SUHH',
        client_state=ClientStates.newcomer,
        #~ newcomer=True,
        gender=dd.Genders.female)
    yield tatjana

    michael = Person.objects.get(name__exact="Mießen Michael")
    jean = Person.objects.get(name__exact="Radermacher Jean")
    #~ yield cpas
    sc = settings.SITE.site_config
    sc.site_company = cpas
    sc.signer1 = michael
    sc.signer2 = jean
    yield sc
    yield role(company=cpas,
               person=michael,
               type=sc.signer1_function)
    yield role(company=cpas,
               person=jean,
               type=sc.signer2_function)

    bernard = Person.objects.get(name__exact="Bodard Bernard")

    kw = dd.str2kw('name', _("Employment office"))  # Arbeitsvermittler
    cct = ClientContactType(**kw)
    yield cct
    kw = dict(client_contact_type=cct, country=belgium, city=eupen)
    adg = company(name=u"Arbeitsamt der D.G.", **kw)
    adg.save()
    yield adg
    settings.SITE.site_config.job_office = adg
    yield settings.SITE.site_config
    adg_dir = role(company=adg, person=bernard, type=1)
    yield adg_dir

    kw = dd.str2kw('name', _("Physician"))  # Arzt
    if dd.is_installed('aids'):
        kw.update(can_refund=True)
    cct = ClientContactType(**kw)
    yield cct
    kw = dict(client_contact_type=cct, country=belgium, city=eupen)
    yield person(first_name="Waltraud", last_name="Waldmann", **kw)

    kw = dd.str2kw('name', _("Family doctor"))  # Hausarzt
    if dd.is_installed('aids'):
        kw.update(can_refund=True)
    cct = ClientContactType(**kw)
    yield cct
    kw = dict(client_contact_type=cct, country=belgium, city=eupen)
    yield person(first_name="Werner", last_name="Wehnicht", **kw)

    kw = dd.str2kw('name', _("Dentist"))
    if dd.is_installed('aids'):
        kw.update(can_refund=True)
    cct = ClientContactType(**kw)
    yield cct
    kw = dict(client_contact_type=cct, country=belgium,
              city=eupen, title="Dr.")
    yield person(first_name="Carmen", last_name="Castou", **kw)
    yield person(first_name="Walter", last_name="Waldmann", **kw)

    kw = dd.str2kw('name', _("Pediatrician"))
    if dd.is_installed('aids'):
        kw.update(can_refund=True)
    cct = ClientContactType(**kw)
    yield cct
    kw = dict(client_contact_type=cct, country=belgium,
              city=eupen, title="Dr.")
    yield person(first_name="Killian", last_name="Kimmel", **kw)

    # kw = dd.str2kw('name', _("Landlord"))  # Vermieter
    # if dd.is_installed('aids'):
    #     kw.update(can_refund=True)
    # cct = ClientContactType(**kw)
    # yield cct
    # kw = dict(client_contact_type=cct, country=belgium, city=eupen)
    # yield person(first_name="Vera", last_name="Veltz", **kw)
    # yield person(first_name="Vanessa", last_name="Veithen", **kw)

    #~ from django.core.exceptions import ValidationError
    # ~ # a circular reference: bernard is contact for company adg and also has himself as `job_office_contact`
    #~ try:
      #~ bernard.job_office_contact = adg_dir
      #~ bernard.clean()
      #~ bernard.save()
    #~ except ValidationError:
        #~ pass
    #~ else:
        #~ raise Exception("Expected ValidationError")

    DIRECTORS = (annette, hans, andreas, bernard)

    #~ USERS = Cycler(root,melanie,hubert,alicia)
    AGENTS = Cycler(melanie, hubert, alicia, judith)
    COACHINGTYPES = Cycler(rt.models.coachings.CoachingType.objects.filter(
        does_gss=False, does_integ=False))

    #~ CLIENTS = Cycler(andreas,annette,hans,ulrike,erna,tatjana)
    count = 0
    #~ for person in Person.objects.filter(gender__isnull=False):
    for person in Person.objects.exclude(gender=''):
        if not person.birth_date:  # not those from humanlinks
            if User.objects.filter(partner=person).count() == 0:
                if contacts.Role.objects.filter(person=person).count() == 0:
                    birth_date = settings.SITE.demo_date(-170 * count - 16 * 365)
                    national_id = generate_ssin(birth_date, person.gender)

                    client = person2client(person,
                                           national_id=national_id,
                                           birth_date=birth_date)
                    # youngest client is 16; 170 days between each client

                    count += 1
                    if count % 2:
                        client.client_state = ClientStates.coached
                    elif count % 5:
                        client.client_state = ClientStates.newcomer
                    else:
                        client.client_state = ClientStates.former

                    # Dorothée is three times in our database
                    if client.first_name == "Dorothée":
                        client.national_id = None
                        client.birth_date = ''

                    client.full_clean()
                    client.save()

    #~ CLIENTS = Cycler(Client.objects.filter(is_active=True,newcomer=False))
    CLIENTS = Cycler(
        Client.objects.filter(client_state=ClientStates.coached))

    #~ oshz = Company.objects.get(name=u"ÖSHZ Eupen")

    #~ project = Instantiator('projects.Project').build
    #~ note = Instantiator('notes.Note').build
    LanguageKnowledge = rt.models.cv.LanguageKnowledge
    Language = rt.models.languages.Language
    # langk = Instantiator('cv.LanguageKnowledge').build

    def langk(person=None, language=None, **kwargs):
        language = Language.objects.get(pk=language)
        try:
            obj = LanguageKnowledge.objects.get(
                person=person, language=language)
            for k, v in kwargs.items():
                setattr(obj, k, v)
        except LanguageKnowledge.DoesNotExist:
            obj = LanguageKnowledge(
                person=person, language=language, **kwargs)
        obj.full_clean()
        obj.save()
        return obj

    #~ prj = project(name="Testprojekt",company=oshz)
    #~ yield prj
    #~ yield note(user=user,project=prj,date=i2d(20091006),subject="Programmierung",company=oshz)

    #~ prj = project(name="Testprojekt",company=oshz)
    #~ yield prj
    #~ yield note(user=user,project=prj,date=i2d(20091007),subject="Anschauen",company=oshz)

    Note = resolve_model('notes.Note')
    USERS = Cycler(User.objects.all())
    SUBJECTS = Cycler(u"""
    Erstgespräch
    Versammlung beim AG
    Zwischenbericht
    Krisensitzung
    """.splitlines())

    for i in range(10):
        yield Note(user=USERS.pop(),
                   date=settings.SITE.demo_date(days=i),
                   subject=SUBJECTS.pop())

    schule = StudyType.objects.get(pk=1)
    # uni = StudyType.objects.get(pk=4)
    abi = u"Abitur"
    study = Instantiator('cv.Study').build

    gerd = CLIENTS.pop()
    luc = CLIENTS.pop()
    ly = CLIENTS.pop()
    mari = CLIENTS.pop()
    iiris = CLIENTS.pop()

    luc.card_number = '591413288107'
    luc.card_valid_from = i2d(20110819)
    luc.card_valid_until = i2d(20160819)
    luc.card_issuer = "Eupen"
    luc.card_type = BeIdCardTypes.belgian_citizen
    luc.save()
    luc.make_demo_picture()

    gerd.card_number = '123456789012'
    gerd.card_valid_from = i2d(20120819)
    gerd.card_valid_until = i2d(20130818)
    gerd.card_issuer = "Eupen"
    gerd.card_type = BeIdCardTypes.foreigner_c
    gerd.save()
    gerd.make_demo_picture()

    yield study(person=luc, type=schule, content=abi,
                start_date='19740901', end_date='19860630')
    yield study(person=gerd, type=schule, content=abi,
                start_date='19740901', end_date='19860630')

    yield langk(person=luc, language='ger', written='4', spoken='4')
    yield langk(person=gerd, language='ger', written='4', spoken='4')
    yield langk(person=mari, language='ger', written='2', spoken='4')
    yield langk(person=iiris, language='ger', written='0', spoken='4')
    yield langk(person=ly, language='ger', written='2', spoken='1')

    yield langk(person=luc, language='fre', written='4', spoken='3')
    yield langk(person=gerd, language='fre', written='4', spoken='3')

    yield langk(person=luc, language='eng', written='4', spoken='3')
    yield langk(person=gerd, language='eng', written='4', spoken='3')
    yield langk(person=ly, language='eng', written='3', spoken='3')

    yield langk(person=gerd, language='dut', written='3', spoken='3')

    yield langk(person=luc, language='est', written='3', spoken='3')
    yield langk(person=ly, language='est', written='4', spoken='4')
    yield langk(person=mari, language='est', written='3', spoken='4')
    yield langk(person=iiris, language='est', written='0', spoken='3')

    jobtype = Instantiator(jobs.JobType, 'name').build
    art607 = jobtype(u'Sozialwirtschaft = "majorés"')
    yield art607
    yield jobtype(u'Intern')
    yield jobtype(u'Extern (Öffentl. VoE mit Kostenrückerstattung)')
    yield jobtype(u'Extern (Privat Kostenrückerstattung)')
    #~ yield jobtype(u'VSE')
    yield jobtype(u'Sonstige')

    rcycle = mti.insert_child(rcycle, jobs.JobProvider)
    yield rcycle
    bisa = mti.insert_child(bisa, jobs.JobProvider)
    yield bisa
    proaktiv = mti.insert_child(proaktiv, jobs.JobProvider)
    yield proaktiv

    # jobs (Art.60-7)
    CSTATES = Cycler(jobs.CandidatureStates.objects())
    JOBS_CONTRACT_TYPES = Cycler(jobs.ContractType.objects.all())
    JTYPES = Cycler(jobs.JobType.objects.all())

    PROVIDERS = Cycler(jobs.JobProvider.objects.all())
    SECTORS = Cycler(cv.Sector.objects.all())
    FUNCTIONS = Cycler(cv.Function.objects.all())
    REMARKS = Cycler(
        _("A very hard job."),
        '',
        _("No supervisor. Only for independent people."), '', '', '')

    for i in range(8):
        f = FUNCTIONS.pop()
        yield jobs.Job(provider=PROVIDERS.pop(),
                       type=JTYPES.pop(),
                       contract_type=JOBS_CONTRACT_TYPES.pop(),
                       name=str(f),
                       remark=REMARKS.pop(),
                       sector=SECTORS.pop(), function=f)

    JOBS = Cycler(jobs.Job.objects.all())

    for i in range(40):
        yield jobs.Candidature(job=JOBS.pop(),
                               person=CLIENTS.pop(),
                               state=CSTATES.pop(),
                               date_submitted=settings.SITE.demo_date(-40 + i))

    # reset SECTORS and FUNCTIONS
    SECTORS = Cycler(cv.Sector.objects.all())
    FUNCTIONS = Cycler(cv.Function.objects.all())

    obj = jobs.Offer(
        name="Übersetzer DE-FR (m/w)",
        remark="""\
Wir sind auf der Suche nach einem Deutsch-Französich Übersetzer
(M/F) um einen Selbständigenr zu Geschäftsessen und kommerziellen
Termine zu begleiten. Sie übernehmen die Übersetzung von Gespräche
während kommerziellen Kontakte mit deutschen Kunden.
Es ist spontane und pünktliche Aufträge, den ganzen Tag, in
Eupen und/oder Deutschland.
Regelmäßigkeit: 1-2 Mal pro Monat, je nach Bedarf.
Flexibilität: die Termine sind je nach Kandidat anpassbar.""",
        provider=PROVIDERS.pop(),
        selection_from=settings.SITE.demo_date(-120),
        selection_until=settings.SITE.demo_date(-20),
        start_date=settings.SITE.demo_date(10),
        sector=SECTORS.pop(),
        function=FUNCTIONS.pop())
    yield obj

    # reset SECTORS and FUNCTIONS
    SECTORS = Cycler(cv.Sector.objects.all())
    FUNCTIONS = Cycler(cv.Function.objects.all())

    for i in range(30):
        yield jobs.Candidature(
            person=CLIENTS.pop(),
            state=CSTATES.pop(),
            date_submitted=settings.SITE.demo_date(-20 + i * 2),
            sector=SECTORS.pop(),
            function=FUNCTIONS.pop(),
        )

    COUNTRIES = Cycler(countries.Country.objects.all())
    COMPANIES = Cycler(Company.objects.all())

    # reset SECTORS and FUNCTIONS
    SECTORS = Cycler(cv.Sector.objects.all())
    FUNCTIONS = Cycler(cv.Function.objects.all())
    DURATIONS = Cycler([1, 2, 3, 6, 6, 9, 12, 12, 24, 24])  # months
    STATES = Cycler(cv.EducationEntryStates.items())

    for i in range(30):
        start_date = settings.SITE.demo_date(-1200 + i * 2)
        d = DURATIONS.pop()
        end_date = DurationUnits.months.add_duration(start_date, d)
        yield cv.Experience(
            person=CLIENTS.pop(),
            company=COMPANIES.pop(),
            country=COUNTRIES.pop(),
            start_date=start_date,
            end_date=end_date,
            sector=SECTORS.pop(),
            function=FUNCTIONS.pop(),
        )

    TRAINING_TYPES = Cycler(cv.StudyType.objects.filter(is_training=True))
    for i in range(20):
        start_date = settings.SITE.demo_date(-1200 + i * 2)
        d = DURATIONS.pop()
        end_date = DurationUnits.months.add_duration(start_date, d)
        yield cv.Training(
            person=CLIENTS.pop(),
            type=TRAINING_TYPES.pop(),
            school=SCHOOLS.pop(),
            country=COUNTRIES.pop(),
            start_date=start_date,
            end_date=end_date,
            sector=SECTORS.pop(),
            function=FUNCTIONS.pop(),
            state=STATES.pop(),
        )

    STUDY_TYPES = Cycler(cv.StudyType.objects.filter(is_study=True))
    EDULEVELS = Cycler(cv.EducationLevel.objects.all())
    for i in range(20):
        start_date = settings.SITE.demo_date(-1200 + i * 2)
        d = DURATIONS.pop()
        end_date = DurationUnits.months.add_duration(start_date, d)
        yield cv.Study(
            person=CLIENTS.pop(),
            type=STUDY_TYPES.pop(),
            school=SCHOOLS.pop(),
            country=COUNTRIES.pop(),
            start_date=start_date,
            end_date=end_date,
            state=STATES.pop(),
            education_level=EDULEVELS.pop(),
        )


    #~ baker = Properties.objects.get(pk=1)
    #~ baker.save()
    #~ yield baker

    """
    Distribute properties to persons. The distribution should be
    "randomly", but independant of site's language setting.
    """

    for i, p in enumerate(Client.objects.all()):
        if i % 2:
            country = belgium
        else:
            country = COUNTRIES.pop()
        p.birth_country_id = country
        p.nationality_id = country

        if i % 3:
            langk(p, 'eng', written='3', spoken='3')
        elif i % 5:
            langk(p, 'eng', written='4', spoken='4')
        if p.zip_code == '4700':
            langk(p,'ger',native=True)
            if i % 2:
                langk(p, 'fre', written='2', spoken='2')
            p.is_cpas = True
            #~ p.is_active = True
            #~ p.client_state = ClientStates.coached
            #~ p.native_language_id = 'ger'
        p.save()

    for short_code, isocode in (
        ('B', 'BE'),
        ('D', 'DE'),
        ('F', 'FR'),
    ):
        c = countries.Country.objects.get(pk=isocode)
        c.short_code = short_code
        c.save()

    i = pcsw.Client.objects.order_by('name').__iter__()
    p = next(i)
    offset = 0
    for f in cv.Function.objects.all():
        yield jobs.Candidature(person=p, function=f, sector=f.sector,
                               #~ date_submitted=i2d(20111019))
                               date_submitted=settings.SITE.demo_date(offset))
        p = next(i)
        offset -= 1

    PERSONGROUPS = Cycler(pcsw.PersonGroup.objects.all())
    AGENTS_SCATTERED = Cycler(
        alicia, hubert, melanie, caroline, hubert, melanie, hubert, melanie)
    ENDINGS = Cycler(rt.models.coachings.CoachingEnding.objects.all())
    for client in pcsw.Client.objects.all():
        story = COACHING_STORIES.get(client.client_state)
        if story:
            if not client.group:
                client.group = PERSONGROUPS.pop()
                PERSONGROUPS.pop()
                # ~ for i in range(5-client.group.id): PERSONGROUPS.pop() #
                client.save()
            periods = story.pop()
            type = COACHINGTYPES.pop()
            for a, b, primary, ct in periods:
                if ct == CT_OTHER:
                    type = COACHINGTYPES.pop()
                elif ct == CT_GSS:
                    type = ASD
                elif ct == CT_INTEG:
                    type = DSBE
                kw = dict(client=client,
                          user=AGENTS_SCATTERED.pop(),
                          type=type,
                          primary=primary)
                if a is not None:
                    kw.update(start_date=settings.SITE.demo_date(a))
                if b is not None:
                    kw.update(end_date=settings.SITE.demo_date(b))
                    kw.update(ending=ENDINGS.pop())
                yield rt.models.coachings.Coaching(**kw)

    # every 10th partner is obsolete

    for i, p in enumerate(contacts.Partner.objects.all()):
        if i % 10 == 0:
            p.is_obsolete = True
            p.save()

    # The reception desk opens at 8am. 20 visitors have checked in,
    # half of which

    RECEPTION_CLIENTS = Cycler(reception.Clients.request(user=theresia))
    REASONS = Cycler(_("Urgent problem"), '', _("Complain"), _("Information"))
    today = settings.SITE.demo_date()
    now = datetime.datetime(today.year, today.month, today.day, 8, 0)
    for i in range(1, 20):
        obj = RECEPTION_CLIENTS.pop()
        now += datetime.timedelta(minutes=3 * i, seconds=3 * i)
        obj = reception.create_prompt_event(
            obj, obj,
            AGENTS.pop(),
            REASONS.pop(),
            settings.SITE.site_config.client_guestrole,
            now)
        yield obj

    # TODO: the following possibly causes more than one busy guest per
    # agent.
    qs = cal.Guest.objects.filter(waiting_since__isnull=False)
    busy_agents = set()
    for i, obj in enumerate(qs):
        busy_since = obj.waiting_since + \
            datetime.timedelta(minutes=2 * i, seconds=2 * i)
        if i % 3 == 0:
            obj.gone_since = busy_since + \
                datetime.timedelta(minutes=2 * i, seconds=3 * i)
            obj.state = cal.GuestStates.gone
        elif not obj.event.user in busy_agents:
            obj.busy_since = busy_since
            obj.state = cal.GuestStates.busy
            busy_agents.add(obj.event.user)

        yield obj

    Calendar = dd.resolve_model('cal.Calendar')
    COLORS = Cycler(Calendar.COLOR_CHOICES)

    for u in settings.SITE.user_model.objects.exclude(user_type=None):
        obj = Calendar(name=u.username, color=COLORS.pop())
        yield obj
        u.calendar = obj
        u.save()

    # create a primary ClientAddress for each Client.
    # no longer needed. done by checkdata.fixtures.demo2
    # for obj in settings.SITE.models.contacts.Partner.objects.all():
    #     obj.repairdata()

    # have partners speak different languages
    # most partners speak first language
    if len(settings.SITE.languages):
        ld = []  # language distribution
        ld = [settings.SITE.languages[0].django_code] * 10
        if len(settings.SITE.languages) > 1:
            ld += [settings.SITE.languages[1].django_code] * 3
            if len(settings.SITE.languages) > 2:
                ld += [settings.SITE.languages[2].django_code]
        LANGS = Cycler(ld)
        for obj in settings.SITE.models.contacts.Partner.objects.all():
            obj.language = LANGS.pop()
            obj.save()

#~ logger.info("20121010 lino_welfare.fixtures.demo has been imported")
