# -*- coding: UTF-8 -*-
logger.info("Loading 4 objects to table cal_guestrole...")
# fields: id, ref, name
loader.save(create_cal_guestrole(1,None,['Kollege', 'Coll\xe8gue', 'Colleague']))
loader.save(create_cal_guestrole(2,None,['Besucher', 'Visiteur', 'Visitor']))
loader.save(create_cal_guestrole(3,None,['Vorsitzender', 'Pr\xe9sident', 'Chairman']))
loader.save(create_cal_guestrole(4,None,['Schriftf\xfchrer', 'Greffier', 'Reporter']))

loader.flush_deferred_objects()
