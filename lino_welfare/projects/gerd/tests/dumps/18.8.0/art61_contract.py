# -*- coding: UTF-8 -*-
logger.info("Loading 7 objects to table art61_contract...")
# fields: id, signer1, signer2, user, company, contact_person, contact_role, printed_by, client, language, applies_from, applies_until, date_decided, date_issued, user_asd, exam_policy, ending, date_ended, duration, reference_person, responsibilities, remark, type, job_title, status, cv_duration, regime, subsidize_10, subsidize_20, subsidize_30, subsidize_40, subsidize_50
loader.save(create_art61_contract(1,148,163,6,100,None,None,6,128,u'',date(2012,10,24),date(2014,10,23),None,None,None,None,None,date(2014,10,23),624,u'',None,u'',1,u'',None,None,None,True,False,False,False,False))
loader.save(create_art61_contract(2,148,163,4,101,None,None,7,139,u'',date(2012,11,23),date(2013,11,22),None,None,None,None,None,date(2013,11,22),312,u'',None,u'',1,u'',None,None,None,False,True,False,False,False))
loader.save(create_art61_contract(3,148,163,5,102,None,None,8,139,u'',date(2013,11,23),date(2014,11,23),None,None,None,None,None,date(2014,11,23),480,u'',None,u'',1,u'',None,None,None,True,True,False,False,False))
loader.save(create_art61_contract(4,148,163,6,103,None,None,9,152,u'',date(2012,12,23),date(2014,12,22),None,None,None,None,None,date(2014,12,22),624,u'',None,u'',1,u'',None,None,None,False,False,True,False,False))
loader.save(create_art61_contract(5,148,163,6,104,None,None,10,161,u'',date(2013,1,22),date(2014,1,21),None,None,None,None,None,date(2014,1,21),312,u'',None,u'',1,u'',None,None,None,True,False,False,False,False))
loader.save(create_art61_contract(6,148,163,4,100,None,None,11,161,u'',date(2014,1,22),date(2015,1,22),None,None,None,None,None,date(2015,1,22),480,u'',None,u'',1,u'',None,None,None,False,True,False,False,False))
loader.save(create_art61_contract(7,148,163,6,101,None,None,12,178,u'',date(2013,2,21),date(2015,2,20),None,None,None,None,None,date(2015,2,20),624,u'',None,u'',1,u'',None,None,None,True,True,False,False,False))

loader.flush_deferred_objects()
