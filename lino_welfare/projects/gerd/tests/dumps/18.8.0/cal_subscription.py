# -*- coding: UTF-8 -*-
logger.info("Loading 9 objects to table cal_subscription...")
# fields: id, user, calendar, is_hidden
loader.save(create_cal_subscription(1,6,3,False))
loader.save(create_cal_subscription(2,9,4,False))
loader.save(create_cal_subscription(3,5,5,False))
loader.save(create_cal_subscription(4,10,6,False))
loader.save(create_cal_subscription(5,4,7,False))
loader.save(create_cal_subscription(6,11,8,False))
loader.save(create_cal_subscription(7,2,9,False))
loader.save(create_cal_subscription(8,1,10,False))
loader.save(create_cal_subscription(9,3,11,False))

loader.flush_deferred_objects()
