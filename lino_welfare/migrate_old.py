# -*- coding: UTF-8 -*-
# Copyright 2011-2012 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

"""
The migrations in this module are no longer being used 
but archived here as historic examples.


"""

from builtins import str
import datetime
from decimal import Decimal
from django.conf import settings

from lino.utils.dpy import Migrator

from lino.core.utils import resolve_model
from lino.utils import mti
from lino.utils import dblogger
from lino_xl.lib.countries.models import PlaceTypes as CityTypes
from lino.utils.mti import create_child


def install(globals_dict):
    "Backward compat when loading dumpy fixtures created before 1.4.4"
    settings.SITE.install_migrations(globals_dict)


def migrate_from_1_1_16(globals_dict):
    NATIVES = []
    Person = resolve_model("contacts.Person")
    LanguageKnowledge = resolve_model("dsbe.LanguageKnowledge")

    def create_contacts_person(country_id, city_id, name, addr1, street_prefix, street, street_no, street_box, addr2, zip_code, region, language, email, url, phone, gsm, fax, remarks, first_name, last_name, title, id, is_active, activity_id, bank_account1, bank_account2, remarks2, gesdos_id, is_cpas, is_senior, group_id, coached_from, coached_until, coach1_id, coach2_id, sex, birth_date, birth_date_circa, birth_place, birth_country_id, civil_state, national_id, health_insurance_id, pharmacy_id, nationality_id, card_number, card_valid_from, card_valid_until, card_type, card_issuer, noble_condition, residence_type, in_belgium_since, unemployed_since, needs_residence_permit, needs_work_permit, work_permit_suspended_until, aid_type_id, income_ag, income_wg, income_kg, income_rente, income_misc, is_seeking, unavailable_until, unavailable_why, native_language_id, obstacles, skills, job_agents, job_office_contact_id):
        p = Person(
            country_id=country_id, city_id=city_id, name=name, addr1=addr1, street_prefix=street_prefix, street=street, street_no=street_no, street_box=street_box, addr2=addr2, zip_code=zip_code, region=region, language=language, email=email, url=url, phone=phone, gsm=gsm, fax=fax, remarks=remarks, first_name=first_name, last_name=last_name, title=title, id=id, is_active=is_active, activity_id=activity_id, bank_account1=bank_account1, bank_account2=bank_account2, remarks2=remarks2, gesdos_id=gesdos_id, is_cpas=is_cpas, is_senior=is_senior, group_id=group_id, coached_from=coached_from, coached_until=coached_until, coach1_id=coach1_id, coach2_id=coach2_id, sex=sex, birth_date=birth_date, birth_date_circa=birth_date_circa, birth_place=birth_place, birth_country_id=birth_country_id, civil_state=civil_state, national_id=national_id,
            health_insurance_id=health_insurance_id, pharmacy_id=pharmacy_id, nationality_id=nationality_id, card_number=card_number, card_valid_from=card_valid_from, card_valid_until=card_valid_until, card_type=card_type, card_issuer=card_issuer, noble_condition=noble_condition, residence_type=residence_type, in_belgium_since=in_belgium_since, unemployed_since=unemployed_since, needs_residence_permit=needs_residence_permit, needs_work_permit=needs_work_permit, work_permit_suspended_until=work_permit_suspended_until, aid_type_id=aid_type_id, income_ag=income_ag, income_wg=income_wg, income_kg=income_kg, income_rente=income_rente, income_misc=income_misc, is_seeking=is_seeking, unavailable_until=unavailable_until, unavailable_why=unavailable_why, obstacles=obstacles, skills=skills, job_agents=job_agents, job_office_contact_id=job_office_contact_id)
        if native_language_id:
            NATIVES.append((native_language_id, p))
        return p

    def after_load():
        for native_language_id, p in NATIVES:
            try:
                lk = p.languageknowledge_set.get(
                    language__id=native_language_id)
            except LanguageKnowledge.DoesNotExist:
                lk = p.languageknowledge_set.create(
                    language_id=native_language_id, native=True)
            else:
                lk.native = True
            lk.save()

    globals_dict.update(create_contacts_person=create_contacts_person)
    globals_dict.update(after_load=after_load)
    return '1.1.17'


def migrate_from_1_1_17(globals_dict):

    from lino_xl.lib.cal.models import migrate_reminder
    from lino.modlib.jobs.models import Job, Contract, JobProvider, \
        ContractEnding, ExamPolicy, ContractType

    Company = resolve_model("contacts.Company")
    Upload = resolve_model("uploads.Upload")
    Link = resolve_model("links.Link")
    Note = resolve_model("notes.Note")

    def get_or_create_job(provider_id, contract_type_id):
        try:
            return Job.objects.get(provider__id=provider_id, contract_type__id=contract_type_id)
        except Job.DoesNotExist:
            if provider_id is None:
                provider = None
            else:
                try:
                    provider = JobProvider.objects.get(pk=provider_id)
                except JobProvider.DoesNotExist:
                    company = Company.objects.get(pk=provider_id)
                    provider = mti.insert_child(company, JobProvider)
                    provider.save()
            if provider is None:
                name = 'Stelle%s(intern)' % contract_type_id
            else:
                name = 'Stelle%s@%s' % (contract_type_id, provider)
            job = Job(
                provider=provider,
                contract_type_id=contract_type_id,
                name=name
            )
            job.save()
            return job

    CONTRACTS = []
    REMINDERS = []
    UPLOADS = []

    def create_dsbe_contract(id, user_id, reminder_date, reminder_text,
                             delay_value, delay_type, reminder_done, must_build, person_id,
                             company_id, contact_id, language, type_id, applies_from,
                             applies_until, date_decided, date_issued, duration, regime,
                             schedule, hourly_rate, refund_rate, reference_person,
                             responsibilities, stages, goals, duties_asd, duties_dsbe,
                             duties_company, duties_person, user_asd_id, exam_policy_id,
                             ending_id, date_ended):
        job = get_or_create_job(company_id, type_id)
        obj = Contract(id=id, user_id=user_id,
                       #~ reminder_date=reminder_date,
                       #~ reminder_text=reminder_text,delay_value=delay_value,
                       #~ delay_type=delay_type,reminder_done=reminder_done,
                       must_build=must_build, person_id=person_id,
                       job=job,
                       provider_id=company_id,
                       contact_id=contact_id, language=language, type_id=type_id,
                       applies_from=applies_from, applies_until=applies_until, date_decided=date_decided, date_issued=date_issued, duration=duration, regime=regime, schedule=schedule, hourly_rate=hourly_rate, refund_rate=refund_rate, reference_person=reference_person, responsibilities=responsibilities, stages=stages, goals=goals, duties_asd=duties_asd, duties_dsbe=duties_dsbe, duties_company=duties_company, duties_person=duties_person, user_asd_id=user_asd_id, exam_policy_id=exam_policy_id, ending_id=ending_id, date_ended=date_ended)
        REMINDERS.append(
            (obj, (reminder_date, reminder_text, delay_value, delay_type, reminder_done)))
        return obj

    def delayed_create_dsbe_contract(*args):
        CONTRACTS.append(args)

    def create_links_link(id, user_id, reminder_date, reminder_text, delay_value, delay_type, reminder_done, person_id, company_id, type_id, date, url, name):
        obj = Link(id=id, user_id=user_id,
                   #~ reminder_date=reminder_date,reminder_text=reminder_text,
                   #~ delay_value=delay_value,delay_type=delay_type,
                   #~ reminder_done=reminder_done,
                   person_id=person_id, company_id=company_id, type_id=type_id, date=date, url=url, name=name)
        REMINDERS.append(
            (obj, (reminder_date, reminder_text, delay_value, delay_type, reminder_done)))
        return obj

    def create_notes_note(id, user_id, reminder_date, reminder_text, delay_value, delay_type, reminder_done, must_build, person_id, company_id, date, type_id, event_type_id, subject, body, language):
        obj = Note(id=id, user_id=user_id,
                   #~ reminder_date=reminder_date,reminder_text=reminder_text,
                   #~ delay_value=delay_value,delay_type=delay_type,
                   #~ reminder_done=reminder_done,
                   must_build=must_build, person_id=person_id, company_id=company_id, date=date, type_id=type_id, event_type_id=event_type_id, subject=subject, body=body, language=language)
        REMINDERS.append(
            (obj, (reminder_date, reminder_text, delay_value, delay_type, reminder_done)))
        return obj

    def create_uploads_upload(id, user_id, owner_type_id, owner_id, reminder_date, reminder_text, delay_value, delay_type, reminder_done, file, mimetype, created, modified, description, type_id):
        obj = Upload(id=id, user_id=user_id,
                     owner_type_id=owner_type_id, owner_id=owner_id,
                     valid_until=reminder_date,
                     #~ reminder_date=reminder_date,reminder_text=reminder_text,
                     #~ delay_value=delay_value,delay_type=delay_type,
                     #~ reminder_done=reminder_done,
                     file=file, mimetype=mimetype,
                     created=created, modified=modified, description=description, type_id=type_id)
        #~ REMINDERS.append((obj,(reminder_date,reminder_text,delay_value,delay_type,reminder_done)))
        # must relay the saving of uploads because owner is a generic foreign key
        # which doesn't fail to save the instance but returns None for the owner if it doesn't yet
        # exist.
        UPLOADS.append(obj)
        #~ return obj

    def after_load():
        for args in CONTRACTS:
            obj = create_dsbe_contract(*args)
            obj.full_clean()
            obj.save()
        for obj, args in REMINDERS:
            migrate_reminder(obj, *args)
        for obj in UPLOADS:
            obj.save()

    globals_dict.update(create_dsbe_contract=delayed_create_dsbe_contract)
    globals_dict.update(Contract=Contract)
    globals_dict.update(ContractEnding=ContractEnding)
    globals_dict.update(ContractType=ContractType)
    globals_dict.update(ExamPolicy=ExamPolicy)
    globals_dict.update(create_uploads_upload=create_uploads_upload)
    globals_dict.update(create_notes_note=create_notes_note)
    globals_dict.update(create_links_link=create_links_link)
    globals_dict.update(after_load=after_load)
    #~ globals_dict.update(create_jobs_contracttype=globals_dict['create_dsbe_contracttype'])
    #~ globals_dict.update(create_jobs_exampolicy=globals_dict['create_dsbe_exampolicy'])
    return '1.2.0'


def migrate_from_1_2_0(globals_dict):
    return '1.2.1'


def migrate_from_1_2_1(globals_dict):
    """
    - rename model contacts.ContactType to contacts.RoleType
    - rename model contacts.Contact to contacts.Role 
      (and field company to parent, person to child)
    - change the id of existing users because User is now subclass of Contact
      and modify SiteConfig.next_partner_id
    - part of module jobs has been split to isip
    """

    old_contenttypes = """\
    39;activity;dsbe;activity
    43;aid type;dsbe;aidtype
    31;Attendance;cal;attendance
    67;Attendee;cal;attendee
    68;Attendee Role;cal;attendeerole
    65;calendar;cal;calendar
    8;city;countries;city
    20;Company;contacts;company
    16;company type;contacts;companytype
    18;contact;contacts;contact
    59;Contact Person;contacts;role
    17;contact type;contacts;contacttype
    2;content type;contenttypes;contenttype
    54;Contract;jobs;contract
    53;Contract Ending;jobs;contractending
    51;Contract Type;jobs;contracttype
    58;Contracts Situation;jobs;contractssituation
    7;country;countries;country
    46;Course;dsbe;course
    45;Course Content;dsbe;coursecontent
    42;Course Ending;dsbe;courseending
    44;course provider;dsbe;courseprovider
    47;Course Requests;dsbe;courserequest
    4;Data Control Listing;lino;datacontrollisting
    32;Event;cal;event
    22;Event Type;notes;eventtype
    30;Event Type;cal;eventtype
    23;Event/Note;notes;note
    52;examination policy;jobs;exampolicy
    41;exclusion;dsbe;exclusion
    40;exclusion type;dsbe;exclusiontype
    60;Incoming Mail;mails;inmail
    34;Integration Phase;dsbe;persongroup
    56;Job;jobs;job
    38;job experience;dsbe;jobexperience
    50;Job Provider;jobs;jobprovider
    57;Job Requests;jobs;jobrequest
    55;Job Type;jobs;jobtype
    6;Language;countries;language
    37;language knowledge;dsbe;languageknowledge
    25;link;links;link
    24;link type;links;linktype
    61;mail;mails;mail
    21;Note Type;notes;notetype
    63;Outgoing Mail;mails;outmail
    19;Person;contacts;person
    48;Person Search;dsbe;personsearch
    29;place;cal;place
    12;Property;properties;property
    13;Property;properties;personproperty
    10;Property Choice;properties;propchoice
    11;Property Group;properties;propgroup
    9;Property Type;properties;proptype
    62;Recipient;mails;recipient
    66;recurrence set;cal;recurrenceset
    64;Role Type;contacts;roletype
    3;site config;lino;siteconfig
    36;study or education;dsbe;study
    35;study type;dsbe;studytype
    33;Task;cal;task
    5;Text Field Template;lino;textfieldtemplate
    28;Third Party;thirds;third
    15;Unwanted property;properties;unwantedskill
    27;Upload;uploads;upload
    26;upload type;uploads;uploadtype
    1;User;users;user
    49;wanted language knowledge;dsbe;wantedlanguageknowledge
    14;Wanted property;properties;wantedskill"""
    contenttypes_dict = {}
    for ln in old_contenttypes.splitlines():
        ln = ln.strip()
        if ln:
            a = ln.split(';')
            if len(a) != 4:
                raise Exception("%r : invalid format!" % ln)
            tst = a[2] + '.' + a[3]
            if tst == 'contacts.contacttype':
                a[3] = 'roletype'
            elif tst == 'jobs.exampolicy':
                a[2] = 'isip'
                a[3] = 'contract'
                """existing data was affected  by the "dpy & contenttypes" bug:
                (Tasks 487,488, 489, 490, 491, 492, 493, 494) had wrongly owner_type 
                exampolicy 
                """
            elif tst == 'jobs.contractending':
                a[2] = 'isip'
            contenttypes_dict[int(a[0])] = (a[2], a[3])

    from lino.modlib.isip import models as isip
    from lino.modlib.jobs import models as jobs

    Role = resolve_model("contacts.Role")
    RoleType = resolve_model("contacts.RoleType")
    from django.contrib.contenttypes.models import ContentType
    #~ ContentType = resolve_model("contenttypes.ContentType")

    def new_contenttype(old_id):
        label, name = contenttypes_dict.get(old_id)
        try:
            return ContentType.objects.get(app_label=label, model=name).pk
        except ContentType.DoesNotExist:
            raise Exception("No ContentType %s.%s" % (label, name))

    Event = resolve_model("cal.Event")
    Task = resolve_model("cal.Task")
    Person = resolve_model("contacts.Person")
    Company = resolve_model("contacts.Company")
    #~ Contract = resolve_model("jobs.Contract")
    Job = resolve_model("jobs.Job")
    Link = resolve_model("links.Link")
    SiteConfig = resolve_model("lino.SiteConfig")
    TextFieldTemplate = resolve_model("lino.TextFieldTemplate")
    Note = resolve_model("notes.Note")
    Upload = resolve_model("uploads.Upload")
    User = resolve_model("users.User")
    PersonSearch = resolve_model("dsbe.PersonSearch")
    WantedLanguageKnowledge = resolve_model("dsbe.WantedLanguageKnowledge")
    LanguageKnowledge = resolve_model("dsbe.LanguageKnowledge")
    Study = resolve_model("dsbe.Study")
    PersonProperty = resolve_model("properties.PersonProperty")

    globals_dict.update(ExamPolicy=resolve_model("isip.ExamPolicy"))
    globals_dict.update(ContractEnding=resolve_model("isip.ContractEnding"))

    #~ ISIP_CTYPES = {}
    #~ JOBS_CTYPES = {}
    CONTRACT_TYPES = {}

    scl = list(globals_dict.get('lino_siteconfig_objects')())
    assert len(scl) == 1
    global new_next_partner_id
    new_next_partner_id = user_id_offset = scl[0].next_partner_id

    def new_user_id(old_id):
        if old_id is None:
            return None
        global new_next_partner_id
        i = old_id + user_id_offset
        new_next_partner_id = max(new_next_partner_id, i + 1)
        return i

    def create_lino_siteconfig(id, default_build_method, site_company_id, job_office_id, propgroup_skills_id, propgroup_softskills_id, propgroup_obstacles_id, residence_permit_upload_type_id, work_permit_upload_type_id, driving_licence_upload_type_id, next_partner_id):
        next_partner_id = new_next_partner_id
        return SiteConfig(id=id, default_build_method=default_build_method, site_company_id=site_company_id, job_office_id=job_office_id, propgroup_skills_id=propgroup_skills_id, propgroup_softskills_id=propgroup_softskills_id, propgroup_obstacles_id=propgroup_obstacles_id, residence_permit_upload_type_id=residence_permit_upload_type_id, work_permit_upload_type_id=work_permit_upload_type_id, driving_licence_upload_type_id=driving_licence_upload_type_id, next_partner_id=next_partner_id)
    globals_dict.update(create_lino_siteconfig=create_lino_siteconfig)

    def create_dsbe_study(id, country_id, city_id, person_id, type_id, content, started, stopped, success, language_id, school, remarks):
        if school is None:
            school = ''
        if remarks is None:
            remarks = ''
        if content is None:
            content = ''
        return Study(id=id, country_id=country_id, city_id=city_id, person_id=person_id, type_id=type_id, content=content, started=started, stopped=stopped, success=success, language_id=language_id, school=school, remarks=remarks)
    globals_dict.update(create_dsbe_study=create_dsbe_study)

    def create_properties_personproperty(id, group_id, property_id, value, person_id, remark):
        if remark is None:
            remark = ''
        return PersonProperty(id=id, group_id=group_id, property_id=property_id, value=value, person_id=person_id, remark=remark)
    globals_dict.update(
        create_properties_personproperty=create_properties_personproperty)

    def create_users_user(id, username, first_name, last_name, email, is_staff, is_expert, is_active, is_superuser, last_login, date_joined):
        if email is None:
            email = ''
        return User(id=new_user_id(id), username=username, first_name=first_name, last_name=last_name, email=email, is_staff=is_staff, is_expert=is_expert, is_active=is_active, is_superuser=is_superuser, last_login=last_login, date_joined=date_joined)
    globals_dict.update(create_users_user=create_users_user)

    def create_uploads_upload(id, user_id, owner_type_id, owner_id, file, mimetype, created, modified, description, type_id, valid_until):
        if description is None:
            description = ''
        owner_type_id = new_contenttype(owner_type_id)
        return Upload(id=id, user_id=new_user_id(user_id), owner_type_id=owner_type_id, owner_id=owner_id, file=file, mimetype=mimetype, created=created, modified=modified, description=description, type_id=type_id, valid_until=valid_until)
    globals_dict.update(create_uploads_upload=create_uploads_upload)

    def create_notes_note(id, user_id, must_build, person_id, company_id, date, type_id, event_type_id, subject, body, language):
        if subject is None:
            subject = ''
        return Note(id=id, user_id=new_user_id(user_id), must_build=must_build, person_id=person_id, company_id=company_id, date=date, type_id=type_id, event_type_id=event_type_id, subject=subject, body=body, language=language)
    globals_dict.update(create_notes_note=create_notes_note)

    def create_contacts_contacttype(id, name, name_fr, name_en):
        #~ return ContactType(id=id,name=name,name_fr=name_fr,name_en=name_en)
        return RoleType(id=id, name=name, name_fr=name_fr, name_en=name_en)
    globals_dict.update(
        create_contacts_contacttype=create_contacts_contacttype)

    def create_lino_textfieldtemplate(id, user_id, name, description, text):
        return TextFieldTemplate(id=id, user_id=new_user_id(user_id), name=name, description=description, text=text)
    globals_dict.update(
        create_lino_textfieldtemplate=create_lino_textfieldtemplate)

    def create_links_link(id, user_id, person_id, company_id, type_id, date, url, name):
        return Link(id=id, user_id=new_user_id(user_id), person_id=person_id, company_id=company_id, type_id=type_id, date=date, url=url, name=name)
    globals_dict.update(create_links_link=create_links_link)

    def create_jobs_contract(id, user_id, must_build, person_id, provider_id, contact_id, language, job_id, type_id, applies_from, applies_until, date_decided, date_issued, duration, regime, schedule, hourly_rate, refund_rate, reference_person, responsibilities, stages, goals, duties_asd, duties_dsbe, duties_company, duties_person, user_asd_id, exam_policy_id, ending_id, date_ended):
        if regime is None:
            regime = ''
        if schedule is None:
            schedule = ''
        if refund_rate is None:
            refund_rate = ''
        if reference_person is None:
            reference_person = ''
        user_asd_id = new_user_id(user_asd_id)
        ctype = CONTRACT_TYPES.get(type_id)
        if ctype.name.startswith('VSE'):
            #~ type_id = ISIP_CTYPES.get(type_id).pk
            return isip.Contract(id=id, user_id=new_user_id(user_id),
                                 must_build=must_build, person_id=person_id,
                                 company_id=provider_id, contact_id=contact_id,
                                 language=language,
                                 type_id=type_id, applies_from=applies_from, applies_until=applies_until,
                                 date_decided=date_decided, date_issued=date_issued,
                                 stages=stages, goals=goals, duties_asd=duties_asd,
                                 duties_dsbe=duties_dsbe, duties_company=duties_company,
                                 duties_person=duties_person, user_asd_id=user_asd_id,
                                 exam_policy_id=exam_policy_id,
                                 ending_id=ending_id, date_ended=date_ended)
        else:
            #~ type_id = JOBS_CTYPES.get(type_id).pk
            return jobs.Contract(
                id=id, user_id=new_user_id(user_id), must_build=must_build,
                person_id=person_id, provider_id=provider_id,
                contact_id=contact_id, language=language, job_id=job_id,
                type_id=type_id, applies_from=applies_from, applies_until=applies_until,
                date_decided=date_decided, date_issued=date_issued,
                duration=duration, regime=regime, schedule=schedule, hourly_rate=hourly_rate,
                refund_rate=refund_rate, reference_person=reference_person,
                responsibilities=responsibilities,
                #~ stages=stages,goals=goals,duties_asd=duties_asd,duties_dsbe=duties_dsbe,
                #~ duties_company=duties_company,duties_person=duties_person,
                user_asd_id=user_asd_id, exam_policy_id=exam_policy_id,
                ending_id=ending_id, date_ended=date_ended)
    globals_dict.update(create_jobs_contract=create_jobs_contract)

    def create_dsbe_personsearch(id, user_id, title, aged_from, aged_to, sex, only_my_persons, coached_by_id, period_from, period_until):
        user_id = new_user_id(user_id)
        if sex is None:
            sex = ''
        coached_by_id = new_user_id(coached_by_id)
        return PersonSearch(id=id, user_id=user_id, title=title, aged_from=aged_from, aged_to=aged_to, sex=sex, only_my_persons=only_my_persons, coached_by_id=coached_by_id, period_from=period_from, period_until=period_until)
    globals_dict.update(create_dsbe_personsearch=create_dsbe_personsearch)

    def create_contacts_company(country_id, city_id, name, addr1, street_prefix, street, street_no, street_box, addr2, zip_code, region, language, email, url, phone, gsm, fax, remarks, vat_id, type_id, id, is_active, activity_id, bank_account1, bank_account2, prefix, hourly_rate):
        if email is None:
            email = ''
        if remarks is None:
            remarks = ''
        if bank_account1 is None:
            bank_account1 = ''
        if bank_account2 is None:
            bank_account2 = ''
        return Company(country_id=country_id, city_id=city_id, name=name, addr1=addr1, street_prefix=street_prefix, street=street, street_no=street_no, street_box=street_box, addr2=addr2, zip_code=zip_code, region=region, language=language, email=email, url=url, phone=phone, gsm=gsm, fax=fax, remarks=remarks, vat_id=vat_id, type_id=type_id, id=id, is_active=is_active, activity_id=activity_id, bank_account1=bank_account1, bank_account2=bank_account2, prefix=prefix, hourly_rate=hourly_rate)
    globals_dict.update(create_contacts_company=create_contacts_company)

    def create_contacts_person(country_id, city_id, name, addr1, street_prefix, street, street_no, street_box, addr2, zip_code, region, language, email, url, phone, gsm, fax, remarks, first_name, last_name, title, sex, id, is_active, activity_id, bank_account1, bank_account2, remarks2, gesdos_id, is_cpas, is_senior, group_id, coached_from, coached_until, coach1_id, coach2_id, birth_date, birth_date_circa, birth_place, birth_country_id, civil_state, national_id, health_insurance_id, pharmacy_id, nationality_id, card_number, card_valid_from, card_valid_until, card_type, card_issuer, noble_condition, residence_type, in_belgium_since, unemployed_since, needs_residence_permit, needs_work_permit, work_permit_suspended_until, aid_type_id, income_ag, income_wg, income_kg, income_rente, income_misc, is_seeking, unavailable_until, unavailable_why, obstacles, skills, job_agents, job_office_contact_id):
        if email is None:
            email = ''
        if remarks is None:
            remarks = ''
        if remarks2 is None:
            remarks2 = ''
        if bank_account1 is None:
            bank_account1 = ''
        if bank_account2 is None:
            bank_account2 = ''
        if birth_place is None:
            birth_place = ''
        if civil_state is None:
            civil_state = ''
        if sex is None:
            sex = ''
        if gesdos_id is None:
            gesdos_id = ''
        if card_number is None:
            card_number = ''
        if card_type is None:
            card_type = ''
        if card_issuer is None:
            card_issuer = ''
        if noble_condition is None:
            noble_condition = ''
        if unavailable_why is None:
            unavailable_why = ''
        if job_agents is None:
            job_agents = ''
        coach1_id = new_user_id(coach1_id)
        coach2_id = new_user_id(coach2_id)
        return Person(
            country_id=country_id, city_id=city_id, name=name, addr1=addr1, street_prefix=street_prefix, street=street, street_no=street_no, street_box=street_box, addr2=addr2, zip_code=zip_code, region=region, language=language, email=email, url=url, phone=phone, gsm=gsm, fax=fax, remarks=remarks, first_name=first_name, last_name=last_name, title=title, sex=sex,
            # Person pk is now contact_ptr_id, and FakeDeserializedObject.try_save tests this to decided whether
            # it can defer the save
            id=id,
            contact_ptr_id=id,
            is_active=is_active, activity_id=activity_id, bank_account1=bank_account1, bank_account2=bank_account2, remarks2=remarks2, gesdos_id=gesdos_id, is_cpas=is_cpas, is_senior=is_senior, group_id=group_id, coached_from=coached_from, coached_until=coached_until, coach1_id=coach1_id, coach2_id=coach2_id, birth_date=birth_date, birth_date_circa=birth_date_circa, birth_place=birth_place, birth_country_id=birth_country_id, civil_state=civil_state, national_id=national_id, health_insurance_id=health_insurance_id, pharmacy_id=pharmacy_id, nationality_id=nationality_id, card_number=card_number, card_valid_from=card_valid_from, card_valid_until=card_valid_until, card_type=card_type, card_issuer=card_issuer, noble_condition=noble_condition, residence_type=residence_type, in_belgium_since=in_belgium_since, unemployed_since=unemployed_since, needs_residence_permit=needs_residence_permit, needs_work_permit=needs_work_permit, work_permit_suspended_until=work_permit_suspended_until, aid_type_id=aid_type_id, income_ag=income_ag, income_wg=income_wg, income_kg=income_kg, income_rente=income_rente, income_misc=income_misc, is_seeking=is_seeking, unavailable_until=unavailable_until, unavailable_why=unavailable_why, obstacles=obstacles, skills=skills, job_agents=job_agents, job_office_contact_id=job_office_contact_id)
    globals_dict.update(create_contacts_person=create_contacts_person)

    def create_contacts_contact(id, person_id, company_id, type_id):
        #~ return Contact(id=id,person_id=person_id,company_id=company_id,type_id=type_id)
        if not company_id:
            return None  # field was nullable
        return Role(id=id, child_id=person_id, parent_id=company_id, type_id=type_id)
    globals_dict.update(create_contacts_contact=create_contacts_contact)

    def create_dsbe_wantedlanguageknowledge(id, search_id, language_id, spoken, written):
        if spoken is None:
            spoken = ''
        if written is None:
            written = ''
        return WantedLanguageKnowledge(id=id, search_id=search_id, language_id=language_id, spoken=spoken, written=written)
    globals_dict.update(
        create_dsbe_wantedlanguageknowledge=create_dsbe_wantedlanguageknowledge)

    def create_dsbe_languageknowledge(id, person_id, language_id, spoken, written, native, cef_level):
        if spoken is None:
            spoken = ''
        if written is None:
            written = ''
        if cef_level is None:
            cef_level = ''
        return LanguageKnowledge(id=id, person_id=person_id, language_id=language_id, spoken=spoken, written=written, native=native, cef_level=cef_level)
    globals_dict.update(
        create_dsbe_languageknowledge=create_dsbe_languageknowledge)

    def create_cal_task(id, user_id, created, modified, owner_type_id, owner_id, person_id, company_id, start_date, start_time, summary, description, access_class, sequence, alarm_value, alarm_unit, dt_alarm, due_date, due_time, done, percent, status, auto_type):
        owner_type_id = new_contenttype(owner_type_id)
        user_id = new_user_id(user_id)
        if access_class is None:
            access_class = ''
        if alarm_unit is None:
            alarm_unit = ''
        if summary is None:
            summary = ''
        if status is None:
            status = ''
        if person_id:
            project_id = person_id
            if company_id:
                dblogger.warning(
                    "create_cal_task looses company_id %s for task #%", company_id, id)
        else:
            project_id = company_id
        return Task(id=id, user_id=user_id, created=created, modified=modified, owner_type_id=owner_type_id, owner_id=owner_id, project_id=project_id, start_date=start_date, start_time=start_time, summary=summary, description=description, access_class=access_class, sequence=sequence, alarm_value=alarm_value, alarm_unit=alarm_unit, dt_alarm=dt_alarm, due_date=due_date, due_time=due_time, done=done, percent=percent, status=status, auto_type=auto_type)
    globals_dict.update(create_cal_task=create_cal_task)

    def create_jobs_contracttype(id, build_method, template, ref, name, name_fr, name_en):
        if name.startswith('VSE'):
            obj = isip.ContractType(
                id=id, build_method=build_method, template=template,
                ref=ref, name=name, name_fr=name_fr, name_en=name_en)
        else:
            obj = jobs.ContractType(
                id=id, build_method=build_method, template=template,
                ref=ref, name=name, name_fr=name_fr, name_en=name_en)
        CONTRACT_TYPES[id] = obj
        return obj
    globals_dict.update(create_jobs_contracttype=create_jobs_contracttype)

    def create_jobs_job(id, name, type_id, provider_id, contract_type_id, hourly_rate, capacity, remark):
        ctype = CONTRACT_TYPES.get(contract_type_id)
        if ctype.__class__ != jobs.ContractType:
            dblogger.warning("Dropping VSE Job %s" %
                             list((id, name, type_id, provider_id, contract_type_id, hourly_rate, capacity, remark)))
            return None
        if remark is None:
            remark = ''
        return Job(id=id, name=name, type_id=type_id, provider_id=provider_id, contract_type_id=contract_type_id, hourly_rate=hourly_rate, capacity=capacity, remark=remark)
    globals_dict.update(create_jobs_job=create_jobs_job)

    def create_cal_event(id, user_id, created, modified, must_build, person_id, company_id, start_date, start_time, summary, description, access_class, sequence, alarm_value, alarm_unit, dt_alarm, end_date, end_time, transparent, type_id, place_id, priority, status, duration_value, duration_unit, repeat_value, repeat_unit):
        user_id = new_user_id(user_id)
        return Event(id=id, user_id=user_id, created=created, modified=modified, must_build=must_build, person_id=person_id, company_id=company_id, start_date=start_date, start_time=start_time, summary=summary, description=description, access_class=access_class, sequence=sequence, alarm_value=alarm_value, alarm_unit=alarm_unit, dt_alarm=dt_alarm, end_date=end_date, end_time=end_time, transparent=transparent, type_id=type_id, place_id=place_id, priority=priority, status=status, duration_value=duration_value, duration_unit=duration_unit, repeat_value=repeat_value, repeat_unit=repeat_unit)
    globals_dict.update(create_cal_event=create_cal_event)

    return '1.2.2'


def migrate_from_1_2_2(globals_dict):
    """
    - Moved Study, StudyType and JobExperience from `dsbe` to `jobs`
      (see :blogref:`20110915`).
    - Swap content of notes_NoteType and note.EventType
      (see :blogref:`20110928`).
    """

    globals_dict.update(dsbe_Study=resolve_model("jobs.Study"))
    globals_dict.update(dsbe_StudyType=resolve_model("jobs.StudyType"))
    globals_dict.update(dsbe_JobExperience=resolve_model("jobs.Experience"))

    notes_EventType = resolve_model("notes.EventType")
    notes_Note = resolve_model("notes.Note")
    notes_NoteType = resolve_model("notes.NoteType")

    def create_notes_eventtype(id, name, remark, name_fr, name_en):
        return notes_NoteType(id=id, name=name, remark=remark, name_fr=name_fr, name_en=name_en)
        #~ return notes_EventType(id=id,name=name,remark=remark,name_fr=name_fr,name_en=name_en)
    globals_dict.update(create_notes_eventtype=create_notes_eventtype)

    def create_notes_notetype(id, build_method, template, name, important, remark):
        return notes_EventType(id=id, name=name, remark=remark)
        #~ return notes_NoteType(id=id,build_method=build_method,template=template,name=name,important=important,remark=remark)
    globals_dict.update(create_notes_notetype=create_notes_notetype)

    def create_notes_note(id, user_id, must_build, person_id, company_id, date, type_id, event_type_id, subject, body, language):
        type_id, event_type_id = event_type_id, type_id
        return notes_Note(id=id, user_id=user_id, must_build=must_build, person_id=person_id, company_id=company_id, date=date, type_id=type_id, event_type_id=event_type_id, subject=subject, body=body, language=language)
    globals_dict.update(create_notes_note=create_notes_note)

    jobs_JobRequest = resolve_model("jobs.Candidature")

    def create_jobs_jobrequest(id, person_id, job_id, date_submitted, contract_id, remark):
        return jobs_JobRequest(id=id, person_id=person_id, job_id=job_id, date_submitted=date_submitted, contract_id=contract_id, remark=remark)
    globals_dict.update(create_jobs_jobrequest=create_jobs_jobrequest)

    return '1.2.3'


def migrate_from_1_2_3(globals_dict):
    """
    - removed jobs.Wish
    """
    jobs_Candidature = resolve_model("jobs.Candidature")

    def create_jobs_candidature(id, person_id, job_id, date_submitted, contract_id, remark):
        return jobs_Candidature(id=id, person_id=person_id, job_id=job_id, date_submitted=date_submitted, remark=remark)
    globals_dict.update(create_jobs_candidature=create_jobs_candidature)

    return '1.2.4'


def migrate_from_1_2_4(globals_dict):
    """
    - removed alarm fields from cal.Event and cal.Task
    - new model CourseOffer. 
      For each Course instance, create a corresponding CourseOffer instance.
    """
    cal_Event = resolve_model("cal.Event")

    def create_cal_event(id, user_id, created, modified, project_id, must_build, calendar_id, uid, start_date, start_time, summary, description, access_class, sequence, alarm_value, alarm_unit, dt_alarm, user_modified, rset_id, end_date, end_time, transparent, type_id, place_id, priority, status, duration_value, duration_unit):
        return cal_Event(id=id, user_id=user_id, created=created, modified=modified, project_id=project_id, must_build=must_build, calendar_id=calendar_id, uid=uid, start_date=start_date, start_time=start_time, summary=summary, description=description, access_class=access_class, sequence=sequence, user_modified=user_modified, rset_id=rset_id, end_date=end_date, end_time=end_time, transparent=transparent, type_id=type_id, place_id=place_id, priority=priority, status=status, duration_value=duration_value, duration_unit=duration_unit)
    globals_dict.update(create_cal_event=create_cal_event)

    cal_Task = resolve_model("cal.Task")
    new_content_type_id = globals_dict['new_content_type_id']

    def create_cal_task(id, user_id, created, modified, owner_type_id, owner_id, project_id, calendar_id, uid, start_date, start_time, summary, description, access_class, sequence, alarm_value, alarm_unit, dt_alarm, user_modified, rset_id, due_date, due_time, done, percent, status, auto_type):
        owner_type_id = new_content_type_id(owner_type_id)
        return cal_Task(id=id, user_id=user_id, created=created, modified=modified, owner_type_id=owner_type_id, owner_id=owner_id, project_id=project_id, calendar_id=calendar_id, uid=uid, start_date=start_date, start_time=start_time, summary=summary, description=description, access_class=access_class, sequence=sequence, user_modified=user_modified, rset_id=rset_id, due_date=due_date, due_time=due_time, done=done, percent=percent, status=status, auto_type=auto_type)
    globals_dict.update(create_cal_task=create_cal_task)

    from lino.utils.instantiator import i2d
    dsbe_CourseOffer = resolve_model("dsbe.CourseOffer")
    dsbe_Course = resolve_model("dsbe.Course")

    def create_dsbe_course(id, title, content_id, provider_id, start_date, remark):
        o = dsbe_CourseOffer(id=id, title=title, content_id=content_id,
                             provider_id=provider_id, description=remark)
        o.full_clean()
        o.save()
        if start_date is None:
            start_date = i2d(20110901)
        return dsbe_Course(id=id, offer=o, start_date=start_date)
        #~ return dsbe_Course(id=id,title=title,content_id=content_id,provider_id=provider_id,start_date=start_date,remark=remark)
    globals_dict.update(create_dsbe_course=create_dsbe_course)

    dsbe_CourseRequest = resolve_model("dsbe.CourseRequest")

    def create_dsbe_courserequest(id, person_id, content_id, date_submitted, course_id, remark, date_ended, ending_id):
        return dsbe_CourseRequest(
            id=id, person_id=person_id, content_id=content_id, date_submitted=date_submitted, course_id=course_id,
            offer_id=course_id,
            remark=remark, date_ended=date_ended, ending_id=ending_id)
    globals_dict.update(create_dsbe_courserequest=create_dsbe_courserequest)

    return '1.2.5'


def migrate_from_1_2_5(globals_dict):
    return '1.2.6'


def migrate_from_1_2_6(globals_dict):
    """
    - Rename fields `sex` to `gender` 
      in `contacts.Person`, `users.User`, `dsbe.PersonSearch`.
    - add previously hard-coded objects from 
      :mod:`lino_xl.lib.cal.fixtures.std`
    """
    from lino.utils.mti import insert_child
    contacts_Contact = resolve_model("contacts.Contact")
    contacts_Person = resolve_model("contacts.Person")
    users.User = resolve_model("users.User")
    dsbe_PersonSearch = resolve_model("dsbe.PersonSearch")
    cal_Event = resolve_model("cal.Event")
    cal_Task = resolve_model("cal.Task")
    cal_AccessClass = resolve_model("cal.AccessClass")
    cal_Priority = resolve_model("cal.Priority")
    cal_TaskStatus = resolve_model("cal.TaskStatus")
    cal_EventStatus = resolve_model("cal.EventStatus")
    new_content_type_id = globals_dict['new_content_type_id']

    def create_contacts_person(contact_ptr_id, first_name, last_name, title, sex, birth_date, birth_date_circa, is_active, activity_id, bank_account1, bank_account2, remarks2, gesdos_id, is_cpas, is_senior, group_id, coached_from, coached_until, coach1_id, coach2_id, birth_place, birth_country_id, civil_state, national_id, health_insurance_id, pharmacy_id, nationality_id, card_number, card_valid_from, card_valid_until, card_type, card_issuer, noble_condition, residence_type, in_belgium_since, unemployed_since, needs_residence_permit, needs_work_permit, work_permit_suspended_until, aid_type_id, income_ag, income_wg, income_kg, income_rente, income_misc, is_seeking, unavailable_until, unavailable_why, obstacles, skills, job_agents, job_office_contact_id):
        return insert_child(contacts_Contact.objects.get(pk=contact_ptr_id),
                            contacts_Person, first_name=first_name, last_name=last_name,
                            title=title, gender=sex, birth_date=birth_date, birth_date_circa=birth_date_circa, is_active=is_active, activity_id=activity_id, bank_account1=bank_account1, bank_account2=bank_account2, remarks2=remarks2, gesdos_id=gesdos_id, is_cpas=is_cpas, is_senior=is_senior, group_id=group_id, coached_from=coached_from, coached_until=coached_until, coach1_id=coach1_id, coach2_id=coach2_id, birth_place=birth_place, birth_country_id=birth_country_id, civil_state=civil_state, national_id=national_id, health_insurance_id=health_insurance_id, pharmacy_id=pharmacy_id, nationality_id=nationality_id, card_number=card_number, card_valid_from=card_valid_from, card_valid_until=card_valid_until, card_type=card_type, card_issuer=card_issuer, noble_condition=noble_condition, residence_type=residence_type, in_belgium_since=in_belgium_since, unemployed_since=unemployed_since, needs_residence_permit=needs_residence_permit, needs_work_permit=needs_work_permit, work_permit_suspended_until=work_permit_suspended_until, aid_type_id=aid_type_id, income_ag=income_ag, income_wg=income_wg, income_kg=income_kg, income_rente=income_rente, income_misc=income_misc, is_seeking=is_seeking, unavailable_until=unavailable_until, unavailable_why=unavailable_why, obstacles=obstacles, skills=skills, job_agents=job_agents, job_office_contact_id=job_office_contact_id)
    globals_dict.update(create_contacts_person=create_contacts_person)

    def create_users_user(contact_ptr_id, first_name, last_name, title, sex, username, is_staff, is_expert, is_active, is_superuser, last_login, date_joined, is_spis):
        return insert_child(
            contacts_Contact.objects.get(pk=contact_ptr_id), users.User,
            first_name=first_name, last_name=last_name, title=title,
            gender=sex,
            username=username, is_staff=is_staff, is_expert=is_expert, is_active=is_active, is_superuser=is_superuser, last_login=last_login, date_joined=date_joined, is_spis=is_spis)
    globals_dict.update(create_users_user=create_users_user)

    def create_dsbe_personsearch(id, user_id, title, aged_from, aged_to, sex, only_my_persons, coached_by_id, period_from, period_until):
        return dsbe_PersonSearch(id=id, user_id=user_id, title=title,
                                 aged_from=aged_from, aged_to=aged_to, gender=sex,
                                 only_my_persons=only_my_persons, coached_by_id=coached_by_id, period_from=period_from, period_until=period_until)
    globals_dict.update(create_dsbe_personsearch=create_dsbe_personsearch)

    def get_it_or_none(m, ref):
        try:
            return m.objects.get(ref=ref)
        except m.DoesNotExist:
            return None

    def create_cal_event(id, user_id, created, modified, project_id, must_build, calendar_id, uid, start_date, start_time, summary, description, access_class, sequence, user_modified, rset_id, end_date, end_time, transparent, type_id, place_id, priority, status, duration_value, duration_unit):
        status = get_it_or_none(cal_EventStatus, status)
        priority = get_it_or_none(cal_Priority, priority)
        access_class = get_it_or_none(cal_AccessClass, access_class)

        return cal_Event(
            id=id, user_id=user_id, created=created, modified=modified,
            project_id=project_id, must_build=must_build, calendar_id=calendar_id,
            uid=uid, start_date=start_date, start_time=start_time,
            summary=summary, description=description,
            access_class=access_class,
            sequence=sequence, user_modified=user_modified,
            rset_id=rset_id, end_date=end_date, end_time=end_time,
            transparent=transparent, type_id=type_id, place_id=place_id,
            priority=priority,
            status=status,
            duration_value=duration_value, duration_unit=duration_unit)
    globals_dict.update(create_cal_event=create_cal_event)

    def create_cal_task(id, user_id, created, modified, owner_type_id, owner_id, project_id, calendar_id, uid, start_date, start_time, summary, description, access_class, sequence, user_modified, rset_id, due_date, due_time, done, percent, status, auto_type):
        owner_type_id = new_content_type_id(owner_type_id)
        status = get_it_or_none(cal_TaskStatus, status)
        access_class = get_it_or_none(cal_AccessClass, access_class)
        return cal_Task(id=id, user_id=user_id, created=created,
                        modified=modified, owner_type_id=owner_type_id, owner_id=owner_id,
                        project_id=project_id, calendar_id=calendar_id, uid=uid,
                        start_date=start_date, start_time=start_time, summary=summary,
                        description=description,
                        access_class=access_class,
                        sequence=sequence, user_modified=user_modified, rset_id=rset_id,
                        due_date=due_date, due_time=due_time, done=done,
                        percent=percent, status=status, auto_type=auto_type)
    globals_dict.update(create_cal_task=create_cal_task)

    objects = globals_dict['objects']

    def new_objects():
        from lino_xl.lib.cal.fixtures import std
        yield std.objects()
        yield objects()
    globals_dict.update(objects=new_objects)

    #~ raise Exception("todo: sex -> gender in Person, PersonSearch")
    return '1.2.7'


def migrate_from_1_2_7(globals_dict):
    """Convert `birth_date` fields to the new :class:`lino.fields.IncompleteDate` type.
    See :blogref:`20111119`.
    """
    from lino.utils.mti import insert_child
    contacts_Contact = resolve_model("contacts.Contact")
    contacts_Person = resolve_model("contacts.Person")

    def create_contacts_person(contact_ptr_id, birth_date, birth_date_circa, first_name, last_name, title, gender, is_active, activity_id, bank_account1, bank_account2, remarks2, gesdos_id, is_cpas, is_senior, group_id, coached_from, coached_until, coach1_id, coach2_id, birth_place, birth_country_id, civil_state, national_id, health_insurance_id, pharmacy_id, nationality_id, card_number, card_valid_from, card_valid_until, card_type, card_issuer, noble_condition, residence_type, in_belgium_since, unemployed_since, needs_residence_permit, needs_work_permit, work_permit_suspended_until, aid_type_id, income_ag, income_wg, income_kg, income_rente, income_misc, is_seeking, unavailable_until, unavailable_why, obstacles, skills, job_agents, job_office_contact_id):
        if birth_date_circa:
            raise Exception("birth_date_circa for %s %s %s" %
                            (contact_ptr_id, first_name, last_name))
        return insert_child(contacts_Contact.objects.get(pk=contact_ptr_id), contacts_Person, birth_date=birth_date, first_name=first_name, last_name=last_name, title=title, gender=gender, is_active=is_active, activity_id=activity_id, bank_account1=bank_account1, bank_account2=bank_account2, remarks2=remarks2, gesdos_id=gesdos_id, is_cpas=is_cpas, is_senior=is_senior, group_id=group_id, coached_from=coached_from, coached_until=coached_until, coach1_id=coach1_id, coach2_id=coach2_id, birth_place=birth_place, birth_country_id=birth_country_id, civil_state=civil_state, national_id=national_id, health_insurance_id=health_insurance_id, pharmacy_id=pharmacy_id, nationality_id=nationality_id, card_number=card_number, card_valid_from=card_valid_from, card_valid_until=card_valid_until, card_type=card_type, card_issuer=card_issuer, noble_condition=noble_condition, residence_type=residence_type, in_belgium_since=in_belgium_since, unemployed_since=unemployed_since, needs_residence_permit=needs_residence_permit, needs_work_permit=needs_work_permit, work_permit_suspended_until=work_permit_suspended_until, aid_type_id=aid_type_id, income_ag=income_ag, income_wg=income_wg, income_kg=income_kg, income_rente=income_rente, income_misc=income_misc, is_seeking=is_seeking, unavailable_until=unavailable_until, unavailable_why=unavailable_why, obstacles=obstacles, skills=skills, job_agents=job_agents, job_office_contact_id=job_office_contact_id)
    globals_dict.update(create_contacts_person=create_contacts_person)

    return '1.2.8'


def migrate_from_1_2_8(globals_dict):
    """
Convert Schedule and Regime fields in contracts.
NOT Convert Roles to Links (and RoleTypes to LinkTypes).
Needs manual adaption of dpy file:

- Replace line ``from lino.utils.mti import insert_child`` 
  by ``from lino.utils.mti import create_child as insert_child``
  
- Replace lines like 
  ``insert_child(contacts_Contact.objects.get(pk=contact_ptr_id),...)``
  by
  ``insert_child(contacts_Contact,contact_ptr_id,...)``
- 
    """
    jobs_Contract = resolve_model("jobs.Contract")
    Schedule = resolve_model("jobs.Schedule")
    Regime = resolve_model("jobs.Regime")

    def convert(cl, name):
        if not name:
            return None
        try:
            return cl.objects.get(name=name)
        except cl.DoesNotExist:
            obj = cl(name=name)
            obj.save()
            return obj

    def create_jobs_contract(id, user_id, must_build, person_id, contact_id, language, applies_from, applies_until, date_decided, date_issued, user_asd_id, exam_policy_id, ending_id, date_ended, type_id, provider_id, job_id, duration, regime, schedule, hourly_rate, refund_rate, reference_person, responsibilities, remark):
        schedule = convert(Schedule, schedule)
        regime = convert(Regime, regime)
        return jobs_Contract(id=id, user_id=user_id, must_build=must_build, person_id=person_id, contact_id=contact_id, language=language, applies_from=applies_from, applies_until=applies_until, date_decided=date_decided, date_issued=date_issued, user_asd_id=user_asd_id, exam_policy_id=exam_policy_id, ending_id=ending_id, date_ended=date_ended, type_id=type_id, provider_id=provider_id, job_id=job_id, duration=duration, regime=regime, schedule=schedule, hourly_rate=hourly_rate, refund_rate=refund_rate, reference_person=reference_person, responsibilities=responsibilities, remark=remark)
    globals_dict.update(create_jobs_contract=create_jobs_contract)

    #~ contacts_Role = resolve_model("links.Link")
    #~ contacts_RoleType = resolve_model("links.LinkType")

    #~ from django.contrib.contenttypes.models import ContentType
    #~ Person = resolve_model('contacts.Person')
    #~ Company = resolve_model('contacts.Company')
    #~ a_type = ContentType.objects.get_for_model(Company)
    #~ b_type = ContentType.objects.get_for_model(Person)
    #~ DEFAULT_LINKTYPE = contacts_RoleType(name='*',a_type=a_type,b_type=b_type,id=99)
    #~ DEFAULT_LINKTYPE.save()

    #~ def create_contacts_roletype(id, name, name_fr, name_en, use_in_contracts):
        #~ return contacts_RoleType(id=id,name=name,name_fr=name_fr,name_en=name_en,
            #~ a_type=a_type,b_type=b_type,
            #~ use_in_contracts=use_in_contracts)
    #~ globals_dict.update(create_contacts_roletype=create_contacts_roletype)

    #~ def create_contacts_role(id, parent_id, child_id, type_id):
        #~ if type_id is None:
            #~ type_id = DEFAULT_LINKTYPE.pk
        #~ return contacts_Role(id=id,a_id=parent_id,b_id=child_id,type_id=type_id)
    #~ globals_dict.update(create_contacts_role=create_contacts_role)

    contacts_Role = resolve_model("contacts.Role")

    def create_contacts_role(id, parent_id, child_id, type_id):
        return contacts_Role(id=id, company_id=parent_id, person_id=child_id, type_id=type_id)
    globals_dict.update(create_contacts_role=create_contacts_role)

    #~ ignore any data from previous links module:

    def create_links_link(id, user_id, person_id, company_id, type_id, date, url, name):
        return None
    globals_dict.update(create_links_link=create_links_link)

    def create_links_linktype(id, name):
        return None
    globals_dict.update(create_links_linktype=create_links_linktype)
    del globals_dict['links_LinkType']
    del globals_dict['links_Link']

    #~ Discovered that due to a bug in previous dpy versions
    #~ there were some Upload records on Role and RoleType
    #~ in a customer's database. That's why we need to redefine also the
    #~ global variables contacts_Role and contacts_RoleType:

    #~ globals_dict.update(contacts_Role=contacts_Role)
    #~ globals_dict.update(contacts_RoleType=contacts_RoleType)

    #~ add previously hard-coded jobs.Regime and jobs.Schedule from fixture

    objects = globals_dict['objects']

    def new_objects():
        from lino.modlib.jobs.fixtures import std
        yield std.objects()
        yield objects()
    globals_dict.update(objects=new_objects)

    #~ from lino.utils.mti import create_child
    #~ globals_dict.update(insert_child=create_child)
    return '1.3.0'


def migrate_from_1_3_0(globals_dict):
    return '1.3.1'


def migrate_from_1_3_1(globals_dict):
    return '1.3.2'


def migrate_from_1_3_2(globals_dict):
    """
    - new field `isip.ExamPolicy.every_unit` 
    - new `dsbe.PersonGroup.active`
    - In :class:`lino.mixins.printable.CachedPrintable`,
      BooleanField `must_build` has been replaced by a DateTimeField `build_time`.
      
    """
    cal_Event = resolve_model('cal.Event')
    cal_Guest = resolve_model('cal.Guest')
    isip_Contract = resolve_model('isip.Contract')
    jobs_Contract = resolve_model('jobs.Contract')
    jobs_ContractsSituation = resolve_model('jobs.ContractsSituation')
    lino_DataControlListing = resolve_model('lino.DataControlListing')
    mails_Mail = resolve_model('mails.Mail')
    notes_Note = resolve_model('notes.Note')
    new_content_type_id = globals_dict.get('new_content_type_id')

    def create_cal_event(id, user_id, created, modified, owner_type_id, owner_id, project_id, must_build, calendar_id, uid, start_date, start_time, summary, description, access_class_id, sequence, auto_type, user_modified, rset_id, end_date, end_time, transparent, type_id, place_id, priority_id, status_id, duration_value, duration_unit):
        owner_type_id = new_content_type_id(owner_type_id)
        obj = cal_Event(
            id=id, user_id=user_id, created=created, modified=modified, owner_type_id=owner_type_id, owner_id=owner_id, project_id=project_id,
            #~ must_build=must_build,
            calendar_id=calendar_id, uid=uid, start_date=start_date, start_time=start_time, summary=summary, description=description, access_class_id=access_class_id, sequence=sequence, auto_type=auto_type, user_modified=user_modified, rset_id=rset_id, end_date=end_date, end_time=end_time, transparent=transparent, type_id=type_id, place_id=place_id, priority_id=priority_id, status_id=status_id, duration_value=duration_value, duration_unit=duration_unit)
        obj.build_time = obj.get_cache_mtime()
        return obj
    globals_dict.update(create_cal_event=create_cal_event)

    def create_cal_guest(id, must_build, contact_id, language, event_id, role_id, status_id, remark):
        obj = cal_Guest(id=id,
                        #~ must_build=must_build,
                        contact_id=contact_id, language=language, event_id=event_id, role_id=role_id, status_id=status_id, remark=remark)
        obj.build_time = obj.get_cache_mtime()
        return obj
    globals_dict.update(create_cal_guest=create_cal_guest)

    def create_isip_contract(id, user_id, must_build, person_id, contact_id, language, applies_from, applies_until, date_decided, date_issued, user_asd_id, exam_policy_id, ending_id, date_ended, type_id, company_id, stages, goals, duties_asd, duties_dsbe, duties_company, duties_person):
        obj = isip_Contract(id=id, user_id=user_id,
                            #~ must_build=must_build,
                            person_id=person_id, contact_id=contact_id, language=language, applies_from=applies_from, applies_until=applies_until, date_decided=date_decided, date_issued=date_issued, user_asd_id=user_asd_id, exam_policy_id=exam_policy_id, ending_id=ending_id, date_ended=date_ended, type_id=type_id, company_id=company_id, stages=stages, goals=goals, duties_asd=duties_asd, duties_dsbe=duties_dsbe, duties_company=duties_company, duties_person=duties_person)
        obj.build_time = obj.get_cache_mtime()
        return obj
    globals_dict.update(create_isip_contract=create_isip_contract)

    def create_jobs_contract(id, user_id, must_build, person_id, contact_id, language, applies_from, applies_until, date_decided, date_issued, user_asd_id, exam_policy_id, ending_id, date_ended, type_id, provider_id, job_id, duration, regime_id, schedule_id, hourly_rate, refund_rate, reference_person, responsibilities, remark):
        obj = jobs_Contract(id=id, user_id=user_id,
                            #~ must_build=must_build,
                            person_id=person_id, contact_id=contact_id, language=language, applies_from=applies_from, applies_until=applies_until, date_decided=date_decided, date_issued=date_issued, user_asd_id=user_asd_id, exam_policy_id=exam_policy_id, ending_id=ending_id, date_ended=date_ended, type_id=type_id, provider_id=provider_id, job_id=job_id, duration=duration, regime_id=regime_id, schedule_id=schedule_id, hourly_rate=hourly_rate, refund_rate=refund_rate, reference_person=reference_person, responsibilities=responsibilities, remark=remark)
        obj.build_time = obj.get_cache_mtime()
        return obj
    globals_dict.update(create_jobs_contract=create_jobs_contract)

    def create_jobs_contractssituation(id, must_build, date, contract_type_id, job_type_id):
        obj = jobs_ContractsSituation(id=id,
                                      #~ must_build=must_build,
                                      date=date, contract_type_id=contract_type_id, job_type_id=job_type_id)
        obj.build_time = obj.get_cache_mtime()
        return obj
    globals_dict.update(
        create_jobs_contractssituation=create_jobs_contractssituation)

    def create_lino_datacontrollisting(id, must_build, date):
        obj = lino_DataControlListing(id=id,
                                      #~ must_build=must_build,
                                      date=date)
        obj.build_time = obj.get_cache_mtime()
        return obj
    globals_dict.update(
        create_lino_datacontrollisting=create_lino_datacontrollisting)

    def create_mails_mail(id, must_build, type_id, sender_id, subject, body, received, sent):
        obj = mails_Mail(id=id,
                         #~ must_build=must_build,
                         type_id=type_id, sender_id=sender_id, subject=subject, body=body, received=received, sent=sent)
        obj.build_time = obj.get_cache_mtime()
        return obj
    globals_dict.update(create_mails_mail=create_mails_mail)

    def create_notes_note(id, user_id, must_build, person_id, company_id, date, type_id, event_type_id, subject, body, language):
        obj = notes_Note(id=id, user_id=user_id,
                         #~ must_build=must_build,
                         person_id=person_id, company_id=company_id, date=date, type_id=type_id, event_type_id=event_type_id, subject=subject, body=body, language=language)
        obj.build_time = obj.get_cache_mtime()
        return obj
    globals_dict.update(create_notes_note=create_notes_note)

    return '1.3.3'


def migrate_from_1_3_3(globals_dict):
    """
    Convert Person.residence_type data type from INT to CHAR.
    """

    contacts_Contact = resolve_model("contacts.Contact")
    contacts_Person = resolve_model("contacts.Person")
    from lino.utils.mti import create_child

    def create_contacts_person(contact_ptr_id, birth_date, first_name, last_name, title, gender, is_active, newcomer, is_deprecated, activity_id, bank_account1, bank_account2, remarks2, gesdos_id, is_cpas, is_senior, group_id, coached_from, coached_until, coach1_id, coach2_id, birth_place, birth_country_id, civil_state, national_id, health_insurance_id, pharmacy_id, nationality_id, card_number, card_valid_from, card_valid_until, card_type, card_issuer, noble_condition, residence_type, in_belgium_since, unemployed_since, needs_residence_permit, needs_work_permit, work_permit_suspended_until, aid_type_id, income_ag, income_wg, income_kg, income_rente, income_misc, is_seeking, unavailable_until, unavailable_why, obstacles, skills, job_agents, job_office_contact_id):
        residence_type = str(residence_type)
        return create_child(contacts_Contact, contact_ptr_id, contacts_Person, birth_date=birth_date, first_name=first_name, last_name=last_name, title=title, gender=gender, is_active=is_active, newcomer=newcomer, is_deprecated=is_deprecated, activity_id=activity_id, bank_account1=bank_account1, bank_account2=bank_account2, remarks2=remarks2, gesdos_id=gesdos_id, is_cpas=is_cpas, is_senior=is_senior, group_id=group_id, coached_from=coached_from, coached_until=coached_until, coach1_id=coach1_id, coach2_id=coach2_id, birth_place=birth_place, birth_country_id=birth_country_id, civil_state=civil_state, national_id=national_id, health_insurance_id=health_insurance_id, pharmacy_id=pharmacy_id, nationality_id=nationality_id, card_number=card_number, card_valid_from=card_valid_from, card_valid_until=card_valid_until, card_type=card_type, card_issuer=card_issuer, noble_condition=noble_condition, residence_type=residence_type, in_belgium_since=in_belgium_since, unemployed_since=unemployed_since, needs_residence_permit=needs_residence_permit, needs_work_permit=needs_work_permit, work_permit_suspended_until=work_permit_suspended_until, aid_type_id=aid_type_id, income_ag=income_ag, income_wg=income_wg, income_kg=income_kg, income_rente=income_rente, income_misc=income_misc, is_seeking=is_seeking, unavailable_until=unavailable_until, unavailable_why=unavailable_why, obstacles=obstacles, skills=skills, job_agents=job_agents, job_office_contact_id=job_office_contact_id)
    globals_dict.update(create_contacts_person=create_contacts_person)

    return '1.3.4'


def migrate_from_1_3_4(globals_dict):
    return '1.3.5'


def migrate_from_1_3_5(globals_dict):
    return '1.3.6'


def migrate_from_1_3_6(globals_dict):
    """\
Adds new fields Person.broker, Person.faculty, User.is_newcomer, User.newcomer_quota
and new models Broker and Faculty, Competence."""
    return '1.3.7'


def migrate_from_1_3_7(globals_dict):
    """
    - Remove field newcomers.Faculty.body
    - Add field dsbe.CourseRequest.urgent
    """
    newcomers_Faculty = resolve_model("newcomers.Faculty")

    def create_newcomers_faculty(id, name, body, body_fr, body_en, name_fr, name_en):
        return newcomers_Faculty(id=id, name=name, name_fr=name_fr, name_en=name_en)
    globals_dict.update(create_newcomers_faculty=create_newcomers_faculty)
    return '1.3.8'


def migrate_from_1_3_8(globals_dict):
    """
    - Remove fields `cal.Event.duration_value` and `cal.Event.duration_unit`
    """
    cal_Event = resolve_model("cal.Event")
    new_content_type_id = globals_dict['new_content_type_id']

    def create_cal_event(id, user_id, created, modified, owner_type_id, owner_id, project_id, build_time, calendar_id, uid, start_date, start_time, summary, description, access_class_id, sequence, auto_type, user_modified, rset_id, end_date, end_time, transparent, type_id, place_id, priority_id, status_id, duration_value, duration_unit):
        owner_type_id = new_content_type_id(owner_type_id)
        return cal_Event(
            id=id, user_id=user_id, created=created, modified=modified,
            owner_type_id=owner_type_id, owner_id=owner_id, project_id=project_id,
            build_time=build_time, calendar_id=calendar_id,
            uid=uid, start_date=start_date, start_time=start_time,
            summary=summary, description=description, access_class_id=access_class_id,
            sequence=sequence, auto_type=auto_type,
            user_modified=user_modified, rset_id=rset_id, end_date=end_date, end_time=end_time,
            transparent=transparent, type_id=type_id, place_id=place_id,
            priority_id=priority_id, status_id=status_id
            #~ ,duration_value=duration_value,duration_unit=duration_unit
        )
    globals_dict.update(create_cal_event=create_cal_event)
    return '1.3.9'


def migrate_from_1_3_9(globals_dict):
    """
    - remove tables lino_datacontrollisting and jobs_contractssituation
    """
    def lino_datacontrollisting_objects():
        return None
    globals_dict.update(
        lino_datacontrollisting_objects=lino_datacontrollisting_objects)

    def jobs_contractssituation_objects():
        return None
    globals_dict.update(
        jobs_contractssituation_objects=jobs_contractssituation_objects)
    return '1.4.0'


def migrate_from_1_4_0(globals_dict):
    """
    No database changes.
    """
    return '1.4.1'


def migrate_from_1_4_1(globals_dict):
    """
    Some new fields in IdentifyPersonRequest with default values.
    """
    return '1.4.2'


def migrate_from_1_4_2(globals_dict):
    """
    Field `jobs.contract.provider` renamed to company
    """
    jobs_Contract = resolve_model("jobs.Contract")

    def create_jobs_contract(id, user_id, build_time, person_id, contact_id, language, applies_from, applies_until, date_decided, date_issued, user_asd_id, exam_policy_id, ending_id, date_ended, type_id, provider_id, job_id, duration, regime_id, schedule_id, hourly_rate, refund_rate, reference_person, responsibilities, remark):
        return jobs_Contract(id=id, user_id=user_id, build_time=build_time,
                             person_id=person_id, contact_id=contact_id,
                             language=language, applies_from=applies_from,
                             applies_until=applies_until, date_decided=date_decided,
                             date_issued=date_issued, user_asd_id=user_asd_id,
                             exam_policy_id=exam_policy_id, ending_id=ending_id,
                             date_ended=date_ended, type_id=type_id,
                             #~ provider_id=provider_id,
                             company_id=provider_id,
                             job_id=job_id, duration=duration, regime_id=regime_id, schedule_id=schedule_id, hourly_rate=hourly_rate, refund_rate=refund_rate, reference_person=reference_person, responsibilities=responsibilities, remark=remark)
    globals_dict.update(create_jobs_contract=create_jobs_contract)
    return '1.4.3'


def migrate_from_1_4_3(globals_dict):
    """
    - :mod:`lino_xl.lib.contacts` : renamed "Contact" to "Partner".
    - :mod:`lino_xl.lib.outbox` : renamed "Mail.contact" to "Mail.partner".
    - renamed "bcss" to "cbss"
    - renamed "lino.apps.dsbe" to "lino.apps.pcsw"
    - cal.Event.rset
    - new user permissions system (fields like `is_staff` replaced by `level`)
    - manually handle invalid contracts and persons. See :blogref:`20120418`.
    - removed field `title` from bcss.IdentifyPersonRequest
    - Users are no longer MTI subclass of Partner but have a FK `partner`. 
    - `cbss.IdentifyPersonRequest`: field `project` replaced by `person`.
    - convert Person.civil_state to choicelist CivilState
    - new tables cbss.Purpose and cbss.Sector
    - add default data from library fixtures (debts, households, purposes)
    - convert Companies with prefix == 'Eheleute' to a Household
    - convert tables cal.EventStatus, cal.TaskStatus and cal.GuestStatus to choicelists.
    - table thirds.Third no longer exists
    - new fields MailableType to cal.EventType and notes.NoteType
    - severe test in isip.Contract
    - added workflow to modules courses and cal
    - notes.Note is now ProjectRelated 
      (and field `company` is injected by lino.apps.pcsw)
    """
    from lino.core.utils import resolve_model
    from lino.utils.mti import create_child
    from lino.modlib.users.models import UserTypes
    #~ from lino.utils import mti
    #~ from lino.utils import dblogger

    contacts_Contact = resolve_model("contacts.Partner")
    users.User = resolve_model("users.User")
    globals_dict.update(contacts_Contact=contacts_Contact)
    globals_dict.update(
        bcss_IdentifyPersonRequest=resolve_model("cbss.IdentifyPersonRequest"))
    globals_dict.update(dsbe_Activity=resolve_model("pcsw.Activity"))
    globals_dict.update(dsbe_AidType=resolve_model("pcsw.AidType"))
    globals_dict.update(dsbe_Course=resolve_model("courses.Course"))
    globals_dict.update(
        dsbe_CourseContent=resolve_model("courses.CourseContent"))
    #~ globals_dict.update(dsbe_CourseEnding = resolve_model("courses.CourseEnding"))
    globals_dict.update(
        dsbe_CourseOffer=resolve_model("courses.CourseOffer"))
    globals_dict.update(
        dsbe_CourseProvider=resolve_model("courses.CourseProvider"))
    globals_dict.update(
        dsbe_CourseRequest=resolve_model("courses.CourseRequest"))
    globals_dict.update(dsbe_Exclusion=resolve_model("pcsw.Exclusion"))
    globals_dict.update(
        dsbe_ExclusionType=resolve_model("pcsw.ExclusionType"))
    globals_dict.update(
        dsbe_LanguageKnowledge=resolve_model("cv.LanguageKnowledge"))
    globals_dict.update(dsbe_PersonGroup=resolve_model("pcsw.PersonGroup"))
    globals_dict.update(dsbe_PersonSearch=resolve_model("pcsw.PersonSearch"))
    globals_dict.update(
        dsbe_WantedLanguageKnowledge=resolve_model("pcsw.WantedLanguageKnowledge"))

    mails_Recipient = resolve_model("mails.Recipient")

    def create_mails_recipient(id, mail_id, contact_id, type, address, name):
        return mails_Recipient(id=id, mail_id=mail_id, partner_id=contact_id, type=type, address=address, name=name)
    globals_dict.update(create_mails_recipient=create_mails_recipient)

    cal_Event = resolve_model("cal.Event")
    from lino_xl.lib.cal.utils import EntryStates, TaskState, GuestState
    new_content_type_id = globals_dict['new_content_type_id']

    def create_cal_event(id, user_id, created, modified, owner_type_id, owner_id, project_id, build_time, calendar_id, uid, start_date, start_time, summary, description, access_class_id, sequence, auto_type, user_modified, rset_id, end_date, end_time, transparent, type_id, place_id, priority_id, status_id):
        owner_type_id = new_content_type_id(owner_type_id)
        state = EntryStates.migrate(status_id)
        if state is None:
            if start_date < datetime.date.today():
                state = EntryStates.obsolete
            elif user_modified:
                state = EntryStates.draft
        calendar_id = type_id or 2
        return cal_Event(
            id=id, user_id=user_id, created=created, modified=modified, owner_type_id=owner_type_id, owner_id=owner_id, project_id=project_id, build_time=build_time, calendar_id=calendar_id, uid=uid, start_date=start_date, start_time=start_time, summary=summary, description=description,
            #~ access_class_id=access_class_id,
            sequence=sequence, auto_type=auto_type,
            #~ user_modified=user_modified,
            #~ rset_id=rset_id,
            end_date=end_date, end_time=end_time, transparent=transparent,
            #~ type_id=type_id,
            place_id=place_id, priority_id=priority_id, state=state)
    globals_dict.update(create_cal_event=create_cal_event)

    cal_Task = resolve_model("cal.Task")

    def create_cal_task(id, user_id, created, modified, owner_type_id, owner_id, project_id, calendar_id, uid, start_date, start_time, summary, description, access_class_id, sequence, auto_type, user_modified, rset_id, due_date, due_time, done, percent, status_id):
        owner_type_id = new_content_type_id(owner_type_id)
        state = TaskState.migrate(status_id)
        if done:
            state = TaskState.done
        elif state is None and user_modified:
            state = TaskState.todo
        calendar_id = None
        return cal_Task(
            id=id, user_id=user_id, created=created, modified=modified, owner_type_id=owner_type_id, owner_id=owner_id,
            project_id=project_id, calendar_id=calendar_id, uid=uid, start_date=start_date, start_time=start_time, summary=summary, description=description,
            #~ access_class_id=access_class_id,
            sequence=sequence, auto_type=auto_type,
            #~ user_modified=user_modified,
            #~ rset_id=rset_id,
            due_date=due_date, due_time=due_time,
            # done=done,
            percent=percent,
            state=state)
    globals_dict.update(create_cal_task=create_cal_task)

    cal_Guest = resolve_model("cal.Guest")

    def create_cal_guest(id, build_time, contact_id, language, event_id, role_id, status_id, remark):
        return cal_Guest(
            id=id, build_time=build_time, contact_id=contact_id, language=language,
            event_id=event_id, role_id=role_id,
            #~ status_id=GuestState.migrate(status_id),
            remark=remark)
    globals_dict.update(create_cal_guest=create_cal_guest)

    def create_users_user(contact_ptr_id, first_name, last_name, title, gender, username, is_staff, is_expert, is_active, is_superuser, last_login, date_joined, is_spis, is_newcomers, newcomer_quota):
        kw = dict()
        #~ if is_staff or is_expert or is_superuser:
            # level = UserLevels.manager
            #~ kw.update(user_type=UserTypes.gerd)
            # kw.update(level=level)
        #~ else:
            #~ level = UserLevel.user
        #~ if is_spis:
            #~ kw.update(level=level)
            #~ kw.update(integ_level = level)
            #~ kw.update(cbss_level = level)
        #~ if is_newcomers:
            #~ kw.update(level=level)
            #~ kw.update(newcomers_level = level)
        if username in ('gerd', 'lsaffre'):
            kw.update(user_type='900')  # UserTypes.admin)
        elif username in ('hubert', 'alicia', 'uwe'):
            kw.update(profile='100')  # UserTypes.hubert)
        #~ elif username == 'gerd':
            #~ kw.update(debts_level=UserLevel.manager)
        elif username == 'kerstin':
            kw.update(profile='300')  # UserTypes.kerstin)
        elif username == 'caroline':
            kw.update(profile='200')  # UserTypes.caroline)
            #~ kw.update(debts_level=UserLevel.user)
            #~ kw.update(level=UserLevel.user)
        #~ return create_child(contacts_Contact,contact_ptr_id,users.User,
        if not date_joined:
            date_joined = datetime.datetime.now()
        return users.User(partner_id=contact_ptr_id,
                          id=contact_ptr_id,
                          first_name=first_name, last_name=last_name,
                          email=contacts_Contact.objects.get(
                              pk=contact_ptr_id).email,
                          #~ title=title,gender=gender,
                          username=username,
                          #~ is_staff=is_staff,is_expert=is_expert,is_active=is_active,is_superuser=is_superuser,
                          #~ last_login=last_login,date_joined=date_joined,
                          created=date_joined,
                          modified=date_joined,
                          #~ is_spis=is_spis,is_newcomers=is_newcomers,
                          newcomer_quota=newcomer_quota, **kw)
    globals_dict.update(create_users_user=create_users_user)

    #~ from django.core.exceptions import ValidationError

    isip_Contract = resolve_model("isip.Contract")

    def create_isip_contract(id, user_id, build_time, person_id, company_id, contact_id, language, applies_from, applies_until, date_decided, date_issued, user_asd_id, exam_policy_id, ending_id, date_ended, type_id, stages, goals, duties_asd, duties_dsbe, duties_company, duties_person):
        #~ - isip.Contract [u'Contracts ends before it started.'] (3 object(s), e.g. Contract(id=62,user=200085,person=21936,langua
        #~ ge=u'de',applies_from=datetime.date(2009, 12, 19),date_decided=datetime.date(2010, 1, 14),date_issued=datetime.date(2010
        #~ , 1, 14),ending=2,date_ended=datetime.date(2009, 8, 31),type=9,stages=u'Abitur'))
        if id == 62:
            date_ended = applies_from

        #~ - isip.Contract [u'Contracts ends before it started.'] (2 object(s), e.g. Contract(id=204,user=200096,person=22287,langu
        #~ age=u'de',applies_from=datetime.date(2011, 12, 1),applies_until=datetime.date(2011, 8, 1),user_asd=200088,exam_policy=1,
        #~ type=7))
        if id == 204:
            applies_from = applies_until
            #~ applies_until = None

        #~ - isip.Contract [u'Contracts ends before it started.'] (1 object(s), e.g. Contract(id=325,user=200099,build_time=datetim
        #~ e.datetime(2012, 4, 12, 9, 51, 19),person=22423,language=u'de',applies_from=datetime.date(2012, 4, 1),applies_until=date
        #~ time.date(2011, 7, 31),date_decided=datetime.date(2012, 4, 12),date_issued=datetime.date(2012, 4, 12),user_asd=200097,ex
        #~ '))
        if id == 325:
            applies_until = None
            #~ applies_until = None
        return isip_Contract(pk=id, user_id=user_id, build_time=build_time, person_id=person_id, company_id=company_id, contact_id=contact_id, language=language, applies_from=applies_from, applies_until=applies_until, date_decided=date_decided, date_issued=date_issued, user_asd_id=user_asd_id, exam_policy_id=exam_policy_id, ending_id=ending_id, date_ended=date_ended, type_id=type_id, stages=stages, goals=goals, duties_asd=duties_asd, duties_dsbe=duties_dsbe, duties_company=duties_company, duties_person=duties_person)
    #~ 20120604 globals_dict.update(create_isip_contract=create_isip_contract)

    jobs_Contract = resolve_model("jobs.Contract")

    def create_jobs_contract(id, user_id, build_time, person_id, company_id, contact_id, language, applies_from, applies_until, date_decided, date_issued, user_asd_id, exam_policy_id, ending_id, date_ended, type_id, job_id, duration, regime_id, schedule_id, hourly_rate, refund_rate, reference_person, responsibilities, remark):
        if id == 153:  # VSE#62 : [u'Contracts ends before it started.
            # was 31.08.-01.09.2011, now 01.09.-01.09.2011
            applies_until = applies_from
            #~ applies_until = None
        return jobs_Contract(id=id, user_id=user_id, build_time=build_time, person_id=person_id, company_id=company_id, contact_id=contact_id, language=language, applies_from=applies_from, applies_until=applies_until, date_decided=date_decided, date_issued=date_issued, user_asd_id=user_asd_id, exam_policy_id=exam_policy_id, ending_id=ending_id, date_ended=date_ended, type_id=type_id, job_id=job_id, duration=duration, regime_id=regime_id, schedule_id=schedule_id, hourly_rate=hourly_rate, refund_rate=refund_rate, reference_person=reference_person, responsibilities=responsibilities, remark=remark)
    #~ 20120604 globals_dict.update(create_jobs_contract=create_jobs_contract)

    bcss_IdentifyPersonRequest = resolve_model("cbss.IdentifyPersonRequest")

    def create_bcss_identifypersonrequest(id, user_id, project_id, birth_date, first_name, last_name, title, gender, sent, status, request_xml, response_xml, national_id, middle_name, tolerance):
        if not birth_date:
            return None
        return bcss_IdentifyPersonRequest(
            id=id, user_id=user_id, person_id=project_id,
            birth_date=birth_date, first_name=first_name, last_name=last_name,
            gender=gender, sent=sent, status=status, request_xml=request_xml, response_xml=response_xml, national_id=national_id, middle_name=middle_name, tolerance=tolerance)
    globals_dict.update(
        create_bcss_identifypersonrequest=create_bcss_identifypersonrequest)

    from lino_xl.lib.courses.models import CourseRequestStates
    #~ courses_CourseRequest = resolve_model("courses.CourseRequest")
    dsbe_CourseRequest = resolve_model("courses.CourseRequest")

    def create_dsbe_courserequest(id, person_id, offer_id, content_id, date_submitted, urgent, course_id, remark, date_ended, ending_id):
        state = CourseRequestStates.migrate(ending_id)
        if course_id is not None and state == CourseRequestStates.candidate:
            state = CourseRequestStates.registered
        return dsbe_CourseRequest(
            id=id, person_id=person_id, offer_id=offer_id, content_id=content_id, date_submitted=date_submitted,
            urgent=urgent,
            course_id=course_id, remark=remark, date_ended=date_ended,
            state=state)
            #~ ending_id=ending_id)
    globals_dict.update(create_dsbe_courserequest=create_dsbe_courserequest)

    from lino.apps.pcsw.models import CivilState
    contacts_Person = resolve_model("contacts.Person")

    def create_contacts_person(contact_ptr_id, birth_date, first_name, last_name, title, gender, is_active, newcomer, is_deprecated, activity_id, bank_account1, bank_account2, remarks2, gesdos_id, is_cpas, is_senior, group_id, coached_from, coached_until, coach1_id, coach2_id, birth_place, birth_country_id, civil_state, national_id, health_insurance_id, pharmacy_id, nationality_id, card_number, card_valid_from, card_valid_until, card_type, card_issuer, noble_condition, residence_type, in_belgium_since, unemployed_since, needs_residence_permit, needs_work_permit, work_permit_suspended_until, aid_type_id, income_ag, income_wg, income_kg, income_rente, income_misc, is_seeking, unavailable_until, unavailable_why, obstacles, skills, job_agents, job_office_contact_id, broker_id, faculty_id):
        civil_state = CivilState.old2new(civil_state)
        if title in ("Herr", "Herrn", "Frau", u"Fräulein", "Madame"):
            title = ''

        return create_child(contacts_Contact, contact_ptr_id, contacts_Person, birth_date=birth_date, first_name=first_name, last_name=last_name, title=title, gender=gender, is_active=is_active, newcomer=newcomer, is_deprecated=is_deprecated, activity_id=activity_id, bank_account1=bank_account1, bank_account2=bank_account2, remarks2=remarks2, gesdos_id=gesdos_id, is_cpas=is_cpas, is_senior=is_senior, group_id=group_id, coached_from=coached_from, coached_until=coached_until, coach1_id=coach1_id, coach2_id=coach2_id, birth_place=birth_place, birth_country_id=birth_country_id, civil_state=civil_state, national_id=national_id, health_insurance_id=health_insurance_id, pharmacy_id=pharmacy_id, nationality_id=nationality_id, card_number=card_number, card_valid_from=card_valid_from, card_valid_until=card_valid_until, card_type=card_type, card_issuer=card_issuer, noble_condition=noble_condition, residence_type=residence_type, in_belgium_since=in_belgium_since, unemployed_since=unemployed_since, needs_residence_permit=needs_residence_permit, needs_work_permit=needs_work_permit, work_permit_suspended_until=work_permit_suspended_until, aid_type_id=aid_type_id, income_ag=income_ag, income_wg=income_wg, income_kg=income_kg, income_rente=income_rente, income_misc=income_misc, is_seeking=is_seeking, unavailable_until=unavailable_until, unavailable_why=unavailable_why, obstacles=obstacles, skills=skills, job_agents=job_agents, job_office_contact_id=job_office_contact_id, broker_id=broker_id, faculty_id=faculty_id)
    globals_dict.update(create_contacts_person=create_contacts_person)

    contacts_Company = resolve_model("contacts.Company")
    households_Household = resolve_model("households.Household")
    households_Type = resolve_model("households.Type")

    def create_contacts_company(contact_ptr_id, prefix, vat_id, type_id, is_active, newcomer, is_deprecated, activity_id, bank_account1, bank_account2, hourly_rate):
        if prefix == 'Eheleute' and vat_id.endswith('.999'):
            type = households_Type.objects.get(pk=1)
            return create_child(contacts_Contact, contact_ptr_id, households_Household, type=type, is_active=is_active, newcomer=newcomer, is_deprecated=is_deprecated, activity_id=activity_id, bank_account1=bank_account1, bank_account2=bank_account2)
        return create_child(contacts_Contact, contact_ptr_id, contacts_Company, prefix=prefix, vat_id=vat_id, type_id=type_id, is_active=is_active, newcomer=newcomer, is_deprecated=is_deprecated, activity_id=activity_id, bank_account1=bank_account1, bank_account2=bank_account2, hourly_rate=hourly_rate)
    globals_dict.update(create_contacts_company=create_contacts_company)

    def create_cal_taskstatus(id, name, ref, name_fr, name_en):
        pass
    globals_dict.update(create_cal_taskstatus=create_cal_taskstatus)

    def create_cal_eventstatus(id, name, ref, reminder, name_fr, name_en):
        pass
    globals_dict.update(create_cal_eventstatus=create_cal_eventstatus)

    def create_cal_gueststatus(id, name, ref, name_fr, name_en):
        pass
    globals_dict.update(create_cal_gueststatus=create_cal_gueststatus)

    def create_thirds_third(*args):
        dblogger.info("Ignored thirds.Third %r", args)
        return None
    globals_dict.update(create_thirds_third=create_thirds_third)

    def create_dsbe_courseending(*args):
        dblogger.info("Ignored dsbe.CourseEnding %r", args)
        return None
    globals_dict.update(create_dsbe_courseending=create_dsbe_courseending)

    notes_NoteType = resolve_model("notes.NoteType")

    def create_notes_notetype(id, name, build_method, template, important, remark, name_fr, name_en):
        return notes_NoteType(id=id, name=name, build_method=build_method,
                              email_template='Default.eml.html',
                              template=template, important=important, remark=remark, name_fr=name_fr,
                              name_en=name_en)
    globals_dict.update(create_notes_notetype=create_notes_notetype)

    notes_Note = resolve_model("notes.Note")

    def create_notes_note(id, user_id, build_time, person_id, company_id, date, type_id, event_type_id, subject, body, language):
        return notes_Note(id=id, user_id=user_id, build_time=build_time,
                          #~ person_id=person_id,
                          project_id=person_id,
                          company_id=company_id, date=date, type_id=type_id, event_type_id=event_type_id, subject=subject, body=body, language=language)
    globals_dict.update(create_notes_note=create_notes_note)

    #~ cal_EventType = resolve_model("cal.EventType")
    #~ def create_cal_eventtype(id, name, build_method, template, name_fr, name_en):
        #~ return cal_EventType(id=id,name=name,build_method=build_method,template=template,
          #~ email_template='Default.eml.html',
          #~ name_fr=name_fr,name_en=name_en)
    #~ globals_dict.update(create_cal_eventtype=create_cal_eventtype)

    #~ cal_Calendar= resolve_model("cal.Calendar")
    #~ def create_cal_calendar(id, user_id, type, name, description,
        #~ url_template, username, password, readonly, is_default, is_hidden, start_date, color):
        #~ return cal_Calendar(id=id,user_id=user_id,type=type,name=name,description=description,url_template=url_template,username=username,password=password,readonly=readonly,is_default=is_default,is_private=is_hidden,start_date=start_date,color=color)
    #~ globals_dict.update(create_cal_calendar=create_cal_calendar)

    cal_Calendar = resolve_model("cal.Calendar")
    #~ cal_EventType = resolve_model("cal.EventType")

    def create_cal_eventtype(id, name, build_method, template, name_fr, name_en):
        return cal_Calendar(
            id=id, name=name, build_method=build_method, template=template,
            email_template='Default.eml.html',
            name_fr=name_fr, name_en=name_en)
    globals_dict.update(create_cal_eventtype=create_cal_eventtype)

    def create_cal_calendar(id, user_id, type, name, description,
                            url_template, username, password, readonly, is_default, is_hidden, start_date, color):
        return None
        #~ return cal_Calendar(id=id,user_id=user_id,type=type,name=name,description=description,url_template=url_template,username=username,password=password,readonly=readonly,is_default=is_default,is_private=is_hidden,start_date=start_date,color=color)
    globals_dict.update(create_cal_calendar=create_cal_calendar)

    def create_cal_accessclass(*args):
        return None
    globals_dict.update(create_cal_accessclass=create_cal_accessclass)

    objects = globals_dict['objects']

    def new_objects():
        from lino_xl.lib.households.fixtures import std
        yield std.objects()
        from lino.modlib.debts.fixtures import std
        yield std.objects()
        yield objects()
        from lino.modlib.cbss.fixtures import cbss
        yield cbss.objects()
        #~ from lino.modlib.cbss.fixtures import purposes
        #~ yield purposes.objects()
        #~ from lino.modlib.cbss.fixtures import inscodes
        #~ yield inscodes.objects()
    globals_dict.update(objects=new_objects)

    return '1.4.4'


def migrate_from_1_4_4(globals_dict):
    return '1.4.5'


def migrate_from_1_4_5(globals_dict):
    return '1.4.6'


def migrate_from_1_4_6(globals_dict):
    return '1.4.7'


def migrate_from_1_4_7(globals_dict):
    return '1.4.8'


def migrate_from_1_4_8(globals_dict):
    return '1.4.9'


def migrate_from_1_4_9(globals_dict):
    return '1.4.10'


class Migrator(Migrator):
    def migrate_from_1_4_10(self, globals_dict):
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
        users.User = resolve_model("users.User")
        isip_Contract = resolve_model("isip.Contract")
        jobs_Contract = resolve_model("jobs.Contract")
        contacts_Role = resolve_model("contacts.Role")
        properties_PropType = resolve_model("properties.PropType")
        isip_ExamPolicy = resolve_model("isip.ExamPolicy")

        cal = dd.resolve_app('cal')
        pcsw = dd.resolve_app('pcsw')
        postings = dd.resolve_app('postings')

        NOW = datetime.datetime(2012, 9, 6, 0, 0)

        def find_contact(contact_id):
            try:
                return contacts_Role.objects.get(pk=contact_id)
            except contacts_Role.DoesNotExist:
                return None

        def convert_region(region):
            region = region.strip()
            if not region:
                return None
            try:
                return countries_City.objects.get(name=region, country__id='BE')
            except countries_City.DoesNotExist:
                o = countries_City(name=region, country__id='BE')
                o.full_clean()
                o.save()
                logger.info("Created region %s", o)
                return o

        def create_contacts_partner(id, country_id, city_id, name, addr1, street_prefix, street, street_no, street_box, addr2, zip_code, region, language, email, url, phone, gsm, fax, remarks):
            region = convert_region(region)
            return contacts_Partner(id=id, country_id=country_id, city_id=city_id, name=name, addr1=addr1, street_prefix=street_prefix, street=street, street_no=street_no, street_box=street_box, addr2=addr2, zip_code=zip_code, region=region, language=language, email=email, url=url, phone=phone, gsm=gsm, fax=fax, remarks=remarks, modified=NOW, created=NOW)
        globals_dict.update(create_contacts_partner=create_contacts_partner)

        def create_countries_city(id, name, country_id, zip_code, inscode):
            return countries_City(id=id, name=name,
                                  type=CityTypes.city,
                                  country_id=country_id, zip_code=zip_code, inscode=inscode)
        globals_dict.update(create_countries_city=create_countries_city)

        def create_debts_account(id, name, seqno, group_id, type, required_for_household, required_for_person, periods, help_text, name_fr, name_en):
            if periods is not None:
                periods = Decimal(periods)
            return debts_Account(id=id, name=name, seqno=seqno, group_id=group_id, type=type, required_for_household=required_for_household, required_for_person=required_for_person, periods=periods, help_text=help_text, name_fr=name_fr, name_en=name_en)
        globals_dict.update(create_debts_account=create_debts_account)

        def create_debts_accountgroup(id, name, seqno, account_type, help_text, name_fr, name_en):
            #~ return debts_AccountGroup(id=id,chart_id=1,name=name,seqno=seqno,account_type=account_type,help_text=help_text,name_fr=name_fr,name_en=name_en)
            return debts_AccountGroup(id=id, chart_id=1, name=name, ref=str(seqno), account_type=account_type, help_text=help_text, name_fr=name_fr, name_en=name_en)
        globals_dict.update(create_debts_accountgroup=create_debts_accountgroup)

        def create_contacts_company(partner_ptr_id, prefix, vat_id, type_id, is_active, newcomer, is_deprecated, activity_id, bank_account1, bank_account2, hourly_rate):
            p = contacts_Partner.objects.get(pk=partner_ptr_id)
            p.is_obsolete = is_deprecated
            p.activity_id = activity_id
            p.bank_account1 = bank_account1
            p.bank_account2 = bank_account2
            p.save()
            return create_child(
                contacts_Partner, partner_ptr_id, contacts_Company, prefix=prefix, vat_id=vat_id, type_id=type_id,
                #~ is_active=is_active,
                #~ newcomer=newcomer,
                #~ hourly_rate=hourly_rate
            )
        globals_dict.update(create_contacts_company=create_contacts_company)

        def create_households_household(partner_ptr_id, is_active, newcomer, is_deprecated, activity_id, bank_account1, bank_account2, prefix, type_id):
            p = contacts_Partner.objects.get(pk=partner_ptr_id)
            p.is_obsolete = is_deprecated
            p.activity_id = activity_id
            p.bank_account1 = bank_account1
            p.bank_account2 = bank_account2
            p.save()
            return create_child(
                contacts_Partner, partner_ptr_id, households_Household,
                #~ is_active=is_active,newcomer=newcomer,
                #~ is_deprecated=is_deprecated,activity_id=activity_id,bank_account1=bank_account1,bank_account2=bank_account2,
                prefix=prefix, type_id=type_id)
        globals_dict.update(
            create_households_household=create_households_household)

        def create_contacts_person(partner_ptr_id, birth_date, first_name, last_name, title, gender, is_active, newcomer, is_deprecated, activity_id, bank_account1, bank_account2, remarks2, gesdos_id, is_cpas, is_senior, group_id, coached_from, coached_until, coach1_id, coach2_id, birth_place, birth_country_id, civil_state, national_id, health_insurance_id, pharmacy_id, nationality_id, card_number, card_valid_from, card_valid_until, card_type, card_issuer, noble_condition, residence_type, in_belgium_since, unemployed_since, needs_residence_permit, needs_work_permit, work_permit_suspended_until, aid_type_id, income_ag, income_wg, income_kg, income_rente, income_misc, is_seeking, unavailable_until, unavailable_why, obstacles, skills, job_agents, job_office_contact_id, broker_id, faculty_id):
            p = contacts_Partner.objects.get(pk=partner_ptr_id)
            p.is_obsolete = is_deprecated
            p.activity_id = activity_id
            p.bank_account1 = bank_account1
            p.bank_account2 = bank_account2
            p.save()

            yield create_child(contacts_Partner, partner_ptr_id, contacts_Person,
                               birth_date=birth_date,
                               first_name=first_name, last_name=last_name, title=title, gender=gender,
                               #~ is_active=is_active,newcomer=newcomer,
                               #~ is_deprecated=is_deprecated,activity_id=activity_id,
                               #~ bank_account1=bank_account1,bank_account2=bank_account2
                               )
            #~ if national_id and national_id.strip() != '0' and not is_deprecated:
            if national_id.strip() == '0':
                national_id = ''
            remarks2 = remarks2.strip()
            if national_id or gesdos_id or remarks2:
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
                yield create_child(contacts_Person, partner_ptr_id, pcsw_Client,
                                   #~ birth_date=birth_date,
                                   #~ first_name=first_name,last_name=last_name,title=title,gender=gender,
                                   #~ is_active=is_active,newcomer=newcomer,is_deprecated=is_deprecated,
                                   #~ activity_id=activity_id,
                                   #~ bank_account1=bank_account1,bank_account2=bank_account2,
                                   remarks2=remarks2, gesdos_id=gesdos_id, is_cpas=is_cpas,
                                   is_senior=is_senior, group_id=group_id,
                                   #~ coached_from=coached_from,coached_until=coached_until,
                                   #~ coach1_id=coach1_id,coach2_id=coach2_id,
                                   birth_place=birth_place,
                                   birth_country_id=birth_country_id, civil_state=civil_state,
                                   national_id=national_id,
                                   client_state=client_state,
                                   health_insurance_id=health_insurance_id, pharmacy_id=pharmacy_id,
                                   nationality_id=nationality_id, card_number=card_number, card_valid_from=card_valid_from, card_valid_until=card_valid_until, card_type=card_type, card_issuer=card_issuer, noble_condition=noble_condition, residence_type=residence_type, in_belgium_since=in_belgium_since, unemployed_since=unemployed_since, needs_residence_permit=needs_residence_permit, needs_work_permit=needs_work_permit, work_permit_suspended_until=work_permit_suspended_until, aid_type_id=aid_type_id, income_ag=income_ag, income_wg=income_wg, income_kg=income_kg, income_rente=income_rente, income_misc=income_misc, is_seeking=is_seeking, unavailable_until=unavailable_until, unavailable_why=unavailable_why, obstacles=obstacles, skills=skills, job_agents=job_agents,
                                   job_office_contact_id=job_office_contact_id, broker_id=broker_id, faculty_id=faculty_id)
                #~ if coached_from or coached_until:

                def user2type(user_id):
                    #~ pcsw_CoachingType
                    if user_id in (200085, 200093, 200096, 200099):
                        return 2  # DSBE
                    return 1  # ASD
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
                    obj._before_dumpy_save = add_contact_fields(
                        obj, job_office_contact_id)
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
                    dblogger.warning(
                        "Lost data for Person %s without NISS: %s",
                        partner_ptr_id, lost)
                    p = contacts_Person.objects.get(pk=partner_ptr_id)
                    if p.remarks:
                        p.remarks += '\n'
                    p.remarks += u'''Datenmigration 20121024: Person hatte weder NISS noch Gesdos-Nr und wurde deshalb kein Klient. Folgende Angaben gingen dabei verloren : ''' + \
                        repr(lost)
                    p.save()
        globals_dict.update(create_contacts_person=create_contacts_person)

        from django.contrib.contenttypes.models import ContentType

        def new_content_type_id(m):
            if m is None:
                return m
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
            if not state:
                state = cal.EntryStates.new
            return cal_Event(id=id, owner_type_id=owner_type_id, owner_id=owner_id, user_id=user_id, created=created, modified=modified, project_id=project_id, build_time=build_time, start_date=start_date, start_time=start_time, end_date=end_date, end_time=end_time, uid=uid, summary=summary, description=description, calendar_id=calendar_id, access_class=access_class, sequence=sequence, auto_type=auto_type, transparent=transparent, place_id=place_id, priority_id=priority_id, state=state)
        globals_dict.update(create_cal_event=create_cal_event)

        def create_cal_task(id, owner_type_id, owner_id, user_id, created, modified, project_id, start_date, start_time, uid, summary, description, calendar_id, access_class, sequence, auto_type, due_date, due_time, percent, state):
            owner_type_id = new_content_type_id(owner_type_id)
            if not state:
                state = cal.TaskStates.todo
            return cal_Task(id=id, owner_type_id=owner_type_id, owner_id=owner_id, user_id=user_id, created=created, modified=modified, project_id=project_id, start_date=start_date, start_time=start_time, uid=uid, summary=summary, description=description, calendar_id=calendar_id, access_class=access_class, sequence=sequence, auto_type=auto_type, due_date=due_date, due_time=due_time, percent=percent, state=state)
        globals_dict.update(create_cal_task=create_cal_task)

        def create_lino_helptext(id, content_type_id, field, help_text):
            content_type_id = new_content_type_id(content_type_id)
            return lino_HelpText(id=id, content_type_id=content_type_id, field=field, help_text=help_text)
        globals_dict.update(create_lino_helptext=create_lino_helptext)

        def create_outbox_attachment(id, owner_type_id, owner_id, mail_id):
            owner_type_id = new_content_type_id(owner_type_id)
            return outbox_Attachment(id=id, owner_type_id=owner_type_id, owner_id=owner_id, mail_id=mail_id)
        globals_dict.update(create_outbox_attachment=create_outbox_attachment)

        def create_outbox_mail(id, owner_type_id, owner_id, user_id, project_id, date, subject, body, sent):
            owner_type_id = new_content_type_id(owner_type_id)
            return outbox_Mail(id=id, owner_type_id=owner_type_id, owner_id=owner_id, user_id=user_id, project_id=project_id, date=date, subject=subject, body=body, sent=sent)
        globals_dict.update(create_outbox_mail=create_outbox_mail)

        def create_postings_posting(id, owner_type_id, owner_id, user_id, project_id, partner_id, state, date):
            owner_type_id = new_content_type_id(owner_type_id)
            if not state:
                state = postings.PostingStates.open
            return postings_Posting(id=id, owner_type_id=owner_type_id, owner_id=owner_id, user_id=user_id, project_id=project_id, partner_id=partner_id, state=state, date=date)
        globals_dict.update(create_postings_posting=create_postings_posting)

        def create_uploads_upload(id, owner_type_id, owner_id, user_id, created, modified, file, mimetype, type_id, valid_until, description):
            owner_type_id = new_content_type_id(owner_type_id)
            return uploads_Upload(id=id, owner_type_id=owner_type_id, owner_id=owner_id, user_id=user_id, created=created, modified=modified, file=file, mimetype=mimetype, type_id=type_id, valid_until=valid_until, description=description)
        globals_dict.update(create_uploads_upload=create_uploads_upload)

        def add_contact_fields(obj, contact_id):
            def fn():
                contact = find_contact(contact_id)
                obj.contact_person = contact.person
                obj.contact_role = contact.type
            return fn

        def create_isip_contract(id, user_id, build_time, person_id, company_id, contact_id, language, applies_from, applies_until, date_decided, date_issued, user_asd_id, exam_policy_id, ending_id, date_ended, type_id, stages, goals, duties_asd, duties_dsbe, duties_company, duties_person):
            #~ contact = find_contact(contact_id)
            obj = isip_Contract(id=id, user_id=user_id, build_time=build_time,
                                client_id=person_id,
                                company_id=company_id,
                                #~ contact_person=contact.person,
                                #~ contact_role=contact.type,
                                #~ contact_id=contact_id,
                                language=language, applies_from=applies_from, applies_until=applies_until, date_decided=date_decided, date_issued=date_issued, user_asd_id=user_asd_id, exam_policy_id=exam_policy_id, ending_id=ending_id, date_ended=date_ended, type_id=type_id, stages=stages, goals=goals, duties_asd=duties_asd, duties_dsbe=duties_dsbe, duties_company=duties_company, duties_person=duties_person)
            obj._before_dumpy_save = add_contact_fields(obj, contact_id)
            return obj

        globals_dict.update(create_isip_contract=create_isip_contract)

        def create_jobs_contract(id, user_id, build_time, person_id, company_id, contact_id, language, applies_from, applies_until, date_decided, date_issued, user_asd_id, exam_policy_id, ending_id, date_ended, type_id, job_id, duration, regime_id, schedule_id, hourly_rate, refund_rate, reference_person, responsibilities, remark):
            if hourly_rate is not None:
                hourly_rate = Decimal(hourly_rate)
            obj = jobs_Contract(id=id, user_id=user_id, build_time=build_time,
                                client_id=person_id,
                                company_id=company_id,
                                language=language, applies_from=applies_from, applies_until=applies_until, date_decided=date_decided, date_issued=date_issued, user_asd_id=user_asd_id, exam_policy_id=exam_policy_id, ending_id=ending_id, date_ended=date_ended, type_id=type_id, job_id=job_id, duration=duration, regime_id=regime_id, schedule_id=schedule_id, hourly_rate=hourly_rate, refund_rate=refund_rate, reference_person=reference_person, responsibilities=responsibilities, remark=remark)
            obj._before_dumpy_save = add_contact_fields(obj, contact_id)
            return obj
        globals_dict.update(create_jobs_contract=create_jobs_contract)

        def create_properties_proptype(id, name, choicelist, default_value, limit_to_choices, multiple_choices, name_fr, name_en):
            if choicelist == 'HowWell':
                choicelist = 'properties.HowWell'
            elif choicelist == 'Gender':
                choicelist = 'contacts.Gender'
            return properties_PropType(id=id, name=name, choicelist=choicelist, default_value=default_value, limit_to_choices=limit_to_choices, multiple_choices=multiple_choices, name_fr=name_fr, name_en=name_en)
        globals_dict.update(create_properties_proptype=create_properties_proptype)

        def create_isip_exampolicy(id, name, project_id, start_date, start_time, end_date, end_time, uid, summary, description, every, every_unit, calendar_id, name_fr, name_en):
            return isip_ExamPolicy(id=id, name=name, start_date=start_date, start_time=start_time, end_date=end_date, end_time=end_time, summary=summary, description=description, every=every, every_unit=every_unit, calendar_id=calendar_id, name_fr=name_fr, name_en=name_en)
        globals_dict.update(create_isip_exampolicy=create_isip_exampolicy)

        objects = globals_dict['objects']

        def new_objects():
            yield users_User(username="watch_tim", modified=NOW, created=NOW)
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


    def migrate_from_1_0(self, globals_dict):
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


    def migrate_from_1_0_1(self, globals_dict):
        """
        - New field `countries.Country.nationalities`
        """
        return '1.0.2'


    def migrate_from_1_0_2(self, globals_dict):
        """
        - Removed field `countries.Country.nationalities`
        """

        countries_Country = resolve_model("countries.Country")

        def create_countries_country(name, isocode, short_code, iso3, name_fr, name_en, nationalities, inscode):
            return countries_Country(
                name=name, isocode=isocode, short_code=short_code, iso3=iso3,
                name_fr=name_fr, name_en=name_en,
                #~ nationalities=nationalities,
                inscode=inscode)
        globals_dict.update(create_countries_country=create_countries_country)

        return '1.0.3'


    def migrate_from_1_0_3(self, globals_dict):
        return '1.0.4'


    def migrate_from_1_0_4(self, globals_dict):
        properties_PropType = resolve_model("properties.PropType")

        def create_properties_proptype(id, name, choicelist, default_value, limit_to_choices, multiple_choices, name_fr, name_en):
            if choicelist == 'contacts.Gender':
                choicelist = 'lino.Genders'
            return properties_PropType(id=id, name=name, choicelist=choicelist, default_value=default_value, limit_to_choices=limit_to_choices, multiple_choices=multiple_choices, name_fr=name_fr, name_en=name_en)
        globals_dict.update(create_properties_proptype=create_properties_proptype)

        def noop(*args):
            return None
        globals_dict.update(create_pcsw_personsearch=noop)
        globals_dict.update(create_pcsw_wantedlanguageknowledge=noop)
        globals_dict.update(create_properties_unwantedskill=noop)
        globals_dict.update(create_properties_wantedskill=noop)

        return '1.0.5'


    def migrate_from_1_0_5(self, globals_dict):
        cal_Event = resolve_model("cal.Event")
        new_content_type_id = globals_dict.get('new_content_type_id')

        def create_cal_event(id, owner_type_id, owner_id, user_id, created, modified, project_id, build_time, start_date, start_time, end_date, end_time, summary, description, uid, calendar_id, access_class, sequence, auto_type, transparent, place_id, priority_id, state):
            owner_type_id = new_content_type_id(owner_type_id)
            #~ if state and state.value == '15':
            if state == '15':
                state = '10'
            return cal_Event(id=id, owner_type_id=owner_type_id, owner_id=owner_id, user_id=user_id, created=created, modified=modified, project_id=project_id, build_time=build_time, start_date=start_date, start_time=start_time, end_date=end_date, end_time=end_time, summary=summary, description=description, uid=uid, calendar_id=calendar_id, access_class=access_class, sequence=sequence, auto_type=auto_type, transparent=transparent, place_id=place_id, priority_id=priority_id, state=state)
        globals_dict.update(create_cal_event=create_cal_event)
        return '1.0.6'


    def migrate_from_1_0_6(self, globals_dict):
        return '1.0.7'


    def migrate_from_1_0_7(self, globals_dict):
        return '1.0.8'


    def migrate_from_1_0_8(self, globals_dict):
        return '1.0.9'


    def migrate_from_1_0_9(self, globals_dict):
        """
        lino.Change -> changes.Change
        """
        lino_Change = resolve_model("changes.Change")
        new_content_type_id = globals_dict.get('new_content_type_id')

        def create_lino_change(id, time, type, user_id, object_type_id, object_id, master_type_id, master_id, diff):
            object_type_id = new_content_type_id(object_type_id)
            master_type_id = new_content_type_id(master_type_id)
            return lino_Change(id=id, time=time, type=type, user_id=user_id, object_type_id=object_type_id, object_id=object_id, master_type_id=master_type_id, master_id=master_id, diff=diff)
        globals_dict.update(create_lino_change=create_lino_change)
        return '1.0.10'


    def migrate_from_1_0_10(self, globals_dict):
        """
        - Change ClientStates.invalid to ClientStates.coached
        """
        create_child = globals_dict.get('create_child')
        contacts_Person = globals_dict.get('contacts_Person')
        pcsw_Client = globals_dict.get('pcsw_Client')

        def create_pcsw_client(person_ptr_id, remarks2, gesdos_id, is_cpas, is_senior, group_id, birth_place, birth_country_id, civil_state, national_id, health_insurance_id, pharmacy_id, nationality_id, card_number, card_valid_from, card_valid_until, card_type, card_issuer, noble_condition, residence_type, in_belgium_since, unemployed_since, needs_residence_permit, needs_work_permit, work_permit_suspended_until, aid_type_id, income_ag, income_wg, income_kg, income_rente, income_misc, is_seeking, unavailable_until, unavailable_why, obstacles, skills, job_agents, job_office_contact_id, client_state, refusal_reason, broker_id, faculty_id):
            if client_state == '60':
                client_state = '30'
            return create_child(contacts_Person, person_ptr_id, pcsw_Client, remarks2=remarks2, gesdos_id=gesdos_id, is_cpas=is_cpas, is_senior=is_senior, group_id=group_id, birth_place=birth_place, birth_country_id=birth_country_id, civil_state=civil_state, national_id=national_id, health_insurance_id=health_insurance_id, pharmacy_id=pharmacy_id, nationality_id=nationality_id, card_number=card_number, card_valid_from=card_valid_from, card_valid_until=card_valid_until, card_type=card_type, card_issuer=card_issuer, noble_condition=noble_condition, residence_type=residence_type, in_belgium_since=in_belgium_since, unemployed_since=unemployed_since, needs_residence_permit=needs_residence_permit, needs_work_permit=needs_work_permit, work_permit_suspended_until=work_permit_suspended_until, aid_type_id=aid_type_id, income_ag=income_ag, income_wg=income_wg, income_kg=income_kg, income_rente=income_rente, income_misc=income_misc, is_seeking=is_seeking, unavailable_until=unavailable_until, unavailable_why=unavailable_why, obstacles=obstacles, skills=skills, job_agents=job_agents, job_office_contact_id=job_office_contact_id, client_state=client_state, refusal_reason=refusal_reason, broker_id=broker_id, faculty_id=faculty_id)
        globals_dict.update(create_pcsw_client=create_pcsw_client)
        return '1.0.11'


    def migrate_from_1_0_11(self, globals_dict):
        """
        - The app_label of TextFieldTemplate, SiteConfig and HelpText is no longer "lino" but "ui"
        """
        globals_dict.update(
            lino_TextFieldTemplate=resolve_model("ui.TextFieldTemplate"))
        globals_dict.update(lino_SiteConfig=resolve_model("ui.SiteConfig"))
        globals_dict.update(lino_HelpText=resolve_model("ui.HelpText"))
        return '1.0.12'


    def migrate_from_1_0_12(self, globals_dict):
        return '1.0.13'


    def migrate_from_1_0_13(self, globals_dict):
        return '1.0.14'


    def migrate_from_1_0_14(self, globals_dict):
        return '1.0.15'


    def migrate_from_1_0_15(self, globals_dict):
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


    def migrate_from_1_0_16(self, globals_dict):
        return '1.0.17'  # was never used in production


    def migrate_from_1_0_17(self, globals_dict):
        """
        Replaced field `active` by `state` in :ref:`welfare.jobs.Candidature`.
        """
        jobs_Candidature = resolve_model("jobs.Candidature")
        CandidatureStates = settings.SITE.models.jobs.CandidatureStates

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


    def migrate_from_1_1_0(self, globals_dict):
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
            if name is not None:
                kw.update(bv2kw('name', name))
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

        def noop(*args):
            return None
        globals_dict.update(create_cal_membership=noop)

        pcsw_CoachingType = resolve_model('pcsw.CoachingType')
        users_Team = resolve_model("auth.Team")

        def after_load(loader):
            for o in pcsw_CoachingType.objects.all():
                kw = dict()
                for n in 'id name name_fr'.split():
                    kw[n] = getattr(o, n)
                users_Team(**kw).save()
        # globals_dict.update(after_load=after_load)
        self.after_load(after_load)
        return '1.1.1'


    def migrate_from_1_1_1(self, globals_dict):
        return '1.1.2'


    def migrate_from_1_1_2(self, globals_dict):
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
            if dist_amount is not None:
                dist_amount = Decimal(dist_amount)
            kw.update(dist_amount=dist_amount)
            return debts_Budget(**kw)
        globals_dict.update(create_debts_budget=create_debts_budget)
        return '1.1.3'


    def migrate_from_1_1_3(self, globals_dict):
        """
        - New field ui.SiteConfig.debts_master_budget
        """
        return '1.1.4'


    def migrate_from_1_1_4(self, globals_dict):
        """
        - jobs.StudyType --> isip.StudyType
        """

        jobs_StudyType = resolve_model('isip.StudyType')
        bv2kw = globals_dict.get('bv2kw')

        def create_jobs_studytype(id, name):
            kw = dict()
            kw.update(id=id)
            if name is not None:
                kw.update(bv2kw('name', name))
            return jobs_StudyType(**kw)
        globals_dict.update(create_jobs_studytype=create_jobs_studytype)

        return '1.1.5'


    def migrate_from_1_1_5(self, globals_dict):
        return '1.1.6'


    def migrate_from_1_1_6(self, globals_dict):
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
            if name is not None:
                kw.update(bv2kw('name', name))
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

    def migrate_from_1_1_7(self, globals_dict):
        """
        - in isip.ExamPolicy, renamed field `max_occurences` to `max_events`
        - cal.EntryStates : "notified" becomes "draft", "absent" becomes "cancelled"
        - renamed app "ui" to "system"
        - in `cal.Room` removed fields `company` and `company_contact`
        """
        bv2kw = globals_dict['bv2kw']
        new_content_type_id = globals_dict['new_content_type_id']

        isip_ExamPolicy = resolve_model('isip.ExamPolicy')

        def create_isip_exampolicy(id, name, start_date, start_time, end_date, end_time, every, every_unit, monday, tuesday, wednesday, thursday, friday, saturday, sunday, max_occurences, calendar_id):
            kw = dict()
            kw.update(id=id)
            if name is not None:
                kw.update(bv2kw('name', name))
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

        from lino_xl.lib.cal.models import EntryStates
        old2new = {
            '30': EntryStates.draft.value,
            '80': EntryStates.cancelled.value,
        }
        cal_Event = resolve_model("cal.Event")

        def create_cal_event(id, owner_type_id, owner_id, user_id, created, modified, project_id, build_time, start_date, start_time, end_date, end_time, summary, description, uid, calendar_id, access_class, sequence, auto_type, transparent, room_id, priority_id, state, assigned_to_id):

            state = old2new.get(state, state)

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
        globals_dict.update(
            ui_TextFieldTemplate=resolve_model('system.TextFieldTemplate'))
        globals_dict.update(ui_HelpText=resolve_model('system.HelpText'))

        cal_Room = resolve_model("cal.Room")

        def create_cal_room(id, name, company_id, contact_person_id, contact_role_id):
            kw = dict()
            kw.update(id=id)
            if name is not None:
                kw.update(bv2kw('name', name))
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


    def migrate_from_1_1_8(self, globals_dict):
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
            kwargs.update(client_calendar_id=kwargs.pop('client_calender_id'))
            return orig_system_SiteConfig(**kwargs)
        globals_dict.update(system_SiteConfig=system_SiteConfig)

        def create_postings_posting(*args):
            return None
        globals_dict.update(create_postings_posting=create_postings_posting)

        from lino_xl.lib.cal.models import EntryStates
        old2new = {
            '60': EntryStates.cancelled.value,
            '30': EntryStates.took_place.value,
        }
        cal_Event = resolve_model("cal.Event")
        new_content_type_id = globals_dict.get('new_content_type_id')

        def create_cal_event(id, owner_type_id, owner_id, user_id, created, modified, project_id, build_time, start_date, start_time, end_date, end_time, summary, description, uid, calendar_id, access_class, sequence, auto_type, transparent, room_id, priority_id, state, assigned_to_id):
            state = old2new.get(state, state)  # changed
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



    def migrate_from_1_1_10(self, globals_dict):
        """

        - Renamed `cal.Calendar` to `cal.EventType`.
          For each "Calendar" of the old version we create an "EventType".
          After migration we will manually create one "Calendar"
          (new version's meaning) for each user.
        - Rename field `calendar` to `event_type` in
          users.User, cal.Subscription and `cal.Event`.
          Removed it in cal.Task.
        - Removed field `uid` in cal.Event and cal.Task
        - Renamed SiteConfig default_calendar to default_event_type
        - Removed field `help_text` in `accounts.Group` and `accounts.Account`
        - Renamed `countries.City` to `countries.Place`
        - Convert existing CVs from `notes.Note` to `excerpts.Excerpt`

        - Removed field SiteConfig attestation_note_nature_id and
          debts_bailiff_type_id

        - after_load: create default excerpt types, create one
          calendar per user, convert existing cv notes to excerpts

        """
 
        bv2kw = globals_dict['bv2kw']
        new_content_type_id = globals_dict['new_content_type_id']

        cal_EventType = resolve_model("cal.EventType")

        def create_cal_calendar(id, name, seqno, build_method, template, attach_to_email, email_template, type, description, url_template, username, password, readonly, is_appointment, start_date, color, event_label, invite_team_members_id, invite_client):
            kw = dict()
            kw.update(id=id)
            if name is not None:
                kw.update(bv2kw('name', name))
            kw.update(seqno=seqno)
            #kw.update(build_method=build_method)
            #kw.update(template=template)
            kw.update(attach_to_email=attach_to_email)
            kw.update(email_template=email_template)
            #~ kw.update(type=type)
            #~ kw.update(description=description)
            #~ kw.update(url_template=url_template)
            #~ kw.update(username=username)
            #~ kw.update(password=password)
            #~ kw.update(readonly=readonly)
            kw.update(is_appointment=is_appointment)
            kw.update(start_date=start_date)
            #~ kw.update(color=color)
            if event_label is not None:
                kw.update(bv2kw('event_label', event_label))
            # kw.update(invite_team_members_id=invite_team_members_id)
            kw.update(invite_client=invite_client)
            return cal_EventType(**kw)
        globals_dict.update(create_cal_calendar=create_cal_calendar)

        users_User = resolve_model("users.User")

        def create_users_user(id, created, modified, username, password, profile, initials, first_name, last_name, email, remarks, language, partner_id, access_class, calendar_id, coaching_type_id, coaching_supervisor, newcomer_quota):
            kw = dict()
            kw.update(id=id)
            kw.update(created=created)
            kw.update(modified=modified)
            kw.update(username=username)
            kw.update(password=password)
            kw.update(profile=profile)
            kw.update(initials=initials)
            kw.update(first_name=first_name)
            kw.update(last_name=last_name)
            kw.update(email=email)
            kw.update(remarks=remarks)
            kw.update(language=language)
            kw.update(partner_id=partner_id)
            kw.update(access_class=access_class)
            #~ kw.update(calendar_id=calendar_id)
            kw.update(coaching_type_id=coaching_type_id)
            kw.update(coaching_supervisor=coaching_supervisor)
            kw.update(newcomer_quota=newcomer_quota)
            return users_User(**kw)
        globals_dict.update(create_users_user=create_users_user)

        #~ cal_Subscription = resolve_model("cal.Subscription")
        #~ def create_cal_subscription(id, user_id, calendar_id, is_hidden):
            #~ kw = dict()
            #~ kw.update(id=id)
            #~ kw.update(user_id=user_id)
            #~ kw.update(event_type_id=calendar_id)
            #~ kw.update(is_hidden=is_hidden)
            #~ return cal_Subscription(**kw)
        #~ globals_dict.update(create_cal_subscription=create_cal_subscription)
    #~

        cal_Event = resolve_model("cal.Event")

        def create_cal_event(id, owner_type_id, owner_id, user_id, created, modified, project_id, build_time, start_date, start_time, end_date, end_time, summary, description, uid, calendar_id, access_class, sequence, auto_type, transparent, room_id, priority_id, state, assigned_to_id):
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
            #~ kw.update(uid=uid)
            kw.update(event_type_id=calendar_id)
            #~ kw.update(calendar_id=calendar_id)
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

        cal_Task = resolve_model("cal.Task")

        def create_cal_task(id, owner_type_id, owner_id, user_id, created, modified, project_id, start_date, start_time, summary, description, uid, calendar_id, access_class, sequence, auto_type, due_date, due_time, percent, state):
            kw = dict()
            kw.update(id=id)
            owner_type_id = new_content_type_id(owner_type_id)
            kw.update(owner_type_id=owner_type_id)
            kw.update(owner_id=owner_id)
            kw.update(user_id=user_id)
            kw.update(created=created)
            kw.update(modified=modified)
            kw.update(project_id=project_id)
            kw.update(start_date=start_date)
            kw.update(start_time=start_time)
            kw.update(summary=summary)
            kw.update(description=description)
            #~ kw.update(uid=uid)
            #~ kw.update(calendar_id=calendar_id)
            kw.update(access_class=access_class)
            kw.update(sequence=sequence)
            kw.update(auto_type=auto_type)
            kw.update(due_date=due_date)
            kw.update(due_time=due_time)
            kw.update(percent=percent)
            kw.update(state=state)
            return cal_Task(**kw)
        globals_dict.update(create_cal_task=create_cal_task)

        isip_ExamPolicy = resolve_model("isip.ExamPolicy")

        def create_isip_exampolicy(id, name, start_date, start_time, end_date, end_time, every_unit, every, monday, tuesday, wednesday, thursday, friday, saturday, sunday, max_events, calendar_id):
            kw = dict()
            kw.update(id=id)
            if name is not None:
                kw.update(bv2kw('name', name))
            kw.update(start_date=start_date)
            kw.update(start_time=start_time)
            kw.update(end_date=end_date)
            kw.update(end_time=end_time)
            kw.update(every_unit=every_unit)
            kw.update(every=every)
            # kw.update(monday=monday)
            # kw.update(tuesday=tuesday)
            # kw.update(wednesday=wednesday)
            # kw.update(thursday=thursday)
            # kw.update(friday=friday)
            for wd in WORKDAYS:
                kw[wd.name] = True
            # kw.update(saturday=saturday)
            # kw.update(sunday=sunday)
            kw.update(max_events=max_events)
            kw.update(event_type_id=calendar_id)
            #~ kw.update(calendar_id=calendar_id)
            return isip_ExamPolicy(**kw)
        globals_dict.update(create_isip_exampolicy=create_isip_exampolicy)

        accounts_Account = resolve_model("accounts.Account")
        accounts_Group = resolve_model("accounts.Group")

        def create_accounts_group(id, name, chart_id, ref, account_type, help_text):
            kw = dict()
            kw.update(id=id)
            if name is not None: kw.update(bv2kw('name',name))
            kw.update(chart_id=chart_id)
            kw.update(ref=ref)
            kw.update(account_type=account_type)
            # kw.update(help_text=help_text)
            assert not help_text
            return accounts_Group(**kw)

        def create_accounts_account(id, name, seqno, chart_id, group_id, ref, type, help_text, required_for_household, required_for_person, periods, default_amount):
            kw = dict()
            kw.update(id=id)
            if name is not None: kw.update(bv2kw('name',name))
            kw.update(seqno=seqno)
            kw.update(chart_id=chart_id)
            kw.update(group_id=group_id)
            kw.update(ref=ref)
            kw.update(type=type)
            # kw.update(help_text=help_text)
            assert not help_text
            kw.update(required_for_household=required_for_household)
            kw.update(required_for_person=required_for_person)
            if periods is not None:
                periods = Decimal(periods)
            kw.update(periods=periods)
            if default_amount is not None:
                default_amount = Decimal(default_amount)
            kw.update(default_amount=default_amount)
            return accounts_Account(**kw)

        globals_dict.update(create_accounts_group=create_accounts_group)
        globals_dict.update(create_accounts_account=create_accounts_account)

        countries_Place = resolve_model("countries.Place")
        globals_dict.update(countries_City=countries_Place)

        system_SiteConfig = resolve_model('system.SiteConfig')

        def f(**kwargs):
            del kwargs['attestation_note_nature_id']
            del kwargs['debts_bailiff_type_id']
            kwargs.pop('farest_future', None)

            return system_SiteConfig(**kwargs)
        globals_dict.update(system_SiteConfig=f)

        cal_Calendar = resolve_model('cal.Calendar')
        users_User = resolve_model("users.User")
        Note = resolve_model("notes.Note")
        NoteType = resolve_model("notes.NoteType")
        Excerpt = resolve_model("excerpts.Excerpt")
        ExcerptType = resolve_model("excerpts.ExcerptType")
        ContentType = resolve_model("contenttypes.ContentType")
        pcsw_Client = resolve_model("pcsw.Client")

        from lino_welfare.fixtures.std2 import excerpt_types
        from lino_welfare.modlib.aids.fixtures.std import objects \
            as aids_objects
        
        def before_load(loader):
            "Load std fixtures from excerpts and aids."
            loader.save(excerpt_types())
            loader.save(aids_objects())

        self.before_load(before_load)

        def target_name(obj):
            bm = obj.get_build_method()
            if bm is None:
                return None
            return bm.get_target(None, obj).name

        def after_load(loader):
            "Convert CVs and write migrate_from_1_1_10.py script."
            fname = os.path.join(
                settings.SITE.project_dir, 'migrate_from_1_1_10.py')
            fd = file(fname, 'w')
            fd.write("""\
#!/usr/bin/env python
import os
import shutil

def doit(a, b):
    if a and b:
        # shutil.copyfile(a, b)
        os.rename(a, b)
        # os.remove(a)
""")
            # Create a Calendar for each (active) user.
            for u in users_User.objects.exclude(profile=''):
                cal = cal_Calendar(name=u.username)
                loader.save(cal)
                u.calendar = cal
                loader.save(u)

            # We need to transfer the '.rtf' files of existing CVs
            # because users have manually edited these files.

            cvnt = NoteType.objects.get(template='cv.odt')
            cvat = ExcerptType.objects.get(template='cv.odt')

            ct = ContentType.objects.get_for_model(pcsw_Client)
            for note in Note.objects.filter(type=cvnt):
                kw = dict()
                # owner_type_id = new_content_type_id(note.owner_type_id)
                if note.project_id is not None:
                    kw.update(owner_id=note.project_id)
                    kw.update(owner_type=ct)
                # kw.update(owner_id=note.owner_id)
                kw.update(user_id=note.user_id)
                kw.update(project_id=note.project_id)
                kw.update(build_time=note.build_time)
                kw.update(company_id=note.company_id)
                kw.update(build_method=note.build_method)
                kw.update(contact_person_id=note.contact_person_id)
                kw.update(contact_role_id=note.contact_role_id)
                # kw.update(date=date)
                kw.update(excerpt_type=cvat)
                # assert note.event_type_id == 
                # assert not note.subject
                # kw.update(body=body)
                kw.update(language=note.language)
                att = Excerpt(**kw)
                att.full_clean()
                att.save()

                if note.build_time:
                    fd.write("doit(%r, %r)\n" % (
                        target_name(note), target_name(att)))

                note.delete()

            fd.close()
            logger.info("Wrote after_migrate script %s", fname)

        self.after_load(after_load)

        return '1.1.11'

    def migrate_from_1_1_11(self, globals_dict):
        """
        - aids.AidType: removed field "remark"
        - aids.Aid: renamed fields
          "project" to "client"
          "type" to "aid_type"
        - excerpts.Excerpt.type : renamed to excerpt_type

        Note: this method is overridden by
        :mod:`lino_welfare.settings.chatelet`.

        """
    
        # humanlinks_Link = resolve_model("humanlinks.Link")
    
        # def create_humanlinks_link(id, seqno, type,
        #                            parent_id, child_id):
        #     kw = dict()
        #     kw.update(id=id)
        #     # kw.update(seqno=seqno)
        #     kw.update(type=type)
        #     kw.update(parent_id=parent_id)
        #     kw.update(child_id=child_id)
        #     return humanlinks_Link(**kw)
        # globals_dict.update(create_humanlinks_link=create_humanlinks_link)
    
        bv2kw = globals_dict['bv2kw']
        new_content_type_id = globals_dict.get('new_content_type_id')
        uploads_Upload = resolve_model("uploads.Upload")
    
        def create_uploads_upload(
                id, owner_type_id, owner_id, user_id, modified,
                created, file, mimetype, type_id, valid_until,
                description):
            kw = dict()
            kw.update(id=id)
            owner_type_id = new_content_type_id(owner_type_id)
            kw.update(owner_type_id=owner_type_id)
            kw.update(owner_id=owner_id)
            kw.update(user_id=user_id)
            # kw.update(modified=modified)
            # kw.update(created=created)
            kw.update(file=file)
            kw.update(mimetype=mimetype)
            kw.update(type_id=type_id)
            kw.update(valid_until=valid_until)
            kw.update(description=description)
            return uploads_Upload(**kw)
        globals_dict.update(create_uploads_upload=create_uploads_upload)
    
        aids_AidType = resolve_model('aids.AidType')
        bv2kw = globals_dict.get('bv2kw')

        notes_NoteType = resolve_model("notes.NoteType")

        def create_notes_notetype(id, name, build_method, template, attach_to_email, email_template, important, remark, body_template):
            kw = dict()
            kw.update(id=id)
            if name is not None: kw.update(bv2kw('name', name))
            kw.update(build_method=build_method)
            kw.update(template=template)
            kw.update(attach_to_email=attach_to_email)
            kw.update(email_template=email_template)
            kw.update(important=important)
            kw.update(remark=remark)
            # kw.update(body_template=body_template)
            # kw.update(is_attestation=is_attestation)
            return notes_NoteType(**kw)
        globals_dict.update(create_notes_notetype=create_notes_notetype)

        def create_aids_aidtype(id, name, foo, build_method, template, remark):
            kw = dict()
            kw.update(id=id)
            if name is not None: kw.update(bv2kw('name',name))
            # kw.update(build_method=build_method)
            # kw.update(template=template)
            # kw.update(remark=remark)
            return aids_AidType(**kw)
        globals_dict.update(create_aids_aidtype=create_aids_aidtype)

        aids_Aid = resolve_model('aids.Aid')
        def create_aids_aid(id, client_id, aid_regime, aid_type_id, decided_date, decider_id, applies_from, applies_until, category_id, amount):
            kw = dict()
            kw.update(id=id)
            kw.update(client_id=client_id)
            kw.update(decided_date=decided_date)
            kw.update(decider_id=decider_id)
            kw.update(applies_from=applies_from)
            kw.update(applies_until=applies_until)
            kw.update(aid_type_id=aid_type_id)
            kw.update(category_id=category_id)
            kw.update(aid_regime=aid_regime)
            if amount is not None: amount = Decimal(amount)
            kw.update(amount=amount)
            return aids_Aid(**kw)
        globals_dict.update(create_aids_aid=create_aids_aid)

        cal_EventType = resolve_model('cal.EventType')
        def create_cal_eventtype(id, name, seqno, build_method, template, attach_to_email, email_template, description, is_appointment, all_rooms, locks_user, start_date, event_label, invite_client):
            kw = dict()
            kw.update(id=id)
            if name is not None: kw.update(bv2kw('name',name))
            kw.update(seqno=seqno)
            # kw.update(build_method=build_method)
            # kw.update(template=template)
            kw.update(attach_to_email=attach_to_email)
            kw.update(email_template=email_template)
            kw.update(description=description)
            kw.update(is_appointment=is_appointment)
            kw.update(all_rooms=all_rooms)
            kw.update(locks_user=locks_user)
            kw.update(start_date=start_date)
            if event_label is not None: kw.update(bv2kw('event_label',event_label))
            # kw.update(invite_team_members_id=invite_team_members_id)
            kw.update(invite_client=invite_client)
            return cal_EventType(**kw)
        globals_dict.update(create_cal_eventtype=create_cal_eventtype)

        excerpts_Excerpt = resolve_model('excerpts.Excerpt')
        def create_attestations_attestation(id, owner_type_id, owner_id, user_id, project_id, build_time, build_method, company_id, contact_person_id, contact_role_id, type_id, language):
            kw = dict()
            kw.update(id=id)
            owner_type_id = new_content_type_id(owner_type_id)
            kw.update(owner_type_id=owner_type_id)
            kw.update(owner_id=owner_id)
            kw.update(user_id=user_id)
            kw.update(project_id=project_id)
            kw.update(build_time=build_time)
            kw.update(build_method=build_method)
            kw.update(company_id=company_id)
            kw.update(contact_person_id=contact_person_id)
            kw.update(contact_role_id=contact_role_id)
            kw.update(excerpt_type_id=type_id)
            kw.update(language=language)
            return excerpts_Excerpt(**kw)
        globals_dict.update(
            create_attestations_attestation=create_attestations_attestation)

        system_TextFieldTemplate = resolve_model('system.TextFieldTemplate')
        
        def create_system_textfieldtemplate(id, user_id, name, description, text):
            kw = dict()
            kw.update(id=id)
            kw.update(user_id=user_id)
            kw.update(name=name)
            kw.update(description=description)
            # kw.update(team_id=team_id)
            kw.update(text=text)
            return system_TextFieldTemplate(**kw)
        globals_dict.update(
            create_system_textfieldtemplate=create_system_textfieldtemplate)

        contacts_Partner = resolve_model('contacts.Partner')
        sepa = dd.resolve_app('sepa')


        def create_contacts_partner(id, created, modified, country_id, city_id, region_id, zip_code, addr1, street_prefix, 
            street, street_no, street_box, addr2, name, language, email, url, phone, gsm, fax, remarks, is_obsolete, activity_id):
            kw = dict()
            kw.update(id=id)
            kw.update(created=created)
            kw.update(modified=modified)
            kw.update(country_id=country_id)
            kw.update(city_id=city_id)
            kw.update(region_id=region_id)
            kw.update(zip_code=zip_code)
            kw.update(name=name)
            kw.update(addr1=addr1)
            kw.update(street_prefix=street_prefix)
            kw.update(street=street)
            kw.update(street_no=street_no)
            kw.update(street_box=street_box)
            kw.update(addr2=addr2)
            kw.update(language=language)
            kw.update(email=email)
            kw.update(url=url)
            kw.update(phone=phone)
            kw.update(gsm=gsm)
            kw.update(fax=fax)
            kw.update(remarks=remarks)
            kw.update(is_obsolete=is_obsolete)
            kw.update(activity_id=activity_id)
            if False:
                kw.update(bank_account1=bank_account1)
                kw.update(bank_account2=bank_account2)
            accs = []
            if dd.is_installed('sepa'):
              primary = True
              for x in (bank_account1, bank_account2):
                x = x.strip()
                if x:
                    a = x.split(':')
                    if len(a) == 2:
                        bic, iban = a
                    else:
                        try:
                            # logger.info(
                            #   "20140415 Compute IBAN/BIC for %s", x)
                            iban, bic = belgian_nban_to_iban_bic(x)
                        except Exception:
                            iban = x
                            bic = ''
                    # some fields contain just ":", ignore these.
                    if iban:
                        accs.append(sepa.Account(
                            partner_id=id, primary=primary,
                            iban=iban, bic=bic))
                        if primary:
                            kw.update(iban=iban, bic=bic)
                            primary = False

            yield contacts_Partner(**kw)
            yield accs

        globals_dict.update(
            create_contacts_partner=create_contacts_partner)

        households_Member = resolve_model('households.Member')

        def create_households_member(id, role_id, household_id, person_id, start_date, end_date):
            kw = dict()
            kw.update(id=id)
            # kw.update(role=role_id)
            kw.update(household_id=household_id)
            kw.update(person_id=person_id)
            kw.update(start_date=start_date)
            kw.update(end_date=end_date)
            return households_Member(**kw)
        globals_dict.update(
            create_households_member=create_households_member)

        globals_dict.update(create_users_team=noop)

        # globals_dict.update(create_households_member=noop)
        globals_dict.update(create_households_role=noop)
        globals_dict.update(create_humanlinks_link=noop)
        globals_dict.update(create_cal_subscription=noop)

        def after_load(loader):
            "create primary address for all Partners"
            for o in settings.SITE.models.contacts.Partner.objects.all():
                o.repairdata()
        self.after_load(after_load)

        cal_GuestRole = resolve_model('cal.GuestRole')

        def create_cal_guestrole(id, name, build_method, template, attach_to_email, email_template):
            kw = dict()
            kw.update(id=id)
            if name is not None: kw.update(bv2kw('name',name))
            # kw.update(build_method=build_method)
            # kw.update(template=template)
            kw.update(attach_to_email=attach_to_email)
            kw.update(email_template=email_template)
            return cal_GuestRole(**kw)
        globals_dict.update(
            create_cal_guestrole=create_cal_guestrole)

        isip_ContractType = resolve_model('isip.ContractType')
        def create_isip_contracttype(id, name, build_method, template, ref, exam_policy_id, needs_study_type):
            kw = dict()
            kw.update(id=id)
            if name is not None: kw.update(bv2kw('name',name))
            # kw.update(build_method=build_method)
            # kw.update(template=template)
            kw.update(ref=ref)
            kw.update(exam_policy_id=exam_policy_id)
            kw.update(needs_study_type=needs_study_type)
            return isip_ContractType(**kw)
        globals_dict.update(
            create_isip_contracttype=create_isip_contracttype)

        jobs_ContractType = resolve_model('jobs.ContractType')
        def create_jobs_contracttype(id, name, build_method, template, ref, exam_policy_id):
            kw = dict()
            kw.update(id=id)
            if name is not None: kw.update(bv2kw('name',name))
            # kw.update(build_method=build_method)
            # kw.update(template=template)
            kw.update(ref=ref)
            kw.update(exam_policy_id=exam_policy_id)
            return jobs_ContractType(**kw)
        globals_dict.update(
            create_jobs_contracttype=create_jobs_contracttype)

        debts_Budget = resolve_model('debts.Budget')
        def create_debts_budget(id, user_id, build_time, date, partner_id, print_todos, print_empty_rows, include_yearly_incomes, intro, conclusion, dist_amount):
            kw = dict()
            kw.update(id=id)
            kw.update(user_id=user_id)
            # kw.update(build_time=build_time)
            kw.update(date=date)
            kw.update(partner_id=partner_id)
            kw.update(print_todos=print_todos)
            kw.update(print_empty_rows=print_empty_rows)
            kw.update(include_yearly_incomes=include_yearly_incomes)
            kw.update(intro=intro)
            kw.update(conclusion=conclusion)
            if dist_amount is not None: dist_amount = Decimal(dist_amount)
            kw.update(dist_amount=dist_amount)
            return debts_Budget(**kw)
        globals_dict.update(
            create_debts_budget=create_debts_budget)

        Excerpt = resolve_model("excerpts.Excerpt")
        ExcerptType = resolve_model("excerpts.ExcerptType")
        ContentType = resolve_model("contenttypes.ContentType")

        isip_Contract = resolve_model('isip.Contract')

        def create_isip_contract(id, user_id, build_time, signer1_id, signer2_id, company_id, contact_person_id, contact_role_id, client_id, language, applies_from, 
                applies_until, date_decided, date_issued, user_asd_id, exam_policy_id, ending_id, date_ended, type_id, stages, goals, duties_asd, duties_dsbe, 
                duties_company, duties_person, study_type_id):
 
            kw = dict()
            kw.update(id=id)
            kw.update(user_id=user_id)
            # kw.update(build_time=build_time)
            kw.update(signer1_id=signer1_id)
            kw.update(signer2_id=signer2_id)
            kw.update(company_id=company_id)
            kw.update(contact_person_id=contact_person_id)
            kw.update(contact_role_id=contact_role_id)
            kw.update(client_id=client_id)
            kw.update(language=language)
            kw.update(applies_from=applies_from)
            kw.update(applies_until=applies_until)
            kw.update(date_decided=date_decided)
            kw.update(date_issued=date_issued)
            kw.update(user_asd_id=user_asd_id)
            kw.update(exam_policy_id=exam_policy_id)
            kw.update(ending_id=ending_id)
            kw.update(date_ended=date_ended)
            kw.update(type_id=type_id)
            kw.update(stages=stages)
            kw.update(goals=goals)
            kw.update(duties_asd=duties_asd)
            kw.update(duties_dsbe=duties_dsbe)
            kw.update(duties_company=duties_company)
            kw.update(duties_person=duties_person)
            kw.update(study_type_id=study_type_id)
            if build_time:
                isip_et = ExcerptType.objects.get(template='vse.odt')
                isip_ot = ContentType.objects.get_for_model(isip_Contract)
                e = Excerpt(
                    build_time=build_time,
                    user_id=user_id,
                    owner_type=isip_ot,
                    owner_id=id,
                    excerpt_type=isip_et)
                yield e
                kw.update(printed_by=e)
            yield isip_Contract(**kw)

        globals_dict.update(
            create_isip_contract=create_isip_contract)

        jobs_Contract = resolve_model('jobs.Contract')

        def create_jobs_contract(id, user_id, build_time, signer1_id, signer2_id, company_id, contact_person_id, 
                contact_role_id, client_id, language, applies_from, applies_until, date_decided, date_issued, user_asd_id, exam_policy_id, ending_id, 
                date_ended, type_id, job_id, duration, regime_id, schedule_id, hourly_rate, refund_rate, reference_person, responsibilities, remark):
            kw = dict()
            kw.update(id=id)
            kw.update(user_id=user_id)
            # kw.update(build_time=build_time)
            kw.update(signer1_id=signer1_id)
            kw.update(signer2_id=signer2_id)
            kw.update(company_id=company_id)
            kw.update(contact_person_id=contact_person_id)
            kw.update(contact_role_id=contact_role_id)
            kw.update(client_id=client_id)
            kw.update(language=language)
            kw.update(applies_from=applies_from)
            kw.update(applies_until=applies_until)
            kw.update(date_decided=date_decided)
            kw.update(date_issued=date_issued)
            kw.update(user_asd_id=user_asd_id)
            kw.update(exam_policy_id=exam_policy_id)
            kw.update(ending_id=ending_id)
            kw.update(date_ended=date_ended)
            kw.update(type_id=type_id)
            kw.update(job_id=job_id)
            kw.update(duration=duration)
            kw.update(regime_id=regime_id)
            kw.update(schedule_id=schedule_id)
            if hourly_rate is not None: hourly_rate = Decimal(hourly_rate)
            kw.update(hourly_rate=hourly_rate)
            kw.update(refund_rate=refund_rate)
            kw.update(reference_person=reference_person)
            kw.update(responsibilities=responsibilities)
            kw.update(remark=remark)
            if build_time:
                jobs_et = ExcerptType.objects.get(template='art60-7.odt')
                jobs_ot = ContentType.objects.get_for_model(jobs_Contract)
                e = Excerpt(
                    build_time=build_time,
                    user_id=user_id,
                    owner_type=jobs_ot,
                    owner_id=id,
                    excerpt_type=jobs_et)
                yield e
                kw.update(printed_by=e)
            yield jobs_Contract(**kw)

        globals_dict.update(
            create_jobs_contract=create_jobs_contract)

        pcsw_CoachingType = resolve_model('pcsw.CoachingType')
        isip = dd.resolve_app('isip')
        
        def create_pcsw_coachingtype(id, name):
            kw = dict()
            kw.update(id=id)
            if id != isip.COACHINGTYPE_ASD:
                kw.update(does_gss=False)
            if id != isip.COACHINGTYPE_DSBE:
                kw.update(does_integ=False)
            if name is not None: kw.update(bv2kw('name', name))
            return pcsw_CoachingType(**kw)
        globals_dict.update(
            create_pcsw_coachingtype=create_pcsw_coachingtype)

        globals_dict.update(
            pcsw_ClientAddress=resolve_model("addresses.Address"))

        system_SiteConfig = resolve_model('system.SiteConfig')

        def f(**kwargs):
            kwargs.pop('farest_future', None)

            return system_SiteConfig(**kwargs)
        globals_dict.update(system_SiteConfig=f)

        return '1.1.12'

    def migrate_from_1_1_12(self, globals_dict):
        """
        - rename `aids.Decider` to `boards.Board`
        """
        globals_dict.update(
            aids_Decider=resolve_model("boards.Board"))

        aids_Aid = resolve_model('aids.Aid')

        def create_aids_aid(
                id, client_id, aid_regime, aid_type_id, decided_date,
                decider_id, applies_from, applies_until, category_id,
                amount):
            kw = dict()
            kw.update(id=id)
            kw.update(client_id=client_id)
            kw.update(aid_regime=aid_regime)
            kw.update(aid_type_id=aid_type_id)
            kw.update(decided_date=decided_date)
            kw.update(board_id=decider_id)
            kw.update(start_date=applies_from)
            kw.update(end_date=applies_until)
            kw.update(category_id=category_id)
            if amount is not None: amount = Decimal(amount)
            kw.update(amount=amount)
            return aids_Aid(**kw)
        globals_dict.update(create_aids_aid=create_aids_aid)
        
        return '1.1.13'


    def migrate_from_1_1_13(self, globals_dict):
        """Move company, contact_person and contact_role from isip.Contract
        to isip.ContractPartner

        """
        isip_Contract = resolve_model("isip.Contract")
        isip_contractpartner = resolve_model("isip.ContractPartner")

        def create_isip_contract(id, user_id, signer1_id, signer2_id, company_id, contact_person_id, contact_role_id, printed_by_id, client_id, language, applies_from, applies_until, date_decided, date_issued, user_asd_id, exam_policy_id, ending_id, date_ended, type_id, stages, goals, duties_asd, duties_dsbe, duties_company, duties_person, study_type_id):
            kw = dict()
            kw.update(id=id)
            kw.update(user_id=user_id)
            kw.update(signer1_id=signer1_id)
            kw.update(signer2_id=signer2_id)
            kw.update(printed_by_id=printed_by_id)
            kw.update(client_id=client_id)
            kw.update(language=language)
            kw.update(applies_from=applies_from)
            kw.update(applies_until=applies_until)
            kw.update(date_decided=date_decided)
            kw.update(date_issued=date_issued)
            kw.update(user_asd_id=user_asd_id)
            kw.update(exam_policy_id=exam_policy_id)
            kw.update(ending_id=ending_id)
            kw.update(date_ended=date_ended)
            kw.update(type_id=type_id)
            kw.update(stages=stages)
            kw.update(goals=goals)
            kw.update(duties_asd=duties_asd)
            kw.update(duties_dsbe=duties_dsbe)
            kw.update(duties_person=duties_person)
            kw.update(study_type_id=study_type_id)
            yield isip_Contract(**kw)
        
            if company_id:
                pkw = dict()
                pkw.update(contract_id=id)
                pkw.update(company_id=company_id)
                pkw.update(contact_person_id=contact_person_id)
                pkw.update(contact_role_id=contact_role_id)
                pkw.update(duties_company=duties_company)
                yield isip_contractpartner(**pkw)

        globals_dict.update(create_isip_contract=create_isip_contract)

        return '1.1.14'

    def migrate_from_1_1_14(self, globals_dict):
        """
        aids.Aid: removed fields `board` and `date_decided`
        """
        aids_Aid = resolve_model("aids.Aid")
        def create_aids_aid(id, start_date, end_date, decided_date, board_id, client_id, aid_regime, aid_type_id, category_id, amount):
            kw = dict()
            kw.update(id=id)
            kw.update(start_date=start_date)
            kw.update(end_date=end_date)
            # kw.update(decided_date=decided_date)
            # kw.update(board_id=board_id)
            kw.update(client_id=client_id)
            kw.update(aid_regime=aid_regime)
            kw.update(aid_type_id=aid_type_id)
            kw.update(category_id=category_id)
            if amount is not None: amount = Decimal(amount)
            kw.update(amount=amount)
            return aids_Aid(**kw)
        globals_dict.update(create_aids_aid=create_aids_aid)

        return '1.1.15'

    def migrate_from_1_1_15(self, globals_dict):
        """aids.Aid renamed to aids.Confirmation."""

        aids_Aid = resolve_model("aids.Confirmation")
        globals_dict.update(aids_Aid=aids_Aid)

        def create_aids_aid(id, start_date, end_date, client_id, aid_regime, aid_type_id, category_id, amount, remark):
            kw = dict()
            kw.update(id=id)
            kw.update(start_date=start_date)
            kw.update(end_date=end_date)
            kw.update(client_id=client_id)
            # kw.update(aid_regime=aid_regime)
            kw.update(aid_type_id=aid_type_id)
            kw.update(category_id=category_id)
            if amount is not None: amount = Decimal(amount)
            kw.update(amount=amount)
            kw.update(remark=remark)
            return aids_Aid(**kw)

        globals_dict.update(create_aids_aid=create_aids_aid)

        return '1.1.16'

    def migrate_from_1_1_16(self, globals_dict):
        """\
- lino_xl.lib.courses.CourseStates : state 40 (Ended) no longer exists
- excerpts.Excerpt: remove fields language, company, contact_person
  and contact_role
- cal.GuestRole is no longer a PrintableType
- Removed the different UploadAreas (medical, jobs...)
        """
        bv2kw = globals_dict['bv2kw']
        new_content_type_id = globals_dict['new_content_type_id']
        cal_GuestRole = resolve_model("cal.GuestRole")
        uploads_UploadType = resolve_model("uploads.UploadType")
        uploads_Upload = resolve_model("uploads.Upload")
        aids_AidType = resolve_model("aids.AidType")

        def create_cal_guestrole(id, name, attach_to_email, email_template):
            kw = dict()
            kw.update(id=id)
            if name is not None: kw.update(bv2kw('name',name))
            # kw.update(attach_to_email=attach_to_email)
            # kw.update(email_template=email_template)
            return cal_GuestRole(**kw)
        globals_dict.update(create_cal_guestrole=create_cal_guestrole)

        def create_uploads_uploadtype(id, name, upload_area, max_number, wanted, warn_expiry_unit, warn_expiry_value):
            kw = dict()
            kw.update(id=id)
            if name is not None: kw.update(bv2kw('name',name))
            # kw.update(upload_area=upload_area)
            kw.update(max_number=max_number)
            kw.update(wanted=wanted)
            kw.update(warn_expiry_unit=warn_expiry_unit)
            kw.update(warn_expiry_value=warn_expiry_value)
            return uploads_UploadType(**kw)
        globals_dict.update(create_uploads_uploadtype=create_uploads_uploadtype)

        def create_uploads_upload(id, owner_type_id, owner_id, user_id, project_id, file, mimetype, company_id, contact_person_id, contact_role_id, upload_area, type_id, description, valid_from, valid_until, remark):
            kw = dict()
            kw.update(id=id)
            owner_type_id = new_content_type_id(owner_type_id)
            kw.update(owner_type_id=owner_type_id)
            kw.update(owner_id=owner_id)
            kw.update(user_id=user_id)
            kw.update(project_id=project_id)
            kw.update(file=file)
            kw.update(mimetype=mimetype)
            kw.update(company_id=company_id)
            kw.update(contact_person_id=contact_person_id)
            kw.update(contact_role_id=contact_role_id)
            # kw.update(upload_area=upload_area)
            kw.update(type_id=type_id)
            kw.update(description=description)
            kw.update(valid_from=valid_from)
            kw.update(valid_until=valid_until)
            kw.update(remark=remark)
            return uploads_Upload(**kw)
        globals_dict.update(create_uploads_upload=create_uploads_upload)

        def create_aids_aidtype(id, name, company_id, contact_person_id, contact_role_id, aid_regime, confirmation_type, long_name, short_name, board_id, print_directly, confirmed_by_primary_coach, pharmacy_type_id):
            kw = dict()
            kw.update(id=id)
            if name is not None: kw.update(bv2kw('name',name))
            kw.update(company_id=company_id)
            kw.update(contact_person_id=contact_person_id)
            kw.update(contact_role_id=contact_role_id)
            kw.update(aid_regime=aid_regime)
            kw.update(confirmation_type=confirmation_type)
            # if long_name is not None: kw.update(bv2kw('long_name',long_name))
            kw.update(short_name=short_name)
            kw.update(board_id=board_id)
            kw.update(print_directly=print_directly)
            kw.update(confirmed_by_primary_coach=confirmed_by_primary_coach)
            kw.update(pharmacy_type_id=pharmacy_type_id)
            return aids_AidType(**kw)
        globals_dict.update(create_aids_aidtype=create_aids_aidtype)

        return '1.1.17'

    def migrate_from_1_1_18(self, globals_dict):
        """
Moved models from jobs to cv: Study, Experience, Regime, Sector, Status.
Moved models from isip to cv: StudyType, EducationLevel.
Renamed field started to start_date and stopped to end_date in: cv.Study, cv.Experience.
Removed field `study_regime` in `Study` and `StudyType`.
New models cv.TrainingType, cv.Training, cv.Duration.
Moved model `system.HelpText` to `contenttypes.HelpText`.
Convert field `Study.success` to `Study.state`.

"""
        from lino_xl.lib.cv.mixins import SchoolingStates

        bv2kw = globals_dict['bv2kw']
        new_content_type_id = globals_dict['new_content_type_id']

        globals_dict.update(isip_Function=resolve_model("cv.Function"))
        globals_dict.update(
            isip_EducationLevel=resolve_model("cv.EducationLevel"))
        globals_dict.update(jobs_Function=resolve_model("cv.Function"))
        globals_dict.update(jobs_Regime=resolve_model("cv.Regime"))
        globals_dict.update(jobs_Status=resolve_model("cv.Status"))
        globals_dict.update(jobs_Sector=resolve_model("cv.Sector"))
        globals_dict.update(
            system_HelpText=resolve_model("contenttypes.HelpText"))

        jobs_Experience = resolve_model("cv.Experience")
        jobs_Study = resolve_model("cv.Study")
        isip_StudyType = resolve_model("cv.StudyType")

        def create_isip_studytype(id, name, study_regime, education_level_id):
            kw = dict()
            kw.update(id=id)
            if name is not None: kw.update(bv2kw('name',name))
            # kw.update(study_regime=study_regime)
            kw.update(education_level_id=education_level_id)
            return isip_StudyType(**kw)
        globals_dict.update(create_isip_studytype=create_isip_studytype)

        def create_jobs_experience(id, sector_id, function_id, person_id, started, stopped, company, title, country_id, status_id, is_training, regime_id, remarks):
            kw = dict()
            kw.update(id=id)
            kw.update(sector_id=sector_id)
            kw.update(function_id=function_id)
            kw.update(person_id=person_id)
            kw.update(start_date=started)
            kw.update(end_date=stopped)
            kw.update(company=company)
            kw.update(title=title)
            kw.update(country_id=country_id)
            kw.update(status_id=status_id)
            kw.update(is_training=is_training)
            kw.update(regime_id=regime_id)
            kw.update(remarks=remarks)
            return jobs_Experience(**kw)
        globals_dict.update(create_jobs_experience=create_jobs_experience)

        def create_jobs_study(id, country_id, city_id, zip_code, person_id, started, stopped, study_regime, type_id, content, success, language_id, school, remarks):
            kw = dict()
            kw.update(id=id)
            kw.update(country_id=country_id)
            kw.update(city_id=city_id)
            kw.update(zip_code=zip_code)
            kw.update(person_id=person_id)
            kw.update(start_date=started)
            kw.update(end_date=stopped)
            # kw.update(study_regime=study_regime)
            kw.update(type_id=type_id)
            kw.update(content=content)
            # kw.update(success=success)
            if success:
                kw.update(state=SchoolingStates.success)
            kw.update(language_id=language_id)
            kw.update(school=school)
            kw.update(remarks=remarks)
            return jobs_Study(**kw)
        globals_dict.update(create_jobs_study=create_jobs_study)

        return '1.1.19'

    def migrate_from_1_1_19(self, globals_dict):
        return '1.1.20'

    def migrate_from_1_1_20(self, globals_dict):
        """In `uploads.Upload`, renamed valid_from to start_date and
valid_until to end_date.

        """
        uploads_Upload = resolve_model("uploads.Upload")
        new_content_type_id = globals_dict['new_content_type_id']

        def create_uploads_upload(id, project_id, file, mimetype, user_id, owner_type_id, owner_id, company_id, contact_person_id, contact_role_id, upload_area, type_id, description, valid_from, valid_until, remark):
            kw = dict()
            kw.update(id=id)
            kw.update(project_id=project_id)
            kw.update(file=file)
            kw.update(mimetype=mimetype)
            kw.update(user_id=user_id)
            owner_type_id = new_content_type_id(owner_type_id)
            kw.update(owner_type_id=owner_type_id)
            kw.update(owner_id=owner_id)
            kw.update(company_id=company_id)
            kw.update(contact_person_id=contact_person_id)
            kw.update(contact_role_id=contact_role_id)
            kw.update(upload_area=upload_area)
            kw.update(type_id=type_id)
            kw.update(description=description)
            kw.update(start_date=valid_from)
            kw.update(end_date=valid_until)
            kw.update(remark=remark)
            return uploads_Upload(**kw)
        globals_dict.update(create_uploads_upload=create_uploads_upload)

        return '1.1.21'

    def migrate_from_1_1_21(self, globals_dict):
        """The account charts model has been replaced by a choicelist.

        """

        from lino_xl.lib.accounts.choicelists import AccountCharts
        bv2kw = globals_dict['bv2kw']

        accounts_Group = rt.models.accounts.Group
        accounts_Account = rt.models.accounts.Account

        def create_accounts_group(id, name, chart_id, ref, account_type, entries_layout):
            kw = dict()
            kw.update(id=id)
            if name is not None: kw.update(bv2kw('name',name))
            # kw.update(chart_id=chart_id)
            kw.update(chart=AccountCharts.debts)
            kw.update(ref=ref)
            kw.update(account_type=account_type)
            kw.update(entries_layout=entries_layout)
            return accounts_Group(**kw)
        globals_dict.update(create_accounts_group=create_accounts_group)

        def create_accounts_account(id, seqno, name, chart_id, group_id, ref, type, required_for_household, required_for_person, periods, default_amount):
            kw = dict()
            kw.update(id=id)
            kw.update(seqno=seqno)
            if name is not None: kw.update(bv2kw('name',name))
            kw.update(chart=AccountCharts.debts)
            # kw.update(chart_id=chart_id)
            kw.update(group_id=group_id)
            kw.update(ref=ref)
            kw.update(type=type)
            kw.update(required_for_household=required_for_household)
            kw.update(required_for_person=required_for_person)
            if periods is not None: periods = Decimal(periods)
            kw.update(periods=periods)
            if default_amount is not None: default_amount = Decimal(default_amount)
            kw.update(default_amount=default_amount)
            return accounts_Account(**kw)
        globals_dict.update(create_accounts_account=create_accounts_account)

        globals_dict.update(create_accounts_chart=noop)

        return '1.1.22'

