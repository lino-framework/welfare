# -*- coding: UTF-8 -*-
logger.info("Loading 12 objects to table aids_refundconfirmation...")
# fields: id, created, start_date, end_date, user, company, contact_person, contact_role, printed_by, signer, state, client, granting, remark, language, doctor_type, doctor, pharmacy
loader.save(create_aids_refundconfirmation(1,dt(2018,12,16,8,8,9),date(2014,5,27),date(2014,6,26),4,None,None,None,4,5,u'01',139,44,u'',u'fr',7,215,200))
loader.save(create_aids_refundconfirmation(2,dt(2018,12,16,8,8,9),date(2014,5,27),date(2014,6,26),6,None,None,None,None,5,u'02',139,44,u'',u'fr',8,216,None))
loader.save(create_aids_refundconfirmation(3,dt(2018,12,16,8,8,9),date(2014,5,27),date(2014,6,26),9,None,None,None,None,5,u'01',139,44,u'',u'fr',9,217,None))
loader.save(create_aids_refundconfirmation(4,dt(2018,12,16,8,8,9),date(2014,5,27),date(2014,5,27),5,None,None,None,None,4,u'02',141,45,u'',u'en',10,219,201))
loader.save(create_aids_refundconfirmation(5,dt(2018,12,16,8,8,9),date(2014,5,27),date(2014,5,27),10,None,None,None,None,4,u'01',141,45,u'',u'en',7,215,None))
loader.save(create_aids_refundconfirmation(6,dt(2018,12,16,8,8,9),date(2014,5,27),date(2014,5,27),4,None,None,None,None,4,u'02',141,45,u'',u'en',8,216,None))
loader.save(create_aids_refundconfirmation(7,dt(2018,12,16,8,8,9),date(2014,5,28),None,6,None,None,None,None,5,u'01',142,46,u'',u'de',9,218,None))
loader.save(create_aids_refundconfirmation(8,dt(2018,12,16,8,8,9),date(2014,5,28),None,9,None,None,None,None,5,u'02',142,46,u'',u'de',10,219,None))
loader.save(create_aids_refundconfirmation(9,dt(2018,12,16,8,8,9),date(2014,5,28),None,5,None,None,None,None,5,u'01',142,46,u'',u'de',7,215,None))
loader.save(create_aids_refundconfirmation(10,dt(2018,12,16,8,8,9),date(2014,5,28),date(2015,5,28),10,None,None,None,None,4,u'02',144,47,u'',u'de',8,216,None))
loader.save(create_aids_refundconfirmation(11,dt(2018,12,16,8,8,9),date(2014,5,28),date(2015,5,28),4,None,None,None,None,4,u'01',144,47,u'',u'de',9,217,None))
loader.save(create_aids_refundconfirmation(12,dt(2018,12,16,8,8,9),date(2014,5,28),date(2015,5,28),6,None,None,None,None,4,u'02',144,47,u'',u'de',10,219,None))

loader.flush_deferred_objects()
