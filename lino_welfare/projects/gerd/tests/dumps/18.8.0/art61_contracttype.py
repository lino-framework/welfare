# -*- coding: UTF-8 -*-
logger.info("Loading 1 objects to table art61_contracttype...")
# fields: id, ref, name, full_name, exam_policy, overlap_group, template
loader.save(create_art61_contracttype(1,None,['Art.61-Konvention', "Mise \xe0 l'emploi art.61", 'Art61 job supplyment'],u'',None,None,u''))

loader.flush_deferred_objects()
