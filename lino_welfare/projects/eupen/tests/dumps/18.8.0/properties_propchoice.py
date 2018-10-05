# -*- coding: UTF-8 -*-
logger.info("Loading 2 objects to table properties_propchoice...")
# fields: id, type, value, text
loader.save(create_properties_propchoice(1,3,u'1',['M\xf6bel', 'Meubles', 'Furniture']))
loader.save(create_properties_propchoice(2,3,u'2',['Hosting', 'Hosting', 'Web hosting']))

loader.flush_deferred_objects()
