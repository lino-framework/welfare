# -*- coding: UTF-8 -*-
logger.info("Loading 2 objects to table xcourses_courseprovider...")
# fields: company_ptr
loader.save(create_xcourses_courseprovider(230))
loader.save(create_xcourses_courseprovider(231))

loader.flush_deferred_objects()
