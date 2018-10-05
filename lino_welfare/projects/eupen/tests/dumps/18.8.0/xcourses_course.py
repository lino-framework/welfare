# -*- coding: UTF-8 -*-
logger.info("Loading 3 objects to table xcourses_course...")
# fields: id, offer, title, start_date, remark
loader.save(create_xcourses_course(1,1,u'',date(2014,6,21),u''))
loader.save(create_xcourses_course(2,2,u'',date(2014,6,7),u''))
loader.save(create_xcourses_course(3,3,u'',date(2014,6,7),u''))

loader.flush_deferred_objects()
