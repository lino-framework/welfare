# -*- coding: UTF-8 -*-
logger.info("Loading 11 objects to table uploads_upload...")
# fields: id, project, start_date, end_date, file, mimetype, user, owner_type, owner_id, company, contact_person, contact_role, upload_area, type, description, remark, needed
loader.save(create_uploads_upload(1,116,None,date(2015,5,17),u'',u'',5,pcsw_Client,116,None,None,None,'90',1,u'',u'',True))
loader.save(create_uploads_upload(2,116,None,date(2015,5,17),u'',u'',5,pcsw_Client,116,None,None,None,'90',2,u'',u'',True))
loader.save(create_uploads_upload(3,177,None,date(2015,5,27),u'',u'',5,pcsw_Client,177,None,None,None,'90',3,u'',u'',True))
loader.save(create_uploads_upload(4,177,None,date(2015,5,27),u'',u'',5,pcsw_Client,177,None,None,None,'90',4,u'',u'',True))
loader.save(create_uploads_upload(5,118,None,date(2015,6,6),u'',u'',5,pcsw_Client,118,None,None,None,'90',5,u'',u'',False))
loader.save(create_uploads_upload(6,118,None,date(2015,6,6),u'',u'',5,pcsw_Client,118,None,None,None,'90',6,u'',u'',False))
loader.save(create_uploads_upload(7,121,None,date(2014,4,22),u'',u'',7,pcsw_Client,121,None,None,None,'90',4,u'',u'',False))
loader.save(create_uploads_upload(8,121,None,date(2014,5,25),u'',u'',7,pcsw_Client,121,None,None,None,'90',4,u'',u'',True))
loader.save(create_uploads_upload(9,124,None,date(2015,3,18),u'',u'',7,pcsw_Client,124,None,None,None,'90',1,u'',u'',True))
loader.save(create_uploads_upload(10,124,None,date(2014,8,30),u'',u'',6,pcsw_Client,124,None,None,None,'90',2,u'',u'',True))
loader.save(create_uploads_upload(11,124,None,date(2014,6,1),u'',u'',9,pcsw_Client,124,None,None,None,'90',3,u'',u'',True))

loader.flush_deferred_objects()
