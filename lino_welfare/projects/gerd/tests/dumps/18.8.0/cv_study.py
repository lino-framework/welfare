# -*- coding: UTF-8 -*-
logger.info("Loading 22 objects to table cv_study...")
# fields: id, start_date, end_date, country, city, zip_code, person, duration_text, language, school, state, remarks, type, education_level, content
loader.save(create_cv_study(1,date(1974,9,1),date(1986,6,30),None,None,u'',118,u'',None,u'',None,None,1,None,u'Abitur'))
loader.save(create_cv_study(2,date(1974,9,1),date(1986,6,30),None,None,u'',116,u'',None,u'',None,None,1,None,u'Abitur'))
loader.save(create_cv_study(3,date(2011,2,7),date(2011,3,7),u'CN',None,u'',118,u'',None,u'Leicester Islamic Academy',u'2',None,1,1,u''))
loader.save(create_cv_study(4,date(2011,2,9),date(2011,4,9),u'CO',None,u'',124,u'',None,u'Leicester Montessori School',u'0',None,2,2,u''))
loader.save(create_cv_study(5,date(2011,2,11),date(2011,5,11),u'CR',None,u'',127,u'',None,u'Sathya Sai School',u'1',None,3,3,u''))
loader.save(create_cv_study(6,date(2011,2,13),date(2011,8,13),u'CS',None,u'',128,u'',None,u'Stoneygate School',u'2',None,4,4,u''))
loader.save(create_cv_study(7,date(2011,2,15),date(2011,8,15),u'CSHH',None,u'',129,u'',None,u"St Crispin's School",u'0',None,5,5,u''))
loader.save(create_cv_study(8,date(2011,2,17),date(2011,11,17),u'CTKI',None,u'',130,u'',None,u'',u'1',None,6,1,u''))
loader.save(create_cv_study(9,date(2011,2,19),date(2012,2,19),u'CU',None,u'',132,u'',None,u'Leicester College',u'2',None,7,2,u''))
loader.save(create_cv_study(10,date(2011,2,21),date(2012,2,21),u'CV',None,u'',133,u'',None,u'Gateway College',u'0',None,8,3,u''))
loader.save(create_cv_study(11,date(2011,2,23),date(2013,2,23),u'CX',None,u'',137,u'',None,u'Regent College, Leicester',u'1',None,1,4,u''))
loader.save(create_cv_study(12,date(2011,2,25),date(2013,2,25),u'CY',None,u'',139,u'',None,u'Wyggeston and Queen Elizabeth I College',u'2',None,2,5,u''))
loader.save(create_cv_study(13,date(2011,2,27),date(2011,3,27),u'CZ',None,u'',141,u'',None,u'',u'0',None,3,1,u''))
loader.save(create_cv_study(14,date(2011,3,1),date(2011,5,1),u'DDDE',None,u'',142,u'',None,u'Darul Uloom Leicester',u'1',None,4,2,u''))
loader.save(create_cv_study(15,date(2011,3,3),date(2011,6,3),u'DE',None,u'',144,u'',None,u'Emmanuel Christian School, Leicester',u'2',None,5,3,u''))
loader.save(create_cv_study(16,date(2011,3,5),date(2011,9,5),u'DEDE',None,u'',146,u'',None,u'Leicester High School for Girls',u'0',None,6,4,u''))
loader.save(create_cv_study(17,date(2011,3,7),date(2011,9,7),u'DJ',None,u'',147,u'',None,u'Leicester Grammar School',u'1',None,7,5,u''))
loader.save(create_cv_study(18,date(2011,3,9),date(2011,12,9),u'DK',None,u'',152,u'',None,u'Leicester Islamic Academy',u'2',None,8,1,u''))
loader.save(create_cv_study(19,date(2011,3,11),date(2012,3,11),u'DM',None,u'',153,u'',None,u'Leicester Montessori School',u'0',None,1,2,u''))
loader.save(create_cv_study(20,date(2011,3,13),date(2012,3,13),u'DO',None,u'',155,u'',None,u'Sathya Sai School',u'1',None,2,3,u''))
loader.save(create_cv_study(21,date(2011,3,15),date(2013,3,15),u'DYBJ',None,u'',157,u'',None,u'Stoneygate School',u'2',None,3,4,u''))
loader.save(create_cv_study(22,date(2011,3,17),date(2013,3,17),u'DZ',None,u'',159,u'',None,u"St Crispin's School",u'0',None,4,5,u''))

loader.flush_deferred_objects()
