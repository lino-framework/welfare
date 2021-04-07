# -*- coding: UTF-8 -*-
# Copyright 2010-2015 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

""".. management_command:: watch_tim

Starts a daemon that watches the specified directory for a file
:xfile:`changelog.json` to appear.  This is to synchronize changes
made in TIM to the Lino database.

"""

import os
import codecs
import time
import datetime
import json

from dateutil import parser as dateparser

from django.core.management.base import CommandError
from django.core.exceptions import ValidationError
from django.db import connection


from django.conf import settings

from django.db import IntegrityError
import six

from lino.core.utils import is_valid_email
from lino.core.diff import ChangeWatcher

from lino.api import dd, rt
from lino.mixins.human import name2kw
from lino_xl.lib.contacts.utils import street2kw
from lino.utils import join_words

from lino.utils import dblogger
from lino.utils import mti
#~ from lino.core import changes
#~ from lino.modlib import models as changes

from lino.utils.daemoncommand import DaemonCommand

from lino.utils.ssin import is_valid_ssin
from lino_xl.lib.beid.mixins import BeIdCardTypes


LONG_TIME_AGO = datetime.date(1990, 1, 1)

IGNORABLE_ERRORS = (ValidationError, IntegrityError)

#~ from lino_welfare.modlib.pcsw import models as pcsw
#~ from lino_welfare.modlib.pcsw.management.commands.initdb_tim import ADR_id

settings.SITE.startup()  # populate the model cache

pcsw = dd.resolve_app('pcsw')
users = dd.resolve_app('users')
#~ contacts = dd.resolve_app('contacts')
#~ households = dd.resolve_app('households')
#~ countries = dd.resolve_app('countries')

#~ Country = countries.Country
#~ Place = countries.Place
Country = dd.resolve_model('countries.Country')
Place = dd.resolve_model('countries.Place')
#~ Person = contacts.Person
#~ Person = pcsw.Person
#~ Company = contacts.Company
#~ Company = pcsw.Company
Person = dd.resolve_model('contacts.Person')
Client = dd.resolve_model('pcsw.Client')
Partner = dd.resolve_model('contacts.Partner')
#~ Client = pcsw.Client
Company = dd.resolve_model('contacts.Company')
Household = dd.resolve_model('households.Household')
households_Type = dd.resolve_model("households.Type")
#~ Household = pcsw.Household
#~ Household = households.Household
#~ households_Type = households.Type
from lino_xl.lib.clients.choicelists import ClientStates

CCTYPE_HEALTH_INSURANCE = 1
CCTYPE_PHARMACY = 2


def store(kw, **d):
    for k, v in d.items():
        if v is not None:
        # see :doc:`/blog/2011/0711`
        #~ if v:
            kw[k] = v


def store_date(row, obj, rowattr, objattr):
    v = row[rowattr]
    if v:
        if isinstance(v, six.string_types):
            v = dateparser.parse(v)
        setattr(obj, objattr, v)


def convert_sex(v):
    if v in ('W', 'F'):
        return 'F'
    if v == 'M':
        return 'M'
    return None


def isolang(x):
    if x == 'K':
        return 'et'
    if x == 'E':
        return 'en'
    if x == 'D':
        return 'de'
    if x == 'F':
        return 'fr'
    if x == 'N':
        return 'nl'
    return 'de'  # silently tolerate invalid values


def ADR_id(cIdAdr):
    if len(cIdAdr) != 3:
        return None
    try:
        return 199000 + int(cIdAdr)
    except ValueError:
        return None


def par2client(row, person):
    #~ person.is_active = iif(row['IDPRT']=='I',False,True)
    if row['IDPRT'] == 'S':
        person.is_cpas = True
    elif row['IDPRT'] == 'A':
        person.is_senior = True


def checkcc(person, pk, nType):
    #~ pk = ADR_id(cIdAdr)
    try:
        Company.objects.get(pk=pk)
    #~ except ValueError,e:
        #~ dblogger.warning(u"%s : invalid health_insurance or pharmacy %r",dd.obj2str(person),cIdAdr)
        #~ return
    except Company.DoesNotExist as e:
        raise Exception(
            "%s : Pharmacy or Health Insurance %s doesn't exist" %
            (dd.obj2str(person), pk))
        #~ dblogger.warning(u"%s : Company %s doesn't exist (please create manually in Lino).",
            #~ dd.obj2str(person),pk)
        #~ return
    qs = rt.models.clients.ClientContact.objects.filter(
        client=person,
        type__id=nType)
    if qs.count() == 0:
        cc = rt.models.clients.ClientContact(
            client=person,
            company_id=pk,
            type=rt.models.clients.ClientContactType.objects.get(id=nType))
        cc.save()
        dd.on_ui_created.send(sender=cc, request=REQUEST)
        #~ changes.log_create(REQUEST,cc)
    elif qs.count() == 1:
        cc = qs[0]
        if cc.company_id != pk:
            watcher = ChangeWatcher(cc)
            cc.company_id = pk
            cc.save()
            watcher.send_update(REQUEST)
            #~ watcher.log_diff(REQUEST)
    else:
        dblogger.warning(u"%s : more than 1 ClientContact (type=%r)",
                         dd.obj2str(person), nType)


def pxs2client(row, person):

    kw = {}
    store(kw,
          card_number=row['CARDNUMBER'],
          card_issuer=row.get('CARDISSUER', ''),      # 20110110
          noble_condition=row.get('NOBLEECOND', ''),      # 20110110
          birth_place=row.get('BIRTHPLACE', ''),
          remarks2=row.get('MEMO', ''),
          gender=convert_sex(row['SEXE'])
          )
    for k, v in kw.items():
        setattr(person, k, v)

    par2client(row, person)

    if 'CARDTYPE' in row:
        if row['CARDTYPE'] == 0:
            #~ person.card_type = BeIdCardTypes.blank_item
            person.card_type = ''
        else:
            person.card_type = BeIdCardTypes.get_by_value(str(row['CARDTYPE']))

    if row['IDMUT']:
        checkcc(person, ADR_id(row['IDMUT']), CCTYPE_HEALTH_INSURANCE)
    if row['APOTHEKE']:
        checkcc(person, row['APOTHEKE'], CCTYPE_PHARMACY)

        #~ try:
            #~ person.pharmacy = Company.objects.get(pk=int(row['APOTHEKE']))
        #~ except ValueError,e:
            #~ dblogger.warning(u"%s : invalid pharmacy %r",dd.obj2str(person),row['APOTHEKE'])
        #~ except Company.DoesNotExist,e:
            #~ dblogger.warning(u"%s : pharmacy %s not found",dd.obj2str(person),row['APOTHEKE'])

    nat = row['NATIONALIT']
    if nat:
        try:
            country = Country.objects.get(short_code__exact=nat)
        except Country.DoesNotExist:
            country = Country(isocode=nat, name=nat, short_code=nat)
            country.save()
        person.nationality = country

    store_date(row, person, 'GEBDAT', 'birth_date')
    store_date(row, person, 'VALID1', 'card_valid_from')
    store_date(row, person, 'VALID2', 'card_valid_until')


def country2kw(row, kw):
    # for both PAR and ADR

    if 'PROF' in row:
        activity = row['PROF']
        if activity:
            try:
                activity = int(activity)
            except ValueError:
                dblogger.info("Ignored invalid value PROF = %r", activity)
            else:
                if activity:
                    try:
                        activity = pcsw.Activity.objects.get(pk=activity)
                    except pcsw.Activity.DoesNotExist:
                        activity = pcsw.Activity(
                            id=activity, name=str(activity))
                        activity.save(force_insert=True)
                    kw.update(activity=activity)

    country = row['PAYS']
    if country:
        try:
            country = Country.objects.get(short_code__exact=country)
        except Country.DoesNotExist:
            country = Country(isocode=country, name=country,
                              short_code=country)
            country.save()
        kw.update(country=country)

        zip_code = row['CP']
        if zip_code:
            kw.update(zip_code=zip_code)
            try:
                city = Place.objects.get(
                    country=country,
                    zip_code__exact=zip_code,
                )
                kw.update(city=city)
            except Place.DoesNotExist as e:
                city = Place(zip_code=zip_code, name=zip_code, country=country)
                city.save()
                kw.update(city=city)
                #~ dblogger.warning("%s-%s : %s",row['PAYS'],row['CP'],e)
            except Place.MultipleObjectsReturned as e:
                dblogger.warning("%s-%s : %s", row['PAYS'], row['CP'], e)

    email = row['EMAIL']
    if email:
        if is_valid_email(email):
            kw.update(email=email)
        else:
            dblogger.warning("Ignoring invalid email address %s", email)
    store(kw,
          phone=row['TEL'],
          fax=row['FAX'],
          )

    kw.update(street2kw(join_words(row['RUE'], row['RUENUM'], row['RUEBTE'])))


#~ def is_company(data):
def PAR_model(data):
    """
    - wer eine SSIN oder Gesdos-Nr hat ist ein Klient, selbst wenn er auch eine Mwst-Nummer hat.
    - Neuzugänge (Attribut N) sind ebenfalls immer Klienten

    """
    has_first_name = len(data.get('FIRME', '').split()) > 1
    if has_first_name:
        nb2 = data.get('NB2', False)
        if nb2:  # SSIN
            if nb2.strip() == '0':
                data['NB2'] = ''
            else:
                return Client
        if data.get('NB1', False):  # gesdos-Nr
            if not data.get('NOTVA', False):
                return Client
        attribs = data.get('ATTRIB', False)
        if attribs and 'N' in attribs:  # newcomer
            return Client
        # ~ if data.get('IDUSR',False): # Sozi
            #~ return Client
    if data.get('NOTVA', False):
        return Company
    if data.get('ALLO', '') in (u"Eheleute",):
        return Household
    if has_first_name:
        return Person
    return Partner


def json2py(dct):
    if '__date__' in dct:
        d = dct['__date__']
        if d['year'] == 0 or d['month'] == 0 or d['day'] == 0:
            return None
        try:
            return datetime.date(d['year'], d['month'], d['day'])
        except ValueError as e:
            raise ValueError("%s : %s", dct, e)
    return dct


#~ def data2kw(data,kw,**d):
    #~ for k,n in d.items():
        #~ if data.has_key(n):
            #~ kw[k] = data[n]


#~ CONTACT_FIELDS = '''id name street street_no street_box addr1 addr2
#~ country city zip_code region language email url phone gsm remarks'''.split()

REQUEST = dd.PseudoRequest("watch_tim")


class Controller:

    "Deserves more documentation."
    allow_put2post = True

    def set_timestamp(self, timespec):
        d, t = timespec.split()
        self.today = dateparser.parse(d).date()
        if not isinstance(self.today, datetime.date):
            raise Exception("%r was parsed to %r" % (timespec, self.today))
        #~ self.today = parsedate(s)
        #~ return datetime.date(*settings.SITE.parse_date(s))

    def applydata(self, obj, data, **mapper):
        """
        Stores values from `data` into `obj` using mapper.
        `mapper` is a `dict` whose keys are Lino field names and whose values are TIM field names.
        e.g. something like `dict(id='IDPAR',street='STREET')`.
        Deserves more documentation.
        """
        for lino_name, tim_name in mapper.items():
            if tim_name in data:
                setattr(obj, lino_name, data[tim_name])
        settings.TIM2LINO_LOCAL(self.__class__.__name__, obj)

    def validate_and_save(self, obj):
        "Deserves more documentation."
        #~ dblogger.info("20121022 validate_and_save %s",dd.obj2str(obj,True))
        obj.full_clean()
        #~ 20120921 dblogger.log_changes(REQUEST,obj)
        obj.save()

    def old_validate_and_save(self, obj):
        "Deserves more documentation."
        try:
            obj.full_clean()
            #~ 20120921 dblogger.log_changes(REQUEST,obj)
            obj.save()
        except ValidationError as e:
            # here we only log an dd.obj2str() of the object
            # full traceback will be logged in watch() after process_line()
            dblogger.warning("Validation failed for %s : %s",
                             dd.obj2str(obj), e)
            raise  # re-raise (propagate) exception with original traceback
            #~ dblogger.exception(e)

    def get_object(self, kw):
        raise NotImplementedError

    def DELETE(self, **kw):
        obj = self.get_object(kw)
        if obj is None:
            dblogger.warning("%s:%s : DELETE failed (does not exist)",
                             kw['alias'], kw['id'])
            return
        msg = obj.disable_delete(REQUEST)
        if msg:
            dblogger.warning("%s:%s : DELETE failed: %s",
                             kw['alias'], kw['id'], msg)
            return

        #~ 20120921 dblogger.log_deleted(REQUEST,obj)
        dd.pre_ui_delete.send(sender=obj, request=REQUEST)
        #~ changes.log_delete(REQUEST,obj)
        obj.delete()
        dblogger.info("%s:%s (%s) : DELETE ok",
                      kw['alias'], kw['id'], dd.obj2str(obj))

    #~ def prepare_data(self,data):
        #~ return data

    def create_object(self, kw):
        return self.model()

    def POST(self, **kw):
        #~ dblogger.info("%s.POST(%s)",self.__class__.__name__,kw)
        #~ self.prepare_data(kw['data'])
        obj = self.get_object(kw)
        if obj is None:
            obj = self.create_object(kw)
            if obj is None:
                dblogger.warning("%s:%s (%s) : ignored POST %s",
                                 kw['alias'], kw['id'], obj, kw['data'])
                return
            #~ watcher = changes.Watcher(obj,True)
            self.set_timestamp(kw['time'])
            self.applydata(obj, kw['data'])
            dblogger.info("%s:%s (%s) : POST %s",
                          kw['alias'], kw['id'], dd.obj2str(obj), kw['data'])
            self.validate_and_save(obj)
            dd.on_ui_created.send(sender=obj, request=REQUEST)
            #~ changes.log_create(REQUEST,obj)
        else:
            watcher = ChangeWatcher(obj)
            dblogger.info("%s:%s : POST becomes PUT", kw['alias'], kw['id'])
            self.set_timestamp(kw['time'])
            self.applydata(obj, kw['data'])
            dblogger.info("%s:%s (%s) : POST %s",
                          kw['alias'], kw['id'], dd.obj2str(obj), kw['data'])
            self.validate_and_save(obj)
            watcher.send_update(REQUEST)
            #~ watcher.log_diff(REQUEST)
            #~ obj.save()

    def PUT(self, **kw):
        #~ dblogger.info("%s.PUT(%s)",self.__class__.__name__,kw)
        obj = self.get_object(kw)
        if obj is None:
            if self.allow_put2post:
                dblogger.info("%s:%s : PUT becomes POST",
                              kw['alias'], kw['id'])
                kw['method'] = 'POST'
                return self.POST(**kw)
            else:
                dblogger.warning(
                    "%s:%s : PUT ignored (row does not exist)", kw['alias'], kw['id'])
                return
        watcher = ChangeWatcher(obj)
        if self.PUT_special(watcher, **kw):
            return
        self.set_timestamp(kw['time'])
        self.applydata(obj, kw['data'])
        dblogger.info("%s:%s (%s) : PUT %s",
                      kw['alias'], kw['id'], dd.obj2str(obj), kw['data'])
        self.validate_and_save(obj)
        watcher.send_update(REQUEST)
        #~ watcher.log_diff(REQUEST)
        #~ obj.save()
        #~ dblogger.info("%s:%s : PUT %s",kw['alias'],kw['id'],kw['data'])

    def PUT_special(self, watcher, **kw):
        pass


def ADR_applydata(obj, data, **kw):
    #~ kw.update(
        #~ street='RUE',
        #~ street_box='RUEBTE',
        #~ phone='TEL',
    #~ )
    #~ if data.has_key('RUENUM'):
        #~ obj.street_no = data['RUENUM'].strip()
    #~ kw = {}
    country2kw(data, kw)
    for k, v in kw.items():
        setattr(obj, k, v)


class PAR(Controller):

    """
    Controller for synchronizing PAR from TIM to Lino.
    Remember the possible hierarchy of "partner" models coming from TIM::

      Partner
      - Company
      - Household
      - Person
        - Client

    """

    #~ def prepare_data(self,data):
        #~ if data['NB2']:
            #~ if not is_valid_ssin(data['NB2']):
                #~ dblogger.warning("Ignored invalid SSIN %s" % data['NB2'])
                #~ data['NB2'] = ''
        #~ return data

    def applydata(self, obj, data, **mapper):
        mapper.update(
            id='IDPAR',
            remarks='MEMO',
            bank_account1='COMPTE1',
            bank_account2='COMPTE2',
        )
        ADR_applydata(obj, data)  # ,**mapper)
        #~ kw.update(street2kw(join_words(data['RUE'],

        store_date(data, obj, 'DATCREA', 'created')

        if 'LANGUE' in data:
            obj.language = isolang(data['LANGUE'])

        #~ dblogger.info("20111223 %r",data)
        if 'ATTRIB' in data:
            #~ obj.newcomer = ("N" in data['ATTRIB'])
            #~ obj.is_obsolete = ("A" in data['ATTRIB'] or "W" in data['ATTRIB'])
            obj.is_obsolete = ("W" in data['ATTRIB'])

        if issubclass(obj.__class__, Person):
            #~ mapper.update(title='ALLO')
            title = data.get('ALLO', '')
            if title in ("Herr", "Herrn", "Frau", u"Fräulein", "Madame", "Monsieur"):
                title = ''
            obj.title = title
            if 'FIRME' in data:
                for k, v in name2kw(data['FIRME']).items():
                    setattr(obj, k, v)
            if 'NAME2' in data:
                setattr(obj, 'addr1', data['NAME2'])
            if obj.__class__ is Client:
                par2client(data, obj)
                mapper.update(gesdos_id='NB1')
                if 'NB2' in data:
                    obj.national_id = data['NB2'] or None
                    #~ if obj.national_id:
                        #~ if not is_valid_ssin(obj.national_id):
                            #~ dblogger.info("%s : invalid SSIN %s",dd.obj2str(obj),obj.national_id)
                            #~ obj.national_id = None
                #~ else 20121108:
                    #~ obj.national_id = str(obj.id)
                    #~ if obj.is_deprecated:
                        #~ obj.national_id += ' (A)'
                if 'ATTRIB' in data and "N" in data['ATTRIB']:
                    obj.client_state = ClientStates.newcomer
                elif data['IDPRT'] == 'I':
                    obj.client_state = ClientStates.former
                #~
                else:
                    obj.client_state = ClientStates.coached
                #~ elif obj.national_id and is_valid_ssin(obj.national_id):
                    #~ obj.client_state = ClientStates.coached
                #~ else:
                    #~ obj.client_state = ClientStates.invalid
                #~ if data.has_key('NB1'):
                    #~ obj.gesdos_id = data['NB1']
                #~ if not obj.national_id:
                    #~ obj.national_id = str()
                if 'IDUSR' in data:
                    username = settings.TIM2LINO_USERNAME(data['IDUSR'])
                    if username:
                        #~ print 20130222, username
                        u = users.User.get_by_username(username)
                        #~ u = users.User.objects.get(username=username)
                        """
                        typical cases:
                        - imported client has been assigned a coach in Lino,
                          then filled IDUSR and removed PARATTR_N in TIM
                        """
                    else:
                        u = None

                    if obj.pk is None:
                        # must pre-save the client here to save related
                        # coachings
                        obj.save()

                    try:
                        coaching = rt.models.coachings.Coaching.objects.get(
                            client=obj, primary=True)
                    except rt.models.coachings.Coaching.DoesNotExist as e:
                        try:
                            coaching = rt.models.coachings.Coaching.objects.get(
                                client=obj, user=u, end_date__isnull=True)
                            watcher = ChangeWatcher(coaching)
                            coaching.primary = True
                            coaching.save()
                            watcher.send_update(REQUEST)
                            #~ watcher.log_diff(REQUEST)
                        except rt.models.coachings.Coaching.DoesNotExist as e:
                            if u is not None:
                                coaching = rt.models.coachings.Coaching(
                                    client=obj, primary=True, user=u,
                                    type=u.coaching_type,
                                    start_date=obj.created)
                                coaching.save()
                                dd.on_ui_created.send(
                                    sender=coaching, request=REQUEST)
                                #~ changes.log_create(REQUEST,coaching)
                        except Exception as e:
                            raise Exception(
                                "More than one active coaching for %r by %r" % (obj, u))

                    except Exception as e:
                        raise Exception(
                            "More than one primary coaching for %r : %s" % (obj, e))

                    else:
                        watcher = ChangeWatcher(coaching)
                        if u is None or u != coaching.user:
                            """
                            If the coach has changed, maintain the old coaching in history.
                            """
                            coaching.primary = False
                            coaching.end_date = self.today
                        else:
                            coaching.type = u.coaching_type
                            if coaching.start_date is None:
                                coaching.start_date = obj.created

                            if obj.client_state == ClientStates.coached:
                                coaching.end_date = None  # 1990
                            else:
                                #~ coaching.end_date = LONG_TIME_AGO
                                coaching.end_date = coaching.start_date

                        if watcher.is_dirty():
                            coaching.full_clean()
                            coaching.save()
                            watcher.send_update(REQUEST)

                        if u is not None and coaching.user != u:
                            """
                            create a new coaching
                            """
                            coaching = rt.models.coachings.Coaching(
                                client=obj, primary=True,
                                user=u,
                                type=u.coaching_type,
                                start_date=self.today)
                            coaching.save()
                            dd.on_ui_created.send(
                                sender=coaching, request=REQUEST)

        elif obj.__class__ is Company:
            #~ obj.prefix = data.get('ALLO','')
            mapper.update(prefix='ALLO')
            mapper.update(vat_id='NOTVA')
            mapper.update(name='FIRME')
        elif obj.__class__ is Household:
            #~ mapper.update(prefix='ALLO')
            #~ mapper.update(vat_id='NOTVA')
            mapper.update(name='FIRME')
            if data.get('ALLO', '') == "Eheleute":
                obj.type = households_Type.objects.get(pk=1)
        elif obj.__class__ is Partner:
            mapper.update(name='FIRME')
            mapper.update(prefix='ALLO')

        Controller.applydata(self, obj, data, **mapper)

    def get_object(self, kw):
        pk = kw['id']
        if not pk:
            return None
        pk = int(pk)
        if pk == 0:
            # mysql: "The database backend does not accept 0 as a value for
            # AutoField."
            return None
        #~ possible_models = [Client, Person, Company, Household, Partner]
        #~ model = PAR_model(kw['data'])
        #~ delete_child
        #~ try:
            #~ return model.objects.get(pk=id)
        #~ except model.DoesNotExist:
            #~ pass
        try:
            return Client.objects.get(pk=pk)
        except Client.DoesNotExist:
            pass
        try:
            return Person.objects.get(pk=pk)
        except Person.DoesNotExist:
            pass
        try:
            return Company.objects.get(pk=pk)
        except Company.DoesNotExist:
            pass
        try:
            return Household.objects.get(pk=pk)
        except Household.DoesNotExist:
            pass
        try:
            return Partner.objects.get(pk=pk)
        except Partner.DoesNotExist:
            pass

    def PUT_special(self, watcher, **kw):
        obj = watcher.watched
        model = PAR_model(kw['data'])
        if obj.__class__ != model:
            dblogger.info(
                "%s:%s (%s) : %s becomes %s", kw[
                    'alias'], kw['id'], dd.obj2str(obj),
                obj.__class__.__name__, model.__name__)
            self.swapclass(watcher, model, kw['data'])
            return True

    def swapclass(self, watcher, new_class, data):
        """
        Convert the watched object to a new_class instance and apply data accordingly.
        Caution: Here be dragons! See also :mod:`lino_welfare.tests.watchtim_tests`.

        """
        obj = watcher.watched
        old_class = obj.__class__
        assert old_class is not new_class
        newobj = None
        #~ print 20130222, old_class, new_class
        if old_class is Partner:
            partner = obj
        else:
            partner = obj.partner_ptr
        if old_class is Client:
            # convert Client to Person, then continue as if old_class had been
            # Person
            dd.pre_remove_child.send(
                sender=obj, request=REQUEST, child=old_class)
            mti.delete_child(obj, old_class)
            newobj = obj = obj.person_ptr
            old_class = Person

        if old_class is new_class:
            return

        #~ if new_class is not old_class and not issubclass(new_class,old_class):
        if not issubclass(new_class, old_class):
            dd.pre_remove_child.send(
                sender=obj, request=REQUEST, child=old_class)
            mti.delete_child(obj, old_class)
            newobj = obj = partner

        if new_class is Client:
            # create the Person if necessary:
            #~ partner = obj.partner_ptr
            try:
                person = Person.objects.get(pk=partner.id)
            except Person.DoesNotExist:
                dd.pre_add_child.send(
                    sender=partner, request=REQUEST, child=Person)
                person = mti.insert_child(partner, Person)
            self.applydata(person, data)
            self.validate_and_save(person)
            # create the Client
            newobj = obj = person

        if new_class is not Partner:
            dd.pre_add_child.send(sender=obj, request=REQUEST,
                                  child=new_class)
            newobj = mti.insert_child(obj, new_class)
        if newobj is not None:
            self.applydata(newobj, data)
            self.validate_and_save(newobj)

    def create_object(self, kw):
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

    def create_object(self, kw):
        raise Exception("Cannot create Client %s from PXS" % kw['id'])

    def PUT_special(self, watcher, **kw):
        pass

    def get_object(self, kw):
        id = kw['id']
        try:
            return pcsw.Client.objects.get(pk=id)
        except pcsw.Client.DoesNotExist:
            pass

    def applydata(self, obj, data, **d):
        d.update(
            card_number='CARDNUMBER',
            birth_place='BIRTHPLACE',
            birth_date='GEBDAT',
        )
        Controller.applydata(self, obj, data, **d)
        pxs2client(data, obj)

    #~ def POST(self,**kw):
        #~ """Deserves more documentation."""
        # Don't use the POST defined in PAR!
        #~ return Controller.POST(self,**kw)
        #~ self.PUT(**kw)


# ~ class PLZ(PAR): # 20121003 why was this? caused AttributeError 'Place' object has no attribute 'street'
class PLZ(Controller):

    model = Place

    def get_object(self, kw):
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

    def applydata(self, obj, data, **d):
        d.update(
            name='NOM',
            zip_code='CP',
        )
        try:
            obj.country = Country.objects.get(short_code__exact=data['PAYS'])
        except Country.DoesNotExist:
            pass
        Controller.applydata(self, obj, data, **d)


class NAT(Controller):

    model = Country

    def get_object(self, kw):
        id = kw['id']
        try:
            return Country.objects.get(short_code__exact=id)
        except Country.DoesNotExist:
            pass

    def applydata(self, obj, data, **d):
        d.update(
            short_code='IDNAT',
            name='NAME',
            isocode='ISOCODE',
        )
        Controller.applydata(self, obj, data, **d)


class ADR(Controller):

    u"""
    Aus ADR werden nur die Krankenkassen (d.h. ADR->IdMut nicht leer)
    nach Lino übernommen,
    wobei `Company.id = 199000 + int(ADR->IdMut)`.
    """
    model = Company

    def create_object(self, kw):
        "Returns None if ADR->IdMut is empty or invalid."
        idmut = kw['data']['IDMUT']
        if idmut:
            pk = ADR_id(idmut)
            if pk:
                return Company(id=pk)

    def get_object(self, kw):
        idmut = kw['data']['IDMUT']
        if idmut:
            pk = ADR_id(idmut)
            if pk:
                try:
                    return Company.objects.get(id__exact=pk)
                except Company.DoesNotExist:
                    pass

    def applydata(self, obj, data, **d):
        d.update(
            name='NAME',
        )
        ADR_applydata(obj, data, **d)
        Controller.applydata(self, obj, data, **d)


controllers = dict(
    #~ NAT=NAT(),
    #~ PLZ=PLZ(),
    PAR=PAR(),
    PXS=PXS(),
    ADR=ADR(),
)


def process_line(ln):
    d = json.loads(ln, object_hook=json2py)
    kw = {}
    for k, v in d.items():
        kw[str(k)] = v
    ctrl = controllers.get(kw['alias'], None)
    if ctrl is None:
        #~ raise Exception("%(alias)s : no such controller." % kw)
        #~ logger.debug("Ignoring change %(time)s for %(alias)s:%(id)s",kw['time'],kw['alias'],kw['id'])
        dblogger.info("Ignoring change %(time)s for %(alias)s:%(id)s", kw)
        return
    #~ kw['data'] = ctrl.prepare_data(kw['data'])
    m = getattr(ctrl, kw['method'])
    m(**kw)


def watch(data_dir):
    "Deserves more documentation."
    infile = os.path.join(data_dir, 'changelog.json')
    if not os.path.exists(infile):
        #~ print "Nothing to do."
        return

    watching = os.path.join(data_dir, 'changelog.watching.json')
    if not os.path.exists(watching):
        try:
            os.rename(infile, watching)
        except Exception as e:
            dblogger.debug("Could not rename %s to %s: %s",
                           infile, watching, e)
            return
    dblogger.info("Processing file %s", watching)
    fd_watching = codecs.open(watching, 'r', encoding='cp850')

    failed = os.path.join(data_dir, 'changelog.failed.json')
    fd_failed = codecs.open(failed, 'a', encoding='cp850')
    #~ log = open(os.path.join(data_dir,'changelog.done.log'),'a')
    i = 0
    for ln in fd_watching.readlines():
        i += 1
        dblogger.debug("process_line(%r,%r)", i, ln)
        try:
            process_line(ln)
        except Exception as e:
            #~ raise
            fd_failed.write("// %s %r\n%s\n\n" % (
                time.strftime("%Y-%m-%d %H:%M:%S"), e, ln))
            #~ fd_failed.write(ln+'\n')
            #~ dblogger.warning("%s:%d: %r\nin changelog line %s", watching,i,e,ln)
            dblogger.warning(
                "Exception '%r' while processing changelog line:\n%s",
                e, ln)
            # for ValidationError we don't want a full traceback with mail to
            # the admins.
            if not isinstance(e, IGNORABLE_ERRORS):
                dblogger.exception(e)
            #~ raise
    fd_watching.close()
    fd_failed.close()
    os.remove(watching)
    dblogger.info("%d changes have been processed.", i)
    #~ log.close()


def main(*args, **options):
    if len(args) != 1:
        raise CommandError(
            'Please specify the path to your TIM changelog directory')
    data_dir = args[0]
    #~ msg = "Started watch_tim %s on %s ..."
    #~ dblogger.info(msg,data_dir)
    #~ dblogger.info(msg,lino.__version__,data_dir)

    settings.SITE.startup()

    #~ def goodbye():
        #~ msg = "Stopped watch_tim %s on %s ..."
        #~ dblogger.info(msg,data_dir)
        #~ dblogger.info(msg,lino.__version__,data_dir)
    # ~ # signal.signal(signal.SIGTERM,on_SIGTERM)
    #~ atexit.register(goodbye)

    #~ last_warning = None
    while True:
        try:
            watch(data_dir)
        except Exception as e:
            dblogger.exception(e)
        connection.close()
        time.sleep(1)


class Command(DaemonCommand):

    args = '<path_to_tim_changelog>'
    help = 'Starts an observer service that propagates changes of your TIM data into Lino'

    #~ stdout = '/var/log/lino/watch_tim.log'
    #~ stdout = os.path.join(settings.PROJECT_DIR, "watch_tim","stdout.log")
    #~ stderr = '/var/log/lino/watch_tim.errors.log'
    #~ os.path.join(settings.PROJECT_DIR, "watch_tim","errors.log")
    #~ pidfile = os.path.join(settings.PROJECT_DIR, "watch_tim","pid")
    # ~ pidfile = '/var/run/watch_tim.pid' # os.path.j

    #~ preserve_loggers = (logger,dblogger.logger)
    preserve_loggers = [dblogger.logger]

    #~ def handle_daemon(self, *args, **options):
    def handle(self, *args, **options):
        main(*args, **options)
