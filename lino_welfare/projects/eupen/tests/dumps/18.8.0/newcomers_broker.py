# -*- coding: UTF-8 -*-
logger.info("Loading 2 objects to table newcomers_broker...")
# fields: id, name
loader.save(create_newcomers_broker(1,u'Police'))
loader.save(create_newcomers_broker(2,u'Other PCSW'))

loader.flush_deferred_objects()
