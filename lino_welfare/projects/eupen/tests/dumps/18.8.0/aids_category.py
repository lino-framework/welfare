# -*- coding: UTF-8 -*-
logger.info("Loading 3 objects to table aids_category...")
# fields: id, name
loader.save(create_aids_category(1,['Zusammenlebend', 'Cohabitant', 'Living together']))
loader.save(create_aids_category(2,['Alleinstehend', 'Persone isol\xe9e', 'Living alone']))
loader.save(create_aids_category(3,['Person mit Familienlasten', 'Personne qui cohabite avec une famille \xe0 sa charge', 'Person with family at charge']))

loader.flush_deferred_objects()
