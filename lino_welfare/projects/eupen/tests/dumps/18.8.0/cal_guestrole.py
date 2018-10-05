# -*- coding: UTF-8 -*-
logger.info("Loading 4 objects to table cal_guestrole...")
# fields: id, name
loader.save(create_cal_guestrole(1,['Kollege', 'Coll\xe8gue', 'Colleague']))
loader.save(create_cal_guestrole(2,['Besucher', 'Visiteur', 'Visitor']))
loader.save(create_cal_guestrole(3,['Vorsitzender', 'Pr\xe9sident', 'Chairman']))
loader.save(create_cal_guestrole(4,['Schriftf\xfchrer', 'Greffier', 'Reporter']))

loader.flush_deferred_objects()
