# -*- coding: UTF-8 -*-
logger.info("Loading 12 objects to table cal_calendar...")
# fields: id, name, description, color
loader.save(create_cal_calendar(1,['Allgemein', 'G\xe9n\xe9ral', 'General'],u'',1))
loader.save(create_cal_calendar(2,['nicolas', '', ''],u'',1))
loader.save(create_cal_calendar(3,['alicia', '', ''],u'',2))
loader.save(create_cal_calendar(4,['caroline', '', ''],u'',3))
loader.save(create_cal_calendar(5,['hubert', '', ''],u'',4))
loader.save(create_cal_calendar(6,['judith', '', ''],u'',5))
loader.save(create_cal_calendar(7,['melanie', '', ''],u'',6))
loader.save(create_cal_calendar(8,['patrick', '', ''],u'',7))
loader.save(create_cal_calendar(9,['romain', '', ''],u'',8))
loader.save(create_cal_calendar(10,['rolf', '', ''],u'',9))
loader.save(create_cal_calendar(11,['robin', '', ''],u'',10))
loader.save(create_cal_calendar(12,['theresia', '', ''],u'',11))

loader.flush_deferred_objects()
