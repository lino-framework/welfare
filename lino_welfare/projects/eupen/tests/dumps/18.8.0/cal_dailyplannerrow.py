# -*- coding: UTF-8 -*-
logger.info("Loading 3 objects to table cal_dailyplannerrow...")
# fields: id, seqno, designation, start_time, end_time
loader.save(create_cal_dailyplannerrow(1,1,['Vormittags', 'Avant-midi', 'AM'],None,time(12,0,0)))
loader.save(create_cal_dailyplannerrow(2,2,['Nachmittags', 'Apr\xe8s-midi', 'PM'],time(12,0,0),None))
loader.save(create_cal_dailyplannerrow(3,3,['Ganztags', 'Journ\xe9e enti\xe8re', 'All day'],None,None))

loader.flush_deferred_objects()
