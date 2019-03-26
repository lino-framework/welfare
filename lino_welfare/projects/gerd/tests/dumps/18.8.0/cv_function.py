# -*- coding: UTF-8 -*-
logger.info("Loading 4 objects to table cv_function...")
# fields: id, name, remark, sector
loader.save(create_cv_function(1,['Kellner', 'Serveur', 'Waiter'],u'',5))
loader.save(create_cv_function(2,['Koch', 'Cuisinier', 'Cook'],u'',5))
loader.save(create_cv_function(3,['K\xfcchenassistent', 'Aide Cuisinier', 'Cook assistant'],u'',5))
loader.save(create_cv_function(4,['Tellerw\xe4scher', 'Plongeur', 'Dishwasher'],u'',5))

loader.flush_deferred_objects()
