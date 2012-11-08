# -*- coding: UTF-8 -*-
## Copyright 2010-2012 Luc Saffre
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

"""
Starts a daemon that 
watches the specified directory for a file :xfile:`changelog.json` 
to appear.
"""

import os
import sys
import codecs
import time
import datetime
#~ import signal
import atexit

#~ import logging
#~ logger = logging.getLogger(__name__)

from dateutil import parser as dateparser

from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ValidationError


from django.conf import settings


from django.db.utils import DatabaseError
# OperationalError
from django.utils import simplejson
#~ from django.contrib.auth import models as auth
#~ from lino.modlib.users import models as users
from django.utils.encoding import force_unicode

import lino

from lino import dd
from lino.modlib.contacts.utils import name2kw, street2kw
from lino.utils import join_words, unicode_string

from lino.utils import dblogger
from lino.utils import mti
from lino.core.modeltools import obj2str
from lino.core import changes
from lino.core.modeltools import is_valid_email

from lino.utils.daemoncommand import DaemonCommand

from lino.utils.niss import is_valid_niss

#~ from lino.apps.pcsw.models  import is_valid_niss

#~ from lino_welfare.modlib.pcsw import models as pcsw
#~ from lino_welfare.modlib.pcsw.management.commands.initdb_tim import ADR_id

pcsw = dd.resolve_app('pcsw')
users = dd.resolve_app('users')
Country = dd.resolve_model('countries.Country')
City = dd.resolve_model('countries.City')
Person = dd.resolve_model(settings.LINO.person_model)
Client = dd.resolve_model('pcsw.Client')
Company = dd.resolve_model(settings.LINO.company_model)
Household = dd.resolve_model('households.Household')
households_Type = dd.resolve_model("households.Type")

CCTYPE_HEALTH_INSURANCE = 1
CCTYPE_PHARMACY = 2

def store(kw,**d):
    for k,v in d.items():
        if v is not None:
        # see :doc:`/blog/2011/0711`
        #~ if v:
            kw[k] = v

def store_date(row,obj,rowattr,objattr):
    v = row[rowattr]
    if v:
        if isinstance(v,basestring):
            v = dateparser.parse(v)
        setattr(obj,objattr,v)
      
def convert_sex(v):
    if v in ('W','F'): return 'F'
    if v == 'M': return 'M'
    return None
      
def isolang(x):
    if x == 'K' : return 'et'
    if x == 'E' : return 'en'
    if x == 'D' : return 'de'
    if x == 'F' : return 'fr'
    if x == 'N' : return 'nl'
      
def ADR_id(cIdAdr):
    assert len(cIdAdr) == 3
    #~ assert [cIdAdr:-3] == '000'
    try:
        return 199000+int(cIdAdr)
    except ValueError,e:
        return None




def par2client(row,person):
    #~ person.is_active = iif(row['IDPRT']=='I',False,True)
    if row['IDPRT'] == 'S':
        person.is_cpas = True
    elif row['IDPRT'] == 'A':
        person.is_senior = True
        

def checkcc(person,pk,nType):
    #~ pk = ADR_id(cIdAdr)
    try:
        Company.objects.get(pk=pk)
    #~ except ValueError,e:
        #~ dblogger.warning(u"%s : invalid health_insurance or pharmacy %r",obj2str(person),cIdAdr)
        #~ return
    except Company.DoesNotExist,e:
        raise Exception(
            "%s : Pharmacy or Health Insurance %s doesn't exist" % 
            (obj2str(person),pk))
        #~ dblogger.warning(u"%s : Company %s doesn't exist (please create manually in Lino).",
            #~ obj2str(person),pk)
        #~ return
    qs = pcsw.ClientContact.objects.filter(
        client=person,
        type__id=nType)
    if qs.count() == 0:
        cc = pcsw.ClientContact(
            client=person,
            company_id=pk,
            type=pcsw.ClientContactType.objects.get(id=nType))
        cc.save()
        changes.log_create(REQUEST,cc)
    elif qs.count() == 1:
        cc = qs[0]
        if cc.company_id != pk:
            watcher = changes.Watcher(cc)
            cc.company_id = pk
            cc.save()
            watcher.log_diff(REQUEST)
    else:
        dblogger.warning(u"%s : more than 1 ClientContact (type=%r)",obj2str(person),nType)



def pxs2client(row,person):
  
    kw = {}
    store(kw,
      card_number=row['CARDNUMBER'],
      card_issuer=row.get('CARDISSUER',''),      # 20110110
      noble_condition=row.get('NOBLEECOND',''),      # 20110110
      birth_place=row.get('BIRTHPLACE',''),
      remarks2=row.get('MEMO',''),
      gender=convert_sex(row['SEXE'])
    )
    for k,v in kw.items():
        setattr(person,k,v)
    
    par2client(row,person)    
        
    if row.has_key('CARDTYPE'):
        #~ row.card_type = pcsw.BeIdCardType.items_dict.get(row['CARDTYPE'].strip(),'')
        #~ from lino.apps.pcsw import models as pcsw
        if row['CARDTYPE'] == 0:
            #~ person.card_type = pcsw.BeIdCardType.blank_item
            person.card_type = ''
        else:
            person.card_type = pcsw.BeIdCardType.get_by_value(str(row['CARDTYPE']))
            
    if row['IDMUT']:
        checkcc(person,ADR_id(row['IDMUT']),CCTYPE_HEALTH_INSURANCE)
    if row['APOTHEKE']:
        checkcc(person,row['APOTHEKE'],CCTYPE_PHARMACY)
        
        #~ try:
            #~ person.pharmacy = Company.objects.get(pk=int(row['APOTHEKE']))
        #~ except ValueError,e:
            #~ dblogger.warning(u"%s : invalid pharmacy %r",obj2str(person),row['APOTHEKE'])
        #~ except Company.DoesNotExist,e:
            #~ dblogger.warning(u"%s : pharmacy %s not found",obj2str(person),row['APOTHEKE'])
            
    nat = row['NATIONALIT']
    if nat:
        try:
            country = Country.objects.get(short_code__exact=nat)
        except Country.DoesNotExist:
            country = Country(isocode=nat,name=nat,short_code=nat)
            country.save()
        person.nationality=country
        
    store_date(row,person,'GEBDAT','birth_date')
    store_date(row,person,'VALID1','card_valid_from')
    store_date(row,person,'VALID2','card_valid_until')
            


def country2kw(row,kw):
    # for both PAR and ADR
    
    if row.has_key('PROF'):
        activity = row['PROF']
        if activity:
            try:
                activity = int(activity)
            except ValueError:
                dblogger.debug("Ignored invalid value PROF = %r",activity)
            else:
                if activity:
                    try:
                        activity = pcsw.Activity.objects.get(pk=activity)
                    except pcsw.Activity.DoesNotExist:
                        activity = pcsw.Activity(id=activity,name=unicode(activity))
                        activity.save(force_insert=True)
                    kw.update(activity=activity)
        
    country = row['PAYS']
    if country:
        try:
            country = Country.objects.get(short_code__exact=country)
        except Country.DoesNotExist:
            country = Country(isocode=country,name=country,short_code=country)
            country.save()
        kw.update(country=country)
    
    email = row['EMAIL']
    if email and is_valid_email(email):
        kw.update(email=email)
    store(kw,
      phone=row['TEL'],
      fax=row['FAX'],
      )
      
    kw.update(street2kw(join_words(row['RUE'],row['RUENUM'],row['RUEBTE'])))
    
    zip_code = row['CP']
    if zip_code:
        kw.update(zip_code=zip_code)
        try:
            city = City.objects.get(
              country=country,
              zip_code__exact=zip_code,
              )
            kw.update(city=city)
        except City.DoesNotExist,e:
            city = City(zip_code=zip_code,name=zip_code,country=country)
            city.save()
            kw.update(city=city)
            #~ dblogger.warning("%s-%s : %s",row['PAYS'],row['CP'],e)
        except City.MultipleObjectsReturned,e:
            dblogger.warning("%s-%s : %s",row['PAYS'],row['CP'],e)



#~ def is_company(data):
def PAR_model(data):
    """
    - wer eine NISS oder Gesdos-Nr hat ist ein Klient, selbst wenn er auch eine MwSt-Nummer hat.
    - Neuzugänge (Attribut N) sind ebenfalls immer Klienten
    
    """
    if data.get('NB2',False): # NISS
        return Client
    if data.get('NB1',False): # gesdos-Nr
        return Client
    attribs = data.get('ATTRIB',False)
    if attribs and 'N' in attribs: # newcomer
        return Client
    if data.get('NOTVA',False):
        return Company
    if data.get('ALLO','') in (u"Eheleute",):
        return Household
    return Person
    

    
def json2py(dct):
    if '__date__' in dct:
        d = dct['__date__']
        if d['year'] == 0 or d['month'] == 0 or d['day'] == 0:
            return None
        try:
            return datetime.date(d['year'], d['month'],d['day'])
        except ValueError,e:
            raise ValueError("%s : %s", dct,e)
    return dct
    

#~ def data2kw(data,kw,**d):
    #~ for k,n in d.items():
        #~ if data.has_key(n):
            #~ kw[k] = data[n]


CONTACT_FIELDS = '''id name street street_no street_box addr2 
country city zip_code region language email url phone gsm remarks'''.split()

#~ class PseudoRequest:
    #~ user = "watch_tim"
#~ REQUEST = PseudoRequest()

REQUEST = changes.PseudoRequest("watch_tim")
#~ 20120921 REQUEST = dblogger.PseudoRequest("watch_tim")

class Controller:
    "Deserves more documentation."
    allow_put2post = True
    def applydata(self,obj,data,**mapper):
        """
        Stores values from `data` into `obj` using mapper.
        `mapper` is a `dict` whose keys are Lino field names and whose values are TIM field names.
        e.g. something like `dict(id='IDPAR',street='STREET')`.
        Deserves more documentation.
        """
        for lino_name,tim_name in mapper.items():
            if data.has_key(tim_name):
                setattr(obj,lino_name,data[tim_name])
        settings.TIM2LINO_LOCAL(self.__class__.__name__,obj)
        
    def validate_and_save(self,obj):
        "Deserves more documentation."
        dblogger.info("20121022 validate_and_save %s",obj2str(obj,True))
        obj.full_clean()
        #~ 20120921 dblogger.log_changes(REQUEST,obj)
        obj.save()
                
    def old_validate_and_save(self,obj):
        "Deserves more documentation."
        try:
            obj.full_clean()
            #~ 20120921 dblogger.log_changes(REQUEST,obj)
            obj.save()
        except ValidationError,e:
            # here we only log an obj2str() of the object 
            # full traceback will be logged in watch() after process_line()
            dblogger.warning("Validation failed for %s : %s",obj2str(obj),e)
            raise # re-raise (propagate) exception with original traceback
            #~ dblogger.exception(e)
                
    def get_object(self,kw):
        raise NotImplementedError
        
    def DELETE(self,**kw):
        obj = self.get_object(kw)
        if obj is None:
            dblogger.warning("%s:%s : DELETE failed (does not exist)",
                kw['alias'],kw['id'])
            return
        msg = obj.disable_delete(ar)
        if msg:
            dblogger.warning("%s:%s : DELETE failed: %s",kw['alias'],kw['id'],msg)
            return
            
        #~ 20120921 dblogger.log_deleted(REQUEST,obj)
        changes.log_delete(REQUEST,obj)
        obj.delete()
        dblogger.debug("%s:%s (%s) : DELETE ok",kw['alias'],kw['id'],obj2str(obj))
        
    #~ def prepare_data(self,data):
        #~ return data
        
    def create_object(self,kw):
        return self.model()
                    
    def POST(self,**kw):
        #~ dblogger.info("%s.POST(%s)",self.__class__.__name__,kw)
        #~ self.prepare_data(kw['data'])
        obj = self.get_object(kw)
        if obj is None:
            obj = self.create_object(kw)
            if obj is None:
                dblogger.warning("%s:%s (%s) : ignored POST %s",
                    kw['alias'],kw['id'],obj,kw['data'])
                return
            #~ watcher = changes.Watcher(obj,True)
            self.applydata(obj,kw['data'])
            dblogger.debug("%s:%s (%s) : POST %s",kw['alias'],kw['id'],obj2str(obj),kw['data'])
            self.validate_and_save(obj)
            changes.log_create(REQUEST,obj)
        else:
            watcher = changes.Watcher(obj)
            dblogger.info("%s:%s : POST becomes PUT",kw['alias'],kw['id'])
            self.applydata(obj,kw['data'])
            dblogger.debug("%s:%s (%s) : POST %s",kw['alias'],kw['id'],obj2str(obj),kw['data'])
            self.validate_and_save(obj)
            watcher.log_diff(REQUEST)
            #~ obj.save()
        
    def PUT(self,**kw):
        #~ dblogger.info("%s.PUT(%s)",self.__class__.__name__,kw)
        obj = self.get_object(kw)
        if obj is None:
            if self.allow_put2post:
                dblogger.info("%s:%s : PUT becomes POST",kw['alias'],kw['id'])
                kw['method'] = 'POST'
                return self.POST(**kw)
            else:
                dblogger.warning("%s:%s : PUT ignored (row does not exist)",kw['alias'],kw['id'])
                return 
        watcher = changes.Watcher(obj)
        if self.PUT_special(watcher,**kw):
            return 
        self.applydata(obj,kw['data'])
        dblogger.debug("%s:%s (%s) : PUT %s",kw['alias'],kw['id'],obj2str(obj),kw['data'])
        self.validate_and_save(obj)
        watcher.log_diff(REQUEST)
        #~ obj.save()
        #~ dblogger.debug("%s:%s : PUT %s",kw['alias'],kw['id'],kw['data'])
        
    def PUT_special(self,watcher,**kw):
        pass
        
def ADR_applydata(obj,data,**kw):
    #~ kw.update(
        #~ street='RUE',
        #~ street_box='RUEBTE',
        #~ phone='TEL',
    #~ )
    #~ if data.has_key('RUENUM'):
        #~ obj.street_no = data['RUENUM'].strip()
    #~ kw = {}
    country2kw(data,kw)
    for k,v in kw.items():
        setattr(obj,k,v)
    
                
class PAR(Controller):
    "Deserves more documentation."
  
    #~ def prepare_data(self,data):
        #~ if data['NB2']:
            #~ if not is_valid_niss(data['NB2']):
                #~ dblogger.warning("Ignored invalid NISS %s" % data['NB2'])
                #~ data['NB2'] = ''
        #~ return data
                
    def applydata(self,obj,data,**mapper):
        mapper.update(
            id='IDPAR', 
            remarks='MEMO',
            bank_account1='COMPTE1',
            bank_account2='COMPTE2',
        )
        ADR_applydata(obj,data) # ,**mapper)
        #~ kw.update(street2kw(join_words(data['RUE'],
        
        store_date(data,obj,'DATCREA','created')
        
        
        if data.has_key('LANGUE'):
            obj.language = isolang(data['LANGUE'])
        
        
        #~ dblogger.info("20111223 %r",data)
        if data.has_key('ATTRIB'):
            #~ obj.newcomer = ("N" in data['ATTRIB'])
            #~ obj.is_deprecated = ("A" in data['ATTRIB'] or "W" in data['ATTRIB'])
            obj.is_obsolete = ("W" in data['ATTRIB'])
        
        if issubclass(obj.__class__,Person):
            #~ mapper.update(title='ALLO')
            title = data.get('ALLO','')
            if title in ("Herr","Herrn","Frau",u"Fräulein","Madame","Monsieur"):
                title = ''
            obj.title = title
            if data.has_key('FIRME'):
                for k,v in name2kw(data['FIRME']).items():
                    setattr(obj,k,v)
            if obj.__class__ is Client:
                par2client(data,obj)
                mapper.update(gesdos_id='NB1')
                if data.has_key('NB2'):
                    obj.national_id = data['NB2']
                    #~ if obj.national_id: 
                        #~ if not is_valid_niss(obj.national_id):
                            #~ dblogger.info("%s : invalid SSIN %s",obj2str(obj),obj.national_id)
                            #~ obj.national_id = None
                #~ else 20121108:
                    #~ obj.national_id = str(obj.id)
                    #~ if obj.is_deprecated:
                        #~ obj.national_id += ' (A)'
                if data.has_key('ATTRIB') and "N" in data['ATTRIB']:
                    obj.client_state = pcsw.ClientStates.newcomer
                elif data['IDPRT'] == 'I':
                    obj.client_state = pcsw.ClientStates.former
                #~ 
                elif obj.national_id and is_valid_niss(obj.national_id):
                    obj.client_state = pcsw.ClientStates.coached
                else:
                    obj.client_state = pcsw.ClientStates.invalid
                #~ if data.has_key('NB1'):
                    #~ obj.gesdos_id = data['NB1']
                #~ if not obj.national_id:
                    #~ obj.national_id = str()
                if data.has_key('IDUSR'):
                    username = settings.TIM2LINO_USERNAME(data['IDUSR'])
                    if obj.pk is None:
                        obj.save() # must force a pre save() here to save related coachings
                    if username:
                        u = users.User.objects.get(username=username)
                        #~ try:
                            #~ u = users.User.objects.get(username=username)
                        #~ except users.User.DoesNotExist,e:
                            #~ dblogger.warning(
                              #~ u"PAR->IdUsr %r (converted to %r) doesn't exist! while saving %s",
                              #~ data['IDUSR'],username,obj2str(obj))
                        #~ obj.coach1 = u
                        """
                        typical cases:
                        - imported client has got assign_coach in Lino, then removed PARATTR_N in TIM
                        """
                        try:
                            coaching = pcsw.Coaching.objects.get(client=obj,primary=True)
                            #~ if coaching.user != u or coaching.start_date != obj.created or coaching.end_date is not None:
                            if coaching.user != u or coaching.end_date is not None or coaching.start_date is None:
                                watcher = changes.Watcher(coaching)
                                coaching.user = u
                                if coaching.start_date is None:
                                    coaching.start_date = obj.created
                                coaching.end_date = None
                                coaching.save()
                                watcher.log_diff(REQUEST)
                        except pcsw.Coaching.DoesNotExist,e:
                            try:
                                coaching = pcsw.Coaching.objects.get(client=obj,user=u,end_date__isnull=True)
                                watcher = changes.Watcher(coaching)
                                coaching.primary = True
                                coaching.save()
                                watcher.log_diff(REQUEST)
                            except pcsw.Coaching.DoesNotExist,e:
                                coaching = pcsw.Coaching(client=obj,primary=True,user=u,start_date=obj.created)
                                coaching.save()
                                changes.log_create(REQUEST,coaching)
                            except Exception,e:
                                raise Exception("More than one primary coaching for %r by %r" % (obj,u))
                        except Exception,e:
                            raise Exception("More than one primary coaching for %r : %s" % (obj,e))

                    else:
                        #~ obj.coach1 = None
                        try:
                            coaching = pcsw.Coaching.objects.get(client=obj,primary=True)
                            changes.log_delete(REQUEST,coaching)
                            coaching.delete()
                            
                        except pcsw.Coaching.DoesNotExist,e:
                            pass
                        
        elif obj.__class__ is Company:
            mapper.update(prefix='ALLO')
            mapper.update(vat_id='NOTVA')
            mapper.update(name='FIRME')
        elif obj.__class__ is Household:
            #~ mapper.update(prefix='ALLO')
            #~ mapper.update(vat_id='NOTVA')
            mapper.update(name='FIRME')
            if data.get('ALLO','') == "Eheleute":
                obj.type = households_Type.objects.get(pk=1)
            
        Controller.applydata(self,obj,data,**mapper)
        
    def get_object(self,kw):
        id = kw['id']
        if not id:
            return None
        #~ possible_models = [Client, Person, Company, Household, Partner]
        #~ model = PAR_model(kw['data'])
        #~ delete_child
        #~ try:
            #~ return model.objects.get(pk=id)
        #~ except model.DoesNotExist:
            #~ pass
        try:
            return Client.objects.get(pk=id)
        except Client.DoesNotExist:
            pass
        try:
            return Person.objects.get(pk=id)
        except Person.DoesNotExist:
            pass
        try:
            return Company.objects.get(pk=id)
        except Company.DoesNotExist:
            pass
        try:
            return Household.objects.get(pk=id)
        except Household.DoesNotExist:
            pass
        
    def PUT_special(self,watcher,**kw):
        obj = watcher.watched
        model = PAR_model(kw['data'])
        if obj.__class__ != model:
            dblogger.info("%s:%s (%s) : %s becomes %s",kw['alias'],kw['id'],obj2str(obj),
                obj.__class__.__name__,model.__name__)
            self.swapclass(watcher,model,kw['data'])
            return True
            
    def swapclass(self,watcher,new_class,data):
        obj = watcher.watched
        #~ kw = {}
        #~ for n in CONTACT_FIELDS:
            #~ kw[n] = getattr(obj,n)
            #~ v = data.get(n,None)
            #~ if v is not None:
                #~ kw[n] = v
        old_class = obj.__class__
        if issubclass(old_class,new_class):
            #~ it was a Client and becomes a Person
            changes.log_remove_child(REQUEST,obj,old_class)
            mti.delete_child(obj,old_class)
            #~ changes.log_delete(REQUEST,obj)
            newobj = new_class.objects.get(pk=obj.id)
        elif issubclass(new_class,old_class):
            #~ it was only a Person and becomes a Client
            changes.log_add_child(REQUEST,obj,new_class)
            newobj = mti.insert_child(obj,new_class)
        else:
            obj = obj.partner_ptr
            changes.log_remove_child(REQUEST,obj,old_class)
            mti.delete_child(obj,old_class)
            changes.log_add_child(REQUEST,obj,new_class)
            newobj = mti.insert_child(obj,new_class)
            
        self.applydata(newobj,data)
        self.validate_and_save(newobj)
        return newobj
        
    def create_object(self,kw):
        return PAR_model(kw['data'])(id=kw['id'])
        #~ if is_company(kw['data']):
            #~ return Company()
        #~ else:
            #~ return Person()
      
    #~ def POST(self,**kw):
        #~ self.applydata(obj,kw['data'])
        #~ self.validate_and_save(obj)
        #~ dblogger.debug("%s:%s (%s): POST %s",kw['alias'],kw['id'],obj,kw['data'])
            

class PXS(Controller):
    "Controller for importing PXS changes to Person."
  
    allow_put2post = False
    """This is False because the following case cannot be resolved: 
    a Person that exists in TIM but not in Lino gets her PXS modified in TIM. 
    TIM issues a PUT on PXS. Lino cannot convert this into a POST and create 
    the person because e.g. name ist not known.
    
    TIM schreibt beim Erstellen eines neuen Partners logischerweise 
    sowohl für PAR als auch für PXS ein POST. Weil die beiden in Lino 
    aber eine einzige Tabelle sind, bekamen wir dann beim POST des PXS 
    eine Fehlermeldung "Partner with this id already exists".
        
    """
    
    def create_object(self,kw):
        raise Exception("Tried to create a Person from PXS")
        
    def PUT_special(self,watcher,**kw):
        pass
        
    def get_object(self,kw):
        id = kw['id']
        try:
            return pcsw.Client.objects.get(pk=id)
        except pcsw.Client.DoesNotExist:
            pass
            
    def applydata(self,obj,data,**d):
        d.update(
            card_number='CARDNUMBER',
            birth_place='BIRTHPLACE',
            birth_date='GEBDAT',
        )
        Controller.applydata(self,obj,data,**d)
        pxs2client(data,obj)
        
    #~ def POST(self,**kw):
        #~ """Deserves more documentation."""
        # Don't use the POST defined in PAR!
        #~ return Controller.POST(self,**kw)
        #~ self.PUT(**kw)
        
        
#~ class PLZ(PAR): # 20121003 why was this? caused AttributeError 'City' object has no attribute 'street'
class PLZ(Controller):
  
    model = City
    
    def get_object(self,kw):
        id = kw['id']
        if len(id) != 2:
            raise Exception("%r : invalid id for PLZ" % id)
        try:
            return self.model.objects.get(
              country__short_code__exact=id[0],
              zip_code__exact=id[1],
              )
        except self.model.DoesNotExist:
            pass
            
    def applydata(self,obj,data,**d):
        d.update(
            name='NOM',
            zip_code='CP',
        )
        try:
            obj.country = Country.objects.get(short_code__exact=data['PAYS'])
        except Country.DoesNotExist:
            pass  
        Controller.applydata(self,obj,data,**d)

class NAT(Controller):
  
    model = Country
    
    def get_object(self,kw):
        id = kw['id']
        try:
            return Country.objects.get(short_code__exact=id)
        except Country.DoesNotExist:
            pass
            
    def applydata(self,obj,data,**d):
        d.update(
            short_code='IDNAT',
            name='NAME',
            isocode='ISOCODE',
        )
        Controller.applydata(self,obj,data,**d)


class ADR(Controller):
    u"""
    Aus ADR werden nur die Krankenkassen (d.h. ADR->IdMut nicht leer)
    nach Lino übernommen, 
    wobei `Company.id = 199000 + int(ADR->IdMut)`.
    """
    model = Company
    
    def create_object(self,kw):
        "Returns None if ADR->IdMut is empty or invalid."
        idmut = kw['data']['IDMUT']
        if idmut:
            pk = ADR_id(idmut)
            if pk:
                return Company(id=pk)
      
    def get_object(self,kw):
        idmut = kw['data']['IDMUT']
        if idmut:
            pk = ADR_id(idmut)
            if pk:
                try:
                    return Company.objects.get(id__exact=pk)
                except Company.DoesNotExist:
                    pass
            
    def applydata(self,obj,data,**d):
        d.update(
            name='NAME',
        )
        ADR_applydata(obj,data,**d)
        Controller.applydata(self,obj,data,**d)


controllers = dict(
  NAT=NAT(),
  PLZ=PLZ(),
  PAR=PAR(),
  PXS=PXS(),
  ADR=ADR(),
  )

def process_line(i,ln):
    dblogger.debug("process_line(%r,%r)",i,ln)
    d = simplejson.loads(ln,object_hook=json2py)
    kw = {}
    for k,v in d.items():
        kw[str(k)] = v
    ctrl = controllers.get(kw['alias'],None)
    if ctrl is None:
        raise Exception("%(alias)s : no such controller." % kw)
        #~ logger.debug("Ignoring change %s for %(alias)s:%(id)s",kw['time'],kw['alias'],kw['id'])
        #~ return
    #~ kw['data'] = ctrl.prepare_data(kw['data'])
    m = getattr(ctrl,kw['method'])
    m(**kw)
    
  
def watch(data_dir):
    "Deserves more documentation."
    infile = os.path.join(data_dir,'changelog.json')
    if not os.path.exists(infile):
        #~ print "Nothing to do."
        return
        
    watching = os.path.join(data_dir,'changelog.watching.json')
    if not os.path.exists(watching):
        try:
            os.rename(infile,watching)
        except Exception,e:
            dblogger.debug("Could not rename %s to %s: %s",infile,watching,e)
            return
    dblogger.info("Processing file %s",watching)
    fd_watching = codecs.open(watching,'r',encoding='cp850')
    
    failed = os.path.join(data_dir,'changelog.failed.json')
    fd_failed = codecs.open(failed,'a',encoding='cp850')
    #~ log = open(os.path.join(data_dir,'changelog.done.log'),'a')
    i = 0
    for ln in fd_watching.readlines():
        i += 1
        try:
            process_line(i,ln)
        except Exception,e:
            #~ raise
            fd_failed.write("// %s %r\n%s\n\n" % (
                time.strftime("%Y-%m-%d %H:%M:%S"),e,ln))
            #~ fd_failed.write(ln+'\n')
            #~ dblogger.warning("%s:%d: %r\nin changelog line %s", watching,i,e,ln)
            dblogger.warning(
                "Exception '%r' while processing changelog line:\n%s", 
                e,ln)
            # for ValidationError we don't want a full traceback with mail to the admins.
            if not isinstance(e,ValidationError):
                dblogger.exception(e)
            #~ raise
    fd_watching.close()
    fd_failed.close()
    os.remove(watching)
    dblogger.info("%d changes have been processed.",i)
    #~ log.close()
        

def main(*args,**options):
    if len(args) != 1:
        raise CommandError('Please specify the path to your TIM changelog directory')
    data_dir = args[0]
    msg = "Started watch_tim %s on %s ..."
    #~ logger.info(msg,data_dir)
    dblogger.info(msg,lino.__version__,data_dir)
    
    settings.LINO.startup() 
        
    def goodbye():
        msg = "Stopped watch_tim %s on %s ..."
        #~ logger.info(msg,data_dir)
        dblogger.info(msg,lino.__version__,data_dir)
    #~ signal.signal(signal.SIGTERM,on_SIGTERM)
    atexit.register(goodbye)
    
    #~ last_warning = None
    while True:
        try:
            watch(data_dir)
        except Exception,e:
            dblogger.exception(e)
        time.sleep(1)

class Command(DaemonCommand):
  
    args = '<path_to_tim_changelog>'
    help = 'Starts an observer service that propagates changes of your TIM data into Lino'
    
    #~ stdout = '/var/log/lino/watch_tim.log' 
    #~ stdout = os.path.join(settings.PROJECT_DIR, "watch_tim","stdout.log")
    #~ stderr = '/var/log/lino/watch_tim.errors.log' 
    #~ os.path.join(settings.PROJECT_DIR, "watch_tim","errors.log")
    #~ pidfile = os.path.join(settings.PROJECT_DIR, "watch_tim","pid")
    #~ pidfile = '/var/run/watch_tim.pid' # os.path.j    
    
    #~ preserve_loggers = (logger,dblogger.logger)
    preserve_loggers = [dblogger.logger]
    
    def handle_daemon(self, *args, **options):
        main(*args,**options)


