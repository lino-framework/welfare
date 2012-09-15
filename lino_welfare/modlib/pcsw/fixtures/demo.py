# -*- coding: UTF-8 -*-
## Copyright 2008-2012 Luc Saffre
## This file is part of the Lino project.
## Lino is free software; you can redistribute it and/or modify 
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 3 of the License, or
## (at your option) any later version.
## Lino is distributed in the hope that it will be useful, 
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
## GNU General Public License for more details.
## You should have received a copy of the GNU General Public License
## along with Lino; if not, see <http://www.gnu.org/licenses/>.

import decimal
#~ from dateutil.relativedelta import relativedelta
#~ ONE_DAY = relativedelta(days=1)
import datetime
ONE_DAY = datetime.timedelta(days=1)

from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext as _


from lino.utils import i2d, Cycler
from lino.utils.instantiator import Instantiator
from lino.core.modeltools import resolve_model
from lino.utils.babel import babel_values, default_language
from lino.utils.restify import restify
from lino.utils import dblogger
#~ from lino.models import update_site_config
from lino.utils import mti
from lino import dd

#~ from django.contrib.auth import models as auth
#~ from lino.modlib.users import models as auth
#~ from lino.modlib.contacts.utils import GENDER_FEMALE, GENDER_MALE
from lino.utils.choicelists import Gender
from lino_welfare.modlib.jobs import models as jobs
from lino.modlib.contacts import models as contacts
from lino.modlib.countries import models as countries
from lino_welfare.modlib.pcsw import models as pcsw
from lino_welfare.modlib.isip import models as isip

#~ dblogger.info('Loading')


#~ DEMO_LINKS = [
  #~ dict(name="Lino website",url="http://lino.saffre-rumma.net"),
  #~ dict(name="Django website",url="http://www.djangoproject.com"),
  #~ dict(name="ExtJS website",url="http://www.sencha.com"),
  #~ dict(name="Python website",url="http://www.python.org"),
  #~ dict(name="Google",url="http://www.google.com"),
#~ ]


#~ def coaching_stories(state):
COACHING_STORIES = dict()
COACHING_STORIES[pcsw.ClientStates.former] =  Cycler(
    [ 
        (-1000,-500,True) 
    ],[ 
        (None,-60,True) 
    ],[ 
        (-900,-430,False),
        (-430,-200,True),
    ])
COACHING_STORIES[pcsw.ClientStates.active] = Cycler(
    [ 
        (-800,-440,False),
        (-440,-210,False),
        (-210,None,True),
    ],[ 
        (-220,None,True),
    ],[
        (-810,None,True),
        (-440,-230,False),
        (-230,None,False),
    ])
    
#~ COACHING_STORIES = Cycler(coaching_stories())

        

    


#~ auth = models.get_app('auth')
#~ projects = models.get_app('projects')
#~ contacts = models.get_app('contacts')
#~ notes = models.get_app('notes')
#~ properties = models.get_app('properties')


#char_pv = Instantiator('properties.CharPropValue').build
#CharPropValue = resolve_model('properties.CharPropValue')
#~ from lino.modlib.properties import models as properties # CharPropValue, BooleanPropValue
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



def unused_coachings(p,type,coach1,coach2,coached_from,coached_until=None):
    if coach1:
        yield pcsw.Coaching(
            project=p,
            type=type,
            primary=True,
            #~ state=pcsw.CoachingStates.active,
            user=coach1,
            start_date=coached_from,
            end_date=coached_until)
    if coach2:
        yield pcsw.Coaching(
            project = p,
            type=type,
            #~ state=pcsw.CoachingStates.active,
            user=coach2,
            start_date=coached_from,
            end_date=coached_until)



def objects():
  
    sector = Instantiator(jobs.Sector).build
    for ln in SECTORS_LIST.splitlines():
        if ln:
            a = ln.split('|')
            if len(a) == 3:
                kw = dict(en=a[0],fr=a[1],de=a[2])
                yield sector(**babel_values('name',**kw))
                
    horeca = jobs.Sector.objects.get(pk=5)
    function = Instantiator(jobs.Function,sector=horeca).build
    yield function(**babel_values('name',
          de=u"Kellner",
          fr=u'Serveur',
          en=u'Waiter',
          ))
    yield function(**babel_values('name',
          de=u"Koch",
          fr=u'Cuisinier',
          en=u'Cook',
          ))
    yield function(**babel_values('name',
          de=u"Küchenassistent",
          fr=u'Aide Cuisinier',
          en=u'Cook assistant',
          ))
    yield function(**babel_values('name',
          de=u"Tellerwäscher",
          fr=u'Plongeur',
          en=u'Dishwasher',
          ))

    contractType = Instantiator(jobs.ContractType,"ref",
        exam_policy=3,
        build_method='appypdf',
        template=u'art60-7.odt').build
    #~ yield contractType('art60-7a',
      #~ **babel_values('name',
          #~ de=u"Konvention Art.60§7 Sozialökonomie",
          #~ fr=u'Convention art.60§7 économie sociale',
          #~ en=u'Convention art.60§7 social economy',
          #~ ))
    yield contractType('art60-7a',
      **babel_values('name',
          de=u"Sozialökonomie",
          fr=u'économie sociale',
          en=u'social economy',
          ))
    yield contractType('art60-7b',
      **babel_values('name',
          de=u"Sozialökonomie - majoré",
          fr=u'économie sociale - majoré',
          en=u'social economy - increased',
          ))
    yield contractType('art60-7c',
      **babel_values('name',
          de=u"mit Rückerstattung",
          fr=u'avec remboursement',
          en=u'social economy with refund',
          ))
    yield contractType('art60-7d',
      **babel_values('name',
          de=u"mit Rückerstattung Schule",
          fr=u'avec remboursement école',
          en=u'social economy school',
          ))
    yield contractType('art60-7e',
      **babel_values('name',
          de=u"Stadt Eupen",
          fr=u"ville d'Eupen",
          en=u'town',
          ))
    
    contractType = Instantiator(isip.ContractType,"ref",
      exam_policy=1,
      build_method='appypdf',template=u'vse.odt').build
    yield contractType("vsea",**babel_values('name',
          de=u"VSE Ausbildung",
          fr=u"VSE Ausbildung",
          en=u"VSE Ausbildung",
          ))
    yield contractType("vseb",**babel_values('name',
          de=u"VSE Arbeitssuche",
          fr=u"VSE Arbeitssuche",
          en=u"VSE Arbeitssuche",
          ))
    yield contractType("vsec",**babel_values('name',
          de=u"VSE Lehre",
          fr=u"VSE Lehre",
          en=u"VSE Lehre",
          ))
    yield contractType("vsed",**babel_values('name',
          de=u"VSE Vollzeitstudium",
          fr=u"VSE Vollzeitstudium",
          en=u"VSE Vollzeitstudium",
          ))
    yield contractType("vsee",**babel_values('name',
          de=u"VSE Sprachkurs",
          fr=u"VSE Sprachkurs",
          en=u"VSE Sprachkurs",
          ))
    #~ yield contractType(u"VSE Integration")
    #~ yield contractType(u"VSE Cardijn")
    #~ yield contractType(u"VSE Work & Job")
    
  
  
    Person = resolve_model(settings.LINO.person_model)
    Company = resolve_model(settings.LINO.company_model)
    #~ Contact = resolve_model('contacts.Contact')
    Role = resolve_model('contacts.Role')
    RoleType = resolve_model('contacts.RoleType')
    #~ Link = resolve_model('links.Link')
    #~ Contract = resolve_model('jobs.Contract')
    #~ JobProvider = resolve_model('jobs.JobProvider')
    #~ Function = resolve_model('jobs.Function')
    #~ Sector = resolve_model('jobs.Sector')
    User = resolve_model('users.User')
    #~ Country = resolve_model('countries.Country')
    Client = resolve_model('pcsw.Client')
    
    rt = RoleType.objects.get(pk=4) # It manager
    rt.use_in_contracts = False
    rt.save()

    person = Instantiator(Person).build
    client = Instantiator(Client).build
    company = Instantiator(Company).build
    #~ contact = Instantiator(Contact).build
    role = Instantiator(Role).build
    #~ link = Instantiator(Link).build
    #~ exam_policy = Instantiator('isip.ExamPolicy').build

    City = resolve_model('countries.City')
    #~ Job = resolve_model('jobs.Job')
    #~ City = settings.LINO.modules.countries.City
    StudyType = resolve_model('jobs.StudyType')
    #~ Country = resolve_model('countries.Country')
    Property = resolve_model('properties.Property')
  
    
    #~ country = Instantiator('countries.Country',"isocode name").build
    #~ yield country('SUHH',"Soviet Union")
    
    eupen = City.objects.get(name__exact='Eupen')
    kettenis = City.objects.get(name__exact='Kettenis')
    vigala = City.objects.get(name__exact='Vigala')
    ee = countries.Country.objects.get(pk='EE')
    be = belgium = countries.Country.objects.get(isocode__exact='BE')
    #~ luc = person(first_name="Luc",last_name="Saffre",city=vigala,country='EE',card_number='122')
    #~ yield luc
    andreas = Person.objects.get(name__exact="Arens Andreas")
    annette = Person.objects.get(name__exact="Arens Annette")
    hans = Person.objects.get(name__exact="Altenberg Hans")
    ulrike = Person.objects.get(name__exact="Charlier Ulrike")
    erna = Person.objects.get(name__exact=u"Ärgerlich Erna")
    
    cpas = company(name=u"ÖSHZ Eupen",city=eupen,country=belgium)
    yield cpas
    bisa = company(name=u"BISA",city=eupen,country=belgium)
    yield bisa 
    bisa_dir = role(company=bisa,person=annette,type=1)
    yield bisa_dir 
    rcycle = company(name=u"R-Cycle Sperrgutsortierzentrum",city=eupen,country=belgium)
    yield rcycle
    rcycle_dir = role(company=rcycle,person=andreas,type=1)
    yield rcycle_dir
    yield role(company=rcycle,person=erna,type=2)
    yield role(company=rcycle,person=ulrike,type=4) # IT manager : no contracts
    yield company(name=u"Die neue Alternative V.o.G.",city=eupen,country=belgium)
    proaktiv = company(name=u"Pro Aktiv V.o.G.",city=eupen,country=belgium)
    yield proaktiv
    proaktiv_dir = role(company=proaktiv,person=hans,type=1)
    yield role(company=proaktiv,person=ulrike,type=4) # IT manager : no contracts
    yield proaktiv_dir
    yield company(name=u"Werkstatt Cardijn V.o.G.",city=eupen,country=belgium)
    yield company(name=u"Behindertenstätten Eupen",city=eupen,country=belgium)
    yield company(name=u"Beschützende Werkstätte Eupen",city=eupen,country=belgium)
    
    kw = dict(is_health_insurance=True,country=belgium)
    yield company(name=u"Alliance Nationale des Mutualités Chrétiennes",**kw)
    yield company(name=u"Mutualité Chrétienne de Verviers - Eupen",**kw)
    yield company(name=u"Union Nationale des Mutualités Neutres",**kw)
    yield company(name=u"Mutualia - Mutualité Neutre",**kw)
    yield company(name=u"Solidaris - Mutualité socialiste et syndicale de la province de Liège",**kw)
    
    kw = dict(is_pharmacy=True,country=belgium,city=eupen)
    yield company(name=u"Apotheke Reul",street=u'Klosterstraße',street_no=20,**kw)
    yield company(name=u"Apotheke Schunck",street=u'Bergstraße',street_no=59,**kw)
    yield company(name=u"Pharmacies Populaires de Verviers",street=u'Aachener Straße',street_no=258,**kw)
    yield company(name=u"Bosten-Bocken A",street=u'Haasstraße',street_no=6,**kw)
    
    kw = dict(is_attorney=True,country=belgium,city=eupen)
    yield company(name=u"Brüll Christine",street=u'Schilsweg',street_no=4,**kw)
    yield company(name=u"Brocal Catherine",street=u'Neustraße',street_no=115,**kw)
    yield company(name=u"Bourseaux Alexandre",street=u'Aachener Straße',street_no=21,**kw)
    yield company(name=u"Baguette Stéphanie",street=u'Gospertstraße',street_no=24,**kw)
    
    def person2client(p,**kw):
        c = mti.insert_child(p,Client,**kw)
        c.client_state = pcsw.ClientStates.active
        c.save()
        return Client.objects.get(pk=p.pk)
    
    luc = Person.objects.get(name__exact="Saffre Luc")
    luc = person2client(luc,national_id = '680601 053-29')
    luc.birth_place = 'Eupen'
    luc.birth_date = '1968-06-01'
    luc.birth_country = be
    luc.full_clean()
    luc.save()
    
    ly = person(first_name="Ly",last_name="Rumma",
      city=vigala,country='EE',
      #~ card_number='123',birth_country=ee,birth_date='0000-04-27',
      #~ national_id='1234',
      #~ client_state=pcsw.ClientStates.newcomer,
      gender=Gender.female)
    yield ly
    mari = person(first_name="Mari",last_name="Saffre",
      city=vigala,country='EE',
      #~ card_number='124',birth_country=ee,
      #~ birth_date=i2d(20020405),
      #~ national_id='1235',
      #~ client_state=pcsw.ClientStates.newcomer,
      gender=Gender.female)
    yield mari
    iiris = person(first_name="Iiris",last_name="Saffre",
      city=vigala,country='EE',
      #~ card_number='125',birth_country=ee,
      #~ birth_date=i2d(20080324),
      #~ national_id='1236',
      #~ client_state=pcsw.ClientStates.newcomer,
      gender=Gender.female)
    yield iiris
    
    gerd = person(first_name="Gerd",
      last_name="Xhonneux",city=kettenis,
      email='gerd@example.com',
      name="Xhonneux Gerd",country='BE',gender=Gender.male)
    yield gerd
    yield role(company=cpas,person=gerd,type=4)
    #~ yield link(a=cpas,b=gerd,type=4)
    
    # see :doc:`/blog/2011/1007`
    tatjana = client(
        first_name=u"Tatjana",last_name=u"Kasennova",
        #~ first_name=u"Татьяна",last_name=u"Казеннова",
        city=kettenis,country='BE', 
        national_id='1237',
        birth_place="Moskau", # birth_country='SUHH',
        client_state=pcsw.ClientStates.newcomer,
        #~ newcomer=True,
        gender=Gender.female)
    yield tatjana
    
    from django.core.exceptions import ValidationError
    # a circular reference: bernard is contact for company adg and also has himself as `job_office_contact`
    bernard = Person.objects.get(name__exact="Bodard Bernard")
    adg = company(name=u"Arbeitsamt der D.G.",city=eupen,country=belgium,is_job_office=True)
    settings.LINO.update_site_config(job_office=adg)
    yield adg
    adg_dir = role(company=adg,person=bernard,type=1)
    #~ adg_dir = link(a=adg,b=bernard,type=1)
    yield adg_dir
    
    #~ try:
      #~ bernard.job_office_contact = adg_dir
      #~ bernard.clean()
      #~ bernard.save()
    #~ except ValidationError:
        #~ pass
    #~ else:
        #~ raise Exception("Expected ValidationError")
      
    DIRECTORS = (annette,hans,andreas,bernard)
    
    yield User(username='gerd',partner=gerd,profile='900')
    
    melanie = person(first_name=u"Mélanie",last_name=u"Mélard",
        email='melanie@example.com',
        city=eupen,country='BE',gender=Gender.female,language='fr')
    yield melanie
    melanie = User(username="melanie",partner=melanie,profile='110') 
    yield melanie
    
    hubert = person(first_name=u"Hubert",last_name=u"Huppertz",
        email='hubert@example.com',
        city=eupen,country='BE',gender=Gender.male)
    yield hubert
    hubert = User(username="hubert",partner=hubert,profile='100') 
    yield hubert
    
    alicia = person(first_name=u"Alicia",last_name=u"Allmanns",
        email='alicia@example.com',
        city=eupen,country='BE',gender=Gender.female)
    yield alicia
    alicia = User(username="alicia",partner=alicia,profile='100') 
    yield alicia
    
    elmar = person(first_name=u"Elmar",last_name=u"Elsen",
        city=eupen,country='BE',gender=Gender.male)
    yield elmar
    elmar = User(username="elmar",partner=elmar,profile='400') 
    yield elmar
    
    charles = person(first_name=u"Charles",last_name=u"Cabeil-Esaice",
        city=eupen,country='BE',gender=Gender.male)
    yield charles
    charles = User(username="charles",partner=charles,profile='500') 
    yield charles
    
    DSBE = pcsw.CoachingType(name="DSBE")
    yield DSBE
    yield pcsw.CoachingType(name="ASD")
    yield pcsw.CoachingType(name="Schuldnerberatung")
    
    
    #~ USERS = Cycler(root,melanie,hubert,alicia)
    AGENTS = Cycler(melanie,hubert,alicia)
    COACHINGTYPES = Cycler(pcsw.CoachingType.objects.all())
    
    #~ CLIENTS = Cycler(andreas,annette,hans,ulrike,erna,tatjana)
    count = 0
    for person in Person.objects.all():
        if User.objects.filter(partner=person).count() == 0:
          if contacts.Role.objects.filter(person=person).count() == 0:
            #~ if not person in DIRECTORS:
            client = person2client(person,national_id=str(person.pk))
            count += 1
            if count % 2:
                #~ client.is_active = True
                client.client_state=pcsw.ClientStates.active
                #~ args = [client,COACHINGTYPES.pop(),AGENTS.pop()]
                #~ if count % 2:
                    #~ args.append(None)
                #~ else:
                    #~ args.append(AGENTS.pop())
                #~ args.append(settings.LINO.demo_date(-7 * count))
                #~ if count % 6:
                    #~ args.append(settings.LINO.demo_date(-7 * count))
                #~ yield coachings(*args)
                    
            elif count % 5:
                #~ client.newcomer = True
                client.client_state=pcsw.ClientStates.newcomer
            else:
                client.client_state=pcsw.ClientStates.former
                
            client.clean()
            client.save()
            
    #~ CLIENTS = Cycler(Client.objects.filter(is_active=True,newcomer=False))
    CLIENTS = Cycler(Client.objects.filter(client_state=pcsw.ClientStates.active))
    
    #~ oshz = Company.objects.get(name=u"ÖSHZ Eupen")
    
    
    #~ project = Instantiator('projects.Project').build
    #~ note = Instantiator('notes.Note').build
    langk = Instantiator('cv.LanguageKnowledge').build

    #~ prj = project(name="Testprojekt",company=oshz)
    #~ yield prj 
    #~ yield note(user=user,project=prj,date=i2d(20091006),subject="Programmierung",company=oshz)
    
    #~ prj = project(name="Testprojekt",company=oshz)
    #~ yield prj 
    #~ yield note(user=user,project=prj,date=i2d(20091007),subject="Anschauen",company=oshz)
    
    
    Note = resolve_model('notes.Note')
    USERS = Cycler(User.objects.all())
    SUBJECTS = Cycler("""
    Erstgespräch
    Versammlung beim AG
    Zwischenbericht
    Krisensitzung 
    """.splitlines())
    
    for i in range(10):
        yield Note(user=USERS.pop(),
          date=settings.LINO.demo_date(days=i),
          subject=SUBJECTS.pop())
    

    if False:
        #~ yield note(user=root,date=settings.LINO.demo_date(),
        yield note(user=root,date=i2d(20091006),
            subject="Programmierung",company=cpas,
            type=1,event_type=1)
        yield note(user=user,date=i2d(20091007),subject="Testen",company=cpas)
        yield note(user=root,date=i2d(20100517),subject="Programmierung",company=cpas)
        yield note(user=user,date=i2d(20100518),subject="Testen",company=cpas)
        yield note(user=user,date=i2d(20110526),subject="Formatted notes",
            company=cpas,body=restify(u"""\
Formatted notes
===============

Lino has now a WYSIWYG text editor. 

Examples
--------

- Enumerations like this list
- Character formatting : **bold**, *italics*, ``typewriter``.
- External `Links <http://lino.saffre-rumma.net/todo.html>`_
- Tables:

  ============ =======
  Package      Version
  ============ =======
  mercurial    1
  apache2      2 
  tinymce      3
  ============ =======
  
Lorem ipsum 
-----------

Lorem ipsum dolor sit amet, consectetur adipisici elit, sed eiusmod tempor incidunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquid ex ea commodi consequat. Quis aute iure reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint obcaecat cupiditat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

Duis autem vel eum iriure dolor in hendrerit in vulputate velit esse molestie consequat, vel illum dolore eu feugiat nulla facilisis at vero eros et accumsan et iusto odio dignissim qui blandit praesent luptatum zzril delenit augue duis dolore te feugait nulla facilisi. Lorem ipsum dolor sit amet, consectetuer adipiscing elit, sed diam nonummy nibh euismod tincidunt ut laoreet dolore magna aliquam erat volutpat.  

"""))
    
    schule = StudyType.objects.get(pk=1)
    uni = StudyType.objects.get(pk=4)
    #~ abi = StudyContent.objects.get(name=u"Abitur")
    abi = u"Abitur"
    study = Instantiator('jobs.Study').build
    
    gerd = CLIENTS.pop()
        
    yield study(person=luc,type=schule,content=abi,
      started='19740901',stopped='19860630')
    yield study(person=gerd,type=schule,content=abi,
      started='19740901',stopped='19860630')

    yield langk(person=luc,language='ger',written='4',spoken='4')
    yield langk(person=gerd,language='ger',written='4',spoken='4')
    yield langk(person=mari,language='ger',written='2',spoken='4')
    yield langk(person=iiris,language='ger',written='0',spoken='4')
    yield langk(person=ly,language='ger',written='2',spoken='1')
    
    yield langk(person=luc,language='fre',written='4',spoken='3')
    yield langk(person=gerd,language='fre',written='4',spoken='3')
    
    yield langk(person=luc,language='eng',written='4',spoken='3')
    yield langk(person=gerd,language='eng',written='4',spoken='3')
    yield langk(person=ly,language='eng',written='3',spoken='3')
    
    yield langk(person=gerd,language='dut',written='3',spoken='3')
    
    yield langk(person=luc,language='est',written='3',spoken='3')
    yield langk(person=ly,language='est',written='4',spoken='4')
    yield langk(person=mari,language='est',written='3',spoken='4')
    yield langk(person=iiris,language='est',written='0',spoken='3')
    
    
    jobtype = Instantiator(jobs.JobType,'name').build
    art607 = jobtype(u'Sozialwirtschaft = "majorés"')
    yield art607 
    yield jobtype(u'Intern')
    yield jobtype(u'Extern (Öffentl. VoE mit Kostenrückerstattung)')
    yield jobtype(u'Extern (Privat Kostenrückerstattung)')
    #~ yield jobtype(u'VSE')
    yield jobtype(u'Sonstige')
    
    rcycle = mti.insert_child(rcycle,jobs.JobProvider)
    yield rcycle 
    bisa = mti.insert_child(bisa,jobs.JobProvider)
    yield bisa 
    proaktiv = mti.insert_child(proaktiv,jobs.JobProvider)
    yield proaktiv
    
    #~ job = Instantiator('jobs.Job','provider type contract_type name').build
    #~ bisajob = job(bisa,art607,1,"bisa")
    #~ yield bisajob
    #~ rcyclejob = job(rcycle,art607,2,"rcycle")
    #~ yield rcyclejob 
    #~ proaktivjob = job(proaktiv,art607,2,"proaktiv",sector=horeca,function=1)
    #~ yield proaktivjob
    
    
    # isip (VSE)
    
    
    ISIP_DURATIONS = Cycler(30,312,480)
    ISIP_CONTRACT_TYPES = Cycler(isip.ContractType.objects.all())
    
    
    # jobs (Art.60-7)
    
    #~ from lino_welfare.modlib.jobs.models import Job
    #~ CTYPES = Cycler(*[x for x in ContractType.objects.all()])
    #~ JTYPES = Cycler(*[x for x in JobType.objects.all()])
    JOBS_CONTRACT_TYPES = Cycler(jobs.ContractType.objects.all())
    JTYPES = Cycler(jobs.JobType.objects.all())
    
    PROVIDERS = Cycler(jobs.JobProvider.objects.all())
    SECTORS = Cycler(jobs.Sector.objects.all())
    FUNCTIONS = Cycler(jobs.Function.objects.all())
    
    for i in range(8):
        f = FUNCTIONS.pop()
        yield jobs.Job(provider=PROVIDERS.pop(),
          type=JTYPES.pop(),
          contract_type=JOBS_CONTRACT_TYPES.pop(),
          name=unicode(f),
          sector=SECTORS.pop(),function=f)
    
    JOBS = Cycler(jobs.Job.objects.all())
        
    for i in range(30):
        yield jobs.Candidature(job=JOBS.pop(),person=CLIENTS.pop(),
          date_submitted=settings.LINO.demo_date(-30+i))
    

    

    #~ from lino.sites.pcsw.models import Course, CourseContent, CourseRequest
    
    courseprovider = Instantiator('courses.CourseProvider').build
    #~ oikos = company(name=u"Oikos",city=eupen,country='BE',
      #~ is_courseprovider=True)
    oikos = courseprovider(name=u"Oikos",city=eupen,country='BE')
    yield oikos
    
    #~ kap = company(name=u"KAP",city=eupen,country='BE',
      #~ is_courseprovider=True)
    kap = courseprovider(name=u"KAP",city=eupen,country='BE')
    yield kap
    
    CourseContent = resolve_model('courses.CourseContent')
    yield CourseContent(id=1,name=u"Deutsch")
    yield CourseContent(id=2,name=u"Französisch")
    
    COURSECONTENTS = Cycler(CourseContent.objects.all())
    
    creq = Instantiator('courses.CourseRequest').build
    for i in range(20):
        yield creq(
            person=CLIENTS.pop(),content=COURSECONTENTS.pop(),
            date_submitted=settings.LINO.demo_date(-i*2))
    #~ yield creq(person=ulrike,content=1,date_submitted=settings.LINO.demo_date(-30))
    #~ yield creq(person=tatjana,content=1,date_submitted=settings.LINO.demo_date(-30))
    #~ yield creq(person=erna,content=2,date_submitted=settings.LINO.demo_date(-30))
    
    offer = Instantiator('courses.CourseOffer').build
    course = Instantiator('courses.Course').build
    yield offer(provider=oikos,title=u"Deutsch für Anfänger",content=1)
    #~ yield course(offer=1,start_date=i2d(20110110))
    yield course(offer=1,start_date=settings.LINO.demo_date(+30))
    
    yield offer(provider=kap,title=u"Deutsch für Anfänger",content=1)
    #~ yield course(offer=2,start_date=i2d(20110117))
    yield course(offer=2,start_date=settings.LINO.demo_date(+16))
    
    yield offer(provider=kap,title=u"Français pour débutants",content=2)
    #~ yield course(offer=3,start_date=i2d(20110124))
    yield course(offer=3,start_date=settings.LINO.demo_date(+16))
    
    #~ baker = Properties.objects.get(pk=1)
    #~ baker.save()
    #~ yield baker

    """
    Distribute properties to persons. The distribution should be
    "randomly", but independant of site's language setting.
    """
    
    #~ pp = Instantiator('properties.PersonProperty',
        #~ 'person property value').build
    #~ props = [p for p in Property.objects.order_by('id')]
    #~ i = 0
    #~ L = len(props)
    #~ assert L > 10 
    #~ for p in Person.objects.all():
        #~ for n in range(3):
            #~ if i >= L: 
                #~ i = 0
            #~ prop = props[i]
            #~ i += 1
            #~ yield pp(p,prop,prop.type.default_value)
            
    PP = resolve_model('properties.PersonProperty')
    #~ pp = Instantiator('properties.PersonProperty',
        #~ 'person property value').build
    #~ PROPS = Cycler(Property.objects.order_by('id'))
    #~ props = [p for p in Property.objects.order_by('id')]
    #~ i = 0
    #~ L = len(props)
    #~ assert L > 10 
    PERSONS = Cycler(Client.objects.all())
    for prop in Property.objects.order_by('id'):
        for n in range(10):
            #~ prop = PROPS.pop()
            VALUES = Cycler(prop.type.choices_for(prop))
            #~ print "20120409", repr(VALUES.items)
            #~ for n in range(3):
            if len(VALUES) == 0:
                yield PP(person=PERSONS.pop(),property=prop)
            else:
                for n in range(len(VALUES)):
                    yield PP(person=PERSONS.pop(),property=prop,value=VALUES.pop()[0].value)
            
            
            
    #~ langk = Instantiator('cv.LanguageKnowledge',
        #~ 'person:name language written spoken').build
    #~ yield langk(u"Ausdemwald Alfons",'est','1','1')
    #~ yield langk(u"Ausdemwald Alfons",'ger','4','3')
    #~ yield langk(u"Bastiaensen Laurent",'ger','4','3')
    #~ yield langk(u"Bastiaensen Laurent",'fre','4','3')
    #~ yield langk(u"Eierschal Emil",'ger','4','3')
    #~ yield langk(u"Ärgerlich Erna",'ger','4','4')
    
    persongroup = Instantiator('pcsw.PersonGroup','name').build
    #~ pg1 = persongroup(u"Art. 60 § 7",ref_name='1')
    pg1 = persongroup(u"Bilan",ref_name='1')
    yield pg1
    #~ pg2 = persongroup(u"Préformation",ref_name='2')
    pg2 = persongroup(u"Formation",ref_name='2')
    yield pg2
    #~ yield persongroup(u"Formation",ref_name='3')
    yield persongroup(u"Recherche",ref_name='4')
    yield persongroup(u"Travail",ref_name='4bis')
    standby = persongroup(u"Standby",ref_name='9',active=False)
    yield standby
    
    COUNTRIES = Cycler(countries.Country.objects.all())
    
    for i,p in enumerate(Client.objects.all()):
        if i % 2:
            country = belgium
        else:
            country = COUNTRIES.pop()
        p.birth_country_id = country
        p.nationality_id = country
        
        # youngest client is 16; 170 days between each client
        p.birth_date = settings.LINO.demo_date(-170*i - 16*365)
        
        if i % 3:
            p.languageknowledge_set.create(language_id='eng',written='3',spoken='3')
        elif i % 5:
            p.languageknowledge_set.create(language_id='eng',written='4',spoken='4')
        if p.zip_code == '4700':
            p.languageknowledge_set.create(language_id='ger',native=True)
            if i % 2:
                p.languageknowledge_set.create(language_id='fre',written='2',spoken='2')
            p.is_cpas = True
            #~ p.is_active = True
            #~ p.client_state = pcsw.ClientStates.active
            #~ p.native_language_id = 'ger'
        p.save()

    for short_code,isocode in (
        ('B', 'BE'),
        ('D', 'DE'),
        ('F', 'FR'),
      ):
      c = countries.Country.objects.get(pk=isocode)
      c.short_code = short_code
      c.save()
      
    root = User.objects.get(username='root')
      
    #~ p = Client.objects.get(name=u"Ärgerlich Erna")
    #~ p.birth_date = i2d(19800301)
    #~ p.coached_from = settings.LINO.demo_date(-7*30)
    #~ p.coached_until = None
    #~ p.coach1 = root
    #~ p.coach2 = alicia # User.objects.get(username='alicia')
    #~ p.gender = Gender.female 
    #~ p.group = pg1
    #~ p.save()
    
    #~ yield coachings(p,COACHINGTYPES.pop(),root,alicia,settings.LINO.demo_date(-7*30))
    
    #~ task = Instantiator('cal.Task').build
    #~ yield task(user=root,start_date=i2d(20110717),
        #~ summary=u"Anrufen Termin",
        #~ owner=p)
    
    #~ p = Client.objects.get(name=u"Eierschal Emil")
    #~ p.birth_date = i2d(19800501)
    #~ p.coached_from = settings.LINO.demo_date(-2*30)
    #~ p.coached_until = settings.LINO.demo_date(10*30)
    #~ p.coach1 = User.objects.get(username='root')
    #~ p.group = pg2
    #~ p.gender = Gender.male
    #~ p.national_id = 'INVALID-45'
    #~ p.save()
    
    #~ yield coachings(p,COACHINGTYPES.pop(),root,None,settings.LINO.demo_date(-2*30),settings.LINO.demo_date(10*30))

    #~ p = Client.objects.get(name=u"Bastiaensen Laurent")
    #~ p.birth_date = i2d(19810601)
    #~ p.coached_from = None
    #~ p.coached_until = settings.LINO.demo_date(-2*30)
    #~ p.unavailable_until = settings.LINO.demo_date(2*30)
    #~ p.coach1 = User.objects.get(username='root')
    #~ p.coach2 = alicia # User.objects.get(username='alicia')
    #~ p.group = pg1
    #~ p.gender = Gender.male
    #~ p.national_id = '810601 211-83'
    #~ p.save()

    #~ yield coachings(p,COACHINGTYPES.pop(),root,alicia,None,settings.LINO.demo_date(-2*30))
    
    #~ p = Client.objects.get(name=u"Chantraine Marc")
    #~ p.birth_date = i2d(19500301)
    #~ p.coached_from = settings.LINO.demo_date(10)
    #~ p.coached_until = None
    #~ p.coach1 = User.objects.get(username='root')
    #~ p.group = pg2
    #~ p.gender = Gender.male
    #~ p.save()

    #~ yield coachings(p,COACHINGTYPES.pop(),root,None,settings.LINO.demo_date(10),None)
    
    #~ p = Client.objects.get(name=u"Charlier Ulrike")
    #~ p.birth_date = i2d(19600401)
    #~ p.coached_from = settings.LINO.demo_date(-3*30)
    #~ p.coached_until = None
    #~ p.coach1 = alicia # User.objects.get(username='alicia')
    #~ p.gender = Gender.female
    #~ p.group = pg1
    #~ p.save()
    
    #~ yield coachings(p,COACHINGTYPES.pop(),alicia,None,settings.LINO.demo_date(-3*30),None)


    #~ p = Client.objects.get(name=u"Collard Charlotte")
    #~ p.birth_date = i2d(19800401)
    #~ p.coached_from = settings.LINO.demo_date(-6*30)
    #~ p.coached_until = None
    #~ p.coach1 = User.objects.get(username='root')
    #~ p.gender = Gender.female
    #~ p.group = standby
    #~ p.save()
    
    #~ yield coachings(p,COACHINGTYPES.pop(),root,None,settings.LINO.demo_date(-6*30),None)

    #~ etype = Instantiator('cal.EventType','name').build
    #~ yield etype("interner Termin")
    #~ yield etype("Termin beim Klienten")
    #~ yield etype("Termin beim Arbeitgeber")
    
    #~ event = Instantiator('cal.Event',
      #~ 'start_date project summary',
      #~ user=alicia).build
    #~ yield event(settings.LINO.demo_date(+1),hans,u"Stand der Dinge")
    #~ yield event(settings.LINO.demo_date(+1),annette,u"Problem Kühlschrank")
    #~ yield event(settings.LINO.demo_date(+2),andreas,u"Mein dritter Termin")

    i = pcsw.Client.objects.order_by('name').__iter__()
    p = i.next()
    offset = 0
    for f in jobs.Function.objects.all():
        yield jobs.Candidature(person=p,function=f,sector=f.sector,
            #~ date_submitted=i2d(20111019))
            date_submitted=settings.LINO.demo_date(offset))
        p = i.next()
        offset -= 1
        
    PERSONGROUPS = Cycler(pcsw.PersonGroup.objects.all())
    for client in pcsw.Client.objects.exclude(client_state=pcsw.ClientStates.newcomer):
    #~ for i in range(30):
        #~ client = CLIENTS.pop()
        if not client.group:
            client.group = PERSONGROUPS.pop()
            PERSONGROUPS.pop()
            #~ for i in range(5-client.group.id): PERSONGROUPS.pop() # 
            client.save()
        periods = COACHING_STORIES[client.client_state].pop()
        for a,b,primary in periods:
            kw = dict(project=client,type=COACHINGTYPES.pop(),user=AGENTS.pop(),primary=primary)
            if a is not None:
                kw.update(start_date=settings.LINO.demo_date(a))
            if b is not None:
                kw.update(end_date=settings.LINO.demo_date(b))
            yield pcsw.Coaching(**kw)

    JOBS_CONTRACT_DURATIONS = Cycler(312,480,624)
    #~ jobs_contract = Instantiator('jobs.Contract').build
    for i,coaching in enumerate(pcsw.Coaching.objects.filter(type=DSBE)):
        af = coaching.start_date or settings.LINO.demo_date(-600+i*40)
        kw = dict(applies_from=af,person=coaching.project,user=coaching.user)
        if i % 2:
            yield jobs.Contract(
                type=JOBS_CONTRACT_TYPES.pop(),
                duration=JOBS_CONTRACT_DURATIONS.pop(),
                job=JOBS.pop(),**kw)
        else:
            #~ af = settings.LINO.demo_date(-100+i*7)
            yield isip.Contract(type=ISIP_CONTRACT_TYPES.pop(),
                #~ applies_from=af,
                applies_until=af+datetime.timedelta(days=ISIP_DURATIONS.pop()),**kw)
                

    
