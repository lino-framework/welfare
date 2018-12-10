# -*- coding: UTF-8 -*-
# Copyright 2014-2018 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

"""
This migrator overrides the default :ref:`welfare` migrator.
"""

import logging
logger = logging.getLogger(__name__)

from lino_welfare.migrate import *


class Migrator(Migrator):

    def migrate_from_1_1_11(self, globals_dict):
        """Special migration for chatelet 1.1.12.  
        Was used on 20140325 and on 20140407.

        - course providers are companies
        - pupils are clients
        - courses.Line replaces courses.CourseOffer
        - courses.Topic replaces courses.CourseContent

        """
    
        super(Migrator, self).migrate_from_1_1_11(globals_dict)
    
        def noop(*args):
            return None
        globals_dict.update(create_courses_courseprovider=noop)
        globals_dict.update(create_courses_course=noop)
        globals_dict.update(create_courses_courserequest=noop)
    
        # globals_dict.update(create_humanlinks_link=noop)
        # globals_dict.update(create_uploads_upload=noop)

        courses_CourseOffer = resolve_model('courses.Line')
    
        def create_courses_courseoffer(
                id, title, content_id, provider_id, description):
            kw = dict()
            kw.update(id=id)
            kw.update(name=title)
            kw.update(topic_id=content_id)
            # kw.update(provider_id=provider_id)
            kw.update(description=description)
            return courses_CourseOffer(**kw)
        globals_dict.update(
            create_courses_courseoffer=create_courses_courseoffer)

        courses_CourseContent = resolve_model('courses.Topic')
        globals_dict.update(courses_CourseContent=courses_CourseContent)

        globals_dict.update(courses_Teacher=resolve_model('contacts.Person'))
        globals_dict.update(courses_Pupil=resolve_model('pcsw.Client'))

        return '1.1.12'

    def migrate_from_1_1_16(self, globals_dict):
        """
        Migrate `properties` to new `cv` module

        """
    
        super(Migrator, self).migrate_from_1_1_14(globals_dict)

        def noop(*args):
            return None
        globals_dict.update(create_properties_propgroup=noop)
        globals_dict.update(create_properties_proptype=noop)

        system_SiteConfig = resolve_model("system.SiteConfig")
        def create_system_siteconfig(id, default_build_method, signer1_id, signer2_id, signer1_function_id, signer2_function_id, default_event_type_id, site_calendar_id, max_auto_events, client_calendar_id, client_guestrole_id, team_guestrole_id, next_partner_id, site_company_id, prompt_calendar_id, system_note_type_id, propgroup_skills_id, propgroup_softskills_id, propgroup_obstacles_id, job_office_id, residence_permit_upload_type_id, work_permit_upload_type_id, driving_licence_upload_type_id, sector_id, cbss_org_unit, ssdn_user_id, ssdn_email, cbss_http_username, cbss_http_password):
            kw = dict()
            kw.update(id=id)
            kw.update(default_build_method=default_build_method)
            kw.update(signer1_id=signer1_id)
            kw.update(signer2_id=signer2_id)
            kw.update(signer1_function_id=signer1_function_id)
            kw.update(signer2_function_id=signer2_function_id)
            kw.update(default_event_type_id=default_event_type_id)
            kw.update(site_calendar_id=site_calendar_id)
            kw.update(max_auto_events=max_auto_events)
            kw.update(client_calendar_id=client_calendar_id)
            kw.update(client_guestrole_id=client_guestrole_id)
            kw.update(team_guestrole_id=team_guestrole_id)
            kw.update(next_partner_id=next_partner_id)
            kw.update(site_company_id=site_company_id)
            kw.update(prompt_calendar_id=prompt_calendar_id)
            kw.update(system_note_type_id=system_note_type_id)
            # kw.update(propgroup_skills_id=propgroup_skills_id)
            # kw.update(propgroup_softskills_id=propgroup_softskills_id)
            # kw.update(propgroup_obstacles_id=propgroup_obstacles_id)
            kw.update(job_office_id=job_office_id)
            kw.update(residence_permit_upload_type_id=residence_permit_upload_type_id)
            kw.update(work_permit_upload_type_id=work_permit_upload_type_id)
            kw.update(driving_licence_upload_type_id=driving_licence_upload_type_id)
            kw.update(sector_id=sector_id)
            kw.update(cbss_org_unit=cbss_org_unit)
            kw.update(ssdn_user_id=ssdn_user_id)
            kw.update(ssdn_email=ssdn_email)
            kw.update(cbss_http_username=cbss_http_username)
            kw.update(cbss_http_password=cbss_http_password)
            return system_SiteConfig(**kw)
        globals_dict.update(
            create_system_siteconfig=create_system_siteconfig)



        cv_Skill = resolve_model('cv.Skill')
        cv_SoftSkill = resolve_model('cv.SoftSkill')
        cv_Obstacle = resolve_model('cv.Obstacle')
        cv_SoftSkillType = resolve_model('cv.SoftSkillType')
        cv_ObstacleType = resolve_model('cv.ObstacleType')
        bv2kw = globals_dict['bv2kw']

        def create_properties_property(id, name, group_id, type_id):
            kw = dict()
            kw.update(id=id)
            if name is not None: kw.update(bv2kw('name',name))
            if group_id == 1:
                logger.warning("Ignored Skill %s", name)
                return None
            elif group_id == 2:
                return cv_SoftSkillType(**kw)
            elif group_id == 3:
                return cv_ObstacleType(**kw)
            else:
                raise Exception("Invalid group %s for %s" % (group_id, name))
            # kw.update(group_id=group_id)
            # kw.update(type_id=type_id)
            # return properties_Property(**kw)
        globals_dict.update(
            create_properties_property=create_properties_property)

        def create_properties_personproperty(
                id, group_id, property_id, value, person_id, remark):
            kw = dict()
            kw.update(id=id)
            kw.update(person_id=person_id)
            kw.update(remark=remark)
        
            if group_id == 1:
                return cv_Skill(**kw)
            elif group_id == 2:
                t = cv_SoftSkillType.objects.get(pk=property_id)
                kw.update(type=t)
                return cv_SoftSkill(**kw)
            elif group_id == 3:
                t = cv_ObstacleType.objects.get(pk=property_id)
                kw.update(type=t)
                return cv_Obstacle(**kw)
            else:
                raise Exception("Invalid group %s for %s" % (group_id, name))
            # kw.update(group_id=group_id)
            # kw.update(property_id=property_id)
            # kw.update(value=value)
            # return properties_PersonProperty(**kw)
        globals_dict.update(
            create_properties_personproperty=create_properties_personproperty)

        return '1.1.17'

