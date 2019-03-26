# -*- coding: UTF-8 -*-
logger.info("Loading 4 objects to table cal_priority...")
# fields: id, name, ref
loader.save(create_cal_priority(1,['sehr dringend', 'tr\xe8s urgent', 'very urgent'],u'1'))
loader.save(create_cal_priority(2,['dringend', 'urgent', 'urgent'],u'3'))
loader.save(create_cal_priority(3,['normal', 'normal', 'normal'],u'5'))
loader.save(create_cal_priority(4,['nicht dringend', 'pas urgent', 'not urgent'],u'9'))

loader.flush_deferred_objects()
