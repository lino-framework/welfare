# -*- coding: UTF-8 -*-
logger.info("Loading 3 objects to table cv_regime...")
# fields: id, name
loader.save(create_cv_regime(1,['Vollzeit', 'Temps-plein', 'Full-time']))
loader.save(create_cv_regime(2,['Teilzeit', 'Temps partiel', 'Part-time']))
loader.save(create_cv_regime(3,['Sonstige', 'Autre', 'Other']))

loader.flush_deferred_objects()
