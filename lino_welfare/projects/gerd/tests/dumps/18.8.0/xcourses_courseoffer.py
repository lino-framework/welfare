# -*- coding: UTF-8 -*-
logger.info("Loading 3 objects to table xcourses_courseoffer...")
# fields: id, title, guest_role, content, provider, description
loader.save(create_xcourses_courseoffer(1,u'Deutsch f\xfcr Anf\xe4nger',None,1,230,u''))
loader.save(create_xcourses_courseoffer(2,u'Deutsch f\xfcr Anf\xe4nger',None,1,231,u''))
loader.save(create_xcourses_courseoffer(3,u'Fran\xe7ais pour d\xe9butants',None,2,231,u''))

loader.flush_deferred_objects()
