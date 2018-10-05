# -*- coding: UTF-8 -*-
logger.info("Loading 5 objects to table pcsw_persongroup...")
# fields: id, name, ref_name, active
loader.save(create_pcsw_persongroup(1,u'Auswertung',u'1',True))
loader.save(create_pcsw_persongroup(2,u'Ausbildung',u'2',True))
loader.save(create_pcsw_persongroup(3,u'Suchen',u'4',True))
loader.save(create_pcsw_persongroup(4,u'Arbeit',u'4bis',True))
loader.save(create_pcsw_persongroup(5,u'Standby',u'9',True))

loader.flush_deferred_objects()
