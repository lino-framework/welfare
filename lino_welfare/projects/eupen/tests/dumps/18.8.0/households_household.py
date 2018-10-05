# -*- coding: UTF-8 -*-
logger.info("Loading 14 objects to table households_household...")
# fields: partner_ptr, type
loader.save(create_households_household(232,1))
loader.save(create_households_household(233,2))
loader.save(create_households_household(234,3))
loader.save(create_households_household(235,4))
loader.save(create_households_household(236,5))
loader.save(create_households_household(237,6))
loader.save(create_households_household(254,1))
loader.save(create_households_household(255,2))
loader.save(create_households_household(256,1))
loader.save(create_households_household(257,1))
loader.save(create_households_household(270,1))
loader.save(create_households_household(271,2))
loader.save(create_households_household(272,2))
loader.save(create_households_household(273,1))

loader.flush_deferred_objects()
