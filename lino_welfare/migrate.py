# -*- coding: UTF-8 -*-
# Copyright 2011-2015 Luc Saffre
# This file is part of Lino Welfare.
#
# Lino Welfare is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# Lino Welfare is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License along with Lino Welfare.  If not, see
# <http://www.gnu.org/licenses/>.

"""
This is a real-world example of how the application developer
can provide automatic data migrations for :ref:`dpy`.

This module is used because a :ref:`welfare`
Site has :setting:`migration_class` set to
``"lino_welfare.migrate.Migrator"``.

"""

import logging
logger = logging.getLogger(__name__)


import os
import datetime
from decimal import Decimal
from django.conf import settings
from lino.utils.dpy import Migrator
from lino.core.utils import resolve_model
from lino.api import dd, rt
from lino.modlib.sepa.utils import belgian_nban_to_iban_bic
from lino.modlib.cal.utils import WORKDAYS


SINCE_ALWAYS = datetime.date(1990, 1, 1)

def noop(*args):
    return None

class Migrator(Migrator):
    "The standard migrator for :ref:`welfare`."
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
            for o in settings.SITE.modules.contacts.Partner.objects.all():
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
- lino.modlib.courses.CourseStates : state 40 (Ended) no longer exists
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
        from lino.modlib.cv.mixins import SchoolingStates

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

        from lino.modlib.accounts.choicelists import AccountCharts
        bv2kw = globals_dict['bv2kw']

        accounts_Group = rt.modules.accounts.Group
        accounts_Account = rt.modules.accounts.Account

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

    def migrate_from_1_1_22(self, globals_dict):
        """- contenttypes.HelpText renamed to gfks.HelpText 

- Fields Partner.bic and Partner.iban no longer exist. Check whether
  sepa.Account exists.

        """

        globals_dict.update(contenttypes_HelpText=rt.modules.gfks.HelpText)

        if dd.is_installed('sepa'):
            self.sepa_accounts = []
            contacts_Partner = rt.modules.contacts.Partner

            def create_contacts_partner(id, modified, created, country_id, city_id, zip_code, region_id, addr1, street_prefix, street, street_no, street_box, addr2, name, language, email, url, phone, gsm, fax, remarks, is_obsolete, activity_id, client_contact_type_id, iban, bic):

                kw = dict()
                kw.update(id=id)
                kw.update(modified=modified)
                kw.update(created=created)
                kw.update(country_id=country_id)
                kw.update(city_id=city_id)
                kw.update(zip_code=zip_code)
                kw.update(region_id=region_id)
                kw.update(addr1=addr1)
                kw.update(street_prefix=street_prefix)
                kw.update(street=street)
                kw.update(street_no=street_no)
                kw.update(street_box=street_box)
                kw.update(addr2=addr2)
                kw.update(name=name)
                kw.update(language=language)
                kw.update(email=email)
                kw.update(url=url)
                kw.update(phone=phone)
                kw.update(gsm=gsm)
                kw.update(fax=fax)
                kw.update(remarks=remarks)
                kw.update(is_obsolete=is_obsolete)
                kw.update(activity_id=activity_id)
                kw.update(client_contact_type_id=client_contact_type_id)
                # kw.update(iban=iban)
                # kw.update(bic=bic)
                if iban:
                    self.sepa_accounts.append((id, bic, iban))
                return contacts_Partner(**kw)

            globals_dict.update(create_contacts_partner=create_contacts_partner)

            def check_sepa_accounts(loader):
                Account = rt.modules.sepa.Account
                for pk, bic, iban in self.sepa_accounts:
                    try:
                        Account.objects.get(partner_id=pk, bic=bic, iban=iban)
                    except Account.MultipleObjectsReturned:
                        pass
                    except Account.DoesNotExist:
                        obj = Account(partner_id=pk, bic=bic, iban=iban)
                        obj.full_clean()
                        obj.save()
                        logger.info("20150825 created %s for partner #%s",
                                    obj, pk)
            self.after_load(check_sepa_accounts)
        return '1.1.23'
