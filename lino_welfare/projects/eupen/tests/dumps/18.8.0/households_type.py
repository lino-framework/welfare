# -*- coding: UTF-8 -*-
logger.info("Loading 6 objects to table households_type...")
# fields: id, name
loader.save(create_households_type(1,['Ehepaar', 'Couple mari\xe9', 'Married couple']))
loader.save(create_households_type(2,['Geschiedenes Paar', 'Couple divorc\xe9', 'Divorced couple']))
loader.save(create_households_type(3,['Faktischer Haushalt', 'Cohabitation de fait', 'Factual household']))
loader.save(create_households_type(4,['Legale Wohngemeinschaft', 'Cohabitation l\xe9gale', 'Legal cohabitation']))
loader.save(create_households_type(5,['Getrennt', 'Isol\xe9', 'Isolated']))
loader.save(create_households_type(6,['Sonstige', 'Autre', 'Other']))

loader.flush_deferred_objects()
