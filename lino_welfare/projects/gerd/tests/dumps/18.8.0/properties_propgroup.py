# -*- coding: UTF-8 -*-
logger.info("Loading 3 objects to table properties_propgroup...")
# fields: id, name
loader.save(create_properties_propgroup(1,['Fachkompetenzen', 'Comp\xe9tences professionnelles', 'Skills']))
loader.save(create_properties_propgroup(2,['Sozialkompetenzen', 'Comp\xe9tences sociales', 'Soft skills']))
loader.save(create_properties_propgroup(3,['Hindernisse', 'Obstacles', 'Obstacles']))

loader.flush_deferred_objects()
