# -*- coding: UTF-8 -*-
## Copyright 2011-2013 Luc Saffre
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
This is a real-world example of how the application developer 
can provide automatic data migrations for 
:ref:`dpy`.

This module is used because 
:mod:`lino_welfare.settings.Site` has
:attr:`migration_module <north.Site.migration_module>` 
set to ``"lino_welfare.migrate"``.

"""

import logging
logger = logging.getLogger(__name__)


import datetime
from decimal import Decimal
from django.conf import settings
from lino.core.dbutils import resolve_model
from lino.utils import mti
from lino.utils import dblogger
from lino import dd

SINCE_ALWAYS = datetime.date(1990,1,1)

def migrate_from_1_4_10(globals_dict):
    """
    - convert contacts.Partner.region from a CHAR to a FK(City)
    - add a Default accounts.Chart for debts module
    - debts.Account renamed to accounts.Account
    - debts.AccountGroup renamed to accounts.AccountGroup
    - convert Persons to Clients
    - fill pcsw.Coachings from fields coached_from, coached_until, coach1, coach2
    - fill pcsw.ClientContacts from fields health_insurance, pharmacy, job_office_contact
    - jobs.Contracts and isip.Contracts: rename `person` to `client`, 
      replace `contact` by `contact_person` and `contact_role`
    """
    
    countries_City = resolve_model("countries.City")
    debts_Account = resolve_model("accounts.Account")    
    debts_AccountGroup = resolve_model("accounts.Group")
    contacts_Partner = resolve_model("contacts.Partner")
    contacts_Company = resolve_model("contacts.Company")
    contacts_Person = resolve_model("contacts.Person")
    households_Household = resolve_model("households.Household")
    pcsw_Client = resolve_model("pcsw.Client")
    pcsw_Coaching = resolve_model("pcsw.Coaching")
    pcsw_ClientContact = resolve_model("pcsw.ClientContact")
    cal_Event = resolve_model("cal.Event")
    cal_Task = resolve_model("cal.Task")
    lino_HelpText = resolve_model("lino.HelpText")
    outbox_Attachment = resolve_model("outbox.Attachment")
    outbox_Mail = resolve_model("outbox.Mail")
    postings_Posting = resolve_model("postings.Posting")
    uploads_Upload = resolve_model("uploads.Upload")
    pcsw_CoachingType = resolve_model("pcsw.CoachingType")
    pcsw_ClientContactType = resolve_model("pcsw.ClientContactType")
    accounts_Chart = resolve_model("accounts.Chart")    
    users_User = resolve_model("users.User")    
    isip_Contract = resolve_model("isip.Contract")
    jobs_Contract = resolve_model("jobs.Contract")
    contacts_Role = resolve_model("contacts.Role")
    properties_PropType = resolve_model("properties.PropType")
    isip_ExamPolicy = resolve_model("isip.ExamPolicy")    
    
    cal = dd.resolve_app('cal')
    pcsw = dd.resolve_app('pcsw')
    postings = dd.resolve_app('postings')
    
    NOW = datetime.datetime(2012,9,6,0,0)
    
    from lino.modlib.countries.models import CityTypes
    from lino.utils.mti import create_child
    #~ from lino_welfare.modlib.pcsw import models as pcsw
    
    def find_contact(contact_id):
        try:
            return contacts_Role.objects.get(pk=contact_id)
        except contacts_Role.DoesNotExist:
            return None
    
    
    def convert_region(region):
        region = region.strip()
        if not region: return None
        try:
            return countries_City.objects.get(name=region,country__id='BE')
        except countries_City.DoesNotExist:
            o = countries_City(name=region,country__id='BE')
            o.full_clean()
            o.save()
            logger.info("Created region %s",o)
            return o
            
    def create_contacts_partner(id, country_id, city_id, name, addr1, street_prefix, street, street_no, street_box, addr2, zip_code, region, language, email, url, phone, gsm, fax, remarks):
        region = convert_region(region)
        return contacts_Partner(id=id,country_id=country_id,city_id=city_id,name=name,addr1=addr1,street_prefix=street_prefix,street=street,street_no=street_no,street_box=street_box,addr2=addr2,zip_code=zip_code,region=region,language=language,email=email,url=url,phone=phone,gsm=gsm,fax=fax,remarks=remarks,modified=NOW,created=NOW)
    globals_dict.update(create_contacts_partner=create_contacts_partner)
    
    def create_countries_city(id, name, country_id, zip_code, inscode):
        return countries_City(id=id,name=name,
            type=CityTypes.city,
            country_id=country_id,zip_code=zip_code,inscode=inscode)    
    globals_dict.update(create_countries_city=create_countries_city)
    
    def create_debts_account(id, name, seqno, group_id, type, required_for_household, required_for_person, periods, help_text, name_fr, name_en):
        if periods is not None: periods = Decimal(periods)
        return debts_Account(id=id,name=name,seqno=seqno,group_id=group_id,type=type,required_for_household=required_for_household,required_for_person=required_for_person,periods=periods,help_text=help_text,name_fr=name_fr,name_en=name_en)
    globals_dict.update(create_debts_account=create_debts_account)
    
    def create_debts_accountgroup(id, name, seqno, account_type, help_text, name_fr, name_en):
        #~ return debts_AccountGroup(id=id,chart_id=1,name=name,seqno=seqno,account_type=account_type,help_text=help_text,name_fr=name_fr,name_en=name_en)    
        return debts_AccountGroup(id=id,chart_id=1,name=name,ref=str(seqno),account_type=account_type,help_text=help_text,name_fr=name_fr,name_en=name_en)    
    globals_dict.update(create_debts_accountgroup=create_debts_accountgroup)
    
    def create_contacts_company(partner_ptr_id, prefix, vat_id, type_id, is_active, newcomer, is_deprecated, activity_id, bank_account1, bank_account2, hourly_rate):
        p = contacts_Partner.objects.get(pk=partner_ptr_id)
        p.is_obsolete=is_deprecated
        p.activity_id=activity_id
        p.bank_account1=bank_account1
        p.bank_account2=bank_account2
        p.save()
        return create_child(contacts_Partner,partner_ptr_id,contacts_Company,prefix=prefix,vat_id=vat_id,type_id=type_id,
            #~ is_active=is_active,
            #~ newcomer=newcomer,
            #~ hourly_rate=hourly_rate
            )
    globals_dict.update(create_contacts_company=create_contacts_company)
    
    def create_households_household(partner_ptr_id, is_active, newcomer, is_deprecated, activity_id, bank_account1, bank_account2, prefix, type_id):
        p = contacts_Partner.objects.get(pk=partner_ptr_id)
        p.is_obsolete=is_deprecated
        p.activity_id=activity_id
        p.bank_account1=bank_account1
        p.bank_account2=bank_account2
        p.save()
        return create_child(contacts_Partner,partner_ptr_id,households_Household,
          #~ is_active=is_active,newcomer=newcomer,
          #~ is_deprecated=is_deprecated,activity_id=activity_id,bank_account1=bank_account1,bank_account2=bank_account2,
          prefix=prefix,type_id=type_id)    
    globals_dict.update(create_households_household=create_households_household)
    
    def create_contacts_person(partner_ptr_id, birth_date, first_name, last_name, title, gender, is_active, newcomer, is_deprecated, activity_id, bank_account1, bank_account2, remarks2, gesdos_id, is_cpas, is_senior, group_id, coached_from, coached_until, coach1_id, coach2_id, birth_place, birth_country_id, civil_state, national_id, health_insurance_id, pharmacy_id, nationality_id, card_number, card_valid_from, card_valid_until, card_type, card_issuer, noble_condition, residence_type, in_belgium_since, unemployed_since, needs_residence_permit, needs_work_permit, work_permit_suspended_until, aid_type_id, income_ag, income_wg, income_kg, income_rente, income_misc, is_seeking, unavailable_until, unavailable_why, obstacles, skills, job_agents, job_office_contact_id, broker_id, faculty_id):
        p = contacts_Partner.objects.get(pk=partner_ptr_id)
        p.is_obsolete=is_deprecated
        p.activity_id=activity_id
        p.bank_account1=bank_account1
        p.bank_account2=bank_account2
        p.save()
      
        yield create_child(contacts_Partner,partner_ptr_id,contacts_Person,
            birth_date=birth_date,
            first_name=first_name,last_name=last_name,title=title,gender=gender,
            #~ is_active=is_active,newcomer=newcomer,
            #~ is_deprecated=is_deprecated,activity_id=activity_id,
            #~ bank_account1=bank_account1,bank_account2=bank_account2
            )
        #~ if national_id and national_id.strip() != '0' and not is_deprecated:
        if national_id.strip() == '0':
            national_id = ''
        remarks2 = remarks2.strip()
        if national_id or gesdos_id or remarks2 :
            #~ if is_deprecated:
                #~ national_id += ' (A)'
            if not national_id:
                national_id = str(partner_ptr_id)
            client_state = pcsw.ClientStates.coached
            if newcomer:
                client_state = pcsw.ClientStates.newcomer
            elif not is_active:
                client_state = pcsw.ClientStates.former
            elif national_id == str(partner_ptr_id):
                client_state = pcsw.ClientStates.invalid
            #~ if partner_ptr_id == 20560:
                #~ national_id += 'b'
            #~ elif partner_ptr_id == 6748:
                #~ national_id += 'a'
            #~ elif partner_ptr_id == 22050:
                #~ national_id += 'a'
            yield create_child(contacts_Person,partner_ptr_id,pcsw_Client,
                #~ birth_date=birth_date,
                #~ first_name=first_name,last_name=last_name,title=title,gender=gender,
                #~ is_active=is_active,newcomer=newcomer,is_deprecated=is_deprecated,
                #~ activity_id=activity_id,
                #~ bank_account1=bank_account1,bank_account2=bank_account2,
                remarks2=remarks2,gesdos_id=gesdos_id,is_cpas=is_cpas,
                is_senior=is_senior,group_id=group_id,
                #~ coached_from=coached_from,coached_until=coached_until,
                #~ coach1_id=coach1_id,coach2_id=coach2_id,
                birth_place=birth_place,
                birth_country_id=birth_country_id,civil_state=civil_state,
                national_id=national_id,
                client_state=client_state,
                health_insurance_id=health_insurance_id,pharmacy_id=pharmacy_id,
                nationality_id=nationality_id,card_number=card_number,card_valid_from=card_valid_from,card_valid_until=card_valid_until,card_type=card_type,card_issuer=card_issuer,noble_condition=noble_condition,residence_type=residence_type,in_belgium_since=in_belgium_since,unemployed_since=unemployed_since,needs_residence_permit=needs_residence_permit,needs_work_permit=needs_work_permit,work_permit_suspended_until=work_permit_suspended_until,aid_type_id=aid_type_id,income_ag=income_ag,income_wg=income_wg,income_kg=income_kg,income_rente=income_rente,income_misc=income_misc,is_seeking=is_seeking,unavailable_until=unavailable_until,unavailable_why=unavailable_why,obstacles=obstacles,skills=skills,job_agents=job_agents,
                job_office_contact_id=job_office_contact_id,broker_id=broker_id,faculty_id=faculty_id)
            #~ if coached_from or coached_until:
            def user2type(user_id):
                #~ pcsw_CoachingType
                if user_id in (200085,200093,200096,200099): return 2 # DSBE
                return 1 # ASD
            if coach2_id and coach2_id != coach1_id:
                kw = dict(client_id=partner_ptr_id)
                ti = user2type(coach2_id)
                if ti == 2:
                    kw.update(start_date=coached_from or SINCE_ALWAYS)
                    kw.update(end_date=coached_until)
                else:
                    kw.update(start_date=SINCE_ALWAYS)
                kw.update(
                    user_id=coach2_id,
                    type_id=ti)
                yield pcsw_Coaching(**kw)
                
            if coach1_id:
                kw = dict(client_id=partner_ptr_id)
                kw.update(start_date=coached_from or SINCE_ALWAYS)
                ti = user2type(coach1_id)
                if ti == 2:
                    kw.update(end_date=coached_until)
                    kw.update(start_date=coached_from or SINCE_ALWAYS)
                else:
                    kw.update(start_date=SINCE_ALWAYS)
                kw.update(
                    user_id=coach1_id,
                    primary=True,
                    type_id=ti)
                #~ if ti == 1:
                    #~ kw.update(start_date=coached_from or SINCE_ALWAYS,
                        #~ end_date=coached_until)
                #~ else:
                    #~ kw.update(start_date=SINCE_ALWAYS)
                yield pcsw_Coaching(**kw)
              
                #~ yield pcsw_Coaching(
                    #~ client_id=partner_ptr_id,
                    #~ start_date=coached_from,
                    #~ end_date=coached_until,
                    #~ primary=True,
                    #~ user_id=coach1_id,
                    #~ type_id=user2type(coach1_id))
            if health_insurance_id:
                yield pcsw_ClientContact(
                    client_id=partner_ptr_id,
                    #~ type=pcsw.ClientContactTypes.health_insurance,
                    type_id=1,
                    company_id=health_insurance_id)
            if pharmacy_id:
                yield pcsw_ClientContact(
                    client_id=partner_ptr_id,
                    #~ type=pcsw.ClientContactTypes.pharmacy,
                    type_id=2,
                    company_id=pharmacy_id)
            if job_office_contact_id:
                obj = pcsw_ClientContact(
                    client_id=partner_ptr_id,
                    #~ type=pcsw.ClientContactTypes.job_office,
                    type_id=3,
                    company_id=settings.SITE.site_config.job_office.id)
                obj._before_dumpy_save = add_contact_fields(obj,job_office_contact_id)
                yield obj
        else:
            #~ silently ignored if lost: 
            #~ is_cpas is_senior coach1_id coach2_id 
            #~ health_insurance_id 
            lost_fields = """
            gesdos_id 
            group_id 
            coached_from coached_until
            birth_place 
            birth_country_id civil_state
            national_id
            pharmacy_id
            nationality_id card_number card_valid_from
            card_valid_until card_type card_issuer
            noble_condition residence_type
            in_belgium_since unemployed_since
            needs_residence_permit needs_work_permit
            work_permit_suspended_until aid_type_id 
            income_ag income_wg income_kg income_rente
            income_misc is_seeking unavailable_until
            unavailable_why obstacles skills job_agents
            job_office_contact_id broker_id faculty_id
            """.split()
            lost = dict()
            for n in lost_fields:
                v = locals().get(n)
                if v:
                    lost[n] = v
            if lost:
                dblogger.warning("Lost data for Person %s without NISS: %s",
                    partner_ptr_id,lost)
                p = contacts_Person.objects.get(pk=partner_ptr_id)
                if p.remarks:
                    p.remarks += '\n'
                p.remarks += u'''Datenmigration 20121024: Person hatte weder NISS noch Gesdos-Nr und wurde deshalb kein Klient. Folgende Angaben gingen dabei verloren : ''' + repr(lost)
                p.save()
    globals_dict.update(create_contacts_person=create_contacts_person)
    
    
    
    from django.contrib.contenttypes.models import ContentType
    def new_content_type_id(m):
        if m is None: return m
        # if not fmn: return None
        # m = resolve_model(fmn)
        if m is contacts_Person:
            m = pcsw_Client
        ct = ContentType.objects.get_for_model(m)
        if ct is None: 
            raise Exception("Ignored GFK to unknown model %s" % m)
            #~ logger.warning("Ignored GFK to unknown model %s",m)
            #~ return None
        return ct.pk
    
    def create_cal_event(id, owner_type_id, owner_id, user_id, created, modified, project_id, build_time, start_date, start_time, end_date, end_time, uid, summary, description, calendar_id, access_class, sequence, auto_type, transparent, place_id, priority_id, state):
        owner_type_id = new_content_type_id(owner_type_id)
        if not state: state = cal.EventStates.new
        return cal_Event(id=id,owner_type_id=owner_type_id,owner_id=owner_id,user_id=user_id,created=created,modified=modified,project_id=project_id,build_time=build_time,start_date=start_date,start_time=start_time,end_date=end_date,end_time=end_time,uid=uid,summary=summary,description=description,calendar_id=calendar_id,access_class=access_class,sequence=sequence,auto_type=auto_type,transparent=transparent,place_id=place_id,priority_id=priority_id,state=state)    
    globals_dict.update(create_cal_event=create_cal_event)
    def create_cal_task(id, owner_type_id, owner_id, user_id, created, modified, project_id, start_date, start_time, uid, summary, description, calendar_id, access_class, sequence, auto_type, due_date, due_time, percent, state):
        owner_type_id = new_content_type_id(owner_type_id)
        if not state: state = cal.TaskStates.todo
        return cal_Task(id=id,owner_type_id=owner_type_id,owner_id=owner_id,user_id=user_id,created=created,modified=modified,project_id=project_id,start_date=start_date,start_time=start_time,uid=uid,summary=summary,description=description,calendar_id=calendar_id,access_class=access_class,sequence=sequence,auto_type=auto_type,due_date=due_date,due_time=due_time,percent=percent,state=state)        
    globals_dict.update(create_cal_task=create_cal_task)
    def create_lino_helptext(id, content_type_id, field, help_text):
        content_type_id = new_content_type_id(content_type_id)
        return lino_HelpText(id=id,content_type_id=content_type_id,field=field,help_text=help_text)        
    globals_dict.update(create_lino_helptext=create_lino_helptext)
    def create_outbox_attachment(id, owner_type_id, owner_id, mail_id):
        owner_type_id = new_content_type_id(owner_type_id)
        return outbox_Attachment(id=id,owner_type_id=owner_type_id,owner_id=owner_id,mail_id=mail_id)
    globals_dict.update(create_outbox_attachment=create_outbox_attachment)
    def create_outbox_mail(id, owner_type_id, owner_id, user_id, project_id, date, subject, body, sent):
        owner_type_id = new_content_type_id(owner_type_id)
        return outbox_Mail(id=id,owner_type_id=owner_type_id,owner_id=owner_id,user_id=user_id,project_id=project_id,date=date,subject=subject,body=body,sent=sent)        
    globals_dict.update(create_outbox_mail=create_outbox_mail)
    def create_postings_posting(id, owner_type_id, owner_id, user_id, project_id, partner_id, state, date):
        owner_type_id = new_content_type_id(owner_type_id)
        if not state:
            state = postings.PostingStates.open
        return postings_Posting(id=id,owner_type_id=owner_type_id,owner_id=owner_id,user_id=user_id,project_id=project_id,partner_id=partner_id,state=state,date=date)    
    globals_dict.update(create_postings_posting=create_postings_posting)
    def create_uploads_upload(id, owner_type_id, owner_id, user_id, created, modified, file, mimetype, type_id, valid_until, description):
        owner_type_id = new_content_type_id(owner_type_id)
        return uploads_Upload(id=id,owner_type_id=owner_type_id,owner_id=owner_id,user_id=user_id,created=created,modified=modified,file=file,mimetype=mimetype,type_id=type_id,valid_until=valid_until,description=description)    
    globals_dict.update(create_uploads_upload=create_uploads_upload)
    
    def add_contact_fields(obj,contact_id):
        def fn():
            contact = find_contact(contact_id)
            obj.contact_person=contact.person
            obj.contact_role=contact.type
        return fn
    
    def create_isip_contract(id, user_id, build_time, person_id, company_id, contact_id, language, applies_from, applies_until, date_decided, date_issued, user_asd_id, exam_policy_id, ending_id, date_ended, type_id, stages, goals, duties_asd, duties_dsbe, duties_company, duties_person):
        #~ contact = find_contact(contact_id)
        obj = isip_Contract(id=id,user_id=user_id,build_time=build_time,
          client_id=person_id,
          company_id=company_id,
          #~ contact_person=contact.person,
          #~ contact_role=contact.type,
          #~ contact_id=contact_id,
          language=language,applies_from=applies_from,applies_until=applies_until,date_decided=date_decided,date_issued=date_issued,user_asd_id=user_asd_id,exam_policy_id=exam_policy_id,ending_id=ending_id,date_ended=date_ended,type_id=type_id,stages=stages,goals=goals,duties_asd=duties_asd,duties_dsbe=duties_dsbe,duties_company=duties_company,duties_person=duties_person)    
        obj._before_dumpy_save = add_contact_fields(obj,contact_id)
        return obj
          
    globals_dict.update(create_isip_contract=create_isip_contract)
    
    def create_jobs_contract(id, user_id, build_time, person_id, company_id, contact_id, language, applies_from, applies_until, date_decided, date_issued, user_asd_id, exam_policy_id, ending_id, date_ended, type_id, job_id, duration, regime_id, schedule_id, hourly_rate, refund_rate, reference_person, responsibilities, remark):
        if hourly_rate is not None: hourly_rate = Decimal(hourly_rate)
        obj = jobs_Contract(id=id,user_id=user_id,build_time=build_time,
          client_id=person_id,
          company_id=company_id,
          language=language,applies_from=applies_from,applies_until=applies_until,date_decided=date_decided,date_issued=date_issued,user_asd_id=user_asd_id,exam_policy_id=exam_policy_id,ending_id=ending_id,date_ended=date_ended,type_id=type_id,job_id=job_id,duration=duration,regime_id=regime_id,schedule_id=schedule_id,hourly_rate=hourly_rate,refund_rate=refund_rate,reference_person=reference_person,responsibilities=responsibilities,remark=remark)
        obj._before_dumpy_save = add_contact_fields(obj,contact_id)
        return obj
    globals_dict.update(create_jobs_contract=create_jobs_contract)
    
    def create_properties_proptype(id, name, choicelist, default_value, limit_to_choices, multiple_choices, name_fr, name_en):
        if choicelist == 'HowWell':
            choicelist = 'properties.HowWell'
        elif choicelist == 'Gender':
            choicelist = 'contacts.Gender'
        return properties_PropType(id=id,name=name,choicelist=choicelist,default_value=default_value,limit_to_choices=limit_to_choices,multiple_choices=multiple_choices,name_fr=name_fr,name_en=name_en)    
    globals_dict.update(create_properties_proptype=create_properties_proptype)
    
    def create_isip_exampolicy(id, name, project_id, start_date, start_time, end_date, end_time, uid, summary, description, every, every_unit, calendar_id, name_fr, name_en):
        return isip_ExamPolicy(id=id,name=name,start_date=start_date,start_time=start_time,end_date=end_date,end_time=end_time,summary=summary,description=description,every=every,every_unit=every_unit,calendar_id=calendar_id,name_fr=name_fr,name_en=name_en)    
    globals_dict.update(create_isip_exampolicy=create_isip_exampolicy)
    
    objects = globals_dict['objects']
    def new_objects():
        yield users_User(username="watch_tim",modified=NOW,created=NOW)
        yield accounts_Chart(name="debts Default")
        yield pcsw_ClientContactType(name="Krankenkasse")
        yield pcsw_ClientContactType(name="Apotheke")
        yield pcsw_ClientContactType(name="Arbeitsvermittler")
        yield pcsw_ClientContactType(name="Gerichtsvollzieher")
        yield pcsw_CoachingType(name="ASD")
        yield pcsw_CoachingType(name="DSBE")
        yield pcsw_CoachingType(name="Schuldnerberatung")
        yield objects()
    globals_dict.update(objects=new_objects)
    
    #~ return '1.4.11'
    return '1.0'
    
def migrate_from_1_0(globals_dict):
    #~ """
    #~ Set Client.national_id to None if equal to Client.id or invalid
    #~ """
    
    #~ from lino.utils.niss import is_valid_niss
    #~ from lino.utils.mti import create_child
    
    
    #~ pcsw_Client = resolve_model("pcsw.Client")
    #~ contacts_Person = resolve_model("contacts.Person")
    
    #~ def create_pcsw_client(person_ptr_id, remarks2, gesdos_id, is_cpas, is_senior, group_id, birth_place, birth_country_id, civil_state, national_id, health_insurance_id, pharmacy_id, nationality_id, card_number, card_valid_from, card_valid_until, card_type, card_issuer, noble_condition, residence_type, in_belgium_since, unemployed_since, needs_residence_permit, needs_work_permit, work_permit_suspended_until, aid_type_id, income_ag, income_wg, income_kg, income_rente, income_misc, is_seeking, unavailable_until, unavailable_why, obstacles, skills, job_agents, job_office_contact_id, client_state, broker_id, faculty_id):
        #~ if not is_valid_niss(national_id):
            #~ if national_id != str(person_ptr_id):
                #~ logger.warning("Ignored invalid NISS %s for %d" % (national_id,person_ptr_id))
                #~ national_id = None
        #~ return create_child(contacts_Person,person_ptr_id,pcsw_Client,remarks2=remarks2,gesdos_id=gesdos_id,is_cpas=is_cpas,is_senior=is_senior,group_id=group_id,birth_place=birth_place,birth_country_id=birth_country_id,civil_state=civil_state,national_id=national_id,health_insurance_id=health_insurance_id,pharmacy_id=pharmacy_id,nationality_id=nationality_id,card_number=card_number,card_valid_from=card_valid_from,card_valid_until=card_valid_until,card_type=card_type,card_issuer=card_issuer,noble_condition=noble_condition,residence_type=residence_type,in_belgium_since=in_belgium_since,unemployed_since=unemployed_since,needs_residence_permit=needs_residence_permit,needs_work_permit=needs_work_permit,work_permit_suspended_until=work_permit_suspended_until,aid_type_id=aid_type_id,income_ag=income_ag,income_wg=income_wg,income_kg=income_kg,income_rente=income_rente,income_misc=income_misc,is_seeking=is_seeking,unavailable_until=unavailable_until,unavailable_why=unavailable_why,obstacles=obstacles,skills=skills,job_agents=job_agents,job_office_contact_id=job_office_contact_id,client_state=client_state,broker_id=broker_id,faculty_id=faculty_id)
    #~ globals_dict.update(create_pcsw_client=create_pcsw_client)
    
    return '1.0.1'
    
def migrate_from_1_0_1(globals_dict):
    """
    - New field `countries.Country.nationalities`
    """
    return '1.0.2'
    
def migrate_from_1_0_2(globals_dict):
    """
    - Removed field `countries.Country.nationalities`
    """
    
    countries_Country = resolve_model("countries.Country")
    def create_countries_country(name, isocode, short_code, iso3, name_fr, name_en, nationalities, inscode):
        return countries_Country(name=name,isocode=isocode,short_code=short_code,iso3=iso3,
            name_fr=name_fr,name_en=name_en,
            #~ nationalities=nationalities,
            inscode=inscode)
    globals_dict.update(create_countries_country=create_countries_country)
    
    return '1.0.3'

def migrate_from_1_0_3(globals_dict):
    return '1.0.4'

def migrate_from_1_0_4(globals_dict):
    properties_PropType = resolve_model("properties.PropType")
    def create_properties_proptype(id, name, choicelist, default_value, limit_to_choices, multiple_choices, name_fr, name_en):
        if choicelist == 'contacts.Gender':
            choicelist = 'lino.Genders'
        return properties_PropType(id=id,name=name,choicelist=choicelist,default_value=default_value,limit_to_choices=limit_to_choices,multiple_choices=multiple_choices,name_fr=name_fr,name_en=name_en)    
    globals_dict.update(create_properties_proptype=create_properties_proptype)
    
    def noop(*args): return None
    globals_dict.update(create_pcsw_personsearch=noop)
    globals_dict.update(create_pcsw_wantedlanguageknowledge=noop)
    globals_dict.update(create_properties_unwantedskill=noop)
    globals_dict.update(create_properties_wantedskill=noop)
    
    
    return '1.0.5'

def migrate_from_1_0_5(globals_dict):
    cal_Event = resolve_model("cal.Event")
    new_content_type_id = globals_dict.get('new_content_type_id')
    def create_cal_event(id, owner_type_id, owner_id, user_id, created, modified, project_id, build_time, start_date, start_time, end_date, end_time, summary, description, uid, calendar_id, access_class, sequence, auto_type, transparent, place_id, priority_id, state):
        owner_type_id = new_content_type_id(owner_type_id)
        #~ if state and state.value == '15':
        if state == '15':
            state = '10'
        return cal_Event(id=id,owner_type_id=owner_type_id,owner_id=owner_id,user_id=user_id,created=created,modified=modified,project_id=project_id,build_time=build_time,start_date=start_date,start_time=start_time,end_date=end_date,end_time=end_time,summary=summary,description=description,uid=uid,calendar_id=calendar_id,access_class=access_class,sequence=sequence,auto_type=auto_type,transparent=transparent,place_id=place_id,priority_id=priority_id,state=state)    
    globals_dict.update(create_cal_event=create_cal_event)
    return '1.0.6'

def migrate_from_1_0_6(globals_dict):
    return '1.0.7'

def migrate_from_1_0_7(globals_dict):
    return '1.0.8'
def migrate_from_1_0_8(globals_dict):
    return '1.0.9'
def migrate_from_1_0_9(globals_dict):
    """
    lino.Change -> changes.Change
    """
    lino_Change = resolve_model("changes.Change")
    new_content_type_id = globals_dict.get('new_content_type_id')
    def create_lino_change(id, time, type, user_id, object_type_id, object_id, master_type_id, master_id, diff):
        object_type_id = new_content_type_id(object_type_id)
        master_type_id = new_content_type_id(master_type_id)
        return lino_Change(id=id,time=time,type=type,user_id=user_id,object_type_id=object_type_id,object_id=object_id,master_type_id=master_type_id,master_id=master_id,diff=diff)    
    globals_dict.update(create_lino_change=create_lino_change)
    return '1.0.10'

def migrate_from_1_0_10(globals_dict):
    """
    - Change ClientStates.invalid to ClientStates.coached
    """
    create_child = globals_dict.get('create_child')
    contacts_Person = globals_dict.get('contacts_Person')
    pcsw_Client = globals_dict.get('pcsw_Client')
    def create_pcsw_client(person_ptr_id, remarks2, gesdos_id, is_cpas, is_senior, group_id, birth_place, birth_country_id, civil_state, national_id, health_insurance_id, pharmacy_id, nationality_id, card_number, card_valid_from, card_valid_until, card_type, card_issuer, noble_condition, residence_type, in_belgium_since, unemployed_since, needs_residence_permit, needs_work_permit, work_permit_suspended_until, aid_type_id, income_ag, income_wg, income_kg, income_rente, income_misc, is_seeking, unavailable_until, unavailable_why, obstacles, skills, job_agents, job_office_contact_id, client_state, refusal_reason, broker_id, faculty_id):
        if client_state == '60':
            client_state = '30'
        return create_child(contacts_Person,person_ptr_id,pcsw_Client,remarks2=remarks2,gesdos_id=gesdos_id,is_cpas=is_cpas,is_senior=is_senior,group_id=group_id,birth_place=birth_place,birth_country_id=birth_country_id,civil_state=civil_state,national_id=national_id,health_insurance_id=health_insurance_id,pharmacy_id=pharmacy_id,nationality_id=nationality_id,card_number=card_number,card_valid_from=card_valid_from,card_valid_until=card_valid_until,card_type=card_type,card_issuer=card_issuer,noble_condition=noble_condition,residence_type=residence_type,in_belgium_since=in_belgium_since,unemployed_since=unemployed_since,needs_residence_permit=needs_residence_permit,needs_work_permit=needs_work_permit,work_permit_suspended_until=work_permit_suspended_until,aid_type_id=aid_type_id,income_ag=income_ag,income_wg=income_wg,income_kg=income_kg,income_rente=income_rente,income_misc=income_misc,is_seeking=is_seeking,unavailable_until=unavailable_until,unavailable_why=unavailable_why,obstacles=obstacles,skills=skills,job_agents=job_agents,job_office_contact_id=job_office_contact_id,client_state=client_state,refusal_reason=refusal_reason,broker_id=broker_id,faculty_id=faculty_id)
    globals_dict.update(create_pcsw_client=create_pcsw_client)
    return '1.0.11'

def migrate_from_1_0_11(globals_dict):
    """
    - The app_label of TextFieldTemplate, SiteConfig and HelpText is no longer "lino" but "ui"
    """
    globals_dict.update(lino_TextFieldTemplate = resolve_model("ui.TextFieldTemplate"))
    globals_dict.update(lino_SiteConfig = resolve_model("ui.SiteConfig"))
    globals_dict.update(lino_HelpText = resolve_model("ui.HelpText"))
    return '1.0.12'

def migrate_from_1_0_12(globals_dict): return '1.0.13'
def migrate_from_1_0_13(globals_dict): return '1.0.14'
def migrate_from_1_0_14(globals_dict): return '1.0.15'
def migrate_from_1_0_15(globals_dict): 
    """
    New fields `secretary` and `president` in Contract. 
    """
    Person = dd.resolve_model('contacts.Person')
    #~ FUNCTION_ID_SECRETARY = 3
    #~ FUNCTION_ID_PRESIDENT = 16
    #~ oldf = globals_dict['create_lino_siteconfig']
    #~ def newf(*args):
        #~ obj = oldf(*args)
        #~ obj.secretary_function = contacts.RoleType.objects.get(pk=3)
        #~ obj.president_function = contacts.RoleType.objects.get(pk=16)
        #~ obj.secretary = S
        #~ obj.president = P
        #~ return obj
    #~ globals_dict['create_lino_siteconfig'] = newf

    #~ for fn in ('create_isip_contract','create_jobs_contract','create_lino_siteconfig'):
    #~ for fn in ('create_isip_contract','create_jobs_contract'):
        #~ oldf = globals_dict[fn]
        #~ def newf(*args):
            #~ obj = oldf(*args)
            #~ obj.signer1 = Person.objects.get(pk=84719)
            #~ obj.signer2 = Person.objects.get(pk=86814)
            #~ return obj
        #~ globals_dict[fn] = newf
    fn = 'create_isip_contract'
    oldf = globals_dict[fn]
    def newf(*args):
        obj = oldf(*args)
        obj.signer1 = Person.objects.get(pk=84719)
        obj.signer2 = Person.objects.get(pk=86814)
        return obj
    globals_dict[fn] = newf
    fn = 'create_jobs_contract'
    oldf2 = globals_dict[fn]
    def newf(*args):
        obj = oldf2(*args)
        obj.signer1 = Person.objects.get(pk=84719)
        obj.signer2 = Person.objects.get(pk=86814)
        return obj
    globals_dict[fn] = newf
    return '1.0.16'

def migrate_from_1_0_16(globals_dict): 
    return '1.0.17' # was never used in production
    
def migrate_from_1_0_17(globals_dict): 
    """
    Replaced field `active` by `state` in :ref:`welfare.jobs.Candidature`.
    """
    jobs_Candidature = resolve_model("jobs.Candidature")
    CandidatureStates = settings.SITE.modules.jobs.CandidatureStates
    def create_jobs_candidature(id, sector_id, function_id, person_id, job_id, date_submitted, remark, active):
        kw = dict()
        kw.update(id=id)
        kw.update(sector_id=sector_id)
        kw.update(function_id=function_id)
        kw.update(person_id=person_id)
        kw.update(job_id=job_id)
        kw.update(date_submitted=date_submitted)
        kw.update(remark=remark)
        if active:
            kw.update(state=CandidatureStates.active)
        else:
            kw.update(state=CandidatureStates.inactive)
        return jobs_Candidature(**kw)
    globals_dict.update(create_jobs_candidature=create_jobs_candidature)
    return '1.1.0'

def migrate_from_1_1_0(globals_dict): 
    """
    - cal.Calendar.invite_team_members : ignore this field 
      (set manually the Team where appropriate)
    - new fields Budget.print_empty_rows, and Budget.ignore_yearly_incomes
    - cal.Membership are not converted. Create team memberships manually.
    """
    cal_Calendar = resolve_model('cal.Calendar')
    bv2kw = globals_dict.get('bv2kw')
    def create_cal_calendar(id, name, build_method, template, attach_to_email, email_template, type, description, url_template, username, password, readonly, invite_team_members, start_date, color):
        kw = dict()
        kw.update(id=id)
        if name is not None: kw.update(bv2kw('name',name))
        kw.update(build_method=build_method)
        kw.update(template=template)
        kw.update(attach_to_email=attach_to_email)
        kw.update(email_template=email_template)
        kw.update(type=type)
        kw.update(description=description)
        kw.update(url_template=url_template)
        kw.update(username=username)
        kw.update(password=password)
        kw.update(readonly=readonly)
        #~ kw.update(invite_team_members=invite_team_members)
        kw.update(start_date=start_date)
        kw.update(color=color)
        return cal_Calendar(**kw)
    globals_dict.update(create_cal_calendar=create_cal_calendar)
    def noop(*args): return None
    globals_dict.update(create_cal_membership=noop)
  
   
    pcsw_CoachingType = resolve_model('pcsw.CoachingType')
    users_Team = resolve_model("users.Team")
    def after_load():
        for o in pcsw_CoachingType.objects.all():
            kw = dict()
            for n in 'id name name_fr'.split():
                kw[n] = getattr(o,n)
            users_Team(**kw).save()
    globals_dict.update(after_load=after_load)
    return '1.1.1'

def migrate_from_1_1_1(globals_dict): 
    return '1.1.2'

def migrate_from_1_1_2(globals_dict): 
    """
    - In :ref:`welfare.debts.Budget`, replaced field 
      `ignore_yearly_incomes` by `include_yearly_incomes`
      (meaning is inversed because the most frequent case is to ignore them).
    """
    debts_Budget = resolve_model('debts.Budget')
    def create_debts_budget(id, user_id, build_time, date, partner_id, print_todos, print_empty_rows, ignore_yearly_incomes, intro, conclusion, dist_amount):
        kw = dict()
        kw.update(id=id)
        kw.update(user_id=user_id)
        kw.update(build_time=build_time)
        kw.update(date=date)
        kw.update(partner_id=partner_id)
        kw.update(print_todos=print_todos)
        kw.update(print_empty_rows=print_empty_rows)
        kw.update(include_yearly_incomes=not ignore_yearly_incomes)
        kw.update(intro=intro)
        kw.update(conclusion=conclusion)
        if dist_amount is not None: dist_amount = Decimal(dist_amount)
        kw.update(dist_amount=dist_amount)
        return debts_Budget(**kw)
    globals_dict.update(create_debts_budget=create_debts_budget)
    return '1.1.3'
    
def migrate_from_1_1_3(globals_dict): 
    """
    - New field ui.SiteConfig.debts_master_budget
    """
    return '1.1.4'

def migrate_from_1_1_4(globals_dict): 
    """
    - jobs.StudyType --> isip.StudyType
    """
    
    jobs_StudyType = resolve_model('isip.StudyType')
    bv2kw = globals_dict.get('bv2kw')
    def create_jobs_studytype(id, name):
        kw = dict()
        kw.update(id=id)
        if name is not None: kw.update(bv2kw('name',name))
        return jobs_StudyType(**kw)
    globals_dict.update(create_jobs_studytype=create_jobs_studytype)

    
    return '1.1.5'

def migrate_from_1_1_5(globals_dict): 
    return '1.1.6'

def migrate_from_1_1_6(globals_dict): 
    """
    renamed cal.Place -> cal.Room
    """
    bv2kw = globals_dict['bv2kw']
    new_content_type_id = globals_dict['new_content_type_id']
    
    cal_Place = resolve_model('cal.Room')
    globals_dict.update(cal_Place=cal_Place)
    
    cal_Event = resolve_model('cal.Event')
    def create_cal_event(id, owner_type_id, owner_id, user_id, created, modified, project_id, build_time, start_date, start_time, end_date, end_time, summary, description, uid, calendar_id, access_class, sequence, auto_type, transparent, place_id, priority_id, state, assigned_to_id):
        kw = dict()
        kw.update(id=id)
        owner_type_id = new_content_type_id(owner_type_id)
        kw.update(owner_type_id=owner_type_id)
        kw.update(owner_id=owner_id)
        kw.update(user_id=user_id)
        kw.update(created=created)
        kw.update(modified=modified)
        kw.update(project_id=project_id)
        kw.update(build_time=build_time)
        kw.update(start_date=start_date)
        kw.update(start_time=start_time)
        kw.update(end_date=end_date)
        kw.update(end_time=end_time)
        kw.update(summary=summary)
        kw.update(description=description)
        kw.update(uid=uid)
        kw.update(calendar_id=calendar_id)
        kw.update(access_class=access_class)
        kw.update(sequence=sequence)
        kw.update(auto_type=auto_type)
        kw.update(transparent=transparent)
        kw.update(room_id=place_id)
        kw.update(priority_id=priority_id)
        kw.update(state=state)
        kw.update(assigned_to_id=assigned_to_id)
        return cal_Event(**kw)
    globals_dict.update(create_cal_event=create_cal_event)
    
    isip_ExamPolicy = resolve_model('isip.ExamPolicy')
    def create_isip_exampolicy(id, name, start_date, start_time, end_date, end_time, summary, description, every, every_unit, calendar_id):
        kw = dict()
        kw.update(id=id)
        if name is not None: kw.update(bv2kw('name',name))
        kw.update(start_date=start_date)
        kw.update(start_time=start_time)
        kw.update(end_date=end_date)
        kw.update(end_time=end_time)
        #~ kw.update(summary=summary)
        #~ kw.update(description=description)
        kw.update(every=every)
        kw.update(every_unit=every_unit)
        kw.update(calendar_id=calendar_id)
        return isip_ExamPolicy(**kw)
    globals_dict.update(create_isip_exampolicy=create_isip_exampolicy)

    
    return '1.1.7'
    
def migrate_from_1_1_7(globals_dict): 
    """
    - in isip.ExamPolicy, renamed field `max_occurences` to `max_events`
    - cal.EventStates : "notified" becomes "draft", "absent" becomes "cancelled"
    - renamed app "ui" to "system"
    - in `cal.Room` removed fields `company` and `company_contact`
    """
    bv2kw = globals_dict['bv2kw']
    new_content_type_id = globals_dict['new_content_type_id']
    
    isip_ExamPolicy = resolve_model('isip.ExamPolicy')
    def create_isip_exampolicy(id, name, start_date, start_time, end_date, end_time, every, every_unit, monday, tuesday, wednesday, thursday, friday, saturday, sunday, max_occurences, calendar_id):
        kw = dict()
        kw.update(id=id)
        if name is not None: kw.update(bv2kw('name',name))
        kw.update(start_date=start_date)
        kw.update(start_time=start_time)
        kw.update(end_date=end_date)
        kw.update(end_time=end_time)
        kw.update(every=every)
        kw.update(every_unit=every_unit)
        kw.update(monday=monday)
        kw.update(tuesday=tuesday)
        kw.update(wednesday=wednesday)
        kw.update(thursday=thursday)
        kw.update(friday=friday)
        kw.update(saturday=saturday)
        kw.update(sunday=sunday)
        kw.update(max_events=max_occurences)
        kw.update(calendar_id=calendar_id)
        return isip_ExamPolicy(**kw)
    globals_dict.update(create_isip_exampolicy=create_isip_exampolicy)
    
    from lino.modlib.cal.models import EventStates
    old2new = {
    '30': EventStates.draft.value,
    '80': EventStates.cancelled.value,
    }
    cal_Event = resolve_model("cal.Event")
    
    def create_cal_event(id, owner_type_id, owner_id, user_id, created, modified, project_id, build_time, start_date, start_time, end_date, end_time, summary, description, uid, calendar_id, access_class, sequence, auto_type, transparent, room_id, priority_id, state, assigned_to_id):
        
        state = old2new.get(state,state)
        
        kw = dict()
        kw.update(id=id)
        owner_type_id = new_content_type_id(owner_type_id)
        kw.update(owner_type_id=owner_type_id)
        kw.update(owner_id=owner_id)
        kw.update(user_id=user_id)
        kw.update(created=created)
        kw.update(modified=modified)
        kw.update(project_id=project_id)
        kw.update(build_time=build_time)
        kw.update(start_date=start_date)
        kw.update(start_time=start_time)
        kw.update(end_date=end_date)
        kw.update(end_time=end_time)
        kw.update(summary=summary)
        kw.update(description=description)
        kw.update(uid=uid)
        kw.update(calendar_id=calendar_id)
        kw.update(access_class=access_class)
        kw.update(sequence=sequence)
        kw.update(auto_type=auto_type)
        kw.update(transparent=transparent)
        kw.update(room_id=room_id)
        kw.update(priority_id=priority_id)
        kw.update(state=state)
        kw.update(assigned_to_id=assigned_to_id)
        return cal_Event(**kw)
    globals_dict.update(create_cal_event=create_cal_event)
    
    globals_dict.update(ui_SiteConfig=resolve_model('system.SiteConfig'))
    globals_dict.update(ui_TextFieldTemplate=resolve_model('system.TextFieldTemplate'))
    globals_dict.update(ui_HelpText=resolve_model('system.HelpText'))
    
    cal_Room = resolve_model("cal.Room")
    def create_cal_room(id, name, company_id, contact_person_id, contact_role_id):
        kw = dict()
        kw.update(id=id)
        if name is not None: kw.update(bv2kw('name',name))
        #~ kw.update(company_id=company_id)
        #~ kw.update(contact_person_id=contact_person_id)
        #~ kw.update(contact_role_id=contact_role_id)
        return cal_Room(**kw)
    globals_dict.update(create_cal_room=create_cal_room)
    
    pcsw_Coaching = resolve_model("pcsw.Coaching")
    def create_pcsw_coaching(id, user_id, client_id, start_date, end_date, type_id, primary, ending_id):
        if end_date is not None and start_date is not None:
            if end_date < start_date:
                end_date = start_date
        kw = dict()
        kw.update(id=id)
        kw.update(user_id=user_id)
        kw.update(client_id=client_id)
        kw.update(start_date=start_date)
        kw.update(end_date=end_date)
        kw.update(type_id=type_id)
        kw.update(primary=primary)
        kw.update(ending_id=ending_id)
        return pcsw_Coaching(**kw)
    globals_dict.update(create_pcsw_coaching=create_pcsw_coaching)

    
    
    
    return '1.1.8'

def migrate_from_1_1_8(globals_dict): 
    """
    - Removed `postings` app
    - countries.Language moved to languages.Language
    - Event.state 60 (rescheduled) becomes cancelled
    - Event.state 30 (visit) becomes took_place
    - In :ref:`welfare.system.SiteConfig` renamed `client_calender` to `client_calendar`
    """
    
    globals_dict.update(countries_Language=resolve_model('languages.Language'))
    
    orig_system_SiteConfig = resolve_model('system.SiteConfig')
    def system_SiteConfig(**kwargs):
        kwargs.update(client_calendar_id = kwargs.pop('client_calender_id'))
        return orig_system_SiteConfig(**kwargs)
    globals_dict.update(system_SiteConfig=system_SiteConfig)
    
    def create_postings_posting(*args):
        return None
    globals_dict.update(create_postings_posting=create_postings_posting)
    
    
    from lino.modlib.cal.models import EventStates
    old2new = {
    '60': EventStates.cancelled.value,
    '30': EventStates.took_place.value,
    }
    cal_Event = resolve_model("cal.Event")
    new_content_type_id = globals_dict.get('new_content_type_id')
    
    def create_cal_event(id, owner_type_id, owner_id, user_id, created, modified, project_id, build_time, start_date, start_time, end_date, end_time, summary, description, uid, calendar_id, access_class, sequence, auto_type, transparent, room_id, priority_id, state, assigned_to_id):
        state = old2new.get(state,state) # changed
        kw = dict()
        kw.update(id=id)
        owner_type_id = new_content_type_id(owner_type_id)
        kw.update(owner_type_id=owner_type_id)
        kw.update(owner_id=owner_id)
        kw.update(user_id=user_id)
        kw.update(created=created)
        kw.update(modified=modified)
        kw.update(project_id=project_id)
        kw.update(build_time=build_time)
        kw.update(start_date=start_date)
        kw.update(start_time=start_time)
        kw.update(end_date=end_date)
        kw.update(end_time=end_time)
        kw.update(summary=summary)
        kw.update(description=description)
        kw.update(uid=uid)
        kw.update(calendar_id=calendar_id)
        kw.update(access_class=access_class)
        kw.update(sequence=sequence)
        kw.update(auto_type=auto_type)
        kw.update(transparent=transparent)
        kw.update(room_id=room_id)
        kw.update(priority_id=priority_id)
        kw.update(state=state)
        kw.update(assigned_to_id=assigned_to_id)
        return cal_Event(**kw)
    globals_dict.update(create_cal_event=create_cal_event)
    
    #~ globals_dict.update(isip_StudyType = resolve_model("integ.StudyType"))
    
    return '1.1.9'
