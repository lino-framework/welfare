# -*- coding: UTF-8 -*-
logger.info("Loading 2 objects to table xcourses_coursecontent...")
# fields: id, name
loader.save(create_xcourses_coursecontent(1,u'Deutsch'))
loader.save(create_xcourses_coursecontent(2,u'Franz\xf6sisch'))

loader.flush_deferred_objects()
