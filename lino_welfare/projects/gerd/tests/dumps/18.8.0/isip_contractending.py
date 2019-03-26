# -*- coding: UTF-8 -*-
logger.info("Loading 4 objects to table isip_contractending...")
# fields: id, name, use_in_isip, use_in_jobs, is_success, needs_date_ended
loader.save(create_isip_contractending(1,u'Normal',True,True,False,False))
loader.save(create_isip_contractending(2,u'Alkohol',True,True,False,True))
loader.save(create_isip_contractending(3,u'Gesundheit',True,True,False,True))
loader.save(create_isip_contractending(4,u'H\xf6here Gewalt',True,True,False,True))

loader.flush_deferred_objects()
