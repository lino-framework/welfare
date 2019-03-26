# -*- coding: UTF-8 -*-
logger.info("Loading 1 objects to table system_siteconfig...")
# fields: id, default_build_method, simulate_today, site_company, signer1, signer2, signer1_function, signer2_function, next_partner_id, default_event_type, site_calendar, max_auto_events, hide_events_before, client_calendar, client_guestrole, team_guestrole, prompt_calendar, propgroup_skills, propgroup_softskills, propgroup_obstacles, master_budget, system_note_type, job_office, residence_permit_upload_type, work_permit_upload_type, driving_licence_upload_type, sector, cbss_org_unit, ssdn_user_id, ssdn_email, cbss_http_username, cbss_http_password
loader.save(create_system_siteconfig(1,None,None,187,148,163,None,None,274,None,1,72,date(2014,4,1),4,2,None,6,1,2,3,1,10,214,None,None,None,45,u'0123456789',u'00901234567',u'info@example.com',u'E0123456789',u'p1234567890123456789012345678'))

loader.flush_deferred_objects()
